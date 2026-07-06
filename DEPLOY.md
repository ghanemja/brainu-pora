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
