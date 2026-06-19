"""
Code-from-paper extractor.

Given paper text (or a specific section), Claude returns:
  - runnable Python implementation of the algorithm
  - a small set of inline pytest-style assertions
  - one-paragraph commentary on what each part does
  - a tiny demo invocation

Output is fed to a Pyodide iframe sandbox in the frontend — reader runs +
modifies in-browser, no server eval.

Cached: data/sessions/code_cache/<hash>.json
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "sessions" / "code_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


SYSTEM = """You are a research-engineer translator. Given a passage from a
paper that describes an algorithm (or a clearly named technique), return:

  1. A pure-Python implementation, no external deps beyond the std lib +
     numpy (assume numpy is available; do NOT import torch / sklearn / etc).
     Code MUST run in CPython 3.10 under Pyodide. Keep it under 80 lines.
  2. 3-5 inline assertions (use `assert`) that demonstrate the algorithm
     produces the expected output on a small example.
  3. A 1-paragraph explanation, mapping each function back to the paper.
  4. One demo invocation that prints something interpretable.

Rules:
- No file I/O, no network, no subprocess, no input().
- Use numpy if helpful, otherwise pure stdlib.
- Names must match the paper's notation when reasonable (e.g. `pi`, `A`, `T`).
- If the paper passage is not algorithmic (e.g. theory only), output
  {"runnable": false, "reason": "..."}.

OUTPUT: valid JSON only, no preface, no fence:
{
  "runnable":   true,
  "language":   "python",
  "code":       "<python source>",
  "explanation":"<one paragraph>",
  "demo":       "<demo invocation line(s)>",
  "imports":    ["numpy", ...]
}"""


def extract(passage: str, force: bool = False) -> dict | None:
    """Turn a paper passage into runnable Python."""
    if not passage or not passage.strip():
        return None
    key = hashlib.sha1(passage.encode()).hexdigest()[:16]
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists() and not force:
        try:
            return json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            pass

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=SYSTEM,
            user=f"PAPER PASSAGE:\n\n{passage[:8000]}",
            max_tokens=2500,
            retries=2,
        )
    except Exception:
        return None

    parsed = _parse_json(raw)
    if not parsed:
        return None
    cache_file.write_text(json.dumps(parsed, indent=2))
    return parsed


def _parse_json(raw: str) -> dict | None:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
