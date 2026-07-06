"""
ATP (Agentic Training Platform) API routes — see docs/ATP.md §5.

Mounted by api/server.py:
    from api.atp import router as atp_router
    app.include_router(atp_router)

Endpoints (all bearer-gated by the default auth middleware — api/auth.py):
    GET  /atp/data              — full ATP_DATA blob (T0 public seed)
    GET  /atp/agents            — agent roster
    GET  /atp/agents/{agent_id} — one agent profile (404 if unknown)
    GET  /atp/agents/{agent_id}/report.pdf — official report-card PDF
                                  (Phase 6; any authenticated role;
                                  live awards org-scoped; 404 if unknown)
    GET  /atp/certs             — certification catalog
    GET  /atp/certs/{cert_id}   — one cert (404 if unknown)
    GET  /atp/standard          — the ATP standard (label grammar + principles)
    GET  /atp/marketplace       — marketplace listings
    GET  /atp/hitl              — HITL reward log, latest first (org-scoped)
    POST /atp/hitl              — body {agentId, layer, signal, reason, rater}
                                  → appended (enriched) event  [admin|sme]
    GET  /atp/requests          — expert-composition requests (org-scoped)
    POST /atp/requests          — body {major, specialty, badgeIds, packId}
                                  → appended request           [admin|sme]

Certification engine (Phase 3 — docs/HARDENING.md):
    POST /atp/exams/run         — body {certId, candidateSpec?, agentId?,
                                  dryRun=true} → {jobId} (poll /jobs/{id};
                                  the job result is the award dict) [admin|sme]
    GET  /atp/awards            — org-scoped cert awards, latest first
    GET  /atp/evidence/{id}     — one signed evidence row (org-scoped; 404
                                  cross-tenant/absent — no existence oracle)
    GET  /atp/evidence/{id}/verify — {ok, sigValid, chainPosition}
    GET  /atp/chain/verify      — full evidence-chain verification for the org

Tenancy (Phase 2 — docs/TENANCY.md):
  * The seed catalog (data/agents/certs/standard/marketplace) is T0 public:
    read-only, identical for every org — never merged with tenant rows.
  * atp_hitl / atp_requests are T1 org-internal: reads and writes go through
    the store with org_id taken ONLY from the verified request state
    (request.state.org_id, set by the auth middleware from the JWT) — never
    from a client-supplied body/query value. Fallback 'org-demo' covers
    BU_AUTH_DISABLED dev mode and legacy single-admin tokens.
  * The demo seed rows (RL.hitlLog / EXPERT_REQUESTS) belong to 'org-demo'
    (TENANCY.md leak surface #1), so they are appended only for that org.
  * Writes require role admin|sme via api.auth.require_role; GET endpoints
    are open to any authenticated role (viewer included). Under
    BU_AUTH_DISABLED=1 the middleware runs every request as org-demo/admin,
    so dev mode passes every role gate (pre-Phase-2 behavior preserved).
"""

from __future__ import annotations

import json
import threading

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

# require_role(*roles) → FastAPI dependency that 403s when the verified
# session role is not in `roles` (401 when the middleware never ran).
from api.auth import require_role
from atp import store, tenant_db

router = APIRouter(prefix="/atp")


# ── Tenancy helpers ────────────────────────────────────────────────────────

def _org(request: Request) -> str:
    """Org for this request — ONLY from verified auth state (TENANCY.md §4
    layer 1). 'org-demo' when auth is disabled / legacy single-admin token."""
    return getattr(request.state, "org_id", None) or "org-demo"


# ── Read endpoints — T0 public seed ────────────────────────────────────────

@router.get("/data")
def atp_data():
    """Full ATP_DATA blob (same shape as window.ATP_DATA, minus JS helpers).
    T0 public seed — never merge tenant rows into it (TENANCY.md #9)."""
    return store.get_data()


@router.get("/agents")
def atp_agents():
    return {"agents": store.get_data().get("AGENTS", [])}


@router.get("/agents/{agent_id}")
def atp_agent(agent_id: str):
    for a in store.get_data().get("AGENTS", []):
        if a.get("id") == agent_id:
            return a
    raise HTTPException(404, f"agent {agent_id} not found")


