-- 004_identity (sqlite) — Phase 2 identity & tenancy principals:
-- orgs, org-aware users, append-only access_log (docs/TENANCY.md).
--
-- NOTE on `users`: migration 001 already created `users` as the learner
-- profile table (user_id TEXT PK, display_name, created_at REAL — written by
-- agents/persistence.py). Rather than a second colliding table, this
-- migration EXTENDS it with the identity columns from docs/TENANCY.md:
-- `user_id` serves as the spec's `id`; legacy learner rows keep NULL
-- org_id/email/role and are invisible to identity lookups (which filter on
-- email / (oidc_iss, oidc_sub)).
--
-- Conventions:
--   * ts / created_at columns added here are ISO-8601 UTC strings
--     ("%Y-%m-%dT%H:%M:%SZ"), matching atp/store.py `_now()`.
--     (users.created_at stays REAL — pre-existing column from 001.)
--   * access_log is APPEND-ONLY at the DB level: BEFORE UPDATE / BEFORE
--     DELETE triggers abort with 'append-only' (same pattern as 002).
--   * role CHECK (admin|sme|viewer) is enforced by triggers because SQLite
--     cannot ALTER TABLE ... ADD CHECK; NULL stays allowed for legacy
--     learner rows.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py). Plain ';' inside a statement (e.g.
-- trigger bodies below) is NOT a separator once the marker is used anywhere
-- in the file.

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
ALTER TABLE users ADD COLUMN org_id   TEXT REFERENCES orgs(id);
--;;
ALTER TABLE users ADD COLUMN email    TEXT;
--;;
ALTER TABLE users ADD COLUMN role     TEXT;
--;;
ALTER TABLE users ADD COLUMN oidc_iss TEXT;
--;;
ALTER TABLE users ADD COLUMN oidc_sub TEXT;
--;;
ALTER TABLE users ADD COLUMN pw_hash  TEXT;
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
-- role CHECK via triggers (NULL allowed — legacy learner rows have no role)
CREATE TRIGGER IF NOT EXISTS trg_users_role_check_insert
BEFORE INSERT ON users
WHEN NEW.role IS NOT NULL AND NEW.role NOT IN ('admin', 'sme', 'viewer')
BEGIN
  SELECT RAISE(ABORT, 'users.role must be admin|sme|viewer');
END;
--;;
CREATE TRIGGER IF NOT EXISTS trg_users_role_check_update
BEFORE UPDATE ON users
WHEN NEW.role IS NOT NULL AND NEW.role NOT IN ('admin', 'sme', 'viewer')
BEGIN
  SELECT RAISE(ABORT, 'users.role must be admin|sme|viewer');
END;
--;;
-- ── access_log — tenant-data audit trail (TENANCY.md layer 4) ──────────────
CREATE TABLE IF NOT EXISTS access_log (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
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
-- ── Append-only enforcement (same pattern as 002 atp_hitl) ─────────────────
CREATE TRIGGER IF NOT EXISTS trg_access_log_no_update
BEFORE UPDATE ON access_log
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
--;;
CREATE TRIGGER IF NOT EXISTS trg_access_log_no_delete
BEFORE DELETE ON access_log
BEGIN
  SELECT RAISE(ABORT, 'append-only');
END;
--;;
-- ── Seed: bootstrap org (and nothing else) ─────────────────────────────────
-- Legacy single-admin sessions and BU_BOOTSTRAP_ADMIN_* provisioning map to
-- this org (api/identity.py). domain stays NULL: no OIDC domain auto-join.
INSERT INTO orgs (id, name, domain, created_at)
VALUES ('org-demo', 'Demo Org', NULL, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
ON CONFLICT (id) DO NOTHING;
