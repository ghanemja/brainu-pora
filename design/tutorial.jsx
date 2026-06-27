/* global React */

const { useState: useTutState, useEffect: useTutEffect } = React;

// ─────────────────────────────────────────────────────────────────
// TUTORIAL — first-time welcome walkthrough
//
// Auto-opens on first visit (localStorage flag); reopened from the
// "?" button in the topbar. Six slides match the user's actual
// journey through the app, mapped onto the nav order.
// ─────────────────────────────────────────────────────────────────

const TUT_FLAG = "bu.tutorial.seen.v1";

// Live paper count off the bundled corpus (filled at module-load).
function _paperCount() {
  try { return (window.ARXIVIS?.papers || []).length || 0; } catch { return 0; }
}

const SLIDES = [
  {
    icon: "🧠",
    tag: "00 · WELCOME",
    title: "Brain University in 60 seconds.",
    body:
      "A self-paced learning system built on top of an LLM-curated knowledge graph. Pick a concept, walk a planned tour, watch 30-second video explainers, and let the system re-weight the graph based on what you actually click. Every tab in the top nav is a different way into the same brain.",
    cta: "Show me everything",
  },
  {
    icon: "▲",
    tag: "01 · TRAILHEAD",
    title: "Start at the trailhead.",
    body:
      "Type any concept you're curious about — or accept the foundation picks the system ranks by graph centrality. The 3D 'brain' on the right is the knowledge graph itself; foundation concepts are the high-betweenness nodes. ▲ Begin plans a 6-stop tour for you.",
    highlight: "trailhead",
    tryIt: "trailhead",
    cta: "Try the trailhead",
  },
  {
    icon: "↘",
    tag: "02 · THE WALK",
    title: "Follow the planned tour.",
    body:
      "Six stops: start → deepen ×2 → bridge → deepen ×1-2 → capstone. Each card carries a short rationale paragraph (\"why we go here next\") plus an interactive exercise that lets you play with the idea. Prev / Next moves you through; the 3D minimap shows progress.",
    highlight: "walk",
    tryIt: "walk",
    cta: "Open the walk",
  },
  {
    icon: "▣",
    tag: "02b · INTERACTIVE EXERCISES",
    title: "Each lesson has a playground.",
    body:
      "Spanning-tree builder, BFS step-through, approximation-ratio explorer — embedded canvas sims in 3blue1brown style: yellow vertices, color-coded selection, narrator captions. Click an edge to commit, watch the system tell you if it's valid. Click-to-play, not click-to-read.",
    highlight: "walk",
    cta: "Next",
  },
  {
    icon: "≈",
    tag: "03 · BRIDGE",
    title: "Cross-course bridges are the magic.",
    body:
      "Mid-tour, the system surfaces a 'bridge' to a related course — diff geo → information theory, graph theory → biology. Click ≈ Fork to splice it into your current trail. This is how surprise connections become intuition.",
    highlight: "branch",
    cta: "Next",
  },
  {
    icon: "★",
    tag: "04 · SUMMIT",
    title: "Reach the capstone.",
    body:
      "Finish a trail → Summit. Shows the path you walked across the brain, the concepts you touched, and offers options to start a new trail or open the dashboard.",
    highlight: "summit",
    cta: "Next",
  },
  {
    icon: "▦",
    tag: "05 · DASHBOARD",
    title: "Track your manifold + see the RL.",
    body:
      "Every trail journaled. 3D brain w/ amber-highlighted visited concepts. Plain-English RL panel — \"interest in Manifold concepts +34%\", \"memory of older sessions 92% kept / week\". Hover any number to see the math behind it.",
    highlight: "dashboard",
    tryIt: "dashboard",
    cta: "Open dashboard",
  },
  {
    icon: "💡",
    tag: "06 · PROPOSE",
    title: "Idea → graph response.",
    body:
      "Type any free-text idea or research question. The system finds matching concepts in the graph, traces shortest paths to surface bridge concepts you might not have considered, and writes a grounded paragraph you can use as a starting answer.",
    highlight: "propose",
    tryIt: "propose",
    cta: "Open Propose",
  },
  {
    icon: "◉",
    tag: "07 · 3D MODE",
    title: "Fly through the whole brain.",
    body:
      "Fullscreen WebGL force-directed graph w/ kind-aware coloring (wiki / defense / arXiv), always-on labels sized by degree, cinematic auto-orbit, signal-flow animation that mimics neural firing along edges. The map you've been walking lives here in full.",
    highlight: "explorer",
    tryIt: "explorer",
    cta: "Enter 3D mode",
  },
  {
    icon: "📄",
    tag: "08 · ARXIVIS",
    title: () =>
      `arXivis · ${_paperCount() || "260+"} papers, 30 seconds each.`,
    body:
      "Academic papers projected onto the concept manifold. Each paper gets a 30-second 9:16 video explainer: foundations it rests on, new concepts it introduces, then a 'what the paper teaches' diagram showing the innovation as linked concept nodes. Sort by composite, novelty, rigor, year. Filter by source: arXiv, NTRS, DTIC, OpenAlex.",
    highlight: "arxivis",
    tryIt: "arxivis",
    cta: "Open arXivis",
  },
  {
    icon: "▸",
    tag: "08b · INGEST + ON-DEMAND VIDEO",
    title: "Drop any arXiv URL, watch the cascade.",
    body:
      "+ Ingest paper opens a modal w/ a live SSE cascade: resolve → fetch metadata → Semantic Scholar enrichment (SPECTER2 embedding + TLDR + citations) → classify into nearest cluster → corpus add → 30s video. Papers without a cached video get a 'Generate 30s explainer (~10s)' button — multiprocess render, no pre-bake required.",
    highlight: "arxivis",
    cta: "Next",
  },
  {
    icon: "◇",
    tag: "09 · OPEN PROBLEMS",
    title: "Research gaps the brain surfaces.",
    body:
      "Three lenses: STALE CLUSTERS (corners w/ no recent papers), MISSING BRIDGES (high-degree concepts that should connect but don't co-activate), UNDEREXPLORED HUBS (foundations used by many papers but active in few). This is where a thesis topic hides.",
    highlight: "openprob",
    tryIt: "openprob",
    cta: "See open problems",
  },
  {
    icon: "⚙",
    tag: "10 · TWEAKS",
    title: "Themes, fonts, lesson layout.",
    body:
      "The gear icon in the bottom-right opens a Tweaks panel: palette (Night / Paper / Ocean), display font (Grotesk / Serif / Mono), lesson layout (Postcard / Split / Spread), cinematic auto-orbit on/off. Useful for matching the room you're presenting in.",
    cta: "Got it",
  },
];