@router.get("/agents/{agent_id}/report.pdf")
def atp_agent_report_pdf(agent_id: str, request: Request):
    """Official report-card PDF (Phase 6, docs/HARDENING.md).

    Any authenticated role — the PDF is built from the T0 public seed plus
    the CALLER ORG's live cert awards (org_id from verified request state
    only, TENANCY.md layer 1; atp/reportcard.py reads them through
    atp/tenant_db.py). Served as an attachment download; 404 for agents
    not in the seed roster. Deliberately NOT under /videos or /media —
    those prefixes are public-cached (TENANCY.md leak surface #4).
    """
    # Lazy import: reportlab stays an on-demand dependency — the server
    # boots (and every other route works) even if it is not installed.
    from atp import reportcard

    try:
        pdf = reportcard.build_report_card_pdf(agent_id, org_id=_org(request))
    except reportcard.UnknownAgentError:
        raise HTTPException(404, f"agent {agent_id} not found")
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="agent-{agent_id}-report-card.pdf"',
        },
    )


@router.get("/certs")
def atp_certs():
    return {"certs": store.get_data().get("CERTS", [])}


@router.get("/certs/{cert_id}")
def atp_cert(cert_id: str):
    for c in store.get_data().get("CERTS", []):
        if c.get("id") == cert_id:
            return c
    raise HTTPException(404, f"cert {cert_id} not found")


@router.get("/standard")
def atp_standard():
    return store.get_data().get("STANDARD", {})


@router.get("/marketplace")
def atp_marketplace():
    return store.get_data().get("MARKETPLACE", {"listings": []})


# ── HITL reward log — T1 org-internal ──────────────────────────────────────

@router.get("/hitl")
def atp_hitl_log(request: Request, limit: int = 100):
    """HITL reward log, latest first: the requesting org's live events
    (store.read_hitl already returns latest-first) followed by the seed audit
    history (stored oldest → newest, so reversed here). The seed rows belong
    to 'org-demo' only — other tenants never see them."""
    org = _org(request)
    live = store.read_hitl(limit=limit, org_id=org)
    seed = store.get_data().get("RL", {}).get("hitlLog", []) if org == "org-demo" else []
    return {"events": (live + list(reversed(seed)))[:limit]}


class HitlBody(BaseModel):
    agentId: str
    layer: int
    signal: int
    reason: str = ""
    rater: str = "anon"


@router.post("/hitl", dependencies=[Depends(require_role("admin", "sme"))])
def atp_hitl_submit(body: HitlBody, request: Request):
    """Append a human reward signal (role admin|sme). store.append_hitl
    computes weightedDelta per the RL weighting in docs/ATP.md §1 and logs it
    append-only under the caller's org."""
    if not 1 <= body.layer <= 7:
        raise HTTPException(400, "layer must be an integer in 1..7")
    if body.signal not in (1, -1):
        raise HTTPException(400, "signal must be 1 or -1")
    return store.append_hitl({
        "agentId": body.agentId,
        "layer":   body.layer,
        "signal":  body.signal,
        "reason":  body.reason,
        "rater":   body.rater,
    }, org_id=_org(request))


# ── Expert composition / train-to-order (docs/ATP.md §7) ───────────────────

@router.get("/requests")
def atp_requests(request: Request, limit: int = 100):
    """Expert-composition requests: the requesting org's live commissions
    (store.read_requests already returns latest-first) followed by the seed
    board — which belongs to 'org-demo' only."""
    org = _org(request)
    live = store.read_requests(limit=limit, org_id=org)
    seed = store.get_data().get("EXPERT_REQUESTS", []) if org == "org-demo" else []
    return {"requests": live + seed}


class ComposeBody(BaseModel):
    major: str
    specialty: str = ""
    badgeIds: list[str] = []
    packId: str | None = None


