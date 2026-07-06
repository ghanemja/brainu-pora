-- 004_identity (postgres) — Phase 2 identity & tenancy principals:
-- orgs, org-aware users, append-only access_log (docs/TENANCY.md).
--
-- NOTE on `users`: migration 001 already created `users` as the learner
-- profile table (user_id TEXT PK, display_name, created_at — written by
-- agents/persistence.py). Rather than a second colliding table, this
-- migration EXTENDS it with the identity columns from docs/TENANCY.md:
-- `user_id` serves as the spec's `id`; legacy learner rows keep NULL
-- org_id/email/role and are invisible to identity lookups (which filter on
-- email / (oidc_iss, oidc_sub)).
--
-- Conventions:
--   * ts / created_at columns added here are ISO-8601 UTC strings
--     ("%Y-%m-%dT%H:%M:%SZ"), matching atp/store.py `_now()`.
--     (users.created_at keeps its 001 type — pre-existing column.)
--   * access_log is APPEND-ONLY at the DB level: reuses the plpgsql
--     atp_append_only() trigger function from 002 (re-declared here with
--     CREATE OR REPLACE so this file stands alone).
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py). Plain ';' inside a statement (e.g.
-- the function body below) is NOT a separator once the marker is used
-- anywhere in the file.

CREATE TABLE IF NOT EXISTS orgs (
  id         TEXT PRIMARY KEY,
  name       TEXT,
  domain     TEXT,
  created_at TEXT NOT NULL
);
--;;
CREATE UNIQUE INDEX IF NOT EXISTS idx_orgs_domain
  ON orgs(domain) WHERE domain IS NOT NULL;
--;;
-- ── users: identity columns (see NOTE above) ───────────────────────────────
ALTER TABLE users ADD COLUMN IF NOT EXISTS org_id   TEXT REFERENCES orgs(id);
--;;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email    TEXT;
--;;
ALTER TABLE users ADD COLUMN IF NOT EXISTS role     TEXT;
--;;
ALTER TABLE users ADD COLUMN IF NOT EXISTS oidc_iss TEXT;
--;;
ALTER TABLE users ADD COLUMN IF NOT EXISTS oidc_sub TEXT;
--;;
ALTER TABLE users ADD COLUMN IF NOT EXISTS pw_hash  TEXT;
--;;
-- role CHECK (NULL allowed — legacy learner rows have no role)
ALTER TABLE users ADD CONSTRAINT users_role_check
  CHECK (role IS NULL OR role IN ('admin', 'sme', 'viewer'));
--;;
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email
  ON users(email) WHERE email IS NOT NULL;
--;;
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_oidc
  ON users(oidc_iss, oidc_sub)
  WHERE oidc_iss IS NOT NULL AND oidc_sub IS NOT NULL;
--;;
CREATE INDEX IF NOT EXISTS idx_users_org ON users(org_id);
--;;
-- ── access_log — tenant-data audit trail (TENANCY.md layer 4) ──────────────
CREATE TABLE IF NOT EXISTS access_log (
  id           BIGSERIAL PRIMARY KEY,
  ts           TEXT NOT NULL,
  org_id       TEXT,
  user_id      TEXT,
  role         TEXT,
  method       TEXT,
  path         TEXT,
  target_table TEXT,
  row_count    INTEGER,
  status       INTEGER
);
--;;
CREATE INDEX IF NOT EXISTS idx_access_log_org ON access_log(org_id, id);
--;;
-- ── Append-only enforcement (same pattern/function as 002) ─────────────────
CREATE OR REPLACE FUNCTION atp_append_only() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'append-only: % on % is forbidden', TG_OP, TG_TABLE_NAME;
END;
$$ LANGUAGE plpgsql;
--;;
DROP TRIGGER IF EXISTS trg_access_log_append_only ON access_log;
--;;
CREATE TRIGGER trg_access_log_append_only
BEFORE UPDATE OR DELETE ON access_log
FOR EACH ROW EXECUTE FUNCTION atp_append_only();
--;;
-- ── Seed: bootstrap org (and nothing else) ─────────────────────────────────
-- Legacy single-admin sessions and BU_BOOTSTRAP_ADMIN_* provisioning map to
-- this org (api/identity.py). domain stays NULL: no OIDC domain auto-join.
INSERT INTO orgs (id, name, domain, created_at)
VALUES ('org-demo', 'Demo Org', NULL,
        to_char(now() AT TIME ZONE 'utc', 'YYYY-MM-DD"T"HH24:MI:SS"Z"'))
ON CONFLICT (id) DO NOTHING;
--;;
-- Belt-and-braces for prod (run manually as the DB owner; the trigger above
-- already blocks the app):
--
--   REVOKE UPDATE, DELETE ON access_log FROM <app_role>;
