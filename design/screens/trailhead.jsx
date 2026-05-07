/* global React, BU_DATA, BrainGraph3D, CourseChip, ShimmerCaption */

const { useState, useEffect, useRef } = React;

// ─────────────────────────────────────────────────────────────────
// SCREEN 1 — TRAILHEAD
// Full-bleed 3D graph + 5 ranked starting-point cards.
// ─────────────────────────────────────────────────────────────────

function Trailhead({ onPickStart, learner }) {
  const graphRef = useRef(null);
  const [hoverNode, setHoverNode] = useState(null);
  const [interest, setInterest] = useState(learner?.interest || "");

  // Auto-rotate hint copy
  const phase = hoverNode ? "explore" : "land";

  return (
    <div style={{
      position: "relative",
      height: "calc(100vh - 56px)",
      width: "100%",
      overflow: "hidden",
    }}>
      {/* 3D graph fills the whole canvas */}
      <div style={{ position: "absolute", inset: 0 }}>
        <BrainGraph3D
          ref={graphRef}
          showLabels="hubs"
          cinematic={true}
          onNodeHover={setHoverNode}
          onNodeClick={node => {
            if (node) onPickStart?.(node.id, node.cluster);
          }}
          background="var(--c-bg)"
        />
      </div>

      {/* Top-center overlay copy */}
      <div className="fade-in" style={{
        position: "absolute", top: 28, left: "50%", transform: "translateX(-50%)",
        textAlign: "center", pointerEvents: "none",
        maxWidth: 720,
      }}>
        <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>
          BRAIN UNIVERSITY · TRAILHEAD
        </div>
        <h1 className="t-display" style={{
          margin: 0,
          textShadow: "0 4px 32px rgba(10,14,34,0.9)",
        }}>
          {phase === "land"
            ? <>This is the brain.<br/><span style={{ color: "var(--c-here)" }}>Pick a peak.</span></>
            : <ShimmerCaption text={hoverNode?.name || ""} />}
        </h1>
        <div className="t-cap" style={{
          marginTop: 12, fontFamily: "var(--f-mono)",
          color: "var(--c-ink-muted)", letterSpacing: "0.06em",
        }}>
          {phase === "land"
            ? `${BU_DATA.NODES.length} concepts · ${BU_DATA.CLUSTERS.length} courses · ${BU_DATA.EDGES.length} connections`
            : `${BU_DATA.CLUSTERS[hoverNode.cluster]?.name} · degree ${hoverNode.degree} · click to begin walk`}
        </div>
      </div>

      {/* Bottom-left interest field */}
      <div className="slide-up" style={{
        position: "absolute", bottom: 24, left: 24,
        zIndex: 5, maxWidth: 380,
      }}>
        <div style={{
          background: "color-mix(in oklch, var(--c-bg-elev) 75%, transparent)",
          backdropFilter: "blur(12px)",
          border: "1px solid var(--c-line)",
          borderRadius: "var(--r-lg)",
          padding: 12,
        }}>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 6 }}>
            WHAT INTERESTS YOU?
          </div>
          <input
            value={interest}
            onChange={e => setInterest(e.target.value)}
            placeholder="rocket aerodynamics · graph algorithms for path planning"
            style={{
              width: "100%", padding: "8px 10px",
              background: "var(--c-bg-elev-2)",
              border: "1px solid var(--c-line)",
              borderRadius: "var(--r-md)",
              color: "var(--c-ink)",
              fontFamily: "var(--f-sans)", fontSize: 13,
              outline: "none",
            }}
          />
          <div className="t-cap" style={{ marginTop: 6, color: "var(--c-ink-dim)" }}>
            Drives lesson framing + reorders the start-here list.
          </div>
        </div>
      </div>

      {/* Right rail — start-here cards */}
      <div className="slide-up" style={{
        position: "absolute", top: 92, right: 24, bottom: 24,
        width: 360, display: "flex", flexDirection: "column", gap: 10,
        zIndex: 5,
      }}>
        <div style={{
          display: "flex", justifyContent: "space-between", alignItems: "baseline",
          padding: "0 4px",
        }}>
          <h2 className="t-h2" style={{ margin: 0 }}>Start here</h2>
          <span className="t-tag" style={{ color: "var(--c-ink-muted)" }}>
            FOUNDATION INDEX
          </span>
        </div>
        <div style={{
          flex: 1,
          display: "flex", flexDirection: "column", gap: 10,
          overflowY: "auto", paddingRight: 4,
        }}>
          {BU_DATA.FOUNDATION_PICKS.map((p, i) => (
            <StartCard key={p.raw} pick={p} idx={i}
                       onHover={() => graphRef.current?.focusOn(p.raw, 70)}
                       onClick={() => onPickStart?.(p.raw, p.cluster)} />
          ))}
        </div>
      </div>

      {/* Bottom hint */}
      <div style={{
        position: "absolute", bottom: 18, left: "50%", transform: "translateX(-50%)",
        display: "flex", gap: 14, alignItems: "center",
        background: "color-mix(in oklch, var(--c-bg-elev) 70%, transparent)",
        backdropFilter: "blur(10px)",
        border: "1px solid var(--c-line)",
        borderRadius: 999,
        padding: "6px 14px",
        pointerEvents: "none",
      }}>
        <span className="t-cap" style={{ color: "var(--c-ink-muted)", display: "flex", alignItems: "center", gap: 6 }}>
          <span className="kbd">drag</span> orbit
          <span className="kbd">scroll</span> zoom
          <span className="kbd">click</span> peak
        </span>
      </div>
    </div>
  );
}

