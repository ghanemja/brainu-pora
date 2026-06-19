"""
Difficulty-level rewriter — ELI5 / undergrad / researcher.

Takes any lesson card and rewrites the summary / key_ideas / worked_example
at one of four target levels:
  eli5         no jargon, analogies, 6th-grade reading level
  undergrad    intro-textbook tone, defines terms, single-page proof OK
  grad         assumes core background, dense but readable
  researcher   no hand-holding, formalism, open-question framing

Cached per (lesson_key, level).
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "sessions" / "difficulty_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


LEVELS = {
    "eli5": "no jargon, sixth-grade reading level, lean on analogies and "
            "everyday examples. NO formal notation.",
    "undergrad": "intro-textbook tone. Define every technical term the "
                 "first time. Walk through derivations. One worked example "
                 "with numbers.",
    "grad": "assume core domain background. Dense but readable. Skip "
            "definitional asides. Surface non-obvious implications.",
    "researcher": "no hand-holding. Use precise formalism. Frame the topic "
                  "around open questions and disagreements in the literature.",
}


SYSTEM_TEMPLATE = """You are a tutor rewriting a lesson card for a specific
audience level.

LEVEL: {level} — {desc}

Preserve the lesson's structure (title, summary, key_ideas, worked_example,
engagement_question) but adapt language, depth, and notation to the level.

OUTPUT: valid JSON only, no preface, no fence:
{{
  "title":   "<unchanged>",
  "summary": "<rewritten>",
  "key_ideas": ["<rewritten>", ...],
  "worked_example": "<rewritten or null>",
  "engagement_question": "<rewritten>"
}}"""


def rewrite(lesson: dict, level: str = "undergrad",
            force: bool = False) -> dict:
    """Rewrite a lesson card at `level`. Returns a new dict (does not mutate)."""
    if level not in LEVELS:
        return dict(lesson)
    key = _cache_key(lesson, level)
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists() and not force:
        try:
            cached = json.loads(cache_file.read_text())
            merged = dict(lesson)
            merged.update(cached)
            merged["level"] = level
            return merged
        except json.JSONDecodeError:
            pass

    system = SYSTEM_TEMPLATE.format(level=level, desc=LEVELS[level])
    user = (
        f"ORIGINAL LESSON:\n"
        f"TITLE: {lesson.get('title', '')}\n"
        f"SUMMARY: {lesson.get('summary', '')}\n"
        f"KEY IDEAS:\n- " + "\n- ".join(lesson.get("key_ideas") or [])
        + f"\n\nWORKED EXAMPLE: {lesson.get('worked_example', '') or 'none'}\n"
        f"ENGAGEMENT QUESTION: {lesson.get('engagement_question', '') or 'none'}"
    )

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=system,
            user=user,
            max_tokens=1500,
            retries=2,
        )
        parsed = _parse_json(raw)
    except Exception:
        parsed = None

    if not parsed:
        out = dict(lesson)
        out["level"] = level
        out["level_warning"] = "rewrite failed; original returned"
        return out

    cache_file.write_text(json.dumps(parsed, indent=2))
    merged = dict(lesson)
    merged.update(parsed)
    merged["level"] = level
    return merged


def _cache_key(lesson: dict, level: str) -> str:
    blob = json.dumps({
        "t": lesson.get("title", ""),
        "s": lesson.get("summary", ""),
        "k": lesson.get("key_ideas") or [],
        "w": lesson.get("worked_example", ""),
        "l": level,
    }, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


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
