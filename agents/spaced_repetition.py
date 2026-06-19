"""
SM-2 spaced repetition scheduler.

Each quiz attempt for a (user, node) pair feeds a quality grade 0-5 into
SuperMemo-2. The scheduler stores per-card state in SQLite (lib/persistence)
and surfaces "due now" cards back through the trailhead / dashboard.

Quality grading (from quiz):
  5  correct on first try, < 5s
  4  correct on first try, > 5s
  3  correct after retry
  2  wrong, but explanation accepted
  1  wrong, gave up
  0  no attempt

Public:
  schedule_review(user_id, node, quality) → next_due timestamp
  due_cards(user_id, now=None, limit=10)  → list of {node, ef, interval, due}
"""

from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path

DAY_SECONDS = 86400


@dataclass
class CardState:
    user_id: str
    node: str
    repetitions: int = 0     # n consecutive correct
    ef: float = 2.5          # easiness factor
    interval_days: float = 0.0
    due_ts: float = 0.0
    last_quality: int = -1
    last_review_ts: float = 0.0


def update_sm2(state: CardState, quality: int, now: float | None = None) -> CardState:
    """Apply SM-2 update to a card given quality 0-5. Mutates + returns state."""
    quality = max(0, min(5, int(quality)))
    now = now or time.time()
    if quality < 3:
        # Failed — reset repetition, short re-review (10 min)
        state.repetitions = 0
        state.interval_days = 10 / (24 * 60)  # 10 minutes
    else:
        if state.repetitions == 0:
            state.interval_days = 1
        elif state.repetitions == 1:
            state.interval_days = 6
        else:
            state.interval_days = max(1.0, state.interval_days * state.ef)
        state.repetitions += 1
    # EF update (clamped to floor 1.3)
    state.ef = max(1.3, state.ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    state.due_ts = now + state.interval_days * DAY_SECONDS
    state.last_quality = quality
    state.last_review_ts = now
    return state


# ── Persistence ────────────────────────────────────────────────────────────

def schedule_review(user_id: str, node: str, quality: int,
                    now: float | None = None) -> float:
    """Record a quiz attempt and return the next due timestamp."""
    from .persistence import open_db
    db = open_db()
    state = _load(db, user_id, node) or CardState(user_id=user_id, node=node)
    update_sm2(state, quality, now=now)
    _save(db, state)
    return state.due_ts


def due_cards(user_id: str, now: float | None = None,
              limit: int = 10) -> list[dict]:
    """Return cards whose due_ts <= now, oldest-due first."""
    from .persistence import open_db
    now = now or time.time()
    db = open_db()
    rows = db.execute(
        """SELECT user_id, node, repetitions, ef, interval_days, due_ts,
                  last_quality, last_review_ts
             FROM sr_cards
            WHERE user_id = ? AND due_ts <= ?
         ORDER BY due_ts ASC LIMIT ?""",
        (user_id, now, limit),
    ).fetchall()
    return [_row_to_dict(r) for r in rows]


def all_cards(user_id: str) -> list[dict]:
    from .persistence import open_db
    db = open_db()
    rows = db.execute(
        """SELECT user_id, node, repetitions, ef, interval_days, due_ts,
                  last_quality, last_review_ts
             FROM sr_cards WHERE user_id = ? ORDER BY due_ts""",
        (user_id,),
    ).fetchall()
    return [_row_to_dict(r) for r in rows]


def _load(db, user_id: str, node: str) -> CardState | None:
    row = db.execute(
        """SELECT user_id, node, repetitions, ef, interval_days, due_ts,
                  last_quality, last_review_ts
             FROM sr_cards WHERE user_id = ? AND node = ?""",
        (user_id, node),
    ).fetchone()
    if not row:
        return None
    return CardState(
        user_id=row[0], node=row[1], repetitions=row[2], ef=row[3],
        interval_days=row[4], due_ts=row[5], last_quality=row[6],
        last_review_ts=row[7],
    )


def _save(db, state: CardState) -> None:
    db.execute(
        """INSERT INTO sr_cards
               (user_id, node, repetitions, ef, interval_days, due_ts,
                last_quality, last_review_ts)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(user_id, node) DO UPDATE SET
               repetitions     = excluded.repetitions,
               ef              = excluded.ef,
               interval_days   = excluded.interval_days,
               due_ts          = excluded.due_ts,
               last_quality    = excluded.last_quality,
               last_review_ts  = excluded.last_review_ts""",
        (state.user_id, state.node, state.repetitions, state.ef,
         state.interval_days, state.due_ts, state.last_quality,
         state.last_review_ts),
    )
    db.commit()


def _row_to_dict(row) -> dict:
    return {
        "user_id": row[0], "node": row[1], "repetitions": row[2],
        "ef": row[3], "interval_days": row[4], "due_ts": row[5],
        "last_quality": row[6], "last_review_ts": row[7],
        "due_in_days": (row[5] - time.time()) / DAY_SECONDS,
    }
