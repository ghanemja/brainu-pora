"""
Interactive podcast — pause, ask, resume.

Listener pauses an episode mid-play, types/speaks a question. Claude
generates a 1-3 turn interjection where the hosts answer (Host B explains,
Host A reacts), then the original script resumes.

Wire-up (frontend responsibility):
  - frontend tracks current_turn_index in the running script
  - on pause + question:
       inject = generate_interjection(script, turn_index, question)
       inject_audio = render_interjection_audio(inject)
       play inject_audio, then resume original from turn_index + 1

This module gives:
  - generate_interjection(script, turn_index, question) → list[Turn]
  - render_interjection_audio(turns, voice_backend) → Path (single concat mp3)
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .voices import synthesize

PROJECT_ROOT = Path(__file__).parent.parent
MEDIA_DIR = PROJECT_ROOT / "data" / "sessions" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


SYSTEM = """You are scripting a 1-3 turn interjection inside a podcast.

CONTEXT:
- The listener paused at TURN N and asked a question.
- You have the last 5 turns of the script for context.
- The hosts (A=curious learner, B=expert guide) will briefly address the
  question, then the original script resumes.

RULES:
- Open with HOST B acknowledging the question naturally ("good question —
  the short answer is...") then explaining concisely (1-3 sentences).
- Optionally HOST A reacts/paraphrases for the listener.
- Optionally HOST B closes with a "ok, back to where we were" handoff.
- TOTAL: 1-3 turns. No more.
- Each turn 15-40 words.

OUTPUT: valid JSON array only, no preface, no fence:
[
  {"speaker": "B", "text": "...", "visual": null, "beat": "interject"}
]"""


def generate_interjection(
    script: dict,
    turn_index: int,
    question: str,
    force: bool = False,
) -> list[dict] | None:
    """Generate 1-3 interjection turns answering `question` at turn_index."""
    turns = script.get("turns") or []
    if not turns:
        return None
    window_start = max(0, turn_index - 4)
    window = turns[window_start:turn_index + 1]
    ctx_lines = [f"{t.get('speaker','?')}: {t.get('text','')}" for t in window]

    user = (
        f"EPISODE: {script.get('title', '?')}\n"
        f"TOPIC: {script.get('topic', '?')}\n\n"
        f"RECENT TURNS:\n" + "\n".join(ctx_lines) + "\n\n"
        f"LISTENER QUESTION: {question}"
    )

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=SYSTEM,
            user=user,
            max_tokens=500,
            retries=2,
        )
    except Exception:
        return None

    parsed = _parse_json_array(raw)
    if not parsed:
        return None
    # Annotate
    for t in parsed:
        t["chapter"] = turns[turn_index].get("chapter", 0)
        t["interject"] = True
    return parsed


def render_interjection_audio(
    turns: list[dict],
    voice_backend: str | None = None,
) -> Path | None:
    """Concat audio for interjection turns into one mp3."""
    if not turns:
        return None
    key = hashlib.sha1(
        json.dumps([t.get("text", "") for t in turns]).encode()
    ).hexdigest()[:16]
    out = MEDIA_DIR / f"interject_{key}.mp3"
    if out.exists():
        return out

    try:
        from moviepy import AudioFileClip, concatenate_audioclips
    except ImportError:
        return None

    seg_paths = []
    for i, t in enumerate(turns):
        voice_id = "host_a" if t.get("speaker") == "A" else "host_b"
        p = MEDIA_DIR / f"interject_{key}_t{i}.mp3"
        synthesize(t.get("text", ""), voice_id=voice_id, out_path=p,
                   backend=voice_backend)
        if p.exists():
            seg_paths.append(p)

    if not seg_paths:
        return None
    try:
        clips = [AudioFileClip(str(p)) for p in seg_paths]
        full = concatenate_audioclips(clips)
        full.write_audiofile(str(out), logger=None)
    except Exception:
        return None
    return out if out.exists() else None


# ── Freeform interjection (for local/opaque podcasts w/o turn structure) ──

FREEFORM_SYSTEM = """You are scripting a 1-3 turn interjection inside a
podcast that you only have FREEFORM source material for (no turn list).

CONTEXT YOU GET:
- the source material the podcast was made from (paper / wiki / text)
- (optional) a short quote of what the listener just heard
- the listener's question

WHAT TO PRODUCE:
- HOST B opens with a 1-2 sentence direct answer, grounded in the source.
- HOST A optionally reacts ("oh ok, so the key is...").
- HOST B optionally closes with a handoff ("ok, back to where we were").
- TOTAL: 1-3 turns. Each 15-40 words. Natural conversational tone.

OUTPUT: valid JSON array only, no preface, no fence:
[
  {"speaker": "B", "text": "...", "beat": "interject"}
]"""


def generate_interjection_freeform(
    source_text: str,
    question: str,
    recent_quote: str = "",
) -> list[dict] | None:
    """Generate interjection turns from freeform source (no script needed)."""
    if not source_text or not question.strip():
        return None
    user = (
        f"SOURCE:\n{source_text[:6000]}\n\n"
        f"RECENT QUOTE: {recent_quote or '(unknown — listener paused mid-episode)'}\n"
        f"LISTENER QUESTION: {question.strip()}"
    )
    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=FREEFORM_SYSTEM,
            user=user,
            max_tokens=500,
            retries=2,
        )
    except Exception:
        return None
    parsed = _parse_json_array(raw)
    if not parsed:
        return None
    for t in parsed:
        t["interject"] = True
        t["chapter"] = 0
    return parsed


def _parse_json_array(raw: str) -> list[dict] | None:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if not m:
        return None
    try:
        data = json.loads(m.group(0))
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    return None
