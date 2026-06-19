"""
Live-graph reveal — turn a free-text question into a streaming sequence
of graph-animation events the UI can play back to make the brain graph
literally come alive while it answers.

Why this exists
---------------
Today the wiki_explorer 3D graph is static: it shows the whole brain at
once. The "wow" demo moment is the opposite: a learner types a question,
and they watch their question *land* on the graph — relevant nodes pulse,
edges light up, intermediate bridge concepts reveal one at a time, and a
mini-tour materialises in front of their eyes.

This module produces the event *stream*; rendering is the UI's job. The
event protocol below is renderer-agnostic so we can target the existing
3D graph (three-js / 3d-force-graph), a 2D D3 view, or a screen-recorder
that turns the sequence into a video.

Event protocol
--------------
Every event is a dict of the form:

    {"t": float,           # seconds since stream start
     "action": str,        # see ACTIONS below
     "payload": {...}}     # per-action shape

ACTIONS:
  "focus"          {node, zoom?}           camera/highlight on a node
  "pulse"          {node, color?, ttl?}    one-shot animated ring on a node
  "match"          {node, score}           mark node as a query match
  "edge_light"     {a, b, color?, ttl?}    animate an edge highlight
  "path_step"      {node, idx, of}         one stop in a materializing tour
  "label"          {node, text}            transient label overlay
  "narrate"        {text, voice?}          ask the player to speak this
  "wait"           {seconds}               idle pause
  "open_panel"     {panel, data}           UI overlay (e.g. show synthesis)

Public:
  reveal(question, *, vault_path=None) → list[Event]
  stream(question, ...) → iterator[Event]    (same content, yielded one at a time)
  render_to_html(events, out_path) → Path    (offline preview using 3d-force-graph)
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterator

PROJECT_ROOT = Path(__file__).parent.parent
PREVIEWS_DIR = PROJECT_ROOT / "data" / "sessions" / "live_graph_previews"
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)


# ── Event shape ──────────────────────────────────────────────────────────

@dataclass
class Event:
    t:       float
    action:  str
    payload: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


# ── Public ───────────────────────────────────────────────────────────────

def reveal(question: str, *, vault_path: str | None = None,
           narrate: bool = False) -> list[Event]:
    """Build the full event sequence for a single question. Returns a
    list so callers can serialize, persist, replay, or stream it.
    """
    events: list[Event] = []
    t = 0.0

    # 1. Resolve the question against the graph (matches + bridges + synthesis)
    try:
        from agents.proposal_responder import respond
        resp = respond(question, vault_path=vault_path)
    except Exception:
        resp = {"matched_concepts": [], "bridge_paths": [], "synthesis": ""}

    matched = resp.get("matched_concepts") or []
    bridges = resp.get("bridge_paths") or []
    synth   = resp.get("synthesis") or ""

    # 2. Opening beat: settle the camera
    events.append(Event(t, "open_panel", {
        "panel": "question",
        "data": {"text": question}
    }))
    t += 0.6

    if narrate:
        events.append(Event(t, "narrate",
                            {"text": f"Let me look that up. {question}"}))
        t += 2.5

    # 3. Pulse each matched concept in score order
    if matched:
        events.append(Event(t, "wait", {"seconds": 0.4}))
        t += 0.4
        for i, m in enumerate(matched[:8]):
            events.append(Event(t, "match", {
                "node":  m.get("name"),
                "score": m.get("score", 0.0),
            }))
            events.append(Event(t, "pulse", {
                "node":  m.get("name"),
                "color": "#F96167",         # coral (current location accent)
                "ttl":   1.2,
            }))
            events.append(Event(t, "label", {
                "node": m.get("name"),
                "text": m.get("label", m.get("name", "")),
            }))
            t += 0.35

        # Focus camera on the strongest match
        events.append(Event(t, "focus", {
            "node": matched[0].get("name"),
            "zoom": 1.4,
        }))
        t += 1.0

    # 4. Trace each bridge path step by step
    for b_idx, bridge in enumerate(bridges[:3]):
        path = bridge.get("path") or []
        if len(path) < 2:
            continue
        events.append(Event(t, "open_panel", {
            "panel": "bridge_intro",
            "data":  {
                "a": bridge.get("a"),
                "b": bridge.get("b"),
                "length": bridge.get("length"),
                "idx": b_idx + 1,
                "of":  min(3, len(bridges)),
            }
        }))
        t += 1.0
        for i in range(1, len(path)):
            u, v = path[i - 1], path[i]
            events.append(Event(t, "edge_light", {
                "a": u, "b": v, "color": "#7DD3FC", "ttl": 1.5,
            }))
            events.append(Event(t, "path_step", {
                "node": v,
                "idx":  i,
                "of":   len(path) - 1,
            }))
            events.append(Event(t, "pulse", {
                "node": v, "color": "#FBB036", "ttl": 1.0,
            }))
            t += 0.55

    # 5. Final synthesis panel
    if synth:
        events.append(Event(t, "wait", {"seconds": 0.6}))
        t += 0.6
        events.append(Event(t, "open_panel", {
            "panel": "synthesis",
            "data":  {"markdown": synth},
        }))
        if narrate:
            t += 0.4
            events.append(Event(t, "narrate", {"text": synth}))

    return events


def stream(question: str, *, vault_path: str | None = None,
           narrate: bool = False, realtime: bool = False) -> Iterator[Event]:
    """Same as `reveal` but yields events as an iterator.

    If `realtime=True`, sleep between events to match their `t` field —
    useful for backend-driven UIs that pull events from a websocket.
    """
    events = reveal(question, vault_path=vault_path, narrate=narrate)
    if not events:
        return
    start = time.monotonic()
    for ev in events:
        if realtime:
            target = start + ev.t
            now = time.monotonic()
            if target > now:
                time.sleep(target - now)
        yield ev


# ── Offline HTML preview ─────────────────────────────────────────────────

_PREVIEW_HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Brain University · Live Graph Preview</title>
<style>
  body  { margin:0; background:#0F1733; color:#FAFBFE;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif; }
  #graph { position: fixed; top:0; left:0; right:0; bottom:0; }
  #panel { position: fixed; right: 24px; top: 24px; width: 360px;
           background: rgba(15,23,51,0.85); border:1px solid #1E2761;
           padding: 16px 20px; border-radius: 10px; }
  #panel h2 { margin: 0 0 8px 0; font-size: 16px; color:#7DD3FC; text-transform: uppercase;
              letter-spacing: 0.05em; }
  #panel .q { font-size: 18px; color:#FAFBFE; line-height:1.4; }
  #panel .synth { font-size: 14px; color:#FAFBFE; line-height:1.5; margin-top: 12px; }
  #toolbar { position: fixed; left:24px; bottom:24px;
             background: rgba(15,23,51,0.85); border:1px solid #1E2761;
             padding: 10px 14px; border-radius: 8px; font-size: 13px; }
</style>
<script src="https://unpkg.com/3d-force-graph"></script>
</head><body>
  <div id="graph"></div>
  <div id="panel"><h2>Question</h2><div class="q"></div><div class="synth"></div></div>
  <div id="toolbar">Live-graph preview · auto-playing</div>
<script>
const EVENTS = __EVENTS__;
const GRAPH  = __GRAPH__;
const QUESTION = __QUESTION__;

document.querySelector('#panel .q').textContent = QUESTION;

const colors = { node:'#7DD3FC', match:'#F96167', bridge:'#FBB036', edge:'#1E2761' };

const G = ForceGraph3D()(document.getElementById('graph'))
  .backgroundColor('#0F1733')
  .nodeLabel(n => n.id.replace(/_/g,' '))
  .nodeColor(n => n._color || colors.node)
  .linkColor(l => l._color || colors.edge)
  .linkOpacity(0.3)
  .graphData(GRAPH);

function nodeById(id){ return GRAPH.nodes.find(n => n.id === id); }

function apply(ev){
  const p = ev.payload || {};
  if (ev.action === 'match' || ev.action === 'pulse'){
    const n = nodeById(p.node); if (n){ n._color = p.color || colors.match; }
  } else if (ev.action === 'edge_light'){
    const l = GRAPH.links.find(x =>
      (x.source.id === p.a && x.target.id === p.b) ||
      (x.source.id === p.b && x.target.id === p.a));
    if (l) l._color = p.color || colors.bridge;
  } else if (ev.action === 'focus'){
    const n = nodeById(p.node);
    if (n) G.cameraPosition({x: n.x*1.6, y: n.y*1.6, z: n.z*1.6}, n, 1500);
  } else if (ev.action === 'open_panel' && p.panel === 'synthesis'){
    document.querySelector('#panel .synth').textContent = p.data.markdown;
  }
  G.refresh();
}

let i = 0;
function tick(){
  if (i >= EVENTS.length) return;
  const ev = EVENTS[i++];
  apply(ev);
  const next = EVENTS[i];
  const delay = next ? Math.max(50, (next.t - ev.t) * 1000) : 1000;
  setTimeout(tick, delay);
}
setTimeout(tick, 600);
</script>
</body></html>
"""


def render_to_html(events: list[Event], question: str,
                   *, vault_path: str | None = None,
                   out_path: Path | None = None) -> Path | None:
    """Write a self-contained .html that replays the events against a
    live 3D-force-graph view of the brain. Open in a browser to preview.
    """
    try:
        from graph.clusters import load_graph
    except ImportError:
        return None
    G = load_graph(source="auto", vault_path=vault_path)
    if G is None or G.number_of_nodes() == 0:
        return None

    nodes = [{"id": n} for n in G.nodes()]
    links = [{"source": u, "target": v} for u, v in G.edges()]
    graph_blob = json.dumps({"nodes": nodes, "links": links})
    events_blob = json.dumps([e.to_dict() for e in events])
    question_blob = json.dumps(question)

    html = (_PREVIEW_HTML
            .replace("__EVENTS__", events_blob)
            .replace("__GRAPH__", graph_blob)
            .replace("__QUESTION__", question_blob))

    if out_path is None:
        ts = int(time.time())
        out_path = PREVIEWS_DIR / f"live_graph_{ts}.html"
    out_path.write_text(html)
    return out_path
