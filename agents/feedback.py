"""
Feedback ingestion — turns user signals into graph weight updates + agent
lifecycle events.

Three event kinds:

  register_prompt(prompt, session_id) → Hebbian boost on entities the user
                                        is asking about (small +δ)

  record_response(turn_id, spec_key, prompt, response, session_id)
                                      → log turn, parse citations, attach
                                        to the agent's history

  record_feedback(turn_id, score, comment) → big credit-assignment event:
    - parse the response's citations
    - apply +δ (positive feedback) or -δ (negative feedback) to graph edges
    - update agent's EWMA quality score (may trigger kill)
    - append to data/sessions/sessions.jsonl

Reward shaping:
  thumbs_up   → +1.0
  thumbs_down → -1.0
  neutral     →  0.0
  + per-turn cost of -0.02 baked into score_turn so rambling/empty turns
    decay quality even without explicit user feedback (call decay_idle())
"""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from .citations import parse as parse_citations, TurnCitations
from .lifecycle import ROSTER

PROJECT_ROOT = Path(__file__).parent.parent
SESSIONS_LOG = PROJECT_ROOT / "data" / "sessions" / "sessions.jsonl"
TURNS_LOG    = PROJECT_ROOT / "data" / "sessions" / "turns.jsonl"
SESSIONS_LOG.parent.mkdir(parents=True, exist_ok=True)


# ── Tunables ───────────────────────────────────────────────────────────────

POS_DELTA      = float(os.environ.get("RL_POS_DELTA", 0.20))
NEG_DELTA      = float(os.environ.get("RL_NEG_DELTA", -0.20))
HEBBIAN_DELTA  = float(os.environ.get("RL_HEBBIAN_DELTA", 0.05))
DECAY_RATE     = float(os.environ.get("RL_DECAY_RATE", 0.99))


# ── Public surface ────────────────────────────────────────────────────────

def new_session_id() -> str:
    return f"sess-{int(time.time())}-{str(uuid.uuid4())[:6]}"


def register_prompt(prompt: str, session_id: str | None = None) -> dict:
    """Hebbian boost: bump weights on entities the user just asked about.

    Logic: parse loose entities out of the prompt the same way we parse
    them from agent responses, then nudge their graph edges by HEBBIAN_DELTA.
    Cheap (no LLM call), and over time makes the brain "lean toward" the
    topics the user actually cares about.
    """
    cites = parse_citations(prompt)
    targets = cites.to_credit_targets()
    res = _apply_credit_safe(targets, HEBBIAN_DELTA)
    _append_log(SESSIONS_LOG, {
        "kind": "prompt",
        "ts": time.time(),
        "session_id": session_id or new_session_id(),
        "prompt": prompt[:1000],
        "n_targets": len(targets),
        "edges_updated": res.get("n_edges_updated", 0),
    })
    return {"targets": len(targets), **res}


def record_response(turn_id: str, spec_key: str, prompt: str, response: str,
                    session_id: str | None = None) -> dict:
    """Log a turn the agent took. Attaches to lifecycle citation history.

    Does NOT apply credit yet — that happens in record_feedback once the
    user (or implicit signal) tells us if it was good. Citations are kept
    as the eligibility-trace.
    """
    cites = parse_citations(response)
    targets = cites.to_credit_targets()
    ROSTER.record_turn(spec_key, turn_id, targets)
    _append_log(TURNS_LOG, {
        "kind": "turn",
        "ts": time.time(),
        "session_id": session_id,
        "turn_id": turn_id,
        "spec_key": spec_key,
        "prompt": prompt[:1000],
        "response": response[:4000],
        "n_arxiv": len(cites.arxiv),
        "n_wiki": len(cites.wiki),
        "n_tool": len(cites.tool),
        "n_entities": len(cites.entities),
        "citations": targets,
    })
    return {"turn_id": turn_id, "n_targets": len(targets)}


def record_feedback(turn_id: str, score: float, comment: str = "",
                    session_id: str | None = None) -> dict:
    """Apply user feedback to a previously logged turn.

    score ∈ [-1, +1] (typical: thumbs-up = +1, thumbs-down = -1).
    Looks up the turn in turns.jsonl, parses citations, applies credit,
    and updates the responsible agent's EWMA.
    """
    rec = _find_turn(turn_id)
    if rec is None:
        return {"error": f"turn_id {turn_id} not found"}

    spec_key = rec["spec_key"]
    targets  = rec.get("citations", [])

    # Map score to weight delta
    if score > 0:
        delta = POS_DELTA * score
    else:
        delta = NEG_DELTA * abs(score)
    credit = _apply_credit_safe(targets, delta)

    # Reward in [0,1] for EWMA
    reward = (score + 1) / 2
    life   = ROSTER.score_turn(spec_key, reward)

    _append_log(SESSIONS_LOG, {
        "kind": "feedback",
        "ts": time.time(),
        "session_id": session_id,
        "turn_id": turn_id,
        "spec_key": spec_key,
        "score": score,
        "comment": comment[:500],
        "delta_applied": delta,
        "edges_updated": credit.get("n_edges_updated", 0),
        "agent_state": {
            "ewma": life["ewma"],
            "bad_streak": life["bad_streak"],
            "killed": life["killed"],
            "reason": life["reason"],
            "lifespan_turns": life["lifespan_turns"],
        },
    })
    return {"turn_id": turn_id, **life,
            "edges_updated": credit.get("n_edges_updated", 0),
            "n_targets": len(targets)}


def decay_idle(rate: float | None = None) -> dict:
    """Run a graph-wide weight decay pass. Idempotent & cheap.

    Call once per session-end (or on a cron) to fade stale eligibility
    traces. Without this, weights would only ever grow.
    """
    try:
        from graph.weight_update import decay_all
    except ImportError:
        return {"ok": False, "error": "graph module missing"}
    return decay_all(rate or DECAY_RATE)


# ── Helpers ────────────────────────────────────────────────────────────────

def _apply_credit_safe(targets: list[tuple[str, str]], delta: float) -> dict:
    """Wrap apply_credit so a graph outage doesn't break feedback logging.

    Also writes to the local retrieval-prior store (rag.weights) so the
    BM25 ranker can use the learned signal even without FalkorDB online.
    """
    # Local prior store first — always succeeds, no network
    try:
        from rag.weights import bump as bump_local
        for kind, key in targets:
            if kind == "arxiv":
                paper = key.split("/", 1)[-1]
                bump_local("paper", paper, delta)
            elif kind == "wiki":
                bump_local("wiki", key, delta)
            elif kind == "entity":
                # Entities are graph-only; no chunk-level prior
                pass
    except Exception:
        pass

    # Graph (best-effort)
    try:
        from graph.weight_update import apply_credit
        return apply_credit(targets, delta)
    except Exception as e:
        return {"n_targets": len(targets), "n_edges_updated": 0,
                "errors": [f"{type(e).__name__}: {e}"]}


def _append_log(path: Path, rec: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def _find_turn(turn_id: str) -> dict | None:
    """Linear scan back through turns.jsonl. For typical session sizes
    (low thousands) this is fast enough; index later if needed."""
    if not TURNS_LOG.exists():
        return None
    # Read tail-first for recency
    with TURNS_LOG.open() as f:
        lines = f.readlines()
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("turn_id") == turn_id:
            return obj
    return None
