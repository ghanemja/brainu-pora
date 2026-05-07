"""
Foundational-concept recommender.

Picks the best places to *start* learning by scoring each node on multiple
"fundamentalness" signals:

  degree           — how many concepts it directly connects to
  cluster_span     — how many distinct clusters its neighbours span
  pagerank         — global importance (handles indirect reach)
  cluster_size     — size of the cluster it anchors (bigger = broader topic)
  rl_weight        — learned positive feedback from past learners (rag.weights
                     paper/wiki priors, summed where applicable)
  has_wiki         — boolean bonus if a wiki page exists (lesson is cheap)

Each signal is min-max normalized across the candidate pool, then mixed
with configurable weights into a single fundamentalness score.

The ranker returns ordered Foundation entries with a short, human-readable
rationale string the UI can show on the entry page.

Public:
  recommend(limit=5)                → list[Foundation]
  recommend_for_interest(text, limit=5) → list[Foundation]   (token-overlap boost)
  Foundation: dataclass with name, score, rationale, cluster_id, cluster_name
"""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"


@dataclass
class Foundation:
    name: str                # human-readable label
    raw_name: str            # graph-internal label (underscored)
    score: float
    rationale: str
    cluster_id: int
    cluster_name: str
    metrics: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


# ── Mix weights (env-overridable) ──────────────────────────────────────────

import os

W_DEGREE       = float(os.environ.get("FOUND_W_DEGREE", 0.30))
W_CLUSTER_SPAN = float(os.environ.get("FOUND_W_CLUSTER_SPAN", 0.30))
W_PAGERANK     = float(os.environ.get("FOUND_W_PAGERANK", 0.20))
W_CLUSTER_SIZE = float(os.environ.get("FOUND_W_CLUSTER_SIZE", 0.10))
W_RL_WEIGHT    = float(os.environ.get("FOUND_W_RL", 0.10))


# ── Helpers ────────────────────────────────────────────────────────────────

def _humanize(n: str) -> str:
    return n.replace("_", " ").strip()


def _has_wiki(name: str) -> bool:
    candidates = [
        name, name.replace(" ", "_"), name.replace(" ", "-"),
    ]
    for c in candidates:
        if (WIKI_CONCEPTS / f"{c}.md").exists():
            return True
    return False


def _minmax(d: dict[str, float]) -> dict[str, float]:
    if not d:
        return {}
    vals = list(d.values())
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        return {k: 0.5 for k in d}
    return {k: (v - lo) / (hi - lo) for k, v in d.items()}


# ── Public scoring ────────────────────────────────────────────────────────

