"""
Paper drop — single arXiv URL → graph node + cluster placement + podcast.

Demo cascade:
  1. resolve_arxiv_id(url)          extract paper id from URL
  2. fetch_metadata(paper_id)       title, abstract, authors via arXiv API
  3. classify(paper)                map abstract → existing graph clusters
  4. add_to_corpus(paper, cluster)  append to defense_corpus_samples.json
  5. generate_podcast(paper)        run podcast_script + podcast_video

Drives endpoint POST /paper/drop  → SSE stream of cascade events.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Callable, Iterable

PROJECT_ROOT = Path(__file__).parent.parent
CORPUS_PATH = PROJECT_ROOT / "data" / "defense_corpus_samples.json"

ARXIV_API = "http://export.arxiv.org/api/query"


def resolve_arxiv_id(url_or_id: str) -> str | None:
    """Accept full URL, arXiv ID, or abs/pdf path. Return canonical ID."""
    s = (url_or_id or "").strip()
    if not s:
        return None
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", s)
    if m:
        return m.group(1)
    m = re.search(r"([a-z\-]+/\d{7})", s)
    if m:
        return m.group(1)
    return None


def fetch_metadata(paper_id: str) -> dict | None:
    """Pull title + abstract + authors for an arXiv ID."""
    try:
        import requests
    except ImportError:
        return None
    try:
        r = requests.get(f"{ARXIV_API}?id_list={paper_id}", timeout=30)
    except Exception:
        return None
    if r.status_code != 200:
        return None
    return _parse_first_entry(r.text, paper_id)


def _parse_first_entry(xml: str, paper_id: str) -> dict | None:
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    if not entries:
        return None
    e = entries[0]
    return {
        "id":        paper_id,
        "title":     _strip(_first(e, "title")),
        "authors":   ", ".join(re.findall(r"<author>.*?<name>(.*?)</name>", e, re.DOTALL))[:300],
        "abstract":  _strip(_first(e, "summary"))[:3000],
        "published": _strip(_first(e, "published")),
        "url":       f"https://arxiv.org/abs/{paper_id}",
        "topics":    re.findall(r'<category term="([^"]+)"', e),
    }


def classify(paper: dict, clusters: Iterable, embedding: list[float] | None = None) -> dict:
    """Best-fit cluster for `paper`.

    Strategy:
      1. If `embedding` (SPECTER2 vector) provided AND any cluster has a cached
         centroid, score by cosine similarity. Returns highest.
      2. Else fall back to keyword token overlap with cluster name + top nodes.

    Adds `method` field so callers know which path won.
    """
    clusters = list(clusters or [])

    # ── Path 1: embedding-based rerank ────────────────────────────────────
    if embedding:
        from . import semantic_scholar as ss
        best_e = None
        best_sim = -1.0
        for cluster in clusters:
            centroid = getattr(cluster, "centroid", None)
            if not centroid:
                continue
            sim = ss.cosine(embedding, centroid)
            if sim > best_sim:
                best_sim = sim
                best_e = cluster
        if best_e is not None:
            return {
                "cluster_id":   getattr(best_e, "cluster_id", None),
                "cluster_name": getattr(best_e, "name", None),
                "match_score":  round(best_sim, 4),
                "method":       "specter2_cosine",
            }

    # ── Path 2: keyword overlap fallback ─────────────────────────────────
    text = " ".join([
        paper.get("title", ""), paper.get("abstract", ""),
        " ".join(paper.get("topics", [])),
    ]).lower()
    tokens = set(re.findall(r"[a-z][a-z\-]+", text))

    best = None
    best_score = -1
    for cluster in clusters:
        cname = (getattr(cluster, "name", "") or "").lower()
        nodes = [n.lower() for n, _ in (cluster.top_nodes or [])]
        cluster_tokens = set(re.findall(r"[a-z][a-z\-]+", cname + " " + " ".join(nodes)))
        score = len(tokens & cluster_tokens)
        if score > best_score:
            best_score = score
            best = cluster
    return {
        "cluster_id":   getattr(best, "cluster_id", None) if best else None,
        "cluster_name": getattr(best, "name", None) if best else None,
        "match_score":  best_score,
        "method":       "keyword_overlap",
    }


def add_to_corpus(paper: dict, cluster_info: dict) -> bool:
    """Append paper to defense_corpus_samples.json (idempotent)."""
    corpus = _load_corpus()
    if any(p.get("id") == paper["id"] for p in corpus.get("papers", [])):
        return False
    entry = dict(paper)
    entry["cluster_id"]    = cluster_info.get("cluster_id")
    entry["cluster_name"]  = cluster_info.get("cluster_name")
    entry["ingested_at"]   = dt.datetime.utcnow().isoformat()
    entry["source"]        = "paper_drop"
    corpus.setdefault("papers", []).append(entry)
    CORPUS_PATH.write_text(json.dumps(corpus, indent=2))
    return True


def cascade(url_or_id: str, emit: Callable[[str, dict], None] | None = None,
            also_generate_podcast: bool = True,
            podcast_length: str = "short") -> dict:
    """Run the full paper-drop cascade. emit(kind, data) for each step."""
    def step(kind: str, data: dict):
        if emit:
            try:
                emit(kind, data)
            except Exception:
                pass

    paper_id = resolve_arxiv_id(url_or_id)
    if not paper_id:
        step("error", {"reason": "could not parse arXiv id", "input": url_or_id})
        return {"ok": False, "error": "bad_id"}
    step("resolved", {"paper_id": paper_id})

    paper = fetch_metadata(paper_id)
    if not paper:
        step("error", {"reason": "metadata fetch failed", "paper_id": paper_id})
        return {"ok": False, "error": "fetch_failed"}
    step("fetched", {
        "title": paper["title"],
        "authors": paper["authors"][:120],
        "abstract_excerpt": paper["abstract"][:240] + "…",
    })

    # ── SemSch enrichment: SPECTER2 embedding + TLDR + citation graph ──
    try:
        from . import semantic_scholar as ss
        enriched = ss.enrich(paper_id)
    except Exception as e:
        enriched = None
        step("warn", {"step": "semsch", "error": str(e)})

    if enriched:
        paper["tldr"]                  = enriched.get("tldr") or ""
        paper["citation_count"]        = enriched.get("citation_count", 0)
        paper["influential_citations"] = enriched.get("influential_citations", 0)
        paper["venue"]                 = enriched.get("venue") or ""
        paper["fields_of_study"]       = enriched.get("fields_of_study") or []
        paper["reference_ids"]         = enriched.get("reference_ids") or []
        paper["open_access_pdf"]       = enriched.get("open_access_pdf")
        embedding = enriched.get("embedding") or None
        step("enriched", {
            "tldr_excerpt": (paper["tldr"] or "")[:240],
            "citations":    paper["citation_count"],
            "influential":  paper["influential_citations"],
            "venue":        paper["venue"],
            "n_refs":       len(paper["reference_ids"]),
            "has_embedding": bool(embedding),
        })
    else:
        embedding = None
        step("warn", {"step": "semsch", "error": "no_data"})

    try:
        from graph.corpus_graph import build_mixed_graph
        from graph.clusters import cluster_graph
        G = build_mixed_graph()
        clusters = cluster_graph(G)
    except Exception as e:
        clusters = []
        step("warn", {"step": "cluster_load", "error": str(e)})

    cluster_info = classify(paper, clusters, embedding=embedding)
    step("classified", cluster_info)

    added = add_to_corpus(paper, cluster_info)
    step("ingested", {"new_entry": added, "paper_id": paper_id})

    podcast = None
    if also_generate_podcast:
        step("podcast_starting", {"length": podcast_length})
        try:
            from . import podcast_script
            source = "\n\n".join([
                f"TITLE: {paper['title']}",
                f"ABSTRACT: {paper['abstract']}",
                f"AUTHORS: {paper['authors']}",
                f"TOPICS: {', '.join(paper.get('topics', []))}",
            ])
            podcast = podcast_script.generate_script(
                topic=paper["title"][:80],
                source_text=source,
                length=podcast_length,
                angle=f"new paper on {cluster_info.get('cluster_name', 'this area')}",
            )
            step("podcast_ready", {"turns": len(podcast.get("turns") or [])}
                 if podcast else {"error": "script gen failed"})
        except Exception as e:
            step("warn", {"step": "podcast", "error": str(e)})

    step("done", {"paper_id": paper_id, "cluster_id": cluster_info.get("cluster_id")})
    return {
        "ok": True,
        "paper": paper,
        "cluster": cluster_info,
        "podcast_script": podcast,
    }


# ── helpers ────────────────────────────────────────────────────────────────

def _load_corpus() -> dict:
    if CORPUS_PATH.exists():
        try:
            return json.loads(CORPUS_PATH.read_text())
        except json.JSONDecodeError:
            return {"papers": []}
    return {"papers": []}


def _first(text: str, tag: str) -> str:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return (m.group(1) if m else "").strip()


def _strip(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text or "")).strip()
