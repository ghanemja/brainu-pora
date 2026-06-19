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

const SLIDES = [
  {
    icon: "🧠",
    tag: "00 · WELCOME",
    title: "Brain University in 60 seconds.",
    body:
      "Pick a concept. Walk a 6-stop tour through the knowledge graph. Watch auto-generated 30-second video explainers. Build intuition by traversal, not lecture order. The graph re-weights itself based on what you click — your next visit is sharper.",
    cta: "Show me how",
  },
  {
    icon: "▲",
    tag: "01 · TRAILHEAD",
    title: "Start at the trailhead.",
    body:
      "Type any concept you're curious about — or accept the system's foundation recommendations ranked by graph centrality and your PARA bucket. Hit ▲ Begin to plan your tour.",
    highlight: "trailhead",
    cta: "Next",
  },
  {
    icon: "↘",
    tag: "02 · THE WALK",
    title: "Follow the planned tour.",
    body:
      "Six stops: start → deepen × 2 → bridge → deepen × 2 → capstone. Each card carries a paragraph explaining why we're going here next. Auto-generated video, interactive exercises, and a Socratic check-in at every stop.",
    highlight: "walk",
    cta: "Next",
  },
  {
    icon: "≈",
    tag: "03 · BRIDGE",
    title: "Cross-course bridges are the magic.",
    body:
      "Mid-tour, the system surfaces a 'bridge' to a related course — diff geo → information theory, graph theory → biology. Click ≈ Fork to splice it into your trail. This is how surprise connections become intuition.",
    highlight: "branch",
    cta: "Next",
  },
  {
    icon: "★",
    tag: "04 · SUMMIT + 05 · DASHBOARD",
    title: "Summit, then track your manifold.",
    body:
      "Finish a trail → Summit. The Dashboard shows where you've walked on the 3D brain, every trail journaled, and a transparent RL feedback panel (interest re-weighting, memory decay, lesson quality vs baseline — all in plain English).",
    highlight: "dashboard",
    cta: "Next",
  },
  {
    icon: "📄",
    tag: "08 · ARXIVIS",
    title: "arXivis: see a paper in 30 seconds.",
    body:
      "410+ academic papers projected onto the concept manifold. Each gets a video explainer showing the foundations the paper rests on, the new concepts it introduces, and the innovation it claims. + Ingest paper lets you drop any arXiv URL and watch the cascade live.",
    highlight: "arxivis",
    cta: "Next",
  },
  {
    icon: "◇",
    tag: "09 · OPEN PROBLEMS",
    title: "And finally — research gaps.",
    body:
      "Stale clusters (no recent papers), missing bridges (concepts that should connect but don't), and underexplored hubs. The system surfaces what hasn't been written yet. Use it to find your thesis topic.",
    highlight: "openprob",
    cta: "Got it",
  },
];

function Tutorial({ open, onClose, onJumpTo }) {
  const [idx, setIdx] = useTutState(0);

  useTutEffect(() => {
    if (open) setIdx(0);
  }, [open]);

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
        background: "rgba(8, 12, 24, 0.78)",
        backdropFilter: "blur(10px)",
        display: "grid", placeItems: "center", padding: 24,
        fontFamily: "var(--f-sans, system-ui)",
      }}>
      <div style={{
        width: "min(620px, 100%)",
        background: "var(--c-bg-elev)",
        border: "1px solid var(--c-line-strong)",
        borderRadius: 16,
        boxShadow: "0 24px 80px rgba(0,0,0,0.45)",
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
            {slide.title}
          </h2>
          <p style={{
            margin: "0 0 22px",
            fontSize: 14.5, lineHeight: 1.6, color: "var(--c-ink-muted)",
          }}>
            {slide.body}
          </p>
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
