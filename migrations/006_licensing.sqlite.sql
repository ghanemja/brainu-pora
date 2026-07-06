-- 006_licensing (sqlite) — Phase 4 billing (docs/HARDENING.md): org-scoped
-- agent licenses + append-only usage metering (docs/TENANCY.md: both are
-- T1 org-internal data).
--
-- Conventions (002/004/005):
--   * ts columns are ISO-8601 UTC strings ("%Y-%m-%dT%H:%M:%SZ").
--   * org_id defaults to 'org-demo', the bootstrap org (005 bridge), so dev
--     mode (BU_AUTH_DISABLED=1) keeps working unchanged.
--   * SQLite has NO row-level security: dev/demo isolation relies on layers
--     1-2 of docs/TENANCY.md (route deps + org-scoped SQL via
--     atp/tenant_db.py). The Postgres twin (006_licensing.pg.sql) adds RLS.
--
-- Mutability model (deliberate asymmetry):
--   * `licenses` is MUTABLE — revocation and expiry are DB state transitions
--     (status active -> revoked | expired). A license key alone NEVER
--     suffices: atp/licensing.py check_license() re-reads the row on every
--     call, so a revoked/expired row fails instantly regardless of a valid
--     key signature.
--   * `usage_events` is APPEND-ONLY at the DB level (BEFORE UPDATE / BEFORE
--     DELETE triggers abort) — usage rows are billing evidence and must be
--     as tamper-resistant as the atp_evidence chain.
--
-- Key material: only `key_id` (the public identifier half of the license
-- key) is stored. The secret half is an HMAC over key_id with
-- LICENSE_SIGNING_KEY, shown once at issue time and never persisted.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py) — required for the trigger bodies.

CREATE TABLE IF NOT EXISTS licenses (
  id                  TEXT PRIMARY KEY,
  org_id              TEXT NOT NULL DEFAULT 'org-demo',
  agent_id            TEXT NOT NULL,
  kind                TEXT NOT NULL CHECK (kind IN ('evaluation', 'production')),
  status              TEXT NOT NULL DEFAULT 'active'
                      CHECK (status IN ('active', 'revoked', 'expired')),
  key_id              TEXT NOT NULL UNIQUE,
  created_at          TEXT NOT NULL,
  expires_at          TEXT,            -- NULL = never expires
  revoked_at          TEXT,
  revoked_reason      TEXT,
  stripe_customer     TEXT,            -- NULL for 'manual' (invoice) licenses
  stripe_subscription TEXT,            -- NULL for 'manual' (invoice) licenses
  seats               INTEGER NOT NULL DEFAULT 1
);
--;;
-- (org_id, <pk>) per docs/TENANCY.md invariants; key_id lookup is covered by
-- the UNIQUE constraint's implicit index.
CREATE INDEX IF NOT EXISTS idx_licenses_org ON licenses(org_id, id);
--;;
CREATE TABLE IF NOT EXISTS usage_events (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  ts         TEXT NOT NULL,
  org_id     TEXT NOT NULL DEFAULT 'org-demo',
  license_id TEXT,
  agent_id   TEXT,
  endpoint   TEXT,
  tokens_in  INTEGER,
  tokens_out INTEGER,
  status     TEXT
);
--;;
CREATE INDEX IF NOT EXISTS idx_usage_events_org ON usage_events(org_id, id);
--;;
-- ── Append-only enforcement (same pattern as 002 atp_hitl/atp_evidence) ────
CREATE TRIGGER IF NOT EXISTS trg_usage_events_no_update
BEFORE UPDATE ON usage_events
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
--;;
CREATE TRIGGER IF NOT EXISTS trg_usage_events_no_delete
BEFORE DELETE ON usage_events
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
