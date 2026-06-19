"""
Lesson → SceneSpec adapter.

This module bridges Brain University's lesson dicts to the
SceneSpec JSON shape consumed by:
  - agents.manim_renderer  (SceneSpec → Manim .py → mp4)
  - design/animation-player.jsx  (SceneSpec → browser SVG render)

It is the *deterministic* counterpart of agents.animation_script, which
asks Claude to author a SceneSpec from a paper passage. Here we don't
ask Claude — we expand a lesson dict into a SceneSpec using three
templates picked by lesson shape:

  GraphWalkTemplate         lesson with a `tour_path` (list of node names)
  EquationDerivationTemplate lesson whose content contains LaTeX-y spans
  TitleAndIdeasTemplate     plain prose lesson (default)

SceneSpec emitted matches `agents.animation_script` exactly so any
renderer downstream is interchangeable.

Public:
  lesson_to_spec(lesson, *, template='auto') → dict   # SceneSpec
  render(lesson, *, template='auto', force=False) → Path | None
  is_manim_candidate(lesson) → bool
  available_templates() → list[str]
"""

from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "sessions" / "animation_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


LATEX_RE = re.compile(
    r"(\\frac|\\sum|\\int|\\sqrt|\\partial|\\nabla|\\lim|\\prod|"
    r"\$[^$]+\$|\\\([^)]+\\\)|\\\[[^]]+\\\])"
)


# ── Detection ────────────────────────────────────────────────────────────

def available_templates() -> list[str]:
    return ["auto", "graph_walk", "equation_derivation", "title_and_ideas"]


def is_manim_candidate(lesson: dict) -> bool:
    """True if Manim-style animation would meaningfully outperform plain
    PIL slides for this lesson. The fallback PIL renderer is still
    perfectly usable for prose lessons."""
    if lesson.get("media_style") == "manim":
        return True
    if lesson.get("tour_path"):
        return True
    blob = " ".join([
        lesson.get("summary") or "",
        lesson.get("worked_example") or "",
        " ".join(lesson.get("key_ideas") or []),
    ])
    return bool(LATEX_RE.search(blob))


def _pick_template(lesson: dict) -> str:
    if lesson.get("tour_path"):
        return "graph_walk"
    blob = " ".join([
        lesson.get("worked_example") or "",
        " ".join(lesson.get("key_ideas") or []),
    ])
    if LATEX_RE.search(blob):
        return "equation_derivation"
    return "title_and_ideas"


# ── Public: lesson → SceneSpec ───────────────────────────────────────────

def lesson_to_spec(lesson: dict, *, template: str = "auto") -> dict:
    """Expand a Brain-University lesson dict into a SceneSpec JSON.

    Returns a dict matching the shape documented in
    agents.animation_script (title / duration_s / voiceover / beats[]).
    """
    chosen = _pick_template(lesson) if template == "auto" else template
    if chosen == "graph_walk":
        return _graph_walk_spec(lesson)
    if chosen == "equation_derivation":
        return _equation_derivation_spec(lesson)
    return _title_and_ideas_spec(lesson)


# ── Templates ────────────────────────────────────────────────────────────

def _title_and_ideas_spec(lesson: dict) -> dict:
    """Title card → key-idea callouts → reflection prompt."""
    beats: list[dict] = []
    t = 0.0

    # Title card
    title_dur = 2.5
    beats.append({
        "t": t, "duration_s": title_dur, "kind": "title",
        "payload": {"text": lesson.get("title", "Lesson")},
    })
    t += title_dur

    # Summary as a callout
    if lesson.get("summary"):
        s_dur = max(3.0, min(7.0, 0.04 * len(lesson["summary"])))
        beats.append({
            "t": t, "duration_s": s_dur, "kind": "callout",
            "payload": {"text": lesson["summary"], "position": "center"},
        })
        t += s_dur

    # Key ideas one by one
    for i, idea in enumerate((lesson.get("key_ideas") or [])[:5], 1):
        # title card for "Key idea N"
        h_dur = 1.4
        beats.append({
            "t": t, "duration_s": h_dur, "kind": "title",
            "payload": {"text": f"Key idea {i}"},
        })
        t += h_dur
        body_dur = max(2.5, min(8.0, 0.045 * len(idea)))
        beats.append({
            "t": t, "duration_s": body_dur, "kind": "callout",
            "payload": {"text": idea, "position": "center"},
        })
        t += body_dur

    # Reflection
    if lesson.get("engagement_question"):
        beats.append({
            "t": t, "duration_s": 1.4, "kind": "title",
            "payload": {"text": "Reflect"},
        })
        t += 1.4
        beats.append({
            "t": t, "duration_s": 4.0, "kind": "callout",
            "payload": {"text": lesson["engagement_question"],
                         "position": "center"},
        })
        t += 4.0

    return _wrap_spec(lesson, beats, t)


