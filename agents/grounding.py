"""
Citation-grounded fact-checking — extract atomic claims from a lesson
dict, retrieve the candidate supporting passages from the corpus, and
score per-claim entailment against those passages.

This is the substantive half of the QA gate; `agents.qa_gate` composes
this with reading-level + heuristic scores to produce a publish verdict.

Design notes
------------
- Three signals mixed per claim:
    embedding cosine + lexical recall + LLM entailment rubric
- Falls back to heuristic-only scoring when no LLM key is present
  (the gate still works, just with lower precision).
- Verdicts cached by (lesson_hash, corpus_hash) so re-running on the
  same inputs is free.

Public:
  Claim, GroundingResult           — dataclasses (see below)
  extract_claims(lesson)           → list[Claim]
  ground_claim(claim, corpus='auto') → GroundingResult
  ground_lesson(lesson)            → list[GroundingResult]
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "sessions" / "grounding_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ── Data shapes ──────────────────────────────────────────────────────────

@dataclass
class Claim:
    text:   str
    field:  str                    # 'summary' | 'key_idea' | 'worked' | 'engagement'
    span:   tuple[int, int]        # char offsets inside `field`
    cited:  list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class GroundingResult:
    claim:       Claim
    sources:     list[dict]        # [{kind, id, snippet, similarity}]
    entailment:  float             # 0..1
    verdict:     str               # 'grounded' | 'partial' | 'unsupported'
    signals:     dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["claim"] = self.claim.to_dict()
        return d


# ── Claim extraction ─────────────────────────────────────────────────────

OPINION_FLAGS = re.compile(
    r"\b(we recommend|in our view|we think|arguably|in my opinion|perhaps|"
    r"it seems|some might|one could argue)\b", re.I)

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def _split_sentences(text: str) -> list[tuple[str, tuple[int, int]]]:
    """Return list of (sentence, (start, end))."""
    text = text.strip()
    if not text:
        return []
    out: list[tuple[str, tuple[int, int]]] = []
    cur = 0
    for raw in SENT_SPLIT.split(text):
        raw_s = raw.strip()
        if not raw_s:
            continue
        # find offset of this sentence in original text starting from cur
        idx = text.find(raw_s, cur)
        if idx < 0:
            idx = cur
        out.append((raw_s, (idx, idx + len(raw_s))))
        cur = idx + len(raw_s)
    return out


CITATION_RE = re.compile(
    r"(\[arxiv/[^\]]+\]|\[\[wiki/[^\]]+\]\]|\[tool/[\w_-]+\])"
)


def extract_claims(lesson: dict) -> list[Claim]:
    """Split each lesson text field into atomic factual claims."""
    out: list[Claim] = []
    for field_name in ("summary", "worked_example", "engagement_question"):
        text = lesson.get(field_name) or ""
        for sent, span in _split_sentences(text):
            if OPINION_FLAGS.search(sent):
                continue
            citations = CITATION_RE.findall(sent)
            out.append(Claim(text=sent, field=field_name, span=span,
                              cited=citations))
    for i, idea in enumerate(lesson.get("key_ideas") or []):
        for sent, span in _split_sentences(idea):
            if OPINION_FLAGS.search(sent):
                continue
            citations = CITATION_RE.findall(sent)
            out.append(Claim(text=sent, field=f"key_idea_{i}",
                              span=span, cited=citations))
    return out


# ── Source retrieval (uses existing content_finder) ──────────────────────

def _retrieve_sources(claim_text: str, k: int = 4) -> list[dict]:
    """Pull top-k candidate supporting snippets for a claim.

    Wraps agents.content_finder so we don't duplicate retrieval logic.
    Returns [] if the finder is unreachable."""
    try:
        from agents.content_finder import find
        result = find(claim_text, k=k, allow_web=False)
    except Exception:
        return []
    sources: list[dict] = []
    for chunk in (result.get("rag") or [])[:k]:
        sources.append({
            "kind":    "rag",
            "id":      chunk.get("id") or chunk.get("paper_id", ""),
            "snippet": (chunk.get("snippet") or chunk.get("text", ""))[:400],
            "score":   float(chunk.get("score") or 0.0),
        })
    for chunk in (result.get("defense") or [])[:k]:
        sources.append({
            "kind":    "defense",
            "id":      chunk.get("id") or chunk.get("paper_id", ""),
            "snippet": (chunk.get("snippet") or chunk.get("text", ""))[:400],
            "score":   float(chunk.get("score") or 0.0),
        })
    if result.get("wiki"):
        w = result["wiki"]
        sources.append({
            "kind":    "wiki",
            "id":      w.get("title") or w.get("page", ""),
            "snippet": (w.get("body") or w.get("text", ""))[:400],
            "score":   float(w.get("score") or 0.0),
        })
    if result.get("wikipedia"):
        w = result["wikipedia"]
        sources.append({
            "kind":    "wikipedia",
            "id":      w.get("title", ""),
            "snippet": (w.get("summary") or "")[:400],
            "score":   float(w.get("score") or 0.0),
        })
    return sources


# ── Signal extractors ────────────────────────────────────────────────────

def _lexical_recall(claim: str, snippet: str) -> float:
    """Fraction of significant claim tokens that appear in the snippet."""
    toks = {t.lower() for t in re.findall(r"[A-Za-z]{4,}", claim)}
    if not toks:
        return 0.0
    s_lc = (snippet or "").lower()
    return sum(1 for t in toks if t in s_lc) / len(toks)


def _embedding_similarity(claim: str, snippet: str) -> float | None:
    """Sentence-transformers cosine. None if the lib isn't installed."""
    try:
        from sentence_transformers import SentenceTransformer, util  # type: ignore
        model = _get_st_model()
        if model is None:
            return None
        e1 = model.encode(claim, convert_to_tensor=True,
                          show_progress_bar=False)
        e2 = model.encode(snippet, convert_to_tensor=True,
                          show_progress_bar=False)
        sim = float(util.cos_sim(e1, e2).item())
        return max(0.0, min(1.0, (sim + 1) / 2))   # rescale -1..1 to 0..1
    except Exception:
        return None


