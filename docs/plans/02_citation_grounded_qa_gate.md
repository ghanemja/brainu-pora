# Plan 02 — Citation-grounded QA gate

**Status:** designed, not yet implemented
**Touches:** `agents/judge.py`, `agents/curriculum.py`, new module
`agents/grounding.py`, new module `agents/qa_gate.py`
**Estimated effort:** ~2 engineer-weeks

---

## Why

Today `judge.py` scores a turn on heuristics (presence-of-citation,
length, prompt overlap). That tells you the agent *said* something
plausible — not that the claims are *true with respect to the source
corpus*. For a company-knowledge tool, ungrounded lessons are worse
than no lesson: they look authoritative while being wrong. We need a
gate: a lesson cannot be served until every factual claim is entailed
by a cited source.

## Scope

In:
1. `agents/grounding.py` — claim extraction + per-claim source-entailment scoring.
2. `agents/qa_gate.py` — composite pre-publish gate that fails any lesson below per-axis thresholds.
3. New stage in lesson generation pipeline: after `curriculum.py` produces a lesson, run it through `qa_gate.gate(lesson)` before caching as servable.
4. Persist QA verdicts to `data/sessions/qa_verdicts.jsonl` for replay + analytics.
5. UI exposure: failed lessons surface in `feedback_panel.py` as a "needs human review" queue.

Out (deferred):
- Auto-rewriting failed lessons (Phase 4).
- Multi-judge ensemble across different model families (Phase 4 — separate item in the roadmap).
- Cross-lesson contradiction detection (Phase 4 — separate item).

## API surface

```python
# agents/grounding.py

@dataclass
class Claim:
    text:        str
    span:        tuple[int, int]   # char offsets in source lesson field
    cited:       list[str]         # citation tokens parsed from the surrounding context
    field:       str               # 'summary' | 'key_idea' | 'worked_example' | ...

@dataclass
class GroundingResult:
    claim:       Claim
    sources:     list[dict]        # {kind, id, snippet, similarity}
    entailment:  float             # 0..1, per LLM rubric
    verdict:     str               # 'grounded' | 'partial' | 'unsupported'

def extract_claims(lesson: dict) -> list[Claim]:
    """Split each lesson field into independent factual claims."""

def ground_claim(claim: Claim, *, corpus: str = "auto") -> GroundingResult:
    """Retrieve top-k sources for the claim; score entailment 0..1."""

def ground_lesson(lesson: dict) -> list[GroundingResult]:
    """Convenience: extract + ground every claim in one lesson."""
```

```python
# agents/qa_gate.py

@dataclass
class QAVerdict:
    lesson_id:        str
    pass_:            bool
    scores:           dict[str, float]   # axis -> score in [0,1]
    failed_axes:      list[str]
    unsupported:      list[Claim]
    reading_level:    float              # Flesch-Kincaid grade
    timestamp:        str

GATE_THRESHOLDS = {
    "heuristic_score":   0.60,
    "llm_rubric_score":  0.70,
    "grounding_score":   0.70,   # mean entailment across all claims
    "min_grounded_frac": 0.90,   # ≥90% of claims must be 'grounded'
    "reading_level_max": 14.0,   # don't exceed graduate-level reading
}

def gate(lesson: dict, *, audience: str = "professional") -> QAVerdict:
    """Run the full QA gate. Returns verdict + writes to qa_verdicts.jsonl."""
```

## Pipeline integration

```
curriculum.generate_lesson(node)
  → lesson dict
  → qa_gate.gate(lesson)
      → if pass: write to lesson_cache + serve
      → if fail: write to needs_review_queue
                 surface in feedback_panel
                 do NOT serve
```

`media.py` and `video_generator.py` only ever read from `lesson_cache`,
so they never render a lesson that hasn't passed the gate.

## Claim extraction strategy

1. Split each lesson field by sentence (spaCy or simple regex).
2. Drop sentences that are explicitly opinion-flagged ("we recommend",
   "in our view"). They're not factual claims.
3. For each remaining sentence, the surrounding lesson context (the
   `key_ideas` it lives in + the cited tokens) becomes its provenance
   pool.

## Entailment scoring

Three signals, mixed by weight:

| Signal              | Weight | How                                                                              |
| ------------------- | -----: | -------------------------------------------------------------------------------- |
| Embedding similarity |  0.3  | Sentence-transformer cosine, claim vs top retrieved source snippet.              |
| Lexical overlap      |  0.2  | BM25-style token recall — cheap sanity check.                                    |
| LLM entailment       |  0.5  | Claude rubric: "Does the source explicitly support / contradict / not address?"  |

A claim with score ≥ 0.7 is `grounded`. 0.4–0.7 is `partial`. <0.4 is
`unsupported`.

## Failure modes & rollout

- Cold-start: no corpus yet → all lessons would fail. Gate has a
  `BYPASS_GROUNDING=true` flag that records verdicts but doesn't block,
  used until the corpus is dense enough.
- LLM judge cost: ~1¢ per claim × 8 claims × N lessons. Cache verdicts
  by `(lesson_hash, source_corpus_hash)`.
- Latency: gate adds 5–15s per lesson. Run async; user sees "lesson
  generating" placeholder until verdict + cache write complete.

## Acceptance checks

- [ ] Inject a known-false claim into a test lesson → gate fails it.
- [ ] Inject a known-true-but-uncited claim → gate marks `partial` with the missing-citation surfaced.
- [ ] Real lessons from the current corpus get ≥0.7 mean entailment.
- [ ] Verdicts written to `qa_verdicts.jsonl` are replayable through `scripts/replay_sessions.py`.
- [ ] `feedback_panel.py` shows the needs-review queue and per-axis breakdown.
- [ ] Total per-lesson QA cost <$0.20 with the LLM judge enabled.

## Risks

- Entailment LLM hallucinating its own judgments → run a small
  human-validated golden set monthly, alert on drift.
- Conservative gate kills the velocity of new lessons → tune
  `min_grounded_frac` empirically; start at 0.7 and ratchet up.
