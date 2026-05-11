"""
Open-Problems scorer — find gaps in the concept graph that no paper has
addressed yet, and rank them by how much novelty + value they'd unlock.

Three kinds of gap:

  1. missing_bridge: two high-paper-degree concepts that *should* connect
     (both are foundational, both appear together as activations in
     some paper's foundation set, yet have zero edges between them in
     the corpus). A new paper could earn high novelty bits by linking
     them.

  2. underexplored: a wiki concept that exists in the vocabulary and
     is referenced as a foundation by multiple other papers, but only
     1-2 papers in the corpus actively activate it as a primary
     concept. A focused paper on it would close a key gap.

  3. stale_cluster: a Louvain-style cluster (computed by greedy
     co-occurrence seeding) whose newest activating paper is older
     than the cluster's median paper year. The community has gone
     quiet — open territory for a fresh contribution.

For each problem we attach:
  - closest_papers: top-3 arXivis papers most likely to be relevant
    (concept overlap w/ the problem's involved nodes).
  - suggested_foundations: high-paper-degree concepts the new work
    could build on.

Output: design/open_problems.js (window.OPEN_PROBLEMS).

Run:
  python3 scripts/build_open_problems.py
  python3 scripts/build_open_problems.py --max 60
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARXIVIS_JS   = PROJECT_ROOT / "design" / "arxivis_data.js"
OUT_PATH     = PROJECT_ROOT / "design" / "open_problems.js"


def load_arxivis() -> dict:
    if not ARXIVIS_JS.exists():
        sys.exit(f"missing {ARXIVIS_JS} — run scripts/build_arxivis_data.py first")
    t = ARXIVIS_JS.read_text()
    return json.loads(t[t.find("{"): t.rfind("}") + 1])


GENERIC_STOP = {
    "filter", "reduce", "partition", "match", "map", "graph", "tree",
    "set", "node", "edge", "function", "vector", "matrix", "value",
    "norm", "rate", "loss", "rule", "step", "task", "limit", "row",
    "column", "operator", "label",
    "convert", "split", "merge", "build", "init", "scan", "test",
}


def _is_real_concept(name: str) -> bool:
    """Skip noisy single-verb tokens that aren't really concepts."""
    if not name: return False
    if len(name) < 5: return False
    if name.lower().strip() in GENERIC_STOP: return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=50, help="problems to keep")
    args = ap.parse_args()

    data = load_arxivis()
    papers   = data["papers"]
    universe = data.get("concept_universe", [])
    edges    = data.get("concept_edges", [])  # [a, b, weight]

    # Concept lookup tables
    concept_by_id = {c["id"]: c for c in universe}
    # Paper-degree (count of papers activating this concept) = universe.degree
    # Edge weight (count of papers in which both co-activate) = edges[i][2]
    edge_weight: dict[tuple[str, str], int] = {}
    for e in edges:
        a, b, w = e[0], e[1], (e[2] if len(e) > 2 else 1)
        edge_weight[(a, b)] = w
        edge_weight[(b, a)] = w

    # Per-paper concept set (slug form) for relevance lookup
    paper_concept_set: dict[str, set[str]] = {}
    paper_year: dict[str, int | None] = {}
    for p in papers:
        ids = {c["id"].replace("wiki:", "") for c in p.get("concepts", [])}
        paper_concept_set[p["id"]] = ids
        paper_year[p["id"]] = p.get("year")

    def closest_papers(involved_ids: set[str], k: int = 3) -> list[dict]:
        scored = []
        for p in papers:
            inter = paper_concept_set[p["id"]] & involved_ids
            if not inter:
                continue
            scored.append({
                "id":      p["id"],
                "title":   p["title"],
                "overlap": len(inter),
                "novelty": p.get("novelty_bits", 0),
            })
        scored.sort(key=lambda x: (-x["overlap"], -x["novelty"]))
        return scored[:k]

    def name(slug: str) -> str:
        c = concept_by_id.get(slug)
        if c:
            return c["name"]
        return slug.replace("_", " ")

    problems = []

    # ─── 1. MISSING BRIDGES ─────────────────────────────────────────────
    # Concepts with paper-degree ≥ 3 that have no direct edge despite
    # appearing together as activations in some paper's pair_edges.
    # We approximate this with: cluster of high-degree concepts whose
    # mutual edge_weight is 0.
    high_deg = [c for c in universe
                if c.get("degree", 0) >= 3 and _is_real_concept(c.get("name", ""))]
    # Sort by degree descending, cap to keep N^2 manageable
    high_deg.sort(key=lambda c: -c["degree"])
    high_deg = high_deg[:60]

    # Cluster co-membership = same cluster id from build_arxivis_data
    seen_pairs: set[tuple[str, str]] = set()
    for i, a in enumerate(high_deg):
        for b in high_deg[i + 1:]:
            key = tuple(sorted([a["id"], b["id"]]))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            w = edge_weight.get(key, 0)
            if w > 0:
                continue
            # Higher score for pairs across different clusters
            cross_cluster = a.get("cluster") != b.get("cluster")
            score = (a["degree"] + b["degree"]) * (1.6 if cross_cluster else 1.0)
            problems.append({
                "kind":         "missing_bridge",
                "title":        f"No paper has bridged {name(a['id'])} and {name(b['id'])}",
                "concepts":     [a["id"], b["id"]],
                "score":        round(score, 2),
                "why":          (
                    f"{name(a['id'])} appears in {a['degree']} papers, "
                    f"{name(b['id'])} in {b['degree']}, but the corpus "
                    f"contains zero papers that activate both."
                    + (" Bridges two distinct clusters."
                       if cross_cluster else "")
                ),
                "closest_papers": closest_papers({a["id"], b["id"]}),
                "suggested_foundations": [
                    {"id": a["id"], "name": name(a["id"]), "papers": a["degree"]},
                    {"id": b["id"], "name": name(b["id"]), "papers": b["degree"]},
                ],
            })

    # ─── 2. UNDEREXPLORED ANCHORS ───────────────────────────────────────
    # Concepts mentioned as `foundations` by ≥ 3 papers, but themselves
    # activated as a primary concept in ≤ 2 papers. Foundation pull
    # without active research = open territory.
    foundation_pull: Counter = Counter()
    for p in papers:
        for f in p.get("foundations", []) or []:
            # foundations were stored w/ raw id (e.g. wiki:slug); strip
            slug = f["id"].replace("wiki:", "") if "id" in f else None
            if slug:
                foundation_pull[slug] += 1
    for slug, pull in foundation_pull.items():
        c = concept_by_id.get(slug)
        if not c:
            continue
        if not _is_real_concept(c.get("name", "")):
            continue
        deg = c.get("degree", 0)
        if pull >= 2 and deg <= 2:
            score = pull * 4 + (3 - deg)
            problems.append({
                "kind":         "underexplored",
                "title":        f"{name(slug)} is foundational but barely studied",
                "concepts":     [slug],
                "score":        round(score, 2),
                "why":          (
                    f"{pull} papers in the corpus build ON {name(slug)} as a "
                    f"foundation, yet only {deg} paper{'s' if deg != 1 else ''} "
                    f"focuses on it as a primary subject."
                ),
                "closest_papers": closest_papers({slug}),
                "suggested_foundations": [
                    {"id": slug, "name": name(slug), "papers": deg},
                ],
            })

    # ─── 3. STALE CLUSTERS ──────────────────────────────────────────────
    # For each cluster id, find median year of activating papers + newest.
    # Stale = newest is older than median (community has slowed).
    cluster_papers: dict[int, list[int]] = defaultdict(list)
    cluster_concepts: dict[int, list[str]] = defaultdict(list)
    for c in universe:
        cluster_concepts[c.get("cluster", 0)].append(c["id"])
    for p in papers:
        y = p.get("year")
        if not y:
            continue
        clusters_touched = set()
        for c in p.get("concepts", []):
            slug = c["id"].replace("wiki:", "")
            cid = concept_by_id.get(slug, {}).get("cluster")
            if cid is not None:
                clusters_touched.add(cid)
        for cid in clusters_touched:
            cluster_papers[cid].append(y)

    for cid, years in cluster_papers.items():
        if len(years) < 4:
            continue
        years_sorted = sorted(years)
        median = years_sorted[len(years_sorted) // 2]
        newest = years_sorted[-1]
        # If the newest paper isn't notably newer than the median, cluster's stale
        if newest - median <= 0:
            seed_concepts = [name(s) for s in cluster_concepts[cid][:3]]
            score = len(years) * 0.5 + (median - 2000)
            problems.append({
                "kind":         "stale_cluster",
                "title":        f"Cluster around {', '.join(seed_concepts)} has gone quiet",
                "concepts":     cluster_concepts[cid][:5],
                "score":        round(score, 2),
                "why":          (
                    f"{len(years)} papers in this cluster, median year "
                    f"{median}, newest paper {newest}. No recent activity — "
                    "open territory for a fresh contribution."
                ),
                "closest_papers": closest_papers(set(cluster_concepts[cid][:8])),
                "suggested_foundations": [
                    {"id": s, "name": name(s), "papers": concept_by_id.get(s, {}).get("degree", 1)}
                    for s in cluster_concepts[cid][:3]
                ],
            })

    # Bucket-balance: ensure variety across kinds (avoid 60 missing_bridge dominating)
    by_kind: dict[str, list[dict]] = defaultdict(list)
    for p in problems:
        by_kind[p["kind"]].append(p)
    for k in by_kind:
        by_kind[k].sort(key=lambda p: -p["score"])
    balanced: list[dict] = []
    quota = max(args.max // 3, 5)
    for k in ("missing_bridge", "underexplored", "stale_cluster"):
        balanced.extend(by_kind.get(k, [])[:quota])
    # Top up w/ remaining missing_bridges if room
    while len(balanced) < args.max:
        rest = [p for k in by_kind for p in by_kind[k] if p not in balanced]
        if not rest:
            break
        rest.sort(key=lambda p: -p["score"])
        balanced.append(rest[0])
    balanced.sort(key=lambda p: -p["score"])
    problems = balanced[: args.max]

    out = {
        "problems":     problems,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "corpus_papers":      len(papers),
            "universe_concepts":  len(universe),
            "missing_bridges":    sum(1 for p in problems if p["kind"] == "missing_bridge"),
            "underexplored":      sum(1 for p in problems if p["kind"] == "underexplored"),
            "stale_clusters":     sum(1 for p in problems if p["kind"] == "stale_cluster"),
        },
    }
    js = "window.OPEN_PROBLEMS = " + json.dumps(out, indent=2, ensure_ascii=False) + ";\n"
    OUT_PATH.write_text(js)
    print(f"→ wrote {OUT_PATH} ({OUT_PATH.stat().st_size // 1024} KB)")
    print(f"  {len(problems)} problems: {out['stats']}")
    for p in problems[:5]:
        print(f"  [{p['kind']:14s} {p['score']:6.1f}] {p['title']}")


if __name__ == "__main__":
    main()
