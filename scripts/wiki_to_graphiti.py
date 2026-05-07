"""
One-time seed: import the existing wiki/concepts/*.md pages into Graphiti.

For each markdown page:
  - The page itself becomes an episode (text source)
  - Graphiti auto-extracts entities + relationships
  - reference_time = the file's last-modified time (so the temporal axis
    reflects when each concept was actually added to the wiki)

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 scripts/wiki_to_graphiti.py
    python3 scripts/wiki_to_graphiti.py --max 100   # smoke-test on subset
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"
WIKI_SOURCES = PROJECT_ROOT / "wiki" / "sources"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=None,
                    help="Cap number of pages to ingest (for testing)")
    ap.add_argument("--include_sources", action="store_true",
                    help="Also ingest wiki/sources/*.md")
    ap.add_argument("--sleep", type=float, default=2.0,
                    help="Sleep between API calls (Anthropic rate limit)")
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("✗ ANTHROPIC_API_KEY not set — Graphiti needs it for entity extraction")

    # Defer import; needs graphiti-core installed
    try:
        from graph.temporal_graph import add_episode
    except ImportError as e:
        sys.exit(f"✗ Graphiti not installed: {e}\n  Run: docker/setup_graphiti.sh")

    pages = sorted(WIKI_CONCEPTS.glob("*.md"))
    if args.include_sources:
        pages += sorted(WIKI_SOURCES.glob("*.md"))
    if args.max:
        pages = pages[:args.max]

    print(f"[Wiki→Graphiti] Ingesting {len(pages)} pages...")

    stats = {"ok": 0, "errors": 0, "nodes_added": 0,
             "edges_added": 0, "invalidated": 0}

    for i, page in enumerate(pages, 1):
        body = page.read_text(encoding="utf-8")
        ref_time = datetime.fromtimestamp(page.stat().st_mtime, tz=timezone.utc)
        t0 = time.time()
        print(f"  [{i}/{len(pages)}] {page.stem[:60]}...", flush=True)

        try:
            r = add_episode(
                name=page.stem,
                episode_body=body[:8000],   # cap for cost
                reference_time=ref_time,
                source_description=f"wiki/concepts/{page.name}",
            )
            stats["ok"] += 1
            stats["nodes_added"] += r["n_nodes_added"]
            stats["edges_added"] += r["n_edges_added"]
            stats["invalidated"] += r["n_invalidated"]
            print(f"      ✓ {time.time()-t0:.1f}s · +{r['n_nodes_added']}n / "
                  f"+{r['n_edges_added']}e · totals: {stats['nodes_added']}n {stats['edges_added']}e "
                  f"{stats['invalidated']}inv", flush=True)
        except Exception as e:
            stats["errors"] += 1
            print(f"      ✗ {type(e).__name__}: {str(e)[:200]}", flush=True)
        time.sleep(args.sleep)

    print(f"\n[Done] {stats}")


if __name__ == "__main__":
    main()
