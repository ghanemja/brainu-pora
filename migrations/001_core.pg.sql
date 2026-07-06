-- 001_core (postgres) — existing app schema, ported from
-- agents/persistence.py `_SCHEMA` + agents/jobs.py `_ensure_table`.
--
-- Dialect mapping (column NAMES unchanged so callers don't change):
--   INTEGER PRIMARY KEY AUTOINCREMENT  →  BIGSERIAL PRIMARY KEY
--   REAL epoch-seconds timestamps      →  DOUBLE PRECISION (still epoch
--                                         floats — NOT timestamptz — so
--                                         callers keep passing time.time())
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py). Plain ';' inside a statement is NOT
-- a separator once the marker is used anywhere in the file.

CREATE TABLE IF NOT EXISTS users (
  user_id      TEXT PRIMARY KEY,
  display_name TEXT,
  created_at   DOUBLE PRECISION NOT NULL
);
--;;
CREATE TABLE IF NOT EXISTS walks (
  walk_id      BIGSERIAL PRIMARY KEY,
  user_id      TEXT NOT NULL,
  start_node   TEXT NOT NULL,
  planned_json TEXT NOT NULL,
  completed    INTEGER NOT NULL DEFAULT 0,
  started_at   DOUBLE PRECISION NOT NULL,
  completed_at DOUBLE PRECISION
);
--;;
CREATE TABLE IF NOT EXISTS walk_events (
  event_id      BIGSERIAL PRIMARY KEY,
  walk_id       BIGINT NOT NULL REFERENCES walks(walk_id),
  user_id       TEXT NOT NULL,
  node          TEXT,
  step_idx      INTEGER,
  lesson_mode   TEXT,
  quiz_quality  INTEGER,
  duration_s    DOUBLE PRECISION,
  ts            DOUBLE PRECISION NOT NULL
);
--;;
CREATE INDEX IF NOT EXISTS idx_walk_events_user_node
  ON walk_events(user_id, node);
--;;
CREATE TABLE IF NOT EXISTS sr_cards (
  user_id         TEXT NOT NULL,
  node            TEXT NOT NULL,
  repetitions     INTEGER NOT NULL DEFAULT 0,
  ef              DOUBLE PRECISION NOT NULL DEFAULT 2.5,
  interval_days   DOUBLE PRECISION NOT NULL DEFAULT 0,
  due_ts          DOUBLE PRECISION NOT NULL DEFAULT 0,
  last_quality    INTEGER NOT NULL DEFAULT -1,
  last_review_ts  DOUBLE PRECISION NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, node)
);
--;;
CREATE INDEX IF NOT EXISTS idx_sr_due ON sr_cards(user_id, due_ts);
--;;
CREATE TABLE IF NOT EXISTS podcast_state (
  user_id       TEXT NOT NULL,
  episode_key   TEXT NOT NULL,
  current_turn  INTEGER NOT NULL DEFAULT 0,
  interjections TEXT,
  last_played   DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (user_id, episode_key)
);
--;;
CREATE TABLE IF NOT EXISTS feedback (
  feedback_id BIGSERIAL PRIMARY KEY,
  user_id     TEXT NOT NULL,
  target_kind TEXT NOT NULL,
  target_id   TEXT NOT NULL,
  thumb       INTEGER NOT NULL,
  note        TEXT,
  ts          DOUBLE PRECISION NOT NULL
);
--;;
CREATE INDEX IF NOT EXISTS idx_feedback_target
  ON feedback(target_kind, target_id);
--;;
CREATE TABLE IF NOT EXISTS socratic_sessions (
  session_id  TEXT PRIMARY KEY,
  user_id     TEXT NOT NULL,
  node        TEXT NOT NULL,
  state_json  TEXT NOT NULL,
  updated_at  DOUBLE PRECISION NOT NULL
);
--;;
CREATE TABLE IF NOT EXISTS jobs (
  job_id     TEXT PRIMARY KEY,
  kind       TEXT NOT NULL,
  status     TEXT NOT NULL,
  result     TEXT,
  error      TEXT,
  created_at DOUBLE PRECISION NOT NULL,
  updated_at DOUBLE PRECISION NOT NULL
);
