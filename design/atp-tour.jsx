/* global React */

const { useState: useAtpTourState, useEffect: useAtpTourEffect } = React;

// ─────────────────────────────────────────────────────────────────
// ATP TOUR — agent-view onboarding (docs/HARDENING.md Phase 6)
//
// Modeled on tutorial.jsx (the human-view walkthrough): slides with
// icon/tag/title/body, a [data-nav] spotlight ring on the tab each
// slide describes, live navigation behind the card via onPreview,
// and a localStorage first-visit gate. Auto-opens on the first
// agent-view visit; the topbar "?" button reopens it in agent view
// (the same button opens the human tutorial in human view — wired
// in Brain University.html).
//
// The flag is DISTINCT from the human tutorial's "bu.tutorial.seen.v1"
// so each view gets its own first-run moment.
// ─────────────────────────────────────────────────────────────────

const ATP_TOUR_FLAG = "atp.tour.seen.v1";

// Gold — the agent view's institutional accent (matches atp-atoms).
const ATP_TOUR_ACCENT = "var(--c-cert, #e8c268)";

// Highlight ids MUST match SCREENS_AGENT ids in Brain University.html
// (university/agents/certs/marketplace/governance/vault) — that is what
// the [data-nav] spotlight query resolves against.
const ATP_TOUR_SLIDES = [
  {
    icon: "🎓",
    tag: "00 · WELCOME",
    title: "A university — and a standards body — for agents.",
    body:
      "The agent view is two institutions in one. A university that trains and " +
      "examines AI agents, layer by layer. And a standards body — ATP — that " +
      "publishes exactly what every certification means. Every seal, level and " +
      "claim you'll see resolves to a public, citable standard.",
    cta: "Show me the campus",
  },
  {
    icon: "▲",
    tag: "01 · UNIVERSITY",
    title: "Seven layers, one pyramid.",
    body:
      "The certification pyramid runs L1 (core reasoning) to L7 (autonomous " +
      "operations). Each layer is a versioned blueprint — sections, weights, item " +
      "types, pass criteria — and no layer is skippable. The University page shows " +
      "the whole pyramid and exactly which agents stand on which layer.",
    highlight: "university",
    tryIt: "university",
    cta: "See the pyramid",
  },
  {
    icon: "🤖",
    tag: "02 · AGENTS",
    title: "Every agent wears its record.",
    body:
      "Each profile is fully interpretable: a skill graph where untested skills stay " +
      "visible, certifications with an evidence trail behind every seal, a registrar's " +
      "report card — and failure transparency: the modes, rates and boundaries where " +
      "this agent breaks, published alongside every pass. Trust is the whole record, " +
      "not the highlight reel.",
    highlight: "agents",
    tryIt: "agents",
    cta: "Open the registry",
  },
  {
    icon: "◈",
    tag: "03 · CERTIFICATIONS",
    title: "Blueprints, not vibes.",
    body:
      "A certification is a versioned blueprint examined live against an item bank. " +
      "The judge model must come from a different model family than the candidate — " +
      "separation is enforced in code before any model is called — and every graded " +
      "item lands in a signed, append-only evidence chain anyone in your org can verify.",
    highlight: "certs",
    tryIt: "certs",
    cta: "Browse certifications",
  },
  {
    icon: "⇄",
    tag: "04 · MARKETPLACE",
    title: "Trust first, price second.",
    body:
      "Listings lead with certification level, evidence and failure modes — cost comes " +
      "after trust. And if the expert you need doesn't exist, compose one: pick a major, " +
      "a specialty and badges, and the university trains to order — the result is " +
      "examined and certified before it is ever listed.",
    highlight: "marketplace",
    tryIt: "marketplace",
    cta: "Visit the marketplace",
  },
  {
    icon: "🛡",
    tag: "05 · GOVERNANCE",
    title: "Tiers of permission, humans in the loop.",
    body:
      "Every agent operates inside a permission tier — what it may and may not do, with " +
      "a sandbox to match. Human sign-off (HITL) is a first-class, auditable event: every " +
      "reward, override and revocation is logged append-only and feeds back into the " +
      "agent's standing. Oversight you can replay, not a checkbox.",
    highlight: "governance",
    tryIt: "governance",
    cta: "See governance",
  },
  {
    icon: "🗄",
    tag: "06 · VAULT-LD",
    title: "Institutional memory that compounds.",
    body:
      "Vault-LD keeps company knowledge in four linked planes — wiki, knowledge graph, " +
      "linked-data bindings, and a consolidation loop that writes what agents learn back " +
      "to the top. Playbooks are the certifiable unit, and you can upload your own " +
      "documents: they become org-scoped Vault pages and draft an L5 company-knowledge " +
      "exam for your SMEs to sign off.",
    highlight: "vault",
    tryIt: "vault",
    cta: "Open the vault",
  },
  {
    icon: "📜",
    tag: "07 · A CITABLE STANDARD",
    title: "“ATP-L5.company-ops@2026.1” means the same thing everywhere.",
    body:
      "That is the point of the standards body: a certification label you can cite in a " +
      "contract, an audit or a job posting — with the blueprint, the evidence chain and " +
      "the failure record one click behind it. Reopen this tour anytime from the ? " +
      "button in the top bar.",
    cta: "Start exploring",
  },
];

