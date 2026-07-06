# ATP Tenancy & Isolation Model (Phase 2)

Written BEFORE implementation, per hardening plan. This is the model the code
must satisfy; the leak-surface table is the checklist reviewers verify against.

## Principals

- **Org** (tenant): every customer company. Row in `orgs`. All tenant data
  carries `org_id`.
- **User**: belongs to exactly one org. `users(org_id, role, oidc_iss,
  oidc_sub, email, pw_hash?)`. Roles:
  - `admin` — org settings, members, licenses, policy bindings.
  - `sme` — review/sign-off on L5 exams + evidence; submit HITL rewards.
  - `viewer` — read dashboards, agents, certs; no writes.
- **Platform operator** (us): separate `platform_admin` flag, never implied by
  org membership.

## Sessions & identity

- OIDC authorization-code flow (`OIDC_ISSUER`, `OIDC_CLIENT_ID`,
  `OIDC_CLIENT_SECRET`, `OIDC_REDIRECT_URL`): verify `id_token` against issuer
  JWKS; provision/link user by `(iss, sub)`; org resolved by verified email
  domain → `orgs.domain` allowlist, else invite token.
- Local accounts (dev + fallback): argon2id hashes; seed admin from
  `BU_BOOTSTRAP_ADMIN_EMAIL`/`_PASSWORD` env (fail-loud if partial).
- Session = JWT (HS256, `BU_AUTH_SECRET`), claims `{sub, org_id, role, exp}`.
  Legacy single-admin token keeps working ONLY under `BU_AUTH_DISABLED=1`
  (dev) — the enabled path requires org-scoped JWTs.

## Data classes

| Class | Examples | Protection |
|---|---|---|
| T0 public | ATP standard, seed catalog, marketplace listings | none (read-only endpoints) |
| T1 org-internal | HITL log, expert requests, cert awards, evidence, usage | org-scoped queries + RLS + access log |
| T2 crown jewels | L5 company docs, Vault-LD pages, L5 exam items | T1 + Fernet encryption at rest (`DATA_ENCRYPTION_KEY`, per-org subkey via HKDF(org_id)) |

## Enforcement — four layers (defense in depth)

1. **Route layer**: FastAPI dependencies `require_auth` → `require_role(x)`;
   org_id ONLY ever read from the verified JWT, never from request body/query.
2. **DAL layer**: tenant tables readable/writable exclusively through
   `atp/tenant_db.py` scoped helpers (`scoped_query(org, …)`) that inject
   `WHERE org_id = :org`. Routes are forbidden (by convention + CI grep) from
   raw `query()/execute()` on tenant tables.
3. **DB layer (Postgres)**: Row-Level Security on every tenant table —
   `SET LOCAL app.org_id` per request/transaction, policy
   `USING (org_id = current_setting('app.org_id'))`. SQLite dev relies on
   layers 1–2 (documented gap, dev-only).
4. **Audit**: `access_log` (append-only triggers, same as `atp_hitl`):
   `{ts, org_id, user, role, method, path, table?, row_count, status}` written
   by middleware for every authenticated request touching tenant data.

## Leak surfaces (enumerated) and their closure

