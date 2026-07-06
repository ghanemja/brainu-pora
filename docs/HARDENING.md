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

## Phase 1 — delivered: atp/store.py DAL port ✅ (2026-07-06)
HITL + compose-request logs moved from `data/sessions/*.jsonl` to the
`atp_hitl` / `atp_requests` tables (migration 002) via `atp/db.py`
(`get_engine()` + `run_migrations()`, invoked lazily on first log access —
idempotent, so the startup run stays authoritative). Public surface
unchanged: same function signatures, same camelCase dict keys (snake_case
columns mapped back, JSON-text columns `json.loads`'d), `read_*` still
latest-first — `api/atp.py` untouched. Latest-first ordering uses the
monotonic surrogate: `atp_hitl.id` (autoincrement/BIGSERIAL); `atp_requests`
has a TEXT pk, so sqlite orders by implicit `rowid`, Postgres falls back to
`ts DESC` (second-resolution ties among same-second requests are unordered —
cosmetic; add a BIGSERIAL `seq` in a later migration if it ever matters).
One-time lazy legacy import: if `atp_hitl.jsonl` / `atp_requests.jsonl`
exists and its table is empty, the file is renamed to `*.jsonl.imported`
(the atomic rename doubles as the cross-process claim) and its rows inserted
oldest-first; reruns are no-ops. Verified on a fresh tmp sqlite DB against
the real migrations: §1 formula (`weightedDelta = signal × 0.2 ×
(w/0.26)`), latest-first reads, the 3 canonical compose payloads
(18/18-C/atp-l6-math → matched theorem-math; junk specialty → gap;
6/6-3/atp-l6-bio → gap), legacy import + idempotency, UPDATE/DELETE on
`atp_hitl` aborting via trigger, plus a TestClient smoke over the untouched
`/atp/*` routes and the `BU_AUTH_DISABLED=1` boot check.

## Phase 3 — delivered: exam-core (engine + signing + item banks) ✅ (2026-07-06)
`atp/exams.py` `run_exam(cert_id, candidate_spec=None, org_id='org-demo',
dry_run=False, agent_id=None) -> award dict`: seed cert → item bank
(`atp/items/<cert_id>.json`; missing bank raises `MissingItemBankError` —
blueprints-before-commissioning) → per item × `runs=min(passCriteria.runs,3)`:
candidate answer via `get_backend()`, judge scores strict JSON
`{score 0..1, rationale}` (defensive parse, one retry, else item flagged &
scored 0) → points-weighted section scores, blueprint-weighted overall,
verdict vs `passCriteria` (overall + perSection + zero flagged) → one signed
`exam_item` evidence row per item + one `benchmark_run` summary + an
`atp_cert_awards` row, all through `atp/tenant_db` (org-scoped, RLS on PG).
**Judge/candidate separation enforced in code before any model call**:
`family_of(judge) != family_of(candidate)` else `SeparationError`; judge from
env `ATP_JUDGE_SPEC` (default `claude-haiku-4-5`), `dry_run` →
`dryrun:judge`. `agents/backend.py` gains `family_of()`
(claude/gemma/llama/qwen/deepseek/mistral/gpt/stub, substring;
unknown→'unknown') + `DryRunBackend` — deterministic pure function of the
prompts (SHA-256-driven; judge-style prompts get valid JSON w/ score in
[0.55, 0.95)); `dryrun:candidate`/`dryrun:judge` map to distinct synthetic
families ('stub-a'/'stub-b') so CI exercises the whole loop incl. separation.
`atp/signing.py`: `canonical()` (sorted-keys/compact JSON), `sign(payload,
prev_hash)` = HMAC-SHA256(`EVIDENCE_SIGNING_KEY`) over `prev_hash ||
canonical(payload)`, `verify_row()`, `last_sig(org)`, `verify_chain(org) ->
{ok, length, first_bad}` — per-org prev_hash chain rooted at `'genesis'`;
key is fail-loud (`SigningKeyError`) when unset with auth enabled;
`BU_AUTH_DISABLED=1` dev fallback derives from `BU_AUTH_SECRET` or uses a
process-ephemeral key w/ loud warning. `.env.example` documents
`EVIDENCE_SIGNING_KEY` (key only). Item banks: `atp-l4-math` (18 items, all 4
blueprint sections, adversarial incl.) + `atp-l1-core` (11 items) + SME
editing guide (`atp/items/README.md`); banks are validated at load (section
names must match the blueprint, every section covered). CLI:
`python3 -m atp.exams <cert> [--candidate S] [--dry-run] [--verify-chain]`.
Verified on fresh sqlite: dry-run `atp-l4-math` → award w/ verdict, 19
evidence rows, `verify_chain` ok; rerun appends (19→38, still ok); identical
inputs + key + empty chain reproduce byte-identical sigs; candidate
`claude-haiku-4-5` vs default claude judge → `SeparationError` before any
model call; unknown cert / bank-less cert raise; rotated key flips the chain
to `{ok: false, first_bad: 1}`; `BU_AUTH_DISABLED=1` boot unaffected.
Still open in Phase 3 (other owners): deep-link hash routing
(`#/agent/{id}`, `#/cert/{id}`, `#/evidence/{id}`) and API/UI surfacing of
live awards.

## Phase 4 — delivered: license-core (issue/verify/revoke/meter) ✅ (2026-07-06)
`atp/licensing.py` + migration 006 (`licenses` + `usage_events`, both
dialects). Licenses are T1 org-scoped (docs/TENANCY.md): all reads/writes go
through `atp/tenant_db.py`; on Postgres 006 adds ENABLE+FORCE RLS with the
005 `org_isolation` policy on BOTH tables, plus ONE narrow addition on
`licenses` only — a SELECT-only `key_lookup` policy
(`key_id = current_setting('app.license_key_id', true)`) so
`check_license()` can resolve a signature-verified key to its row without an
org context (the gated proxy's caller is a machine holding only the key; the
org is learned FROM the row, and every subsequent write goes back through
the org-scoped DAL). Deny-by-default preserved: absent both GUCs the
predicates are NULL → zero rows. **Stripe is OPTIONAL by design**: without
`STRIPE_API_KEY` the platform issues 'manual' licenses (invoice-billed
design partners; `stripe_customer`/`stripe_subscription` NULL) and
gating/metering/revocation work identically — Stripe only adds self-serve
checkout on top (other owners: checkout/webhook/gate routes).
Key format `atpk_<key_id>.<sig>` with `sig =
HMAC-SHA256(LICENSE_SIGNING_KEY, key_id)[:32]` — shown ONCE at issue; only
`key_id` stored (key material is unrecoverable from the DB). Key resolution
mirrors `atp/signing.py`: fail-loud `LicenseSigningKeyError` when unset with
auth enabled; `BU_AUTH_DISABLED=1` derives from `BU_AUTH_SECRET` (distinct
domain tag) or uses a process-ephemeral key with a loud warning.
**Revocation = DB state, the key alone never suffices**: `check_license()`
does constant-time HMAC verify (`hmac.compare_digest`, no DB hit for forged
keys) THEN enforces `status=='active'` and `expires_at` NULL/future on the
live row — revoked/expired rows fail instantly regardless of a valid
signature; expired-by-date rows are auto-flipped to `'expired'` on check
(`licenses` is mutable by design). `usage_events` is APPEND-ONLY (BEFORE
UPDATE/DELETE triggers, both dialects — 002 idiom; usage is billing
evidence). Indexes: `(org_id, id)` both tables + UNIQUE `key_id`.
`issue_license` validates agent against the marketplace seed
(`licensing.available`); `list_licenses`/`usage_summary` return camelCase,
latest-first, never key material. `.env.example` documents
`LICENSE_SIGNING_KEY` + optional `STRIPE_API_KEY`/`STRIPE_WEBHOOK_SECRET`.
Verified fresh-sqlite e2e (40 checks): issue → check ok → revoke → check
`{ok:false,reason:'revoked'}` instantly; expired-date flip + fail; tampered/
forged/malformed keys fail; usage UPDATE/DELETE abort 'append-only'; summary
math; cross-org: org-B cannot list/revoke org-A licenses. ALSO verified on
disposable Docker Postgres 16 **as a non-superuser table-owner role** (the
Render configuration FORCE RLS targets): 001→006 apply + rerun no-op; raw
un-scoped SELECT sees 0 rows; `key_lookup` resolves exactly the pinned key
and rejects writes (UPDATE rowcount 0); PG append-only trigger fires;
cross-org isolation holds under RLS. Boot smoke: `BU_AUTH_DISABLED=1` dev
boot unaffected, 006 applies at startup.
Still open in Phase 4 (other owners): Stripe checkout/webhook routes, admin
license API (`require_role`), `/experts/{agent_id}/chat` gate + metering
middleware, `stripe` lib in requirements.
