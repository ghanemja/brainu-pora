#!/usr/bin/env python3
"""
Provision a GPU Inference Endpoint serving the Gemma-4-12B coder GGUF, then
print the URL to wire into Brain University.

You run this (it spends real money on a GPU — ~$0.80/hr ACTIVE, $0 idle via
scale-to-zero). Your forked bucket is empty, so this deploys the public mirror
of the SAME model (gemma-4-12B-coder-fable5-composer2.5-v1), Q4_K_M quant.

    python3 scripts/deploy_gemma_endpoint.py

Requires a logged-in HF token with billing enabled (you already have endpoints,
so it is). A *failed* endpoint does not bill — only a running one does.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# The public mirror of your model + the exact verified GGUF filename.
REPO = "yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF"
GGUF = "gemma4-coding-Q4_K_M.gguf"          # 7.4 GB — fits L4, fast
NAME = "gemma-coder-12b"


def _token() -> str:
    cache = Path.home() / ".cache" / "huggingface" / "token"
    return cache.read_text().strip() if cache.exists() else ""


def main() -> int:
    from huggingface_hub import create_inference_endpoint, get_inference_endpoint
    tok = _token()
    if not tok:
        print("No HF token. Run: huggingface-cli login", file=sys.stderr)
        return 1

    # If a (likely failed) endpoint with this name exists, delete it so we can
    # recreate with the corrected config. Deleting is free.
    try:
        old = get_inference_endpoint(NAME, token=tok)
        print(f"Existing '{NAME}' (status {old.status}) — deleting to recreate…")
        old.delete()
    except Exception:
        pass

    # llama.cpp downloads the GGUF itself from HF at boot (--hf-repo/--hf-file).
    # This avoids relying on HF mounting the repo into the custom container,
    # which it does NOT do — that was the "No such file" failure.
    ep = create_inference_endpoint(
        name=NAME,
        repository=REPO,
        framework="pytorch",
        task="text-generation",
        accelerator="gpu",
        vendor="aws", region="us-east-1",
        instance_type="nvidia-l4", instance_size="x1",
        min_replica=0, max_replica=1, scale_to_zero_timeout=900,
        type="protected",                  # callers send your HF token as bearer
        custom_image={
            "url": "ghcr.io/ggml-org/llama.cpp:server-cuda",
            "health_route": "/health",
            "port": 8080,
        },
        env={
            "LLAMA_ARG_HF_REPO": REPO,
            "LLAMA_ARG_HF_FILE": GGUF,
            "LLAMA_ARG_HOST": "0.0.0.0",
            "LLAMA_ARG_PORT": "8080",
            "LLAMA_ARG_N_GPU_LAYERS": "99",
            "LLAMA_ARG_CTX_SIZE": "8192",
        },
        secrets={"HF_TOKEN": tok},          # for the model download
        token=tok,
    )
    print(f"CREATED '{ep.name}' — status: {ep.status} (building ~5-10 min)")
    print(f"URL: {ep.url}")
    print("\nNext: tell Claude the URL, or run with --wait to block until ready.")
    print("Watch: https://ui.endpoints.huggingface.co/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
