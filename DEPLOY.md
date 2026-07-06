# Brain University — deploy (leadership demo)

Two backend options. **HF Spaces is the default — free, sleeps when idle.**
Render is the paid alternative for always-on traffic.

| Path | Backend | Cost when idle | Cold start |
|------|---------|----------------|------------|
| **A (default)** | HF Spaces Docker | **$0** | ~30–90 s after 48 h sleep |
| B | Render standard | ~$25/mo | none |

→ **Path A** full guide: [HF_SPACES_DEPLOY.md](HF_SPACES_DEPLOY.md)
→ **Path B** (Render) below.

```
┌──────────────┐  HTTPS   ┌─────────────────────┐  HTTPS   ┌──────────────────┐
│ Netlify      │ ───────► │ HF Space  ─OR─ Render│ ───────► │ LLM              │
│ design/ (UI) │  CORS    │ api/ (FastAPI+ffmpeg)│         │ Claude API  OR   │
│ free         │          │ free  /  $25/mo     │          │ HF Gemma endpoint│
└──────────────┘          └─────────────────────┘          └──────────────────┘
       BU_API_BASE ─────────────┘        ANTHROPIC_API_KEY ──┘
```

---

## Path B · Backend → Render (paid, always-on)

> Use Path A (HF Spaces) for the leadership demo. Path B below is for
> production or sustained traffic where you don't want cold starts.

### 1 · Backend → Render

1. **https://dashboard.render.com → New → Blueprint** → connect this repo
   (`ghanemja/brain-university`). Render reads `render.yaml`.

2. Set these env vars in the Blueprint screen (`sync: false` means you set them
   here, not in source). Generate fresh secrets yourself (see PORTFOLIO_ENV.md
   §1) — values are never committed to this repo.

   | Env var               | Value                                                 |
   |-----------------------|-------------------------------------------------------|
   | `ANTHROPIC_API_KEY`   | (your Anthropic key)                                  |
   | `CORS_ORIGINS`        | (leave blank for now — fill after step 2)             |
   | `BU_AUTH_USER`        | `<REDACTED — set via env, rotation handled out-of-band>` |
   | `BU_AUTH_PASSWORD`    | `<REDACTED — set via env, rotation handled out-of-band>` |
   | `BU_AUTH_SECRET`      | `<REDACTED — set via env, rotation handled out-of-band>` |
   | `BU_AUTH_TTL_HOURS`   | `24` (optional)                                       |

   > **Do not** set `BU_AUTH_DISABLED`. That's a local-only escape hatch.

3. Click **Apply**. First build ~6 min (Docker layer + pip + ffmpeg). Service
   URL appears on the service page: `https://brain-university-api-XXX.onrender.com`.
   Copy it.

4. Smoke-test:
   ```bash
   API=https://brain-university-api-XXX.onrender.com
   curl $API/health
   # → {"ok": true}

   # Uses the BU_AUTH_USER / BU_AUTH_PASSWORD values you set in step 2
   curl -X POST $API/login \
     -H 'Content-Type: application/json' \
     -d "{\"username\":\"$BU_AUTH_USER\",\"password\":\"$BU_AUTH_PASSWORD\"}"
   # → {"token":"...","username":"..."}
   ```

---

## 2 · Frontend → Netlify

1. **https://app.netlify.com → Add new site → Import from Git** → pick this
   repo. Netlify reads `netlify.toml`:
   - Publish dir: `design`
   - Build command: `node scripts/gen-config.mjs` (bakes `BU_API_BASE` into
     `design/config.js` at deploy time, no source edit needed)

2. **Site settings → Environment variables**, add:

   | Env var       | Value                              |
   |---------------|------------------------------------|
   | `BU_API_BASE` | Render URL from step 1.3, no trailing slash |

3. **Deploys → Trigger deploy → Clear cache and deploy**. ~30 s.

4. Copy the Netlify URL, e.g. `https://brain-u.netlify.app`.

5. **Back to Render**: set `CORS_ORIGINS` to that exact Netlify URL (no slash).
   Service redeploys in ~2 min.

---

## 3 · Hand to leadership

> **URL**: https://brain-u.netlify.app
> **Username**: <REDACTED — set via env, rotation handled out-of-band>
> **Password**: <REDACTED — set via env, rotation handled out-of-band>

Tutorial auto-opens on first visit. `?` button in topbar reopens it. Sessions
last 24 h (controlled by `BU_AUTH_TTL_HOURS`).

Suggested pitch path (~90 s): Trailhead → Walk 2 stops → ≈ Bridge → arXivis
paper → + Ingest paper → Open Problems.

---

## 4 · After the demo

