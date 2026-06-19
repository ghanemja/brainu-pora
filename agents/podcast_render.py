"""
Podcast renderer — script dict → stitched mp3.

This is the **rendering half** of the podcast pipeline. The other half
is `agents.podcast_script.generate_script(...)`, which takes a topic +
source text and asks Claude to write a NotebookLM-style two-host
script. This module consumes that script (or a lightweight scaffold
when Claude is unreachable) and renders it to audio.

Pipeline
--------
    topic + source ─► podcast_script.generate_script()  [Claude]
                                  │
                                  ▼
                            script dict
                                  │
                                  ▼
       podcast_render.render(script)  ─►  voices.synthesize(per turn)
                                          │
                                          ▼
                              stitch + optional music bed
                                          │
                                          ▼
                          data/sessions/media/podcast_<hash>.mp3

Script shape supported (worktree-canonical from podcast_script.py):
    {
      "title": str,
      "summary": str,
      "duration_target_s": int,
      "chapters": [{"title": str, "summary": str}],
      "turns": [
        {"speaker": "A" | "B", "text": str, "visual": str|None,
         "beat": str|None, "chapter": int}
      ]
    }

Legacy shape also supported (lesson dict with title/summary/key_ideas):
internally we synthesize a quick scaffold via `plan_dialog` and feed
the same renderer.

Public:
  render(script_or_lesson, *, backend='auto', force=False) → Path | None
  plan_dialog(lesson) → list[Turn]    no-LLM fallback scaffold
  cached_path_for(script_or_lesson, *, backend='auto') → Path | None
  stack_ready() → dict[str, bool]
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MEDIA_DIR = PROJECT_ROOT / "data" / "sessions" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


# ── Internal turn shape used by the scaffold ─────────────────────────────

@dataclass
class Turn:
    speaker: str          # 'A' (curious learner) | 'B' (expert guide)
    text:    str
    visual:  str | None = None
    beat:    str | None = None
    chapter: int = 0

    def to_dict(self) -> dict:
        return {"speaker": self.speaker, "text": self.text,
                "visual": self.visual, "beat": self.beat,
                "chapter": self.chapter}


# ── Speaker → voice_id routing (matches voices.py logical voices) ────────

SPEAKER_TO_VOICE = {
    "A":        "host_a",
    "B":        "host_b",
    "narrator": "narrator",
}


# ── Scaffold (no-LLM fallback) ───────────────────────────────────────────

def plan_dialog(lesson: dict) -> list[Turn]:
    """Deterministic scaffold when podcast_script.generate_script can't
    reach Claude. Output is the same Turn shape as the worktree script."""
    title       = lesson.get("title", "today's topic")
    summary     = lesson.get("summary", "")
    key_ideas   = lesson.get("key_ideas") or []
    worked      = lesson.get("worked_example") or ""
    engagement  = lesson.get("engagement_question") or ""

    turns: list[Turn] = []
    turns.append(Turn("A",
        f"OK so we're talking about {title} — give me the one-sentence why-care.",
        beat="hook", chapter=0))
    turns.append(Turn("B",
        summary or f"{title} is one of those concepts that shows up everywhere "
                   f"once you start looking for it.",
        beat="explain", chapter=0))

    for i, idea in enumerate(key_ideas[:5], 1):
        turns.append(Turn("A",
            "Wait — what's the bedrock here?" if i == 1
            else "And the next layer?",
            beat="ask", chapter=1))
        turns.append(Turn("B", idea, beat="explain", chapter=1))

    if worked:
        turns.append(Turn("A",
            "Give me a concrete example — I want to see this in numbers.",
            beat="ask", chapter=2))
        turns.append(Turn("B", worked, beat="example", chapter=2))

    if engagement:
        turns.append(Turn("A",
            "Before we wrap — leave the listeners with something to chew on.",
            beat="ask", chapter=3))
        turns.append(Turn("B", engagement, beat="callback", chapter=3))

    turns.append(Turn("A",
        f"OK that's {title}. Thanks for breaking it down.",
        beat="callback", chapter=3))
    return turns


def _scaffold_script(lesson: dict) -> dict:
    """Wrap the scaffold in the worktree script shape."""
    turns = plan_dialog(lesson)
    return {
        "title":   lesson.get("title", "Untitled"),
        "summary": lesson.get("summary", ""),
        "duration_target_s": 180,
        "chapters": [
            {"title": "Intro",   "summary": "Open the topic."},
            {"title": "Ideas",   "summary": "Walk the key ideas."},
            {"title": "Example", "summary": "Worked example."},
            {"title": "Close",   "summary": "Reflect and sign off."},
        ],
        "turns": [t.to_dict() for t in turns],
        "topic": lesson.get("title", ""),
        "length": "short",
        "_scaffold": True,
    }


# ── Detect: script dict vs lesson dict ───────────────────────────────────

def _is_script(d: dict) -> bool:
    return bool(d.get("turns")) and isinstance(d["turns"], list)


def _ensure_script(d: dict) -> dict:
    """Accept either a script dict or a lesson dict; return a script dict."""
    if _is_script(d):
        return d
    # It's a lesson — try Claude first, fall back to scaffold
    try:
        from agents.podcast_script import generate_script, source_from_wiki
        src = source_from_wiki(d.get("title", ""))
        if not src:
            src = (d.get("summary") or "") + "\n\n" + "\n".join(
                d.get("key_ideas") or [])
        scr = generate_script(
            topic=d.get("title", "Untitled"),
            source_text=src or "(no source available)",
            length="short",
        )
        if scr:
            return scr
    except Exception:
        pass
    return _scaffold_script(d)


# ── Cache helpers ────────────────────────────────────────────────────────

def _cache_key(script: dict, backend: str) -> str:
    blob = json.dumps({
        "title":    script.get("title", ""),
        "n_turns":  len(script.get("turns") or []),
        "first_3":  [t.get("text", "")[:80]
                     for t in (script.get("turns") or [])[:3]],
        "backend":  backend,
        "scaffold": bool(script.get("_scaffold")),
    }, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def cached_path_for(script_or_lesson: dict, *,
                    backend: str = "auto") -> Path | None:
    script = _ensure_script(script_or_lesson)
    p = MEDIA_DIR / f"podcast_{_cache_key(script, backend)}.mp3"
    return p if p.exists() else None


# ── Audio synthesis per turn (delegated to voices.py) ────────────────────

def _synthesize_turn(turn: dict, *, backend: str, key: str,
                     idx: int) -> Path | None:
    text = (turn.get("text") or "").strip()
    if not text:
        return None
    speaker = turn.get("speaker", "A")
    voice_id = SPEAKER_TO_VOICE.get(speaker, "narrator")
    out = MEDIA_DIR / f"podcast_{key}_t{idx:02d}_{voice_id}.mp3"
    if out.exists():
        return out
    try:
        from agents import voices
        result = voices.synthesize(
            text, voice_id=voice_id,
            out_path=out,
            backend=None if backend == "auto" else backend,
        )
        return Path(result) if result else None
    except Exception:
        return None


# ── Main pipeline ────────────────────────────────────────────────────────

def render(script_or_lesson: dict, *, backend: str = "auto",
           force: bool = False, gap_seconds: float = 0.4,
           progress_cb=None) -> Path | None:
    """Render a podcast script (or fall-through lesson) to an mp3.

    Returns a Path to the rendered mp3, or None if no audio could be
    produced (e.g. no TTS backend installed)."""
    script = _ensure_script(script_or_lesson)
    if not script.get("turns"):
        return None

    key = _cache_key(script, backend)
    out_path = MEDIA_DIR / f"podcast_{key}.mp3"
    if out_path.exists() and not force:
        return out_path

    turns = script["turns"]
    audio_paths: list[Path] = []
    for i, t in enumerate(turns, 1):
        if progress_cb:
            try:
                progress_cb(("synth_turn", i, len(turns)))
            except Exception:
                pass
        p = _synthesize_turn(t, backend=backend, key=key, idx=i)
        if p and p.exists():
            audio_paths.append(p)

    if not audio_paths:
        return None

    if progress_cb:
        try:
            progress_cb(("stitching", 1, 1))
        except Exception:
            pass

    return _stitch(audio_paths, out_path, gap_seconds)


# ── Stitching (pydub → ffmpeg fallback) ──────────────────────────────────

def _stitch(paths: list[Path], out_path: Path,
            gap_seconds: float) -> Path | None:
    try:
        from pydub import AudioSegment
    except ImportError:
        return _stitch_with_ffmpeg(paths, out_path, gap_seconds)

    combined = AudioSegment.silent(duration=200)
    gap = AudioSegment.silent(duration=int(gap_seconds * 1000))
    for ap in paths:
        try:
            seg = AudioSegment.from_file(str(ap))
        except Exception:
            continue
        combined += seg + gap

    # Optional ducked music bed
    bed = MEDIA_DIR / "podcast_bed.mp3"
    if (os.environ.get("PODCAST_MUSIC", "").lower() in ("1", "true", "yes")
            and bed.exists()):
        try:
            music = AudioSegment.from_file(str(bed)) - 18  # quiet bed
            loops = int(len(combined) / max(1, len(music))) + 1
            extended = (music * loops)[:len(combined)]
            combined = combined.overlay(extended)
        except Exception:
            pass

    try:
        combined.export(str(out_path), format="mp3")
    except Exception:
        return None
    return out_path if out_path.exists() else None


def _stitch_with_ffmpeg(paths: list[Path], out_path: Path,
                         gap_seconds: float) -> Path | None:
    try:
        import subprocess
        list_file = out_path.with_suffix(".txt")
        with list_file.open("w") as f:
            for p in paths:
                f.write(f"file '{p.as_posix()}'\n")
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
               "-i", str(list_file), "-c", "copy", str(out_path)]
        subprocess.run(cmd, check=True, capture_output=True)
        try:
            list_file.unlink()
        except Exception:
            pass
        return out_path if out_path.exists() else None
    except Exception:
        return None


# ── Stack probe ──────────────────────────────────────────────────────────

def stack_ready() -> dict:
    out = {"pydub": False, "ffmpeg": False, "voices": False,
           "podcast_script": False}
    try:
        import pydub  # noqa
        out["pydub"] = True
    except ImportError:
        pass
    try:
        import imageio_ffmpeg
        if Path(imageio_ffmpeg.get_ffmpeg_exe()).exists():
            out["ffmpeg"] = True
    except Exception:
        pass
    try:
        from agents import voices  # noqa
        out["voices"] = True
    except Exception:
        pass
    try:
        from agents import podcast_script  # noqa
        out["podcast_script"] = True
    except Exception:
        pass
    # Forward the voices.py backend probe so callers see the whole stack
    try:
        from agents import voices as _v
        out["voices_backends"] = _v.available_backends()
    except Exception:
        pass
    return out
