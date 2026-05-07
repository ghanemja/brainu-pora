"""
Lesson-tour planner — pre-compute a multi-stop traversal of the brain graph
for a single learning session.

Given a starting node, plan 5–8 stops following these rules in order:

  1. Stay in the same cluster while there's still high-degree unvisited
     material there (depth before breadth).
  2. When the cluster's juice runs out (3 stops or no good unvisited
     candidates), use a bridge node to jump to the most-connected
     adjacent cluster.
  3. From the new cluster's entry node (the bridge), stay in that
     cluster for 1-2 more stops then move on.
  4. End on a high-pagerank "capstone" node that ties multiple themes
     together.

Each stop carries a `rationale` explaining why we picked it as the next
step. The UI shows these as a storyline overlay on top of the graph.

Public:
  TourStop dataclass
  plan_tour(start_node, max_stops=6) → list[TourStop]
"""

from __future__ import annotations

import os
import random
from dataclasses import asdict, dataclass, field
from typing import Iterable


@dataclass
class TourStop:
    order:        int
    node:         str          # graph-internal name (underscored)
    name:         str          # human-readable
    cluster_id:   int
    cluster_name: str
    kind:         str          # "start" | "deepen" | "bridge" | "capstone"
    rationale:    str
    metrics:      dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


# ── Tunables ───────────────────────────────────────────────────────────────

DEFAULT_STOPS         = int(os.environ.get("TOUR_STOPS", 6))
MAX_DEPTH_PER_CLUSTER = int(os.environ.get("TOUR_MAX_DEPTH", 3))


# ── Helpers ────────────────────────────────────────────────────────────────

def _humanize(s: str) -> str:
    return s.replace("_", " ").strip()


def _cluster_lookup(clusters):
    """Build node→cluster_id and id→cluster maps."""
    n2c = {}
    by_id = {}
    for c in clusters:
        by_id[c.cluster_id] = c
        for m in c.members:
            n2c[m] = c.cluster_id
    return n2c, by_id


# ── Public ─────────────────────────────────────────────────────────────────

