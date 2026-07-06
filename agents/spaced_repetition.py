"""
SM-2 spaced repetition scheduler.

Each quiz attempt for a (user, node) pair feeds a quality grade 0-5 into
SuperMemo-2. The scheduler stores per-card state through agents.persistence
(SQLite or Postgres via the atp.db DAL) and surfaces "due now" cards back
through the trailhead / dashboard.

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


# ── Persistence (agents.persistence helpers — SQLite + Postgres) ──────────

def schedule_review(user_id: str, node: str, quality: int,
                    now: float | None = None) -> float:
    """Record a quiz attempt and return the next due timestamp."""
    from . import persistence
    row = persistence.get_sr_card(user_id, node)
    state = CardState(**row) if row else CardState(user_id=user_id, node=node)
    update_sm2(state, quality, now=now)
    persistence.upsert_sr_card(**asdict(state))
    return state.due_ts


def due_cards(user_id: str, now: float | None = None,
              limit: int = 10) -> list[dict]:
    """Return cards whose due_ts <= now, oldest-due first."""
    from . import persistence
    rows = persistence.due_sr_cards(user_id, now=now, limit=limit)
    return [_with_due_in_days(r) for r in rows]


def all_cards(user_id: str) -> list[dict]:
    from . import persistence
    rows = persistence.all_sr_cards(user_id)
    return [_with_due_in_days(r) for r in rows]


def _with_due_in_days(row: dict) -> dict:
    out = dict(row)
    out["due_in_days"] = (out["due_ts"] - time.time()) / DAY_SECONDS
    return out
