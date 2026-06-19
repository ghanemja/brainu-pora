# Brain University — Objective Charter v1.0

> **This file is load-bearing.** Portfolio-adaptation routine scores proposed changes against this charter. Refined 2026-05-25 from chat-history intent capture; supersedes v0.1 stub.

---

## 1. North Star (one sentence)

**Turn the academic-paper backlog (arXiv + DTIC + NASA) into a guided 3D expedition: each paper projects into a constrained-concept 3D graph (Information-Theory-bounded — papers connect to existing nodes more often than add new ones), every concept node ships an auto-generated 30-second 3blue1brown / MathMotion-style algorithmic visualization + NotebookLM-style audio podcast, and the lesson-tour metaphor walks learners cluster-to-cluster so they grasp the *innovation* in a paper without reading it.**

Two products in one repo:
- **Brain University** (main): self-paced learning over the KG.
- **Arxivis** (`feature/arxivis` tab): arXiv-paper visualizer riding the same 3D graph + video pipeline — see through hype, identify pivotal publications.

Demo target: startup-fund pitch.

---

## 2. Pillars (priority order — earlier wins on conflict)

### Pillar 1 — JOURNEY METAPHOR (mountain expedition, not website)
Learner is protagonist walking a curated path. Every screen answers **"where am I?"** and **"where could I go next?"**.

**Passes if:**
- 3D mind map = primary navigation surface (full-screen on land, glowy clusters w/ distinct colors).
- Lesson tours = 5-8 stops w/ rationale per stop.
- Compass / mini-map visible at all times during tour.
- Side-trail option at every stop (jump to related cluster via bridge node).
- "Where you are" + "Where you could go" rendered explicitly, not implicit.

**Fails if:**
- UI degrades to flat list of articles.
- Tours auto-generated from flat ranking, not graph clusters.
- Learner can't see what's coming next.

### Pillar 2 — 30-SECOND COMPREHENSION
Paper's *innovation* (new algorithm, technique, insight) graspable ≤30s, no paper-read required.

**Passes if:**
- Auto-generated video per paper-node uses 3b1b / MathMotion visual language.
- Visualization shows the algorithm *itself* in motion, not summary text.
- Audio podcast variant (NotebookLM-style) generated alongside for ears-only consumption.
- Caption names contribution explicitly ("this paper introduces X by doing Y").
- Bench: ≥70% of users can name the contribution after 30s on a 50-paper benchmark.

**Fails if:**
- Videos are talking-head summaries (not algorithmic visualization).
- Learner needs to read paper to understand contribution.
- Visualizations are generic stock animation.

### Pillar 3 — INFORMATION-THEORETIC GRAPH PROJECTION
Each paper projects into the existing concept graph w/ constrained scope. Most papers connect existing nodes; few add new ones. This is the novelty signal.

**Passes if:**
- Paper-projection algorithm uses constrained concept set (paper rarely introduces wholly new concept, mostly recombines existing).
- "Highlights existing nodes" + "draws new edges" = primary output. "Adds new node" = rare, flagged as potential pivotal contribution.
- Pivotal-publication score derived from graph-topology centrality after projection.
- Paper lineage + reference network rendered as graph trails (citation paths).

**Fails if:**
- Every paper adds many new nodes (no compression signal, no novelty discrimination).
- Lineage / references invisible in UI.
- Pivotal-publication call is heuristic, not graph-derived.

### Pillar 4 — TEMPORAL EVOLVING GRAPH
KG evolves — connections form *and break* as system learns from learners, citations land, papers drop. Graphiti / FalkorDB temporal backend.

**Passes if:**
- Every edge has creation timestamp + last-reinforcement timestamp.
- Edges decay if not reinforced (citation count + learner traversal).
- New edges propose-and-merge w/ provenance trace (which paper / which learner introduced it).
- RL re-ranks node prominence from learner-feedback signal (thumbs + agent-lifecycle).
- Daily-updates routine ingests new arXiv batch + re-projects into graph.

**Fails if:**
- Graph static once built.
- No edge history.
- Re-ranking is hand-tuned heuristic.
- No daily ingestion cadence.

### Pillar 5 — EVIDENCE-GROUNDED + HYPE-FILTERED
Every concept node grounds in primary source. Hype claims separated from reproduced results.

**Passes if:**
- Each node has Sources tab — RAG / wiki / web cite per claim.
- Claims w/o source flagged.
- "Hype vs reproduced" tag on findings (paper-claim vs replication-confirmed).
- Corpus: arXiv + DTIC + NASA, all openly-redistributable.

**Fails if:**
- Concept text LLM-generated w/o citation.
- No paper-claim-vs-replicated distinction.
- Closed corpus.

---

## 3. Anti-goals

1. **Static knowledge graph.** Violates Pillar 4.
2. **Talking-head video summaries.** Violates Pillar 2 — need algorithmic visualization, not narrated bullets.
3. **Reading-list output.** "Here are 10 papers" defeats north star. Tour-first.
4. **Closed / paywalled corpus.** Must remain ingestable.
5. **Paywalled login for learner.** Free + local-first.
6. **Generic concept inflation.** Every paper adding many nodes = no novelty discrimination (violates Pillar 3).
7. **Researcher-only UX.** Aimed at curious learners + skim-readers, not domain experts who already know the field.

---

## 4. Decision framework

Score 0-3 per pillar (5 pillars). Sum ≥ 8 to proceed. Anti-goal violation = auto-REJECT.

Categorize: PIVOT / ARCHITECTURE_CHANGE / SUPPLEMENT / NEW_FEATURE / MONITOR / REJECT.

---

## 5. Metrics

| Metric | Target | Pillar |
|---|---|---|
| 30-sec comprehension rate (user names paper contribution after 30s video) | ≥70% on 50-paper bench | 2 |
| Tour completion rate | ≥60% (6-stop tour) | 1 |
| Side-trail-taken rate | ≥40% per session | 1 |
| Graph-projection compression (avg new nodes per paper) | <2.0 | 3 |
| Pivotal-publication precision (top-5% by centrality match curator list) | ≥80% | 3 |
| Edge churn rate (edges added + removed per week) | tracked, trending up early | 4 |
| Daily arXiv-ingestion latency (paper → projected node) | <24h | 4 |
| Source-grounding (% concept claims w/ valid cite) | 100% | 5 |
| Video generation latency per paper | <90s | 2 |
| Audio podcast latency per paper | <60s | 2 |
| Demo-pitch readiness (3-min live demo holds w/o crash) | shipped | strategic |

---

## 6. What Brain University is NOT

- Not a chatbot.
- Not a reading list.
- Not Obsidian (Obsidian = data layer, not product).
- Not a paper search engine.
- Not aimed at researchers — aimed at curious learners.
- Not text-summary-first — visualization + audio first.
- Not single-arXiv-domain — multi-corpus (arXiv + DTIC + NASA).

---

## 7. Open questions (resolve before next charter version)

- Arxivis = separate tab vs integrated? (Currently: `feature/arxivis` branch as a tab — decide if it ever merges to main or stays separate product.)
- Daily-arXiv-ingestion frequency: every 24h or every 6h?
- Edge-decay function shape (linear / exponential / Hebbian-by-traversal)?
- How to distinguish "pivotal" vs "popular" papers (centrality vs citation count)?
- Charter overlap w/ [[brainchamp]]'s wiki — share KG or separate?

---

*Charter owner: Janelle. v1.0 — refined from chat history 2026-05-25. Replaces v0.1 stub.*
