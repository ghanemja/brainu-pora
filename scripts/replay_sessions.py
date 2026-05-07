"""
Replay logged sessions through the RL credit-assignment pipeline.

When you change reward shaping (RL_POS_DELTA, RL_NEG_DELTA, etc.) you don't
need to re-run debates — just replay the existing logs. This script:

  1. Optionally clears existing weights (--reset)
  2. Replays every record in data/sessions/sessions.jsonl in order
  3. For each `feedback` event, looks up the matching turn in turns.jsonl
     and applies the (now-current) credit deltas

Usage:
    python3 scripts/replay_sessions.py
    python3 scripts/replay_sessions.py --reset   # zero weights first
    python3 scripts/replay_sessions.py --since 2026-01-01

Skips the lifecycle EWMA replay — that's path-dependent on the original
order of feedback. Just use it for graph weight recomputation.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

SESSIONS_LOG = PROJECT_ROOT / "data" / "sessions" / "sessions.jsonl"
TURNS_LOG    = PROJECT_ROOT / "data" / "sessions" / "turns.jsonl"


def _index_turns() -> dict[str, dict]:
    """turn_id → record map for O(1) lookup."""
    out: dict[str, dict] = {}
    if not TURNS_LOG.exists():
        return out
    for line in TURNS_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("turn_id"):
            out[obj["turn_id"]] = obj
    return out


def _reset_weights() -> None:
    """Clear `weight` property on every edge."""
    from graph.temporal_graph import _get_driver, _run
    drv = _get_driver()
    cypher = """
    MATCH ()-[r:RELATES_TO]->()
    WHERE r.weight IS NOT NULL
    REMOVE r.weight, r.last_credit_at
    RETURN count(r) AS n
    """
    rs, _, _ = _run(drv.execute_query(cypher))
    n = next((dict(r).get("n", 0) for r in rs), 0)
    print(f"  cleared weight on {n} edges")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true",
                    help="Drop all weights before replay")
    ap.add_argument("--since", default=None,
                    help="Only replay events after ISO date (e.g. 2026-01-01)")
    args = ap.parse_args()

    if not SESSIONS_LOG.exists():
        sys.exit(f"✗ {SESSIONS_LOG} not found — nothing to replay")

    if args.reset:
        print("[1/3] Resetting graph weights...")
        try:
            _reset_weights()
        except Exception as e:
            print(f"  reset failed (continuing anyway): {e}")

    print("[2/3] Indexing turns.jsonl...")
    turns = _index_turns()
    print(f"  indexed {len(turns)} turns")

    cutoff = None
    if args.since:
        cutoff = datetime.fromisoformat(args.since).timestamp()

    print("[3/3] Replaying sessions.jsonl...")
    from agents.feedback import _apply_credit_safe, POS_DELTA, NEG_DELTA, HEBBIAN_DELTA

    n_prompt, n_feedback, n_skipped = 0, 0, 0
    with SESSIONS_LOG.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if cutoff and obj.get("ts", 0) < cutoff:
                continue

            kind = obj.get("kind")
            if kind == "prompt":
                # No turns to look up — Hebbian deltas come from prompt itself
                # We can't redo that without the original prompt; just count.
                n_prompt += 1
            elif kind == "feedback":
                tid = obj.get("turn_id")
                turn = turns.get(tid)
                if turn is None:
                    n_skipped += 1
                    continue
                score = obj.get("score", 0.0)
                if score > 0:
                    delta = POS_DELTA * score
                else:
                    delta = NEG_DELTA * abs(score)
                targets = turn.get("citations", [])
                _apply_credit_safe(targets, delta)
                n_feedback += 1

    print(f"\n[Done] prompts={n_prompt}  feedback={n_feedback}  skipped={n_skipped}")


if __name__ == "__main__":
    main()
