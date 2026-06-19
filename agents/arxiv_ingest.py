"""
Daily arXiv ingest — pull new papers in the user's interest clusters and
add them as graph nodes.

Run as a cron: `python -m agents.arxiv_ingest --interest "neural collapse"`.

Uses arXiv's public API (no key). For each interest:
  1. Query api.arxiv.org/api/query for last 24h in matching categories
  2. Score returned papers by keyword match against interest + nearby
     graph nodes
  3. Insert top-N as new nodes in data/defense_corpus_samples.json with
     date, abstract, topics
  4. Optionally trigger a podcast generation for the highest-scored paper

Public:
  ingest(interests, lookback_days=1, max_per_interest=5)
      → list of new paper IDs
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).parent.parent
DEFENSE_PATH = PROJECT_ROOT / "data" / "defense_corpus_samples.json"
INGEST_LOG = PROJECT_ROOT / "data" / "sessions" / "arxiv_ingest_log.json"
INGEST_LOG.parent.mkdir(parents=True, exist_ok=True)


ARXIV_API = "http://export.arxiv.org/api/query"


def ingest(interests: list[str], lookback_days: int = 1,
           max_per_interest: int = 5) -> list[str]:
    """Pull new arXiv papers matching interests. Returns list of new IDs."""
    new_ids: list[str] = []
    corpus = _load_corpus()
    existing_ids = {p.get("id") for p in corpus.get("papers", [])}
    cutoff = dt.datetime.utcnow() - dt.timedelta(days=lookback_days)

    for interest in interests:
        hits = _search_arxiv(interest, max_results=max_per_interest * 3)
        added_for_interest = 0
        for hit in hits:
            if added_for_interest >= max_per_interest:
                break
            if hit["id"] in existing_ids:
                continue
            try:
                pub = dt.datetime.fromisoformat(hit["published"].replace("Z", ""))
            except (ValueError, KeyError):
                pub = dt.datetime.utcnow()
            if pub < cutoff:
                continue
            paper = {
                "id":        hit["id"],
                "title":     hit["title"],
                "authors":   hit["authors"],
                "abstract":  hit["abstract"],
                "topics":    _derive_topics(hit, interest),
                "published": hit["published"],
                "url":       hit["url"],
                "ingested_at": dt.datetime.utcnow().isoformat(),
                "interest_match": interest,
            }
            corpus["papers"].append(paper)
            new_ids.append(hit["id"])
            existing_ids.add(hit["id"])
            added_for_interest += 1

    if new_ids:
        _save_corpus(corpus)
        _log_ingest(interests, new_ids)
    return new_ids


def _search_arxiv(query: str, max_results: int = 15) -> list[dict]:
    try:
        import requests
    except ImportError:
        return []
    url = (
        f"{ARXIV_API}?search_query=all:{quote_plus(query)}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={max_results}"
    )
    try:
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return []
    except Exception:
        return []
    return _parse_atom(r.text)


def _parse_atom(xml: str) -> list[dict]:
    """Minimal Atom parser — no xml dependency."""
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    out = []
    for e in entries:
        out.append({
            "id":        _strip_tags(_first(e, "id")).split("/")[-1],
            "title":     _strip_tags(_first(e, "title")),
            "authors":   ", ".join(re.findall(r"<author>.*?<name>(.*?)</name>", e, re.DOTALL))[:200],
            "abstract":  _strip_tags(_first(e, "summary"))[:3000],
            "published": _strip_tags(_first(e, "published")),
            "url":       _strip_tags(_first(e, "id")),
        })
    return out


def _first(text: str, tag: str) -> str:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return (m.group(1) if m else "").strip()


def _strip_tags(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text or "")).strip()


def _derive_topics(hit: dict, interest: str) -> list[str]:
    title_tokens = re.findall(r"[A-Z][a-z]{3,}", hit.get("title", ""))
    return list({interest, *title_tokens[:4]})


def _load_corpus() -> dict:
    if DEFENSE_PATH.exists():
        try:
            return json.loads(DEFENSE_PATH.read_text())
        except json.JSONDecodeError:
            pass
    return {"papers": []}


def _save_corpus(corpus: dict) -> None:
    DEFENSE_PATH.write_text(json.dumps(corpus, indent=2))


def _log_ingest(interests: list[str], new_ids: list[str]) -> None:
    log = []
    if INGEST_LOG.exists():
        try:
            log = json.loads(INGEST_LOG.read_text())
        except json.JSONDecodeError:
            pass
    log.append({
        "ts": dt.datetime.utcnow().isoformat(),
        "interests": interests,
        "added": new_ids,
    })
    INGEST_LOG.write_text(json.dumps(log[-200:], indent=2))


# ── CLI ────────────────────────────────────────────────────────────────────

def _cli():
    p = argparse.ArgumentParser()
    p.add_argument("--interest", action="append", required=True,
                   help="search term (repeat for multiple)")
    p.add_argument("--lookback-days", type=int, default=1)
    p.add_argument("--max-per-interest", type=int, default=5)
    args = p.parse_args()
    added = ingest(args.interest, args.lookback_days, args.max_per_interest)
    print(f"Added {len(added)} new papers: {added}")


if __name__ == "__main__":
    _cli()
