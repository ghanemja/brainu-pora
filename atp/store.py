"""
ATP store — seed access plus the two append-only logs.

  get_data()                      → the full ATP_DATA dict (seed, cached)
  append_hitl(event) -> event     → enrich with weightedDelta + ts + auditId,
                                     insert into the atp_hitl table
  read_hitl(limit=100)            → HITL log, latest first
  append_request(payload) -> req  → compute status via the compose matching
                                     rule, build pipeline stages, insert into
                                     the atp_requests table
  read_requests(limit=100)        → request log, latest first

Phase 1 (docs/HARDENING.md): both logs live in DAL tables (atp_hitl /
atp_requests — migration 002; append-only enforced by DB triggers) instead of
JSONL on ephemeral disk. Public shapes are unchanged: the same camelCase dict
keys (snake_case columns mapped back, JSON-text columns decoded) and read_*
still return latest-first lists. Legacy data/sessions/atp_hitl.jsonl /
atp_requests.jsonl are imported once into their empty table on first access,
then renamed to *.jsonl.imported (idempotent; the rename doubles as the
cross-process claim so rows land exactly once).

Phase 2 (docs/TENANCY.md): the four log functions take an OPTIONAL
`org_id` keyword (default `'org-demo'`, the bootstrap org every pre-tenancy
row belongs to — migration 005's column default). All table access is routed
through atp/tenant_db.py: writes stamp org_id, reads add `WHERE org_id =
:org`, and on Postgres every statement runs under `SET LOCAL app.org_id`
(RLS). Existing callers that don't pass org_id keep the exact pre-tenancy
behaviour against the demo org — signatures and returned shapes unchanged
(returned dicts do NOT grow an org key). Legacy JSONL imports land in
'org-demo'.
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from pathlib import Path

from sqlalchemy import inspect as sa_inspect

from . import tenant_db
from .seed import build_seed
from .tenant_db import DEFAULT_ORG

PROJECT_ROOT = Path(__file__).parent.parent
SESSIONS_DIR = PROJECT_ROOT / "data" / "sessions"
LEGACY_HITL_LOG = SESSIONS_DIR / "atp_hitl.jsonl"          # pre-Phase-1 log
LEGACY_REQUESTS_LOG = SESSIONS_DIR / "atp_requests.jsonl"  # pre-Phase-1 log

_DATA: dict | None = None


# ── Seed access ─────────────────────────────────────────────────────────────

def get_data() -> dict:
    """Return the full ATP_DATA payload. Cached — seed is pure data."""
    global _DATA
    if _DATA is None:
        _DATA = build_seed()
    return _DATA


# ── HITL reward log (§1 formula) ────────────────────────────────────────────

def append_hitl(event: dict, org_id: str = DEFAULT_ORG) -> dict:
    """Enrich a HITL reward signal and append it to the audit table.

    Input:  {agentId, layer, signal (+1|-1), reason, rater}
    Adds:   ts, weightedDelta, auditId
    Formula (§1): weightedDelta = signal × 0.2 × (weight[layer] / 0.26)
    The row is stamped with `org_id` (docs/TENANCY.md); the returned dict
    keeps its pre-tenancy shape.
    """
    data = get_data()
    weights = data["RL"]["rewardWeights"]

    layer = int(event.get("layer", 1))
    signal = int(event.get("signal", 0))
    weight = float(weights.get(f"L{layer}", 0.0))
    weighted_delta = round(signal * 0.2 * (weight / 0.26), 5)

    enriched = {
        "ts": event.get("ts") or _now(),
        "rater": event.get("rater", "anonymous"),
        "agentId": event.get("agentId"),
        "layer": layer,
        "signal": signal,
        "weightedDelta": weighted_delta,
        "reason": event.get("reason", ""),
        "auditId": f"audit-{uuid.uuid4().hex[:10]}",
    }
    _ensure_ready("atp_hitl", LEGACY_HITL_LOG, _HITL_COLS)
    tenant_db.insert_scoped("atp_hitl", _to_row(enriched, _HITL_COLS), org_id)
    return enriched


def read_hitl(limit: int = 100, org_id: str = DEFAULT_ORG) -> list[dict]:
    """Return `org_id`'s HITL log, latest first (capped at `limit`)."""
    _ensure_ready("atp_hitl", LEGACY_HITL_LOG, _HITL_COLS)
    return _read_latest("atp_hitl", _HITL_COLS, limit, org_id)


# ── Compose / train-to-order requests (§7.2) ────────────────────────────────

