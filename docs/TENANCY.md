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
