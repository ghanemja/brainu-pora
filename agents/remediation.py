"""
Wrong-answer remediation — targeted micro-lesson on a specific quiz gap.

When a learner picks the wrong choice on a quiz question:
  - we know the question text, all choices, correct_idx, their pick
  - we know the parent lesson card
We ask Claude to produce a 3-paragraph remediation specific to the
misconception their wrong choice implies — not a generic re-explanation.

Output:
  {
    "diagnosis":  str,    # 1-2 sentence "you probably thought ..."
    "reteach":    str,    # 1 paragraph correct framing
    "check":      {"q": str, "a": str},   # follow-up check question
    "next_card":  str | None              # graph node to walk to next
  }
"""

from __future__ import annotations

import json
import re


SYSTEM = """You are a tutor diagnosing a specific misconception.

Given a quiz question, the correct answer, the wrong answer the learner
picked, and the lesson context, produce a remediation that:
  - Names the SPECIFIC misconception their wrong choice reveals (not generic).
  - Corrects it in one short paragraph (4-6 sentences).
  - Ends with one follow-up check question (open-ended, one sentence).
  - Optionally recommends one related graph node the learner should review
    BEFORE retrying.

OUTPUT: valid JSON only, no preface, no fence:
{
  "diagnosis": "<1-2 sentences naming the misconception>",
  "reteach":   "<one paragraph correcting it>",
  "check":     {"q": "<follow-up question>", "a": "<one-sentence expected answer>"},
  "next_card": "<graph node name or null>"
}"""


def remediate(
    *,
    lesson: dict,
    question: str,
    choices: list[str],
    correct_idx: int,
    picked_idx: int,
) -> dict | None:
    """Generate a misconception-specific remediation for a wrong answer."""
    if picked_idx == correct_idx:
        return None  # nothing to remediate
    if not (0 <= picked_idx < len(choices)) or not (0 <= correct_idx < len(choices)):
        return None

    user = (
        f"LESSON: {lesson.get('title', '')}\n"
        f"SUMMARY: {lesson.get('summary', '')}\n"
        f"KEY IDEAS:\n- " + "\n- ".join(lesson.get("key_ideas") or [])
        + f"\n\nQUIZ QUESTION: {question}\n"
        f"CORRECT ANSWER: {choices[correct_idx]}\n"
        f"LEARNER PICKED: {choices[picked_idx]}\n"
        f"OTHER CHOICES: " + " | ".join(
            c for i, c in enumerate(choices)
            if i not in {correct_idx, picked_idx}
        )
    )

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=SYSTEM,
            user=user,
            max_tokens=600,
            retries=2,
        )
    except Exception:
        return None

    return _parse_json(raw)


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