def append_request(payload: dict, org_id: str = DEFAULT_ORG) -> dict:
    """Create an expert-composition request from a wizard submission.

    Input:  {major, specialty, badgeIds, packId}
    Computes status against the seed agents with the same matching rule as
    the client-side `matchExperts`, builds the pipeline stages, appends to
    the request table (stamped with `org_id`), and returns the request.
    """
    data = get_data()
    badge_ids = list(payload.get("badgeIds") or [])
    pack_id = payload.get("packId")
    major = str(payload.get("major") or "")

    status, matched_agent_id, gap = _match(
        data, major, badge_ids, pack_id,
        # Wizard sends the concentration id as `specialty` (§7.2 payload);
        # accept an explicit concentrationId too for parity with matchExperts.
        payload.get("concentrationId") or payload.get("specialty") or None)
    pipeline = _pipeline_for(status)

    req = {
        "id": f"req-{uuid.uuid4().hex[:8]}",
        "ts": _now(),
        "major": major,
        "specialty": payload.get("specialty", ""),
        "badgeIds": badge_ids,
        "packId": pack_id,
        "layers": list(payload.get("layers") or []),
        "corpora": list(payload.get("corpora") or []),
        "status": status,
        "matchedAgentId": matched_agent_id,
        "gap": gap,
        "pipeline": pipeline,
        "resultAgentId": None,
    }
    _ensure_ready("atp_requests", LEGACY_REQUESTS_LOG, _REQUEST_COLS)
    tenant_db.insert_scoped("atp_requests", _to_row(req, _REQUEST_COLS), org_id)
    return req


def read_requests(limit: int = 100, org_id: str = DEFAULT_ORG) -> list[dict]:
    """Return `org_id`'s request log, latest first (capped at `limit`)."""
    _ensure_ready("atp_requests", LEGACY_REQUESTS_LOG, _REQUEST_COLS)
    return _read_latest("atp_requests", _REQUEST_COLS, limit, org_id)


# ── Matching rule (mirrors atp_data.js matchExperts) ────────────────────────

def _match(data: dict, major: str, badge_ids: list[str], pack_id, concentration_id=None):
    """Return (status, matchedAgentId, gap) for a composition request.

    Mirrors the client-side `matchExperts`: competencies come from the named
    concentration if `concentration_id` is given, otherwise the union of every
    concentration in the major.

    exact  = agent whose skills cover all of those competencies AND holds every
             requested badge AND (packId ? bound to pack policies : true)
    partial → gap analysis; else training (commission).
    """
    # Resolve the concentration tolerantly: by id ('18-C') or display name
    # ('Applied Mathematics', case-insensitive prefix). Unresolvable text
    # (free-form specialty) falls back to the whole-major union rather than
    # an empty competency set.
    want = str(concentration_id).strip().lower() if concentration_id else ""
    resolved = None
    majors = [m for m in data["COMPOSE"]["majors"] if str(m["course"]) == str(major)]
    if want:
        for m in majors:
            for cc in m["concentrations"]:
                nm = cc.get("name", "").lower()
                if cc["id"].lower() == want or nm == want or (nm and want.startswith(nm)):
                    resolved = cc["id"]
                    break
            if resolved:
                break

    comps: list[str] = []
    for m in majors:
        for cc in m["concentrations"]:
            if resolved and cc["id"] != resolved:
                continue
            comps.extend(cc.get("competencies", []))
    comps = list(dict.fromkeys(comps))  # de-dup, keep order

    pack_policies: list[str] = []
    if pack_id:
        pk = next((p for p in data["COMPOSE"]["packs"] if p["id"] == pack_id), None)
        if pk:
            pack_policies = list(pk.get("policyIds", []))

    exact: list[str] = []
    partials: list[dict] = []
    for a in data["AGENTS"]:
        if a.get("status") == "revoked":
            continue
        skill_names = {s["name"] for s in a.get("skills", [])}
        cert_ids = set(a.get("certIds", []))
        policy_ids = set(a.get("policyIds", []))

        covered = [c for c in comps if c in skill_names]
        missing = [c for c in comps if c not in skill_names]
        holds_badges = all(b in cert_ids for b in badge_ids)
        bound_pack = (not pack_id) or all(p in policy_ids for p in pack_policies)

        if comps and not missing and holds_badges and bound_pack:
            exact.append(a["id"])
        elif covered or any(b in cert_ids for b in badge_ids):
            partials.append({"agentId": a["id"], "covered": covered, "missing": missing})

    if exact:
        return "matched", exact[0], None

    if partials:
        partials.sort(key=lambda p: len(p["covered"]), reverse=True)
        covered = sorted({c for p in partials for c in p["covered"]})
        missing = [c for c in comps if c not in covered]
        gap = {"covered": covered, "missing": missing,
               "coveringAgentIds": [p["agentId"] for p in partials[:3]]}
        return "gap", None, gap

    return "training", None, None


def _pipeline_for(status: str) -> list[dict]:
    stages = ["requested", "corpus-mapped", "fine-tuning", "certifying", "listed"]
    if status == "matched":
        done = {s: True for s in stages}  # existing asset already covers it
    elif status == "gap":
        done = {"requested": True}
    else:  # training / commission
        done = {"requested": True, "corpus-mapped": True}
    now = _now()
    return [{"stage": s, "ts": now if done.get(s) else None, "done": bool(done.get(s))}
            for s in stages]


# ── DAL access (atp/tenant_db.py — migrations 002 + 005) ────────────────────

