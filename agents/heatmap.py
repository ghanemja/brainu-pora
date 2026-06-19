"""
Knowledge gap heatmap — per-user mastery score for each graph cluster.

Drives a UI viz that shows "which areas of the brain map am I cold in?".
Also feeds the RL ranker so weak clusters get prioritized as start cards.

Mastery score per cluster ∈ [0, 1]:
  factor 1  fraction of nodes in cluster the user has visited
  factor 2  mean quiz quality (0-5 → 0-1) on visited nodes
  factor 3  SR repetition depth (saturates at repetitions >= 3)

Composite: 0.3 * visit_frac + 0.4 * quiz_mean + 0.3 * sr_depth

Public:
  mastery_per_cluster(user_id, clusters) → dict[cluster_id → {score, breakdown}]
  weakest(user_id, clusters, n=5)        → list of cluster_id sorted ascending
"""

from __future__ import annotations

from typing import Iterable


def mastery_per_cluster(user_id: str, clusters: Iterable) -> dict:
    """Compute per-cluster mastery for a user."""
    from .persistence import open_db
    db = open_db()
    visited = _visited_nodes(db, user_id)
    sr_state = _sr_state(db, user_id)

    out = {}
    for cluster in clusters:
        cid = getattr(cluster, "cluster_id", None)
        nodes = [n for n, _ in (cluster.top_nodes or [])]
        if not nodes:
            continue
        n_total = len(nodes)
        n_visited = sum(1 for n in nodes if n in visited)
        visit_frac = n_visited / max(1, n_total)

        quiz_scores = [
            visited[n]["best_quality"] for n in nodes
            if n in visited and visited[n]["best_quality"] is not None
        ]
        quiz_mean = (sum(quiz_scores) / 5.0 / len(quiz_scores)) if quiz_scores else 0.0

        sr_depths = [
            min(3, sr_state[n]["repetitions"]) / 3.0
            for n in nodes if n in sr_state
        ]
        sr_depth = (sum(sr_depths) / len(sr_depths)) if sr_depths else 0.0

        score = 0.3 * visit_frac + 0.4 * quiz_mean + 0.3 * sr_depth
        out[cid] = {
            "score":       round(score, 3),
            "visit_frac":  round(visit_frac, 3),
            "quiz_mean":   round(quiz_mean, 3),
            "sr_depth":    round(sr_depth, 3),
            "n_visited":   n_visited,
            "n_total":     n_total,
            "cluster_name": getattr(cluster, "name", str(cid)),
        }
    return out


def weakest(user_id: str, clusters: Iterable, n: int = 5) -> list[int]:
    """Return cluster_ids sorted by mastery ascending — weakest first."""
    scores = mastery_per_cluster(user_id, clusters)
    ordered = sorted(scores.items(), key=lambda kv: kv[1]["score"])
    return [cid for cid, _ in ordered[:n]]


def _visited_nodes(db, user_id: str) -> dict:
    """Map node → {best_quality, n_visits}. Reads sessions table."""
    rows = db.execute(
        """SELECT node, MAX(quiz_quality), COUNT(*)
             FROM walk_events
            WHERE user_id = ? AND node IS NOT NULL
         GROUP BY node""",
        (user_id,),
    ).fetchall()
    return {r[0]: {"best_quality": r[1], "n_visits": r[2]} for r in rows}


def _sr_state(db, user_id: str) -> dict:
    rows = db.execute(
        "SELECT node, repetitions FROM sr_cards WHERE user_id = ?",
        (user_id,),
    ).fetchall()
    return {r[0]: {"repetitions": r[1]} for r in rows}
