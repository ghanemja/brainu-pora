# 🎓 Brain University

A self-paced learning architecture built on top of an LLM-curated knowledge
graph. Students enter through a 3D mind map, get auto-recommended starting
concepts, walk a planned lesson tour through clusters of related ideas,
watch auto-generated video explainers, take quizzes, and feed back into a
reinforcement-learning loop that re-ranks the graph for the next learner.

> **Status:** functional prototype. Hand-off candidate for UI/design polish.
> All apps run via `streamlit`. Data layer = local Python (Obsidian vault
> loader + optional Graphiti/FalkorDB temporal graph + BM25 indices).
>
> **👉 Designers: read [`DESIGN_BRIEF.md`](DESIGN_BRIEF.md) before touching pixels.**
> It explains the journey-through-the-graph metaphor, the first-90-seconds
> onboarding beats, the four user types, voice/tone, hard requirements,
> and the specific UI moments to mock up first.

---

## What's in here

```
ui/                        Streamlit apps (each runs independently)
  learning_app.py          → main "Brain University" student experience
  wiki_explorer.py         → PARA / Notes / Search / 3D graph / Propose
  feedback_panel.py        → RL feedback panel (thumbs / agent lifecycle)
  retrieval_inspector.py   → debug what each retriever surfaces

agents/                    Python data layer
  citations.py             parse [arxiv/...] / [[wiki/...]] tokens
  content_finder.py        unified RAG-first → web-fallback search
  curriculum.py            lesson-card generator (fast / Claude rich)
  feedback.py              RL feedback ingestion + reward shaping
  judge.py                 auto-judge (heuristic + LLM rubric)
  lesson_plan.py           pre-planned 6-stop tour through the graph
  lifecycle.py             agent EWMA / kill threshold / negative replay
  media.py                 YouTube search + TTS narration + slides HTML
  proposal_responder.py    text → matched concepts → grounded synthesis
  video_generator.py       PIL + gTTS + moviepy → mp4 lessons
  specialists.py           multi-domain Claude debate roster
  orchestrator.py          debate runner (with RL hooks)
  synthesizer.py           debate → final design proposal

graph/                     Knowledge-graph plumbing
  obsidian_loader.py       any folder of .md files → networkx graph
  clusters.py              Louvain communities = "courses"
  foundations.py           graph centrality + RL + PARA → "Start here"
  corpus_graph.py          mixes wiki + defense corpus + arXiv categories
  temporal_graph.py        thin Graphiti / FalkorDB wrapper (optional)
  weight_update.py         FalkorDB edge-weight CRUD for RL credit assignment

rag/                       BM25 retrieval
  weights.py               local paper/wiki priors (independent of FalkorDB)
  build_split_indices.py   per-domain BM25 builder

scripts/
  export_quartz_site.py    static-site exporter (3D graph + per-note pages)
  replay_sessions.py       offline replay of RL feedback events
  wiki_to_graphiti.py      ingest wiki into FalkorDB (optional)
  corpus_to_graphiti.py    ingest defense corpus into FalkorDB (optional)

eval/
  rl_eval.py               paired baseline-vs-RL eval harness

wiki/concepts/             20 sample wiki notes (full corpus is 1,217 — held
                            elsewhere; vault path is configurable)

docker/
  docker-compose.yml       FalkorDB container for the optional temporal graph
```

---

## Run

```bash
# 1. install deps
pip install -r requirements.txt

# 2. (optional) point at your Obsidian vault
export OBSIDIAN_VAULT="$HOME/Documents/MyVault"

# 3. (optional) Anthropic key for richer lessons + auto-judge LLM
export ANTHROPIC_API_KEY=sk-ant-...

# 4. (optional) start FalkorDB if you want temporal graph + entity extraction
cd docker && docker compose up -d && cd ..

# 5. launch any of the apps (each is independent)
streamlit run ui/learning_app.py    --server.port 8513   # student-facing
streamlit run ui/wiki_explorer.py   --server.port 8514   # PARA / 3D / Propose
streamlit run ui/feedback_panel.py  --server.port 8515   # RL admin
streamlit run ui/retrieval_inspector.py --server.port 8511   # debug

# OR build a static site
python3 scripts/export_quartz_site.py --serve --port 8516
```

Without any of the optional pieces, everything still works — just falls
back to the wiki-only graph + heuristic synthesis.

---

## Key concepts

### 1. Graph-as-curriculum
- **Clusters** (Louvain communities) = courses
- **High-degree nodes** = lesson candidates
- **Bridge nodes** = cross-course transfer credits
- **PARA bucketing** (Projects/Areas/Resources/Archives) = recommendation bias