# dict key ↔ table column; declaration order = INSERT/SELECT column order.
_HITL_COLS = {
    "ts": "ts",
    "rater": "rater",
    "agentId": "agent_id",
    "layer": "layer",
    "signal": "signal",
    "weightedDelta": "weighted_delta",
    "reason": "reason",
    "auditId": "audit_id",
}
_REQUEST_COLS = {
    "id": "id",
    "ts": "ts",
    "major": "major",
    "specialty": "specialty",
    "badgeIds": "badge_ids",
    "packId": "pack_id",
    "layers": "layers",
    "corpora": "corpora",
    "status": "status",
    "matchedAgentId": "matched_agent_id",
    "gap": "gap",
    "pipeline": "pipeline",
    "resultAgentId": "result_agent_id",
}
_JSON_COLS = {"badge_ids", "layers", "corpora", "gap", "pipeline"}  # JSON text

_DB_LOCK = threading.Lock()
_DB_READY = False
_LEGACY_DONE: set[str] = set()
_ORDER: dict[str, str] = {}


def _engine():
    """Engine from the Phase-1 DAL. Imported lazily so this module (and
    `import api.server`) stays importable before atp/db.py lands; first log
    access also ensures migrations ran — the server runs them at startup too,
    and the runner is idempotent, so a second call is a no-op."""
    global _DB_READY
    from atp import db  # deferred: see docstring

    if not _DB_READY:
        with _DB_LOCK:
            if not _DB_READY:
                fn = (getattr(db, "ensure_migrations", None)
                      or getattr(db, "run_migrations", None)
                      or getattr(db, "migrate", None))
                if callable(fn):
                    try:
                        fn()
                    except TypeError:  # runner variant that takes the engine
                        fn(db.get_engine())
                _DB_READY = True
    return db.get_engine()


def _ensure_ready(table: str, legacy: Path, cols: dict) -> None:
    """Engine + migrations up, then the one-time legacy JSONL import."""
    _engine()
    _import_legacy_once(table, legacy, cols)


def _read_latest(table: str, cols: dict, limit: int, org_id: str) -> list[dict]:
    sel = ", ".join(cols.values())
    rows = tenant_db.scoped_query(
        org_id,
        f"SELECT {sel} FROM {table} WHERE org_id = :org"
        f" ORDER BY {_order_by(table)} LIMIT :n",
        {"org": org_id, "n": int(limit)})
    return [_to_dict(r, cols) for r in rows]


def _order_by(table: str) -> str:
    """Newest-first ordering. Prefer the monotonic surrogate key from
    migration 002 (`seq`), tolerate an integer `id` pk, then fall back to
    sqlite's implicit rowid / the ts column so reads survive DDL drift."""
    cached = _ORDER.get(table)
    if cached:
        return cached
    engine = _engine()
    info = {c["name"]: str(c["type"]).upper() for c in sa_inspect(engine).get_columns(table)}
    if "seq" in info:
        order = "seq DESC"
    elif "INT" in info.get("id", ""):
        order = "id DESC"
    elif engine.dialect.name == "sqlite":
        order = "rowid DESC"
    else:
        order = "ts DESC"
    _ORDER[table] = order
    return order


def _to_row(rec: dict, cols: dict) -> dict:
    """camelCase log dict → snake_case column dict (JSON cols dumped)."""
    row = {}
    for key, col in cols.items():
        v = rec.get(key)
        if col in _JSON_COLS and v is not None:
            v = json.dumps(v, default=str)
        row[col] = v
    return row


def _to_dict(row: dict, cols: dict) -> dict:
    """DB row (scoped_query dict) → the exact dict shape the JSONL logs used
    (camelCase keys — org_id is intentionally NOT part of the shape)."""
    rec = {}
    for key, col in cols.items():
        v = row[col]
        if col in _JSON_COLS and v is not None:
            v = json.loads(v)
        rec[key] = v
    return rec


def _import_legacy_once(table: str, legacy: Path, cols: dict) -> None:
    """One-time lazy migration of the pre-Phase-1 JSONL log.

    If the legacy file exists and the table holds no 'org-demo' rows, rename
    the file to *.jsonl.imported (the atomic rename is the cross-process
    claim — a racing worker gets FileNotFoundError and skips) and import its
    rows oldest-first so surrogate-key order matches insertion order.
    Pre-tenancy rows belong to the bootstrap org, so imports are stamped
    'org-demo' (docs/TENANCY.md leak surface #1). Idempotent: reruns see
    either no file or existing rows and do nothing.
    """
    if table in _LEGACY_DONE:
        return
    with _DB_LOCK:
        if table in _LEGACY_DONE:
            return
        if legacy.exists():
            count = tenant_db.scoped_query(
                DEFAULT_ORG,
                f"SELECT COUNT(*) AS n FROM {table} WHERE org_id = :org",
                {"org": DEFAULT_ORG})[0]["n"]
            if not count:
                claimed = legacy.with_name(legacy.name + ".imported")
                try:
                    legacy.rename(claimed)
                except FileNotFoundError:
                    claimed = None  # another worker claimed the import
                if claimed:
                    for line in claimed.read_text().splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except json.JSONDecodeError:
                            continue  # same tolerance the JSONL reader had
                        tenant_db.insert_scoped(
                            table, _to_row(rec, cols), DEFAULT_ORG)
        _LEGACY_DONE.add(table)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
