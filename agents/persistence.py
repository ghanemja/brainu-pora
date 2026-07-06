"""
Persistence layer — app state via the shared DAL (atp.db).

Stores:
  users             — anonymous user_id + display_name + created_at
  walks             — recorded tours (start_node + planned stops + completed)
  walk_events       — per-stop event log (node, lesson_mode, quiz_quality, ts)
  sr_cards          — spaced-repetition state per (user, node)
  podcast_state     — per-user per-episode play position + interjections
  feedback          — thumbs-up/down on lessons (feeds RL ranker)
  socratic_sessions — Socratic dialogue state per session_id

Schema lives in migrations/ (001_core ports the old inline `_SCHEMA`,
003_confusion the table agents/confusion.py used to lazy-create) and is
applied once per process at import via ensure_schema() (idempotent).

Database location — resolved by atp.db, in precedence order:
  1. DATABASE_URL — full SQLAlchemy URL (Postgres in prod:
     postgresql+psycopg2://…; any sqlite:/// URL also works)
  2. BRAIN_DB     — legacy env var: filesystem path to a SQLite file
  3. default     — data/brain_university.db (SQLite; dev/demo)

open_db() survives as a DEPRECATED, SQLite-only shim with ZERO in-repo
callers — kept only for external scripts holding hand-written sqlite SQL.
Every call emits a DeprecationWarning naming the caller, and it raises under
Postgres — use atp.db.query/execute or the helpers below instead.
"""

from __future__ import annotations

import inspect
import json
import re
import sqlite3
import time
import warnings
from pathlib import Path

from atp import db

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_DB = PROJECT_ROOT / "data" / "brain_university.db"

_SCHEMA_READY = False


def ensure_schema() -> None:
    """Apply pending migrations once per process (idempotent, guarded)."""
    global _SCHEMA_READY
    if not _SCHEMA_READY:
        db.run_migrations()
        _SCHEMA_READY = True


ensure_schema()


# ── Deprecated raw-connection shim ──────────────────────────────────────────

def open_db(path: str | Path | None = None) -> sqlite3.Connection:
    """DEPRECATED — raw sqlite3.Connection onto the app database.

    No in-repo callers remain (all ported to atp.db / the helpers in this
    module); kept only for external scripts holding hand-written sqlite SQL.
    Works ONLY when the app runs on SQLite; under Postgres (DATABASE_URL) it
    raises — use atp.db.query/execute or the helpers in this module.

    With an explicit `path`, opens that SQLite file and applies the sqlite
    migration DDL so ad-hoc scratch DBs keep working as before.
    """
    caller = inspect.stack()[1]
    warnings.warn(
        f"agents.persistence.open_db() is deprecated and SQLite-only "
        f"(called from {caller.filename}:{caller.lineno} in "
        f"{caller.function}) — use atp.db.query/execute or the "
        f"agents.persistence helpers instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    if path is None:
        if db.is_postgres():
            raise RuntimeError(
                "agents.persistence.open_db() is a SQLite-only legacy shim, "
                "but this deployment runs on Postgres (DATABASE_URL). Use "
                "atp.db.query/execute or the agents.persistence helpers."
            )
        ensure_schema()  # engine + migrations create the file/schema
        target = Path(db.get_engine().url.database or DEFAULT_DB)
        return sqlite3.connect(str(target))

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target))
    for script in _sqlite_migration_scripts():
        conn.executescript(script)
    return conn


def _sqlite_migration_scripts() -> list[str]:
    """SQLite DDL of every migration, dialect-preferred (.sqlite.sql > .sql).

    Only for the explicit-path open_db() compat case — the real database is
    migrated by atp.db.run_migrations(). Assumes idempotent DDL (IF NOT
    EXISTS), which the shipped migrations use. `--;;` separator lines are
    plain SQL comments, so executescript() handles the files as-is.
    """
    if not db.MIGRATIONS_DIR.is_dir():
        return []
    by_base: dict[str, dict[str | None, Path]] = {}
    for p in db.MIGRATIONS_DIR.iterdir():
        m = re.match(r"^(\d+_\w+?)(?:\.(pg|sqlite))?\.sql$", p.name)
        if m:
            by_base.setdefault(m.group(1), {})[m.group(2)] = p
    scripts: list[str] = []
    for base in sorted(by_base):
        best = by_base[base].get("sqlite") or by_base[base].get(None)
        if best is not None:  # pg-only bases don't apply to a sqlite file
            scripts.append(best.read_text())
    return scripts


