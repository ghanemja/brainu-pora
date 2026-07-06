-- 007_knowledge (postgres) — Phase 6 first-customer UX (docs/HARDENING.md):
-- company-knowledge ingestion (vault docs) + generated L5 exam drafts, PLUS
-- layer 3 (RLS) on both tables.
--
-- Data class T2 "crown jewels" (docs/TENANCY.md): uploaded company documents
-- and the exam items derived from them. Protection = T1 (org-scoped queries
-- via atp/tenant_db.py + RLS below) PLUS Fernet encryption at rest via
-- atp/crypto.py encrypt_for_org (per-org HKDF subkeys):
--   * vault_docs.content_enc / summary_enc  — 'enc1:…' ciphertext, never
--     plaintext (leak surface #7: T2 columns are ciphertext in dumps by
--     construction).
--   * l5_drafts.items_json_enc              — exam items derived from the
--     docs, encrypted for the same reason; the blueprint (section names +
--     weights only) stays plaintext for review listings.
-- Tenant files NEVER land under /videos or /media (leak surface #4) — there
-- is no file path at all: content lives only in these encrypted columns.
--
-- Mutability model: NOT append-only, by design. Drafts are working documents
-- (draft -> approved | rejected state transitions; docs move uploaded ->
-- drafted -> signed). The tamper-evident record of who signed what lives in
-- the atp_evidence hash chain instead: approve/reject writes a signed
-- 'sme_signoff' evidence row via atp/signing.py append_chain.
--
-- RLS model — DENY BY DEFAULT, exactly the 005 policy pattern:
--   * org_isolation on both tables:
--       USING / WITH CHECK (org_id = current_setting('app.org_id', true))
--     current_setting(..., true) is NULL when unset → predicate NULL → row
--     invisible / write rejected. Do NOT add a NULL fallback (see 005).
--   * FORCE ROW LEVEL SECURITY so the table-owner app role has no bypass.
--   * No extra policies: unlike licenses (006 key_lookup) there is no
--     key-only access path — every read/write is org-authenticated.
--
-- Statement separator convention: a line containing only `--;;` splits this
-- file into statements (see atp/db.py).

CREATE TABLE IF NOT EXISTS vault_docs (
  id          TEXT PRIMARY KEY,
  org_id      TEXT NOT NULL DEFAULT 'org-demo',
  title       TEXT NOT NULL,
  filename    TEXT,
  mime        TEXT,
  content_enc TEXT NOT NULL,   -- Fernet 'enc1:…' via crypto.encrypt_for_org
  summary_enc TEXT,            -- heuristic summary, encrypted too (T2)
  uploaded_by TEXT,
  created_at  TEXT NOT NULL,
  status      TEXT NOT NULL DEFAULT 'uploaded'
              CHECK (status IN ('uploaded', 'drafted', 'signed'))
);
--;;
-- (org_id, <pk>) per docs/TENANCY.md invariants.
CREATE INDEX IF NOT EXISTS idx_vault_docs_org ON vault_docs(org_id, id);
--;;
CREATE TABLE IF NOT EXISTS l5_drafts (
  id             TEXT PRIMARY KEY,
  org_id         TEXT NOT NULL DEFAULT 'org-demo',
  cert_label     TEXT NOT NULL,
  blueprint_json TEXT NOT NULL,  -- sections/weights only — reviewable, plaintext
  items_json_enc TEXT NOT NULL,  -- T2: items derived from docs are encrypted
  doc_ids_json   TEXT NOT NULL,  -- JSON array of vault_docs.id this draft covers
  status         TEXT NOT NULL DEFAULT 'draft'
                 CHECK (status IN ('draft', 'approved', 'rejected')),
  created_by     TEXT,
  created_at     TEXT NOT NULL,
  reviewed_by    TEXT,
  reviewed_at    TEXT,
  review_note    TEXT
);
--;;
CREATE INDEX IF NOT EXISTS idx_l5_drafts_org ON l5_drafts(org_id, id);
--;;
-- ── Row-Level Security (layer 3, 005 pattern) ───────────────────────────────
-- CREATE POLICY has no IF NOT EXISTS → DROP IF EXISTS first so a
-- partially-applied database can be re-run safely.
ALTER TABLE vault_docs ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE vault_docs FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON vault_docs;
--;;
CREATE POLICY org_isolation ON vault_docs FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
--;;
ALTER TABLE l5_drafts ENABLE ROW LEVEL SECURITY;
--;;
ALTER TABLE l5_drafts FORCE ROW LEVEL SECURITY;
--;;
DROP POLICY IF EXISTS org_isolation ON l5_drafts;
--;;
CREATE POLICY org_isolation ON l5_drafts FOR ALL
  USING      (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
