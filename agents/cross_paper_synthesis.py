"""
Cross-paper / cross-concept synthesis episodes.

Given a graph cluster (Louvain community from graph/clusters.py), produce
a long-form podcast episode that braids together 3-6 source concepts +
their underlying papers into a single conversational arc.

Map:
  cluster.top_nodes  → individual wiki pages + linked defense-corpus papers
  cluster.bridges    → cross-cluster callbacks the hosts can use as hooks
  cluster.name       → episode "season" label

Output: a PodcastScript dict (same shape as podcast_script.generate_script),
ready for podcast_video.render().
"""

from __future__ import annotations

from . import podcast_script


SYSTEM_PROMPT = podcast_script.SYSTEM_PROMPT + """

CROSS-PAPER MODE:
This is a synthesis episode, not a single-paper deep-dive. You have 3-6
related source concepts (each with its own wiki + paper). Your job:

- Open by naming the THEME (the cluster name) and the tension that ties
  the sources together (e.g. "they all use X but disagree about Y").
- Visit each source in turn, but only ~3 turns per source — then HAND OFF
  to the next via an explicit bridge ("which connects to..." / "the same
  pattern shows up in...").
- The worked example should compare two sources side-by-side with numbers.
- Use cluster-bridge callbacks: name another cluster the listener could
  branch into next.
"""


def synthesize_episode(
    cluster,
    length: str = "long",
    angle: str = "",
    force: bool = False,
) -> dict | None:
    """Generate a cross-paper synthesis script from a graph cluster."""
    source = podcast_script.source_from_cluster(cluster)
    if not source.strip():
        return None
    topic = f"{getattr(cluster, 'name', 'this cluster')} — synthesis episode"

    # Use the cross-paper system prompt by monkey-patching the system var
    original_system = podcast_script.SYSTEM_PROMPT
    try:
        podcast_script.SYSTEM_PROMPT = SYSTEM_PROMPT
        script = podcast_script.generate_script(
            topic=topic,
            source_text=source,
            length=length,
            angle=angle or f"connect the sources under '{getattr(cluster, 'name', '?')}'",
            force=force,
        )
    finally:
        podcast_script.SYSTEM_PROMPT = original_system

    if not script:
        return None

    # Annotate with cluster metadata so renderer can build branding
    script["kind"] = "cross_paper"
    script["cluster_id"] = getattr(cluster, "cluster_id", None)
    script["cluster_name"] = getattr(cluster, "name", None)
    script["source_nodes"] = [n for n, _ in (cluster.top_nodes or [])[:6]]
    return script