_ST_MODEL = None


def _get_st_model():
    global _ST_MODEL
    if _ST_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
            _ST_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            _ST_MODEL = False
    return _ST_MODEL or None


LLM_RUBRIC_SYSTEM = """You are a fact-checker. Given a CLAIM and a SOURCE
snippet, decide whether the source supports the claim.

Output strict JSON only, no preface:
  {"verdict": "supports" | "contradicts" | "not_addressed",
   "confidence": <0..1>,
   "reason": "<one short sentence>"}"""


def _llm_entailment(claim: str, snippet: str) -> dict | None:
    """Optional Claude pass that returns a structured verdict."""
    try:
        from agents.specialists import SYNTHESIZER_MODEL
        from agents.orchestrator import _call_claude
    except Exception:
        return None
    user = f"CLAIM: {claim}\n\nSOURCE: {snippet}"
    try:
        raw = _call_claude(model=SYNTHESIZER_MODEL,
                            system=LLM_RUBRIC_SYSTEM,
                            user=user, max_tokens=150, retries=1).strip()
    except Exception:
        return None
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


# ── Main grounding pipeline ──────────────────────────────────────────────

W_LEXICAL = float(os.environ.get("GROUNDING_W_LEXICAL", 0.2))
W_EMBED   = float(os.environ.get("GROUNDING_W_EMBED",   0.3))
W_LLM     = float(os.environ.get("GROUNDING_W_LLM",     0.5))

VERDICT_GROUNDED   = 0.70
VERDICT_PARTIAL    = 0.40


def ground_claim(claim: Claim, *, corpus: str = "auto") -> GroundingResult:
    """Score how well a single claim is supported by the corpus."""
    sources = _retrieve_sources(claim.text)
    if not sources:
        return GroundingResult(
            claim=claim, sources=[], entailment=0.0,
            verdict="unsupported",
            signals={"reason": "no sources retrieved"},
        )

    # Score each source against the claim; pick the best
    best_entail = 0.0
    best_signals: dict = {}
    for src in sources:
        snippet = src.get("snippet") or ""
        lex = _lexical_recall(claim.text, snippet)
        emb = _embedding_similarity(claim.text, snippet)
        llm = _llm_entailment(claim.text, snippet) if (
            os.environ.get("ANTHROPIC_API_KEY") and
            os.environ.get("QA_USE_LLM", "1") != "0"
        ) else None

        # Mix
        parts: list[tuple[float, float]] = []   # (weight, value)
        parts.append((W_LEXICAL, lex))
        if emb is not None:
            parts.append((W_EMBED, emb))
        if llm:
            v = llm.get("verdict", "")
            conf = float(llm.get("confidence", 0.5))
            if v == "supports":
                parts.append((W_LLM, conf))
            elif v == "contradicts":
                parts.append((W_LLM, 0.0))
                # contradictory evidence isn't just "unsupported", it's
                # *evidence of falsehood* — heavy penalty.
                best_signals["contradicted"] = True
            else:
                parts.append((W_LLM, 0.2))
        total_w = sum(w for w, _ in parts)
        score = sum(w * v for w, v in parts) / max(total_w, 1e-6)

        if score > best_entail:
            best_entail = score
            best_signals = {
                "lex": round(lex, 3),
                "embed": (round(emb, 3) if emb is not None else None),
                "llm": llm,
                "source_kind": src.get("kind"),
                "source_id":   src.get("id"),
            }

    if best_signals.get("contradicted"):
        verdict = "unsupported"
    elif best_entail >= VERDICT_GROUNDED:
        verdict = "grounded"
    elif best_entail >= VERDICT_PARTIAL:
        verdict = "partial"
    else:
        verdict = "unsupported"

    return GroundingResult(claim=claim, sources=sources,
                            entailment=round(best_entail, 3),
                            verdict=verdict, signals=best_signals)


def ground_lesson(lesson: dict) -> list[GroundingResult]:
    """Extract every claim in `lesson` and ground each."""
    return [ground_claim(c) for c in extract_claims(lesson)]


# ── Cache helpers (callers may want to memoize) ──────────────────────────

def lesson_cache_key(lesson: dict) -> str:
    blob = json.dumps({
        "title":   lesson.get("title", ""),
        "summary": lesson.get("summary", ""),
        "ideas":   lesson.get("key_ideas") or [],
        "worked":  lesson.get("worked_example") or "",
        "engage":  lesson.get("engagement_question") or "",
    }, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def load_cached(lesson: dict) -> list[GroundingResult] | None:
    p = CACHE_DIR / f"grounded_{lesson_cache_key(lesson)}.json"
    if not p.exists():
        return None
    try:
        blob = json.loads(p.read_text())
    except Exception:
        return None
    out: list[GroundingResult] = []
    for d in blob:
        c = Claim(**d["claim"])
        out.append(GroundingResult(
            claim=c, sources=d.get("sources") or [],
            entailment=float(d.get("entailment") or 0),
            verdict=d.get("verdict", "unsupported"),
            signals=d.get("signals") or {},
        ))
    return out


def save_cached(lesson: dict, results: list[GroundingResult]) -> None:
    p = CACHE_DIR / f"grounded_{lesson_cache_key(lesson)}.json"
    p.write_text(json.dumps([r.to_dict() for r in results], indent=2))
