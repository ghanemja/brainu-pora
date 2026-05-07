# 🎓 Brain University — Design Brief

A prompt for the design team. Read before touching any pixels.

---

## The vision in one sentence

**Brain University turns a knowledge graph into a guided expedition** — the
learner is a protagonist walking a curated path through ideas, not a user
poking at a UI.

Plain Obsidian gives you static notes and a pretty 2D graph; Brain
University gives you *agency over a body of knowledge.* The graph is the
world; the learner is moving through it; every screen should answer two
questions at all times: **"where am I?"** and **"where could I go next?"**

---

## The journey metaphor (anchor everything to this)

Think of it as **trekking a mountain range**, not browsing a website.

| Trek concept | Brain University equivalent |
|---|---|
| Trailhead | Entry hero — the 3D mind map + auto-recommended starting peaks |
| Trail | Lesson Tour — a 6-stop pre-planned path with rationale per stop |
| Summit | A capstone concept that ties multiple ideas together |
| Compass | The "Where you are" mini-map (current node highlighted, visited dimmed) |
| Trail-marker | "Why we go here next" rationale card on each stop |
| Side-trail | Bridge nodes — chances to leave the planned route into a related course |
| Resupply point | Sources tab — where this concept is grounded (RAG / wiki / web) |
| Photograph | Auto-generated mp4 the learner can save and re-watch |
| Climbing buddy | The proposal responder — type any half-formed idea and the brain answers |
| Trail journal | Progress tab — what you've visited, what you still owe |

When in doubt about a screen: ask **"would a hiker want this here on the
mountain?"** If yes, ship it. If it's a UI thing a hiker wouldn't care
about, cut it.

---

## The first 90 seconds (onboarding tutorial)

This is the entire reason we're rebuilding the UI. Get this right and the
rest of the product carries itself.

