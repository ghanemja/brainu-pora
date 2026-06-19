# Local Gemma Setup (GGUF) — run the whole app on a local LLM

Brain University routes **every** generation call (lessons, quizzes, podcasts,
animations, confusion analysis, debates) through a single function,
`_call_claude` in `agents/orchestrator.py`. Point that function at a local
OpenAI-compatible server and the entire app runs on your own machine — no
Anthropic API key required.

The model used here is the fine-tuned GGUF
**`gemma-4-12B-coder-fable5-composer2.5-v1`**, published as a Hugging Face
"bucket":
<https://huggingface.co/buckets/jang0294/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF-bucket>

> An HF *bucket* is just a file store. Grab the `.gguf` with
> `huggingface-cli download` or the web UI's download button — there is no
> auto-pull from a model id like a normal repo.

A 12B model at Q4 quantization runs comfortably on an Apple M-series Mac with
**~16 GB RAM** (Q4_K_M ≈ 7–8 GB on disk, leaves room for the OS). More RAM lets
you raise the context window.

---

## Environment variables

| Variable           | Required | Example                          | Meaning                                                                 |
| ------------------ | -------- | -------------------------------- | ----------------------------------------------------------------------- |
| `LLM_BACKEND`      | no\*     | `local`                          | Force the local path. Either this **or** `LOCAL_LLM_BASE` flips the app to local. |
| `LOCAL_LLM_BASE`   | yes      | `http://localhost:11434/v1`      | Base URL of the OpenAI-compatible server, **including `/v1`**. The app POSTs to `${LOCAL_LLM_BASE}/chat/completions`. |
| `LOCAL_LLM_MODEL`  | yes      | `gemma-coder`                    | Model name the server knows it by.                                      |
| `LOCAL_LLM_KEY`    | no       | *(unset)*                        | Bearer token. Only sent if set — Ollama / llama.cpp need none.          |
| `ANTHROPIC_API_KEY`| no       | `sk-ant-...`                     | If present, used as a **fallback** when the local server is unreachable. If absent, a local failure raises a clear error. |

\* Setting either `LLM_BACKEND=local` or `LOCAL_LLM_BASE` switches the app to
local. If neither is set, the app uses the unchanged Anthropic path.

---

## Option A — Ollama (recommended)

Easiest path: Ollama manages the model, exposes an OpenAI-compatible API at
`:11434/v1`, and stays running in the background.

1. **Install Ollama** — <https://ollama.com/download> (or `brew install ollama`),
   then start it (`ollama serve`, or just launch the app).

2. **Download the GGUF** from the HF bucket:

   ```bash
   pip install -U "huggingface_hub[cli]"
   huggingface-cli download \
     buckets/jang0294/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF-bucket \
     --include "*Q4_K_M.gguf" \
     --local-dir ./gemma-gguf
   # (or grab the .gguf from the bucket's web UI and drop it in ./gemma-gguf)
   ```

3. **Write a `Modelfile`** next to the downloaded `model.gguf`:

   ```Dockerfile
   FROM ./gemma-gguf/gemma-4-12B-coder-fable5-composer2.5-v1.Q4_K_M.gguf

   # Gemma chat template
   TEMPLATE """{{ if .System }}<start_of_turn>user
   {{ .System }}

   {{ .Prompt }}<end_of_turn>
   {{ else }}<start_of_turn>user
   {{ .Prompt }}<end_of_turn>
   {{ end }}<start_of_turn>model
   {{ .Response }}<end_of_turn>
   """

   PARAMETER stop "<end_of_turn>"
   PARAMETER temperature 0.3
   PARAMETER num_ctx 8192
   ```

4. **Register the model:**

   ```bash
   ollama create gemma-coder -f Modelfile
   ```

5. **Configure the app:**

   ```bash
   export LLM_BACKEND=local
   export LOCAL_LLM_BASE=http://localhost:11434/v1
   export LOCAL_LLM_MODEL=gemma-coder
   ```

That's it — every generation now runs on the local Gemma.

---

## Option B — llama-cpp-python server

A lightweight pure-Python OpenAI-compatible server. Good when you already have
the `.gguf` and don't want Ollama.

```bash
pip install 'llama-cpp-python[server]'

python -m llama_cpp.server \
  --model ./gemma-gguf/gemma-4-12B-coder-fable5-composer2.5-v1.Q4_K_M.gguf \
  --port 8000 \
  --n_ctx 8192
```

On Apple Silicon, install with Metal acceleration for speed:

```bash
CMAKE_ARGS="-DGGML_METAL=on" pip install --force-reinstall --no-cache-dir 'llama-cpp-python[server]'
```

Configure the app (the server reports the model under the basename, but any
string works — it serves the single loaded model):

```bash
export LLM_BACKEND=local
export LOCAL_LLM_BASE=http://localhost:8000/v1
export LOCAL_LLM_MODEL=gemma
```

---

## Option C — llama.cpp `llama-server` binary

The native C++ server from the llama.cpp project. Fastest, no Python runtime.

```bash
# Build llama.cpp (Metal is on by default on macOS)
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp && cmake -B build && cmake --build build --config Release -j

# Serve the GGUF with the OpenAI-compatible API
./build/bin/llama-server \
  -m /path/to/gemma-4-12B-coder-fable5-composer2.5-v1.Q4_K_M.gguf \
  --port 8080 \
  -c 8192
```

`llama-server` exposes `/v1/chat/completions`, so set the base to include `/v1`:

```bash
export LLM_BACKEND=local
export LOCAL_LLM_BASE=http://localhost:8080/v1
export LOCAL_LLM_MODEL=gemma
```

---

## Smoke test

Hit the endpoint directly to confirm the server is up before running the app
(swap the host/port for whichever option you picked):

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-coder",
    "messages": [
      {"role": "system", "content": "You are a concise tutor."},
      {"role": "user", "content": "In one sentence, what is backpropagation?"}
    ],
    "max_tokens": 128,
    "temperature": 0.3
  }'
```

A healthy response contains `choices[0].message.content`. If `LOCAL_LLM_KEY` is
set on your server, add `-H "Authorization: Bearer $LOCAL_LLM_KEY"`.

Then run any generation flow in the app — it now goes to local Gemma. If
`ANTHROPIC_API_KEY` is also set, the app falls back to Claude automatically when
the local server is down.

---

## How the routing works

- `agents/orchestrator.py` → `_call_local_llm(system, user, max_tokens)` POSTs
  to `${LOCAL_LLM_BASE}/chat/completions` and parses
  `choices[0].message.content`. `_call_claude` calls it first whenever local is
  configured, then falls back to Anthropic (or raises) on failure.
- `agents/backend.py` → `LocalOpenAIBackend` mirrors the same call for the
  `Backend` abstraction. Use the resolver spec `local:<base_url>` (e.g.
  `local:http://localhost:11434/v1`) in a Specialist's `base_model` to route a
  single agent through it.
