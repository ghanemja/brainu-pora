"""
Unified content finder for the learning app.

Priority order (cheap → expensive, local → remote):
  1. wiki/concepts/<topic>.md           full text if it exists
  2. Specialist.retrieve over BM25      top arXiv chunks across aero/mech/cs
  3. defense_corpus manifest BM25       DTIC / NTRS / OpenAlex / arXiv-defense
  4. Wikipedia REST API (en)            fallback open-web summary
  5. DuckDuckGo HTML search             only if explicitly requested

All steps are best-effort and isolated — if step 3 errors, steps 4 keep going.

Public:
  find(topic, k=5, allow_web=True) → {
    "wiki": dict | None,           # local wiki page (text + path)
    "rag":  list[dict],            # arXiv BM25 hits across all 3 specialists
    "defense": list[dict],         # defense-corpus BM25 hits
    "wikipedia": dict | None,      # Wikipedia summary (only if allow_web)
    "web": list[dict],             # DDG hits (only if allow_web)
  }
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).parent.parent
WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"
DEFENSE_MANIFEST = PROJECT_ROOT / "data" / "defense_corpus" / "MANIFEST.jsonl"


# ── Wiki ──────────────────────────────────────────────────────────────────

def _find_wiki(topic: str) -> dict | None:
    """Best-effort path lookup. Returns {title, path, text} or None."""
    candidates = [
        topic, topic.replace(" ", "_"), topic.replace(" ", "-"),
        topic.title().replace(" ", "_"),
    ]
    for c in candidates:
        p = WIKI_CONCEPTS / f"{c}.md"
        if p.exists():
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            return {"title": p.stem.replace("_", " "),
                    "path": str(p.relative_to(PROJECT_ROOT)),
                    "text": txt}
    # case-insensitive scan
    target = topic.replace(" ", "_").lower()
    for p in WIKI_CONCEPTS.glob("*.md"):
        if p.stem.lower() == target:
            return {"title": p.stem.replace("_", " "),
                    "path": str(p.relative_to(PROJECT_ROOT)),
                    "text": p.read_text(errors="ignore")}
    return None


# ── Specialist BM25 (all three domains) ──────────────────────────────────

def _find_rag(topic: str, k: int = 5) -> list[dict]:
    out: list[dict] = []
    try:
        from agents.specialists import SPECIALISTS
    except Exception:
        return out
    for key, spec in SPECIALISTS.items():
        try:
            hits = spec.retrieve(topic, top_k=k)
            for h in hits:
                h2 = dict(h)
                h2["domain"] = key
                out.append(h2)
        except Exception:
            continue
    out.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return out[: k * 2]


# ── Defense corpus BM25 ──────────────────────────────────────────────────

_defense_index_cache: dict | None = None


def _defense_index():
    global _defense_index_cache
    if _defense_index_cache is not None:
        return _defense_index_cache
    if not DEFENSE_MANIFEST.exists():
        _defense_index_cache = {"bm25": None, "chunks": []}
        return _defense_index_cache
    chunks = []
    for line in DEFENSE_MANIFEST.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        title = obj.get("title", "") or ""
        abstract = obj.get("abstract", "") or ""
        if not (title or abstract):
            continue
        chunks.append({**obj, "text": f"{title}\n\n{abstract}"})
    if not chunks:
        _defense_index_cache = {"bm25": None, "chunks": []}
        return _defense_index_cache
    try:
        from rank_bm25 import BM25Okapi
    except ImportError:
        _defense_index_cache = {"bm25": None, "chunks": chunks}
        return _defense_index_cache
    TOK = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")
    tokenized = [
        [t.lower() for t in TOK.findall(c["text"]) if len(t) > 2]
        for c in chunks
    ]
    _defense_index_cache = {"bm25": BM25Okapi(tokenized), "chunks": chunks}
    return _defense_index_cache


def _find_defense(topic: str, k: int = 5) -> list[dict]:
    idx = _defense_index()
    if idx["bm25"] is None or not idx["chunks"]:
        return []
    TOK = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")
    toks = [t.lower() for t in TOK.findall(topic) if len(t) > 2]
    if not toks:
        return []
    scores = idx["bm25"].get_scores(toks)
    ranked = sorted(zip(scores, idx["chunks"]), key=lambda x: x[0], reverse=True)
    out = []
    for s, c in ranked[: k]:
        if s <= 0:
            break
        out.append({**c, "_score": float(s)})
    return out


# ── Wikipedia REST API ────────────────────────────────────────────────────

def _find_wikipedia(topic: str) -> dict | None:
    """Hit Wikipedia summary endpoint. No API key needed."""
    try:
        import urllib.request as _u
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(topic.replace(' ', '_'))}"
        req = _u.Request(url, headers={"User-Agent": "BrainUniversity/0.1 (learning-app)"})
        with _u.urlopen(req, timeout=6) as r:
            data = json.loads(r.read().decode("utf-8"))
        if not data.get("extract"):
            return None
        return {
            "title":   data.get("title", topic),
            "extract": data.get("extract", ""),
            "url":     data.get("content_urls", {}).get("desktop", {}).get("page",
                       f"https://en.wikipedia.org/wiki/{quote_plus(topic)}"),
            "thumbnail": (data.get("thumbnail") or {}).get("source"),
        }
    except Exception:
        return None


# ── DuckDuckGo HTML search ────────────────────────────────────────────────

DDG_RESULT_RE = re.compile(
    r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
DDG_SNIPPET_RE = re.compile(
    r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def _find_web_ddg(topic: str, k: int = 5) -> list[dict]:
    """Cheap DuckDuckGo HTML scrape. Best-effort — DDG sometimes throttles
    or changes markup. Use sparingly."""
    try:
        import urllib.request as _u
        url = f"https://duckduckgo.com/html/?q={quote_plus(topic)}"
        req = _u.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36",
        })
        with _u.urlopen(req, timeout=6) as r:
            html = r.read().decode("utf-8", errors="ignore")
        urls = DDG_RESULT_RE.findall(html)[:k]
        snippets = DDG_SNIPPET_RE.findall(html)[:k]
        out = []
        for i, (u, title) in enumerate(urls):
            snip = snippets[i] if i < len(snippets) else ""
            # Unwrap DDG's redirect prefix
            if u.startswith("//duckduckgo.com/l/?uddg="):
                from urllib.parse import unquote
                u = unquote(u.split("uddg=", 1)[-1].split("&", 1)[0])
            out.append({
                "title":   _strip_html(title)[:160],
                "url":     u,
                "snippet": _strip_html(snip)[:280],
            })
        return out
    except Exception:
        return []


# ── Public ─────────────────────────────────────────────────────────────────

def find(topic: str, k: int = 5, allow_web: bool = True) -> dict:
    """Return everything we know about `topic` from cheapest to costliest.

    `allow_web=False` skips Wikipedia + DDG (offline mode).
    """
    out = {
        "wiki":       _find_wiki(topic),
        "rag":        _find_rag(topic, k=k),
        "defense":    _find_defense(topic, k=k),
        "wikipedia":  None,
        "web":        [],
    }
    if allow_web:
        out["wikipedia"] = _find_wikipedia(topic)
        # Skip DDG by default — opt-in via second flag
    return out


def find_with_web(topic: str, k: int = 5) -> dict:
    """Like find() but also runs a DuckDuckGo HTML scrape. Slow + flaky."""
    out = find(topic, k=k, allow_web=True)
    out["web"] = _find_web_ddg(topic, k=k)
    return out
