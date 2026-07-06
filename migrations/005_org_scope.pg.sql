-- 005_org_scope (postgres) — Phase 2 tenancy (docs/TENANCY.md): org_id
-- columns + (org_id, <pk>) indexes on every tenant table, PLUS layer 3:
-- Row-Level Security.
--
-- The 'org-demo' default is the backward-compat bridge: all pre-tenancy rows
-- (and any writer not yet passing an org) belong to the bootstrap demo org.
--
-- RLS model — DENY BY DEFAULT, no permissive fallback:
--   * Policy predicate: org_id = current_setting('app.org_id', true).
--     current_setting(..., true) returns NULL when the setting is absent, so
--     the predicate is NULL → row invisible / write rejected. A session that
--     forgets to set app.org_id sees ZERO rows — that is intentional; do NOT
--     "fix" it by adding an `OR current_setting(...) IS NULL` fallback.
--   * FORCE ROW LEVEL SECURITY: on managed Postgres (Render) the app role is
--     usually the table OWNER, and owners bypass plain ENABLE'd RLS. FORCE
--     applies the policy to the owner too, so there is no bypass path from
--     the application credentials.
--   * The app sets the org per transaction via atp/tenant_db.py:
--       SELECT set_config('app.org_id', :org, true)   -- == SET LOCAL
--     inside the same transaction as the scoped statement. ALL application
--     access to these tables must therefore go through atp/tenant_db.py
--     (raw atp.db query()/execute() on tenant tables returns nothing / fails
--     WITH CHECK — by design).
--   * Superuser / a separate migration-owner role can still ALTER; app-role
--     credentials cannot disable their own policies unless they own the
--     tables — for defense in depth run the 002-documented REVOKEs and,
--     where possible, run the app as a non-owner role.
--
-- Ordering dependency: `access_log` is created by migration 004 (orgs /
-- users / access_log); 004 < 005 so it exists by the time this file runs.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py).

ALTER TABLE atp_hitl        ADD COLUMN IF NOT EXISTS org_id TEXT NOT NULL DEFAULT 'org-demo';
--;;
ALTER TABLE atp_requests    ADD COLUMN IF NOT EXISTS org_id TEXT NOT NULL DEFAULT 'org-demo';
--;;
ALTER TABLE atp_evidence    ADD COLUMN IF NOT EXISTS org_id TEXT NOT NULL DEFAULT 'org-demo';
--;;
ALTER TABLE atp_cert_awards ADD COLUMN IF NOT EXISTS org_id TEXT NOT NULL DEFAULT 'org-demo';
--;;
ALTER TABLE jobs            ADD COLUMN IF NOT EXISTS org_id TEXT NOT NULL DEFAULT 'org-demo';
--;;
-- (org_id, <pk>) per docs/TENANCY.md invariants. jobs has no `id` column —
-- its pk is job_id; atp_requests' pk is TEXT id.
CREATE INDEX IF NOT EXISTS idx_atp_hitl_org        ON atp_hitl(org_id, id);
--;;
CREATE INDEX IF NOT EXISTS idx_atp_requests_org    ON atp_requests(org_id, id);
--;;
CREATE INDEX IF NOT EXISTS idx_atp_evidence_org    ON atp_evidence(org_id, id);
--;;
CREATE INDEX IF NOT EXISTS idx_atp_cert_awards_org ON atp_cert_awards(org_id, id);
--;;
CREATE INDEX IF NOT EXISTS idx_jobs_org            ON jobs(org_id, job_id);
--;;
-- ── Row-Level Security (layer 3) ───────────────────────────────────────────
-- CREATE POLICY has no IF NOT EXISTS → DROP IF EXISTS first (002 trigger
-- pattern) so a partially-applied database can be re-run safely.

ALTER TABLE atp_hitl ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE atp_hitl FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON atp_hitl;
--;;
CREATE POLICY org_isolation ON atp_hitl FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
--;;
ALTER TABLE atp_requests ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE atp_requests FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON atp_requests;
--;;
CREATE POLICY org_isolation ON atp_requests FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
--;;
ALTER TABLE atp_evidence ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE atp_evidence FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON atp_evidence;
--;;
CREATE POLICY org_isolation ON atp_evidence FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
--;;
ALTER TABLE atp_cert_awards ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE atp_cert_awards FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON atp_cert_awards;
--;;
CREATE POLICY org_isolation ON atp_cert_awards FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
--;;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE jobs FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON jobs;
--;;
CREATE POLICY org_isolation ON jobs FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
--;;
-- access_log is created in 004 with an org_id column (nullable — rows with
-- NULL org_id are simply invisible under the policy below, which is the
-- correct deny-by-default). The ADD COLUMN is a belt-and-braces no-op that
-- keeps this file valid even if 004's shape drifts; the (org_id, id) index
-- lives with its DDL in 004.
ALTER TABLE access_log ADD COLUMN IF NOT EXISTS org_id TEXT NOT NULL DEFAULT 'org-demo';
--;;
ALTER TABLE access_log ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE access_log FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON access_log;
--;;
CREATE POLICY org_isolation ON access_log FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
