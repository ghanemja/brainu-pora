/* global React, BU_DATA, CourseChip, KindGlyph, TopoRidge, BrainGraph3D */

const { useState, useEffect, useMemo } = React;

// ─────────────────────────────────────────────────────────────────
// SCREEN 5 — RETURNING-LEARNER DASHBOARD
// "What trails you've walked, what's open, where you stopped."
// ─────────────────────────────────────────────────────────────────

const MOCK_TRAILS = [
  {
    id: "t1", title: "Reynolds → Manifolds → Markov chains",
    started: "yesterday", progress: 1.0, stops: 6, courses: 3,
    summary: "Aero → Diff geo → Info theory. Capstone reached.",
    color: "#7641eb",
  },
  {
    id: "t2", title: "Graph theory → Louvain → PageRank",
    started: "3 days ago", progress: 0.5, stops: 6, courses: 2,
    summary: "Stopped at PageRank — bridge to information theory pending.",
    color: "#2ec4b6",
  },
  {
    id: "t3", title: "State space → Kalman → Hodgkin-Huxley",
    started: "last week", progress: 0.83, stops: 6, courses: 3,
    summary: "Almost summit — one stop left in cellular biology.",
    color: "#1e6fa8",
  },
];

function Dashboard({ learner, onResume, onNewTrail }) {
  const totalNodesVisited = 14;
  const totalCourses = 4;
  const totalConcepts = BU_DATA.NODES.length;
  return (
    <div style={{ minHeight: "calc(100vh - 56px)" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 56, pointerEvents: "none", opacity: 0.45 }}>
        <TopoRidge height={420} layers={6} />
      </div>

      <div style={{ position: "relative", maxWidth: 1120, margin: "0 auto", padding: "48px 28px 80px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: 32 }}>
          <div>
            <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>WELCOME BACK</div>
            <h1 className="t-display" style={{ margin: "6px 0 0" }}>
              {learner?.name || "Learner"}
            </h1>
            <p className="t-cap" style={{ margin: "6px 0 0" }}>
              {totalNodesVisited} concepts walked · {totalCourses} courses entered ·
              {" "}<span style={{ color: "var(--c-ink-muted)" }}>{totalConcepts - totalNodesVisited} concepts unwalked</span>
            </p>
          </div>
          <button className="btn primary" onClick={onNewTrail}>
            ▲ Plan a new trail
          </button>
        </div>

        {/* Progress on the brain */}
        <div className="card" style={{ padding: 0, overflow: "hidden", marginBottom: 32 }}>
          <div style={{ padding: "12px 16px", borderBottom: "1px solid var(--c-line)",
                        display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div className="t-h3">Where you've been on the brain</div>
              <div className="t-cap" style={{ marginTop: 2 }}>
                Visited concepts in amber. Hovering rotates the camera.
              </div>
            </div>
            <span className="t-mono" style={{ fontSize: 11, color: "var(--c-ink-muted)" }}>
              {totalNodesVisited}/{totalConcepts} ·
              <span style={{ color: "var(--c-visited)" }}> {Math.round(100*totalNodesVisited/totalConcepts)}% explored</span>
            </span>
          </div>
          <div style={{ height: 360, background: "var(--c-bg-elev-2)" }}>
            <BrainGraph3D
              visited={new Set(["Reynolds_number","Boundary_layer","Navier_Stokes","Manifold","Tensor","Markov_chain",
                                "Graph_theory","Louvain_clustering","PageRank","BFS","Dijkstra","State_space","Kalman_filter","Lyapunov_stability"])}
              showLabels="hubs"
              cinematic={true}
              background="var(--c-bg-elev-2)"
            />
          </div>
        </div>

        {/* Trails grid */}
        <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 12 }}>
          YOUR TRAIL JOURNAL
        </div>
        <div style={{
          display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px,1fr))",
          gap: 12,
        }}>
          {MOCK_TRAILS.map(t => (
            <TrailCard key={t.id} trail={t} onResume={() => onResume(t.id)} />
          ))}
          {/* Surprise me card */}
          <div className="card" style={{
            display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center",
            minHeight: 200, cursor: "pointer",
            border: "1px dashed var(--c-line-strong)",
            background: "transparent",
          }} onClick={onNewTrail}>
            <div style={{ fontSize: 28, color: "var(--c-bridge)", marginBottom: 6 }}>≈</div>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>Surprise me</div>
            <div className="t-cap" style={{ textAlign: "center", maxWidth: 200 }}>
              Pick a random unvisited peak with high cross-course span.
            </div>
          </div>
        </div>

        {/* Streaks / RL feedback (subtle, no gamification slop) */}
        <div style={{ marginTop: 32,
                      display: "grid", gridTemplateColumns: "2fr 1fr", gap: 12 }}>
          <div className="card">
            <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>
              SYSTEM IS LEARNING FROM YOU
            </div>
            <div style={{ display: "flex", gap: 24, fontFamily: "var(--f-mono)", fontSize: 12 }}>
              <div>
                <div style={{ color: "var(--c-ink-muted)" }}>Hebbian boost</div>
                <div style={{ fontSize: 18, color: "var(--c-ink)", marginTop: 2 }}>
                  Manifold +0.34
                </div>
              </div>
              <div>
                <div style={{ color: "var(--c-ink-muted)" }}>Eligibility decay</div>
                <div style={{ fontSize: 18, color: "var(--c-ink)", marginTop: 2 }}>
                  λ = 0.92 / session
                </div>
              </div>
              <div>
                <div style={{ color: "var(--c-ink-muted)" }}>Auto-judge score</div>
                <div style={{ fontSize: 18, color: "var(--c-cs)", marginTop: 2 }}>
                  +12 vs baseline
                </div>
              </div>
            </div>
            <div className="t-cap" style={{ marginTop: 10 }}>
              Your last 6 walks have re-weighted the graph for the next learner. That's how the
              brain grows.
            </div>
          </div>
          <div className="card recessed" style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
            <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>STREAK</div>
            <div className="t-num" style={{ marginTop: 6, color: "var(--c-visited)" }}>4</div>
            <div className="t-cap" style={{ marginTop: 2 }}>days walking</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function TrailCard({ trail, onResume }) {
  const done = trail.progress >= 1;
  return (
    <div className="card" style={{ display: "flex", flexDirection: "column", gap: 10,
                                    padding: 16, cursor: "pointer" }} onClick={onResume}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>
            {done ? "★ COMPLETED" : "RESUME · " + trail.started.toUpperCase()}
          </div>
          <h3 style={{ margin: "4px 0 0", fontSize: 15.5, fontWeight: 600, lineHeight: 1.3, letterSpacing: "-0.01em" }}>
            {trail.title}
          </h3>
        </div>
        {done && <span style={{ color: "var(--c-summit)", fontSize: 18 }}>★</span>}
      </div>
      <div className="t-cap" style={{ flex: 1 }}>{trail.summary}</div>
      {/* Topo-style progress */}
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{
          flex: 1, height: 6, borderRadius: 3,
          background: "var(--c-bg-elev-2)",
          overflow: "hidden",
        }}>
          <div style={{
            width: `${trail.progress * 100}%`, height: "100%",
            background: done
              ? "linear-gradient(90deg, var(--c-here), var(--c-visited), var(--c-bridge), var(--c-summit))"
              : "linear-gradient(90deg, var(--c-here), var(--c-visited))",
          }} />
        </div>
        <span style={{ fontFamily: "var(--f-mono)", fontSize: 11, color: "var(--c-ink-muted)" }}>
          {Math.round(trail.progress * trail.stops)}/{trail.stops}
        </span>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
// SCREEN 6 — PROPOSE
// Free-text idea → matched concepts + grounded synthesis
// ─────────────────────────────────────────────────────────────────

function Propose({ onJumpToNode }) {
  const examples = Object.keys(BU_DATA.PROPOSE_EXAMPLES);
  const [query, setQuery] = useState(examples[0]);
  const [submitted, setSubmitted] = useState(examples[0]);
  const [thinking, setThinking] = useState(false);
  const result = BU_DATA.PROPOSE_EXAMPLES[submitted];

  const handleSubmit = (q) => {
    setSubmitted(null);
    setThinking(true);
    setTimeout(() => {
      const found = BU_DATA.PROPOSE_EXAMPLES[q] || BU_DATA.PROPOSE_EXAMPLES[examples[0]];
      setSubmitted(q in BU_DATA.PROPOSE_EXAMPLES ? q : examples[0]);
      setThinking(false);
    }, 1200);
  };

  return (
    <div style={{ minHeight: "calc(100vh - 56px)", padding: "48px 28px 80px" }}>
      <div style={{ maxWidth: 880, margin: "0 auto" }}>
        <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>≈ PROPOSE</div>
        <h1 className="t-display" style={{ margin: "6px 0 4px" }}>
          Drop in a half-formed idea.
        </h1>
        <p className="t-cap" style={{ marginBottom: 24, fontSize: 14 }}>
          The brain finds matching concepts, traces shortest paths between them, and writes back a
          grounded paragraph you can use as a starting answer.
        </p>

        {/* Input — deliberately not a search bar */}
        <div style={{ position: "relative" }}>
          <textarea
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="e.g. drone swarm coordination · explain entropy to a physicist · how does diffusion show up in ion channels?"
            style={{
              width: "100%", minHeight: 96,
              background: "var(--c-bg-elev)",
              border: "1px solid var(--c-line-strong)",
              borderRadius: "var(--r-lg)",
              padding: "16px 18px",
              color: "var(--c-ink)",
              fontFamily: "var(--f-sans)", fontSize: 16, lineHeight: 1.5,
              outline: "none", resize: "vertical",
            }}
            onKeyDown={e => { if (e.key === "Enter" && (e.metaKey||e.ctrlKey)) handleSubmit(query); }}
          />
          <button className="btn primary" onClick={() => handleSubmit(query)} style={{
            position: "absolute", bottom: 12, right: 12,
          }}>Trace ⏎</button>
        </div>

        {/* Example chips */}
        <div style={{ marginTop: 12, display: "flex", gap: 6, flexWrap: "wrap" }}>
          <span className="t-cap" style={{ color: "var(--c-ink-dim)", marginRight: 4 }}>Try:</span>
          {examples.map(ex => (
            <button key={ex} className="btn ghost" style={{ fontSize: 12, padding: "4px 10px" }}
              onClick={() => { setQuery(ex); handleSubmit(ex); }}>
              {ex}
            </button>
          ))}
        </div>

        {/* Result */}
        {thinking && (
          <div style={{ marginTop: 32 }} className="fade-in">
            <div className="shimmer-text t-h2">
              Tracing through {BU_DATA.NODES.length} concepts ·
              finding bridges · grounding response…
            </div>
            <div style={{
              marginTop: 16, height: 4, borderRadius: 2,
              background: "linear-gradient(90deg, transparent, var(--c-bridge), transparent)",
              backgroundSize: "200% 100%",
              animation: "shimmer 1.4s infinite",
            }} />
          </div>
        )}

        {!thinking && submitted && result && (
          <div className="slide-up" style={{ marginTop: 32 }}>
            {/* Matched concepts */}
            <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>
              MATCHED · {result.matched.length} CONCEPTS IN GRAPH
            </div>
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 24 }}>
              {result.matched.map(id => {
                const node = BU_DATA.NODES.find(n => n.id === id);
                if (!node) return null;
                const c = BU_DATA.CLUSTERS[node.cluster];
                return (
                  <button key={id} className="btn"
                    onClick={() => onJumpToNode?.(id, node.cluster)}
                    style={{
                      borderColor: c.color + "55",
                      background: c.color + "0c",
                      fontFamily: "var(--f-mono)", fontSize: 12,
                    }}>
                    <span style={{ color: c.color }}>●</span>
                    {node.name}
                  </button>
                );
              })}
            </div>

            {/* Bridges traced */}
            {result.bridges.length > 0 && (
              <div style={{ marginBottom: 24 }}>
                <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>
                  BRIDGES TRACED · {result.bridges.length} FOUND
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {result.bridges.map((b, i) => (
                    <div key={i} className="card recessed" style={{ padding: 12 }}>
                      <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 6,
                                    fontFamily: "var(--f-mono)", fontSize: 12 }}>
                        <span style={{ color: "var(--c-ink)" }}>{b.from.replace(/_/g," ")}</span>
                        <span style={{ color: "var(--c-bridge)" }}>≈</span>
                        <span style={{ color: "var(--c-ink)" }}>{b.to.replace(/_/g," ")}</span>
                      </div>
                      <div className="t-cap" style={{ fontSize: 13, color: "var(--c-ink-muted)", lineHeight: 1.5 }}>
                        {b.via}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Synthesis paragraph */}
            <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>
              GROUNDED SYNTHESIS
            </div>
            <div className="card" style={{ padding: 24,
              borderLeft: "3px solid var(--c-bridge)",
            }}>
              <p style={{ margin: 0, fontSize: 16, lineHeight: 1.65 }}>{result.synthesis}</p>
              <div className="t-cap" style={{
                marginTop: 14, color: "var(--c-ink-dim)",
                display: "flex", gap: 12,
              }}>
                <span>generated by `agents.proposal_responder`</span>
                <span>·</span>
                <span>grounded in {result.matched.length} graph concepts + {result.bridges.length} traced bridges</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

window.Dashboard = Dashboard;
window.Propose = Propose;