def plan_tour(start_node: str, max_stops: int = DEFAULT_STOPS,
              seed: int | None = None) -> list[TourStop]:
    """Return an ordered list of TourStops starting at `start_node`.

    Uses the cluster catalog + the underlying networkx graph. If anything
    fails (no graph, missing node), returns a single-stop tour with the
    start node only.
    """
    try:
        import networkx as nx
        from graph.clusters import load_clusters, build_clusters, load_graph
    except ImportError:
        return [_solo_stop(start_node, 0, "?")]

    rnd = random.Random(seed)
    clusters = load_clusters() or build_clusters(force=False)
    if not clusters:
        return [_solo_stop(start_node, 0, "?")]

    G = load_graph()
    if G is None or G.number_of_nodes() == 0:
        return [_solo_stop(start_node, 0, "?")]

    n2c, by_id = _cluster_lookup(clusters)
    start_orig = start_node.replace(" ", "_") if " " in start_node else start_node
    if start_orig not in G:
        # Try humanized → underscored form
        for cand in (start_node, start_node.replace(" ", "_")):
            if cand in G:
                start_orig = cand
                break
        else:
            return [_solo_stop(start_node, 0, "?")]

    visited: set[str] = {start_orig}
    stops: list[TourStop] = []

    cur_cid = n2c.get(start_orig, -1)
    cur_cluster = by_id.get(cur_cid)
    cur_cluster_name = cur_cluster.name if cur_cluster else "?"

    # Stop 1 — start
    stops.append(TourStop(
        order=1, node=start_orig, name=_humanize(start_orig),
        cluster_id=cur_cid, cluster_name=cur_cluster_name,
        kind="start",
        rationale=(
            f"We start here because **{_humanize(start_orig)}** is one of "
            f"the most foundational nodes in the graph — it sits at the "
            f"core of the *{cur_cluster_name}* course and connects out to "
            f"many other concepts. Mastering it unlocks the rest of this region."
        ),
        metrics={"degree": int(G.degree(start_orig))},
    ))

    # PageRank for ranking unvisited candidates
    try:
        pr = nx.pagerank(G, weight="weight")
    except Exception:
        pr = {n: G.degree(n) for n in G.nodes()}

    depth_in_cluster = 1
    while len(stops) < max_stops:
        prev = stops[-1]

        # Decide whether to deepen or bridge
        should_bridge = (
            depth_in_cluster >= MAX_DEPTH_PER_CLUSTER
            or _no_good_deepen(G, by_id.get(prev.cluster_id), visited)
        )

        if should_bridge:
            nxt = _pick_bridge(G, by_id, n2c, prev.node, prev.cluster_id, visited, pr)
            if nxt is None:
                # No bridge available — fall back to deepen
                nxt = _pick_deepen(G, by_id.get(prev.cluster_id), visited, pr)
                if nxt is None:
                    break
                kind = "deepen"
                rationale = _rationale_deepen(prev, nxt, G, depth_in_cluster, by_id)
                depth_in_cluster += 1
            else:
                kind = "bridge"
                new_cid = n2c.get(nxt, prev.cluster_id)
                new_cluster_name = (by_id.get(new_cid).name
                                     if by_id.get(new_cid) else "?")
                rationale = (
                    f"Now we **bridge into the {new_cluster_name} course** "
                    f"via {_humanize(nxt)}, because this concept connects "
                    f"the two areas. You've built up enough context in "
                    f"*{prev.cluster_name}* to make sense of how it relates."
                )
                cur_cid = new_cid
                cur_cluster_name = new_cluster_name
                depth_in_cluster = 1
        else:
            nxt = _pick_deepen(G, by_id.get(prev.cluster_id), visited, pr)
            if nxt is None:
                # No deeper candidate — try bridge as fallback
                nxt = _pick_bridge(G, by_id, n2c, prev.node, prev.cluster_id, visited, pr)
                if nxt is None:
                    break
                kind = "bridge"
                new_cid = n2c.get(nxt, prev.cluster_id)
                new_cluster_name = (by_id.get(new_cid).name
                                     if by_id.get(new_cid) else "?")
                rationale = (
                    f"This *{prev.cluster_name}* course has no more high-"
                    f"value unvisited concepts close to where we are. "
                    f"Bridging into **{new_cluster_name}** via {_humanize(nxt)}."
                )
                cur_cid = new_cid
                cur_cluster_name = new_cluster_name
                depth_in_cluster = 1
            else:
                kind = "deepen"
                rationale = _rationale_deepen(prev, nxt, G, depth_in_cluster, by_id)
                depth_in_cluster += 1

        visited.add(nxt)
        stops.append(TourStop(
            order=len(stops) + 1,
            node=nxt, name=_humanize(nxt),
            cluster_id=cur_cid, cluster_name=cur_cluster_name,
            kind=kind, rationale=rationale,
            metrics={"degree": int(G.degree(nxt)),
                      "pagerank": round(float(pr.get(nxt, 0.0)), 4)},
        ))

    # Mark the final stop as a capstone if we picked something high-pagerank
    if stops:
        last = stops[-1]
        last_pr = float(pr.get(last.node, 0))
        median_pr = sorted(pr.values())[len(pr) // 2] if pr else 0
        if last_pr > median_pr * 1.5:
            last.kind = "capstone"
            last.rationale += (
                "  · This is a *capstone* concept — it ties multiple themes "
                "from the tour together; a good place to stop and consolidate."
            )

    return stops


def _solo_stop(start_node, idx, cname):
    return [TourStop(
        order=1, node=start_node.replace(" ", "_"),
        name=_humanize(start_node),
        cluster_id=-1, cluster_name=cname, kind="start",
        rationale=("We start with this concept. Graph context is limited — "
                    "tour will be a single stop until the brain graph "
                    "is rebuilt."),
        metrics={},
    )]


def _no_good_deepen(G, cluster, visited) -> bool:
    if cluster is None:
        return True
    candidates = [m for m in cluster.members
                  if m not in visited and m in G]
    return not candidates


def _pick_deepen(G, cluster, visited, pr) -> str | None:
    """Pick the next concept inside the current cluster.
    Prefer high-degree + high-pagerank concepts adjacent to already-visited
    nodes (so the lesson chain stays connected)."""
    if cluster is None:
        return None
    visited_in_cluster = visited & set(cluster.members)
    pool = [m for m in cluster.members
            if m not in visited and m in G]
    if not pool:
        return None

    # Score: prefer neighbours of visited (so the chain is connected)
    def _score(n):
        deg = G.degree(n)
        prx = pr.get(n, 0)
        adj = sum(1 for v in visited_in_cluster if G.has_edge(n, v))
        return (adj * 5) + (deg * 0.5) + (prx * 100)

    pool.sort(key=_score, reverse=True)
    return pool[0]


def _pick_bridge(G, by_id, n2c, current_node, current_cid, visited, pr) -> str | None:
    """Pick a bridge: a neighbour-of-visited node whose cluster differs
    from current_cid, preferring high-degree."""
    cluster = by_id.get(current_cid)
    if cluster is None:
        return None

    # Use the cluster's pre-computed bridges first
    for b_name, _ in cluster.bridges:
        if b_name in visited or b_name not in G:
            continue
        return b_name

    # Fallback: scan the whole cluster's neighbourhood
    candidates: list[tuple[float, str]] = []
    for member in cluster.members:
        if member not in G:
            continue
        for nbr in G.neighbors(member):
            if nbr in visited:
                continue
            ncid = n2c.get(nbr)
            if ncid is None or ncid == current_cid:
                continue
            score = G.degree(nbr) + pr.get(nbr, 0) * 100
            candidates.append((score, nbr))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def _rationale_deepen(prev, nxt, G, depth, by_id) -> str:
    """One-sentence storyline for staying in the same cluster."""
    if depth == 1:
        return (
            f"Next we go deeper into the same course. "
            f"**{_humanize(nxt)}** is closely related to "
            f"{_humanize(prev.node)} — they share an edge — and seeing "
            f"how the cluster's ideas chain together cements the topic."
        )
    cluster = by_id.get(prev.cluster_id)
    members_left = (
        len([m for m in cluster.members if m != nxt])
        if cluster else 0
    )
    return (
        f"Staying in *{prev.cluster_name}* for one more stop. "
        f"**{_humanize(nxt)}** has the highest connectivity among the "
        f"unvisited concepts here, so it builds the most context. "
        f"({members_left} concepts still in this course.)"
    )
