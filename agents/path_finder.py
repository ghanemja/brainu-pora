"""
Concept-to-concept path finder — given any two nodes in the brain graph,
build a weighted shortest path and render it as a mini-tour the UI can
walk just like a regular `lesson_plan` tour.

This is the "show me how Backpropagation connects to Transformers"
feature. Pedagogically it's much more interesting than a generic tour:
the learner picks the endpoints, the graph fills in the bridge.

Algorithm
---------
1. Resolve both endpoints (accept human-readable or underscored names).
2. Try multiple path strategies, pick the most informative:
     a. weighted shortest path (edge weight = inverse importance)
     b. cluster-aware path that prefers staying inside clusters when
        possible (deeper context per cluster transition)
     c. high-pagerank path: among paths within +1 hop of shortest,
        prefer the one whose intermediate nodes have highest pagerank
        (i.e. the most "load-bearing" bridge concepts)
3. For each stop in the chosen path, classify its role:
     - "endpoint_a"      → starting concept
     - "deepen"          → still inside endpoint_a's cluster
     - "bridge"          → first stop in a new cluster (cluster crossing)
     - "deepen_target"   → inside endpoint_b's cluster, approaching b
     - "endpoint_b"      → destination
4. Write per-stop rationales explaining why this intermediate concept
   was picked.

The returned shape matches `agents.lesson_plan.TourStop` exactly so the
existing tour renderer can display it without modification.

Public:
  plan_path(a, b, strategy="auto", vault_path=None) → list[TourStop]
  available_strategies() → list[str]
  plan_path_between_clusters(cid_a, cid_b) → list[TourStop]
"""

from __future__ import annotations

import os
from typing import Iterable

from agents.lesson_plan import TourStop


# ── Tunables ───────────────────────────────────────────────────────────────

MAX_PATH_LEN = int(os.environ.get("PATH_FINDER_MAX_LEN", 8))
PR_BIAS      = float(os.environ.get("PATH_FINDER_PR_BIAS", 0.3))


# ── Public ─────────────────────────────────────────────────────────────────

def available_strategies() -> list[str]:
    return ["auto", "shortest", "cluster_aware", "pagerank_biased"]


def plan_path(a: str, b: str, *, strategy: str = "auto",
              max_len: int = MAX_PATH_LEN,
              vault_path: str | None = None) -> list[TourStop]:
    """Return an ordered list of TourStops walking from a to b.

    Falls back to a 1-stop tour at `a` if anything goes wrong (graph
    unavailable, nodes missing, no path).
    """
    try:
        import networkx as nx
        from graph.clusters import load_graph, load_clusters
    except ImportError:
        return _solo(a)

    G = load_graph(source="auto", vault_path=vault_path)
    if G is None or G.number_of_nodes() == 0:
        return _solo(a)

    a_orig = _resolve(a, G)
    b_orig = _resolve(b, G)
    if a_orig is None or b_orig is None or a_orig == b_orig:
        return _solo(a if a_orig is None else a_orig)

    clusters = load_clusters() or []
    n2c, by_cid = _cluster_lookup(clusters)

    pr = _safe_pagerank(G)

    # Try strategies in order, pick the most informative valid path
    candidates: list[list[str]] = []
    overflow:   list[list[str]] = []

    def try_strat(name: str):
        try:
            p = _path_for_strategy(name, G, a_orig, b_orig, n2c, pr, max_len)
            if not p or len(p) < 2:
                return
            if len(p) <= max_len + 1:
                candidates.append(p)
            else:
                overflow.append(p)
        except Exception:
            pass

    if strategy == "auto":
        for s in ("cluster_aware", "pagerank_biased", "shortest"):
            try_strat(s)
    else:
        try_strat(strategy)

    if not candidates:
        # Soft fallback: graph really does require more hops than the
        # cap; pick the shortest overflow path and truncate it down to
        # max_len hops, keeping the endpoints + the most-pagerank-y
        # intermediates so the tour still arrives at b.
        if not overflow:
            return _solo(a_orig)
        overflow.sort(key=len)
        full = overflow[0]
        candidates = [_truncate_path(full, max_len, pr)]

    # Pick the path with the best score: shorter is better, more
    # cluster-diverse is better, higher mean pagerank on interiors is better.
    def score(path: list[str]) -> float:
        length = len(path) - 1
        cids = {n2c.get(n, -1) for n in path}
        n_clusters = len(cids)
        if length <= 1:
            interior_pr = 0.0
        else:
            interior_pr = sum(pr.get(n, 0) for n in path[1:-1]) / (length - 1)
        # Lower length is better; bonus for cluster diversity; small bonus for pagerank
        return -length + 0.5 * n_clusters + interior_pr * 5

    candidates.sort(key=score, reverse=True)
    path = candidates[0]

    return _path_to_stops(path, G, n2c, by_cid, pr)


def plan_path_between_clusters(cid_a: int, cid_b: int,
                                vault_path: str | None = None) -> list[TourStop]:
    """Convenience: pick the highest-degree node in each cluster as
    endpoints, then plan_path between them."""
    try:
        from graph.clusters import load_clusters
    except ImportError:
        return []
    clusters = load_clusters() or []
    by_cid = {c.cluster_id: c for c in clusters}
    a_cluster = by_cid.get(cid_a)
    b_cluster = by_cid.get(cid_b)
    if a_cluster is None or b_cluster is None:
        return []
    if not a_cluster.top_nodes or not b_cluster.top_nodes:
        return []
    a = a_cluster.top_nodes[0][0].replace(" ", "_")
    b = b_cluster.top_nodes[0][0].replace(" ", "_")
    return plan_path(a, b, vault_path=vault_path)


# ── Strategy implementations ──────────────────────────────────────────────

