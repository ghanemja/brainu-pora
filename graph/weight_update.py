"""
Edge-weight updates for the brain graph (FalkorDB / Graphiti).

Every RELATES_TO edge has an optional `weight` property (default 1.0). The RL
system bumps or decrements it via Cypher when feedback arrives on a response
that cited the corresponding entities.

Three credit kinds, three matchers:
  apply_to_entity(name, delta)   → weight on every edge touching node `name`
  apply_to_wiki(page_slug, delta) → weight on edges sourced from that wiki page
  apply_to_arxiv(paper_id, delta) → weight on edges sourced from that arXiv paper

Plus:
  decay_all(rate)                → multiply every weight by `rate` (0<rate<1)
                                   — call once per session for eligibility-trace
                                   decay so old credits fade.

All operations no-op gracefully if FalkorDB / Graphiti is offline so the rest
of the app keeps working.
"""

from __future__ import annotations

import os
from typing import Iterable


GROUP_ID = os.environ.get("GRAPHITI_GROUP", "gemma_eng_wiki")


def _driver():
    """Return FalkorDB driver, or None if unavailable."""
    try:
        from graph.temporal_graph import _get_driver
        return _get_driver()
    except Exception:
        return None


def _run_cypher(cypher: str, params: dict | None = None) -> dict:
    """Execute Cypher, returning {ok, rows, error}. Never raises."""
    drv = _driver()
    if drv is None:
        return {"ok": False, "rows": [], "error": "falkordb driver unavailable"}
    try:
        from graph.temporal_graph import _run
        records, _, _ = _run(drv.execute_query(cypher, params or {}))
        return {"ok": True, "rows": [dict(r) for r in records], "error": None}
    except Exception as e:
        return {"ok": False, "rows": [], "error": f"{type(e).__name__}: {e}"}


# ── Public API ─────────────────────────────────────────────────────────────

def apply_to_entity(name: str, delta: float, group_id: str | None = None) -> dict:
    """Bump weight on every active edge touching node `name`.

    `name` matches case-insensitively against Entity.name. We update the
    `weight` property on outgoing AND incoming edges (so an entity gets
    credit no matter which direction its mention came from).
    """
    gid = group_id or GROUP_ID
    cypher = f"""
    MATCH (n)-[r:RELATES_TO]-()
    WHERE toLower(n.name) = toLower($name)
      AND r.group_id = '{gid}'
      AND (r.invalid_at IS NULL OR r.invalid_at = '' OR r.invalid_at = 'None')
    SET r.weight = coalesce(r.weight, 1.0) + $delta,
        r.last_credit_at = $ts
    RETURN count(r) AS n_updated
    """
    import time
    return _run_cypher(cypher, {"name": name, "delta": float(delta),
                                "ts": time.time()})


def apply_to_wiki(page_slug: str, delta: float,
                  group_id: str | None = None) -> dict:
    """Bump weight on edges that came from a wiki page episode.

    Graphiti tags every edge with the source episode's `name`, which for
    wiki ingestion is the page stem. Match on that.
    """
    gid = group_id or GROUP_ID
    # Strip path prefix if any: "concepts/Foo.md" → "Foo"
    slug = page_slug.split("/")[-1].replace(".md", "")
    cypher = f"""
    MATCH ()-[r:RELATES_TO]->()
    WHERE r.group_id = '{gid}'
      AND r.episodes IS NOT NULL
      AND any(e IN r.episodes WHERE e CONTAINS $slug)
    SET r.weight = coalesce(r.weight, 1.0) + $delta,
        r.last_credit_at = $ts
    RETURN count(r) AS n_updated
    """
    import time
    return _run_cypher(cypher, {"slug": slug, "delta": float(delta),
                                "ts": time.time()})


def apply_to_arxiv(paper_id: str, delta: float,
                   group_id: str | None = None) -> dict:
    """Bump weight on edges sourced from a specific arXiv paper.

    Defense corpus + arXiv ingestion uses paper_id (e.g. '2603.21148') in
    the episode name. Match on substring of source_description / episodes.
    """
    gid = group_id or GROUP_ID
    cypher = f"""
    MATCH ()-[r:RELATES_TO]->()
    WHERE r.group_id = '{gid}'
      AND ((r.source_description IS NOT NULL AND r.source_description CONTAINS $pid)
           OR (r.episodes IS NOT NULL AND any(e IN r.episodes WHERE e CONTAINS $pid)))
    SET r.weight = coalesce(r.weight, 1.0) + $delta,
        r.last_credit_at = $ts
    RETURN count(r) AS n_updated
    """
    import time
    return _run_cypher(cypher, {"pid": paper_id, "delta": float(delta),
                                "ts": time.time()})


def decay_all(rate: float = 0.99, group_id: str | None = None) -> dict:
    """Multiply every weight by `rate`. Call once per session.

    rate < 1.0 implements an eligibility-trace style decay: credit assigned
    last week fades, credit assigned this turn is fresh. Floor at 0.05 so
    weights don't underflow to zero (you'd lose entities entirely).
    """
    gid = group_id or GROUP_ID
    cypher = f"""
    MATCH ()-[r:RELATES_TO]->()
    WHERE r.group_id = '{gid}'
      AND r.weight IS NOT NULL
    SET r.weight = CASE
        WHEN r.weight * $rate < 0.05 THEN 0.05
        ELSE r.weight * $rate END
    RETURN count(r) AS n_updated
    """
    return _run_cypher(cypher, {"rate": float(rate)})


def get_weights(names: Iterable[str], group_id: str | None = None) -> dict:
    """Lookup current weights for a set of entity names. Useful for UI / debug."""
    gid = group_id or GROUP_ID
    name_list = [n for n in names if n]
    if not name_list:
        return {"ok": True, "rows": [], "error": None}
    cypher = f"""
    MATCH (n)-[r:RELATES_TO]-()
    WHERE r.group_id = '{gid}'
      AND toLower(n.name) IN [x IN $names | toLower(x)]
    RETURN n.name AS name, avg(coalesce(r.weight, 1.0)) AS avg_weight,
           count(r) AS n_edges
    """
    return _run_cypher(cypher, {"names": list(name_list)})


# ── Batched helper for full credit-assignment from a TurnCitations ─────────

def apply_credit(targets: list[tuple[str, str]], delta: float,
                 group_id: str | None = None) -> dict:
    """Apply `delta` across a flat list of (kind, key) credit targets.

    kind ∈ {arxiv, wiki, tool, entity}.  tool credits are a no-op for now —
    tools don't have graph edges, but we keep them in the API for symmetry.
    Returns {n_targets, n_edges_updated, errors:[…]}.
    """
    n_edges = 0
    errors: list[str] = []
    for kind, key in targets:
        if kind == "arxiv":
            # key is "category/paper_id"
            paper = key.split("/", 1)[-1]
            r = apply_to_arxiv(paper, delta, group_id)
        elif kind == "wiki":
            r = apply_to_wiki(key, delta, group_id)
        elif kind == "entity":
            r = apply_to_entity(key, delta, group_id)
        else:
            continue
        if not r.get("ok"):
            errors.append(f"{kind}/{key}: {r.get('error')}")
            continue
        for row in r["rows"]:
            n_edges += int(row.get("n_updated", 0))
    return {"n_targets": len(targets), "n_edges_updated": n_edges, "errors": errors}
