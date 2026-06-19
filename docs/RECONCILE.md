# Worktree Reconciliation — trusting-hopper-857eaa → main

**Date:** 2026-05-25
**Trigger:** discovered `.claude/worktrees/trusting-hopper-857eaa/`
contains 20 new agent modules + an `api/` server that overlap with the
four modules just landed on main (`path_finder.py`,
`podcast_generator.py`, `video_manim.py`, `live_graph.py`).

The worktree is at the same git commit as main (`ba110d5`) and every
file that exists in both is byte-identical. The worktree is purely
additive: the merge is mechanical for non-overlapping files and a
design call for the three overlap pairs.

---

## Cherry-pick plan (non-overlapping new files)

These have no equivalent on main and are copied as-is.

### Agents
- `agents/animation_script.py`     — Claude → SceneSpec JSON
- `agents/arxiv_ingest.py`         — arXiv ingestion (Arxivis pillar)
- `agents/audio_briefing.py`       — daily audio briefing
- `agents/citation_backtrack.py`   — Phase 4 QA candidate
- `agents/code_extractor.py`       — code-snippet extraction
- `agents/confusion.py`            — learner confusion signals
- `agents/cross_paper_synthesis.py` — multi-paper synthesis
- `agents/difficulty.py`           — Phase 4 QA item (difficulty calibration)
- `agents/heatmap.py`              — engagement heatmap
- `agents/interactive_podcast.py`  — interactive (pause-to-ask) podcast
- `agents/paper_drop.py`           — paper-onboarding flow
- `agents/persistence.py`          — session persistence
- `agents/podcast_video.py`        — podcast + visual sync
- `agents/remediation.py`          — when a learner gets stuck
- `agents/socratic.py`             — Socratic question generator
- `agents/spaced_repetition.py`    — Phase 3 roadmap item (FSRS)
- `agents/time_travel.py`          — replay a session at a past timestamp
- `agents/voice_input.py`          — Phase 6 wow item (voice tutor)

### API
- `api/__init__.py`
- `api/server.py`  (690 lines — FastAPI? — needs read; surface of the React UI)

### Worktree-canonical overlap files (also cherry-picked)
- `agents/voices.py`         → adopted as canonical TTS facade
- `agents/podcast_script.py` → adopted as canonical podcast-script generator
- `agents/manim_renderer.py` → adopted as canonical Manim renderer

---

## Reconciliation per overlap pair

### A. TTS facade

**Files:** `agents/voices.py` (worktree, 183 lines) vs the unwritten
`agents/tts.py` I'd been about to build per `docs/plans/01_*`.

**Decision: adopt `voices.py`.** It already implements all four
backends (gTTS, pyttsx3, ElevenLabs, OpenAI) with a clean logical-voice
abstraction (`host_a` / `host_b` / `narrator`) routed via a per-backend
`VOICE_MAP`. My `podcast_generator.py` was already coded against an
`agents.tts.synthesize(...)` facade — that call now routes to
`voices.synthesize(text, voice_id, out_path)` instead. Plan 01 stays
relevant: SSML support, captions, and Whisper word-timestamps still
need to be added on top of `voices.py`.

### B. Podcast generation

**Files:** `agents/podcast_script.py` (worktree, 239 lines) vs my
`agents/podcast_generator.py` (470 lines).

**Decision: keep both, split responsibilities.**

- **Worktree's `podcast_script.py`** stays canonical for *script
  generation* (Claude → JSON with chapters, visual cues, speaker A/B,
  callbacks, hook beats, length variants). It has caching, validation,
  and source builders for wiki / paper / cluster. Better than my
  deterministic scaffold.

- **My `podcast_generator.py` → renamed `podcast_render.py`.**
  Repurposed as the *renderer*: given a script (worktree shape OR
  legacy dict), call `voices.synthesize()` per turn, stitch with
  `pydub` / ffmpeg fallback, mix in optional music bed, write to
  `data/sessions/media/podcast_<hash>.mp3`. The scaffold dialog planner
  I wrote (`plan_dialog`) stays as a no-LLM fallback when the
  worktree script generator can't reach Claude.

The pipeline becomes:

```
lesson dict  ─┬─►  podcast_script.generate_script()    [Claude]
              │                  │
              │                  ▼
              │            script dict (worktree shape)
              ▼                  │
podcast_render.plan_dialog       │   ◄─ fallback when LLM unavailable
              │                  │
              └────────►  podcast_render.render(script) ──► mp3
                                                       │
                                          voices.synthesize per turn
```

### C. Manim / video generation

**Files:** `agents/animation_script.py` + `agents/manim_renderer.py`
(worktree, 136 + 191 lines) vs my `agents/video_manim.py` (440 lines).

**Decision: keep both, split responsibilities.**

- **Worktree pair stays canonical for the SceneSpec → mp4 pipeline.**
  `animation_script.py` is Claude → SceneSpec JSON; `manim_renderer.py`
  is SceneSpec → Manim `.py` → mp4. The SceneSpec is also consumed by
  `design/animation-player.jsx` for a browser SVG renderer, so the data
  shape is load-bearing for the React UI direction.

- **My `video_manim.py` → renamed `lesson_to_scene.py`.** Repurposed
  as a *brain-uni-lesson → SceneSpec adapter*: given a brain-uni lesson
  dict (with `title`, `key_ideas`, `worked_example`, `tour_path`,
  etc.), emit a SceneSpec JSON the worktree renderer can consume. The
  three scene archetypes I wrote (`TitleAndIdeasScene`,
  `EquationDerivationScene`, `GraphWalkScene`) become three "scene
  templates" — each one expands into a sequence of SceneSpec beats.

The pipeline becomes:

```
lesson dict ──► lesson_to_scene.lesson_to_spec()  ──► SceneSpec JSON
                                                       │
                                                       ▼
                                       manim_renderer.render(spec)
                                                       │
                                                       ▼
                                                     mp4
```

For browser playback, `design/animation-player.jsx` consumes the same
SceneSpec JSON directly — no mp4 needed for the React side.

---

## Files I'm not removing / renaming

| Mine                  | Verdict     | Why                                    |
| --------------------- | ----------- | -------------------------------------- |
| `agents/path_finder.py` | Keep as-is | No worktree equivalent. New territory. |
| `agents/live_graph.py`  | Keep as-is | No worktree equivalent. New territory. |
| `scripts/demo_new_features.py` | Update | Adjust imports to new canonical names. |
| `docs/plans/01..04*.md` | Keep with footnotes | Designs still valid; add a note pointing at voices.py as the starting point for plan 01. |
| `ROADMAP.md` | Update | Re-map Phase 0 ("done") to new module names; mark spaced_repetition + voice_input + difficulty as partially shipped in Phase 3/4/6. |

---

## What the user gets after this reconciliation

A clean `main` with:

- 18 brand-new agent modules cherry-picked from the worktree
- A canonical TTS facade (`voices.py`)
- A canonical podcast pipeline split into script generation
  (`podcast_script.py`) + rendering (`podcast_render.py`)
- A canonical SceneSpec pipeline split into spec generation
  (`animation_script.py` for Claude, `lesson_to_scene.py` for lesson
  dicts) + rendering (`manim_renderer.py`)
- An `api/` server they can build the React UI against
- Updated docs that describe the actual current state of the repo

After reconciliation, the original Phase 1 priorities (TTS facade, QA
gate) become **incremental builds on top of `voices.py` and a fresh
`grounding.py` / `qa_gate.py`** — instead of duplicating work that's
already shipped.
