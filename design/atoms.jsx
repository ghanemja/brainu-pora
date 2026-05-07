/* global React, BU_DATA */

// ── Shared atoms used across screens ─────────────────────────────

const { useState, useEffect, useRef, useMemo } = React;

// Topographic ridge SVG — used on dashboard & summit
function TopoRidge({ height = 80, layers = 4, opacity = 0.4 }) {
  const lines = [];
  const w = 1200;
  for (let layer = 0; layer < layers; layer++) {
    const baseY = height * 0.4 + layer * (height * 0.16);
    const amp = height * 0.18 - layer * 3;
    const points = [];
    for (let x = 0; x <= w; x += 12) {
      const y = baseY + Math.sin((x + layer * 130) * 0.012) * amp
                       + Math.sin((x + layer * 80) * 0.024) * (amp * 0.4);
      points.push(`${x},${y.toFixed(1)}`);
    }
    lines.push(<polyline
      key={layer}
      points={points.join(" ")}
      fill="none"
      stroke={`rgba(125,211,252,${(0.06 + layer * 0.04) * opacity * 2})`}
      strokeWidth={layer === layers - 1 ? 1.2 : 0.8}
    />);
  }
  return (
    <svg viewBox={`0 0 ${w} ${height}`} preserveAspectRatio="none"
         style={{ width: "100%", height, display: "block" }}>
      {lines}
    </svg>
  );
}

// Compass — agent identity / "where am I" hint
function Compass({ angle = 0, label = "N" }) {
  return (
    <div style={{
      width: 56, height: 56, borderRadius: "50%",
      border: "1px solid var(--c-line-strong)",
      background: "var(--c-bg-elev)",
      display: "grid", placeItems: "center",
      position: "relative", flexShrink: 0,
    }}>
      <div style={{
        position: "absolute", inset: 4, borderRadius: "50%",
        border: "1px dashed var(--c-line)",
      }} />
      <div style={{
        position: "absolute", top: 4, left: "50%", transform: "translateX(-50%)",
        fontSize: 8, fontFamily: "var(--f-mono)", color: "var(--c-ink-muted)",
      }}>N</div>
      <svg width="40" height="40" viewBox="-20 -20 40 40"
           style={{ transform: `rotate(${angle}deg)`, transition: "transform 800ms cubic-bezier(0.4,0,0.2,1)" }}>
        <polygon points="0,-14 4,4 0,1 -4,4" fill="var(--c-here)" />
        <polygon points="0,14 4,-4 0,-1 -4,-4" fill="var(--c-ink-dim)" opacity="0.5" />
      </svg>
      <div style={{
        position: "absolute", bottom: -18, left: "50%", transform: "translateX(-50%)",
        fontSize: 9, fontFamily: "var(--f-mono)", color: "var(--c-ink-muted)",
        letterSpacing: "0.08em", textTransform: "uppercase", whiteSpace: "nowrap",
      }}>{label}</div>
    </div>
  );
}

// Altitude / progress bar — for tour stops
function Altitude({ idx, total }) {
  const stops = Array.from({ length: total });
  return (
    <div className="altitude-strip" style={{ gap: 10 }}>
      <span>STOP</span>
      <span style={{ color: "var(--c-ink)", fontWeight: 600 }}>{idx + 1} / {total}</span>
      <span style={{ flex: 1 }} />
      <span>ELEV</span>
      <div className="alt-bar"><span style={{ width: `${((idx+1)/total)*100}%` }} /></div>
    </div>
  );
}

// Citation token row
function Evidence({ items = [] }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 6, alignItems: "center" }}>
      <span className="t-cap" style={{ color: "var(--c-ink-dim)" }}>EVIDENCE</span>
      {items.map((c, i) => (
        <span key={i} className="cite">[{c}]</span>
      ))}
    </div>
  );
}

// Course chip with dot
function CourseChip({ clusterId, size = "sm" }) {
  const c = BU_DATA.CLUSTERS[clusterId];
  if (!c) return null;
  const fontSize = size === "sm" ? 11 : 12;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      padding: size === "sm" ? "2px 8px" : "4px 10px",
      borderRadius: 999,
      border: `1px solid ${c.color}55`,
      background: `${c.color}11`,
      color: "var(--c-ink-muted)", fontSize, fontFamily: "var(--f-sans)",
    }}>
      <span style={{ width: 6, height: 6, borderRadius: 999, background: c.color }} />
      {c.name}
    </span>
  );
}

