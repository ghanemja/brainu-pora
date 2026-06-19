"""
60-second audio briefings for lesson stops.

Pre-walk hook: before each stop on a planned tour, play a ~60s "here's
what's about to happen" intro. Builds anticipation + primes attention.

Source: a lesson card (curriculum.lesson_for) — distilled to one paragraph
by Claude (or a templated fallback) then TTS'd via voices.synthesize.

Cache: data/sessions/media/briefing_<hash>.mp3
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .voices import synthesize

PROJECT_ROOT = Path(__file__).parent.parent
MEDIA_DIR = PROJECT_ROOT / "data" / "sessions" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


BRIEF_SYSTEM = """You are a course-prep narrator. Given a lesson title and key
ideas, write a 90-110 word spoken briefing the listener will hear right
before the lesson. Tone: warm, curious, low-jargon.

Pattern:
  1) Sentence 1: name the topic + frame it as a question the listener will
     end up able to answer.
  2) Sentences 2-3: tease the key idea without giving the answer.
  3) Sentence 4: one concrete "by the end of this, you'll be able to ..." beat.

Output: plain text, no preface, no bullets, no headings. 90-110 words."""


def briefing_text(lesson: dict, force: bool = False) -> str:
    """Generate (or load cached) briefing text for a lesson card."""
    key = _key_text(lesson)
    cache = MEDIA_DIR / f"briefing_{key}.txt"
    if cache.exists() and not force:
        return cache.read_text()

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        user = (
            f"TITLE: {lesson.get('title', '')}\n"
            f"SUMMARY: {lesson.get('summary', '')}\n"
            f"KEY IDEAS:\n- "
            + "\n- ".join(lesson.get("key_ideas") or [])
        )
        text = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=BRIEF_SYSTEM,
            user=user,
            max_tokens=300,
            retries=2,
        )
    except Exception:
        text = _fallback(lesson)

    text = (text or "").strip()
    if not text:
        text = _fallback(lesson)
    cache.write_text(text)
    return text


def briefing_audio(lesson: dict, voice_id: str = "narrator",
                   force: bool = False) -> Path | None:
    """Generate audio briefing for a lesson. Returns mp3 path."""
    key = _key_audio(lesson, voice_id)
    out = MEDIA_DIR / f"briefing_{key}.mp3"
    if out.exists() and not force:
        return out
    text = briefing_text(lesson, force=force)
    return synthesize(text, voice_id=voice_id, out_path=out)


def _fallback(lesson: dict) -> str:
    title = lesson.get("title", "this topic")
    summary = lesson.get("summary", "")
    ideas = lesson.get("key_ideas") or []
    teaser = ideas[0] if ideas else ""
    return (
        f"Coming up next: {title}. By the end of the next two minutes you'll "
        f"have a working answer to why this matters and how it connects to "
        f"what you just learned. We'll touch on {teaser.lower() if teaser else 'the core idea'} "
        f"and walk through one concrete example. {summary} Stay curious — "
        f"this one rewards a slow read."
    )


def _key_text(lesson: dict) -> str:
    blob = json.dumps({
        "t": lesson.get("title", ""),
        "s": lesson.get("summary", ""),
        "k": lesson.get("key_ideas") or [],
    }, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def _key_audio(lesson: dict, voice_id: str) -> str:
    return _key_text(lesson) + "_" + voice_id