- **Pause Render service** to stop billing while idle. Netlify static site is
  free regardless.
- **Rotate password**: change `BU_AUTH_PASSWORD` on Render → redeploy. Users
  with old tokens still in.
- **Revoke ALL sessions immediately**: rotate `BU_AUTH_SECRET` instead — every
  previously-minted token invalidates on the next request.

---

## 5 · LLM choice

| | Path A — Claude (default) | Path B — Hosted Gemma |
|---|---|---|
| Setup | `ANTHROPIC_API_KEY` on Render | HF Inference Endpoint + `LOCAL_LLM_*` env vars |
| Ships today? | Yes | After endpoint provision |
| Cost | per token | ~$0.80/GPU-hr active, $0 idle |
| Switch | — | env change only, no redeploy |

Gemma setup: [HF_ENDPOINT_SETUP.md](HF_ENDPOINT_SETUP.md).

---

## 6 · Troubleshooting

| Symptom | Fix |
|---------|-----|
| Login screen "network error" | `CORS_ORIGINS` mismatch — check trailing slash, http vs https, custom domain |
| Login succeeds but every API call 401s | `BU_AUTH_SECRET` differs between instances (scaled >1) — set the env var explicitly |
| `+ Ingest paper` hangs at "Resolving…" | arxiv.org rate-limited backend; check Render logs |
| Paper detail "No 30-second explainer rendered yet" | Click `Generate 30s explainer` — backend renders in ~5 s via multiprocess |
| 3D brain blank | Browser console: usually three.js peer or process.env shim; reload |

---

## 7 · Cost ballpark

| Service | ~Cost |
|---------|-------|
| Netlify (static, free tier) | $0 |
| Render standard plan (always-on) | ~$25/mo |
| Anthropic API | per token usage |
| HF Gemma endpoint (optional) | ~$0 idle, ~$0.80/GPU-hr active |

≈ **$25–50/mo** all-in for a leadership demo + early beta on Claude.

---

## 8 · Pre-launch checklist

