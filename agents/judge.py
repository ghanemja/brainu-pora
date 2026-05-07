"""
Auto-judge — score a single agent turn 0..1 without human feedback.

Two modes:
  heuristic (default, no API call) — cheap signals computed locally:
        - has the agent cited at least one source?  (presence)
        - did it propose a wiki edit?               (contribution)
        - confidence stated?                        (calibration)
        - response length within sane bounds?       (verbosity penalty)
        - does the response actually mention any of the prompt's key tokens?
          (relevance via simple BM25-style overlap)
        - did any tool call succeed?                (utility)
    Mix with fixed weights → score in [0, 1].

  llm (RL_AUTO_JUDGE=llm) — calls the SYNTHESIZER_MODEL with a tight rubric
    prompt to score on 5 axes (relevance, evidence, depth, calibration,
    novelty). Costs an extra Haiku/Sonnet call per turn, ~1¢. Use sparingly.

Public:
  score_turn(turn, problem)             → float in [0,1]
  judge_and_record(turn, problem, ...)  → also calls feedback.record_feedback
"""

from __future__ import annotations

import os
import re
from typing import Any


HEURISTIC_WEIGHTS = {
    "has_citation":   0.25,
    "has_proposal":   0.10,
    "confidence_set": 0.05,
    "length_ok":      0.10,
    "prompt_overlap": 0.30,
    "tool_succeeded": 0.10,
    "no_repetition":  0.10,
}


def _length_score(n_chars: int) -> float:
    """Bell-curve-ish: under 100 chars = bad, 800 = best, over 4000 = drop."""
    if n_chars < 100:    return 0.0
    if n_chars < 300:    return 0.5
    if n_chars < 1500:   return 1.0
    if n_chars < 3000:   return 0.6
    return 0.3


def _prompt_overlap(prompt: str, response: str) -> float:
    """Crude relevance: fraction of prompt content tokens (≥4 char) that
    appear at least once in the response."""
    p_toks = {t.lower() for t in re.findall(r"[a-zA-Z]{4,}", prompt)}
    if not p_toks:
        return 0.0
    r_lc = response.lower()
    hits = sum(1 for t in p_toks if t in r_lc)
    return hits / max(1, len(p_toks))


def _no_repetition(response: str) -> float:
    """Penalize obvious copy-paste loops. 1.0 = clean, 0.0 = repetitive."""
    if len(response) < 200:
        return 1.0
    # Take 50-char shingles, check for high duplication
    shingles = [response[i:i+50] for i in range(0, len(response) - 50, 25)]
    if not shingles:
        return 1.0
    uniq = len(set(shingles))
    return max(0.0, min(1.0, uniq / len(shingles)))


def heuristic_score(response: str, problem: str,
                     citations: list[str] | None = None,
                     wiki_proposal: Any = None,
                     confidence: str = "",
                     tool_calls: list[dict] | None = None) -> dict:
    """Compute heuristic 0..1 score with per-axis breakdown."""
    citations = citations or []
    tool_calls = tool_calls or []

    axes = {
        "has_citation":   1.0 if citations else 0.0,
        "has_proposal":   1.0 if wiki_proposal else 0.0,
        "confidence_set": 1.0 if confidence in ("low", "medium", "high") else 0.0,
        "length_ok":      _length_score(len(response)),
        "prompt_overlap": _prompt_overlap(problem, response),
        "tool_succeeded": 1.0 if any(not t.get("error") for t in tool_calls) else (
                           0.5 if not tool_calls else 0.0),
        "no_repetition":  _no_repetition(response),
    }
    score = sum(axes[k] * w for k, w in HEURISTIC_WEIGHTS.items())
    return {"score": round(score, 3), "axes": axes}


# ── LLM-based judge (optional, costs API call) ────────────────────────────

