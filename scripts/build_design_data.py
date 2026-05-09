"""
Emit `design/data.js` from the live Python data layer so the React UI
that Claude design built consumes our actual graph instead of mock data.

The output preserves the contract the JSX components expect:
  window.BU_DATA = { CLUSTERS, NODES, EDGES, FOUNDATION_PICKS,
                      LESSONS, BRIDGE_PAIRS, PROPOSE_EXAMPLES, TOURS,
                      lessonFor, planTour, adjacencyOf, bridgesFrom }

Strategy:
  - Pull top N Louvain clusters from graph/clusters.py
  - Pick top per-cluster nodes by degree (8 per cluster, capped overall)
  - Edges = induced subgraph on the picked nodes (keeps the JS viz fast)
  - FOUNDATION_PICKS via graph/foundations.recommend()
  - PROPOSE_EXAMPLES via agents/proposal_responder.respond() over a few seed prompts
  - LESSONS pre-rendered via agents/curriculum.lesson_for() (fast mode by default)
  - TOURS pre-planned for every FOUNDATION_PICK via agents/lesson_plan.plan_tour()

The design's `data.js` (mock) is preserved at `design/data.mock.js` so we
can diff and so the UI can fall back to mock if we run with --no-real.

Run:
    python3 scripts/build_design_data.py
    python3 scripts/build_design_data.py --max-clusters 6 --per-cluster 8
    python3 scripts/build_design_data.py --rich-lessons   # uses Claude
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DESIGN_DIR = PROJECT_ROOT / "design"
OUT_PATH = DESIGN_DIR / "data.js"
MOCK_BACKUP = DESIGN_DIR / "data.mock.js"


# ── Cluster-color palette (matches DESIGN_BRIEF.md guidance) ──────────────

PALETTE = [
    {"color": "#7641eb", "emoji": "⌬"},  # purple
    {"color": "#2ec4b6", "emoji": "Φ"},  # teal
    {"color": "#f59e0b", "emoji": "∮"},  # amber
    {"color": "#1e6fa8", "emoji": "⚙"},  # navy-blue
    {"color": "#84cc16", "emoji": "✺"},  # green
    {"color": "#c5a3ff", "emoji": "✦"},  # lavender
    {"color": "#F96167", "emoji": "❉"},  # coral
    {"color": "#FBB036", "emoji": "✱"},  # gold
    {"color": "#7DD3FC", "emoji": "❖"},  # sky
    {"color": "#9B59B6", "emoji": "✥"},
    {"color": "#16A085", "emoji": "❅"},
    {"color": "#E67E22", "emoji": "✲"},
]


def _humanize(s: str) -> str:
    return s.replace("_", " ").strip()


# ── Builders ──────────────────────────────────────────────────────────────

def build_clusters(clusters_full, max_clusters):
    """Take top-N largest clusters and reindex to 0..N-1 for JS consumption."""
    picked = sorted(clusters_full, key=lambda c: len(c.members), reverse=True)[:max_clusters]
    out = []
    for new_idx, c in enumerate(picked):
        pal = PALETTE[new_idx % len(PALETTE)]
        # Build a one-line blurb from the cluster's top concepts
        top_names = [n for n, _ in c.top_nodes[:4]]
        blurb = ", ".join(_humanize(t) for t in top_names) + "."
        out.append({
            "id":     new_idx,
            "name":   _humanize(c.name),
            "color":  pal["color"],
            "emoji":  pal["emoji"],
            "blurb":  blurb,
            "_orig_cluster_id": c.cluster_id,
        })
    return out, picked


def build_nodes_and_edges(picked_clusters, G, per_cluster):
    """Pick top-degree nodes from each cluster, build induced edges."""
    nodes = []
    nodeset = set()
    cluster_idx_by_orig = {}
    for new_idx, c in enumerate(picked_clusters):
        cluster_idx_by_orig[c.cluster_id] = new_idx

    for new_idx, c in enumerate(picked_clusters):
        # Top-degree members in the underlying graph
        ranked = sorted(c.members,
                        key=lambda m: G.degree(m) if m in G else 0,
                        reverse=True)
        for stem in ranked[:per_cluster]:
            if stem in nodeset:
                continue
            deg = int(G.degree(stem)) if stem in G else 0
            nodes.append({
                "id":      stem,
                "cluster": new_idx,
                "degree":  deg,
                "name":    _humanize(stem),
            })
            nodeset.add(stem)

    edges = []
    for u, v in G.edges():
        if u in nodeset and v in nodeset:
            edges.append([u, v])
    return nodes, edges


def add_defense_corpus_nodes(nodes, edges, picked_clusters):
    """Inject defense corpus papers as visible graph nodes.

    Attaches each paper to relevant CS/aero/control clusters via topic match,
    so users can see defense work threaded through the academic graph.
    """
    defense_path = PROJECT_ROOT / "data" / "defense_corpus_samples.json"
    if not defense_path.exists():
        return nodes, edges

    try:
        corpus = json.loads(defense_path.read_text())
    except json.JSONDecodeError:
        return nodes, edges

    # Build cluster-name -> cluster_idx lookup
    cluster_lookup = {}
    for new_idx, c in enumerate(picked_clusters):
        for stem in c.members:
            cluster_lookup[stem.lower()] = new_idx

    # Build set of node ids present
    nodeset = {n["id"] for n in nodes}
    name_lookup = {n["id"].lower(): n["id"] for n in nodes}

    for paper in corpus.get("papers", []):
        paper_id = f"def_{paper['id']}"
        topics = paper.get("topics", [])
        title = paper.get("title", "Defense Paper")

        # Find best-matching cluster: cluster of any node whose name
        # appears in paper topics or title
        haystack = " ".join(topics + [title]).lower()
        matched_nodes = []
        for nid, real_id in name_lookup.items():
            if nid in haystack or any(tok in haystack for tok in nid.split("_") if len(tok) > 3):
                matched_nodes.append(real_id)

        if not matched_nodes:
            continue

        # Cluster = cluster of first matched node
        first_match = matched_nodes[0]
        cl_idx = next((n["cluster"] for n in nodes if n["id"] == first_match), 0)

        nodes.append({
            "id":      paper_id,
            "cluster": cl_idx,
            "degree":  len(matched_nodes),
            "name":    f"⚡ {title[:40]}",
            "kind":    "defense",
        })

        # Connect to top 2 matched nodes
        for target in matched_nodes[:2]:
            edges.append([paper_id, target])

    return nodes, edges


def build_foundation_picks(max_picks=5):
    try:
        from graph.foundations import recommend
        recs = recommend(limit=max_picks)
    except Exception:
        return []
    out = []
    for r in recs:
        m = r.metrics or {}
        out.append({
            "raw":       r.raw_name,
            "name":      r.name,
            "cluster":   None,   # filled in after we have the new cluster index
            "score":     r.score,
            "rationale": r.rationale,
            "metrics":   {
                "degree":   m.get("degree", 0),
                "span":     m.get("cluster_span", 0),
                "size":     m.get("cluster_size", 0),
                "hasWiki":  bool(m.get("has_wiki", False)),
                "rl":       float(m.get("rl_weight", 0.0)),
            },
            "_orig_cluster_id": r.cluster_id,
        })
    return out


def build_lessons(stems, rich=False):
    """Pre-render lesson cards in the JS shape. Fast mode by default."""
    try:
        from agents.curriculum import lesson_for
        from graph.clusters import load_clusters
    except Exception:
        return {}
    clusters = load_clusters() or []
    cluster_by_id = {c.cluster_id: c for c in clusters}
    n2c = {m: c.cluster_id for c in clusters for m in c.members}

    out: dict[str, dict] = {}
    mode = "rich" if rich else "fast"
    for stem in stems:
        cid = n2c.get(stem)
        cluster = cluster_by_id.get(cid)
        if cluster is None:
            continue
        try:
            les = lesson_for(stem, cluster, clusters, interest="", mode=mode)
        except Exception:
            continue
        # Map curriculum.py shape → design's shape
        key_ideas_js = []
        for k in (les.get("key_ideas") or [])[:5]:
            if isinstance(k, dict):
                key_ideas_js.append({"h": k.get("h", ""), "b": k.get("b", "")})
            else:
                # curriculum's fast mode emits plain strings
                # split into header/body if there's a colon, else use whole
                s = str(k)
                if ":" in s and len(s) < 300:
                    h, _, b = s.partition(":")
                    key_ideas_js.append({"h": h.strip(), "b": b.strip()})
                else:
                    key_ideas_js.append({"h": "", "b": s})
        quiz_js = []
        for q in (les.get("quiz") or [])[:3]:
            quiz_js.append({
                "q":       q.get("q", ""),
                "choices": q.get("a_choices") or q.get("choices") or [],
                "correct": int(q.get("correct_idx", q.get("correct", 0))),
                "why":     q.get("why", ""),
            })
        out[stem] = {
            "title":          les.get("title", _humanize(stem)),
            "summary":        les.get("summary", ""),
            "key_ideas":      key_ideas_js,
            "worked_example": les.get("worked_example") or
                               les.get("engagement_question") or "",
            "evidence":       les.get("evidence", []),
            "quiz":           quiz_js,
        }
    return out


def build_propose_examples(seeds: list[str], heuristic_only=True) -> dict:
    try:
        from agents.proposal_responder import respond
    except Exception:
        return {}
    out: dict[str, dict] = {}
    mode = "heuristic" if heuristic_only else "auto"
    for s in seeds:
        try:
            r = respond(s, k=8, mode=mode)
        except Exception:
            continue
        out[s] = {
            "matched":   [m["name"] for m in r.get("matched_concepts") or []][:6],
            "synthesis": r.get("synthesis", ""),
            "bridges":   [
                {
                    "from": b["a"],
                    "to":   b["b"],
                    "via":  " → ".join(_humanize(p) for p in b["path"]),
                }
                for b in (r.get("bridge_paths") or [])[:3]
            ],
        }
    return out


def build_tours(picks, per_pick=6):
    try:
        from agents.lesson_plan import plan_tour
    except Exception:
        return {}
    out: dict[str, list[dict]] = {}
    for p in picks:
        try:
            stops = plan_tour(p["raw"], max_stops=per_pick)
        except Exception:
            continue
        out[p["raw"]] = [
            {
                "node":      s.node,
                "cluster":   s.cluster_id,
                "kind":      s.kind,
                "rationale": s.rationale,
            }
            for s in stops
        ]
    return out


# ── Emit JS ───────────────────────────────────────────────────────────────

JS_TEMPLATE = """// Brain University — REAL data from the Python data layer.
// Generated by scripts/build_design_data.py. Do not edit by hand.
//
// Shape matches the contract in design/data.mock.js:
//   window.BU_DATA = {{ CLUSTERS, NODES, EDGES, FOUNDATION_PICKS,
//                       LESSONS, PROPOSE_EXAMPLES, BRIDGE_PAIRS, TOURS,
//                       lessonFor, planTour, adjacencyOf, bridgesFrom }};
window.BU_DATA = (() => {{
  const CLUSTERS = {clusters_json};
  const NODES = {nodes_json};
  const EDGES = {edges_json};
  const FOUNDATION_PICKS = {picks_json};
  const LESSONS = {lessons_json};
  const PROPOSE_EXAMPLES = {propose_json};
  const TOURS = {tours_json};

  // Adjacency lookup
  const ADJ = {{}};
  for (const [a, b] of EDGES) {{
    (ADJ[a] = ADJ[a] || []).push(b);
    (ADJ[b] = ADJ[b] || []).push(a);
  }}
  function adjacencyOf(nodeId) {{
    const ids = ADJ[nodeId] || [];
    return ids.map(id => NODES.find(n => n.id === id)).filter(Boolean);
  }}

  function bridgesFrom(nodeId) {{
    const node = NODES.find(n => n.id === nodeId);
    if (!node) return [];
    return adjacencyOf(nodeId)
      .filter(n => n.cluster !== node.cluster)
      .map(n => ({{
        via: nodeId,
        to:  n.id, toName: n.name,
        cluster: n.cluster,
        clusterName: CLUSTERS[n.cluster] && CLUSTERS[n.cluster].name,
      }}));
  }}

  function lessonFor(nodeId) {{
    if (LESSONS[nodeId]) return LESSONS[nodeId];
    const node = NODES.find(n => n.id === nodeId);
    if (!node) return null;
    const cluster = CLUSTERS[node.cluster] || {{ name: "?", blurb: "" }};
    return {{
      title: node.name,
      summary: `${{node.name}} sits inside the ${{cluster.name}} course. ${{cluster.blurb}} This concept is connected to ${{node.degree}} others.`,
      key_ideas: [
        {{ h: "Why it matters.", b: `${{node.name}} appears across ${{node.degree}} other concepts.` }},
        {{ h: "What to read first.", b: "Start with the wiki page, then the canonical paper. Do the worked example before the proofs." }},
        {{ h: "Where it goes next.", b: `From here the natural deepening is into adjacent concepts in ${{cluster.name}}.` }},
      ],
      worked_example: "(Auto-generated lesson — full Claude rich-mode lesson available with API key.)",
      evidence: [`wiki/${{node.id}}`],
      quiz: [{{
        q: `Which of these is the strongest reason ${{node.name}} matters?`,
        choices: ["Required by exam", "Hub concept connected to many others", "Easiest topic", "Newest"],
        correct: 1,
        why: "Hub status drives the foundation-scoring algorithm.",
      }}],
    }};
  }}

  function planTour(startId) {{
    if (TOURS[startId]) return TOURS[startId];
    const start = NODES.find(n => n.id === startId);
    if (!start) return null;
    const visited = new Set([startId]);
    const stops = [{{
      node: startId, cluster: start.cluster, kind: "start",
      rationale: "Auto-fallback start. Highest-degree unvisited node nearby will be picked next.",
    }}];
    while (stops.length < 6) {{
      const last = stops[stops.length - 1];
      const adj = adjacencyOf(last.node)
        .filter(n => !visited.has(n.id))
        .sort((a, b) => b.degree - a.degree);
      if (!adj.length) break;
      const next = adj.find(n => n.cluster !== last.cluster) || adj[0];
      visited.add(next.id);
      const kind = next.cluster !== last.cluster ? "bridge" : "deepen";
      stops.push({{
        node: next.id, cluster: next.cluster, kind,
        rationale: kind === "bridge"
          ? `Bridge into ${{CLUSTERS[next.cluster].name}} via ${{next.name}}.`
          : `Deeper in ${{CLUSTERS[next.cluster].name}}: ${{next.name}} (degree ${{next.degree}}).`,
      }});
    }}
    if (stops.length) stops[stops.length - 1].kind = "capstone";
    return stops;
  }}

  // BRIDGE_PAIRS — for the legacy demo screen; auto-derived from edges
  const BRIDGE_PAIRS = {{}};
  for (const [a, b] of EDGES) {{
    const na = NODES.find(n => n.id === a);
    const nb = NODES.find(n => n.id === b);
    if (na && nb && na.cluster !== nb.cluster) {{
      const k = `${{na.cluster}}-${{nb.cluster}}`;
      (BRIDGE_PAIRS[k] = BRIDGE_PAIRS[k] || []).push([a, b]);
    }}
  }}

  return {{ CLUSTERS, NODES, EDGES, FOUNDATION_PICKS,
           LESSONS, PROPOSE_EXAMPLES, BRIDGE_PAIRS, TOURS,
           lessonFor, planTour, adjacencyOf, bridgesFrom }};
}})();
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-clusters", type=int, default=6)
    ap.add_argument("--per-cluster", type=int, default=8)
    ap.add_argument("--rich-lessons", action="store_true",
                    help="Generate lessons with Claude (slow + costs $$)")
    ap.add_argument("--lessons-for-foundations-only", action="store_true",
                    help="Only pre-render lessons for foundation picks")
    ap.add_argument("--no-propose", action="store_true",
                    help="Skip Propose example generation (faster)")
    args = ap.parse_args()

    # 1. Cluster catalog + underlying graph
    print("[1/6] Loading clusters + graph...")
    from graph.clusters import load_clusters, build_clusters as build_cl, load_graph
    clusters_all = load_clusters() or build_cl(force=False)
    if not clusters_all:
        print("✗ No clusters yet. Run the learning app once or call "
              "graph.clusters.build_clusters(force=True).")
        sys.exit(1)
    G = load_graph()
    print(f"  {len(clusters_all)} clusters, "
          f"{G.number_of_nodes()}n / {G.number_of_edges()}e")

    # 2. Build cluster + node + edge subset
    print(f"[2/6] Picking top {args.max_clusters} clusters × "
          f"{args.per_cluster} nodes/cluster")
    clusters_js, picked = build_clusters(clusters_all, args.max_clusters)
    nodes_js, edges_js = build_nodes_and_edges(picked, G, args.per_cluster)
    nodes_js, edges_js = add_defense_corpus_nodes(nodes_js, edges_js, picked)
    print(f"  {len(nodes_js)} nodes, {len(edges_js)} edges")

    # 3. Foundation picks (5)
    print("[3/6] Computing FOUNDATION_PICKS...")
    picks_js = build_foundation_picks(max_picks=5)
    # Map each pick's _orig_cluster_id → new cluster index
    orig_to_new = {c["_orig_cluster_id"]: c["id"] for c in clusters_js}
    for p in picks_js:
        p["cluster"] = orig_to_new.get(p.pop("_orig_cluster_id"), 0)
    print(f"  picks: {[p['name'] for p in picks_js]}")

    # 4. Lessons
    if args.lessons_for_foundations_only:
        lesson_stems = [p["raw"] for p in picks_js]
    else:
        lesson_stems = [n["id"] for n in nodes_js]
    print(f"[4/6] Pre-rendering {len(lesson_stems)} lessons "
          f"({'rich' if args.rich_lessons else 'fast'})...")
    t0 = time.time()
    lessons_js = build_lessons(lesson_stems, rich=args.rich_lessons)
    print(f"  done in {time.time() - t0:.1f}s")

    # 5. Propose examples
    if args.no_propose:
        propose_js = {}
    else:
        seeds = [
            "drone swarm coordination using graph theory",
            "applying control theory to financial trading",
            "stochastic gene expression and information theory",
            "boost-phase intercept with reinforcement learning",
        ]
        print(f"[5/6] Generating {len(seeds)} Propose examples...")
        propose_js = build_propose_examples(seeds, heuristic_only=True)

    # 6. Tours pre-planned for each foundation pick
    print("[6/6] Pre-planning tours for each foundation pick...")
    tours_raw = build_tours(picks_js, per_pick=6)
    # Remap cluster ids in tour stops to new indices
    tours_js: dict = {}
    for k, stops in tours_raw.items():
        tours_js[k] = []
        for s in stops:
            tours_js[k].append({
                "node":      s["node"],
                "cluster":   orig_to_new.get(s["cluster"], 0),
                "kind":      s["kind"],
                "rationale": s["rationale"],
            })
    print(f"  tours: {list(tours_js.keys())}")

    # Strip helper-only fields from clusters
    for c in clusters_js:
        c.pop("_orig_cluster_id", None)

    # Backup the mock once
    mock_src = DESIGN_DIR / "data.js"
    if not MOCK_BACKUP.exists() and mock_src.exists():
        MOCK_BACKUP.write_text(mock_src.read_text())
        print(f"  backed up original mock to {MOCK_BACKUP.name}")

    # Emit
    out = JS_TEMPLATE.format(
        clusters_json=json.dumps(clusters_js, indent=2),
        nodes_json=json.dumps(nodes_js, indent=2),
        edges_json=json.dumps(edges_js),
        picks_json=json.dumps(picks_js, indent=2),
        lessons_json=json.dumps(lessons_js, indent=2),
        propose_json=json.dumps(propose_js, indent=2),
        tours_json=json.dumps(tours_js, indent=2),
    )
    OUT_PATH.write_text(out)
    size_kb = len(out) / 1024
    print(f"\n[Done] wrote {OUT_PATH.relative_to(PROJECT_ROOT)} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