function StartCard({ pick, idx, onHover, onClick }) {
  const [hovered, setHovered] = useState(false);
  const c = BU_DATA.CLUSTERS[pick.cluster];
  return (
    <div
      onMouseEnter={() => { setHovered(true); onHover?.(); }}
      onMouseLeave={() => setHovered(false)}
      onClick={onClick}
      style={{
        background: "color-mix(in oklch, var(--c-bg-elev) 88%, transparent)",
        backdropFilter: "blur(12px)",
        border: `1px solid ${hovered ? c.color + "88" : "var(--c-line)"}`,
        borderRadius: "var(--r-lg)",
        padding: 14,
        cursor: "pointer",
        transition: "border-color 160ms, transform 160ms",
        transform: hovered ? "translateX(-3px)" : "translateX(0)",
        position: "relative",
        animationDelay: `${idx * 60}ms`,
      }}
      className="slide-up"
    >
      {/* Rank pill — sits INSIDE the card so it never gets clipped by the
          right-rail's vertical scroll container.  Was previously at
          left:-10 which stuck it outside; the rail clipped to overflow:hidden
          and the pill became "1, 2, 3" cut down to "_, _, _" depending on
          padding.  Now lives at left:14 with the title pushed to make room. */}
      <div style={{
        position: "absolute", left: 14, top: 14,
        width: 24, height: 24, borderRadius: "50%",
        background: c.color, color: "white",
        display: "grid", placeItems: "center",
        fontFamily: "var(--f-mono)", fontSize: 11, fontWeight: 700,
        boxShadow: "0 1px 2px rgba(0,0,0,0.18)",
        zIndex: 1,
      }}>{idx + 1}</div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", paddingLeft: 36 }}>
        <h3 style={{
          margin: 0, fontSize: 17, fontWeight: 600,
          fontFamily: "var(--f-sans)", letterSpacing: "-0.01em",
        }}>{pick.name}</h3>
        <div style={{
          fontFamily: "var(--f-mono)", fontSize: 13, fontWeight: 600,
          color: c.color,
        }}>{pick.score.toFixed(2)}</div>
      </div>
      <div style={{ marginLeft: 36, marginTop: 6 }}>
        <CourseChip clusterId={pick.cluster} />
      </div>
      <p className="t-cap" style={{ margin: "8px 0 0 36px", color: "var(--c-ink-muted)", fontSize: 12.5, lineHeight: 1.45 }}>
        {pick.rationale}
      </p>
      <div style={{
        marginLeft: 36, marginTop: 10,
        display: "flex", gap: 6, flexWrap: "wrap",
        fontFamily: "var(--f-mono)", fontSize: 10.5,
        color: "var(--c-ink-dim)",
      }}>
        <span>⛓ {pick.metrics.degree}</span>
        <span>· 🌉 {pick.metrics.span}</span>
        <span>· 📚 {pick.metrics.size}</span>
        {pick.metrics.hasWiki && <span>· 📄 wiki</span>}
        {pick.metrics.rl > 0 && <span style={{ color: "var(--c-summit)" }}>· ★ +{pick.metrics.rl.toFixed(2)}</span>}
      </div>
    </div>
  );
}

window.Trailhead = Trailhead;
