"""
Demo script — exercise all four new modules end-to-end.

Run:
    cd ~/Documents/brain-university
    python3 scripts/demo_new_features.py

What it shows
-------------
  1. path_finder       — picks two real concepts from your brain graph
                          and walks the path between them, printing
                          each stop's rationale.
  2. podcast_render    — scaffolds a NotebookLM-style two-host dialog
                          (uses agents.podcast_script + agents.voices
                          when Claude / TTS keys are available;
                          falls back to a deterministic scaffold).
  3. lesson_to_scene   — converts a lesson dict to a SceneSpec the
                          worktree manim_renderer / browser SVG player
                          consume; reports the stack readiness.
  4. live_graph        — builds the event stream for a free-text
                          question, then renders an offline HTML
                          preview using 3d-force-graph. Tells you
                          where to open it.

The script is read-only — it doesn't render audio or video files; it
only exercises the planning side of each module. Once you confirm the
plans look right, kick off the heavier renderers from a UI.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ── Pretty printing ──────────────────────────────────────────────────────

def header(n: int, title: str) -> None:
    print()
    print("═" * 70)
    print(f" {n}. {title}")
    print("═" * 70)


def subhead(text: str) -> None:
    print()
    print(f"── {text} " + "─" * (66 - len(text)))


def wrap(text: str, indent: str = "    ") -> str:
    return textwrap.fill(
        text, width=72, initial_indent=indent, subsequent_indent=indent,
    )


def fail(msg: str) -> None:
    print(f"    ⚠  {msg}")


# ── Auto-pick two reasonable demo endpoints from the actual graph ────────

def pick_endpoints():
    """Return (a, b) — two real node names that are 4-8 hops apart in
    the user's brain graph. Returns (None, None) if the graph isn't
    available, so the demo can skip gracefully."""
    try:
        import networkx as nx
        from graph.clusters import build_clusters, load_graph
    except Exception as e:
        fail(f"could not import graph utilities: {e}")
        return None, None

    # Build clusters if needed; this also primes load_graph()
    build_clusters(force=False)
    G = load_graph()
    if G is None or G.number_of_nodes() == 0:
        fail("graph is empty — check that wiki/concepts/*.md exists")
        return None, None

    ccs = sorted(nx.connected_components(G), key=len, reverse=True)
    if not ccs:
        return None, None
    H = G.subgraph(ccs[0])
    nodes = list(H.nodes())

    import random
    random.seed(7)
    best = None
    for _ in range(200):
        a, b = random.sample(nodes, 2)
        try:
            p = nx.shortest_path(H, a, b)
            if 4 <= len(p) <= 8:
                best = (a, b)
                break
        except Exception:
            continue
    return best if best else (nodes[0], nodes[-1])


# ── Sample lesson used by podcast + manim demos ──────────────────────────

SAMPLE_LESSON = {
    "title":   "Backpropagation",
    "summary": ("Backpropagation is how neural networks learn from their "
                 "mistakes: each weight gets a share of the blame for the "
                 "final error, and a small nudge in the opposite direction."),
    "key_ideas": [
        "The forward pass produces a prediction by chaining layer outputs.",
        ("The backward pass uses the chain rule of calculus to attribute "
          "the error back to each weight, one layer at a time."),
        ("Gradient descent then moves each weight a small step in the "
          "direction that reduces the error most quickly."),
    ],
    "worked_example": (
        "For a 2-layer net with squared loss $L = (y - \\hat{y})^2$, the "
        "gradient with respect to a weight in the final layer is "
        "$\\partial L / \\partial w = 2 (y - \\hat{y}) \\cdot a$, where "
        "$a$ is the activation feeding into that weight."
    ),
    "engagement_question": (
        "Why does the order of operations matter when backpropagating "
        "through a recurrent network with shared weights across time steps?"
    ),
}


# ── Demos ────────────────────────────────────────────────────────────────

def demo_path_finder() -> None:
    header(1, "path_finder — concept-to-concept tour")

    a, b = pick_endpoints()
    if a is None:
        fail("skipping — no graph available")
        return

    print(f"    Picked two random connected concepts:")
    print(f"      from:  {a}")
    print(f"      to:    {b}")

    from agents import path_finder
    stops = path_finder.plan_path(a, b)
    print(f"\n    plan_path returned {len(stops)} stops:\n")
    for s in stops:
        marker = {
            "start":    "▶",
            "deepen":   "·",
            "bridge":   "⇄",
            "capstone": "★",
        }.get(s.kind, "·")
        print(f"    {marker}  #{s.order} [{s.kind:8}] {s.name:35}  "
              f"({s.cluster_name})")
        for line in textwrap.wrap(s.rationale, width=64):
            print(f"           {line}")
        print()


def demo_podcast() -> None:
    header(2, "podcast_render — NotebookLM-style two-host dialog")

    from agents import podcast_render
    turns = podcast_render.plan_dialog(SAMPLE_LESSON)
    print(f"    Sample lesson: {SAMPLE_LESSON['title']!r}")
    n_a = sum(1 for t in turns if t.speaker == "A")
    n_b = sum(1 for t in turns if t.speaker == "B")
    print(f"    Scaffold produced {len(turns)} turns "
          f"({n_a} host A / {n_b} host B)\n")
    for t in turns:
        tag = "HOST A" if t.speaker == "A" else "HOST B"
        beat = f"/{t.beat}" if t.beat else ""
        print(f"    [{tag}{beat}]")
        for line in textwrap.wrap(t.text, width=64):
            print(f"             {line}")
        print()

    print("    Stack readiness for actual audio rendering:")
    sr = podcast_render.stack_ready()
    for k, v in sr.items():
        if isinstance(v, dict):
            print(f"        - {k}:")
            for kk, vv in v.items():
                flag = "✓" if vv else "✗"
                print(f"            {flag} {kk}")
        else:
            flag = "✓" if v else "✗"
            print(f"        {flag} {k}")
    print()
    print("    To actually render an mp3, call:")
    print("        from agents.podcast_render import render")
    print("        path = render(lesson)   # or render(script_dict)")
    print("        # → data/sessions/media/podcast_<hash>.mp3")


def demo_video_manim() -> None:
    header(3, "lesson_to_scene — lesson → SceneSpec adapter")

    from agents import lesson_to_scene

    cases = [
        ("Math lesson (has LaTeX)", SAMPLE_LESSON),
        ("Tour-path lesson (graph walk)",
         {"title": "Tour", "tour_path": ["A", "B", "C", "D"]}),
        ("Plain prose lesson",
         {"title": "X", "key_ideas": ["just plain text, no math, no path"]}),
    ]
    for label, lesson in cases:
        is_cand = lesson_to_scene.is_manim_candidate(lesson)
        template = lesson_to_scene._pick_template(lesson)
        spec = lesson_to_scene.lesson_to_spec(lesson)
        beat_kinds = [b["kind"] for b in spec["beats"]]
        print(f"    {label}")
        print(f"        is_manim_candidate: {is_cand}")
        print(f"        template chosen:    {template}")
        print(f"        spec duration:      {spec['duration_s']:.1f}s")
        print(f"        beat kinds:         {beat_kinds[:8]}"
              f"{' …' if len(beat_kinds) > 8 else ''}")
        print()

    print("    Manim renderer availability:")
    try:
        from agents import manim_renderer
        print(f"        {'✓' if manim_renderer.manim_available() else '✗'} "
              f"`manim` CLI on PATH")
    except Exception as e:
        print(f"        ✗ manim_renderer import failed: {e}")
    print()
    print("    Without `manim` installed, lesson_to_scene.render() falls")
    print("    through to the existing PIL renderer in")
    print("    agents/video_generator.py — so you'll always get a video.")
    print()
    print("    SceneSpec output is also consumable by the browser SVG")
    print("    player in design/animation-player.jsx (no mp4 render needed")
    print("    for the React UI).")


def demo_live_graph() -> None:
    header(4, "live_graph — question → animated graph reveal")

    from agents import live_graph

    # Use a graph-theory question — this matches the bundled wiki corpus
    question = "how do tree decomposition and planar graphs relate to graph coloring?"
    events = live_graph.reveal(question)
    print(f"    Question: {question!r}")
    print(f"    Built {len(events)} events. First 8:\n")
    for ev in events[:8]:
        payload = {k: v for k, v in (ev.payload or {}).items()
                   if k in ("node", "panel", "a", "b", "text")}
        print(f"    {ev.t:5.2f}s  {ev.action:12} {payload}")
    print(f"    … plus {max(0, len(events)-8)} more.")

    out = live_graph.render_to_html(events, question)
    if out is None:
        fail("HTML preview render skipped — graph not available")
        return
    print()
    print(f"    Wrote self-contained HTML preview:")
    print(f"        {out}")
    print()
    print(f"    👉 Open it:")
    print(f"        open '{out}'")
    print()
    print(f"    You'll see your full 3D brain graph; nodes pulse and edges")
    print(f"    light up as the answer to the question unfolds.")


# ── Wrap-up ──────────────────────────────────────────────────────────────

def epilogue() -> None:
    print()
    print("═" * 70)
    print(" Done. Suggested next steps:")
    print("═" * 70)
    print(textwrap.dedent("""
        • Read ROADMAP.md for the prioritized phase plan.
        • Read docs/RECONCILE.md for what changed after the worktree merge.
        • Read docs/plans/01..04*.md for the next-up feature design docs.
        • The repo's UI direction is React (see design/*.jsx). The api/
          server is the backend the React UI calls — start it with:
              uvicorn api.server:app --reload --port 8000
          and the React screens in design/ can call into the agents
          modules through it.
        • To actually render audio/video, install the optional deps:
              pip install gtts pydub                  # podcast audio
              pip install manim                       # 3B1B-style scenes
              brew install ffmpeg                     # stitching
          Then set ELEVENLABS_API_KEY or OPENAI_API_KEY for premium TTS
          via agents.voices.
    """).rstrip())


# ── Main ─────────────────────────────────────────────────────────────────

def main() -> int:
    print("Brain University — new-feature demo")
    print(f"Repo: {PROJECT_ROOT}")
    print(f"Python: {sys.version.split()[0]}")

    demos = [
        ("path_finder",       demo_path_finder),
        ("podcast_generator", demo_podcast),
        ("video_manim",       demo_video_manim),
        ("live_graph",        demo_live_graph),
    ]
    for name, fn in demos:
        try:
            fn()
        except Exception as e:
            fail(f"{name} demo crashed: {e}")
            import traceback
            traceback.print_exc()

    epilogue()
    return 0


if __name__ == "__main__":
    sys.exit(main())