### 2. Lesson Tour
A 6-stop traversal planned per learner: start → deepen 2× → bridge → deepen
1-2× → capstone. Each stop carries a paragraph rationale ("why we go here
next"). Walked via Prev / Next buttons; visualized as an animated path on
the 3D graph.

### 3. Engagement
- **Auto-generated mp4** per lesson (PIL + gTTS + moviepy → 1MB / 25s)
- **YouTube search** embed (no API key, public-page scrape)
- **HTML auto-slideshow** (instant, in-browser, optional TTS audio)
- **3D mind graph** (Three.js / WebGL via `3d-force-graph`) with
  - always-on labels (sized by degree)
  - camera-tour recording → downloadable .webm
  - kind-aware coloring (wiki / defense / arXiv)

### 4. Reinforcement learning
- Per-agent EWMA quality + bad-streak kill threshold
- Citation-based credit assignment to graph edges + paper-level priors
- Hebbian boost on user prompts (what you ask about strengthens)
- Eligibility-trace decay each session
- Auto-judge: heuristic (free) or Claude rubric (~1¢/turn)
- Paired eval harness: same prompts baseline vs RL-on, measure lift

### 5. Idea → graph response
The 💡 Propose tab takes any free-text idea, finds matching concepts in
the graph, traces shortest paths between them to surface bridge concepts,
and writes a grounded paragraph the learner can use as a starting answer.

### 6. arXivis — see the paper in 30 seconds (`feature/arxivis`)
Projects each paper (arXiv slice + DTIC + NTRS + OpenAlex) onto the
brain-university concept manifold. A paper is an **activation pattern**
over the existing graph, not a new island; the 3D viz animates the
exact concepts and edges it lights up, plus a 30-second elevator pitch.

- **Info-theoretic novelty** = concept rarity bits + new-edge bits + new-term bonus.
  Pivotal paper = high edge novelty + many later papers activate same set.
- **Daily brief**: `scripts/arxivis_daily_brief.py` filters to recent
  papers and re-ranks by novelty for the "what should I read today" slot.
- Build pipeline:
  ```bash
  python3 scripts/build_arxivis_data.py --max-per-cat 100 --keep-top 500
  python3 scripts/arxivis_daily_brief.py --top 10
  python3 scripts/render_arxivis_video.py --top 500   # 9:16 explainer per paper
  ```
  Output → `design/arxivis_data.js` + `design/arxivis_daily.js` consumed
  by the new **arXivis** tab in `design/Brain University.html`.

#### Research-assistant rigor scoring
Every paper is scored on the 10 criteria a careful reviewer would check
before quoting it (`agents/arxivis_rigor.py`):
1. Hierarchy of evidence — proof / RCT / meta-analysis vs descriptive
2. Preliminary findings — flag "pilot" / "initial" language
3. Correlation vs. causation — flag causal claims w/o controlled evidence
4. Confounding variables — credit ablations / controlled baselines
5. Conflicts of interest — industry affiliations, funding declared
6. Publication bias — preprint vs peer-reviewed venue (word-bounded match)
7. Replication — code/data release link extracted
8. Sample size — N=… / dataset count parsed from abstract
9. Relative vs. absolute risk — flag % improvement w/o absolute baseline
10. P-value — explicit p< vs hand-wavy "statistically significant"

Composite = `novelty_bits + rigor.total`. Default list ordering uses
composite; the UI also exposes a search input that re-ranks by relevance
to the query × composite (concept name + title + innovation phrase match).

#### Future — code-sandbox reproducibility
Next phase (not yet implemented): if a paper publishes a GitHub repo,
pull it into an ephemeral sandbox, run the README's reproduce script,
diff numbers against the paper's claimed results. Green-flag papers
whose claims reproduce; red-flag those that don't. This would close the
loop between "the paper says X" and "the code actually does X."

Corpus paths (symlinked from the gemma-engineering-ft fine-tune repo —
both gitignored):
  - `data/raw/arxiv/<cat>/*.txt` — 8,325 arXiv papers across 18 categories
  - `data/defense_corpus/MANIFEST.jsonl` — 2,081 DTIC/NTRS/OpenAlex/arXiv-defense records

---

## For UI / design hand-off

The Streamlit apps in `ui/` are intentionally functional, not polished.
The Python data layer in `agents/` + `graph/` is what matters: any UI
can call those modules and render however it likes. Suggested polish work:

1. **Theming** — `.streamlit/config.toml` w/ custom palette + fonts;
   integrate `streamlit-shadcn-ui` for nicer cards/badges
2. **Landing page** — Brain University intro / pricing / "what is this"
   (likely a static React/Tailwind page, separate repo)
3. **Onboarding flow** — first-time user picks interest, watches a
   30-second product tour, sees their first 3D graph
4. **Lesson card design** — current cards are functional Streamlit
   `st.container(border=True)`; redesign as proper cards w/ illustrations
5. **Mobile responsive** — Streamlit is desktop-first; consider a
   FastAPI + React migration if mobile is critical
6. **Brand identity** — name, logo, color system, type system

Color system used in code (palette to honour or replace):
- Coral `#F96167` (current location / accent)
- Amber `#FBB036` (visited / defense corpus)
- Sky `#7DD3FC` (bridges / cross-course / arXiv)
- Navy `#0F1733` (background)
- Cluster palette: 12 distinct colors cycled by Louvain cluster id

---

## License

Proprietary — see top-level repo for terms.
