"""
ATP (Agentic Training Platform) API routes — see docs/ATP.md §5.

Mounted by api/server.py:
    from api.atp import router as atp_router
    app.include_router(atp_router)

Endpoints (all bearer-gated by the default auth middleware — api/auth.py):
    GET  /atp/data              — full ATP_DATA blob
    GET  /atp/agents            — agent roster
    GET  /atp/agents/{agent_id} — one agent profile (404 if unknown)
    GET  /atp/certs             — certification catalog
    GET  /atp/certs/{cert_id}   — one cert (404 if unknown)
    GET  /atp/standard          — the ATP standard (label grammar + principles)
    GET  /atp/marketplace       — marketplace listings
    GET  /atp/hitl              — HITL reward log, latest first
    POST /atp/hitl              — body {agentId, layer, signal, reason, rater}
                                  → appended (enriched) event
    GET  /atp/requests          — expert-composition requests (live + seed)
    POST /atp/requests          — body {major, specialty, badgeIds, packId}
                                  → appended request (status via matching rule)
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from atp import store

router = APIRouter(prefix="/atp")


# ── Read endpoints ─────────────────────────────────────────────────────────

@router.get("/data")
def atp_data():
    """Full ATP_DATA blob (same shape as window.ATP_DATA, minus JS helpers)."""
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


@router.get("/hitl")
def atp_hitl_log(limit: int = 100):
    """HITL reward log, latest first: live events (store.read_hitl already
    returns latest-first) followed by the seed audit history (stored
    oldest → newest, so reversed here). The seed rows keep the governance
    table populated before any live rewards land."""
    live = store.read_hitl(limit=limit)
    seed = store.get_data().get("RL", {}).get("hitlLog", [])
    return {"events": (live + list(reversed(seed)))[:limit]}


# ── HITL reward submission ─────────────────────────────────────────────────

class HitlBody(BaseModel):
    agentId: str
    layer: int
    signal: int
    reason: str = ""
    rater: str = "anon"


@router.post("/hitl")
def atp_hitl_submit(body: HitlBody):
    """Append a human reward signal. store.append_hitl computes weightedDelta
    per the RL weighting in docs/ATP.md §1 and logs it append-only."""
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
    })


# ── Expert composition / train-to-order (docs/ATP.md §7) ───────────────────

@router.get("/requests")
def atp_requests(limit: int = 100):
    """Expert-composition requests: live commissions (store.read_requests
    already returns latest-first) followed by the seed board."""
    live = store.read_requests(limit=limit)
    seed = store.get_data().get("EXPERT_REQUESTS", [])
    return {"requests": live + seed}


class ComposeBody(BaseModel):
    major: str
    specialty: str = ""
    badgeIds: list[str] = []
    packId: str | None = None


@router.post("/requests")
def atp_request_submit(body: ComposeBody):
    """Commission an expert. store.append_request runs the matching rule
    against seed agents, builds the pipeline stages, and appends the request
    to the atp_requests table."""
    return store.append_request({
        "major":     body.major,
        "specialty": body.specialty,
        "badgeIds":  body.badgeIds,
        "packId":    body.packId,
    })
