#!/usr/bin/env python3
"""
Deploy the Brain University backend to a (public) Hugging Face Space.

You run this yourself (your HF token is on your machine). It:
  1. creates the Space  jang0294/brain-university-api  (Docker SDK, public)
  2. uploads the backend code + Dockerfile + the corpus seed
  3. prints the Space URL + the API base URL to wire into the frontend

Run from the repo root:
    python3 scripts/deploy_hf_space.py

Requires:  pip install huggingface_hub   (and a logged-in HF token)
If it complains about an invalid token, run:  huggingface-cli login
"""

from __future__ import annotations

import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_ID = "jang0294/brain-university-api"
API_BASE = "https://jang0294-brain-university-api.hf.space"

SPACE_README = """---
title: Brain University API
emoji: 🧠
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
short_description: FastAPI backend for Brain University
---

# Brain University — backend API

FastAPI service: knowledge-graph lessons, two-host paper podcasts, animated
explainers, multi-agent debate. The Netlify frontend calls this API.

Set `ANTHROPIC_API_KEY` under Settings → Secrets for rich LLM generation, or
the `LOCAL_LLM_*` vars to point at a local/HF Gemma endpoint.
"""


def _token() -> str | None:
    # Prefer the cached login token; the HF_TOKEN env var may be stale.
    cache = Path.home() / ".cache" / "huggingface" / "token"
    if cache.exists():
        t = cache.read_text().strip()
        if t:
            return t
    return os.environ.get("HF_TOKEN")


def main() -> int:
    try:
        from huggingface_hub import HfApi, create_repo
    except ImportError:
        print("Install first:  pip install huggingface_hub", file=sys.stderr)
        return 1

    token = _token()
    api = HfApi(token=token)

    try:
        who = api.whoami()
        print(f"Authenticated as: {who.get('name')}")
    except Exception as e:  # noqa: BLE001
        print(f"HF auth failed ({e}). Run:  huggingface-cli login", file=sys.stderr)
        return 1

    url = create_repo(REPO_ID, repo_type="space", space_sdk="docker",
                      exist_ok=True, token=token)
    print(f"Space: {url}")

    # write the Space README (frontmatter tells HF to build as Docker)
    readme = REPO_ROOT / ".space_readme.md"
    readme.write_text(SPACE_README)

    for d in ["agents", "api", "graph", "rag", "eval", "scripts", "wiki"]:
        api.upload_folder(folder_path=str(REPO_ROOT / d), path_in_repo=d,
                          repo_id=REPO_ID, repo_type="space",
                          ignore_patterns=["__pycache__/*", "*.pyc"], token=token)
        print(f"  uploaded {d}/")

    for f in ["Dockerfile", "requirements.txt"]:
        api.upload_file(path_or_fileobj=str(REPO_ROOT / f), path_in_repo=f,
                        repo_id=REPO_ID, repo_type="space", token=token)
    api.upload_file(path_or_fileobj=str(REPO_ROOT / "data" / "defense_corpus_samples.json"),
                    path_in_repo="data/defense_corpus_samples.json",
                    repo_id=REPO_ID, repo_type="space", token=token)
    api.upload_file(path_or_fileobj=str(readme), path_in_repo="README.md",
                    repo_id=REPO_ID, repo_type="space", token=token)
    readme.unlink(missing_ok=True)

    print("\nDONE — the Space is now building (~5-10 min).")
    print(f"  Watch build: https://huggingface.co/spaces/{REPO_ID}")
    print(f"  API base:    {API_BASE}")
    print("\nNext:")
    print(f"  1. {url} → Settings → Secrets → add ANTHROPIC_API_KEY")
    print(f"  2. Tell Claude the API base ({API_BASE}) to wire the frontend.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