@router.post("/requests", dependencies=[Depends(require_role("admin", "sme"))])
def atp_request_submit(body: ComposeBody, request: Request):
    """Commission an expert (role admin|sme — viewers are read-only,
    TENANCY.md §Principals). store.append_request runs the matching rule
    against seed agents, builds the pipeline stages, and appends the request
    to the atp_requests table under the caller's org."""
    return store.append_request({
        "major":     body.major,
        "specialty": body.specialty,
        "badgeIds":  body.badgeIds,
        "packId":    body.packId,
    }, org_id=_org(request))


# ── Certification engine (Phase 3 — docs/HARDENING.md) ─────────────────────
#
# Exam runs execute in the background (agents/jobs — they call the candidate
# AND the judge model, 30-120s live) and write signed, chained rows into the
# append-only atp_evidence / atp_cert_awards tables (migration 002; org_id +
# RLS from 005). atp/exams.py + atp/signing.py own the exam/signing logic;
# these routes are the org-scoped HTTP surface over them. Reads go through
# atp/tenant_db.py ONLY (TENANCY.md layer 2) with org_id from verified
# request state — never from the client payload.

_DB_READY = False
_DB_LOCK = threading.Lock()
_EVIDENCE_COLNAMES: set[str] | None = None

# camelCase key ↔ snake_case column, same mapping idiom as atp/store.py.
_AWARD_COLS = {
    "id":            "id",
    "ts":            "ts",
    "agentId":       "agent_id",
    "certId":        "cert_id",
    "score":         "score",
    "sectionScores": "section_scores",
    "itemBreakdown": "item_breakdown",
    "evidenceIds":   "evidence_ids",
}
_AWARD_JSON_COLS = {"section_scores", "item_breakdown", "evidence_ids"}

_EVIDENCE_COLS = {
    "id":       "id",
    "ts":       "ts",
    "agentId":  "agent_id",
    "certId":   "cert_id",
    "kind":     "kind",
    "payload":  "payload",
    "sig":      "sig",
    "prevHash": "prev_hash",
}


def _ensure_db() -> None:
    """Engine + migrations up before the first direct tenant_db read here.
    run_migrations() is idempotent (schema_migrations bookkeeping), so this
    is a no-op when the server startup / atp.store already ran it."""
    global _DB_READY
    if _DB_READY:
        return
    with _DB_LOCK:
        if not _DB_READY:
            from atp import db
            db.run_migrations()
            _DB_READY = True


def _loads_maybe(v):
    """json.loads a JSON-text column, tolerating NULL / non-JSON text."""
    if v is None or not isinstance(v, str):
        return v
    try:
        return json.loads(v)
    except (json.JSONDecodeError, ValueError):
        return v


def _row_to_camel(row: dict, cols: dict, json_cols: set = frozenset()) -> dict:
    return {key: (_loads_maybe(row.get(col)) if col in json_cols else row.get(col))
            for key, col in cols.items()}


class ExamRunBody(BaseModel):
    certId: str
    candidateSpec: str | None = None   # agents/backend.get_backend spec string
    agentId: str | None = None
    dryRun: bool = True                # deterministic stub model (CI-safe)


@router.post("/exams/run", dependencies=[Depends(require_role("admin", "sme"))])
def atp_exam_run(body: ExamRunBody, request: Request):
    """Enqueue a certification exam run (role admin|sme).

    Returns {jobId}; poll GET /jobs/{jobId} — when status='done' the job
    result is the award dict (score, sectionScores, itemBreakdown,
    evidenceIds, passed…). The run itself enforces the ATP standard promises
    (docs/ATP.md §2) inside atp/exams.py: judge/candidate model-family
    separation and recorded seed/temperature/run-count reproducibility.
    dryRun (default true) uses the deterministic stub model — no live LLM.
    """
    from agents import jobs

    org = _org(request)
    cert_id = body.certId
    if not any(c.get("id") == cert_id
               for c in store.get_data().get("CERTS", [])):
        raise HTTPException(404, f"cert {cert_id} not found")

    candidate_spec = body.candidateSpec
    agent_id = body.agentId
    dry_run = body.dryRun

    def _task():
        from atp import exams
        return exams.run_exam(
            cert_id,
            candidate_spec,
            org_id=org,
            dry_run=dry_run,
            agent_id=agent_id,
        )

    job_id = jobs.submit("atp_exam", _task, org_id=org)
    # jobId is the documented key; job_id keeps BU_API.runJob() compatible.
    return {"jobId": job_id, "job_id": job_id}