def _equation_derivation_spec(lesson: dict) -> dict:
    """Title → step-by-step transformed equations."""
    beats: list[dict] = []
    t = 0.0

    title_dur = 2.5
    beats.append({
        "t": t, "duration_s": title_dur, "kind": "title",
        "payload": {"text": lesson.get("title", "Derivation")},
    })
    t += title_dur

    blob = (lesson.get("worked_example") or "") + "\n" + \
           "\n".join(lesson.get("key_ideas") or [])

    # Extract LaTeX-like spans
    spans = re.findall(r"\$([^$]+)\$|\\\(([^)]+)\\\)", blob)
    eqs = [a or b for a, b in spans][:6]

    if not eqs:
        # No equations found — fall through to title-and-ideas
        return _title_and_ideas_spec(lesson)

    prev = None
    for eq in eqs:
        if prev is None:
            beats.append({
                "t": t, "duration_s": 3.0, "kind": "equation",
                "payload": {"latex": eq},
            })
        else:
            beats.append({
                "t": t, "duration_s": 3.2, "kind": "transform_eq",
                "payload": {"from_latex": prev, "to_latex": eq, "label": ""},
            })
        t += 3.2
        prev = eq

    return _wrap_spec(lesson, beats, t)


def _graph_walk_spec(lesson: dict) -> dict:
    """Title → animated traversal of `tour_path` node sequence."""
    beats: list[dict] = []
    t = 0.0
    title_dur = 2.5
    beats.append({
        "t": t, "duration_s": title_dur, "kind": "title",
        "payload": {"text": lesson.get("title", "Path")},
    })
    t += title_dur

    path = lesson.get("tour_path") or []
    # Lay nodes out along an arc and emit geometric_step beats for each
    # node + line. The renderer's geometric_step fallback handles this
    # gracefully even if it doesn't yet support arc layout natively.
    import math
    n = len(path)
    radius = 4.5
    positions = []
    for i in range(n):
        theta = math.pi * (1.0 - (i / max(1, n - 1)))
        x = radius * math.cos(theta)
        y = radius * math.sin(theta) - 1.5
        positions.append((round(x, 2), round(y, 2)))

    # Add each node as a callout / highlight pair
    for i, (name, (x, y)) in enumerate(zip(path, positions)):
        beats.append({
            "t": t, "duration_s": 0.9, "kind": "geometric_step",
            "payload": {"svg_primitives": [
                {"kind": "circle", "cx": x, "cy": y, "r": 0.18,
                 "fill": "#7DD3FC"},
                {"kind": "label", "x": x, "y": y - 0.5,
                 "text": name.replace("_", " ")},
            ]},
        })
        t += 0.9
        if i > 0:
            px, py = positions[i - 1]
            beats.append({
                "t": t, "duration_s": 0.7, "kind": "geometric_step",
                "payload": {"svg_primitives": [
                    {"kind": "line", "x1": px, "y1": py, "x2": x, "y2": y,
                     "stroke": "#FBB036", "stroke_width": 4},
                ]},
            })
            t += 0.7

    return _wrap_spec(lesson, beats, t)


# ── Helpers ──────────────────────────────────────────────────────────────

def _wrap_spec(lesson: dict, beats: list[dict], duration: float) -> dict:
    return {
        "title":      lesson.get("title", "Lesson"),
        "duration_s": round(duration, 2),
        "voiceover":  _voiceover_from_lesson(lesson),
        "beats":      beats,
        # Provenance — useful for debugging which adapter produced this spec.
        "_source":    "lesson_to_scene",
        "_lesson_title": lesson.get("title", ""),
    }


def _voiceover_from_lesson(lesson: dict) -> str:
    """Build a flat narration script from the lesson fields. Useful when
    the renderer wants to dub voice over the visual beats."""
    parts: list[str] = []
    if lesson.get("title"):
        parts.append(f"Today's topic: {lesson['title']}.")
    if lesson.get("summary"):
        parts.append(lesson["summary"])
    for idea in (lesson.get("key_ideas") or [])[:5]:
        parts.append(idea)
    if lesson.get("worked_example"):
        parts.append("Here's a worked example. " + lesson["worked_example"])
    if lesson.get("engagement_question"):
        parts.append("Something to think about: " +
                      lesson["engagement_question"])
    return " ".join(parts)


# ── End-to-end convenience ───────────────────────────────────────────────

def render(lesson: dict, *, template: str = "auto",
           force: bool = False, voice: str = "auto",
           style: str = "dark", progress_cb=None) -> Path | None:
    """Convert lesson → SceneSpec → mp4 via manim_renderer.

    Falls back to the existing PIL slide renderer
    (`agents.video_generator.generate`) when Manim is unavailable, so
    this function always returns a video path if any backend can produce
    one.
    """
    spec = lesson_to_spec(lesson, template=template)

    # Try Manim first
    try:
        from agents import manim_renderer
        if manim_renderer.manim_available():
            if progress_cb:
                try:
                    progress_cb(("rendering_manim", 1, 1))
                except Exception:
                    pass
            out = manim_renderer.render(spec, force=force)
            if out and out.exists():
                return out
    except Exception:
        pass

    # Fallback: PIL slide renderer
    try:
        from agents import video_generator
        return video_generator.generate(
            lesson, voice=voice, style=style, force=force,
            progress_cb=progress_cb,
        )
    except Exception:
        return None