LLM_RUBRIC_SYSTEM = """You are an evidence-grounded evaluator scoring a
single specialist's turn in a multi-disciplinary engineering debate. Score
the turn on five axes from 0.0 to 1.0:

  relevance      — does it address the problem stated?
  evidence       — does it cite specific arXiv/wiki/tool sources?
  depth          — quantitative claims, not vague hand-waving?
  calibration    — does the confidence level match the evidence?
  novelty        — does it add something not already in the debate?

Output ONLY a JSON object: {"relevance":0.X, "evidence":0.X, "depth":0.X,
"calibration":0.X, "novelty":0.X, "overall":0.X, "rationale":"<one line>"}"""


def llm_score(response: str, problem: str, prior_turns: str = "") -> dict:
    """Call the synthesizer model to score a turn. Returns same shape as
    heuristic_score: {score, axes}. Falls back to heuristic on any error."""
    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        user = (
            f"PROBLEM:\n{problem}\n\n"
            f"PRIOR TURNS:\n{prior_turns[:2000]}\n\n"
            f"--- TURN TO SCORE ---\n{response[:3000]}"
        )
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=LLM_RUBRIC_SYSTEM,
            user=user,
            max_tokens=300,
            retries=2,
        )
        import json
        m = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
        if not m:
            return {"score": 0.5, "axes": {}, "error": "no JSON in judge output"}
        obj = json.loads(m.group(0))
        return {
            "score": float(obj.get("overall", 0.5)),
            "axes":  {k: float(v) for k, v in obj.items()
                      if k in {"relevance", "evidence", "depth", "calibration", "novelty"}},
            "rationale": obj.get("rationale", ""),
        }
    except Exception as e:
        return {"score": 0.5, "axes": {}, "error": f"{type(e).__name__}: {e}"}


# ── Single entry point ────────────────────────────────────────────────────

def score_turn(turn, problem: str, prior_turns: str = "") -> dict:
    """Score a single AgentTurn. Mode chosen by RL_AUTO_JUDGE env:
       'heuristic' (default) | 'llm' | 'hybrid' (avg of both)."""
    mode = os.environ.get("RL_AUTO_JUDGE", "heuristic").lower()

    h = heuristic_score(
        response=turn.raw_text,
        problem=problem,
        citations=turn.citations,
        wiki_proposal=turn.wiki_proposal,
        confidence=turn.confidence,
        tool_calls=turn.tool_calls,
    )

    if mode == "heuristic":
        return {**h, "mode": "heuristic"}
    if mode == "llm":
        l = llm_score(turn.raw_text, problem, prior_turns)
        return {**l, "mode": "llm", "heuristic": h}
    if mode == "hybrid":
        l = llm_score(turn.raw_text, problem, prior_turns)
        if "error" in l:
            return {**h, "mode": "hybrid_fallback_heur"}
        return {
            "score": round((h["score"] + l["score"]) / 2, 3),
            "axes": {**h["axes"], **l["axes"]},
            "mode": "hybrid",
        }
    return {**h, "mode": "heuristic"}


def judge_and_record(turn, problem: str, prior_turns: str = "",
                     session_id: str | None = None) -> dict:
    """Convenience: score a turn AND apply it as feedback in one call.

    Maps the 0..1 score onto the [-1, +1] feedback range:
        0.0 → -1.0
        0.5 →  0.0
        1.0 → +1.0
    """
    judgement = score_turn(turn, problem, prior_turns)
    score_01 = float(judgement.get("score", 0.5))
    feedback_score = 2 * score_01 - 1   # 0..1 → -1..+1

    try:
        from .feedback import record_feedback
        fb = record_feedback(
            turn_id=turn.turn_id,
            score=feedback_score,
            comment=f"auto-judge[{judgement.get('mode')}]",
            session_id=session_id,
        )
        return {**judgement, "feedback": fb, "mapped_score": feedback_score}
    except Exception as e:
        return {**judgement, "error": f"{type(e).__name__}: {e}"}
