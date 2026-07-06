-- 002_atp (postgres) — ATP tables: HITL reward log, compose requests,
-- evidence chain (filled by Phase 3), cert awards.
--
-- Conventions:
--   * ts columns are ISO-8601 UTC strings ("%Y-%m-%dT%H:%M:%SZ"), matching
--     atp/store.py `_now()`.
--   * "JSON-text" columns store json.dumps() output as TEXT.
--   * atp_hitl and atp_evidence are APPEND-ONLY at the DB level: a plpgsql
--     trigger function raises on UPDATE/DELETE.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py). Plain ';' inside a statement (e.g.
-- the function body below) is NOT a separator once the marker is used
-- anywhere in the file.

CREATE TABLE IF NOT EXISTS atp_hitl (
  id             BIGSERIAL PRIMARY KEY,
  ts             TEXT NOT NULL,
  rater          TEXT,
  agent_id       TEXT,
  layer          INTEGER,
  signal         INTEGER,
  weighted_delta DOUBLE PRECISION,
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
  id        BIGSERIAL PRIMARY KEY,
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
  id             BIGSERIAL PRIMARY KEY,
  ts             TEXT NOT NULL,
  agent_id       TEXT,
  cert_id        TEXT,
  score          DOUBLE PRECISION,
  section_scores TEXT,   -- JSON-text
  item_breakdown TEXT,   -- JSON-text
  evidence_ids   TEXT    -- JSON-text array
);
--;;
-- ── Append-only enforcement ────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION atp_append_only() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'append-only: % on % is forbidden', TG_OP, TG_TABLE_NAME;
END;
$$ LANGUAGE plpgsql;
--;;
DROP TRIGGER IF EXISTS trg_atp_hitl_append_only ON atp_hitl;
--;;
CREATE TRIGGER trg_atp_hitl_append_only
BEFORE UPDATE OR DELETE ON atp_hitl
FOR EACH ROW EXECUTE FUNCTION atp_append_only();
--;;
DROP TRIGGER IF EXISTS trg_atp_evidence_append_only ON atp_evidence;
--;;
CREATE TRIGGER trg_atp_evidence_append_only
BEFORE UPDATE OR DELETE ON atp_evidence
FOR EACH ROW EXECUTE FUNCTION atp_append_only();
--;;
-- Belt-and-braces for prod (run manually as the DB owner; the triggers above
-- already block the app). Superusers/table owners can bypass triggers with
-- `ALTER TABLE ... DISABLE TRIGGER`, so also strip the privilege from the
-- role the API connects as:
--
--   REVOKE UPDATE, DELETE ON atp_hitl, atp_evidence FROM <app_role>;
--
-- (Render Postgres: <app_role> is the user in the DATABASE_URL it hands out.)
