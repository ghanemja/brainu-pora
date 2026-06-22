# Portfolio env playbook

Shared env vars to set on **every** project's HF Space so they all share the
same Gemma endpoint, the same auth tenancy, and the same secret rotation.

Each project still ships independently:
- Own GitHub repo
- Own HF Space (`https://jang0294-<project>.hf.space`)
- Own Netlify site (`https://<project>.netlify.app`)
- Own `BU_API_BASE` (points at THAT project's Space, never shared)

The vars below get copy-pasted unchanged into every Space's Settings →
Variables and secrets.

---

## 1 · Generate canonical secrets ONCE

```bash
# Run once, save to a password manager
python3 -c "import secrets; print('BU_AUTH_SECRET =', secrets.token_urlsafe(48))"
python3 -c "import secrets; print('BU_AUTH_PASSWORD =', secrets.token_urlsafe(16))"
```

Suggested values already minted for you:

```
BU_AUTH_USER     = admin
BU_AUTH_PASSWORD = MJiqvzRqd9SVfw2kmI65og
BU_AUTH_SECRET   = -qLRPjwndg7PvJFWW9a8lRDYXVkEGQkG6eqF1hyKCFyOesGCycU3s3k3jGrP24B3
BU_AUTH_TTL_HOURS = 24
```

Drop these in a password manager (1Password, Bitwarden) under "Portfolio
backend env" — that's your source of truth.

---

## 2 · Shared LLM endpoint (Gemma on HF)

Stand up the Gemma HF Inference Endpoint ONCE per
[HF_ENDPOINT_SETUP.md](HF_ENDPOINT_SETUP.md). Note the URL + token.

```
LLM_BACKEND     = local
LOCAL_LLM_BASE  = https://<your-endpoint>.endpoints.huggingface.cloud/v1
LOCAL_LLM_MODEL = tgi              # or whatever your endpoint reports
LOCAL_LLM_KEY   = hf_xxxxxxxxxxxx   # HF read token
```

Optional fallback (if endpoint asleep / over rate limit):

```
ANTHROPIC_API_KEY = sk-ant-...      # only kicks in if local LLM unreachable
```

---

## 3 · Per-project Space setup checklist

For every NEW project (brain-u, charterscope, agentsannonymous, bookshelf-portfolio, ...):

1. **Create HF Space**: `https://huggingface.co/new-space` → Docker → CPU basic free.

2. **Push the project's repo to the Space:**
   ```bash
   cd <project>
   git remote add hf https://huggingface.co/spaces/jang0294/<project>
   git push hf main
   ```

3. **Set secrets** on the Space (Settings → Variables and secrets). Paste these
   nine values — IDENTICAL across all projects:

   | Key                  | Value                                          |
   |----------------------|------------------------------------------------|
   | `BU_AUTH_USER`       | `admin`                                        |
   | `BU_AUTH_PASSWORD`   | (from password manager)                        |
   | `BU_AUTH_SECRET`     | (from password manager)                        |
   | `BU_AUTH_TTL_HOURS`  | `24`                                           |
   | `LLM_BACKEND`        | `local`                                        |
   | `LOCAL_LLM_BASE`     | (HF endpoint URL)                              |
   | `LOCAL_LLM_MODEL`    | `tgi`                                          |
   | `LOCAL_LLM_KEY`      | `hf_xxxxxxxxxxxx`                              |
   | `ANTHROPIC_API_KEY`  | (fallback, optional)                           |

4. **Set per-project secrets** (different per Space):

   | Key             | Value                                                     |
   |-----------------|-----------------------------------------------------------|
   | `CORS_ORIGINS`  | This project's Netlify URL, e.g. `https://brain-u.netlify.app` |

5. **Netlify**: Import the repo. Set ONE env var:

   | Key           | Value                                                  |
   |---------------|--------------------------------------------------------|
   | `BU_API_BASE` | `https://jang0294-<project>.hf.space` (THIS project's Space) |

6. Deploy Netlify → copy URL → paste back into the Space's `CORS_ORIGINS`.

---

## 4 · What "shared auth secret" actually buys you

| Behavior                                | Works? | How                                                  |
|-----------------------------------------|--------|------------------------------------------------------|
| Same username/password on every project | ✅     | Same `BU_AUTH_USER` + `BU_AUTH_PASSWORD` on every Space |
| One token works against ANY project's backend | ✅     | Same `BU_AUTH_SECRET` → HMAC matches everywhere       |
| Auto-login across project frontends     | ❌     | Tokens live in per-origin localStorage; user logs in per site |
| Revoke all sessions on every project    | ✅     | Rotate `BU_AUTH_SECRET` on every Space → all tokens invalidate |

**The auto-login gap** — each Netlify subdomain is a separate origin, so
localStorage doesn't share. Three ways to fix later if you care:

- **Custom domain w/ subdomains under one apex** (`jang.dev`, `brain.jang.dev`,
  `charter.jang.dev`) → set auth cookie on `.jang.dev`, all subdomains read it.
- **Shared auth UI** at one origin (`auth.jang.dev`) that mints tokens via
  `postMessage` to each project iframe. More plumbing.
- **OAuth proxy** in front of every Space (oauth2-proxy or Cloudflare Access).
  Most setup.

For the leadership demo this doesn't matter — they log in to one site, you're
done.

---

## 5 · Rotation procedure

- **Rotate password only**: change `BU_AUTH_PASSWORD` on every Space. Old tokens
  stay valid until they expire (24 h). New logins require new password.
- **Revoke all sessions immediately**: change `BU_AUTH_SECRET` on every Space.
  Every previously-minted token instantly invalidates. Everyone logs in again.
- **Rotate LLM credentials**: change `LOCAL_LLM_KEY` on every Space; no user
  impact.

For "every Space" you can either click through each one in the HF UI, or use
the HF API:

```bash
# Set the same secret across every space in one shot
for space in brain-university charterscope agentsannonymous bookshelf-portfolio; do
  huggingface-cli space secrets push jang0294/$space \
    BU_AUTH_SECRET="<new-value>"
done
```

(Requires `pip install huggingface_hub` and a write-scope HF token.)

---

## 6 · When to consolidate to umbrella

Stay with separate Spaces while:
- ≤ 5 projects
- Cold-start latency isn't a problem (Spaces stay warm if anyone uses them)
- You like the isolation (one project's deps don't break another's)

Switch to umbrella FastAPI in one Space when:
- > 5 projects
- N independent cold-starts annoy demos
- Shared rate limits / metrics become useful

The umbrella pattern is in [HF_SPACES_DEPLOY.md](HF_SPACES_DEPLOY.md) future-work
section.
