# HF Spaces deploy — free backend, ~$0/mo idle

The Brain University backend (FastAPI + ffmpeg + graph build) runs as a
Docker container on a Hugging Face Space. Pair with Netlify for the static
frontend + an HF Inference Endpoint for Gemma — total bill at idle: **$0**.

```
┌──────────────┐   HTTPS    ┌──────────────────────┐   HTTPS    ┌──────────────────┐
│ Netlify      │ ─────────► │ HF Space (Docker)    │ ─────────► │ HF Inference EP  │
│ design/ UI   │   CORS     │ api/ FastAPI+ffmpeg  │            │ Gemma, scale-to-0│
│ free         │            │ free, sleeps 48h idle│            │ ~$0 idle         │
└──────────────┘            └──────────────────────┘            └──────────────────┘
       BU_API_BASE  ────────────┘    LOCAL_LLM_BASE  ─────────────┘
```

---

## 1 · Create the Space

1. **https://huggingface.co/new-space**
   - Owner: `jang0294` (or your HF username)
   - Space name: `brain-university` (becomes `https://huggingface.co/spaces/jang0294/brain-university`)
   - License: pick one (MIT or Apache 2.0)
   - SDK: **Docker** → **Blank**
   - Hardware: **CPU basic (free)**. Upgrade to **CPU upgrade** ($0.03/hr) only if `/paper/video/render` is too slow.
   - Visibility: **Public** (free private Spaces have stricter limits).

2. Add a remote and push:
   ```bash
   git remote add hf https://huggingface.co/spaces/jang0294/brain-university
   # First push will prompt for HF token (Settings → Access Tokens, write scope)
   git push hf main
   ```
   The Space starts building immediately. Logs at the Space page → "App" tab. First build ~5–8 min (Docker layer + pip + ffmpeg + corpus copy).

3. The Space serves at `https://jang0294-brain-university.hf.space`. Verify:
   ```bash
   curl https://jang0294-brain-university.hf.space/health
   # → {"ok": true}
   ```

> **Why this works out of the box:** README.md already has the HF Spaces YAML
> frontmatter (sdk: docker, app_port: 7860) and the Dockerfile already
> respects $PORT (HF injects 7860). No code edits needed.

---

## 2 · Set secrets on the Space

Space page → **Settings → Variables and secrets** → **New secret**. Add:

| Key                | Value                                                |
|--------------------|------------------------------------------------------|
| `ANTHROPIC_API_KEY`| your Anthropic key (Path A, ship today)              |
| `CORS_ORIGINS`     | `https://<your-site>.netlify.app` (fill after step 3) |
| `BU_AUTH_USER`     | `<REDACTED — set via env, rotation handled out-of-band>` |
| `BU_AUTH_PASSWORD` | `<REDACTED — set via env, rotation handled out-of-band>` |
| `BU_AUTH_SECRET`   | `<REDACTED — set via env, rotation handled out-of-band>` |
| `BU_AUTH_TTL_HOURS`| `24`                                                 |

The Space restarts automatically on secret change.

> **Do not** set `BU_AUTH_DISABLED`. That's a local-only escape hatch.

---

## 3 · Frontend → Netlify

Same as Render path:

1. https://app.netlify.com → Add new site → Import from Git → pick repo.
2. Site settings → Environment variables → `BU_API_BASE = https://jang0294-brain-university.hf.space` (no trailing slash).
3. Deploys → Trigger deploy → Clear cache and deploy.
4. Back to HF Space secrets → set `CORS_ORIGINS` to the exact Netlify URL.
   Space restarts.

---

## 4 · (Optional) Swap Claude → Gemma on HF

If you've stood up a Gemma HF Inference Endpoint per
[HF_ENDPOINT_SETUP.md](HF_ENDPOINT_SETUP.md), add these secrets to the Space:

| Key               | Value                                                       |
|-------------------|-------------------------------------------------------------|
| `LLM_BACKEND`     | `local`                                                     |
| `LOCAL_LLM_BASE`  | `https://<endpoint>.endpoints.huggingface.cloud/v1`         |
| `LOCAL_LLM_MODEL` | `tgi` (or whatever your endpoint reports)                   |
| `LOCAL_LLM_KEY`   | `hf_xxxxxxxx` (HF token w/ read scope)                       |

`ANTHROPIC_API_KEY` is ignored once `LLM_BACKEND=local`. Space restarts.

---

## 5 · Caveats vs. Render

| Trade-off                                  | HF Spaces (free)                | Render standard ($25/mo)   |
|--------------------------------------------|---------------------------------|----------------------------|
| Cost                                       | $0                              | ~$25/mo                    |
| Sleep after inactivity                     | **Yes** — ~48h idle, then cold-starts in ~30–90s | No                         |
| Persistent disk (corpus survives restart)  | **No** on free tier — repo-baked corpus reloads but new ingests die | Yes (5GB at `/data`)       |
| RAM                                        | 16GB free CPU basic             | 2GB standard               |
| Container restart on push                  | Yes                             | Yes                        |
| HTTPS + custom domain                      | Yes                             | Yes                        |
| Logs visible in dashboard                  | Yes                             | Yes                        |

**For a leadership demo**: the sleep + no-persistence trade-offs don't matter.
The ingest cascade still works (paper added to in-memory corpus, video
rendered to ephemeral `/app/design/videos`), it just won't survive a Space
restart. Pre-warm the Space by hitting `/health` 30 s before the meeting and
the demo will be instant.

---

## 6 · Hand to leadership

> **URL**: https://brain-u.netlify.app
> **Username**: <REDACTED — set via env, rotation handled out-of-band>
> **Password**: <REDACTED — set via env, rotation handled out-of-band>

Tutorial auto-opens on first visit. `?` reopens.

---

## 7 · Troubleshooting

| Symptom | Fix |
|---------|-----|
| HF Space stuck on "Building" >15 min | Check Build logs; usually pip dep timeout — retry the push |
| `/health` works but app calls 401 from Netlify | `CORS_ORIGINS` doesn't include the Netlify URL exactly |
| `Generate 30s explainer` fails on the Space | CPU basic may OOM on a heavy paper; upgrade to CPU upgrade ($0.03/hr) |
| First load takes 60 s | Space was asleep — first request wakes it. Pre-warm before demos |
| `git push hf main` rejected | Token lacks write scope. HF → Settings → Access Tokens → new token (write) |
| Container restarts every push | Expected. Pre-warm again. |

---

## 8 · Pre-launch checklist

- [ ] HF Space exists, `/health` returns `{ok:true}`
- [ ] All 6 auth env vars set as Space secrets
- [ ] `CORS_ORIGINS` on Space = exact Netlify URL
- [ ] `BU_API_BASE` on Netlify = Space URL (no trailing slash)
- [ ] `BU_AUTH_DISABLED` UNSET on Space
- [ ] Tutorial opens on Netlify URL after login
- [ ] One pre-warmed paper plays its video without on-demand wait
