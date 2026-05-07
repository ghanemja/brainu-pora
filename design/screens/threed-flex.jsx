/* global React, BU_DATA, BrainGraph3D */

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────────
// SCREEN 7 — 3D MODE FLEX
// Fullscreen viz, always-on labels, recordable camera tour, search.
// The "demo screen for sales / shareables."
// ─────────────────────────────────────────────────────────────────

function ThreeDFlex({ initialNode, visited, onClose, onPickNode }) {
  const graphRef = useRef(null);
  const [labels, setLabels] = useState("hubs");
  const [highlightCluster, setHighlightCluster] = useState(null);
  const [search, setSearch] = useState("");
  const [hover, setHover] = useState(null);
  const [recording, setRecording] = useState(false);
  const [recElapsed, setRecElapsed] = useState(0);

  const filtered = useMemo(() => {
    if (!search.trim()) return [];
    const q = search.toLowerCase();
    return BU_DATA.NODES.filter(n =>
      n.name.toLowerCase().includes(q) || n.id.toLowerCase().includes(q)
    ).slice(0, 6);
  }, [search]);

  useEffect(() => {
    if (initialNode && graphRef.current) {
      setTimeout(() => graphRef.current?.focusOn(initialNode, 70), 600);
    }
  }, [initialNode]);

  useEffect(() => {
    if (!recording) return;
    const t0 = Date.now();
    const id = setInterval(() => setRecElapsed(((Date.now() - t0)/1000)), 100);
    return () => clearInterval(id);
  }, [recording]);

  return (
    <div style={{
      position: "fixed", inset: 0, zIndex: 100,
      background: "var(--c-bg)",
      display: "grid", gridTemplateColumns: "1fr 320px",
    }}>
      {/* Graph */}
      <div style={{ position: "relative" }}>
        <BrainGraph3D
          ref={graphRef}
          currentNode={initialNode}
          visited={visited || new Set()}
          showLabels={labels}
          highlightCluster={highlightCluster}
          cinematic={!recording}
          onNodeHover={setHover}
          onNodeClick={n => onPickNode?.(n.id, n.cluster)}
          background="var(--c-bg)"
        />
        {/* Top-left hud */}
        <div style={{
          position: "absolute", top: 18, left: 18,
          display: "flex", gap: 10, alignItems: "center",
        }}>
          <button className="btn" onClick={onClose}>← Exit fullscreen</button>
          <div style={{
            padding: "6px 12px", borderRadius: 999,
            background: "color-mix(in oklch, var(--c-bg-elev) 80%, transparent)",
            backdropFilter: "blur(8px)",
            border: "1px solid var(--c-line)",
            fontFamily: "var(--f-mono)", fontSize: 11,
            color: "var(--c-ink-muted)", letterSpacing: "0.08em", textTransform: "uppercase",
          }}>BRAIN UNIVERSITY · 3D EXPLORER</div>
        </div>

        {/* Search */}
        <div style={{
          position: "absolute", top: 18, left: "50%", transform: "translateX(-50%)",
          width: 420,
        }}>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="🔎 Search any of 47 concepts… (e.g. Reynolds, Markov, manifold)"
            style={{
              width: "100%",
              background: "color-mix(in oklch, var(--c-bg-elev) 88%, transparent)",
              backdropFilter: "blur(10px)",
              border: "1px solid var(--c-line-strong)",
              borderRadius: 999,
              padding: "10px 18px",
              color: "var(--c-ink)",
              fontFamily: "var(--f-sans)", fontSize: 13.5,
              outline: "none",
            }} />
          {filtered.length > 0 && (
            <div style={{
              position: "absolute", left: 0, right: 0, top: "calc(100% + 4px)",
              background: "var(--c-bg-elev)",
              border: "1px solid var(--c-line)",
              borderRadius: "var(--r-md)",
              padding: 4, boxShadow: "var(--shadow-elev)",
            }}>
              {filtered.map(n => {
                const c = BU_DATA.CLUSTERS[n.cluster];
                return (
                  <button key={n.id} className="btn ghost"
                    onClick={() => {
                      graphRef.current?.focusOn(n.id, 70);
                      setSearch("");
                    }}
                    style={{
                      width: "100%", justifyContent: "flex-start", padding: "8px 12px",
                      borderRadius: 4,
                    }}>
                    <span style={{ width: 8, height: 8, borderRadius: 999, background: c.color }} />
                    <span style={{ flex: 1, textAlign: "left" }}>{n.name}</span>
                    <span className="t-cap">{c.name}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Hover card */}
        {hover && (
          <div style={{
            position: "absolute", bottom: 24, left: 24,
            background: "color-mix(in oklch, var(--c-bg-elev) 88%, transparent)",
            backdropFilter: "blur(10px)",
            border: "1px solid var(--c-line-strong)",
            borderRadius: "var(--r-md)",
            padding: 14, maxWidth: 320,
          }}>
            <div className="t-tag" style={{ color: BU_DATA.CLUSTERS[hover.cluster].color }}>
              {BU_DATA.CLUSTERS[hover.cluster].name}
            </div>
            <div style={{ fontSize: 18, fontWeight: 600, marginTop: 4 }}>{hover.name}</div>
            <div className="t-cap" style={{ marginTop: 6 }}>
              degree <strong style={{ color: "var(--c-ink)" }}>{hover.degree}</strong> · click to begin walk
            </div>
          </div>
        )}

        {/* Recording indicator */}
        {recording && (
          <div style={{
            position: "absolute", top: 70, left: "50%", transform: "translateX(-50%)",
            display: "flex", alignItems: "center", gap: 8,
            padding: "8px 14px", borderRadius: 999,
            background: "rgba(249,97,103,0.18)",
            border: "1px solid var(--c-here)",
            color: "var(--c-here)",
            fontFamily: "var(--f-mono)", fontSize: 12, fontWeight: 500,
          }}>
            <span style={{
              width: 8, height: 8, borderRadius: 999, background: "var(--c-here)",
              animation: "pulseRing 1.2s infinite",
            }} />
            REC · {recElapsed.toFixed(1)}s · camera-tour.webm
          </div>
        )}
      </div>

      {/* Right control rail */}
      <div style={{
        background: "var(--c-bg-elev)",
        borderLeft: "1px solid var(--c-line)",
        padding: 18, display: "flex", flexDirection: "column", gap: 18,
        overflowY: "auto",
      }}>
        <div>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>LABELS</div>
          <div style={{ display: "flex", gap: 4, padding: 3, background: "var(--c-bg-elev-2)",
                        borderRadius: 999, border: "1px solid var(--c-line)" }}>
            {["all","hubs","none"].map(m => (
              <button key={m} onClick={() => setLabels(m)}
                style={{
                  flex: 1, padding: "5px 10px", borderRadius: 999,
                  background: labels === m ? "var(--c-bg-elev)" : "transparent",
                  border: 0, cursor: "pointer",
                  fontFamily: "var(--f-mono)", fontSize: 11,
                  color: labels === m ? "var(--c-ink)" : "var(--c-ink-muted)",
                  textTransform: "uppercase", letterSpacing: "0.08em",
                }}>{m}</button>
            ))}
          </div>
        </div>

        <div>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>HIGHLIGHT COURSE</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            <button onClick={() => setHighlightCluster(null)}
              className="btn ghost" style={{
                justifyContent: "flex-start", fontSize: 12,
                background: highlightCluster == null ? "var(--c-bg-elev-2)" : "transparent",
              }}>
              <span style={{ width: 8, height: 8, borderRadius: 999, background: "var(--c-ink-dim)" }} />
              All courses
            </button>
            {BU_DATA.CLUSTERS.map(c => (
              <button key={c.id} onClick={() => setHighlightCluster(highlightCluster === c.id ? null : c.id)}
                className="btn ghost" style={{
                  justifyContent: "flex-start", fontSize: 12,
                  background: highlightCluster === c.id ? "var(--c-bg-elev-2)" : "transparent",
                }}>
                <span style={{ width: 8, height: 8, borderRadius: 999, background: c.color }} />
                <span style={{ flex: 1, textAlign: "left" }}>{c.name}</span>
                <span className="t-cap" style={{ color: "var(--c-ink-dim)" }}>
                  {BU_DATA.NODES.filter(n => n.cluster === c.id).length}
                </span>
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>CAMERA TOUR</div>
          <button className="btn"
            style={{ width: "100%", borderColor: recording ? "var(--c-here)" : undefined }}
            onClick={() => setRecording(!recording)}>
            {recording ? "■ Stop & download .webm" : "● Record orbit clip"}
          </button>
          <div className="t-cap" style={{ marginTop: 6, color: "var(--c-ink-dim)" }}>
            Auto-orbits the brain for 12s, captures the WebGL canvas to a .webm. Drop into Twitter,
            Slack, slides.
          </div>
        </div>

        <div>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>LEGEND</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12 }}>
            <Legend dot="var(--c-here)" label="You are here" />
            <Legend dot="var(--c-visited)" label="Visited" />
            <Legend dot="var(--c-bridge)" label="Bridge edge" />
            <Legend dot="var(--c-summit)" label="Capstone candidate" />
          </div>
        </div>

        <div style={{ marginTop: "auto" }}>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 6 }}>SHORTCUTS</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 11.5 }}>
            <KbdRow keys={["drag"]} text="Orbit" />
            <KbdRow keys={["scroll"]} text="Zoom" />
            <KbdRow keys={["click"]} text="Focus a node" />
            <KbdRow keys={["esc"]} text="Exit" />
          </div>
        </div>
      </div>
    </div>
  );
}

function Legend({ dot, label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <span style={{ width: 8, height: 8, borderRadius: 999, background: dot }} />
      <span style={{ color: "var(--c-ink-muted)" }}>{label}</span>
    </div>
  );
}

function KbdRow({ keys, text }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <div style={{ display: "flex", gap: 4 }}>
        {keys.map(k => <span key={k} className="kbd">{k}</span>)}
      </div>
      <span style={{ color: "var(--c-ink-muted)" }}>{text}</span>
    </div>
  );
}

window.ThreeDFlex = ThreeDFlex;
