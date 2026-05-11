/* global React, BU_DATA, ARXIVIS, ARXIVIS_VIDEOS, BrainGraph3D */

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────────
// SCREEN 8 — ARXIVIS
// "See through the hype, grasp a paper in 30 seconds."
//
// Project each paper onto the brain-university concept manifold. The
// 3D graph is the world; each paper = an activation pattern. Watch
// the camera fly through the concepts a paper lights up. Read the
// elevator pitch on the side. Done.
//
// Layout (3 cols): paper list │ 3D graph │ paper card
// ─────────────────────────────────────────────────────────────────

function ArXivis({ onClose, onJumpToConcept }) {
  const graphRef = useRef(null);
  const [sortBy, setSortBy] = useState("novelty");        // novelty | year | edges
  const [sourceFilter, setSourceFilter] = useState("ALL"); // ALL | arXiv | NTRS | DTIC | …
  const [selectedId, setSelectedId] = useState(null);
  const [flythrough, setFlythrough] = useState(false);
  const [flyIdx, setFlyIdx] = useState(0);

  // Track viewport so we can switch layout on narrow screens
  const [vw, setVw] = useState(window.innerWidth);
  useEffect(() => {
    const on = () => setVw(window.innerWidth);
    window.addEventListener("resize", on);
    return () => window.removeEventListener("resize", on);
  }, []);
  const narrow = vw < 1000;

  const PAPERS = (window.ARXIVIS?.papers || []);
  const stats  = window.ARXIVIS?.stats || {};

  // ----- filters / sort -----
  const sources = useMemo(() => {
    const s = new Set(PAPERS.map(p => p.source));
    return ["ALL", ...Array.from(s).sort()];
  }, [PAPERS]);

  const filtered = useMemo(() => {
    let xs = PAPERS;
    if (sourceFilter !== "ALL") xs = xs.filter(p => p.source === sourceFilter);
    xs = [...xs];
    if (sortBy === "novelty") xs.sort((a,b) => b.novelty_bits - a.novelty_bits);
    if (sortBy === "year")    xs.sort((a,b) => (b.year || 0) - (a.year || 0));
    if (sortBy === "edges")   xs.sort((a,b) => (b.pair_edges?.length || 0) - (a.pair_edges?.length || 0));
    return xs;
  }, [PAPERS, sortBy, sourceFilter]);

  const selected = useMemo(
    () => filtered.find(p => p.id === selectedId) || filtered[0],
    [filtered, selectedId]
  );

  // Map paper-activated wiki ids onto graph node ids that actually exist
  const activatedGraphNodes = useMemo(() => {
    if (!selected) return [];
    const nodeIds = new Set(BU_DATA.NODES.map(n => n.id));
    // Concept ids in ARXIVIS look like "wiki:slug" — graph node ids are slugs
    return selected.concepts
      .map(c => c.id.replace(/^wiki:/, ""))
      .filter(id => nodeIds.has(id));
  }, [selected]);

  // Auto-flythrough: cycle camera through activated nodes
  useEffect(() => {
    if (!flythrough || !selected || activatedGraphNodes.length === 0) return;
    setFlyIdx(0);
    let i = 0;
    const step = () => {
      const nid = activatedGraphNodes[i];
      graphRef.current?.focusOn(nid, 60);
      setFlyIdx(i);
      i = (i + 1) % activatedGraphNodes.length;
    };
    step();
    const dur = Math.max(2200, 30000 / Math.max(1, activatedGraphNodes.length));
    const id = setInterval(step, dur);
    return () => clearInterval(id);
  }, [flythrough, selected, activatedGraphNodes]);

  // Auto-pick first paper on mount
  useEffect(() => {
    if (!selectedId && filtered[0]) setSelectedId(filtered[0].id);
  }, [filtered, selectedId]);

  // Focus camera on first activated concept whenever paper changes
  useEffect(() => {
    if (selected && activatedGraphNodes[0]) {
      setTimeout(() => graphRef.current?.focusOn(activatedGraphNodes[0], 70), 350);
    }
  }, [selected?.id]);

  if (!window.ARXIVIS) {
    return (
      <div style={{
        position: "fixed", inset: 0, zIndex: 100,
        background: "var(--c-bg)", color: "var(--c-ink)",
        display: "grid", placeItems: "center", padding: 24, textAlign: "center",
      }}>
        <div>
          <h2>arXivis data not loaded</h2>
          <p style={{ opacity: 0.7, maxWidth: 520, margin: "12px auto" }}>
            Run <code>python3 scripts/build_arxivis_data.py</code> to generate
            <code> design/arxivis_data.js</code>, then refresh.
          </p>
          <button className="btn" onClick={onClose}>← Back</button>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      position: "fixed", inset: 0, zIndex: 100,
      background: "var(--c-bg)",
      display: "grid",
      gridTemplateColumns: narrow ? "1fr" : "minmax(260px, 22%) 1fr minmax(300px, 26%)",
      gridTemplateRows: narrow ? "auto 1fr auto auto" : "auto 1fr",
    }}>
      {/* TOP BAR (spans all columns) */}
      <div style={{
        gridColumn: "1 / -1",
        display: "flex", alignItems: "center", gap: 16, padding: "14px 18px",
        borderBottom: "1px solid var(--c-line)",
        background: "var(--c-bg-elev)",
      }}>
        <button className="btn" onClick={onClose}>← Exit</button>
        <div style={{
          fontFamily: "var(--f-mono)", fontSize: 11,
          color: "var(--c-ink-muted)", letterSpacing: "0.10em", textTransform: "uppercase",
        }}>arXivis · see the paper in 30 seconds</div>
        <div style={{ flex: 1 }} />
        <span style={{ fontFamily: "var(--f-mono)", fontSize: 11, opacity: 0.6 }}>
          {filtered.length} papers · {stats.concepts_in_vocab} concept manifold · {stats.papers_with_acts} activated of {stats.total_papers_scanned} scanned
        </span>
      </div>

      {/* LEFT — paper list */}
      <aside style={{
        borderRight: narrow ? "none" : "1px solid var(--c-line)",
        borderBottom: narrow ? "1px solid var(--c-line)" : "none",
        overflow: "hidden", display: "flex", flexDirection: "column",
        background: "var(--c-bg-elev)",
        maxHeight: narrow ? 280 : "none",
      }}>
        <div style={{
          padding: "10px 14px", borderBottom: "1px solid var(--c-line)",
          display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center",
        }}>
          <span style={{ fontSize: 11, opacity: 0.55, fontFamily: "var(--f-mono)" }}>SORT</span>
          {["novelty", "year", "edges"].map(s => (
            <button key={s}
              className={"btn ghost" + (sortBy === s ? " active" : "")}
              onClick={() => setSortBy(s)}
              style={{
                padding: "4px 10px", fontSize: 11.5,
                background: sortBy === s ? "var(--c-ink)" : "transparent",
                color:      sortBy === s ? "var(--c-bg)" : "var(--c-ink-muted)",
                borderRadius: 999,
              }}>
              {s}
            </button>
          ))}
        </div>
        <div style={{
          padding: "8px 14px", borderBottom: "1px solid var(--c-line)",
          display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center",
        }}>
          <span style={{ fontSize: 11, opacity: 0.55, fontFamily: "var(--f-mono)" }}>SOURCE</span>
          {sources.map(s => (
            <button key={s}
              className={"btn ghost" + (sourceFilter === s ? " active" : "")}
              onClick={() => setSourceFilter(s)}
              style={{
                padding: "4px 10px", fontSize: 11.5,
                background: sourceFilter === s ? "var(--c-ink)" : "transparent",
                color:      sourceFilter === s ? "var(--c-bg)" : "var(--c-ink-muted)",
                borderRadius: 999,
              }}>
              {s}
            </button>
          ))}
        </div>
        <div style={{ overflowY: "auto", flex: 1 }}>
          {filtered.map(p => (
            <button key={p.id}
              onClick={() => { setSelectedId(p.id); setFlythrough(false); }}
              style={{
                display: "block", width: "100%", textAlign: "left",
                padding: "10px 14px",
                borderBottom: "1px solid var(--c-line)",
                background: p.id === selected?.id ? "color-mix(in oklch, var(--c-ink) 8%, transparent)" : "transparent",
                cursor: "pointer", border: "none", borderLeft: p.id === selected?.id ? "3px solid var(--c-bridge, #f96167)" : "3px solid transparent",
                color: "var(--c-ink)",
              }}>
              <div style={{
                display: "flex", justifyContent: "space-between", alignItems: "baseline",
                gap: 8, marginBottom: 4,
              }}>
                <span style={{
                  fontFamily: "var(--f-mono)", fontSize: 10,
                  color: badgeColor(p.source), letterSpacing: "0.08em",
                }}>
                  {p.source}{p.year ? ` · ${p.year}` : ""}
                </span>
                <span title="information-theoretic novelty bits" style={{
                  fontFamily: "var(--f-mono)", fontSize: 11, opacity: 0.85,
                }}>
                  ◆ {p.novelty_bits.toFixed(1)}
                </span>
              </div>
              <div style={{ fontSize: 13.5, lineHeight: 1.35, fontWeight: 500 }}>
                {p.title}
              </div>
              <div style={{ fontSize: 11, opacity: 0.55, marginTop: 4 }}>
                {p.concepts.slice(0, 3).map(c => c.name).join(" · ")}
              </div>
            </button>
          ))}
        </div>
      </aside>

      {/* CENTER — 3D graph */}
      <div style={{ position: "relative" }}>
        <BrainGraph3D
          ref={graphRef}
          tourPath={activatedGraphNodes}
          currentNode={activatedGraphNodes[flyIdx] || null}
          showLabels="hubs"
          cinematic={!flythrough}
          signalFlow={true}
          linkOpacity={0.55}
          linkWidth={1.6}
          linkColor="#0a0e22"
          background="var(--c-bg)"
        />

        {/* Bottom HUD: pitch + flythrough controls */}
        {selected && (
          <div style={{
            position: "absolute", bottom: 0, left: 0, right: 0,
            padding: "18px 22px",
            background: "linear-gradient(0deg, color-mix(in oklch, var(--c-bg) 92%, transparent) 0%, transparent 100%)",
            pointerEvents: "none",
          }}>
            <div style={{
              maxWidth: 700, margin: "0 auto",
              background: "color-mix(in oklch, var(--c-bg-elev) 90%, transparent)",
              backdropFilter: "blur(10px)",
              border: "1px solid var(--c-line)",
              borderRadius: "var(--r-lg, 12px)",
              padding: "14px 18px",
              pointerEvents: "auto",
            }}>
              <div style={{
                display: "flex", justifyContent: "space-between",
                alignItems: "center", marginBottom: 6,
              }}>
                <span style={{
                  fontFamily: "var(--f-mono)", fontSize: 10,
                  color: "var(--c-ink-muted)", letterSpacing: "0.10em",
                  textTransform: "uppercase",
                }}>
                  30-second pitch
                </span>
                <button className="btn"
                  onClick={() => setFlythrough(f => !f)}
                  style={{ padding: "5px 14px", fontSize: 11.5 }}>
                  {flythrough ? "⏸ Pause flythrough" : "▶ Fly through concepts"}
                </button>
              </div>
              <div style={{ fontSize: 13.5, lineHeight: 1.55, whiteSpace: "pre-line" }}>
                {selected.pitch}
              </div>
            </div>
          </div>
        )}

        {/* Top-left HUD: current concept indicator during flythrough */}
        {flythrough && activatedGraphNodes[flyIdx] && (
          <div style={{
            position: "absolute", top: 16, left: 16,
            padding: "8px 14px",
            background: "color-mix(in oklch, var(--c-bg-elev) 88%, transparent)",
            backdropFilter: "blur(10px)",
            border: "1px solid var(--c-line)",
            borderRadius: 999,
            fontFamily: "var(--f-mono)", fontSize: 11,
          }}>
            <span style={{ opacity: 0.55 }}>Concept {flyIdx + 1} / {activatedGraphNodes.length}:</span>{" "}
            <span style={{ fontWeight: 600 }}>{(BU_DATA.NODES.find(n => n.id === activatedGraphNodes[flyIdx])?.name) || activatedGraphNodes[flyIdx]}</span>
          </div>
        )}
      </div>

      {/* RIGHT — paper card */}
      <aside style={{
        borderLeft: narrow ? "none" : "1px solid var(--c-line)",
        borderTop:  narrow ? "1px solid var(--c-line)" : "none",
        background: "var(--c-bg-elev)",
        overflowY: "auto",
        padding: "18px 20px",
        maxHeight: narrow ? 320 : "none",
      }}>
        {selected && (
          <>
            <div style={{
              fontFamily: "var(--f-mono)", fontSize: 10,
              color: badgeColor(selected.source), letterSpacing: "0.10em",
              marginBottom: 6,
            }}>
              {selected.source}{selected.year ? ` · ${selected.year}` : ""}
              {selected.category_hint ? ` · ${selected.category_hint}` : ""}
            </div>
            <h2 style={{
              fontSize: 18, lineHeight: 1.3, margin: "0 0 12px 0",
              fontFamily: "var(--f-display, var(--f-sans))",
            }}>
              {selected.title}
            </h2>

            {selected.url && (
              <a href={selected.url} target="_blank" rel="noreferrer"
                 style={{ fontSize: 12, color: "var(--c-bridge, #1e6fa8)" }}>
                Open source ↗
              </a>
            )}

            {/* Novelty breakdown */}
            <div style={{
              marginTop: 18, padding: 14,
              border: "1px solid var(--c-line)",
              borderRadius: 10,
              background: "color-mix(in oklch, var(--c-bg) 60%, transparent)",
            }}>
              <div style={{
                display: "flex", justifyContent: "space-between",
                fontFamily: "var(--f-mono)", fontSize: 11,
                marginBottom: 8, color: "var(--c-ink-muted)",
                letterSpacing: "0.08em", textTransform: "uppercase",
              }}>
                <span>Novelty</span>
                <span>◆ {selected.novelty_bits.toFixed(1)} bits</span>
              </div>
              <NoveltyBar label="concept rarity"  v={selected.novelty_breakdown?.concept_bits}     max={15} />
              <NoveltyBar label="new edges"       v={selected.novelty_breakdown?.edge_bits}        max={90} />
              <NoveltyBar label="innovations"     v={selected.novelty_breakdown?.innovation_bonus} max={8}  />
            </div>

            {/* Activated concepts */}
            <div style={{ marginTop: 18 }}>
              <div style={{
                fontFamily: "var(--f-mono)", fontSize: 10, opacity: 0.6,
                letterSpacing: "0.10em", textTransform: "uppercase", marginBottom: 8,
              }}>
                Activates {selected.concepts.length} concept{selected.concepts.length === 1 ? "" : "s"}
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {selected.concepts.map(c => (
                  <button key={c.id}
                    onClick={() => onJumpToConcept?.(c.id.replace(/^wiki:/, ""))}
                    style={{
                      padding: "4px 10px", fontSize: 11.5,
                      background: "color-mix(in oklch, var(--c-ink) 6%, transparent)",
                      border: "1px solid var(--c-line)",
                      borderRadius: 999,
                      color: "var(--c-ink)", cursor: "pointer",
                    }}>
                    {c.name}{" "}
                    <span style={{ opacity: 0.45 }}>{c.weight.toFixed(1)}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Innovations — actual named contributions from the paper */}
            {selected.innovations?.length > 0 && (
              <div style={{ marginTop: 18 }}>
                <div style={{
                  fontFamily: "var(--f-mono)", fontSize: 10, opacity: 0.6,
                  letterSpacing: "0.10em", textTransform: "uppercase", marginBottom: 8,
                }}>
                  Innovations · what the paper claims
                </div>
                {selected.innovations.slice(0, 5).map((innov, i) => {
                  const isProposes = innov.kind === "proposes";
                  const accent = isProposes ? "#60FFA8" : "#7DD3FC";
                  return (
                    <div key={i} style={{
                      marginBottom: 10, padding: "8px 10px",
                      border: `1px solid ${accent}`,
                      borderLeft: `3px solid ${accent}`,
                      borderRadius: 6,
                      background: "color-mix(in oklch, var(--c-bg) 70%, transparent)",
                    }}>
                      <div style={{
                        display: "flex", justifyContent: "space-between",
                        marginBottom: 4,
                      }}>
                        <span style={{
                          fontFamily: "var(--f-mono)", fontSize: 9,
                          color: accent, letterSpacing: "0.10em",
                          textTransform: "uppercase",
                        }}>
                          {innov.kind} · {innov.pattern}
                        </span>
                      </div>
                      <div style={{ fontSize: 12.5, lineHeight: 1.4 }}>
                        {innov.phrase}
                      </div>
                      {innov.connects_to?.length > 0 && (
                        <div style={{ marginTop: 4, fontSize: 10.5,
                          fontFamily: "var(--f-mono)", opacity: 0.55,
                        }}>
                          → {innov.connects_to.map(c => c.replace(/^wiki:/, "").replace(/_/g, " ")).slice(0,2).join(" · ")}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            {/* Video player — 9:16 explainer (protein-viz aesthetic) */}
            <PaperVideo paperId={selected.id} />

            {/* Activation edges count */}
            <div style={{ marginTop: 22, fontSize: 12, opacity: 0.55 }}>
              <strong>{selected.pair_edges?.length || 0}</strong> concept-pair edges activated
              ·  highlighted amber in graph
            </div>
          </>
        )}
      </aside>
    </div>
  );
}

function PaperVideo({ paperId }) {
  const src = window.ARXIVIS_VIDEOS?.[paperId];
  if (!src) {
    return (
      <div style={{
        marginTop: 18, padding: 14,
        border: "1px dashed var(--c-line)",
        borderRadius: 10,
        fontSize: 12, opacity: 0.55, textAlign: "center",
      }}>
        No 30-second explainer rendered yet.
        <br/>
        <code style={{ fontSize: 10, opacity: 0.7 }}>
          python3 scripts/render_arxivis_video.py --paper-id {paperId}
        </code>
      </div>
    );
  }
  return (
    <div style={{
      marginTop: 18,
      borderRadius: 12, overflow: "hidden",
      background: "#000",
      border: "1px solid var(--c-line)",
    }}>
      <div style={{
        padding: "6px 10px",
        fontFamily: "var(--f-mono)", fontSize: 10,
        color: "#60FFA8", letterSpacing: "0.10em",
        textTransform: "uppercase",
        background: "rgba(96,255,168,0.06)",
        borderBottom: "1px solid var(--c-line)",
      }}>
        30-SECOND EXPLAINER · 9:16
      </div>
      <video src={src} controls autoPlay loop muted playsInline
             style={{ display: "block", width: "100%", maxHeight: 520 }} />
    </div>
  );
}

function NoveltyBar({ label, v, max }) {
  const pct = Math.min(100, Math.max(0, ((v ?? 0) / max) * 100));
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{
        display: "flex", justifyContent: "space-between",
        fontSize: 11, opacity: 0.75, marginBottom: 3,
      }}>
        <span>{label}</span>
        <span style={{ fontFamily: "var(--f-mono)" }}>{(v ?? 0).toFixed(1)}</span>
      </div>
      <div style={{
        height: 4, background: "color-mix(in oklch, var(--c-ink) 8%, transparent)",
        borderRadius: 2,
      }}>
        <div style={{
          width: `${pct}%`, height: "100%",
          background: "var(--c-bridge, #f96167)",
          borderRadius: 2,
        }} />
      </div>
    </div>
  );
}

function badgeColor(source) {
  const s = (source || "").toUpperCase();
  if (s.includes("ARXIV"))    return "#7DD3FC";
  if (s.includes("NTRS"))     return "#FBB036";
  if (s.includes("DTIC"))     return "#F96167";
  if (s.includes("OPENALEX")) return "#84cc16";
  return "var(--c-ink-muted)";
}

window.ArXivis = ArXivis;