function Tutorial({ open, onClose, onJumpTo, onPreview }) {
  const [idx, setIdx] = useTutState(0);

  useTutEffect(() => {
    if (open) setIdx(0);
  }, [open]);

  // Guided tour: as the user advances, navigate the app to the part each slide
  // describes (Trailhead → Walk → Bridge → …) so they SEE it behind the card,
  // instead of just reading cards. onPreview navigates WITHOUT closing.
  useTutEffect(() => {
    if (!open || !onPreview) return;
    const s = SLIDES[idx];
    if (s && s.highlight) onPreview(s.highlight);
  }, [open, idx]);

  useTutEffect(() => {
    if (!open) return;
    const onKey = (e) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight") setIdx(i => Math.min(SLIDES.length - 1, i + 1));
      if (e.key === "ArrowLeft")  setIdx(i => Math.max(0, i - 1));
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;
  const slide = SLIDES[idx];
  const last  = idx === SLIDES.length - 1;

  const finish = () => {
    try { localStorage.setItem(TUT_FLAG, "1"); } catch {}
    onClose();
    if (last && slide.highlight && onJumpTo) onJumpTo(slide.highlight);
  };

  const next = () => {
    if (last) return finish();
    setIdx(i => i + 1);
  };

  return (
    <div
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
      style={{
        position: "fixed", inset: 0, zIndex: 500,
        // Light dim only — the live screen the tour is pointing at must stay
        // visible behind the card. A faint top→bottom gradient keeps the card
        // readable without blacking out the UI.
        background: "linear-gradient(180deg, rgba(8,12,24,0.10) 40%, rgba(8,12,24,0.55) 100%)",
        display: "flex", alignItems: "flex-end", justifyContent: "center",
        padding: "24px 24px 40px",
        fontFamily: "var(--f-sans, system-ui)",
        pointerEvents: "none",   // let the live UI stay interactive; card re-enables below
      }}>
      <div style={{
        pointerEvents: "auto",
        width: "min(620px, 100%)",
        background: "var(--c-bg-elev)",
        border: "1px solid var(--c-line-strong)",
        borderRadius: 16,
        boxShadow: "0 24px 80px rgba(0,0,0,0.55)",
        overflow: "hidden",
      }}>
        {/* Progress strip */}
        <div style={{ display: "flex", gap: 4, padding: "10px 22px 0" }}>
          {SLIDES.map((_, i) => (
            <div key={i}
              onClick={() => setIdx(i)}
              style={{
                flex: 1, height: 3, borderRadius: 2, cursor: "pointer",
                background: i <= idx ? "var(--c-bridge)" : "color-mix(in oklch, var(--c-ink) 12%, transparent)",
                transition: "background 200ms",
              }} />
          ))}
        </div>

        <div style={{ padding: "28px 32px 8px" }}>
          <div style={{ fontSize: 34, marginBottom: 12 }}>{slide.icon}</div>
          <div className="t-tag" style={{
            color: "var(--c-bridge)", marginBottom: 8,
            fontFamily: "var(--f-mono)", fontSize: 11, letterSpacing: "0.12em",
          }}>
            {slide.tag}
          </div>
          <h2 style={{
            margin: "0 0 14px",
            fontSize: 24, lineHeight: 1.25, letterSpacing: "-0.01em",
            color: "var(--c-ink)",
          }}>
            {typeof slide.title === "function" ? slide.title() : slide.title}
          </h2>
          <p style={{
            margin: "0 0 18px",
            fontSize: 14.5, lineHeight: 1.6, color: "var(--c-ink-muted)",
          }}>
            {slide.body}
          </p>
          {slide.tryIt && (
            <button
              onClick={() => {
                try { localStorage.setItem(TUT_FLAG, "1"); } catch {}
                onClose();
                if (onJumpTo) onJumpTo(slide.tryIt);
              }}
              style={{
                marginBottom: 10,
                padding: "8px 14px", fontSize: 12.5, fontWeight: 600,
                background: "color-mix(in oklch, var(--c-bridge) 18%, transparent)",
                color: "var(--c-bridge)",
                border: "1px solid var(--c-bridge)",
                borderRadius: 999, cursor: "pointer",
              }}>
              ▸ Try it now
            </button>
          )}
        </div>

        <div style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          padding: "14px 22px 22px",
          gap: 10,
        }}>
          <button
            onClick={() => {
              try { localStorage.setItem(TUT_FLAG, "1"); } catch {}
              onClose();
            }}
            style={{
              padding: "8px 14px", fontSize: 12,
              background: "transparent", color: "var(--c-ink-muted)",
              border: "none", cursor: "pointer",
              fontFamily: "var(--f-mono)", letterSpacing: "0.05em",
            }}>
            skip tour
          </button>

          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <button
              onClick={() => setIdx(i => Math.max(0, i - 1))}
              disabled={idx === 0}
              style={{
                padding: "8px 12px", fontSize: 13,
                background: "transparent",
                color: idx === 0 ? "var(--c-ink-dim)" : "var(--c-ink)",
                border: "1px solid var(--c-line)",
                borderRadius: 999,
                cursor: idx === 0 ? "not-allowed" : "pointer",
              }}>
              ← Back
            </button>
            <div style={{ fontSize: 11, color: "var(--c-ink-muted)", fontFamily: "var(--f-mono)" }}>
              {idx + 1} / {SLIDES.length}
            </div>
            <button
              onClick={next}
              style={{
                padding: "8px 18px", fontSize: 13, fontWeight: 600,
                background: "var(--c-bridge)", color: "var(--c-bg)",
                border: "none", borderRadius: 999,
                cursor: "pointer",
              }}>
              {slide.cta || (last ? "Done" : "Next →")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function shouldAutoOpenTutorial() {
  try { return !localStorage.getItem(TUT_FLAG); } catch { return true; }
}

window.Tutorial = Tutorial;
window.BUTutorial = { TUT_FLAG, shouldAutoOpenTutorial };
