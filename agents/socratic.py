"""
Socratic mode — Claude probes "why" until concept locks.

Conversational tutoring loop:
  1. Start with a seed question about a graph node.
  2. Learner answers.
  3. Claude grades the answer (depth 0=shallow → 3=expert) AND emits
     either a follow-up "why/how" probe OR a "lock-in" closing summary.
  4. Loop until depth >= 3 OR max_turns hit.

State machine (caller persists between turns):
  {
    "node": str,
    "history": [{"role": "tutor"|"learner", "text": str, "depth": int}],
    "depth_achieved": int,
    "locked": bool,
  }

Public:
  start_session(node, seed_question=None) → SocraticState
  step(state, learner_answer)             → SocraticState (mutated)
"""

from __future__ import annotations

import json
import re
from typing import Any


SYSTEM = """You are a Socratic tutor. You never explain directly. You probe.

For each turn you receive:
  - the topic (a node in a knowledge graph)
  - the conversation so far (alternating tutor + learner turns)
  - the learner's most recent answer

You produce ONE of:
  - a follow-up PROBE that pushes the learner one level deeper (why? how?
    what would happen if X?). Use this when the learner's answer is correct
    but shallow.
  - a CORRECTION-PROBE that surfaces the specific gap WITHOUT giving the
    answer. Use this when the learner is wrong.
  - a LOCK-IN summary that names what they now understand AND what gap
    remains. Use this when depth_achieved >= 3 OR turn count >= 6.

Grade the learner's most recent answer 0-3:
  0  no engagement / "I don't know"
  1  pattern-matched the right vocabulary, no mechanism
  2  named a mechanism but missed an implication
  3  named mechanism AND implication; spotted a non-obvious consequence

OUTPUT: valid JSON only, no preface, no fence:
{
  "grade": 0,
  "kind": "probe" | "correction" | "lock_in",
  "text": "<your reply>",
  "depth_achieved": 0
}"""


def start_session(node: str, seed_question: str | None = None) -> dict:
    seed = seed_question or (
        f"Without looking it up: in plain English, what is {node} actually for? "
        f"And what's the easiest way to confuse it with something else?"
    )
    return {
        "node": node,
        "history": [{"role": "tutor", "text": seed, "depth": 0}],
        "depth_achieved": 0,
        "locked": False,
        "turns": 0,
    }


def step(state: dict, learner_answer: str, max_turns: int = 6) -> dict:
    state["history"].append({
        "role": "learner",
        "text": learner_answer,
        "depth": state.get("depth_achieved", 0),
    })
    state["turns"] = state.get("turns", 0) + 1

    convo_lines = [
        f"{h['role'].upper()}: {h['text']}"
        for h in state["history"][-10:]
    ]
    user_msg = (
        f"TOPIC: {state['node']}\n"
        f"TURN: {state['turns']} / {max_turns}\n"
        f"PRIOR DEPTH: {state['depth_achieved']}\n\n"
        + "\n".join(convo_lines)
    )

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=SYSTEM,
            user=user_msg,
            max_tokens=500,
            retries=2,
        )
        parsed = _parse_json(raw) or {}
    except Exception:
        parsed = {}

    if not parsed:
        # graceful fallback — single probe
        parsed = {
            "grade": 1,
            "kind": "probe",
            "text": "Push further: what would break if this weren't true?",
            "depth_achieved": state["depth_achieved"],
        }

    state["depth_achieved"] = max(
        state["depth_achieved"], int(parsed.get("depth_achieved", 0))
    )
    state["history"].append({
        "role": "tutor",
        "text": parsed.get("text", ""),
        "depth": state["depth_achieved"],
        "kind": parsed.get("kind", "probe"),
        "grade": parsed.get("grade", 0),
    })

    if parsed.get("kind") == "lock_in" or state["turns"] >= max_turns \
            or state["depth_achieved"] >= 3:
        state["locked"] = True

    return state


def _parse_json(raw: str) -> dict | None:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
