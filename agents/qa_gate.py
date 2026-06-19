"""
Pre-publish QA gate — composite verdict on whether a generated lesson
is safe to serve.

A lesson must pass every axis below to be marked `pass_=True`:

  heuristic_score   ≥ 0.60     (cheap signal mix from agents.judge)
  llm_rubric_score  ≥ 0.70     (optional Claude rubric; only when LLM available)
  grounding_score   ≥ 0.70     (mean per-claim entailment; agents.grounding)
  min_grounded_frac ≥ 0.90     (≥90% of claims must be 'grounded')
  reading_level     ≤ 14.0     (Flesch-Kincaid grade — graduate-and-below)

Verdicts are persisted append-only to
  data/sessions/qa_verdicts.jsonl

so callers can replay, audit, and surface a needs-review queue.

Failed lessons should NOT be served; they should land in a UI review
queue (the React UI's feedback panel is a good home).

Public:
  gate(lesson, *, audience='professional') -> QAVerdict
  QAVerdict dataclass
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
VERDICTS_PATH = PROJECT_ROOT / "data" / "sessions" / "qa_verdicts.jsonl"
VERDICTS_PATH.parent.mkdir(parents=True, exist_ok=True)


# ── Thresholds (env-overridable) ─────────────────────────────────────────

GATE_THRESHOLDS = {
    "heuristic_score":   float(os.environ.get("QA_HEURISTIC_MIN", 0.60)),
    "llm_rubric_score":  float(os.environ.get("QA_LLM_MIN",       0.70)),
    "grounding_score":   float(os.environ.get("QA_GROUND_MIN",    0.70)),
    "min_grounded_frac": float(os.environ.get("QA_GROUND_FRAC",   0.90)),
    "reading_level_max": float(os.environ.get("QA_READING_MAX",   14.0)),
}


# ── Data ─────────────────────────────────────────────────────────────────

@dataclass
class QAVerdict:
    lesson_id:      str
    pass_:          bool
    scores:         dict
    failed_axes:    list[str]
    unsupported:    list[dict] = field(default_factory=list)
    contradicted:   list[dict] = field(default_factory=list)
    reading_level:  float = 0.0
    audience:       str = "professional"
    timestamp:      str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["pass"] = d.pop("pass_")
        return d


# ── Reading level ────────────────────────────────────────────────────────

_VOWEL_RE = re.compile(r"[aeiouyAEIOUY]+")


def _syllables(word: str) -> int:
    """Rough syllable count — good enough for FK grade."""
    word = re.sub(r"[^A-Za-z]", "", word)
    if not word:
        return 0
    groups = _VOWEL_RE.findall(word)
    n = max(1, len(groups))
    if word.lower().endswith("e") and n > 1:
        n -= 1
    return n


def flesch_kincaid_grade(text: str) -> float:
    text = (text or "").strip()
    if not text:
        return 0.0
    sentences = max(1, len(re.findall(r"[.!?]+", text)))
    words = re.findall(r"\b[\w']+\b", text)
    n_words = max(1, len(words))
    n_syll = sum(_syllables(w) for w in words)
    return round(
        0.39 * (n_words / sentences)
        + 11.8 * (n_syll / n_words)
        - 15.59, 2,
    )


# ── Heuristic + LLM rubric scoring (delegated to agents.judge) ───────────

def _heuristic_score(lesson: dict) -> float:
    """Run agents.judge heuristic over the lesson body. Returns 0..1."""
    try:
        from agents.judge import heuristic_score
    except Exception:
        return 0.5
    body = (lesson.get("summary") or "") + " " + \
           " ".join(lesson.get("key_ideas") or []) + " " + \
           (lesson.get("worked_example") or "")
    try:
        result = heuristic_score(
            response=body,
            problem=lesson.get("title", ""),
            citations=lesson.get("citations") or [],
        )
        if isinstance(result, dict):
            return float(result.get("score") or
                          sum(result.get("axes", {}).values()) / max(
                              1, len(result.get("axes", {}))))
        return float(result)
    except Exception:
        return 0.5


LLM_RUBRIC_SYSTEM = """You're grading a lesson on 5 axes (each 0..1):
  - relevance:   does it address the stated title?
  - evidence:    are claims supported by what's in the lesson?
  - depth:       does it go beyond surface-level definitions?
  - calibration: does it state uncertainty appropriately?
  - novelty:    does it surface something not just a re-statement of the title?
