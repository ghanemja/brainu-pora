"""
Time-travel — per-user historical mastery snapshots.

Drives a UI slider that scrubs through learning history. For any point in
time, we can compute "what did this user know on date X" by replaying
walk_events + sr_cards up to that timestamp.

Public:
  timeline(user_id) -> list[Snapshot]   keypoints (every walk, every quiz)
  snapshot_at(user_id, ts) -> dict      node-level mastery map at ts
  graph_state(user_id, ts) -> dict      summary for rendering: visited / mastered / total

Mastery for a node at ts:
  quiz_best_quality_up_to_ts / 5
  weighted by SR repetitions clamped to 3
"""

from __future__ import annotations

import time as _time
from typing import Iterable

from atp import db
from .persistence import ensure_schema  # import also applies migrations


def timeline(user_id: str) -> list[dict]:
    """Distinct timestamps where the user's state changed. Used as
    slider tick positions on the frontend."""
    ensure_schema()
    rows = db.query(
        """SELECT ts, node, quiz_quality FROM walk_events
             WHERE user_id = :user_id AND ts IS NOT NULL
             ORDER BY ts ASC""",
        {"user_id": user_id},
    )
    return [{"ts": r["ts"], "node": r["node"],
             "quiz_quality": r["quiz_quality"]} for r in rows]


def snapshot_at(user_id: str, ts: float | None = None) -> dict:
    """Map node → mastery score in [0, 1] as of `ts` (defaults to now)."""
    if ts is None:
        ts = _time.time()
    ensure_schema()
    rows = db.query(
        """SELECT node, MAX(quiz_quality) AS max_q FROM walk_events
             WHERE user_id = :user_id AND node IS NOT NULL AND ts <= :ts
             GROUP BY node""",
        {"user_id": user_id, "ts": ts},
    )
    out: dict[str, float] = {}
    for row in rows:
        node, max_q = row["node"], row["max_q"]
        if node is None:
            continue
        if max_q is None:
            out[node] = 0.2
        else:
            out[node] = round(max(0.2, min(1.0, max_q / 5.0)), 3)
    return out


def graph_state(user_id: str, ts: float | None = None,
                all_nodes: Iterable[str] | None = None) -> dict:
    """Bucket-level summary for the time-travel UI heatmap."""
    mastery = snapshot_at(user_id, ts)
    nodes = list(all_nodes) if all_nodes is not None else list(mastery.keys())
    visited = sum(1 for n in nodes if n in mastery)
    mastered = sum(1 for n in nodes if mastery.get(n, 0) >= 0.8)
    return {
        "ts":       ts,
        "n_total":  len(nodes),
        "visited":  visited,
        "mastered": mastered,
        "mastery":  mastery,
    }
