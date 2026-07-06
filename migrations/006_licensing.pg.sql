-- 006_licensing (postgres) — Phase 4 billing (docs/HARDENING.md): org-scoped
-- agent licenses + append-only usage metering, PLUS layer 3 (RLS) on both
-- tables (docs/TENANCY.md: both are T1 org-internal data).
--
-- Mutability model (deliberate asymmetry):
--   * `licenses` is MUTABLE — revocation and expiry are DB state transitions
--     (status active -> revoked | expired). A license key alone NEVER
--     suffices: atp/licensing.py check_license() re-reads the row on every
--     call, so a revoked/expired row fails instantly regardless of a valid
--     key signature.
--   * `usage_events` is APPEND-ONLY at the DB level (BEFORE UPDATE/DELETE
--     trigger aborts) — usage rows are billing evidence and must be as
--     tamper-resistant as the atp_evidence chain.
--
-- Key material: only `key_id` (the public identifier half of the license
-- key) is stored. The secret half is an HMAC over key_id with
-- LICENSE_SIGNING_KEY, shown once at issue time and never persisted.
--
-- RLS model — DENY BY DEFAULT, 005 policy pattern:
--   * org_isolation on both tables:
--       USING / WITH CHECK (org_id = current_setting('app.org_id', true))
--     current_setting(..., true) is NULL when unset → predicate NULL → row
--     invisible / write rejected. Do NOT add a NULL fallback (see 005).
--   * FORCE ROW LEVEL SECURITY so the table-owner app role has no bypass.
--   * ONE narrow addition on `licenses` only: policy `key_lookup` (SELECT
--     only). check_license() authenticates by license KEY, not by org — the
--     caller of the gated proxy endpoint may be a machine holding only the
--     key, and the org is learned FROM the row. After atp/licensing.py has
--     verified the key's HMAC signature (constant time), it runs, inside one
--     transaction:
--         SELECT set_config('app.license_key_id', :key_id, true);  -- SET LOCAL
--         SELECT ... FROM licenses WHERE key_id = :key_id;
--     which makes exactly the ONE row whose bearer credential was presented
--     visible — nothing else, no writes (writes still require the org GUC
--     via org_isolation's WITH CHECK). Absent both GUCs the predicate is
--     NULL → zero rows, so deny-by-default is preserved.
--   * All other application access goes through atp/tenant_db.py
--     (SET LOCAL app.org_id per transaction), exactly as for the 005 tables.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py).

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
  id         BIGSERIAL PRIMARY KEY,
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
-- ── Append-only enforcement (002/004 pattern) ───────────────────────────────
-- Same trigger function as 002/004; re-declared (CREATE OR REPLACE, identical
-- body) so this migration stands alone.
CREATE OR REPLACE FUNCTION atp_append_only() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'append-only: % on % is forbidden', TG_OP, TG_TABLE_NAME;
END;
$$ LANGUAGE plpgsql;
--;;
DROP TRIGGER IF EXISTS trg_usage_events_append_only ON usage_events;
--;;
CREATE TRIGGER trg_usage_events_append_only
BEFORE UPDATE OR DELETE ON usage_events
FOR EACH ROW EXECUTE FUNCTION atp_append_only();
--;;
-- ── Row-Level Security (layer 3, 005 pattern) ───────────────────────────────
-- CREATE POLICY has no IF NOT EXISTS → DROP IF EXISTS first so a
-- partially-applied database can be re-run safely.
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE licenses FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON licenses;
--;;
CREATE POLICY org_isolation ON licenses FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
--;;
-- Narrow key-based lookup path for check_license() — SELECT only, exactly
-- the row whose (already signature-verified) key_id was pinned via
-- set_config('app.license_key_id', :key_id, true). See header comment.
DROP POLICY IF EXISTS key_lookup ON licenses;
--;;
CREATE POLICY key_lookup ON licenses FOR SELECT
  USING (key_id = current_setting('app.license_key_id', true));
--;;
ALTER TABLE usage_events ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE usage_events FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON usage_events;
--;;
CREATE POLICY org_isolation ON usage_events FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
