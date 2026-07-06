"""
ATP (Agentic Training Platform) API routes — see docs/ATP.md §5.

Mounted by api/server.py:
    from api.atp import router as atp_router
    app.include_router(atp_router)

Endpoints (all bearer-gated by the default auth middleware — api/auth.py):
    GET  /atp/data              — full ATP_DATA blob (T0 public seed)
    GET  /atp/agents            — agent roster
    GET  /atp/agents/{agent_id} — one agent profile (404 if unknown)
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

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

# require_role(*roles) → FastAPI dependency that 403s when the verified
# session role is not in `roles` (401 when the middleware never ran).
from api.auth import require_role
from atp import store

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
