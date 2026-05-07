"""Temporal knowledge graph layer (Graphiti + FalkorDB).

Provides a get_graph() singleton + helpers for:
  - seeding the graph from existing wiki pages
  - ingesting new sources with temporal validity
  - querying current vs historical state
  - exporting node/edge snapshots for the UI time-slider
"""

from .temporal_graph import (
    get_graph,
    add_episode,
    search_nodes,
    search_facts,
    snapshot_at,
)

__all__ = [
    "get_graph",
    "add_episode",
    "search_nodes",
    "search_facts",
    "snapshot_at",
]