# ── User helpers ────────────────────────────────────────────────────────────

def ensure_user(user_id: str, display_name: str | None = None) -> None:
    db.execute(
        """INSERT INTO users (user_id, display_name, created_at)
           VALUES (:user_id, :display_name, :created_at)
           ON CONFLICT(user_id) DO UPDATE SET
             display_name = COALESCE(excluded.display_name, users.display_name)""",
        {"user_id": user_id, "display_name": display_name,
         "created_at": time.time()},
    )


# ── Walks ──────────────────────────────────────────────────────────────────

def start_walk(user_id: str, start_node: str, planned_stops: list[str]) -> int:
    res = db.execute(
        """INSERT INTO walks (user_id, start_node, planned_json, started_at)
           VALUES (:user_id, :start_node, :planned_json, :started_at)
           RETURNING walk_id""",
        {"user_id": user_id, "start_node": start_node,
         "planned_json": json.dumps(planned_stops), "started_at": time.time()},
    )
    return int(res.lastrowid)


def log_walk_event(
    walk_id: int, user_id: str, *,
    node: str | None = None, step_idx: int | None = None,
    lesson_mode: str | None = None, quiz_quality: int | None = None,
    duration_s: float | None = None,
) -> None:
    db.execute(
        """INSERT INTO walk_events
             (walk_id, user_id, node, step_idx, lesson_mode,
              quiz_quality, duration_s, ts)
           VALUES (:walk_id, :user_id, :node, :step_idx, :lesson_mode,
                   :quiz_quality, :duration_s, :ts)""",
        {"walk_id": walk_id, "user_id": user_id, "node": node,
         "step_idx": step_idx, "lesson_mode": lesson_mode,
         "quiz_quality": quiz_quality, "duration_s": duration_s,
         "ts": time.time()},
    )


def complete_walk(walk_id: int) -> None:
    db.execute(
        """UPDATE walks SET completed = 1, completed_at = :completed_at
            WHERE walk_id = :walk_id""",
        {"completed_at": time.time(), "walk_id": walk_id},
    )


def user_walks(user_id: str, limit: int = 50) -> list[dict]:
    rows = db.query(
        """SELECT walk_id, start_node, planned_json, completed,
                  started_at, completed_at
             FROM walks WHERE user_id = :user_id
            ORDER BY started_at DESC LIMIT :limit""",
        {"user_id": user_id, "limit": limit},
    )
    return [
        {
            "walk_id": r["walk_id"], "start_node": r["start_node"],
            "planned": json.loads(r["planned_json"]),
            "completed": bool(r["completed"]),
            "started_at": r["started_at"], "completed_at": r["completed_at"],
        }
        for r in rows
    ]


# ── Spaced-repetition cards ────────────────────────────────────────────────

def upsert_sr_card(
    user_id: str, node: str, *,
    repetitions: int = 0, ef: float = 2.5, interval_days: float = 0.0,
    due_ts: float = 0.0, last_quality: int = -1, last_review_ts: float = 0.0,
) -> None:
    """Insert-or-update the full SM-2 state for one (user, node) card."""
    db.execute(
        """INSERT INTO sr_cards
               (user_id, node, repetitions, ef, interval_days, due_ts,
                last_quality, last_review_ts)
           VALUES (:user_id, :node, :repetitions, :ef, :interval_days,
                   :due_ts, :last_quality, :last_review_ts)
           ON CONFLICT(user_id, node) DO UPDATE SET
               repetitions     = excluded.repetitions,
               ef              = excluded.ef,
               interval_days   = excluded.interval_days,
               due_ts          = excluded.due_ts,
               last_quality    = excluded.last_quality,
               last_review_ts  = excluded.last_review_ts""",
        {"user_id": user_id, "node": node, "repetitions": repetitions,
         "ef": ef, "interval_days": interval_days, "due_ts": due_ts,
         "last_quality": last_quality, "last_review_ts": last_review_ts},
    )


def get_sr_card(user_id: str, node: str) -> dict | None:
    rows = db.query(
        """SELECT user_id, node, repetitions, ef, interval_days, due_ts,
                  last_quality, last_review_ts
             FROM sr_cards WHERE user_id = :user_id AND node = :node""",
        {"user_id": user_id, "node": node},
    )
    return rows[0] if rows else None


