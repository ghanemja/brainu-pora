-- 003_confusion — confusion_signals (agents/confusion.py telemetry).
--
-- Previously lazy-created by confusion.py's _ensure_table() through the
-- sqlite-only open_db() shim; owning it here means Postgres deployments get
-- the table too. Dialect-neutral DDL: one file for both SQLite and Postgres.
-- (confusion.py is now fully on atp.db and no longer creates any DDL.)
--
-- DOUBLE PRECISION (not REAL) so `ts`/`value` keep full float64 precision on
-- Postgres (REAL is float4 there); on SQLite both collapse to REAL affinity.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py).

CREATE TABLE IF NOT EXISTS confusion_signals (
  user_id        TEXT NOT NULL,
  paragraph_hash TEXT NOT NULL,
  signal_kind    TEXT NOT NULL,
  value          DOUBLE PRECISION NOT NULL,
  ts             DOUBLE PRECISION NOT NULL
);
--;;
CREATE INDEX IF NOT EXISTS idx_confusion_user_para
  ON confusion_signals(user_id, paragraph_hash);
