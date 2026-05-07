"""
Thin wrapper around graphiti-core + FalkorDB.

Public surface:
  get_graph()            → singleton Graphiti instance, configured for our env
  add_episode(...)       → ingest a piece of text with timestamp + source label
  search_nodes(query)    → semantic search over entity nodes
  search_facts(query)    → search over (entity-relation-entity) facts
  snapshot_at(t)         → return all edges valid at time t (for UI time-slider)

Why FalkorDB: lightweight Redis-based graph DB, runs in 1 Docker container,
< 100 MB RAM, fully Cypher-compatible. Swap to Neo4j by changing FALKOR_URI
to a bolt:// URL — no other code changes.
"""

from __future__ import annotations

import os
import asyncio
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any

# Graphiti is heavy — defer import until used so the rest of the codebase
# can import this module without requiring Graphiti to be installed.
_graphiti = None


FALKOR_URI = os.environ.get("FALKOR_URI", "redis://localhost:6379")
GROUP_ID = os.environ.get("GRAPHITI_GROUP", "gemma_eng_wiki")


_driver_cache: dict = {}


def _get_driver(group_id: str | None = None):
    """Driver per FalkorDB graph. Graphiti's add_episode uses group_id AS the
    graph name (not as a property), so reads must target the same graph."""
    db = group_id or GROUP_ID
    if db in _driver_cache:
        return _driver_cache[db]
    from graphiti_core.driver.falkordb_driver import FalkorDriver
    host = FALKOR_URI.replace("redis://", "").split(":")[0]
    port = int(FALKOR_URI.replace("redis://", "").split(":")[1]) if ":" in FALKOR_URI else 6379
    _driver_cache[db] = FalkorDriver(host=host, port=port, database=db)
    return _driver_cache[db]


