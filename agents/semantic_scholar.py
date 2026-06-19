"""
Semantic Scholar Graph API client.

Free, no key required (with stricter rate limits). Optional SEMANTIC_SCHOLAR_API_KEY
env var lifts the limit. Returns SPECTER2 embeddings, TLDR summaries, citation
counts, and reference lists keyed by arXiv id.

API docs: https://api.semanticscholar.org/graph/v1

Public methods:
  enrich(arxiv_id) -> dict | None
      One-shot: title, abstract, tldr, embedding (768-d SPECTER2),
      citationCount, influentialCitationCount, year, venue, refs.

  citations(arxiv_id, limit=20) -> list[dict]
      Forward citations — who cites this paper.

  references(arxiv_id, limit=20) -> list[dict]
      Backward citations — what this paper cites.

  recommend(arxiv_id, limit=10) -> list[dict]
      Semantic-Scholar-recommended related papers.

  cosine(a, b) -> float
      Plain cosine between two embedding vectors.

All public funcs catch network/parse errors and return None / []. Caller
is expected to fall back to keyword-based logic when this returns nothing.
"""

from __future__ import annotations

import os
import time
from typing import Iterable

BASE = "https://api.semanticscholar.org/graph/v1"
DEFAULT_FIELDS = (
    "title,abstract,tldr,embedding.specter_v2,year,venue,"
    "citationCount,influentialCitationCount,references.externalIds,"
    "openAccessPdf,fieldsOfStudy"
)
_LAST_CALL = 0.0
_MIN_INTERVAL = 1.05  # 1 req/sec free tier; tiny pad

def _headers() -> dict:
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    return {"x-api-key": key} if key else {}


def _throttle():
    global _LAST_CALL
    elapsed = time.monotonic() - _LAST_CALL
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _LAST_CALL = time.monotonic()


def _get(path: str, params: dict | None = None, max_retries: int = 3) -> dict | None:
    """GET w/ exponential backoff on 429. Returns None on hard failure."""
    try:
        import requests
    except ImportError:
        return None
    backoff = 2.0
    for attempt in range(max_retries):
        _throttle()
        try:
            r = requests.get(f"{BASE}{path}", params=params, headers=_headers(), timeout=20)
        except Exception:
            return None
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                return None
        if r.status_code == 429 and attempt < max_retries - 1:
            time.sleep(backoff)
            backoff *= 2
            continue
        return None
    return None


def enrich(arxiv_id: str, fields: str = DEFAULT_FIELDS) -> dict | None:
    """One-shot lookup by arXiv id. Returns enriched dict or None."""
    if not arxiv_id:
        return None
    data = _get(f"/paper/arXiv:{arxiv_id}", {"fields": fields})
    if not data:
        return None
    emb = (data.get("embedding") or {}).get("vector") or []
    tldr = (data.get("tldr") or {}).get("text") or ""
    refs = data.get("references") or []
    ref_ids = []
    for r in refs[:50]:
        ext = r.get("externalIds") or {}
        if ext.get("ArXiv"):
            ref_ids.append(f"arXiv:{ext['ArXiv']}")
        elif ext.get("DOI"):
            ref_ids.append(f"doi:{ext['DOI']}")
    return {
        "paper_id":              arxiv_id,
        "semsch_title":          data.get("title", ""),
        "semsch_abstract":       data.get("abstract", "") or "",
        "tldr":                  tldr,
        "embedding":             emb,
        "year":                  data.get("year"),
        "venue":                 data.get("venue", "") or "",
        "citation_count":        data.get("citationCount", 0) or 0,
        "influential_citations": data.get("influentialCitationCount", 0) or 0,
        "fields_of_study":       data.get("fieldsOfStudy") or [],
        "reference_ids":         ref_ids,
        "open_access_pdf":       (data.get("openAccessPdf") or {}).get("url"),
    }


def citations(arxiv_id: str, limit: int = 20) -> list[dict]:
    """Forward citations."""
    if not arxiv_id:
        return []
    data = _get(f"/paper/arXiv:{arxiv_id}/citations",
                {"fields": "title,year,externalIds,citationCount", "limit": limit})
    if not data:
        return []
    return data.get("data") or []


def references(arxiv_id: str, limit: int = 20) -> list[dict]:
    """Backward citations."""
    if not arxiv_id:
        return []
    data = _get(f"/paper/arXiv:{arxiv_id}/references",
                {"fields": "title,year,externalIds,citationCount", "limit": limit})
    if not data:
        return []
    return data.get("data") or []


def recommend(arxiv_id: str, limit: int = 10) -> list[dict]:
    """Semantic-Scholar's own related-paper recommendations (different endpoint)."""
    if not arxiv_id:
        return []
    try:
        import requests
    except ImportError:
        return []
    _throttle()
    try:
        r = requests.get(
            f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/arXiv:{arxiv_id}",
            params={"fields": "title,year,externalIds,abstract,tldr", "limit": limit},
            headers=_headers(), timeout=20,
        )
    except Exception:
        return []
    if r.status_code != 200:
        return []
    try:
        return (r.json() or {}).get("recommendedPapers") or []
    except Exception:
        return []


def cosine(a: Iterable[float], b: Iterable[float]) -> float:
    """Plain cosine — no numpy dep."""
    a = list(a); b = list(b)
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na  = sum(x * x for x in a) ** 0.5
    nb  = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)
