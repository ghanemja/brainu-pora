# ATP Production Hardening — running log

Executed in order; one commit per phase. Ground rules (user-set): no git-history
rewrites, no secret rotation in-repo (handled out-of-band), no force-push.

## Phase 0 — Secrets out of code ✅ (2026-07-05)
64 references catalogued; live values redacted from DEPLOY.md /
HF_SPACES_DEPLOY.md / PORTFOLIO_ENV.md; `api/auth.py` fails loudly at startup
when auth is enabled and `BU_AUTH_PASSWORD`/`BU_AUTH_SECRET` unset
(`BU_AUTH_DISABLED=1` = explicit dev opt-in w/ loud banner); `.env.example`
covers every secret env var (keys only); `.gitignore` covers env files.
Deferred by rule: rotation + history purge (out-of-band). Note: rotating the
shared `BU_AUTH_SECRET` logs out all portfolio Spaces at once.

## Phase 1 — Real persistence (contract)
Problem: SQLite on ephemeral disk + single-worker assumptions lose cert
awards, HITL audit log, commissions on restart.

- `atp/db.py` — SQLAlchemy 2.x engine from `DATABASE_URL`
  (default `sqlite:///data/brain_university.db` so dev/demo still works;
  Postgres in prod: `postgresql+psycopg2://…`). `pool_pre_ping=True`,
  `pool_size`/`max_overflow` env-tunable. Migration runner: numbered files in
  `migrations/` (`NNN_name.{sql,pg.sql,sqlite.sql}` — dialect suffix wins),
  tracked in `schema_migrations`, applied at startup, idempotent.
- `migrations/001_core` — ports all existing SQLite tables (users, walks,
  walk_events, sr_cards, podcast_state, feedback, socratic_sessions, jobs)
  plus ATP tables: `atp_hitl`, `atp_requests`, `atp_evidence`,
  `atp_cert_awards`.
- **Append-only at the DB level**: BEFORE UPDATE/DELETE triggers on
  `atp_hitl` + `atp_evidence` raise (both dialects). Postgres additionally
  documents `REVOKE UPDATE, DELETE` for the app role.
- `agents/persistence.py` + `agents/jobs.py` + `atp/store.py` ported to the
  DAL, public function signatures preserved (callers untouched where
  possible). HITL/requests move from jsonl to tables; `read_*` keep
  latest-first contracts.
- Multi-worker/instance: stateless HMAC auth (P0) + DB-backed jobs/state;
  Dockerfile `WORKERS` env (default 1); jobs claimed atomically
  (`UPDATE … WHERE status='queued'` guard).
- render.yaml: `DATABASE_URL` (sync:false) + comment for Render Postgres.
- Verify: full boot + API smoke on SQLite; Postgres DDL applied against a
  disposable Docker Postgres when available, else dialect-lint + documented.

## Phase 2 — Auth + multi-tenancy (contract)
OIDC code flow (issuer/client from env: `OIDC_ISSUER`, `OIDC_CLIENT_ID`,
`OIDC_CLIENT_SECRET`, `OIDC_REDIRECT_URL`) + local dev accounts (argon2
hashes, seed admin via env). JWT session tokens carry `org_id` + `role`
(admin | sme | viewer). New tables: orgs, users(org_id, role, oidc_sub),
`access_log` (append-only). Tenancy: every tenant-scoped table gains
`org_id`; DAL exposes only org-scoped query helpers (no raw table access from
routes); L5/company fields encrypted at rest (Fernet, `DATA_ENCRYPTION_KEY`).
Isolation model + leak-surface analysis written to `docs/TENANCY.md`.

## Phase 3 — Certification engine (contract)
`atp/exams.py`: blueprint → item bank (`atp/items/*.json` per cert, generated
+ human-editable) → exam run via `agents/orchestrator`/`backend.get_backend`
(candidate spec) → judge via a DIFFERENT model family, enforced in code
(`family_of(candidate) != family_of(judge)` else refuse) → verdict via
`qa_gate`-style thresholds vs cert `passCriteria` → evidence records written
append-only, each **HMAC-SHA256-signed** (`EVIDENCE_SIGNING_KEY`) over a
canonical payload + `prev_hash` chain (tamper-evident). `--dry-run` mode
(deterministic stub model) so CI can exercise the loop. Deep links:
hash-router `#/agent/{id}`, `#/cert/{id}`, `#/evidence/{id}` resolve on load.

## Phase 4 — Billing + marketplace (contract)
Stripe (env `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET`; test-mode friendly):
products/prices per listing, checkout session endpoint, webhook →
`licenses` table (org-scoped, status active|revoked|expired, license key =
signed token). Delivery: `/experts/{agent_id}/chat` proxy endpoint gated on a
valid license key + metering row per call (`usage_events`). Revocation:
`licenses.status='revoked'` enforced by the gate middleware on every call
(not just flagged) + license-key signature includes status-check nonce.

## Phase 5 — Ops (contract)
Prod frontend: pinned React **production** UMD self-hosted under
`design/vendor/` (no CDN, no SRI drift) + `scripts/build_frontend.py`
precompiling all `.jsx` → `.js` with Babel at deploy (Netlify build cmd), HTML
switching on compiled bundles when present (dev mode keeps in-browser Babel).
CI (GitHub Actions): P0 boot matrix, seed referential-integrity check, ruff
lint, Playwright smoke (login → 6 agent screens render). In-app rate limiting
(token bucket per IP+token, env-tuned). `/metrics` (Prometheus format) +
structured JSON logs. `scripts/backup_db.sh` (pg_dump + evidence export,
cron-ready). `render.staging.yaml`. Hash-based URL routing shared with P3
deep links.

## Phase 6 — First-customer UX (contract)
Company-knowledge ingestion: upload endpoint (md/pdf/txt) → Vault-LD pages
(org-scoped) → generated L5 exam draft (blueprint + items) → SME review/sign-
off UI (role=sme) → cert eligible. Agent-view onboarding tour (tutorial.jsx
pattern). Report-card PDF export endpoint (server-side, reportlab) +
download button on agent profile.