- [ ] `BU_API_BASE` env var set on Netlify (NOT hardcoded in HTML — `config.js` is generated at build)
- [ ] `CORS_ORIGINS` on Render = exact Netlify URL (not `*`)
- [ ] `BU_AUTH_USER` + `BU_AUTH_PASSWORD` + `BU_AUTH_SECRET` set on Render
- [ ] `BU_AUTH_DISABLED` UNSET on Render (it'd disable all auth)
- [ ] `ANTHROPIC_API_KEY` set on Render
- [ ] `/health` returns `{ok:true}` on the Render URL
- [ ] `POST /login` returns a token
- [ ] First load of the Netlify URL shows login → tutorial after success

---

## 9 · Ops runbook (Phase 5)

### 9.1 Backups

`scripts/backup_db.sh` is DATABASE_URL-aware and cron-ready (no prompts,
meaningful exit codes — see the script header):

- **Postgres** → `pg_dump --format=custom` to `backups/atp-YYYYmmdd-HHMMSS.dump`
- **SQLite** (DATABASE_URL unset / `sqlite:///…`) → `sqlite3 .backup` snapshot
  to `backups/atp-YYYYmmdd-HHMMSS.sqlite3`
- **Every run** also exports the audit surfaces as CSV
  (`atp_evidence`, `atp_hitl`, `access_log`, `usage_events` — docs/TENANCY.md)
  and writes + verifies a `atp-<stamp>.sha256` manifest.
- **Encryption** (leak-surface #7, docs/TENANCY.md): set
  `BACKUP_GPG_RECIPIENT=<key id/email>` and every artifact is GPG-encrypted,
  plaintext removed. The manifest hashes the ciphertext, so integrity checks
  never need the private key. Keep the private key OFF the backup host.
- **Retention**: newest `BACKUP_KEEP` runs kept (default 14), older
  `atp-<stamp>.*` files pruned after each successful run.
- The script drops `backups/.gitignore` (`*`) so dumps can never be committed.

**Postgres + RLS**: the ATP tables are `FORCE ROW LEVEL SECURITY`. The script
sets `row_security = off` (and pg_dump does the same by default), so a role
without `BYPASSRLS` fails **loudly** instead of silently exporting 0 rows.
Create a dedicated backup role:

```sql
CREATE ROLE atp_backup LOGIN PASSWORD '…' BYPASSRLS;
GRANT CONNECT ON DATABASE brain_university TO atp_backup;
GRANT USAGE ON SCHEMA public TO atp_backup;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO atp_backup;
```

**Cron example** (any box that can reach the DB — for Render Postgres use the
*External* connection string, or a Render Cron Job service running the same
command from the repo image):

```cron
# Nightly 03:17 UTC, encrypted, keep 30 days
17 3 * * *  cd /srv/brain-university && \
  DATABASE_URL='postgresql://atp_backup:…@…/brain_university' \
  BACKUP_GPG_RECIPIENT=ops@example.com BACKUP_KEEP=30 \
  scripts/backup_db.sh >> /var/log/atp-backup.log 2>&1
```

Exit codes: `0` ok · `1` config/tool error · `2` dump/export failed ·
`3` manifest verification failed (treat the run's artifacts as suspect).
Alert on any non-zero exit.

### 9.2 Restore drill (run quarterly — a backup is a rumor until restored)

1. Pick a recent artifact: `ls backups/ | tail`.
2. Restore **into staging**, never prod first:
   ```bash
   DATABASE_URL='postgresql://…staging…' \
     scripts/restore_db.sh --yes-i-know backups/atp-20260706-031700.dump
   # sqlite flavor:
   scripts/restore_db.sh --yes-i-know backups/atp-20260706-031700.sqlite3.gpg
   ```
   The script refuses to run without `--yes-i-know`, verifies the artifact
   against its `atp-<stamp>.sha256` manifest first, decrypts `.gpg`
   artifacts (private key required), and for SQLite keeps the current db at
   `<db>.pre-restore-<stamp>`.
3. Verify the tamper-evident evidence chain per org (needs the prod
   `EVIDENCE_SIGNING_KEY` in env):
   ```bash
   python3 -c "from atp import signing; import json; \
     print(json.dumps(signing.verify_chain('org-demo')))"
   ```
   Expect `{"ok": true, …}` for every org id in the `orgs` table. A fresh
   `python3 -m atp.exams <cert> --dry-run --verify-chain --org <org>` also
   re-verifies after appending one exam's evidence.
4. Boot the API against the restored DB, log in, open an agent profile with
   evidence. Note the wall-clock time — that is your real RTO.

### 9.3 Staging promote flow

`render.staging.yaml` deploys the `staging` branch as
`brain-university-api-staging` (starter plan, own Postgres/secrets); the
Netlify staging frontend is a branch deploy of the same site
(setup notes in `render.staging.yaml`'s header).

1. Merge feature work into `staging` → Render + Netlify auto-deploy.
2. Smoke on staging: `/health`; login; the 6 agent screens render;
   `python3 -m atp.exams atp-l4-math --dry-run --verify-chain` against the
   staging DB; a license issue → check → revoke round-trip.
3. Promote: `git checkout main && git merge --ff-only staging && git push`.
   `--ff-only` guarantees prod ships the exact commit staging soaked.
4. Prod auto-deploys (render.yaml `autoDeploy: true`). Re-run the smoke
   against prod. Roll back = Render dashboard → Rollback to the previous
   deploy (code) + restore latest backup (data, only if a migration went bad).

Migrations run at startup (idempotent, transactional on Postgres), so a
promote that includes a new `migrations/NNN_*.sql` applies it on first boot —
take a backup **before** promoting a migration.

### 9.4 Metrics scrape

The API exposes Prometheus-format metrics at `/metrics` (Phase 5 contract).
Scrape it directly:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: brain-university-api
    metrics_path: /metrics
    scheme: https
    static_configs:
      - targets: ["brain-university-api-XXX.onrender.com:443"]
    # If /metrics lands behind the bearer gate, mint a token via POST /login
    # and set:  authorization: { type: Bearer, credentials: "<token>" }
  - job_name: brain-university-api-staging
    metrics_path: /metrics
    scheme: https
    static_configs:
      - targets: ["brain-university-api-staging.onrender.com:443"]
```

Useful first alerts: non-2xx rate, request latency p95, 429 (rate-limit) rate,
job queue depth, and absence of the nightly backup-success log line.

### 9.5 Rate-limit tuning

In-app limiting is a token bucket keyed by **IP + auth token** (Phase 5
contract), tuned via env — knob names are documented in `.env.example` in
your checkout once the limiter lands (bucket size / refill per second).
Tuning guidance:

- Start permissive (e.g. burst 60, ~1 req/s refill) and tighten from data:
  watch the 429 count in `/metrics` and `access_log`.
- LLM-backed endpoints (`/experts/{agent_id}/chat`, exam runs) deserve much
  tighter buckets than static reads — they cost real money per call; the
  `usage_events` metering rows tell you actual per-license call rates.
- Legit bursts: the frontend fires several parallel requests on screen load;
  keep burst ≥ 20 or logins will 429 on slow connections.
- Remember Netlify/Render sit behind proxies — the limiter must read the
  client IP from `X-Forwarded-For`'s first hop, not the socket peer.
