"""
SQLite persistence layer.

Stores:
  users         — anonymous user_id + display_name + created_at
  walks         — recorded tours (start_node + planned stops + completed)
  walk_events   — per-stop event log (node, lesson_mode, quiz_quality, ts)
  sr_cards      — spaced-repetition state per (user, node)
  podcast_state — per-user per-episode play position + interjections
  feedback      — thumbs-up/down on lessons (feeds RL ranker)

Default path: data/brain_university.db (override with BRAIN_DB env var).
"""

from __future__ import annotations

import os
import sqlite3
import time
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_DB = PROJECT_ROOT / "data" / "brain_university.db"


_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  user_id      TEXT PRIMARY KEY,
  display_name TEXT,
  created_at   REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS walks (
  walk_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id      TEXT NOT NULL,
  start_node   TEXT NOT NULL,
  planned_json TEXT NOT NULL,
  completed    INTEGER NOT NULL DEFAULT 0,
  started_at   REAL NOT NULL,
  completed_at REAL
);

CREATE TABLE IF NOT EXISTS walk_events (
  event_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  walk_id       INTEGER NOT NULL,
  user_id       TEXT NOT NULL,
  node          TEXT,
  step_idx      INTEGER,
  lesson_mode   TEXT,
  quiz_quality  INTEGER,
  duration_s    REAL,
  ts            REAL NOT NULL,
  FOREIGN KEY (walk_id) REFERENCES walks(walk_id)
);
CREATE INDEX IF NOT EXISTS idx_walk_events_user_node
  ON walk_events(user_id, node);

CREATE TABLE IF NOT EXISTS sr_cards (
  user_id         TEXT NOT NULL,
  node            TEXT NOT NULL,
  repetitions     INTEGER NOT NULL DEFAULT 0,
  ef              REAL    NOT NULL DEFAULT 2.5,
  interval_days   REAL    NOT NULL DEFAULT 0,
  due_ts          REAL    NOT NULL DEFAULT 0,
  last_quality    INTEGER NOT NULL DEFAULT -1,
  last_review_ts  REAL    NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, node)
);
CREATE INDEX IF NOT EXISTS idx_sr_due ON sr_cards(user_id, due_ts);

CREATE TABLE IF NOT EXISTS podcast_state (
  user_id       TEXT NOT NULL,
  episode_key   TEXT NOT NULL,
  current_turn  INTEGER NOT NULL DEFAULT 0,
  interjections TEXT,
  last_played   REAL NOT NULL,
  PRIMARY KEY (user_id, episode_key)
);

CREATE TABLE IF NOT EXISTS feedback (
  feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     TEXT NOT NULL,
  target_kind TEXT NOT NULL,
  target_id   TEXT NOT NULL,
  thumb       INTEGER NOT NULL,
  note        TEXT,
  ts          REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_feedback_target
  ON feedback(target_kind, target_id);

CREATE TABLE IF NOT EXISTS socratic_sessions (
  session_id  TEXT PRIMARY KEY,
  user_id     TEXT NOT NULL,
  node        TEXT NOT NULL,
  state_json  TEXT NOT NULL,
  updated_at  REAL NOT NULL
);
"""


def open_db(path: str | Path | None = None) -> sqlite3.Connection:
    """Open (and lazily create) the SQLite DB. Returns a Connection."""
    target = Path(path or os.environ.get("BRAIN_DB", DEFAULT_DB))
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target))
    conn.executescript(_SCHEMA)
    return conn


# ── User helpers ────────────────────────────────────────────────────────────

def ensure_user(user_id: str, display_name: str | None = None) -> None:
    db = open_db()
    db.execute(
        """INSERT INTO users (user_id, display_name, created_at)
           VALUES (?, ?, ?)
           ON CONFLICT(user_id) DO UPDATE SET
             display_name = COALESCE(excluded.display_name, users.display_name)""",
        (user_id, display_name, time.time()),
    )
    db.commit()


# ── Walks ──────────────────────────────────────────────────────────────────

def start_walk(user_id: str, start_node: str, planned_stops: list[str]) -> int:
    import json
    db = open_db()
    cur = db.execute(
        """INSERT INTO walks (user_id, start_node, planned_json, started_at)
           VALUES (?, ?, ?, ?)""",
        (user_id, start_node, json.dumps(planned_stops), time.time()),
    )
    db.commit()
    return cur.lastrowid


def log_walk_event(
    walk_id: int, user_id: str, *,
    node: str | None = None, step_idx: int | None = None,
    lesson_mode: str | None = None, quiz_quality: int | None = None,
    duration_s: float | None = None,
) -> None:
    db = open_db()
    db.execute(
        """INSERT INTO walk_events
             (walk_id, user_id, node, step_idx, lesson_mode,
              quiz_quality, duration_s, ts)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (walk_id, user_id, node, step_idx, lesson_mode,
         quiz_quality, duration_s, time.time()),
    )
    db.commit()


def complete_walk(walk_id: int) -> None:
    db = open_db()
    db.execute(
        "UPDATE walks SET completed = 1, completed_at = ? WHERE walk_id = ?",
        (time.time(), walk_id),
    )
    db.commit()


def user_walks(user_id: str, limit: int = 50) -> list[dict]:
    db = open_db()
    rows = db.execute(
        """SELECT walk_id, start_node, planned_json, completed,
                  started_at, completed_at
             FROM walks WHERE user_id = ?
            ORDER BY started_at DESC LIMIT ?""",
        (user_id, limit),
    ).fetchall()
    import json
    return [
        {
            "walk_id": r[0], "start_node": r[1],
            "planned": json.loads(r[2]),
            "completed": bool(r[3]),
            "started_at": r[4], "completed_at": r[5],
        }
        for r in rows
    ]


# ── Podcast state ──────────────────────────────────────────────────────────

def save_podcast_state(user_id: str, episode_key: str, current_turn: int,
                        interjections: list[dict] | None = None) -> None:
    import json
    db = open_db()
    db.execute(
        """INSERT INTO podcast_state
             (user_id, episode_key, current_turn, interjections, last_played)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(user_id, episode_key) DO UPDATE SET
             current_turn  = excluded.current_turn,
             interjections = excluded.interjections,
             last_played   = excluded.last_played""",
        (user_id, episode_key, current_turn,
         json.dumps(interjections or []), time.time()),
    )
    db.commit()


def load_podcast_state(user_id: str, episode_key: str) -> dict | None:
    db = open_db()
    row = db.execute(
        """SELECT current_turn, interjections, last_played
             FROM podcast_state WHERE user_id = ? AND episode_key = ?""",
        (user_id, episode_key),
    ).fetchone()
    if not row:
        return None
    import json
    return {
        "current_turn":  row[0],
        "interjections": json.loads(row[1] or "[]"),
        "last_played":   row[2],
    }


# ── Feedback ───────────────────────────────────────────────────────────────

def add_feedback(user_id: str, target_kind: str, target_id: str,
                 thumb: int, note: str | None = None) -> None:
    db = open_db()
    db.execute(
        """INSERT INTO feedback
             (user_id, target_kind, target_id, thumb, note, ts)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, target_kind, target_id, thumb, note, time.time()),
    )
    db.commit()


def feedback_for_target(target_kind: str, target_id: str) -> list[dict]:
    db = open_db()
    rows = db.execute(
        """SELECT user_id, thumb, note, ts FROM feedback
            WHERE target_kind = ? AND target_id = ?
            ORDER BY ts DESC""",
        (target_kind, target_id),
    ).fetchall()
    return [{"user_id": r[0], "thumb": r[1], "note": r[2], "ts": r[3]} for r in rows]
