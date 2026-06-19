"""
Animation script generator — 3Blue1Brown / Math Motion style.

Claude turns a paper passage (or podcast turn) into a JSON SceneSpec that
two renderers consume:
  - design/animation-player.jsx  — browser KaTeX + SVG + tween player
  - agents/manim_renderer.py     — emits a Manim CE .py file + runs CLI

SceneSpec shape:
{
  "title":      str,
  "duration_s": float,
  "voiceover":  str,                       # optional narration script
  "beats": [
    {
      "t":          float,                 # start in seconds
      "duration_s": float,
      "kind":       "title" | "equation" | "transform_eq" |
                    "vector_field" | "graph_plot" |
                    "geometric_step" | "callout" | "highlight",
      "payload":    { ...kind-specific }
    }
  ]
}

Payload by kind:
  title         {text}
  equation      {latex}
  transform_eq  {from_latex, to_latex, label}    # morph one eq into another
  vector_field  {vectors: [{x,y,dx,dy,color}], grid: bool}
  graph_plot    {x_label, y_label, curves: [{name, color, points:[[x,y],...]}]}
  geometric_step {svg_primitives: [{kind:'circle'|'line'|'polygon', ...}]}
  callout       {text, position: 'top'|'bottom'|'center'}
  highlight     {target_id, color}             # ring a previous element

Caching: data/sessions/animation_cache/<hash>.json
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "sessions" / "animation_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


SYSTEM = """You are an animation director in the style of 3Blue1Brown and
Math Motion. Given a paper passage or concept description, produce a JSON
SceneSpec for a 20-45 second animation that builds geometric / visual
intuition.

PRINCIPLES (lifted from 3b1b):
- One core idea per scene. Stack visual transformations to make it click.
- Equations should MORPH into the next form. Use transform_eq beats so the
  viewer sees Q K^T turn into Q_g K^T (etc.) rather than cutting.
- Show, then label. A vector field appears; THEN a callout names what it
  represents.
- Each beat 2-5 seconds. Total duration 20-45 seconds.
- Voiceover narration tracks the visuals; one sentence per beat.

OUTPUT: valid JSON only, no preface, no fence.

Available beat kinds + payloads:
  title         {"text": "..."}
  equation      {"latex": "..."}
  transform_eq  {"from_latex": "...", "to_latex": "...", "label": "..."}
  vector_field  {"vectors": [{"x":0,"y":0,"dx":1,"dy":2,"color":"#7DD3FC"}], "grid": true}
  graph_plot    {"x_label":"...", "y_label":"...",
                  "curves": [{"name":"...","color":"#FBB036","points":[[0,0],[1,1]]}]}
  geometric_step {"svg_primitives": [
                    {"kind":"circle","cx":50,"cy":50,"r":20,"stroke":"#F96167"},
                    {"kind":"line","x1":0,"y1":0,"x2":100,"y2":100,"stroke":"#7DD3FC"},
                    {"kind":"polygon","points":"10,10 90,10 50,90","fill":"#FBB03622"}
                  ]}
  callout       {"text":"...","position":"top"|"bottom"|"center"}
  highlight     {"target_id":"<id of earlier beat>", "color":"#F96167"}

Each beat may include a "id" string (so later beats can target it via
highlight). Times in seconds, accumulate naturally."""


def generate(passage: str, voiceover_hint: str = "", force: bool = False) -> dict | None:
    """Produce a SceneSpec for `passage`. Cached on hash."""
    if not passage or not passage.strip():
        return None
    key = hashlib.sha1((passage + "|" + voiceover_hint).encode()).hexdigest()[:16]
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists() and not force:
        try:
            return json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            pass

    user = f"PASSAGE:\n\n{passage[:6000]}"
    if voiceover_hint:
        user += f"\n\nVOICEOVER HINT (optional): {voiceover_hint}"

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=SYSTEM,
            user=user,
            max_tokens=3500,
            retries=2,
        )
    except Exception:
        return None

    parsed = _parse_json(raw)
    if not parsed or not parsed.get("beats"):
        return None
    # Best-effort: assign sequential ids if missing
    for i, beat in enumerate(parsed["beats"]):
        beat.setdefault("id", f"b{i}")
    cache_file.write_text(json.dumps(parsed, indent=2))
    return parsed


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
