# Plan 04 — Knowledge-gap detector

**Status:** designed, not yet implemented
**Touches:** new module `agents/gap_detector.py`, optional Slack
connector, `feedback_panel.py` UI, `scripts/gap_report.py`
**Estimated effort:** ~1.5 engineer-weeks

---

## Why

Today the wiki grows only when a human writes a note. In a company
context the most valuable signal is the opposite: **questions that
people ask which we don't have an answer for.** A gap detector turns
Brain University into a tool that actively grows the knowledge graph
by surfacing what's missing.

## Sources of "questions we don't answer well"

| Source                                    | Signal type             | Effort to integrate |
| ----------------------------------------- | ----------------------- | ------------------- |
| Slack messages with `?` in #help-* channels |  Question prompts     | Medium (connector)  |
| Failed proposal-tab queries (no matches)  | Internal signal         | Low (already have)  |
| Lessons that scored low on auto-judge     | Internal signal         | Low                 |
| Quiz questions learners got wrong         | Internal signal         | Medium (needs Plan 03) |
| Search queries with zero hits             | Internal signal         | Low                 |

Phase 1 of this plan ships with the three "internal signal" sources
only; Slack/Confluence search hooks land in Phase 5 of the roadmap.

## Scope

In:
1. `agents/gap_detector.py` — collects gap candidates from internal signals, deduplicates, clusters them.
2. For each gap cluster, propose a wiki-stub draft + suggested cluster placement.
3. Surface gaps in `feedback_panel.py` as a "gaps" tab: rank by frequency × recency × severity.
4. CLI: `scripts/gap_report.py --since=7d` for a weekly digest.
5. Per-gap suggested owner: highest-degree author in adjacent nodes' provenance.

Out (deferred to Phase 5):
- Slack thread ingestion.
- Confluence search-query log.
- Auto-PRing wiki stubs to the vault repo.

## API surface

```python
# agents/gap_detector.py

@dataclass
class GapCandidate:
    text:         str                  # the underlying question / prompt
    source:       str                  # 'proposal_no_match' | 'judge_low_score' | 'quiz_miss' | 'search_zero_hit'
    timestamp:    str
    learner_id:   str | None
    nearest:      list[tuple[str, float]]   # nearest existing concepts + similarity

@dataclass
class GapCluster:
    cluster_id:    str
    canonical:     str             # representative question text
    count:         int
    candidates:    list[GapCandidate]
    suggested_node_name: str       # proposed wiki node title
    suggested_cluster:   int       # which existing cluster it should join
    suggested_owner:     str | None
    stub_markdown:       str       # pre-populated wiki note

def collect_candidates(*, since: str = "7d") -> list[GapCandidate]:
    """Scan internal sources for unanswered questions."""

def cluster_candidates(cs: list[GapCandidate],
                       *, min_cluster_size: int = 2) -> list[GapCluster]:
    """Group near-duplicate candidates by embedding similarity."""

def propose_stubs(clusters: list[GapCluster]) -> list[GapCluster]:
    """Fill in `stub_markdown` + `suggested_node_name` per cluster."""

def write_report(clusters: list[GapCluster], out: Path) -> None:
    """Render a weekly markdown digest grouped by cluster severity."""
```

## Internal-source plumbing

- `proposal_responder.respond()` already returns `matched_concepts`. A wrapper logs a `GapCandidate` whenever this list is empty or top score < 0.3.
- `judge.score_turn()` writes a `GapCandidate(source='judge_low_score')` when the final score is <0.3 *and* there's no matched concept.
- Search box in `wiki_explorer.py` logs zero-result queries.

All sources append to `data/sessions/gaps.jsonl`.

## Stub generation

For each cluster, generate the wiki stub via Claude:

```
You are drafting a wiki stub for an undocumented company concept.
Below are 3 example questions people have asked about it; the existing
related concepts are also listed. Output a 5-section markdown stub:
overview, why it matters, key questions, related concepts, open
questions for the owner.

QUESTIONS:
- {q1}
- {q2}
- {q3}

RELATED CONCEPTS (with cluster):
- {c1} (course: {cluster_name1})
- {c2} (course: {cluster_name2})
```

Stub is `proposed`, not committed; needs human review.

## Suggested owner heuristic

For each gap cluster, look at the nearest existing concepts. The most
common author across their wiki notes' `last_author` git blame becomes
the suggested owner. Falls back to "no owner" if nothing nearby.

## UI: gaps tab in `feedback_panel.py`

- Table: question text · count · last seen · suggested cluster · suggested owner
- Click a row → expand to show all candidates + stub draft + "create note" button (writes the stub to the vault as a draft).
- Filter by source, severity, age, cluster.
- Weekly cron sends the digest to a designated Slack channel.

## Acceptance checks

- [ ] Seed `gaps.jsonl` with 20 synthetic questions; clusterer produces ≤8 clusters with sensible groupings.
- [ ] Each cluster's `stub_markdown` is non-empty and references at least one related concept by name.
- [ ] `feedback_panel.py` renders the gaps tab without errors.
- [ ] `scripts/gap_report.py --since=7d` writes a markdown digest to `data/sessions/gap_report_*.md`.
- [ ] Suggested-owner heuristic returns a non-null author for ≥60% of clusters whose nearest concepts have git history.

## Risks

- Noise: low-quality questions (typos, off-topic) clog the queue. Drop candidates with `len(text) < 20` and require >1 occurrence before clustering.
- PII: questions in Slack often contain personal context. When the Slack connector lands in Phase 5, strip emails/names before clustering and storing.
- Owner suggestions can be wrong / stale — show them as "suggested" not "assigned"; humans confirm.