def _path_for_strategy(strat: str, G, a: str, b: str,
                       n2c: dict, pr: dict, max_len: int) -> list[str] | None:
    import networkx as nx

    if strat == "shortest":
        try:
            return nx.shortest_path(G, a, b, weight=None)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    if strat == "cluster_aware":
        # Edge weight is lower (preferred) if both endpoints are in the
        # same cluster — i.e. stay-in-cluster transitions are cheaper.
        def w(u, v, d):
            return 1.0 if n2c.get(u) == n2c.get(v) else 2.0
        try:
            return nx.shortest_path(G, a, b, weight=w)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    if strat == "pagerank_biased":
        # Edge cost is lower for hops *through* high-pagerank nodes.
        def w(u, v, d):
            return 1.0 / (1e-6 + PR_BIAS * (pr.get(u, 0) + pr.get(v, 0)) + 1.0)
        try:
            return nx.shortest_path(G, a, b, weight=w)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    return None


# ── Stop construction ──────────────────────────────────────────────────────

def _path_to_stops(path: list[str], G, n2c: dict, by_cid: dict,
                   pr: dict) -> list[TourStop]:
    stops: list[TourStop] = []
    a, b = path[0], path[-1]
    cluster_a = n2c.get(a, -1)
    cluster_b = n2c.get(b, -1)

    for i, node in enumerate(path):
        cid = n2c.get(node, -1)
        cluster = by_cid.get(cid)
        cname = cluster.name if cluster else "?"
        prev = path[i - 1] if i > 0 else None
        prev_cid = n2c.get(prev, -1) if prev else None

        if i == 0:
            kind = "start"
            rationale = (
                f"Starting from **{_humanize(node)}** in the *{cname}* "
                f"course. We'll walk through {len(path) - 1} hops to reach "
                f"**{_humanize(b)}**, surfacing the bridge concepts along the way."
            )
        elif i == len(path) - 1:
            kind = "capstone"
            rationale = (
                f"And we arrive at **{_humanize(node)}** — the destination. "
                f"Looking back at the path, you should now see how "
                f"{_humanize(a)} and {_humanize(node)} are connected "
                f"through {len(path) - 2} intermediate concept{'s' if len(path) > 3 else ''}."
            )
        else:
            crossed = cid != prev_cid
            kind = "bridge" if crossed else "deepen"
            if crossed:
                rationale = (
                    f"We cross from *{by_cid.get(prev_cid).name if by_cid.get(prev_cid) else '?'}* "
                    f"into the **{cname}** course via {_humanize(node)} — "
                    f"this concept is what links the two areas in our graph."
                )
            else:
                rationale = (
                    f"Staying in *{cname}*. **{_humanize(node)}** is the "
                    f"natural next hop toward {_humanize(b)} — it has an "
                    f"edge to {_humanize(prev)} and progresses us closer "
                    f"to the destination."
                )

        stops.append(TourStop(
            order=i + 1,
            node=node,
            name=_humanize(node),
            cluster_id=cid,
            cluster_name=cname,
            kind=kind,
            rationale=rationale,
            metrics={
                "degree":   int(G.degree(node)),
                "pagerank": round(float(pr.get(node, 0.0)), 4),
                "step":     i,
                "of":       len(path) - 1,
            },
        ))
    return stops


# ── Helpers ────────────────────────────────────────────────────────────────

def _solo(name: str) -> list[TourStop]:
    return [TourStop(
        order=1, node=name.replace(" ", "_"), name=_humanize(name),
        cluster_id=-1, cluster_name="?",
        kind="start",
        rationale="Could not build a path — graph context is limited.",
        metrics={},
    )]


def _resolve(name: str, G) -> str | None:
    """Accept human-readable or underscored input; return graph-internal name."""
    candidates = [name, name.replace(" ", "_"), name.replace("_", " ")]
    for c in candidates:
        if c in G:
            return c
    # Case-insensitive scan as a last resort
    lc = name.lower()
    for n in G.nodes():
        if n.lower() == lc or n.replace("_", " ").lower() == lc:
            return n
    return None


def _cluster_lookup(clusters) -> tuple[dict, dict]:
    """Map a graph-internal node name to its cluster id.

    Persisted cluster.members can be either humanized ("controlling sets")
    or underscored ("controlling_sets") depending on the loader path
    used at build time; we index both forms so callers don't have to care.
    """
    n2c, by_cid = {}, {}
    for c in clusters:
        by_cid[c.cluster_id] = c
        for m in c.members:
            n2c[m] = c.cluster_id
            n2c[m.replace(" ", "_")] = c.cluster_id
            n2c[m.replace("_", " ")] = c.cluster_id
    return n2c, by_cid


def _truncate_path(path: list[str], max_len: int, pr: dict) -> list[str]:
    """Shrink a too-long path to max_len hops while preserving endpoints
    and the highest-pagerank intermediate nodes (the "load-bearing"
    bridge concepts the learner most needs to see)."""
    if len(path) - 1 <= max_len:
        return path
    a, b = path[0], path[-1]
    interior = path[1:-1]
    keep = max(0, max_len - 1)
    if keep == 0:
        return [a, b]
    # Score each interior node by pagerank; keep the top `keep`, then
    # restore graph order.
    ranked = sorted(interior, key=lambda n: pr.get(n, 0), reverse=True)[:keep]
    keep_set = set(ranked)
    return [a] + [n for n in interior if n in keep_set] + [b]


def _safe_pagerank(G) -> dict:
    try:
        import networkx as nx
        return nx.pagerank(G, weight="weight")
    except Exception:
        return {n: G.degree(n) for n in G.nodes()}


def _humanize(name: str) -> str:
    return name.replace("_", " ").strip()
