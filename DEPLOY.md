# Deploy Brain University (public)

Three pieces, deployed independently, connected by two env vars.

```
┌──────────────┐  HTTPS   ┌─────────────────────┐  HTTPS   ┌──────────────────┐
│ Netlify      │ ───────► │ Render              │ ───────► │ LLM              │
│ design/ (UI) │  CORS    │ api/ (FastAPI+ffmpeg)│         │ Claude API  OR   │
│ free         │          │ ~$25/mo standard    │          │ HF Gemma endpoint│
└──────────────┘          └─────────────────────┘          └──────────────────┘
       BU_API_BASE ─────────────┘        ANTHROPIC_API_KEY ──┘
                                         or LOCAL_LLM_* (see HF_ENDPOINT_SETUP.md)
```

---

## 1. Backend → Render (Docker)

1. Push this repo to GitHub.
2. <https://render.com> → **New → Blueprint** → pick the repo. It reads
   `render.yaml` (Docker web service + 5 GB disk at `/data`).
3. In the service **Environment**, set secrets:
   - `ANTHROPIC_API_KEY` = `sk-ant-...`  (Path A — ship on Claude)
   - `CORS_ORIGINS` = your Netlify URL once you have it (step 2)
   - *(Path B — hosted Gemma later: set `LLM_BACKEND=local` + the three
     `LOCAL_LLM_*` vars per [HF_ENDPOINT_SETUP.md](HF_ENDPOINT_SETUP.md). No
     code change, just env + restart.)*
4. Deploy → copy the URL, e.g. `https://brain-university-api.onrender.com`.
5. Verify:
   ```bash
   curl https://brain-university-api.onrender.com/health      # {"ok": true}
   curl https://brain-university-api.onrender.com/papers | head
   ```

> **Why `plan: standard` not `starter`** — podcast/video render (moviepy +
> ffmpeg + TTS) and graph build are RAM-hungry; the 512 MB starter plan OOMs.
> For many concurrent users, move rendering to a background worker + queue
> later; synchronous is fine for a demo.

### Alt hosts
- **Railway** — `railway.json`/`Procfile` also present; same flow.
- **Fly.io** — `fly launch` reads the `Dockerfile`; has GPU machines if you
  later want Gemma on the same platform.

---

## 2. Point the frontend at the backend

Edit one line in [design/Brain University.html](design/Brain%20University.html):

```diff
- window.BU_API_BASE = "http://localhost:8080";
+ window.BU_API_BASE = "https://brain-university-api.onrender.com";
```

Commit. (For multi-env, inject it at build time instead of hardcoding.)

---

## 3. Frontend → Netlify

```bash
npm i -g netlify-cli
netlify deploy --dir=design --prod
```
or dashboard → Import from Git (reads `netlify.toml`). Copy the resulting
`https://<site>.netlify.app` and set it as `CORS_ORIGINS` on Render (step 1.3),
then redeploy the backend.

---

## 4. LLM: Path A now, Path B later

| | Path A — Claude | Path B — Hosted Gemma |
|---|---|---|
| Setup | set `ANTHROPIC_API_KEY` | HF Inference Endpoint, set `LOCAL_LLM_*` |
| Ships | today | after model→repo + endpoint |
| Cost | per token | ~$0.80/GPU-hr active, $0 idle |
| Switch | — | env change only, no redeploy of code |

Full Gemma-on-HF guide: [HF_ENDPOINT_SETUP.md](HF_ENDPOINT_SETUP.md).
Local Gemma (dev): [GEMMA_SETUP.md](GEMMA_SETUP.md).

---

## 5. Pre-launch checklist

- [ ] `BU_API_BASE` in the HTML points at Render, not localhost
- [ ] `CORS_ORIGINS` on Render = the Netlify origin (not `*`)
- [ ] `ANTHROPIC_API_KEY` (or `LOCAL_LLM_*`) set on Render as a secret
- [ ] `.env` and `data/*.db` are gitignored (they are)
- [ ] Render disk mounted at `/data` so SQLite + media survive redeploys
- [ ] At least one paper ingested so the Papers/Podcast tabs aren't empty
- [ ] Auth gate: the HTML has a demo username/password gate — change the
      `admin`/`password` default before sharing publicly

---

## 6. Cost ballpark (demo + small beta)

| Service | Note | ~Cost |
|---------|------|-------|
| Netlify | static, free tier | $0 |
| Render standard | always-on backend | ~$25/mo |
| Claude API | per token | usage |
| HF Gemma endpoint (optional) | scale-to-zero GPU | ~$0 idle |

≈ **$25-50/mo** all-in for a funder demo + early users on Claude. Swap to the
HF Gemma endpoint when the token bill starts to matter.
