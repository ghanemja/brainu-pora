"""
ATP store — seed access plus the two append-only logs.

  get_data()                      → the full ATP_DATA dict (seed, cached)
  append_hitl(event) -> event     → enrich with weightedDelta + ts + auditId,
                                     append to data/sessions/atp_hitl.jsonl
  read_hitl(limit=100)            → HITL log, latest first
  append_request(payload) -> req  → compute status via the compose matching
                                     rule, build pipeline stages, append to
                                     data/sessions/atp_requests.jsonl
  read_requests(limit=100)        → request log, latest first

Both logs are append-only JSONL (auditable) under data/sessions/.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from .seed import build_seed

PROJECT_ROOT = Path(__file__).parent.parent
SESSIONS_DIR = PROJECT_ROOT / "data" / "sessions"
HITL_LOG = SESSIONS_DIR / "atp_hitl.jsonl"
REQUESTS_LOG = SESSIONS_DIR / "atp_requests.jsonl"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

_DATA: dict | None = None


# ── Seed access ─────────────────────────────────────────────────────────────

def get_data() -> dict:
    """Return the full ATP_DATA payload. Cached — seed is pure data."""
    global _DATA
    if _DATA is None:
        _DATA = build_seed()
    return _DATA


# ── HITL reward log (§1 formula) ────────────────────────────────────────────

def append_hitl(event: dict) -> dict:
    """Enrich a HITL reward signal and append it to the audit log.

    Input:  {agentId, layer, signal (+1|-1), reason, rater}
    Adds:   ts, weightedDelta, auditId
    Formula (§1): weightedDelta = signal × 0.2 × (weight[layer] / 0.26)
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
    _append(HITL_LOG, enriched)
    return enriched


def read_hitl(limit: int = 100) -> list[dict]:
    """Return the HITL reward log, latest first (capped at `limit`)."""
    return _read_tail(HITL_LOG, limit)


# ── Compose / train-to-order requests (§7.2) ────────────────────────────────

def append_request(payload: dict) -> dict:
    """Create an expert-composition request from a wizard submission.

    Input:  {major, specialty, badgeIds, packId}
    Computes status against the seed agents with the same matching rule as
    the client-side `matchExperts`, builds the pipeline stages, appends to
    the request log, and returns the request.
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
    _append(REQUESTS_LOG, req)
    return req


def read_requests(limit: int = 100) -> list[dict]:
    """Return the request log, latest first (capped at `limit`)."""
    return _read_tail(REQUESTS_LOG, limit)


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


# ── Helpers ──────────────────────────────────────────────────────────────────

def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _append(path: Path, rec: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def _read_tail(path: Path, limit: int) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    with path.open() as f:
        lines = f.readlines()
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
        if len(out) >= limit:
            break
    return out