@router.get("/awards")
def atp_awards(request: Request, limit: int = 100):
    """Org-scoped cert awards, latest first (any authenticated role)."""
    org = _org(request)
    _ensure_db()
    sel = ", ".join(_AWARD_COLS.values())
    rows = tenant_db.scoped_query(
        org,
        f"SELECT {sel} FROM atp_cert_awards"
        f" WHERE org_id = :org ORDER BY id DESC LIMIT :n",
        {"org": org, "n": int(limit)})
    return {"awards": [_row_to_camel(r, _AWARD_COLS, _AWARD_JSON_COLS)
                       for r in rows]}


def _evidence_where() -> str:
    """Row-match clause for a path id. The surrogate pk is an integer
    (BIGSERIAL / AUTOINCREMENT — migration 002) so match its text form; if
    the schema also carries a string business id (evidence_id), accept that
    too so award.evidenceIds resolve regardless of which form they use."""
    global _EVIDENCE_COLNAMES
    if _EVIDENCE_COLNAMES is None:
        from sqlalchemy import inspect as sa_inspect

        from atp import db
        _EVIDENCE_COLNAMES = {
            c["name"] for c in sa_inspect(db.get_engine()).get_columns("atp_evidence")}
    if "evidence_id" in _EVIDENCE_COLNAMES:
        return "(evidence_id = :eid OR CAST(id AS TEXT) = :eid)"
    return "CAST(id AS TEXT) = :eid"


def _evidence_row(org: str, evidence_id: str) -> dict | None:
    """One org-scoped evidence row (raw snake_case columns), or None."""
    _ensure_db()
    rows = tenant_db.scoped_query(
        org,
        f"SELECT * FROM atp_evidence"
        f" WHERE org_id = :org AND {_evidence_where()} LIMIT 1",
        {"org": org, "eid": str(evidence_id)})
    return rows[0] if rows else None


@router.get("/evidence/{evidence_id}")
def atp_evidence(evidence_id: str, request: Request):
    """One signed evidence row. Cross-tenant ids 404 with the SAME message
    as unknown ids — no existence oracle (TENANCY.md #6)."""
    row = _evidence_row(_org(request), evidence_id)
    if row is None:
        raise HTTPException(404, f"evidence {evidence_id} not found")
    return _row_to_camel(row, _EVIDENCE_COLS, {"payload"})


@router.get("/evidence/{evidence_id}/verify")
def atp_evidence_verify(evidence_id: str, request: Request):
    """Verify one evidence row: {ok, sigValid, chainPosition}.

    sigValid       — HMAC signature over the row's canonical payload checks
                     out (atp.signing.verify_row).
    chainPosition  — 1-based position of the row in the org's evidence chain.
    ok             — sigValid AND the whole org chain verifies (a valid row
                     inside a tampered ledger is NOT ok).
    """
    from atp import signing

    org = _org(request)
    row = _evidence_row(org, evidence_id)
    if row is None:
        raise HTTPException(404, f"evidence {evidence_id} not found")

    sig_valid = bool(signing.verify_row(row))
    position = tenant_db.scoped_query(
        org,
        "SELECT COUNT(*) AS n FROM atp_evidence"
        " WHERE org_id = :org AND id <= :rid",
        {"org": org, "rid": row["id"]})[0]["n"]
    chain = signing.verify_chain(org)
    chain_ok = bool(chain.get("ok")) if isinstance(chain, dict) else bool(chain)
    return {"ok": sig_valid and chain_ok,
            "sigValid": sig_valid,
            "chainPosition": position}


@router.get("/chain/verify")
def atp_chain_verify(request: Request):
    """Verify the caller org's whole evidence chain (sig + prev_hash links).
    Returns atp.signing.verify_chain's result dict (tamper-evidence promise,
    docs/HARDENING.md Phase 3)."""
    from atp import signing

    _ensure_db()
    result = signing.verify_chain(_org(request))
    return result if isinstance(result, dict) else {"ok": bool(result)}