// Stop kind icon
function KindGlyph({ kind }) {
  const map = {
    start:    { sym: "▲", color: "var(--c-here)",    label: "START" },
    deepen:   { sym: "✕", color: "var(--c-visited)", label: "DEEPEN" },
    bridge:   { sym: "≈", color: "var(--c-bridge)",  label: "BRIDGE" },
    capstone: { sym: "★", color: "var(--c-summit)",  label: "SUMMIT" },
  };
  const m = map[kind] || map.deepen;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      fontFamily: "var(--f-mono)", fontSize: 10.5,
      letterSpacing: "0.1em", textTransform: "uppercase",
      color: m.color,
    }}>
      <span style={{ fontSize: 13, lineHeight: 1 }}>{m.sym}</span>
      {m.label}
    </span>
  );
}

// Mini-map — small SVG of the tour path
function MiniMap({ tour, idx, onJump }) {
  const w = 180, h = 140;
  if (!tour || tour.length === 0) return null;
  // Lay out tour stops in a winding path
  const pts = tour.map((stop, i) => ({
    x: 18 + (w - 36) * (i / (tour.length - 1 || 1)),
    y: h * 0.5 + Math.sin(i * 1.2) * h * 0.25,
    stop, i,
  }));
  const c = BU_DATA.CLUSTERS;

  // Path d-attr
  const d = pts.map((p,i) => i === 0 ? `M${p.x},${p.y}` : `L${p.x},${p.y}`).join(" ");

  return (
    <div style={{
      background: "var(--c-bg-elev)",
      border: "1px solid var(--c-line)",
      borderRadius: "var(--r-md)",
      padding: 10, width: w + 20, position: "relative",
    }}>
      <div style={{
        display: "flex", justifyContent: "space-between", alignItems: "center",
        marginBottom: 6,
      }}>
        <span className="t-tag" style={{ color: "var(--c-ink-muted)" }}>WHERE YOU ARE</span>
        <span className="t-mono" style={{ color: "var(--c-ink-dim)", fontSize: 10 }}>
          {idx + 1}/{tour.length}
        </span>
      </div>
      <svg viewBox={`0 0 ${w} ${h}`} width={w} height={h} style={{ display: "block" }}>
        {/* Topo backdrop */}
        {[0,1,2].map(layer => (
          <path key={layer}
            d={`M0,${h*0.55 + layer*8} ${Array.from({length: 10}).map((_,i) =>
              `L${i*w/10},${h*0.55 + layer*8 + Math.sin(i + layer)*6}`).join(" ")}`}
            stroke={`rgba(125,211,252,${0.12 - layer*0.03})`} strokeWidth="0.8" fill="none" />
        ))}
        {/* Path */}
        <path d={d} stroke="rgba(251,176,54,0.5)" strokeWidth="1.2"
              strokeDasharray="3 3" fill="none" />
        {/* Stops */}
        {pts.map((p, i) => {
          const cl = c[p.stop.cluster];
          const isCurrent = i === idx;
          const isVisited = i < idx;
          const fill = isCurrent ? "#f96167" : isVisited ? "#fbb036" : cl.color;
          const r = isCurrent ? 6 : 4;
          return (
            <g key={i} style={{ cursor: "pointer" }} onClick={() => onJump?.(i)}>
              {isCurrent && <circle cx={p.x} cy={p.y} r="11"
                fill="none" stroke="#f96167" strokeWidth="0.8" opacity="0.5">
                <animate attributeName="r" values="6;14;6" dur="2s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite" />
              </circle>}
              <circle cx={p.x} cy={p.y} r={r} fill={fill}
                      stroke="rgba(245,247,251,0.6)" strokeWidth="0.6" />
              <text x={p.x} y={p.y - 9} fontSize="6.5" fill="rgba(245,247,251,0.7)"
                    fontFamily="JetBrains Mono, monospace" textAnchor="middle">
                {i + 1}
              </text>
            </g>
          );
        })}
      </svg>
      <div style={{ fontSize: 10.5, fontFamily: "var(--f-mono)",
                    color: "var(--c-ink-muted)", marginTop: 4,
                    lineHeight: 1.4, textAlign: "center" }}>
        ▲ start · ≈ bridge · ★ summit
      </div>
    </div>
  );
}

// Streaming-text effect (rationale reveals)
function ShimmerCaption({ text, delay = 0 }) {
  const [shown, setShown] = useState("");
  useEffect(() => {
    let i = 0;
    const t0 = setTimeout(() => {
      const tick = () => {
        i++;
        setShown(text.slice(0, i));
        if (i < text.length) setTimeout(tick, 9);
      };
      tick();
    }, delay);
    return () => clearTimeout(t0);
  }, [text]);
  return <span>{shown}<span style={{ color: "var(--c-bridge)", opacity: shown === text ? 0 : 1 }}>▌</span></span>;
}

Object.assign(window, {
  TopoRidge, Compass, Altitude, Evidence, CourseChip, KindGlyph,
  MiniMap, ShimmerCaption,
});
