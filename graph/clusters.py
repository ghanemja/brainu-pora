"""
Cluster the brain graph into "courses" via community detection.

Two graph sources, in order of preference:
  1. Graphiti / FalkorDB edges (live graph)  — uses entity-relation-entity
  2. Wiki cross-references (fallback)        — parses [[wiki/X]] links between
                                               wiki/concepts/*.md pages

Either way we end up with a networkx undirected graph, run Louvain community
detection, and emit:

  Cluster:
    cluster_id    int
    name          str   (highest-degree node — the "course title")
    members       list[str]   (all node names in cluster)
    top_nodes     list[(name, degree)]  (top 8 lesson candidates)
    bridges       list[(name, [other_cluster_ids…])]  (nodes that connect to
                                                       other clusters — these
                                                       are the "transfer-credit"
                                                       nodes the UI uses to
                                                       jump courses)

Persisted to:
  data/sessions/clusters.json

Public:
  build_clusters(force=False)   → list[Cluster]
  load_clusters()               → cached list[Cluster] or None
  cluster_for_node(name)        → cluster id or None
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict, Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"
CLUSTERS_PATH = PROJECT_ROOT / "data" / "sessions" / "clusters.json"
CLUSTERS_PATH.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class Cluster:
    cluster_id: int
    name: str
    members: list[str]
    top_nodes: list[tuple[str, int]]
    bridges: list[tuple[str, list[int]]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "members": self.members,
            "top_nodes": self.top_nodes,
            "bridges": self.bridges,
        }


# ── Graph loaders ──────────────────────────────────────────────────────────

def _load_from_graphiti() -> "networkx.Graph | None":
    """Pull all active edges from Graphiti; build undirected nx graph."""
    try:
        import networkx as nx
        from graph.temporal_graph import _get_driver, _run, GROUP_ID
    except Exception:
        return None
    try:
        drv = _get_driver()
    except Exception:
        return None
    cypher = f"""
    MATCH (s)-[r:RELATES_TO]->(o)
    WHERE r.group_id = '{GROUP_ID}'
      AND (r.invalid_at IS NULL OR r.invalid_at = '' OR r.invalid_at = 'None')
    RETURN s.name AS source, o.name AS target,
           coalesce(r.weight, 1.0) AS weight
    LIMIT 5000
    """
    try:
        records, _, _ = _run(drv.execute_query(cypher))
    except Exception:
        return None
    G = __import__("networkx").Graph()
    for rec in records:
        d = dict(rec)
        s, t, w = d.get("source"), d.get("target"), float(d.get("weight") or 1.0)
        if not s or not t:
            continue
        if G.has_edge(s, t):
            G[s][t]["weight"] += w
        else:
            G.add_edge(s, t, weight=w)
    return G if G.number_of_edges() > 0 else None


WIKI_LINK_RE = re.compile(r"\[\[wiki/([\w/_.-]+?)\]\]")
WIKI_INTERNAL_RE = re.compile(r"\[\[([\w_]+?)\]\]")  # plain [[Foo_bar]]


def _load_from_wiki() -> "networkx.Graph":
    """Build a graph from wiki cross-links. Each page is a node; every
    [[wiki/X]] or [[X]] in the body becomes an edge."""
    import networkx as nx
    G = nx.Graph()
    if not WIKI_CONCEPTS.exists():
        return G
    pages: dict[str, str] = {}
    for p in WIKI_CONCEPTS.glob("*.md"):
        try:
            pages[p.stem] = p.read_text(errors="ignore")
        except Exception:
            continue
    page_set = set(pages.keys())
    for stem, body in pages.items():
        G.add_node(stem)
        # explicit [[wiki/...]] links
        for m in WIKI_LINK_RE.finditer(body):
            tgt = m.group(1).split("/")[-1].replace(".md", "")
            if tgt and tgt != stem:
                G.add_edge(stem, tgt)
        # bare [[Title]] links — only follow if target exists as a page
        for m in WIKI_INTERNAL_RE.finditer(body):
            tgt = m.group(1)
            if tgt in page_set and tgt != stem:
                G.add_edge(stem, tgt)
        # Same-token co-occurrence: each TitleCase token in body that
        # matches a page name = soft co-occurrence edge
        toks = re.findall(r"\b([A-Z][a-z]{3,})\b", body)
        for tok in set(toks):
            if tok in page_set and tok != stem:
                if G.has_edge(stem, tok):
                    G[stem][tok]["weight"] = G[stem][tok].get("weight", 1) + 1
                else:
                    G.add_edge(stem, tok, weight=1)
    return G


# ── Community detection ────────────────────────────────────────────────────

def _detect_communities(G) -> list[set[str]]:
    """Louvain → list of node-sets per community."""
    import networkx as nx
    if G.number_of_nodes() == 0:
        return []
    try:
        # NX 3.x location
        from networkx.algorithms.community import louvain_communities
        return list(louvain_communities(G, weight="weight", seed=42))
    except Exception:
        try:
            # python-louvain fallback
            import community as community_louvain
            partition = community_louvain.best_partition(G, weight="weight")
            comm_map: dict[int, set[str]] = defaultdict(set)
            for node, cid in partition.items():
                comm_map[cid].add(node)
            return list(comm_map.values())
        except Exception:
            # Worst-case: connected components
            return [set(c) for c in nx.connected_components(G)]


# ── Public API ─────────────────────────────────────────────────────────────

def build_clusters(force: bool = False, source: str = "auto",
                   max_clusters: int = 30,
                   vault_path: str | None = None) -> list[Cluster]:
    """Detect clusters and persist to disk.

    source ∈ {"auto", "graphiti", "wiki", "obsidian"}
      auto: graphiti → obsidian (if vault) → wiki, in that order.
      graphiti: hard-fail to wiki only when graphiti unreachable.
      wiki: ignore graphiti even if online.
      obsidian: load from `vault_path` (or OBSIDIAN_VAULT env / default
                 ~/Documents/* search) — never touches graphiti.
    """
    if not force:
        cached = load_clusters()
        if cached:
            return cached

    G = None
    if source in ("auto", "graphiti"):
        G = _load_from_graphiti()
    if G is None or G.number_of_edges() == 0:
        if source in ("auto", "obsidian"):
            try:
                from graph.obsidian_loader import load_vault, find_default_vault
                vault = Path(vault_path).expanduser() if vault_path else find_default_vault()
                if vault and vault.is_dir():
                    G = load_vault(vault)
            except Exception:
                G = None
    if G is None or G.number_of_edges() == 0:
        G = _load_from_wiki()

    if G is None or G.number_of_nodes() == 0:
        return []

    communities = _detect_communities(G)
    # Sort by size desc; cap to max_clusters
    communities.sort(key=len, reverse=True)
    communities = communities[:max_clusters]

    # Build node→cluster_id map for bridge detection
    node_to_cid: dict[str, int] = {}
    for cid, members in enumerate(communities):
        for n in members:
            node_to_cid[n] = cid

    clusters: list[Cluster] = []
    for cid, members in enumerate(communities):
        # Degree within the full graph
        degrees = sorted(
            ((n, G.degree(n)) for n in members),
            key=lambda x: x[1], reverse=True,
        )
        top_nodes = degrees[:8]
        name = top_nodes[0][0] if top_nodes else f"cluster-{cid}"

        # Bridges: a node whose neighbours span multiple clusters
        bridges = []
        for n in members:
            other_cids: set[int] = set()
            for nbr in G.neighbors(n):
                ncid = node_to_cid.get(nbr)
                if ncid is not None and ncid != cid:
                    other_cids.add(ncid)
            if other_cids:
                bridges.append((n, sorted(other_cids)))
        # Keep top 10 bridges by node-degree (most-connected bridges first)
        bridges.sort(key=lambda x: G.degree(x[0]), reverse=True)
        bridges = bridges[:10]

        clusters.append(Cluster(
            cluster_id=cid,
            name=_humanize(name),
            members=[m for m, _ in degrees],   # ordered by degree
            top_nodes=[(_humanize(n), int(d)) for n, d in top_nodes],
            bridges=[(_humanize(n), cids) for n, cids in bridges],
        ))

    _persist(clusters)
    return clusters


def load_clusters() -> list[Cluster] | None:
    if not CLUSTERS_PATH.exists():
        return None
    try:
        blob = json.loads(CLUSTERS_PATH.read_text())
    except json.JSONDecodeError:
        return None
    out: list[Cluster] = []
    for d in blob:
        out.append(Cluster(
            cluster_id=int(d["cluster_id"]),
            name=str(d["name"]),
            members=list(d.get("members") or []),
            top_nodes=[(str(n), int(deg)) for n, deg in (d.get("top_nodes") or [])],
            bridges=[(str(n), [int(c) for c in cids]) for n, cids in (d.get("bridges") or [])],
        ))
    return out


def load_graph(source: str = "auto", vault_path: str | None = None):
    """Return the same networkx graph used to build clusters.

    source order matches build_clusters().  Used by visualizers that need
    the underlying edges (clusters.json only stores node labels, not edges).
    """
    G = None
    if source in ("auto", "graphiti"):
        G = _load_from_graphiti()
    if G is None or G.number_of_edges() == 0:
        if source in ("auto", "obsidian"):
            try:
                from graph.obsidian_loader import load_vault, find_default_vault
                vault = Path(vault_path).expanduser() if vault_path else find_default_vault()
                if vault and vault.is_dir():
                    G = load_vault(vault)
            except Exception:
                G = None
    if G is None or G.number_of_edges() == 0:
        G = _load_from_wiki()
    return G


def cluster_for_node(name: str) -> int | None:
    cs = load_clusters() or []
    target = name.lower().strip()
    for c in cs:
        for m in c.members:
            if _humanize(m).lower() == target:
                return c.cluster_id
    return None


def _persist(clusters: list[Cluster]) -> None:
    CLUSTERS_PATH.write_text(
        json.dumps([c.to_dict() for c in clusters], indent=2)
    )


def _humanize(name: str) -> str:
    """Replace underscores with spaces and trim noise."""
    return name.replace("_", " ").strip()