def recommend(limit: int = 5, candidate_cap: int = 200) -> list[Foundation]:
    """Score every plausible candidate and return the top `limit`.

    `candidate_cap` bounds the per-cluster set we pull pagerank/etc on, since
    PageRank on the full graph is fine but iterating ALL nodes for the
    explanation strings would be slow.
    """
    try:
        import networkx as nx
        from graph.clusters import load_clusters, build_clusters, load_graph
    except ImportError:
        return []

    clusters = load_clusters() or build_clusters(force=False)
    if not clusters:
        return []
    G = load_graph()
    if G is None or G.number_of_nodes() == 0:
        return []

    # Build node→cluster map
    node_to_cid: dict[str, int] = {}
    cluster_by_id = {c.cluster_id: c for c in clusters}
    for c in clusters:
        for m in c.members:
            node_to_cid[m] = c.cluster_id

    # PageRank once over the full graph
    try:
        pr_full = nx.pagerank(G, weight="weight")
    except Exception:
        # Fallback: degree-only score
        pr_full = {n: G.degree(n) / max(1, G.number_of_edges())
                   for n in G.nodes()}

    # Candidate pool: top-N highest-degree nodes per cluster.
    candidates: list[str] = []
    for c in clusters:
        # Top 8 in each cluster — equiv to top_nodes plus their immediate
        # cluster context (only use names actually present in G)
        for n in c.members[: 12]:
            if n in G:
                candidates.append(n)
        if len(candidates) >= candidate_cap:
            break

    # PARA bucket boost: Resources/Areas favored, Archives downweighted
    para_for_node = _para_lookup(candidates)

    # Per-candidate metrics
    deg = {n: int(G.degree(n)) for n in candidates}
    span: dict[str, int] = {}
    for n in candidates:
        cids = set()
        for nbr in G.neighbors(n):
            cid = node_to_cid.get(nbr)
            if cid is not None:
                cids.add(cid)
        span[n] = len(cids)
    pr = {n: float(pr_full.get(n, 0.0)) for n in candidates}
    csize = {n: len(cluster_by_id.get(node_to_cid.get(n, -1)).members)
             if node_to_cid.get(n) in cluster_by_id else 0
             for n in candidates}
    rl = _rl_weights_for(candidates)

    # Normalize & mix
    n_deg   = _minmax(deg)
    n_span  = _minmax(span)
    n_pr    = _minmax(pr)
    n_csize = _minmax(csize)
    n_rl    = _minmax(rl)

    scored: list[tuple[float, str]] = []
    for n in candidates:
        s = (
            W_DEGREE       * n_deg.get(n, 0)
          + W_CLUSTER_SPAN * n_span.get(n, 0)
          + W_PAGERANK     * n_pr.get(n, 0)
          + W_CLUSTER_SIZE * n_csize.get(n, 0)
          + W_RL_WEIGHT    * n_rl.get(n, 0)
        )
        # Bonus: starting from a node with a wiki page is much more useful
        # than one without — the lesson can render immediately.
        if _has_wiki(n):
            s += 0.05
        # PARA bucket bias: Areas/Resources are good starting points;
        # Projects (active work) are less general; Archives are stale.
        bucket = para_for_node.get(n, "Resources")
        s += {"Areas": 0.04, "Resources": 0.02,
              "Projects": -0.03, "Archives": -0.10}.get(bucket, 0)
        scored.append((s, n))
    scored.sort(reverse=True)

    out: list[Foundation] = []
    seen_clusters: set[int] = set()
    for s, n in scored:
        cid = node_to_cid.get(n, -1)
        # Encourage diversity: don't return 5 starting points from the same
        # cluster. Allow at most 2 per cluster.
        if list(c == cid for c in [f.cluster_id for f in out]).count(True) >= 2:
            continue
        cluster = cluster_by_id.get(cid)
        cname = cluster.name if cluster else f"cluster-{cid}"
        rationale = _build_rationale(
            n, deg[n], span[n], csize[n], rl.get(n, 0.0),
            has_wiki=_has_wiki(n),
        )
        out.append(Foundation(
            name=_humanize(n),
            raw_name=n,
            score=round(s, 3),
            rationale=rationale,
            cluster_id=cid,
            cluster_name=cname,
            metrics={
                "degree":       deg[n],
                "cluster_span": span[n],
                "pagerank":     round(pr[n], 4),
                "cluster_size": csize[n],
                "rl_weight":    round(rl.get(n, 0.0), 3),
                "has_wiki":     _has_wiki(n),
            },
        ))
        if len(out) >= limit:
            break
    return out


def recommend_for_interest(interest: str, limit: int = 5) -> list[Foundation]:
    """Same as recommend(), but boost candidates whose name shares tokens
    with the learner's stated interest."""
    base = recommend(limit=limit * 4)
    if not interest.strip():
        return base[:limit]
    toks = {t.lower() for t in re.findall(r"[a-zA-Z]{4,}", interest)}
    if not toks:
        return base[:limit]

    def _overlap(name: str) -> int:
        nt = {t.lower() for t in re.findall(r"[a-zA-Z]{4,}", name)}
        return len(nt & toks)

    boosted = []
    for f in base:
        bump = 0.10 * _overlap(f.name)
        boosted.append((f.score + bump, f))
    boosted.sort(key=lambda t: t[0], reverse=True)

    # De-dupe + cap
    out: list[Foundation] = []
    seen_clusters: set[int] = set()
    for s, f in boosted:
        # Allow at most 2 per cluster, like recommend()
        if [x.cluster_id for x in out].count(f.cluster_id) >= 2:
            continue
        f2 = Foundation(**{**f.to_dict(), "score": round(s, 3)})
        out.append(f2)
        if len(out) >= limit:
            break
    return out


# ── Rationale builder ──────────────────────────────────────────────────────

