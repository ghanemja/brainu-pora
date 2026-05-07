"""
Lightweight retrieval-time weight store.

Lives alongside the BM25 indices so Specialist.retrieve can apply a learned
prior at query time without hitting FalkorDB. Three keyspaces:

  paper_id       (e.g. "2603.21148")        # arXiv prior
  wiki_slug      (e.g. "Reynolds_number")   # wiki page prior
  defense_id     (e.g. "AD1099286")         # defense corpus prior

All keys default to 1.0. Bumps are additive; weight floors at 0.05 to
prevent extinction. A separate JSON file keeps it trivially mergeable
across processes (retrieval reads, feedback writes — last-writer-wins
is fine for thumbs scale).

API:
  get(kind, key, default=1.0)         → float
  bump(kind, key, delta)              → new weight, persisted
  get_paper_weight(paper_id)          → shortcut
  get_wiki_weight(slug)               → shortcut
  load_all() / dump_all()             → maintenance
  apply_score_prior(chunks, alpha)    → reweight a list of chunks in place
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
WEIGHTS_PATH = PROJECT_ROOT / "data" / "sessions" / "retrieval_weights.json"
WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)

WEIGHT_FLOOR = float(os.environ.get("RL_WEIGHT_FLOOR", 0.05))
WEIGHT_CEIL  = float(os.environ.get("RL_WEIGHT_CEIL", 5.0))

_lock = threading.RLock()
_cache: dict[str, dict[str, float]] | None = None


def _load() -> dict[str, dict[str, float]]:
    global _cache
    if _cache is not None:
        return _cache
    with _lock:
        if _cache is None:
            if WEIGHTS_PATH.exists():
                try:
                    _cache = json.loads(WEIGHTS_PATH.read_text())
                except json.JSONDecodeError:
                    _cache = {}
            else:
                _cache = {}
            for k in ("paper", "wiki", "defense"):
                _cache.setdefault(k, {})
    return _cache


def _save() -> None:
    with _lock:
        WEIGHTS_PATH.write_text(json.dumps(_cache, indent=2, default=str))


# ── Public ─────────────────────────────────────────────────────────────────

def get(kind: str, key: str, default: float = 1.0) -> float:
    return float(_load().get(kind, {}).get(key, default))


def bump(kind: str, key: str, delta: float) -> float:
    """Apply additive delta. Floored / ceiled. Returns new weight."""
    if not key:
        return 1.0
    with _lock:
        store = _load().setdefault(kind, {})
        old = float(store.get(key, 1.0))
        new = max(WEIGHT_FLOOR, min(WEIGHT_CEIL, old + float(delta)))
        store[key] = new
        _save()
        return new


def decay_all(rate: float = 0.99) -> int:
    """Multiply every weight by `rate`. Returns count of weights decayed."""
    n = 0
    with _lock:
        c = _load()
        for kind in c:
            for k, v in list(c[kind].items()):
                v_new = max(WEIGHT_FLOOR, v * rate)
                c[kind][k] = v_new
                n += 1
        _save()
    return n


def reset() -> None:
    """Drop every learned weight. Used by eval harness for clean baselines."""
    global _cache
    with _lock:
        _cache = {"paper": {}, "wiki": {}, "defense": {}}
        _save()


def snapshot() -> dict:
    """Compact view for UI/debug."""
    c = _load()
    return {
        "paper":   dict(sorted(c.get("paper", {}).items(),
                                key=lambda kv: kv[1], reverse=True)[:50]),
        "wiki":    dict(sorted(c.get("wiki", {}).items(),
                                key=lambda kv: kv[1], reverse=True)[:50]),
        "defense": dict(sorted(c.get("defense", {}).items(),
                                key=lambda kv: kv[1], reverse=True)[:50]),
        "totals":  {kind: len(c.get(kind, {})) for kind in ("paper", "wiki", "defense")},
    }


# ── Apply prior to BM25 retrieval ─────────────────────────────────────────

def apply_score_prior(chunks: list[dict], alpha: float = 0.5) -> list[dict]:
    """Re-rank a chunk list by mixing BM25 score with learned weight.

    new_score = bm25_score * (1 + alpha * (weight - 1))

    alpha = 0.0 → no effect (pure BM25)
    alpha = 1.0 → weight fully scales score
    Default 0.5 is a soft prior — RL nudges, doesn't dictate.

    Sort by new_score and return. Mutates each chunk to add `_prior_score`
    and `_weight` for inspection.
    """
    out = []
    for c in chunks:
        # Pick weight kind from chunk's source field
        w = _weight_for_chunk(c)
        bm25 = float(c.get("_score", 0.0))
        prior_score = bm25 * (1 + alpha * (w - 1))
        c2 = dict(c)
        c2["_weight"] = w
        c2["_prior_score"] = prior_score
        c2["_score"] = prior_score   # downstream code keys off _score
        out.append(c2)
    out.sort(key=lambda x: x.get("_prior_score", 0), reverse=True)
    return out


def _weight_for_chunk(chunk: dict) -> float:
    """Look up weight for a single chunk based on its source kind."""
    source = chunk.get("source", "") or ""
    paper_id = chunk.get("paper_id", "") or ""

    # Defense-corpus chunk (built by retrieval_inspector's defense BM25)
    if source.startswith("dtic/") or source.startswith("ntrs/") \
       or source.startswith("openalex/") or source.startswith("arxiv/"):
        # Try to parse defense id (e.g. "dtic/AD1099286") or paper id
        kind, _, key = source.partition("/")
        if kind == "dtic" or kind == "ntrs" or kind == "openalex":
            return get("defense", key, 1.0)
        # arxiv/<cat>/<paper>... → use paper_id field
        if paper_id:
            return get("paper", paper_id, 1.0)

    # Specialist BM25 chunks: source = "data/raw/arxiv/<cat>/<id>.txt" or
    # "arxiv/<cat>/<id>.txt#<chunk>". paper_id is the cleanest key.
    if paper_id:
        return get("paper", paper_id, 1.0)

    # Fallback: filename stem
    stem = source.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    if stem:
        return get("paper", stem, 1.0)
    return 1.0
