/* global React, BU_DATA, CourseChip, KindGlyph, Compass, TopoRidge */

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────────
// SCREEN 3 — BRANCH POINT (bridge prompt)
// Side panel offering "stay on path" vs "fork to [course]"
// ─────────────────────────────────────────────────────────────────

function BranchPanel({ open, fromNode, onStay, onFork }) {
  const bridges = useMemo(() => fromNode ? BU_DATA.bridgesFrom(fromNode).slice(0, 4) : [], [fromNode]);
  const fromName = fromNode?.replace(/_/g, " ");
  return (
    <>
      {/* backdrop */}
      <div onClick={onStay} style={{
        position: "fixed", inset: 0, zIndex: 50,
        background: "rgba(10,14,34,0.55)",
        backdropFilter: "blur(2px)",
        opacity: open ? 1 : 0, pointerEvents: open ? "auto" : "none",
        transition: "opacity 220ms",
      }} />
      <aside style={{
        position: "fixed", top: 0, right: 0, bottom: 0,
        width: 460, maxWidth: "92vw", zIndex: 51,
        background: "var(--c-bg-elev)",
        borderLeft: "1px solid var(--c-line-strong)",
        boxShadow: "var(--shadow-elev)",
        transform: open ? "translateX(0)" : "translateX(110%)",
        transition: "transform 320ms cubic-bezier(0.4,0,0.2,1)",
        display: "flex", flexDirection: "column",
      }}>
        <div style={{
          padding: "20px 24px",
          borderBottom: "1px solid var(--c-line)",
          display: "flex", justifyContent: "space-between", alignItems: "flex-start",
        }}>
          <div>
            <div className="t-tag" style={{ color: "var(--c-bridge)" }}>≈ BRANCH POINT</div>
            <h2 className="t-h1" style={{ margin: "6px 0 4px" }}>Fork the trail?</h2>
            <p className="t-cap" style={{ margin: 0 }}>
              You're standing at <span className="t-mono">{fromName}</span> — a bridge concept.
              Take it into another course, or stay on the planned route.
            </p>
          </div>
          <button className="btn ghost" onClick={onStay} style={{ padding: 6 }}>✕</button>
        </div>

        <div style={{ flex: 1, overflowY: "auto", padding: "16px 24px" }}>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 10 }}>
            CROSS-COURSE BRIDGES FROM HERE
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {bridges.length === 0 && (
              <div className="t-cap">_no cross-course bridges from this concept_</div>
            )}
            {bridges.map((b, i) => (
              <BridgeCard key={i} bridge={b} onFork={onFork} />
            ))}
          </div>

          <div className="topo-rule" style={{ margin: "24px 0 16px" }} />
          <div className="card recessed">
            <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 6 }}>
              STAY ON THE PLANNED TRAIL
            </div>
            <p className="t-cap" style={{ margin: "0 0 10px" }}>
              The system planned 3 more stops based on your starting peak.
              Forking re-plans live from wherever you go.
            </p>
            <button className="btn" onClick={onStay} style={{ width: "100%" }}>
              ← Continue on the planned trail
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}

