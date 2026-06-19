# Hosting Gemma on Hugging Face Inference Endpoints

Serve your fine-tuned Gemma on an HF dedicated GPU endpoint and point Brain
University at it. **No code change** — the backend already routes to any
OpenAI-compatible `/v1/chat/completions` endpoint with a bearer token.

```
Netlify (frontend) ──► Render (FastAPI) ──► HF Inference Endpoint (Gemma, GPU)
                                            LOCAL_LLM_BASE + LOCAL_LLM_KEY
```

---

## Important: bucket vs repo, GGUF vs safetensors

Your model is in an HF **bucket**
(`huggingface.co/buckets/jang0294/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF-bucket`)
as **GGUF**. Two adjustments before it can be served on a GPU endpoint:

1. **Endpoints deploy from a model *repo*, not a bucket.** Buckets are object
   storage; the Endpoints UI lists model repos. Put the weights in a normal
   model repo (or use a custom container that downloads from the bucket URL).
2. **GGUF is the llama.cpp/Mac format.** HF's default servers (TGI, vLLM) want
   **safetensors**. Pick ONE route below.

---

## Route A — safetensors + TGI  (recommended, least friction)

GPU servers love safetensors. If you still have the LoRA-merged model (the
weights you quantized *from*), this is the clean path.

1. Push safetensors to a model repo:
   ```bash
   huggingface-cli upload jang0294/gemma-4-12B-coder-fable5-composer2.5-v1 \
     ./merged-safetensors-dir
   ```
2. HF → **Inference Endpoints** → **New** → pick that repo.
3. Container: **Text Generation Inference (TGI)** (auto-selected for causal LMs).
4. Hardware: **1× L4 24GB** (fits a 12B at bf16/awq) or A10G. Region near you.
5. **Automatic scale-to-zero: 15 min** (so you only pay when used).
6. Create → wait for "Running" → copy the endpoint URL.
7. TGI exposes an OpenAI-compatible Messages API at `<url>/v1/chat/completions`.

Wire Brain University:
```bash
export LLM_BACKEND=local
export LOCAL_LLM_BASE=https://<your-endpoint>.endpoints.huggingface.cloud/v1
export LOCAL_LLM_MODEL=tgi          # TGI ignores the name; any value works
export LOCAL_LLM_KEY=hf_xxxxxxxx    # your HF access token (read scope)
```

---

## Route B — keep GGUF + llama.cpp custom container

If you only have the GGUF, serve it with a llama.cpp container.

1. Make the `.gguf` reachable by a repo (push it to a model repo, or keep the
   bucket and have the container download it at boot).
2. HF → Inference Endpoints → New → **Custom container**.
3. Image: a llama.cpp server image exposing the OpenAI API, e.g.
   `ghcr.io/ggerganov/llama.cpp:server-cuda` (or build your own).
4. Container command (adjust the model path / download step):
   ```
   --model /repository/<model>.gguf --host 0.0.0.0 --port 80 \
   --n-gpu-layers 999 --ctx-size 8192 --chat-template gemma
   ```
   llama-server exposes `/v1/chat/completions` (OpenAI-compatible).
5. Hardware: L4 24GB. Scale-to-zero 15 min.
6. Copy the URL.

Wire it (same as Route A):
```bash
export LLM_BACKEND=local
export LOCAL_LLM_BASE=https://<your-endpoint>.endpoints.huggingface.cloud/v1
export LOCAL_LLM_MODEL=gemma
export LOCAL_LLM_KEY=hf_xxxxxxxx
```

---

## Smoke test the endpoint

```bash
curl $LOCAL_LLM_BASE/chat/completions \
  -H "Authorization: Bearer $LOCAL_LLM_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"'"$LOCAL_LLM_MODEL"'","messages":[{"role":"user","content":"Say hi in 3 words."}],"max_tokens":20}'
```
Expect a JSON body with `choices[0].message.content`. If that works, Brain
University works — it hits the exact same route.

---

## How it plugs into the app (already wired)

- `agents/orchestrator.py` `_call_claude` → tries `_call_local_llm` first when
  `LLM_BACKEND=local` / `LOCAL_LLM_BASE` set. Covers lessons, quizzes,
  podcasts, animations.
- `agents/backend.py` `get_backend` → routes the multi-agent **debate**
  specialists to the same endpoint when `LLM_BACKEND=local`.
- Falls back to Anthropic **only** if the endpoint fails *and* `ANTHROPIC_API_KEY`
  is set; otherwise raises a clear error naming the env vars.

Set the four `LOCAL_LLM_*` / `LLM_BACKEND` vars in your **Render** service
(Environment tab) the same way you'd set them locally.

---

## Cost

| Item | Idle | Active |
|------|------|--------|
| HF Endpoint, 1× L4 24GB, scale-to-zero | **$0** | ~$0.80/hr |
| First request after idle | — | ~20-40s cold start (model load) |

For a demo or early users, scale-to-zero keeps this near-free between sessions.
The cold start is the tradeoff; keep one warm instance (disable scale-to-zero)
if you need instant responses during a live pitch.

---

## When NOT to bother

If you just want it live fast and don't care about per-token cost yet, skip all
of this: set `ANTHROPIC_API_KEY` on Render, leave `LLM_BACKEND` unset, ship on
Claude. Flip to the HF endpoint later by setting the four vars — no redeploy of
code, just an env change + restart.
```
