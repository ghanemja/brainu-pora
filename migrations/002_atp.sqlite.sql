-- 002_atp (sqlite) — ATP tables: HITL reward log, compose requests,
-- evidence chain (filled by Phase 3), cert awards.
--
-- Conventions:
--   * ts columns are ISO-8601 UTC strings ("%Y-%m-%dT%H:%M:%SZ"), matching
--     atp/store.py `_now()`.
--   * "JSON-text" columns store json.dumps() output as TEXT.
--   * atp_hitl and atp_evidence are APPEND-ONLY at the DB level: BEFORE
--     UPDATE / BEFORE DELETE triggers abort with 'append-only'.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py). Plain ';' inside a statement (e.g.
-- trigger bodies below) is NOT a separator once the marker is used anywhere
-- in the file.

CREATE TABLE IF NOT EXISTS atp_hitl (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  ts             TEXT NOT NULL,
  rater          TEXT,
  agent_id       TEXT,
  layer          INTEGER,
  signal         INTEGER,
  weighted_delta REAL,
  reason         TEXT,
  audit_id       TEXT
);
--;;
CREATE INDEX IF NOT EXISTS idx_atp_hitl_agent ON atp_hitl(agent_id);
--;;
CREATE TABLE IF NOT EXISTS atp_requests (
  id               TEXT PRIMARY KEY,
  ts               TEXT NOT NULL,
  major            TEXT,
  specialty        TEXT,
  badge_ids        TEXT,   -- JSON-text array
  pack_id          TEXT,
  layers           TEXT,   -- JSON-text array
  corpora          TEXT,   -- JSON-text array
  status           TEXT,
  matched_agent_id TEXT,
  gap              TEXT,   -- JSON-text object (nullable)
  pipeline         TEXT,   -- JSON-text array of stage dicts
  result_agent_id  TEXT
);
--;;
-- Evidence chain — empty until Phase 3 (exam runs) writes signed records.
CREATE TABLE IF NOT EXISTS atp_evidence (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  ts        TEXT NOT NULL,
  agent_id  TEXT,
  cert_id   TEXT,
  kind      TEXT,
  payload   TEXT,   -- JSON-text canonical payload (HMAC-signed)
  sig       TEXT,
  prev_hash TEXT
);
--;;
CREATE INDEX IF NOT EXISTS idx_atp_evidence_agent
  ON atp_evidence(agent_id, cert_id);
--;;
CREATE TABLE IF NOT EXISTS atp_cert_awards (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  ts             TEXT NOT NULL,
  agent_id       TEXT,
  cert_id        TEXT,
  score          REAL,
  section_scores TEXT,   -- JSON-text
  item_breakdown TEXT,   -- JSON-text
  evidence_ids   TEXT    -- JSON-text array
);
--;;
-- ── Append-only enforcement ────────────────────────────────────────────────
CREATE TRIGGER IF NOT EXISTS trg_atp_hitl_no_update
BEFORE UPDATE ON atp_hitl
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
--;;
CREATE TRIGGER IF NOT EXISTS trg_atp_hitl_no_delete
BEFORE DELETE ON atp_hitl
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
--;;
CREATE TRIGGER IF NOT EXISTS trg_atp_evidence_no_update
BEFORE UPDATE ON atp_evidence
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
--;;
CREATE TRIGGER IF NOT EXISTS trg_atp_evidence_no_delete
BEFORE DELETE ON atp_evidence
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
