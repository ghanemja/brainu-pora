# Brain University — Roadmap

A prioritized punch list for turning Brain University from a working
prototype into a product that wows learners and doubles as a company-
knowledge cataloging tool. Each feature is scored on **impact** (1–5,
how much it moves the headline experience) and **effort** (1–5, eng-
weeks for one engineer with the existing stack). Higher impact and
lower effort sort to the top.

> Companion documents — read these before starting work on each item:
> - [`docs/plans/01_elevenlabs_tts_captions.md`](docs/plans/01_elevenlabs_tts_captions.md)
> - [`docs/plans/02_citation_grounded_qa_gate.md`](docs/plans/02_citation_grounded_qa_gate.md)
> - [`docs/plans/03_mastery_aware_traversal.md`](docs/plans/03_mastery_aware_traversal.md)
> - [`docs/plans/04_knowledge_gap_detector.md`](docs/plans/04_knowledge_gap_detector.md)

---

## Phase 0 — Now (already landed this iteration)

These shipped in the current branch as scaffolding. They are functional
but each has follow-ups noted in their module docstring. After the
worktree reconciliation (see [docs/RECONCILE.md](docs/RECONCILE.md))
the canonical pipeline now splits **script generation** (LLM) from
**rendering** (deterministic), to match the React-UI direction in
`design/`.

| Feature                          | Module(s)                                                          | What it does                                                                                       |
| -------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Concept-to-concept path tour     | `agents/path_finder.py`                                            | Pick any two nodes; get a weighted shortest path rendered as `TourStop`s with per-stop rationales. |
| NotebookLM-style podcast         | `agents/podcast_script.py` (script) + `agents/podcast_render.py` (mp3) | Source text → Claude → script JSON → voices.py per turn → stitched mp3.                            |
| TTS facade                       | `agents/voices.py`                                                 | Logical voice ids (`host_a` / `host_b` / `narrator`) routed across gTTS / pyttsx3 / ElevenLabs / OpenAI. |
| 3Blue1Brown-style scene pipeline | `agents/animation_script.py` (LLM spec) + `agents/lesson_to_scene.py` (lesson spec) + `agents/manim_renderer.py` (mp4) | SceneSpec JSON consumed by Manim and the React browser player.                                     |
| Live-graph reveal event stream   | `agents/live_graph.py`                                             | Free-text question → streaming sequence of `(action, payload)` events the UI replays as animation. |
| Cherry-picked partial features   | `agents/spaced_repetition.py` (Phase 3), `agents/voice_input.py` (Phase 6), `agents/difficulty.py` (Phase 4), `agents/citation_backtrack.py` (Phase 4 QA candidate), 14 others | Came in from the worktree merge — see RECONCILE.md.                                                |

---

## Phase 1 — Highest leverage (in progress)

These are the four items with detailed design docs in `docs/plans/`.
Each is high-impact and self-contained enough to ship independently.

| # | Feature                          | Status | Impact | Effort | Doc                                                                  |
| - | -------------------------------- | ------ | -----: | -----: | -------------------------------------------------------------------- |
| 1 | TTS facade (voices.py) + captions module | **shipped** | 5 | 2 | [01_elevenlabs_tts_captions.md](docs/plans/01_elevenlabs_tts_captions.md) — `voices.py` (worktree) + `captions.py` (new) |
| 2 | Citation-grounded QA gate        | **shipped** | 5 | 3 | [02_citation_grounded_qa_gate.md](docs/plans/02_citation_grounded_qa_gate.md) — `grounding.py` + `qa_gate.py` |
| 3 | Mastery-aware traversal (BKT)    | not started | 4 | 3 | [03_mastery_aware_traversal.md](docs/plans/03_mastery_aware_traversal.md) — note: worktree `spaced_repetition.py` overlaps |
| 4 | Knowledge-gap detector           | not started | 4 | 2 | [04_knowledge_gap_detector.md](docs/plans/04_knowledge_gap_detector.md) |

**Still missing for Plan 01** (TTS + captions): Whisper word-timestamp
end-to-end (have the function in `captions.py`; needs to be wired into
`video_generator.py`), and SSML/burn-in captions on the PIL renderer.
**Still missing for Plan 02** (QA gate): pipeline hook in
`curriculum.py` so newly-generated lessons run the gate automatically
before being cached; review-queue surface in the React UI.

