/* global React, BU_DATA, OPEN_PROBLEMS, ARXIVIS, BrainGraph3D */

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────────
// SCREEN 9 — OPEN PROBLEMS
// Surfaces gaps in the concept graph that no paper has yet
// addressed. Each problem suggests papers closest to tackling
// it + the foundational concepts a contributor could build on.
// ─────────────────────────────────────────────────────────────────

function OpenProblems({ onClose, onJumpToConcept }) {
  const graphRef = useRef(null);
  const [kindFilter, setKindFilter] = useState("ALL");
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [vw, setVw] = useState(window.innerWidth);
  useEffect(() => {
    const on = () => setVw(window.innerWidth);
    window.addEventListener("resize", on);
    return () => window.removeEventListener("resize", on);
  }, []);
  const narrow = vw < 1000;

  const PROBLEMS = window.OPEN_PROBLEMS?.problems || [];
  const stats    = window.OPEN_PROBLEMS?.stats || {};

  const kinds = useMemo(() => {
    const s = new Set(PROBLEMS.map(p => p.kind));
    return ["ALL", ...Array.from(s).sort()];
  }, [PROBLEMS]);

  const filtered = useMemo(() => {
    if (kindFilter === "ALL") return PROBLEMS;
    return PROBLEMS.filter(p => p.kind === kindFilter);
  }, [PROBLEMS, kindFilter]);

  const selected = filtered[selectedIdx] || filtered[0];

  // arXivis brain reused — same concept universe, but the highlighted set is
  // the problem's involved concepts (drawn red/coral instead of amber, so
  // user can distinguish "this paper activates X" from "this gap involves X").
  const customNodes = useMemo(
    () => window.ARXIVIS?.concept_universe || [],
    []
  );
  const customLinks = useMemo(
    () => window.ARXIVIS?.concept_edges || [],
    []
  );

  const involvedSet = useMemo(() => {
    if (!selected) return new Set();
    return new Set(selected.concepts.map(c => c.replace(/^wiki:/, "")));
  }, [selected]);

  // Auto-zoom to the involved concepts whenever problem changes
  useEffect(() => {
    if (!selected || !graphRef.current) return;
    const t = setTimeout(() => {
      graphRef.current?.fitToSet?.(involvedSet, 140);
    }, 350);
    return () => clearTimeout(t);
  }, [selected?.title, involvedSet]);

  if (!window.OPEN_PROBLEMS) {
    return (
      <div style={{
        position: "fixed", inset: 0, zIndex: 100,
        background: "var(--c-bg)", color: "var(--c-ink)",
        display: "grid", placeItems: "center", padding: 24, textAlign: "center",
      }}>
        <div>
          <h2>open_problems data not loaded</h2>
          <p style={{ opacity: 0.7, maxWidth: 520, margin: "12px auto" }}>
            Run <code>python3 scripts/build_open_problems.py</code> to
            generate <code>design/open_problems.js</code>.
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
      gridTemplateColumns: narrow ? "1fr" : "minmax(320px, 26%) minmax(0, 1fr) minmax(320px, 28%)",
      gridTemplateRows: narrow ? "auto 1fr auto auto" : "auto 1fr",
    }}>
      {/* TOP BAR */}
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
        }}>open problems · gaps the corpus hasn't filled</div>
        <div style={{ flex: 1 }} />
        <span style={{ fontFamily: "var(--f-mono)", fontSize: 11, opacity: 0.6 }}>
          {filtered.length} of {PROBLEMS.length} · {stats.missing_bridges || 0} bridges · {stats.underexplored || 0} underexplored · {stats.stale_clusters || 0} stale
        </span>
      </div>

      {/* LEFT — problem list */}
      <aside style={{
        borderRight: narrow ? "none" : "1px solid var(--c-line)",
        borderBottom: narrow ? "1px solid var(--c-line)" : "none",
        background: "var(--c-bg-elev)",
        overflow: "hidden", display: "flex", flexDirection: "column",
        maxHeight: narrow ? 320 : "none",
      }}>
        <div style={{
          padding: "8px 14px", borderBottom: "1px solid var(--c-line)",
          display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center",
        }}>
          <span style={{ fontSize: 11, opacity: 0.55, fontFamily: "var(--f-mono)" }}>KIND</span>
          {kinds.map(k => (
            <button key={k}
              onClick={() => { setKindFilter(k); setSelectedIdx(0); }}
              style={{
                padding: "4px 10px", fontSize: 11.5,
                background: kindFilter === k ? "var(--c-ink)" : "transparent",
                color:      kindFilter === k ? "var(--c-bg)" : "var(--c-ink-muted)",
                border: "1px solid var(--c-line)",
                borderRadius: 999, cursor: "pointer",
              }}>
              {k}
            </button>
          ))}
        </div>
        <div style={{ overflowY: "auto", flex: 1 }}>
          {filtered.map((p, i) => (
            <button key={p.title + i}
              onClick={() => setSelectedIdx(i)}
              style={{
                display: "block", width: "100%", textAlign: "left",
                padding: "10px 14px",
                borderBottom: "1px solid var(--c-line)",
                background: i === selectedIdx ? "color-mix(in oklch, var(--c-ink) 8%, transparent)" : "transparent",
                cursor: "pointer", border: "none",
                borderLeft: i === selectedIdx ? "3px solid #F96167" : "3px solid transparent",
                color: "var(--c-ink)",
              }}>
              <div style={{
                display: "flex", justifyContent: "space-between", alignItems: "baseline",
                gap: 8, marginBottom: 4,
              }}>
                <span style={{
                  fontFamily: "var(--f-mono)", fontSize: 10,
                  color: kindColor(p.kind), letterSpacing: "0.08em",
                  textTransform: "uppercase",
                }}>
                  {p.kind.replace(/_/g, " ")}
                </span>
                <span title="open-problem score" style={{
                  fontFamily: "var(--f-mono)", fontSize: 11, opacity: 0.85,
                }}>
                  ◇ {p.score.toFixed(1)}
                </span>
              </div>
              <div style={{ fontSize: 13.5, lineHeight: 1.35, fontWeight: 500 }}>
                {p.title}
              </div>
            </button>
          ))}
        </div>
      </aside>

      {/* CENTER — brain w/ involved concepts highlighted in coral */}
      <div style={{ position: "relative" }}>
        <BrainGraph3D
          ref={graphRef}
          customNodes={customNodes}
          customLinks={customLinks}
          highlightSet={involvedSet}
          showLabels="hubs"
          cinematic={true}
          signalFlow={false}
          linkOpacity={0.5}
          linkWidth={1.4}
          linkColor="#0a0e22"
          background="var(--c-bg)"
        />
        {selected && involvedSet.size > 0 && (
          <div style={{
            position: "absolute", top: 16, left: 16,
            maxWidth: 420,
            padding: "12px 16px",
            background: "color-mix(in oklch, var(--c-bg-elev) 94%, transparent)",
            backdropFilter: "blur(10px)",
            border: "1px solid var(--c-line)",
            borderRadius: 12,
            fontFamily: "var(--f-sans)", fontSize: 12.5,
            lineHeight: 1.5,
            color: "var(--c-ink)",
          }}>
            <div style={{
              fontFamily: "var(--f-mono)", fontSize: 10,
              color: kindColor(selected.kind), letterSpacing: "0.10em",
              textTransform: "uppercase", marginBottom: 8, fontWeight: 700,
            }}>
              {selected.kind.replace(/_/g, " ")} ◇ {selected.score.toFixed(1)}
            </div>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>
              {selected.title}
            </div>
            <div style={{ opacity: 0.75 }}>{selected.why}</div>
          </div>
        )}
      </div>

      {/* RIGHT — papers closest to addressing it + suggested foundations */}
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
              fontFamily: "var(--f-mono)", fontSize: 10, opacity: 0.55,
              letterSpacing: "0.10em", textTransform: "uppercase", marginBottom: 8,
            }}>
              Closest papers
            </div>
            {selected.closest_papers?.length > 0 ? (
              selected.closest_papers.map((cp, i) => (
                <div key={cp.id} style={{
                  padding: "10px 12px", marginBottom: 8,
                  border: "1px solid var(--c-line)",
                  borderRadius: 8,
                  background: "color-mix(in oklch, var(--c-bg) 60%, transparent)",
                }}>
                  <div style={{
                    display: "flex", justifyContent: "space-between",
                    marginBottom: 4, fontFamily: "var(--f-mono)", fontSize: 10,
                    opacity: 0.65,
                  }}>
                    <span>match overlap {cp.overlap}</span>
                    <span>◆ {(cp.novelty || 0).toFixed(1)}</span>
                  </div>
                  <div style={{ fontSize: 12.5, lineHeight: 1.35 }}>
                    {cp.title}
                  </div>
                </div>
              ))
            ) : (
              <div style={{ fontSize: 12, opacity: 0.55, marginBottom: 12 }}>
                No corpus paper currently touches these concepts — wide-open territory.
              </div>
            )}

            <div style={{
              marginTop: 16,
              fontFamily: "var(--f-mono)", fontSize: 10, opacity: 0.55,
              letterSpacing: "0.10em", textTransform: "uppercase", marginBottom: 8,
            }}>
              Suggested foundations
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {selected.suggested_foundations.map(f => (
                <button key={f.id}
                  onClick={() => onJumpToConcept?.(f.id)}
                  style={{
                    padding: "5px 12px", fontSize: 12,
                    background: "color-mix(in oklch, #1e6fa8 14%, transparent)",
                    border: "1px solid #1e6fa8",
                    borderRadius: 999, color: "var(--c-ink)", cursor: "pointer",
                  }}>
                  {f.name}
                  <span style={{ opacity: 0.55, marginLeft: 6 }}>({f.papers}p)</span>
                </button>
              ))}
            </div>

            <div style={{
              marginTop: 22,
              padding: "10px 12px",
              border: "1px dashed var(--c-line)",
              borderRadius: 8,
              fontSize: 11.5, lineHeight: 1.5, opacity: 0.7,
            }}>
              <span style={{
                fontFamily: "var(--f-mono)", fontSize: 9.5,
                color: "var(--c-ink-muted)", letterSpacing: "0.10em",
                textTransform: "uppercase", display: "block", marginBottom: 4,
              }}>What this means</span>
              {selected.kind === "missing_bridge" && (
                <>A paper that activates BOTH of these concepts together would
                earn high novelty bits — neither has been bridged in the corpus.</>
              )}
              {selected.kind === "underexplored" && (
                <>This concept is widely used as scaffolding but rarely centered.
                A focused study on it would fill a deeply-cited gap.</>
              )}
              {selected.kind === "stale_cluster" && (
                <>This research community has slowed. A fresh contribution here
                would re-activate a quiet region of the brain.</>
              )}
            </div>
          </>
        )}
      </aside>
    </div>
  );
}

function kindColor(kind) {
  if (kind === "missing_bridge") return "#F96167";
  if (kind === "underexplored")  return "#FBB036";
  if (kind === "stale_cluster")  return "#9B59B6";
  return "var(--c-ink-muted)";
}

window.OpenProblems = OpenProblems;
