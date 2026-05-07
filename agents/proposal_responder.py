"""
Proposal-to-brain connector.

Take any free-text idea / proposal / question from the user, find the
concepts in our knowledge base it touches, and produce a grounded
response that:

  1. Lists the matched concepts (vault + RAG + Graphiti) with relevance.
  2. Walks the graph between them to surface bridge concepts the user
     may not have realised connected their ideas.
  3. Returns a one-paragraph "what the brain says about this" synthesis
     — heuristic by default, Claude-grounded if RL_PROPOSAL_LLM is set.

This is the "novel value" beyond plain Obsidian: not just storing notes,
but having the graph respond to a proposal by tying it to existing
knowledge and surfacing structural connections.

Public:
  respond(text, k=8) → {
    'matched_concepts':  [{name, source, score, ...}],
    'bridge_paths':      [{a, b, path:[…], length}],
    'synthesis':         str,
    'related_corpus':    {rag, defense, wiki, wikipedia},
    'mode':              'heuristic' | 'llm',
  }
"""

from __future__ import annotations

import os
import re
from typing import Iterable

TOK = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in TOK.findall(text) if len(t) > 3}


# ── Match user text against the vault graph ───────────────────────────────

def _match_concepts(text: str, vault_path: str | None = None,
                     k: int = 12) -> list[dict]:
    """Score every node in the brain graph by token overlap with the text.

    Cheap, deterministic, no LLM. Returns top-k node hits with scores.
    """
    try:
        from graph.clusters import load_graph, load_clusters
    except ImportError:
        return []
    G = load_graph(source="auto", vault_path=vault_path)
    if G is None or G.number_of_nodes() == 0:
        return []
    clusters = load_clusters() or []
    n2c = {}
    cluster_by_id = {c.cluster_id: c for c in clusters}
    for c in clusters:
        for m in c.members:
            n2c[m] = c.cluster_id

    text_toks = _tokens(text)
    if not text_toks:
        return []

    scored = []
    for node in G.nodes():
        node_toks = _tokens(node)
        if not node_toks:
            continue
        # Jaccard-ish + raw overlap
        overlap = len(node_toks & text_toks)
        if overlap == 0:
            # Substring match as cheaper fallback
            ln = node.replace("_", " ").lower()
            if any(t in ln for t in text_toks):
                overlap = 0.5
            else:
                continue
        score = overlap + (overlap / max(len(node_toks), 1)) * 0.5
        cid = n2c.get(node, -1)
        cname = cluster_by_id.get(cid).name if cid in cluster_by_id else "?"
        scored.append({
            "name":    node,
            "label":   node.replace("_", " "),
            "score":   round(float(score), 3),
            "degree":  G.degree(node),
            "cluster": cid,
            "cluster_name": cname,
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]


def _bridge_paths(matched: list[dict], vault_path: str | None,
                   max_paths: int = 5, max_len: int = 4) -> list[dict]:
    """For each pair of high-scoring matches, find the shortest path in
    the graph. Returns the most informative paths (shortest, novel-node-rich).
    """
    if len(matched) < 2:
        return []
    try:
        import networkx as nx
        from graph.clusters import load_graph
    except ImportError:
        return []
    G = load_graph(source="auto", vault_path=vault_path)
    if G is None:
        return []

    out: list[dict] = []
    seen_pairs: set[tuple[str, str]] = set()
    # Try the top-N candidates as path endpoints
    top = matched[:6]
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            a, b = top[i]["name"], top[j]["name"]
            key = tuple(sorted((a, b)))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            if a not in G or b not in G:
                continue
            try:
                path = nx.shortest_path(G, a, b)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
            if len(path) > max_len + 1:
                continue
            # Prefer paths that include intermediate nodes (genuine bridges)
            novelty = sum(1 for p in path[1:-1] if p not in {x["name"] for x in matched})
            out.append({
                "a":      a,
                "b":      b,
                "path":   path,
                "length": len(path) - 1,
                "novelty": novelty,
            })
    out.sort(key=lambda x: (x["length"], -x["novelty"]))
    return out[:max_paths]


# ── Synthesis ─────────────────────────────────────────────────────────────

def _heuristic_synthesis(text: str, matched: list[dict],
                         bridges: list[dict]) -> str:
    """Cheap rule-based summary. No LLM."""
    if not matched:
        return ("Nothing in the brain graph matches this proposal yet. "
                "It looks like a fresh seed — consider writing a wiki "
                "note for the central idea so future queries can find it.")
    top_names = ", ".join(f"**{m['label']}**" for m in matched[:3])
    parts = [
        f"The brain knows about {len(matched)} concepts that touch this "
        f"proposal — most relevant: {top_names}."
    ]
    # Cluster-distribution colour
    cluster_counts: dict[str, int] = {}
    for m in matched:
        cluster_counts[m["cluster_name"]] = cluster_counts.get(
            m["cluster_name"], 0) + 1
    multi_cluster = [c for c, n in cluster_counts.items() if n >= 1]
    if len(multi_cluster) >= 2:
        parts.append(
            f"Your idea spans {len(multi_cluster)} different courses "
            f"({', '.join(sorted(set(multi_cluster))[:4])}), so the answer "
            f"will need to integrate views from each."
        )
    if bridges:
        b = bridges[0]
        if b["length"] >= 2:
            mid = " → ".join(p.replace("_", " ") for p in b["path"])
            parts.append(
                f"In the graph, {b['a'].replace('_',' ')} reaches "
                f"{b['b'].replace('_',' ')} via: *{mid}* — that intermediate "
                f"path is worth reading before answering the proposal."
            )
    return " ".join(parts)


PROPOSAL_LLM_SYSTEM = """You are an expert knowledge navigator. The user
proposes an idea or asks a question. We've already searched the knowledge
graph and surfaced the most relevant concepts and bridge paths. Your job
is to write a single grounded paragraph (4-6 sentences) that:

  1. Restates the user's proposal in concrete technical terms.
  2. Names the 2-3 most relevant concepts the graph found.
  3. Surfaces any non-obvious connections from the bridge paths.
  4. Ends with the single best next-question to investigate.

Be specific. Avoid filler phrases. Cite concepts using markdown bold.
Output the paragraph only — no preface, no bullet list."""


def _llm_synthesis(text: str, matched: list[dict],
                   bridges: list[dict]) -> str:
    """Optional LLM synthesis — call the synthesizer model. Falls back to
    heuristic on any error or missing API key."""
    try:
        from agents.specialists import SYNTHESIZER_MODEL
        from agents.orchestrator import _call_claude
        ctx_parts = [f"PROPOSAL: {text}", ""]
        ctx_parts.append("MATCHED CONCEPTS (with cluster):")
        for m in matched[:8]:
            ctx_parts.append(f"  - {m['label']} (course: {m['cluster_name']}, "
                              f"degree: {m['degree']})")
        if bridges:
            ctx_parts.append("\nBRIDGE PATHS THROUGH THE GRAPH:")
            for b in bridges[:4]:
                p = " → ".join(x.replace("_", " ") for x in b["path"])
                ctx_parts.append(f"  - {p}")
        user_msg = "\n".join(ctx_parts)
        return _call_claude(
            model=SYNTHESIZER_MODEL,
            system=PROPOSAL_LLM_SYSTEM,
            user=user_msg,
            max_tokens=400,
            retries=1,
        ).strip()
    except Exception:
        return _heuristic_synthesis(text, matched, bridges)


# ── Public ─────────────────────────────────────────────────────────────────

def respond(text: str, k: int = 12, vault_path: str | None = None,
            mode: str = "auto") -> dict:
    """Main entry point.

    mode ∈ {auto, heuristic, llm}. auto = llm if ANTHROPIC_API_KEY else heuristic.
    """
    matched = _match_concepts(text, vault_path=vault_path, k=k)
    bridges = _bridge_paths(matched, vault_path=vault_path)

    if mode == "auto":
        mode_eff = "llm" if os.environ.get("ANTHROPIC_API_KEY") else "heuristic"
    else:
        mode_eff = mode

    if mode_eff == "llm":
        synthesis = _llm_synthesis(text, matched, bridges)
    else:
        synthesis = _heuristic_synthesis(text, matched, bridges)

    # Also pull related corpus content via the unified finder
    related: dict = {"rag": [], "defense": [], "wiki": None, "wikipedia": None}
    try:
        from agents.content_finder import find
        f = find(text, k=5, allow_web=False)
        related = {
            "rag":     f.get("rag", [])[:5],
            "defense": f.get("defense", [])[:5],
            "wiki":    f.get("wiki"),
            "wikipedia": f.get("wikipedia"),
        }
    except Exception:
        pass

    return {
        "matched_concepts": matched,
        "bridge_paths":     bridges,
        "synthesis":        synthesis,
        "related_corpus":   related,
        "mode":             mode_eff,
    }