**Why these four first:** narration quality is the single biggest "this
feels modern vs 2014" gap (#1); shipping any generated content into a
company-knowledge context without grounding is a liability (#2);
mastery-aware traversal is what separates an "edu-tainment" tour from a
real learning tool (#3); the gap detector is what turns Brain University
from a passive cataloging tool into one that actively grows the wiki
(#4).

---

## Phase 2 — Video & podcast polish (weeks 5–8)

Build on the Phase 0 scaffolding so the generated artifacts are
genuinely shareable.

| Feature                              | Impact | Effort | Notes                                                                                       |
| ------------------------------------ | -----: | -----: | ------------------------------------------------------------------------------------------- |
| Manim "graph walk" template          |   4    |   2    | One reusable Manim scene that animates the cluster + the lesson tour's path through it.     |
| Whisper word-level timestamps        |   3    |   1    | Sidecar `.json` of `{word, t_start, t_end}` per video → click-to-jump player.               |
| Pause-and-quiz interactive layer     |   4    |   3    | Player overlays a 1-question check between key ideas; result feeds into RL feedback.        |
| Podcast: real LLM-written script     |   4    |   1    | Replace the deterministic interview scaffold with a Claude pass that writes a real dialog.  |
| Podcast: ducking + intro/outro music |   2    |   1    | Background bed under speech, ducked when either host talks. ffmpeg sidechain.               |
| Avatar narrator (HeyGen / D-ID)      |   3    |   4    | Optional branded "BU professor" avatar for marketing videos. Cost-gate behind env flag.     |

---

## Phase 3 — Graph traversal & wow moments (weeks 9–14)

| Feature                                  | Impact | Effort | Notes                                                                                          |
| ---------------------------------------- | -----: | -----: | ---------------------------------------------------------------------------------------------- |
| Live-graph UI integration                |   5    |   3    | Wire `agents/live_graph.py` into `wiki_explorer.py` as a streaming animation overlay.          |
| Spaced-repetition layer (FSRS)           |   4    |   2    | Interleave already-visited concepts into new tours by forgetting curve. Builds on BKT.         |
| Multi-objective scoring in `lesson_plan` |   4    |   2    | Mix pagerank + novelty + mastery + recency + goal into one configurable score.                 |
| Prerequisite vs associative edges        |   4    |   3    | Edge `kind` field; planner respects "X requires Y." LLM-pass to label existing edges.          |
| "Why am I here?" breadcrumbs             |   3    |   1    | One-paragraph storyline of the last 5 stops on demand. Reuses tour-stop rationales.            |
| Diagnostic-test cold start               |   3    |   2    | 5-question quiz at session start → initialises mastery priors over the graph.                  |
| Embedding-based soft edges               |   3    |   2    | Sentence-transformer over note text adds latent edges Obsidian links missed.                   |

---

## Phase 4 — Quality assurance (weeks 9–14, parallel track)

| Feature                              | Impact | Effort | Notes                                                                                  |
| ------------------------------------ | -----: | -----: | -------------------------------------------------------------------------------------- |
| Multi-judge ensemble                 |   4    |   2    | Heuristic + 2 LLM judges; disagreement routes to human review queue.                   |
| Golden-set regression harness        |   4    |   2    | 20 manually-validated lessons; alert if any model/prompt change drops a score >10%.    |
| Reading-level + smell detector       |   3    |   1    | Flesch-Kincaid + vague-hedging-token frequency. Block publish if outside band.         |
| Cross-lesson consistency checker     |   3    |   3    | Flag contradictions between lessons in the same cluster. LLM entailment pass.          |
| Citation freshness & ownership flag  |   3    |   2    | Stale-source detection + "owner has left" yellow flag on the 3D graph.                 |
| Quiz-as-validation feedback loop     |   4    |   3    | Real learner quiz results back into per-lesson quality score.                          |
| Visual-slide lint (overflow, WCAG)   |   2    |   1    | Pre-encode check on every PIL-rendered slide.                                          |

---

## Phase 5 — Company-knowledge cataloging (weeks 15–24)

Turning the tool from "learning platform" into "company brain."

| Feature                          | Impact | Effort | Notes                                                                              |
| -------------------------------- | -----: | -----: | ---------------------------------------------------------------------------------- |
| Notion connector                 |   5    |   2    | Ingest Notion pages → wiki notes with stable backlinks.                            |
| Confluence connector             |   4    |   2    | Same shape as Notion.                                                              |
| Slack threads → candidate notes  |   4    |   3    | Question + accepted answer pairs become wiki stubs for review.                     |
| GitHub READMEs + ADRs            |   3    |   2    | Pull every `README.md`, `docs/**/*.md`, `*adr*.md` from selected repos.            |
| Meeting transcript → notes       |   4    |   4    | Loom / Zoom transcript → extract decisions + glossary terms.                       |
| Ownership graph                  |   4    |   2    | Each concept gets an owner; surfaces on graph as colour overlay.                   |
| Role-based onboarding paths      |   5    |   3    | New-hire tour generated from role + PARA bucketing + high-pagerank starts.         |
| Expertise edges (employee→concept) |   4  |   3    | Edges built from authorship + commits + Slack answers. "Who do I ask?" UI.        |
| Access controls + audit trail    |   4    |   3    | ACL per concept; lesson + video gated; full read log for compliance.               |
| Search inside video transcripts  |   3    |   2    | Whisper transcripts indexed in BM25 → timestamped results.                         |

---

## Phase 6 — Demo & "wow" surface area (weeks 20–26)

| Feature                          | Impact | Effort | Notes                                                                              |
| -------------------------------- | -----: | -----: | ---------------------------------------------------------------------------------- |
| Voice tutor (push-to-talk in player) |  5   |   3    | Hold-to-talk mid-lesson, ask clarifier, get grounded answer.                       |
| "Teach me X for an [audience]"   |   4    |   1    | Same source content, three pedagogical rewrites: exec / engineer / child.          |
| Multiplayer learning             |   3    |   4    | Overlay two learners' tours on the same graph in different colors.                 |
| Personal knowledge-twin export   |   3    |   2    | Subgraph of visited nodes + mastery shading; downloadable.                         |
| Podcast export at every level    |   3    |   1    | Already scaffolded — just expose UI buttons everywhere a lesson exists.            |
| Disagreement view                |   3    |   3    | Where do two sources contradict? Surface as a "discuss" widget.                    |

---

## Phase 7 — Robustness & operations (continuous)

These are not flashy and they don't ship in a single sprint. They
should be running in the background of every other phase.

| Feature                          | Impact | Effort | Notes                                                                              |
| -------------------------------- | -----: | -----: | ---------------------------------------------------------------------------------- |
| Move video gen to task queue     |   4    |   2    | RQ / Dramatiq / Celery; retries; DLQ; per-task observability.                      |
| Pydantic schemas on lesson dicts |   3    |   1    | Replace `dict` with `Lesson(BaseModel)`; silent typos go away.                     |
| OpenTelemetry traces             |   3    |   2    | Span per agent turn, per slide render, per TTS call.                               |
| Cost guardrails                  |   4    |   1    | Per-session + per-day spend caps; graceful degradation to heuristic synth.         |
| Health endpoint                  |   2    |   1    | Probes every dep in `stack_ready()` + Anthropic + FalkorDB. Surfaces broken pieces.|
| Snapshot + restore               |   3    |   2    | `make snapshot` for graph, FalkorDB, RL state, lesson cache.                       |
| Sandboxed markdown render        |   3    |   1    | Strip embedded HTML from untrusted Obsidian content.                               |
| Versioned lessons + rollback     |   3    |   2    | `lesson_v3.json` style; diff & roll-back across prompt iterations.                 |

---

## Scoring rubric

- **Impact 5** = headline demo moment, single feature noticeably moves NPS.
- **Impact 4** = enables a whole new use case (e.g. company knowledge).
- **Impact 3** = clear quality lift but not a new capability.
- **Impact 2** = polish or operational hygiene.
- **Impact 1** = nice-to-have.

- **Effort 1** = ≤ 2 days for one engineer.
- **Effort 2** = ≈ 1 week.
- **Effort 3** = ≈ 2 weeks.
- **Effort 4** = ≈ 3–4 weeks.
- **Effort 5** = quarter-scale.

---

## Open questions to resolve before Phase 5

1. Where does company-private content live in the repo vs an external vault?
2. Auth model — SSO from day one, or build-and-bolt-on?
3. Tenant isolation — single DB with row-level scoping, or one FalkorDB per org?
4. Audit-log retention policy — 90 days, 1 year, indefinite?
5. Which connectors are "must ship in v1" vs "post-v1"? (See Phase 5 table.)