function BridgeCard({ bridge, onFork }) {
  const c = BU_DATA.CLUSTERS[bridge.cluster];
  return (
    <div style={{
      border: `1px solid ${c.color}55`,
      borderRadius: "var(--r-md)",
      padding: 14,
      background: `${c.color}0c`,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <div>
          <div className="t-tag" style={{ color: c.color }}>FORK TO</div>
          <h3 style={{ margin: "4px 0 0", fontSize: 16, fontWeight: 600 }}>{c.name}</h3>
        </div>
        <CourseChip clusterId={bridge.cluster} />
      </div>
      <p className="t-cap" style={{ margin: "8px 0 12px" }}>
        Via <span className="t-mono" style={{ color: "var(--c-bridge)" }}>{bridge.toName}</span> —
        the bridge concept that lives on both sides.
      </p>
      <button className="btn primary" style={{ width: "100%" }}
        onClick={() => onFork(bridge.to, bridge.cluster)}>
        Walk into {c.name} →
      </button>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
// SCREEN 4 — SUMMIT (capstone celebration)
// ─────────────────────────────────────────────────────────────────

function Summit({ tour, onAnotherTrail, onDashboard }) {
  const start = tour?.[0];
  const end = tour?.[tour.length - 1];
  const courses = [...new Set(tour.map(s => s.cluster))];
  return (
    <div style={{ minHeight: "calc(100vh - 56px)",
                  background: "linear-gradient(180deg, var(--c-bg) 0%, var(--c-bg-elev) 100%)" }}>
      <div style={{ position: "absolute", inset: 0, top: 56, pointerEvents: "none", overflow: "hidden" }}>
        <TopoRidge height={640} layers={9} opacity={0.6} />
      </div>

      <div style={{ position: "relative", maxWidth: 880, margin: "0 auto",
                    padding: "60px 28px 80px" }}>
        <div style={{ textAlign: "center" }} className="fade-in">
          <div className="t-tag" style={{ color: "var(--c-summit)", marginBottom: 14 }}>
            ★ SUMMIT REACHED
          </div>
          <h1 className="t-display" style={{ margin: 0, fontSize: 56 }}>
            You walked from
          </h1>
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center",
                        gap: 12, margin: "16px 0", flexWrap: "wrap" }}>
            <PathPill node={start} />
            <span style={{ color: "var(--c-ink-dim)", fontSize: 24 }}>→</span>
            <PathPill node={tour[Math.floor(tour.length / 2)]} muted />
            <span style={{ color: "var(--c-ink-dim)", fontSize: 24 }}>→</span>
            <PathPill node={end} summit />
          </div>
          <p style={{ fontSize: 17, color: "var(--c-ink-muted)", maxWidth: 600,
                      margin: "20px auto 0", lineHeight: 1.6 }}>
            The thread between them: <strong style={{ color: "var(--c-ink)" }}>
            curvature, regime, and statistics</strong> — three lenses on the same flow.
            You crossed {courses.length} courses in {tour.length} stops.
          </p>
        </div>

        {/* Stats row */}
        <div style={{ marginTop: 40,
          display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12,
        }}>
          <Stat label="STOPS" value={tour.length} />
          <Stat label="COURSES" value={courses.length} />
          <Stat label="BRIDGES TAKEN" value={tour.filter(s => s.kind === "bridge").length} />
          <Stat label="WALK TIME" value="~28m" />
        </div>

        {/* Auto-mp4 download card */}
        <div className="card" style={{ marginTop: 32, padding: 0, overflow: "hidden" }}>
          <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", gap: 0 }}>
            <div style={{
              background: "linear-gradient(135deg, #1e2761 0%, #7641eb 100%)",
              position: "relative", display: "grid", placeItems: "center",
              minHeight: 160,
            }}>
              <div style={{
                width: 64, height: 64, borderRadius: "50%",
                background: "rgba(245,247,251,0.95)",
                display: "grid", placeItems: "center",
                fontSize: 22, color: "#1e2761", paddingLeft: 4,
                boxShadow: "0 6px 24px rgba(0,0,0,0.4)",
                cursor: "pointer",
              }}>▶</div>
              <div style={{
                position: "absolute", top: 10, left: 10,
                fontFamily: "var(--f-mono)", fontSize: 10,
                color: "rgba(245,247,251,0.7)", letterSpacing: "0.06em", textTransform: "uppercase",
              }}>YOUR_WALK.MP4</div>
              <div style={{
                position: "absolute", bottom: 10, left: 10,
                fontFamily: "var(--f-mono)", fontSize: 10,
                color: "rgba(245,247,251,0.7)",
              }}>1.2 MB · 28s · auto-narrated</div>
            </div>
            <div style={{ padding: 18 }}>
              <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 6 }}>
                YOUR PHOTOGRAPH
              </div>
              <h3 style={{ margin: "0 0 6px", fontSize: 18, fontWeight: 600 }}>
                The trip in 28 seconds
              </h3>
              <p className="t-cap" style={{ margin: "0 0 12px" }}>
                Auto-generated from your walk: title slide → key idea per stop →
                capstone synthesis. Voice-narrated. Save it, share it.
              </p>
              <div style={{ display: "flex", gap: 8 }}>
                <button className="btn primary">⬇ Download mp4</button>
                <button className="btn">Watch in browser</button>
              </div>
            </div>
          </div>
        </div>

        {/* Reflection */}
        <div style={{ marginTop: 24 }}>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>
            REFLECT — OPTIONAL
          </div>
          <textarea placeholder="What clicked? What's still hazy? (one line is enough — feeds the RL loop.)"
            style={{
              width: "100%", minHeight: 70,
              background: "var(--c-bg-elev)",
              border: "1px solid var(--c-line)",
              borderRadius: "var(--r-md)",
              padding: 12, color: "var(--c-ink)",
              fontFamily: "var(--f-sans)", fontSize: 13.5,
              outline: "none", resize: "vertical",
            }} />
        </div>

        {/* Two next-step buttons */}
        <div style={{ marginTop: 28,
          display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12,
        }}>
          <button className="btn" style={{
            padding: 18, flexDirection: "column", alignItems: "flex-start",
          }}
            onClick={onAnotherTrail}>
            <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>SAME RANGE</div>
            <div style={{ fontSize: 16, fontWeight: 600, marginTop: 4 }}>
              Another trail in this range →
            </div>
            <div className="t-cap" style={{ marginTop: 4 }}>
              Re-plan from the summit, deeper in the same cluster.
            </div>
          </button>
          <button className="btn primary" style={{
            padding: 18, flexDirection: "column", alignItems: "flex-start",
          }}
            onClick={onDashboard}>
            <div className="t-tag" style={{ color: "rgba(255,255,255,0.7)" }}>DIFFERENT RANGE</div>
            <div style={{ fontSize: 16, fontWeight: 600, marginTop: 4 }}>
              A totally different range →
            </div>
            <div className="t-cap" style={{ marginTop: 4, color: "rgba(255,255,255,0.85)" }}>
              Pick a fresh peak from the trailhead.
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}

function PathPill({ node, muted, summit }) {
  if (!node) return null;
  const cluster = BU_DATA.CLUSTERS[node.cluster];
  return (
    <div style={{
      padding: "10px 16px", borderRadius: 999,
      border: `1px solid ${summit ? "var(--c-summit)" : muted ? "var(--c-line)" : cluster.color}`,
      background: summit ? "color-mix(in oklch, var(--c-summit) 18%, transparent)"
                          : muted ? "var(--c-bg-elev)" : `${cluster.color}22`,
      fontFamily: "var(--f-mono)", fontWeight: 500, fontSize: 14,
      color: summit ? "var(--c-summit)" : muted ? "var(--c-ink-muted)" : "var(--c-ink)",
    }}>
      {summit && <span style={{ marginRight: 6 }}>★</span>}
      {node.node?.replace(/_/g, " ")}
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div style={{
      padding: "16px 14px",
      background: "var(--c-bg-elev)",
      border: "1px solid var(--c-line)",
      borderRadius: "var(--r-md)",
      textAlign: "center",
    }}>
      <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>{label}</div>
      <div className="t-num" style={{ marginTop: 6, color: "var(--c-ink)" }}>{value}</div>
    </div>
  );
}

window.BranchPanel = BranchPanel;
window.Summit = Summit;