function ATPTour({ open, onClose, onJumpTo, onPreview }) {
  const [idx, setIdx] = useAtpTourState(0);

  useAtpTourEffect(() => {
    if (open) setIdx(0);
  }, [open]);

  // Guided tour: navigate the agent view to the screen each slide describes
  // so the user SEES it behind the card (tutorial.jsx pattern — onPreview
  // navigates WITHOUT closing).
  useAtpTourEffect(() => {
    if (!open || !onPreview) return;
    const s = ATP_TOUR_SLIDES[idx];
    if (s && s.highlight) onPreview(s.highlight);
  }, [open, idx]);

  // Spotlight: ring the [data-nav] tab for the current slide. Measured after
  // the navigation above settles.
  const [navRect, setNavRect] = useAtpTourState(null);
  useAtpTourEffect(() => {
    if (!open) { setNavRect(null); return; }
    const s = ATP_TOUR_SLIDES[idx];
    if (!s || !s.highlight) { setNavRect(null); return; }
    const measure = () => {
      const el = document.querySelector('[data-nav="' + s.highlight + '"]');
      setNavRect(el ? el.getBoundingClientRect() : null);
    };
    const id = setTimeout(measure, 140);
    window.addEventListener("resize", measure);
    return () => { clearTimeout(id); window.removeEventListener("resize", measure); };
  }, [open, idx]);

  useAtpTourEffect(() => {
    if (!open) return;
    const onKey = (e) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight") setIdx(i => Math.min(ATP_TOUR_SLIDES.length - 1, i + 1));
      if (e.key === "ArrowLeft")  setIdx(i => Math.max(0, i - 1));
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;
  const slide = ATP_TOUR_SLIDES[idx];
  const last  = idx === ATP_TOUR_SLIDES.length - 1;

  const markSeen = () => {
    try { localStorage.setItem(ATP_TOUR_FLAG, "1"); } catch {}
  };

  const finish = () => {
    markSeen();
    onClose();
    // Land back at the agent view's home, not on the last slide's screen.
    if (onJumpTo) onJumpTo("university");
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
        // Light dim only — the live agent view the tour points at must stay
        // visible behind the card (same treatment as the human tutorial).
        background: "linear-gradient(180deg, rgba(8,12,24,0.10) 40%, rgba(8,12,24,0.55) 100%)",
        display: "flex", alignItems: "flex-end", justifyContent: "center",
        padding: "24px 24px 40px",
        fontFamily: "var(--f-sans, system-ui)",
        pointerEvents: "none",   // live UI stays interactive; card re-enables below
      }}>
      {/* Spotlight ring around the nav tab this slide describes */}
      {navRect && (
        <div style={{
          position: "fixed",
          left: navRect.left - 6, top: navRect.top - 5,
          width: navRect.width + 12, height: navRect.height + 10,
          border: `2px solid ${ATP_TOUR_ACCENT}`, borderRadius: 10,
          boxShadow: `0 0 0 4px color-mix(in oklch, ${ATP_TOUR_ACCENT} 28%, transparent), 0 0 22px ${ATP_TOUR_ACCENT}`,
          pointerEvents: "none", zIndex: 501,
          transition: "left 220ms, top 220ms, width 220ms",
          animation: "pulseRing 1.4s infinite",
        }} />
      )}
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
          {ATP_TOUR_SLIDES.map((_, i) => (
            <div key={i}
              onClick={() => setIdx(i)}
              style={{
                flex: 1, height: 3, borderRadius: 2, cursor: "pointer",
                background: i <= idx ? ATP_TOUR_ACCENT : "color-mix(in oklch, var(--c-ink) 12%, transparent)",
                transition: "background 200ms",
              }} />
          ))}
        </div>

        <div style={{ padding: "28px 32px 8px" }}>
          <div style={{ fontSize: 34, marginBottom: 12 }}>{slide.icon}</div>
          <div className="t-tag" style={{
            color: ATP_TOUR_ACCENT, marginBottom: 8,
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
            margin: "0 0 18px",
            fontSize: 14.5, lineHeight: 1.6, color: "var(--c-ink-muted)",
          }}>
            {slide.body}
          </p>
          {slide.tryIt && (
            <button
              onClick={() => {
                markSeen();
                onClose();
                if (onJumpTo) onJumpTo(slide.tryIt);
              }}
              style={{
                marginBottom: 10,
                padding: "8px 14px", fontSize: 12.5, fontWeight: 600,
                background: `color-mix(in oklch, ${ATP_TOUR_ACCENT} 18%, transparent)`,
                color: ATP_TOUR_ACCENT,
                border: `1px solid ${ATP_TOUR_ACCENT}`,
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
            onClick={() => { markSeen(); onClose(); }}
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
              {idx + 1} / {ATP_TOUR_SLIDES.length}
            </div>
            <button
              onClick={next}
              style={{
                padding: "8px 18px", fontSize: 13, fontWeight: 600,
                background: ATP_TOUR_ACCENT, color: "var(--c-bg)",
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

function shouldAutoOpenAtpTour() {
  try { return !localStorage.getItem(ATP_TOUR_FLAG); } catch { return true; }
}

// window.ATPTour is the overlay component; the flag + first-visit check ride
// along as statics so the shell can gate auto-open (tutorial.jsx idiom).
ATPTour.TOUR_FLAG = ATP_TOUR_FLAG;
ATPTour.shouldAutoOpen = shouldAutoOpenAtpTour;
window.ATPTour = ATPTour;