def due_sr_cards(user_id: str, now: float | None = None,
                 limit: int = 10) -> list[dict]:
    """Cards whose due_ts <= now, oldest-due first."""
    return db.query(
        """SELECT user_id, node, repetitions, ef, interval_days, due_ts,
                  last_quality, last_review_ts
             FROM sr_cards
            WHERE user_id = :user_id AND due_ts <= :now
         ORDER BY due_ts ASC LIMIT :limit""",
        {"user_id": user_id, "now": now or time.time(), "limit": limit},
    )


def all_sr_cards(user_id: str) -> list[dict]:
    return db.query(
        """SELECT user_id, node, repetitions, ef, interval_days, due_ts,
                  last_quality, last_review_ts
             FROM sr_cards WHERE user_id = :user_id ORDER BY due_ts""",
        {"user_id": user_id},
    )


# ── Podcast state ──────────────────────────────────────────────────────────

def save_podcast_state(user_id: str, episode_key: str, current_turn: int,
                        interjections: list[dict] | None = None) -> None:
    db.execute(
        """INSERT INTO podcast_state
             (user_id, episode_key, current_turn, interjections, last_played)
           VALUES (:user_id, :episode_key, :current_turn, :interjections,
                   :last_played)
           ON CONFLICT(user_id, episode_key) DO UPDATE SET
             current_turn  = excluded.current_turn,
             interjections = excluded.interjections,
             last_played   = excluded.last_played""",
        {"user_id": user_id, "episode_key": episode_key,
         "current_turn": current_turn,
         "interjections": json.dumps(interjections or []),
         "last_played": time.time()},
    )


def load_podcast_state(user_id: str, episode_key: str) -> dict | None:
    rows = db.query(
        """SELECT current_turn, interjections, last_played
             FROM podcast_state
            WHERE user_id = :user_id AND episode_key = :episode_key""",
        {"user_id": user_id, "episode_key": episode_key},
    )
    if not rows:
        return None
    row = rows[0]
    return {
        "current_turn":  row["current_turn"],
        "interjections": json.loads(row["interjections"] or "[]"),
        "last_played":   row["last_played"],
    }


# ── Feedback ───────────────────────────────────────────────────────────────

def add_feedback(user_id: str, target_kind: str, target_id: str,
                 thumb: int, note: str | None = None) -> None:
    db.execute(
        """INSERT INTO feedback
             (user_id, target_kind, target_id, thumb, note, ts)
           VALUES (:user_id, :target_kind, :target_id, :thumb, :note, :ts)""",
        {"user_id": user_id, "target_kind": target_kind,
         "target_id": target_id, "thumb": thumb, "note": note,
         "ts": time.time()},
    )


def feedback_for_target(target_kind: str, target_id: str) -> list[dict]:
    return db.query(
        """SELECT user_id, thumb, note, ts FROM feedback
            WHERE target_kind = :target_kind AND target_id = :target_id
            ORDER BY ts DESC""",
        {"target_kind": target_kind, "target_id": target_id},
    )


# ── Socratic sessions ──────────────────────────────────────────────────────

def save_socratic_session(session_id: str, user_id: str, node: str,
                          state: dict) -> None:
    """Insert-or-replace one Socratic session (state: JSON-serializable)."""
    db.execute(
        """INSERT INTO socratic_sessions
             (session_id, user_id, node, state_json, updated_at)
           VALUES (:session_id, :user_id, :node, :state_json, :updated_at)
           ON CONFLICT(session_id) DO UPDATE SET
             state_json = excluded.state_json,
             updated_at = excluded.updated_at""",
        {"session_id": session_id, "user_id": user_id, "node": node,
         "state_json": json.dumps(state), "updated_at": time.time()},
    )


def load_socratic_session(session_id: str) -> dict | None:
    rows = db.query(
        """SELECT session_id, user_id, node, state_json, updated_at
             FROM socratic_sessions WHERE session_id = :session_id""",
        {"session_id": session_id},
    )
    if not rows:
        return None
    row = rows[0]
    return {
        "session_id": row["session_id"], "user_id": row["user_id"],
        "node": row["node"], "state": json.loads(row["state_json"]),
        "updated_at": row["updated_at"],
    }


def update_socratic_session(session_id: str, state: dict) -> bool:
    """Update an existing session's state. Returns False if it doesn't exist."""
    res = db.execute(
        """UPDATE socratic_sessions
              SET state_json = :state_json, updated_at = :updated_at
            WHERE session_id = :session_id""",
        {"state_json": json.dumps(state), "updated_at": time.time(),
         "session_id": session_id},
    )
    return res.rowcount > 0