| # | Surface | Risk | Closure |
|---|---|---|---|
| 1 | `GET /atp/hitl`, `GET /atp/requests` currently GLOBAL | org A sees org B rewards/commissions | add `org_id` columns (migration 004), scope reads by JWT org; seed demo rows belong to `org-demo` |
| 2 | Jobs table shared | job payloads may embed tenant data | `jobs.org_id` + scoped `GET /jobs/{id}` (404 cross-tenant, not 403 — don't leak existence) |
| 3 | SSE streams (`/debate/stream`, paper drop) | long-lived responses bypass middleware afterthoughts | auth + org checked BEFORE stream starts; no tenant data in stream ids |
| 4 | `/videos/*`, `/media/*` public prefixes | tenant artifacts written under public media dir | tenant uploads NEVER land in those dirs; new `/orgs/{org}/files/*` gated route; CI grep forbids writes to design/videos from tenant paths |
| 5 | Marketplace (intentionally cross-tenant) | listing copy could embed L5 details | listings built ONLY from T0 seed fields + cert labels; commissioned listings show corpus PROVENANCE strings (OCW ids), never pack contents; SME sign-off names shown only to own org |
| 6 | Error messages / 404 vs 403 | existence oracle across tenants | cross-tenant access always 404; validation errors never echo other-org ids |
| 7 | Logs & backups | plaintext T2 in logs/dumps | structured logs redact payload fields; backups encrypt (Phase 5); T2 columns are ciphertext in dumps by construction |
| 8 | In-memory caches (graph cache, seed) | global caches fine (T0); any future per-org cache must key by org_id | convention documented here + CI grep for `lru_cache` on tenant fns |
| 9 | `GET /atp/data` | global seed blob — T0 only | keep; never merge tenant rows into it |
| 10 | Encryption key compromise | one key unlocks all orgs | HKDF per-org subkeys; key rotation re-wrap procedure documented; key only via env |

## Invariants (CI-checkable)

- No route handler passes a client-supplied org id into any query.
- Every tenant table has: `org_id TEXT NOT NULL`, an index on `(org_id, id)`,
  an RLS policy (PG), and appears in the access-log middleware's table map.
- `access_log`, `atp_hitl`, `atp_evidence` reject UPDATE/DELETE (triggers).
- Cross-tenant read attempts in the test suite return 404 and produce an
  access_log row with `status=404`.

## Implemented — data layer (Phase 2, 2026-07-06)

Notes appended AFTER implementation by the tenant-DAL work; the model above
is unchanged — this section records how the code satisfies it and the exact
contracts reviewers/CI can grep for.

### Migration `005_org_scope` (layers 2-3 substrate)

- Both dialects: `atp_hitl`, `atp_requests`, `atp_evidence`,
  `atp_cert_awards`, `jobs` gain `org_id TEXT NOT NULL DEFAULT 'org-demo'`
  plus an `(org_id, <pk>)` index. `jobs` has no `id` column — its index is
  `(org_id, job_id)`; `access_log`'s column + `(org_id, id)` index ship with
  its DDL in `004_identity`. The `'org-demo'` default is the backward-compat
  bridge: every pre-tenancy row (and the legacy single-admin path) belongs to
  the bootstrap org, so the deployed demo keeps working with zero env changes.
- Postgres file additionally applies layer 3 to all six tenant tables:
  `ENABLE ROW LEVEL SECURITY` + **`FORCE ROW LEVEL SECURITY`** + policy
  `org_isolation FOR ALL USING (org_id = current_setting('app.org_id', true))
  WITH CHECK (same)`. `current_setting(…, true)` is NULL when the GUC is
  absent → predicate NULL → **deny by default**. There is deliberately NO
  permissive fallback for a missing setting; a session that forgets to set
  `app.org_id` reads zero rows and cannot insert. FORCE binds the table
  owner too (managed hosts hand the app the owner role). Caveat verified in
  testing: SUPERUSER/BYPASSRLS roles still bypass RLS — never run the app as
  one.
- SQLite file is columns+indexes only (layers 1-2, documented dev-only gap).
- Verified: fresh-DB apply + idempotent re-run on SQLite and on a disposable
  Docker Postgres 16 (as a non-superuser owner role: raw unscoped
  SELECT → 0 rows, raw unscoped INSERT → RLS violation, 002/004 append-only
  triggers still abort after the ALTERs).

### `atp/tenant_db.py` (layer 2)

- `scoped_query(org_id, sql, params)` / `scoped_execute(…)`: a simple-parse
  guard — any statement naming a tenant table (word-boundary match against
  `TENANT_TABLES = {atp_hitl, atp_requests, atp_evidence, atp_cert_awards,
  jobs, access_log}`) must carry an `:org` bind (`\b`-anchored, so `:org_id`
  does not satisfy it) AND `params['org'] == org_id`, else
  `TenantScopeError`. False positives only ever demand MORE scoping.
- On Postgres every helper runs inside one transaction that first executes
  `SELECT set_config('app.org_id', :org, true)` — the bind-safe spelling of
  `SET LOCAL app.org_id`; the GUC dies with the transaction so pooled
  connections cannot leak scope (verified).
- `insert_scoped(table, row, org_id)` builds the INSERT itself and
  overwrites any payload-supplied `org_id` with the caller's verified org.
- `log_access(org_id, user, role, method, path, table, row_count, status)`
  appends to `access_log` through the scoped path. Column mapping (004
  schema, reserved words avoided): `user` → `user_id`, `table` →
  `target_table`.
- `DEFAULT_ORG = 'org-demo'` is exported here; org ids must come from the
  verified JWT (layer 1), never from request payloads.

### `atp/crypto.py` (T2 encryption, leak surface #10)

- Envelope format `enc1:<Fernet token>` in TEXT columns; values without the
  prefix are legacy plaintext and read through unchanged (no key needed).
- Master key: `DATA_ENCRYPTION_KEY` env, read at call time. Per-org subkey:
  `HKDF-SHA256(master, info=org_id)` → Fernet key (cached per
  (master, org)); one org's subkey never unlocks another's rows (cross-org
  decrypt raises, verified).
- Fail-loud: any encrypt, or decrypt of an `enc1:` token, without the key →
  `RuntimeError`; tampered/wrong-org tokens → `ValueError`. No silent
  plaintext writes, no silent empty reads.
- Rotation (re-wrap): keep the old master available out-of-band, decrypt
  each T2 value under old, encrypt under new, write back; `enc1` is the
  version tag — future schemes bump to `enc2` so mixed tables stay readable.

### `atp/store.py`

- `append_hitl` / `read_hitl` / `append_request` / `read_requests` gained an
  optional `org_id='org-demo'` keyword; all table access routes through
  `tenant_db` (writes stamped, reads `WHERE org_id = :org`). Signatures,
  returned camelCase shapes (no org key added), §1 formula, compose matching
  and latest-first ordering are unchanged for existing callers — verified
  against the Phase-1 canon (3 compose payloads, legacy JSONL import → rows
  land in `org-demo`, import idempotency) plus a `BU_AUTH_DISABLED=1` boot +
  `/login` (admin/password) + `/atp/*` TestClient smoke.

### Follow-ups this section makes explicit

- `agents/jobs.py` now routes all `jobs` access through `tenant_db` scoped
  helpers (org_id threaded from submit/get) — no raw-access gap remains
  there. Any FUTURE code touching a tenant table must do the same: with
  FORCE RLS on Postgres, raw `atp.db` statements see zero rows / fail
  WITH CHECK.
- CI greps promised by the invariants (no raw tenant-table access outside
  `atp/tenant_db.py`, no `lru_cache` on tenant fns) belong to the Phase 5 CI
  work.