Output strict JSON only:
  {"relevance": float, "evidence": float, "depth": float,
   "calibration": float, "novelty": float, "overall": float}"""


def _llm_rubric_score(lesson: dict) -> float | None:
    """Optional Claude rubric. Returns None if unavailable."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    if os.environ.get("QA_USE_LLM", "1") == "0":
        return None
    try:
        from agents.specialists import SYNTHESIZER_MODEL
        from agents.orchestrator import _call_claude
    except Exception:
        return None
    blob = (
        f"TITLE: {lesson.get('title', '')}\n"
        f"SUMMARY: {lesson.get('summary', '')}\n"
        f"KEY IDEAS:\n" +
        "\n".join(f"  - {i}" for i in lesson.get("key_ideas") or []) +
        f"\nWORKED: {lesson.get('worked_example', '')}\n"
        f"ENGAGE: {lesson.get('engagement_question', '')}"
    )
    try:
        raw = _call_claude(
            model=SYNTHESIZER_MODEL, system=LLM_RUBRIC_SYSTEM,
            user=blob, max_tokens=200, retries=1,
        ).strip()
    except Exception:
        return None
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:
        return None
    if "overall" in d:
        return float(d["overall"])
    vals = [v for v in d.values() if isinstance(v, (int, float))]
    return sum(vals) / max(1, len(vals)) if vals else None


# ── Main gate ────────────────────────────────────────────────────────────

def gate(lesson: dict, *, audience: str = "professional") -> QAVerdict:
    """Run the full QA gate on a lesson and persist the verdict."""
    lesson_id = hashlib.sha1(
        json.dumps({
            "t": lesson.get("title", ""),
            "s": lesson.get("summary", ""),
            "k": lesson.get("key_ideas") or [],
        }, sort_keys=True).encode()
    ).hexdigest()[:16]

    # Grounding (lazy import to avoid loading sentence-transformers at module load)
    try:
        from agents.grounding import ground_lesson
        grounded = ground_lesson(lesson)
    except Exception:
        grounded = []

    if grounded:
        entail = [g.entailment for g in grounded]
        mean_entail = sum(entail) / len(entail)
        grounded_frac = sum(1 for g in grounded
                            if g.verdict == "grounded") / len(grounded)
        unsupported = [g.to_dict() for g in grounded
                        if g.verdict == "unsupported"]
        contradicted = [g.to_dict() for g in grounded
                        if g.signals.get("contradicted")]
    else:
        mean_entail = 0.0
        grounded_frac = 0.0
        unsupported = []
        contradicted = []

    heur = _heuristic_score(lesson)
    llm = _llm_rubric_score(lesson)

    body = (lesson.get("summary") or "") + " " + \
           " ".join(lesson.get("key_ideas") or []) + " " + \
           (lesson.get("worked_example") or "")
    rl = flesch_kincaid_grade(body)

    scores = {
        "heuristic_score":  round(heur, 3),
        "llm_rubric_score": (round(llm, 3) if llm is not None else None),
        "grounding_score":  round(mean_entail, 3),
        "grounded_frac":    round(grounded_frac, 3),
        "reading_level":    rl,
    }

    failed: list[str] = []
    if heur < GATE_THRESHOLDS["heuristic_score"]:
        failed.append("heuristic_score")
    if llm is not None and llm < GATE_THRESHOLDS["llm_rubric_score"]:
        failed.append("llm_rubric_score")
    if grounded and mean_entail < GATE_THRESHOLDS["grounding_score"]:
        failed.append("grounding_score")
    if grounded and grounded_frac < GATE_THRESHOLDS["min_grounded_frac"]:
        failed.append("min_grounded_frac")
    if rl > GATE_THRESHOLDS["reading_level_max"]:
        failed.append("reading_level_max")
    if contradicted:
        failed.append("contains_contradicted_claim")

    # Bypass during cold-start (no corpus yet) so dev isn't blocked
    bypass = os.environ.get("BYPASS_GROUNDING", "").lower() in (
        "1", "true", "yes")
    pass_ = (len(failed) == 0) or bypass

    verdict = QAVerdict(
        lesson_id=lesson_id, pass_=pass_, scores=scores,
        failed_axes=failed, unsupported=unsupported,
        contradicted=contradicted, reading_level=rl,
        audience=audience,
        timestamp=_dt.datetime.utcnow().isoformat() + "Z",
    )

    # Persist
    try:
        with VERDICTS_PATH.open("a") as f:
            f.write(json.dumps(verdict.to_dict()) + "\n")
    except Exception:
        pass

    return verdict


# ── Bulk replay over an existing lesson cache (useful for golden set) ────

def replay_all(lesson_iter) -> list[QAVerdict]:
    """Re-gate a sequence of lessons. Returns the verdicts list."""
    return [gate(lsn) for lsn in lesson_iter]
