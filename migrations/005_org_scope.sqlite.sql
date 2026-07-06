-- 005_org_scope (sqlite) — Phase 2 tenancy (docs/TENANCY.md): every tenant
-- table gains `org_id TEXT NOT NULL DEFAULT 'org-demo'` plus an
-- (org_id, <pk>) index.
--
-- The 'org-demo' default is the backward-compat bridge: all pre-tenancy rows
-- (and any writer not yet passing an org) belong to the bootstrap demo org,
-- so the deployed single-admin demo keeps working unchanged.
--
-- SQLite has NO row-level security: dev/demo isolation relies on layers 1-2
-- of docs/TENANCY.md (route deps + the atp/tenant_db.py scoped DAL). This is
-- a documented, dev-only gap; the Postgres twin of this migration
-- (005_org_scope.pg.sql) adds layer 3 (RLS).
--
-- Existing append-only triggers on atp_hitl / atp_evidence (migration 002)
-- are unaffected by ADD COLUMN and keep firing.
--
-- No trigger bodies here, so plain ';' statement splitting applies
-- (see atp/db.py). Idempotency comes from schema_migrations tracking —
-- SQLite has no "ADD COLUMN IF NOT EXISTS", so this file must only ever run
-- once per database, which the migration runner guarantees.

ALTER TABLE atp_hitl        ADD COLUMN org_id TEXT NOT NULL DEFAULT 'org-demo';
ALTER TABLE atp_requests    ADD COLUMN org_id TEXT NOT NULL DEFAULT 'org-demo';
ALTER TABLE atp_evidence    ADD COLUMN org_id TEXT NOT NULL DEFAULT 'org-demo';
ALTER TABLE atp_cert_awards ADD COLUMN org_id TEXT NOT NULL DEFAULT 'org-demo';
ALTER TABLE jobs            ADD COLUMN org_id TEXT NOT NULL DEFAULT 'org-demo';

-- (org_id, <pk>) per docs/TENANCY.md invariants. jobs has no `id` column —
-- its pk is job_id; atp_requests' pk is TEXT id.
CREATE INDEX IF NOT EXISTS idx_atp_hitl_org        ON atp_hitl(org_id, id);
CREATE INDEX IF NOT EXISTS idx_atp_requests_org    ON atp_requests(org_id, id);
CREATE INDEX IF NOT EXISTS idx_atp_evidence_org    ON atp_evidence(org_id, id);
CREATE INDEX IF NOT EXISTS idx_atp_cert_awards_org ON atp_cert_awards(org_id, id);
CREATE INDEX IF NOT EXISTS idx_jobs_org            ON jobs(org_id, job_id);
