"""
Citation backtrack — map a claim in a lesson/podcast back to the exact
paragraph in the source paper that supports it.

Pipeline:
  1. Caller passes a claim string + a list of candidate source paper IDs.
  2. We pull each source paper (defense corpus or wiki page), split into
     paragraphs, and score each paragraph against the claim using
     BM25 (rank_bm25) for fast local retrieval.
  3. Top-K paragraphs returned with score + paper_id + paragraph_idx.
  4. Optional: verify(claim, paragraph) → Claude yes/no/partial.

Public:
  candidates(claim, paper_ids, k=3)              → list[Hit]
  verify(claim, paragraph)                       → "supports" | "contradicts" | "neutral"
  Hit = {"paper_id": str, "para_idx": int, "text": str, "score": float}
"""

from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DEFENSE_PATH = PROJECT_ROOT / "data" / "defense_corpus_samples.json"
WIKI_DIR = PROJECT_ROOT / "wiki" / "concepts"


def candidates(claim: str, paper_ids: list[str], k: int = 3) -> list[dict]:
    """Return top-K source paragraphs supporting `claim`."""
    paras: list[tuple[str, int, str]] = []  # (paper_id, idx, text)
    for pid in paper_ids:
        for i, p in enumerate(_paragraphs_for(pid)):
            if len(p) < 40:
                continue
            paras.append((pid, i, p))
    if not paras:
        return []

    try:
        from rank_bm25 import BM25Okapi
        corpus = [_tokens(t) for _, _, t in paras]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(_tokens(claim))
    except ImportError:
        # word-overlap fallback
        claim_tokens = set(_tokens(claim))
        scores = [
            len(claim_tokens & set(_tokens(t))) / max(1, len(claim_tokens))
            for _, _, t in paras
        ]

    ranked = sorted(zip(paras, scores), key=lambda x: -x[1])[:k]
    return [
        {"paper_id": pid, "para_idx": idx, "text": text, "score": float(score)}
        for (pid, idx, text), score in ranked if score > 0
    ]


def verify(claim: str, paragraph: str) -> str:
    """Claude check: does `paragraph` support `claim`?"""
    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=(
                "Decide if PARAGRAPH supports CLAIM. Output one word: "
                "supports / contradicts / neutral. No other text."
            ),
            user=f"CLAIM: {claim}\n\nPARAGRAPH: {paragraph[:2000]}",
            max_tokens=10,
            retries=2,
        )
        verdict = (raw or "").strip().lower().split()[0]
        if verdict in {"supports", "contradicts", "neutral"}:
            return verdict
    except Exception:
        pass
    return "neutral"


# ── Source loaders ─────────────────────────────────────────────────────────

def _paragraphs_for(paper_id: str) -> list[str]:
    """Pull paragraphs for a paper or wiki page."""
    if paper_id.startswith("def/") or paper_id.startswith("paper:"):
        pid = paper_id.split("/", 1)[-1].split(":", 1)[-1]
        return _defense_paragraphs(pid)
    if paper_id.startswith("wiki/") or paper_id.startswith("[[wiki/"):
        stem = re.sub(r"[\[\]]", "", paper_id).removeprefix("wiki/")
        return _wiki_paragraphs(stem)
    # heuristic — try wiki by stem
    return _wiki_paragraphs(paper_id)


def _defense_paragraphs(pid: str) -> list[str]:
    if not DEFENSE_PATH.exists():
        return []
    try:
        corpus = json.loads(DEFENSE_PATH.read_text())
    except json.JSONDecodeError:
        return []
    for paper in corpus.get("papers", []):
        if paper.get("id") == pid:
            body = "\n\n".join([
                paper.get("abstract", ""),
                paper.get("intro", ""),
                paper.get("body", ""),
            ])
            return _split_paras(body)
    return []


def _wiki_paragraphs(stem: str) -> list[str]:
    candidates_path = [
        WIKI_DIR / f"{stem}.md",
        WIKI_DIR / f"{stem.replace(' ', '_')}.md",
        WIKI_DIR / f"{stem.replace(' ', '-')}.md",
    ]
    for p in candidates_path:
        if p.exists():
            return _split_paras(p.read_text(errors="ignore"))
    return []


def _split_paras(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z\-]+", (text or "").lower())