def _build_llm_client():
    """LLM for entity extraction. Anthropic preferred, OpenAI fallback."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        from graphiti_core.llm_client.anthropic_client import AnthropicClient
        from graphiti_core.llm_client.config import LLMConfig
        return AnthropicClient(config=LLMConfig(
            model="claude-haiku-4-5",
            api_key=os.environ["ANTHROPIC_API_KEY"],
        ))
    if os.environ.get("OPENAI_API_KEY"):
        return None  # Graphiti default OpenAI client picks it up
    return None


def _build_embedder():
    """Embedder for vector search. Anthropic has no embeddings API, so we
    pick the first available alternative provider in priority order:
    Voyage (cheap) → Gemini (free tier) → OpenAI."""
    if os.environ.get("VOYAGE_API_KEY"):
        from graphiti_core.embedder.voyage import VoyageAIEmbedder, VoyageAIEmbedderConfig
        return VoyageAIEmbedder(config=VoyageAIEmbedderConfig(
            api_key=os.environ["VOYAGE_API_KEY"], embedding_model="voyage-3-lite",
        ))
    if os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"):
        from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
        return GeminiEmbedder(config=GeminiEmbedderConfig(
            api_key=os.environ.get("GOOGLE_API_KEY") or os.environ["GEMINI_API_KEY"],
            embedding_model="gemini-embedding-001",
        ))
    if os.environ.get("OPENAI_API_KEY"):
        from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
        return OpenAIEmbedder(config=OpenAIEmbedderConfig(
            api_key=os.environ["OPENAI_API_KEY"], embedding_model="text-embedding-3-small",
        ))
    return None


def get_graph():
    """Singleton Graphiti instance backed by FalkorDB.

    Requires:
      - LLM key: ANTHROPIC_API_KEY (preferred) or OPENAI_API_KEY
      - Embedder key: VOYAGE_API_KEY / GOOGLE_API_KEY / OPENAI_API_KEY
        (Anthropic has no embeddings API — must use a different provider.)
    """
    global _graphiti
    if _graphiti is not None:
        return _graphiti

    llm = _build_llm_client()
    embedder = _build_embedder()
    if embedder is None:
        raise RuntimeError(
            "No embedder key found. Set ONE of:\n"
            "  GOOGLE_API_KEY  (free tier — easiest, https://aistudio.google.com/apikey)\n"
            "  VOYAGE_API_KEY  (cheap, https://www.voyageai.com)\n"
            "  OPENAI_API_KEY  (paid)\n"
            "Anthropic has no embeddings API, so even with ANTHROPIC_API_KEY set "
            "Graphiti needs a separate provider for vector search."
        )

    from graphiti_core import Graphiti
    driver = _get_driver()
    kwargs = {"graph_driver": driver, "embedder": embedder}
    if llm is not None:
        kwargs["llm_client"] = llm

    # Cross-encoder (reranker) — Graphiti defaults to OpenAI. Match to whichever
    # provider's key is set, so we don't silently require OPENAI_API_KEY.
    cross_encoder = None
    if os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"):
        from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient
        from graphiti_core.llm_client.config import LLMConfig
        cross_encoder = GeminiRerankerClient(config=LLMConfig(
            api_key=os.environ.get("GOOGLE_API_KEY") or os.environ["GEMINI_API_KEY"],
            model="gemini-2.0-flash-exp",
        ))
    elif os.environ.get("OPENAI_API_KEY"):
        pass  # default works
    else:
        # No reranker provider — try BGE local model (sentence-transformers)
        try:
            from graphiti_core.cross_encoder.bge_reranker_client import BGERerankerClient
            cross_encoder = BGERerankerClient()
        except Exception:
            pass

    if cross_encoder is not None:
        kwargs["cross_encoder"] = cross_encoder

    _graphiti = Graphiti(**kwargs)
    return _graphiti


_loop = None


def _run(coro):
    """Run an async call on a single persistent loop. asyncio.run() per call
    closes the loop, which kills the embedder/LLM clients Graphiti caches."""
    global _loop
    try:
        running = asyncio.get_running_loop()
        # Already inside async context — use nest_asyncio
        import nest_asyncio
        nest_asyncio.apply()
        return running.run_until_complete(coro)
    except RuntimeError:
        pass
    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop.run_until_complete(coro)


# ── Public API ──────────────────────────────────────────────────────────────

def add_episode(name: str, episode_body: str, source: str = "text",
                 reference_time: datetime | None = None,
                 group_id: str | None = None,
                 source_description: str = "") -> dict:
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")):
        raise RuntimeError(
            "Graphiti needs an LLM key for entity extraction. "
            "Set ANTHROPIC_API_KEY (preferred) or OPENAI_API_KEY before ingesting."
        )
    """Ingest a piece of text. Graphiti will:
      1. Extract entities (with deduplication against existing)
      2. Extract relationships
      3. Detect contradictions with existing edges → invalidate old, add new
      4. All edges get t_valid = reference_time (defaults to now)
    """
    g = get_graph()
    if reference_time is None:
        reference_time = datetime.now(timezone.utc)
    from graphiti_core.nodes import EpisodeType
    type_map = {"text": EpisodeType.text, "json": EpisodeType.json,
                "message": EpisodeType.message}
    et = type_map.get(source, EpisodeType.text)

    result = _run(g.add_episode(
        name=name,
        episode_body=episode_body,
        source=et,
        reference_time=reference_time,
        group_id=group_id or GROUP_ID,
        source_description=source_description,
    ))
    return {
        "episode_id": getattr(result, "episode_uuid", None),
        "n_nodes_added": len(getattr(result, "nodes", []) or []),
        "n_edges_added": len(getattr(result, "edges", []) or []),
        "n_invalidated": len(getattr(result, "invalidated_edges", []) or []),
    }


def search_nodes(query: str, limit: int = 10,
                  group_id: str | None = None) -> list[dict]:
    """Hybrid (semantic + BM25 + graph-distance) search over entity nodes."""
    g = get_graph()
    results = _run(g.search(
        query=query,
        num_results=limit,
        group_ids=[group_id or GROUP_ID],
    ))
    out = []
    for r in results:
        out.append({
            "name": getattr(r, "name", ""),
            "summary": getattr(r, "summary", ""),
            "score": getattr(r, "score", None),
            "labels": getattr(r, "labels", []),
        })
    return out


def search_facts(query: str, limit: int = 10,
                  group_id: str | None = None) -> list[dict]:
    """Search edges (facts) currently valid + their provenance."""
    g = get_graph()
    edges = _run(g.search(
        query=query,
        num_results=limit,
        group_ids=[group_id or GROUP_ID],
        center_node_uuid=None,
    ))
    out = []
    for e in edges:
        out.append({
            "fact": getattr(e, "fact", str(e)),
            "valid_at": str(getattr(e, "valid_at", "")),
            "invalid_at": str(getattr(e, "invalid_at", "")),
            "source": getattr(e, "source_node_uuid", ""),
            "target": getattr(e, "target_node_uuid", ""),
        })
    return out


def snapshot_at(t: datetime, limit: int = 200,
                 group_id: str | None = None,
                 include_uuid: bool = True) -> dict:
    """Return all edges that were valid at time `t`.
    Used by the time-slider UI.

    When include_uuid=True, also returns per-edge `uuid` so the live UI can
    diff snapshots and animate newly-added / newly-invalidated edges.
    """
    gid = group_id or GROUP_ID
    driver = _get_driver(gid)
    uuid_col = ", r.uuid AS uuid" if include_uuid else ""
    t_iso = t.isoformat()
    # Graphiti uses group_id AS database name, so the entire current graph
    # already represents this group — no per-row filter needed.
    cypher = f"""
    MATCH (s)-[r:RELATES_TO]->(o)
    WHERE r.valid_at <= '{t_iso}'
      AND (r.invalid_at IS NULL OR r.invalid_at = '' OR r.invalid_at > '{t_iso}')
    RETURN s.name AS source, r.fact AS fact, o.name AS target,
           r.valid_at AS valid_at, r.invalid_at AS invalid_at,
           r.created_at AS created_at{uuid_col}
    ORDER BY r.created_at DESC
    LIMIT {int(limit)}
    """
    try:
        records, headers, _ = _run(driver.execute_query(cypher))
        edges = [dict(rec) for rec in records]
    except Exception as e:
        return {"error": str(e), "edges": []}

    return {"edges": edges, "as_of": t.isoformat()}


def recent_edges(since_seconds: int = 600, limit: int = 500,
                 group_id: str | None = None) -> dict:
    """Return all edges (active + invalidated) plus a 'is_recent' flag for
    edges created within the last `since_seconds`. Used by the live-brain UI
    to pulse newly-formed connections.
    """
    from datetime import timedelta
    gid = group_id or GROUP_ID
    driver = _get_driver(gid)
    cutoff_ms = int((datetime.now(timezone.utc) - timedelta(seconds=since_seconds)).timestamp() * 1000)
    cypher = f"""
    MATCH (s)-[r:RELATES_TO]->(o)
    RETURN s.name AS source, r.fact AS fact, o.name AS target,
           r.valid_at AS valid_at, r.invalid_at AS invalid_at,
           r.created_at AS created_at, r.uuid AS uuid
    ORDER BY r.created_at DESC
    LIMIT {int(limit)}
    """
    try:
        records, _, _ = _run(driver.execute_query(cypher))
        edges = []
        for rec in records:
            d = dict(rec)
            ca = d.get("created_at")
            d["is_recent"] = bool(ca) and (int(ca) if isinstance(ca, (int, float)) else 0) >= cutoff_ms
            d["is_invalidated"] = bool(d.get("invalid_at")) and d.get("invalid_at") not in ("", "None", "null")
            edges.append(d)
    except Exception as e:
        return {"error": str(e), "edges": []}
    return {"edges": edges, "cutoff_ms": cutoff_ms}