### Beat 1 — *land*
- Full-screen 3D mind map auto-rotates slowly
- Labels glow on hub concepts only (so it doesn't look like text vomit)
- Single sentence overlay top-center: **"This is the brain. Pick a peak."**
- After 3 seconds: 5 ranked starting-point cards slide in from the right
  with brief rationale ("connects 7 courses · 129 concepts · evidence:
  arXiv 2603.21148")

### Beat 2 — *commit*
- Learner clicks one card → the 3D camera dives toward that node, locking
  on it as it pulses coral
- A 6-stop tour materializes as a faint glowing path through the graph
- Below the canvas: **"Your route is planned. 6 stops. ~30 min walk.
  Ready?"** with a single big primary button

### Beat 3 — *walk*
- Lesson view = postcard, not webpage. One concept, one screen.
  Title · summary · 3 key ideas · worked example with numbers · quiz.
- "Where you are" mini-map fixed in the bottom-right corner the whole
  walk — learner never wonders where they are in the bigger picture
- "Next stop" preview always visible — they always know what's coming

### Beat 4 — *branch*
- At any stop the learner can hit a **bridge** button — graph zooms
  out, shows the bridge edge to a related course, gives them the
  choice: "stay on the planned trail" or "fork into [Aerodynamics]"
- This is the key engagement moment. Curiosity is rewarded, not punished.
  The system re-plans the tour live from wherever they fork to.

### Beat 5 — *summit*
- Final stop = capstone concept that ties multiple themes together
- "You walked from X → Y → Z. The thread between them is W."
- Auto-generated mp4 of the whole walk drops as a download button
- Two next-step buttons: "another trail in this range" or "a totally
  different range"

---

## The user types

### 1. Curious autodidact (primary)
Drops in to learn one specific thing. Wants depth fast. Hates being
treated like a beginner. **Engagement loop: depth + cross-references.**

### 2. Teacher / TA (primary)
Wants to build a curriculum for their class. Walks the graph to
discover the *order* of concepts they should teach. Wants to export a
lesson plan and customize it. **Engagement loop: planning + export.**

### 3. Researcher (secondary)
Has a half-baked idea. Drops it into the Propose tab. Wants to see what
existing concepts touch it and what bridges might exist. **Engagement
loop: idea → connections → grounded synthesis.**

### 4. Curious lurker (secondary)
Wants to wander. Doesn't have a goal. Surprises themselves. **Engagement
loop: random + serendipity (the 'surprise me' button matters).**

Design every screen for #1. Don't break it for the others.

---

## Tone and voice

- **Confident, not cute.** This is a serious knowledge tool, not Duolingo.
  Avoid mascots, exclamation points, "let's go!" energy.
- **Specific, not generic.** Never write "Learn about graph theory."
  Always: "Graph theory · 47 concepts · prerequisites: set theory."
- **Show numbers.** Edge counts, cluster sizes, degree, score. Numbers
  build trust that the system actually understands the domain.
- **Quiet confidence in the graph.** The graph *is* the experience.
  The UI's job is to get out of the way. No spinner where a clear
  caption would do.
- **Caveman-style microcopy where compression helps.** Fragments OK
  when context makes them unambiguous. Drop articles. Be terse.
  *"Bridge to Aerodynamics via Reynolds number"* not *"You can bridge
  into the Aerodynamics course via the Reynolds number concept"*.

---

## Hard requirements

These are non-negotiable — if a design choice breaks one, it's wrong.

1. **The 3D graph is the home.** Any landing page that doesn't show the
   graph as the dominant element is wrong.
2. **Where am I? always answered.** A mini-map or breadcrumb visible
   at all times during a lesson.
3. **Why are we here? always answered.** Every navigation action shows a
   one-sentence rationale ("we go here because X bridges to Y").
4. **The tour is interruptible.** Every stop has a bridge / surprise /
   replan button. Linear lessons fail the curiosity user.
5. **Sources are surfaceable in one click.** Where did this claim come
   from? RAG / wiki / paper / web — reachable from every lesson card.
6. **Local-first.** Everything works without ANTHROPIC_API_KEY, without
   FalkorDB, without internet. Degraded mode must still feel polished,
   not error-screen.

---

## Anti-patterns to avoid

- ❌ A "course catalog" as the landing page (we already deleted this).
- ❌ Hamburger menus. Knowledge work is too rich for hidden affordances.
- ❌ Linear progress bars in a non-linear graph. The graph IS the progress.
- ❌ Cute mascots, gamification badges, streaks. This is not Duolingo.
- ❌ Centered modal dialogs. Use side panels instead — the graph stays
  visible behind them.
- ❌ "Loading…" spinners with no caption. Show what's loading and how
  many: *"Computing tour through 6 stops · finding bridge concepts…"*
- ❌ Hiding the graph behind a tab. The graph is always primary.
- ❌ Onboarding modals with multi-step wizards. The graph itself teaches
  the affordances — clicks are intuitive.

---

## Color & motion (current palette — feel free to evolve)

| Use | Hex | Meaning |
|---|---|---|
| Coral | `#F96167` | "you are here" / current node / active accent |
| Amber | `#FBB036` | visited / past / defense corpus |
| Sky | `#7DD3FC` | bridge / connection / cross-corpus / arXiv |
| Navy | `#0F1733` | background, deep space |
| Cluster cycle | 12 distinct colors | cluster identity (auto-derived from Louvain) |

Motion principles:
- Graph rotates slowly when idle (alive, not dormant)
- Camera dives ease-in-out (1.5–2s) on click — it's a *journey* between
  nodes, not a teleport
- Newly added nodes pulse once when they appear (the brain is growing)
- Transitions between tabs are slides, not fades — they're literal
  movements through the same world

---

## Specific UI moments to design

These are the screens that matter most. Mock these up first.

1. **Trailhead** (entry hero) — full-bleed 3D graph + 5 starting-point
   cards in a side rail
2. **The walk** (lesson view) — postcard layout, mini-map locked
   bottom-right, "next stop" preview top-right
3. **The branch point** (bridge prompt) — modal-side panel offering
   "stay on path" vs "fork to [course]"
4. **The summit** (capstone celebration) — recap card + auto-generated
   mp4 + two next-trail buttons
5. **The dashboard** (returning learner) — what trails you've walked,
   what's open, where you stopped
6. **The Propose moment** — input field that doesn't look like a search
   bar; results that read like a thoughtful colleague's reply
7. **The 3D-mode flex** — fullscreen viz with always-on labels +
   recordable camera tour. This is the demo screen for sales / shareables.

---

## What success looks like

A new user sees the graph, clicks one node, walks the auto-planned tour,
forks once into a related course, and comes out 25 minutes later able to
explain a real concept they didn't know coming in. They can point at the
graph and say *"I started over there, ended up over here, and the
connection between them is X"* — because the system showed them that
literal path.

If they screenshot the experience and post it on Twitter unprompted,
we won.

---

## What this repo is

- Functional Streamlit prototypes in `ui/` — they prove the data layer
  works end-to-end
- The Python data layer in `agents/` + `graph/` — this is the contract
  the new UI must call into
- Sample wiki notes in `wiki/concepts/` (20 of 1,217) — enough to demo
- Full setup + how-to-run in `README.md`

The Streamlit apps are *placeholders*. The new UI is whatever you build.
The Python modules don't change.