def _build_rationale(name: str, degree: int, span: int, csize: int,
                     rl: float, *, has_wiki: bool) -> str:
    """One sentence explaining why this node is a good place to start.

    Always emits at least three signal phrases so every card carries the
    same information shape — bridge span, connection count, and course
    size. Keeps cards visually balanced even when one signal is weak.
    """
    parts: list[str] = []

    # Bridge span — always emit
    if span >= 3:
        parts.append(f"bridges {span} courses")
    elif span == 2:
        parts.append("bridges two courses")
    elif span == 1:
        parts.append("anchored in one course")
    else:
        parts.append("isolated within its course")

    # Connection count — always emit
    if degree >= 8:
        parts.append(f"connects to {degree} other concepts")
    elif degree >= 3:
        parts.append(f"{degree} direct connections")
    else:
        parts.append(f"degree {degree}")

    # Course size — always emit (with size-aware phrasing)
    if csize >= 50:
        parts.append(f"anchors a {csize}-concept course")
    elif csize >= 15:
        parts.append(f"in a {csize}-concept course")
    elif csize > 0:
        parts.append(f"small {csize}-concept course")

    # Optional: RL feedback (only when meaningful)
    if rl > 0.05:
        parts.append("learners gave it strong feedback")

    # Optional: missing wiki
    if not has_wiki:
        parts.append("no wiki page yet")

    return "; ".join(parts) + "."


# ── PARA bucket lookup ─────────────────────────────────────────────────────

def _para_lookup(names: list[str]) -> dict[str, str]:
    """Return {node_name: PARA bucket} via cheap heuristic on the wiki page
    if present (frontmatter `para:` → tag #project/#area/#resource/#archive
    → folder → 'Resources' fallback)."""
    out: dict[str, str] = {}
    if not WIKI_CONCEPTS.exists():
        return {n: "Resources" for n in names}
    for n in names:
        candidates = [n, n.replace(" ", "_"), n.replace(" ", "-")]
        path = None
        for c in candidates:
            p = WIKI_CONCEPTS / f"{c}.md"
            if p.exists():
                path = p
                break
        if path is None:
            out[n] = "Resources"
            continue
        try:
            head = path.read_text(errors="ignore")[:1500]
        except Exception:
            out[n] = "Resources"
            continue
        # Frontmatter `para:` first
        m = re.search(r"^---\s*\n(.*?)\n---", head, re.DOTALL)
        para_value = None
        tags_in_fm: list[str] = []
        if m:
            for ln in m.group(1).splitlines():
                if ":" not in ln:
                    continue
                k, _, v = ln.partition(":")
                if k.strip().lower() == "para":
                    para_value = v.strip().strip('"').strip("'").lower()
                if k.strip().lower() == "tags":
                    tags_in_fm = [t.strip() for t in v.split(",") if t.strip()]
        if para_value:
            for cand in ("Projects", "Areas", "Resources", "Archives"):
                if cand.lower().startswith(para_value):
                    out[n] = cand
                    break
            else:
                out[n] = "Resources"
            continue
        body_tags = re.findall(r"(?<!\S)#([A-Za-z][\w/\-]+)", head)
        all_tags = {t.lower() for t in (body_tags + tags_in_fm)}
        for cand in ("Projects", "Areas", "Resources", "Archives"):
            if cand.lower()[:-1] in all_tags or cand.lower() in all_tags:
                out[n] = cand
                break
        else:
            out[n] = "Resources"
    return out


# ── RL weight lookup ──────────────────────────────────────────────────────

def _rl_weights_for(names: list[str]) -> dict[str, float]:
    """Sum the learned `wiki` weights for each candidate name (best-effort)."""
    out: dict[str, float] = {n: 0.0 for n in names}
    try:
        from rag.weights import get
    except ImportError:
        return out
    for n in names:
        # Try several key formats — graph node names use underscores, while
        # the prior store may use either spaces or underscores depending on
        # which credit-assignment path wrote the entry.
        for k in (n, n.replace(" ", "_"), _humanize(n)):
            try:
                w = get("wiki", k, 1.0)
            except Exception:
                w = 1.0
            if w != 1.0:
                # Strongest-evidence win
                out[n] = max(out[n], w - 1.0)   # delta from neutral
                break
    return out
