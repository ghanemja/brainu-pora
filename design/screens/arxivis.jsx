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
  const [sortBy, setSortBy] = useState("composite");      // composite | novelty | year | rigor
  const [sourceFilter, setSourceFilter] = useState("ALL"); // ALL | arXiv | NTRS | DTIC | …
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState(null);
  const [flythrough, setFlythrough] = useState(false);
  const [flyIdx, setFlyIdx] = useState(0);
  const [ingestOpen, setIngestOpen] = useState(false);

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

  // Search-relevance score: title + concept-name token match
  const relevanceFor = (p, q) => {
    if (!q) return 0;
    const ql = q.toLowerCase();
    let s = 0;
    const title = (p.title || "").toLowerCase();
    if (title.includes(ql)) s += 30;
    for (const c of p.concepts || []) {
      const n = (c.name || "").toLowerCase();
      if (n.includes(ql)) s += 12 + (c.weight || 0) * 0.5;
    }
    for (const innov of p.innovations || []) {
      if ((innov.phrase || "").toLowerCase().includes(ql)) s += 8;
    }
    return s;
  };

  const filtered = useMemo(() => {
    let xs = PAPERS;
    if (sourceFilter !== "ALL") xs = xs.filter(p => p.source === sourceFilter);
    xs = [...xs];
    const q = search.trim();
    if (q) {
      // Restrict to anything that scores above zero, then sort by
      // relevance × composite (search-aware ranking).
      xs = xs.map(p => ({ p, rel: relevanceFor(p, q) }))
             .filter(x => x.rel > 0)
             .sort((a, b) => (b.rel * (1 + (b.p.composite || 0) / 100))
                            - (a.rel * (1 + (a.p.composite || 0) / 100)))
             .map(x => x.p);
      return xs;
    }
    if (sortBy === "composite") xs.sort((a,b) => (b.composite || 0) - (a.composite || 0));
    if (sortBy === "novelty")   xs.sort((a,b) => b.novelty_bits - a.novelty_bits);
    if (sortBy === "rigor")     xs.sort((a,b) => (b.rigor?.total || 0) - (a.rigor?.total || 0));
    if (sortBy === "year")      xs.sort((a,b) => (b.year || 0) - (a.year || 0));
    return xs;
  }, [PAPERS, sortBy, sourceFilter, search]);

  const selected = useMemo(
    () => filtered.find(p => p.id === selectedId) || filtered[0],
    [filtered, selectedId]
  );

  // arXivis brain = concept universe assembled from ALL kept papers.
  // Far broader than BU_DATA.NODES (which is only ~75 hub concepts).
  const customNodes = useMemo(
    () => window.ARXIVIS?.concept_universe || [],
    []
  );
  const customLinks = useMemo(
    () => window.ARXIVIS?.concept_edges || [],
    []
  );
  const universeIdSet = useMemo(
    () => new Set(customNodes.map(n => n.id)),
    [customNodes]
  );

  // Map paper-activated wiki ids onto graph node ids that actually exist
  const activatedGraphNodes = useMemo(() => {
    if (!selected) return [];
    return selected.concepts
      .map(c => c.id.replace(/^wiki:/, ""))
      .filter(id => universeIdSet.has(id));
  }, [selected, universeIdSet]);

  // Memoize activated set for highlightSet prop
  const activatedSet = useMemo(
    () => new Set(activatedGraphNodes),
    [activatedGraphNodes]
  );

  // "What this paper connects" — map activated concepts back to the
  // universe by paper-degree (foundational vs introduced) and skip
  // concepts that just echo the title.
  const connectionsBlurb = useMemo(() => {
    if (!selected) return null;
    const titleLc = (selected.title || "").toLowerCase();
    const tokenInTitle = (name) =>
      name.toLowerCase().split(/[\s-]+/)
          .some(t => t.length > 3 && titleLc.includes(t));

    // Universe degree (paper count activating each concept)
    const universe = window.ARXIVIS?.concept_universe || [];
    const degreeOf = {};
    for (const n of universe) degreeOf[n.id] = n.degree || 1;

    const acts = (selected.concepts || []).map(c => {
      const slug = c.id.replace(/^wiki:/, "");
      return {
        id:        slug,
        name:      c.name,
        weight:    c.weight,
        degree:    degreeOf[slug] || 1,
        echoes:    tokenInTitle(c.name),
      };
    });
    if (!acts.length) return null;

    const corpusSize = window.ARXIVIS?.papers?.length || 500;
    // Foundations: high paper-degree, not echoing the title
    const foundations = acts
      .filter(a => !a.echoes)
      .sort((a, b) => b.degree - a.degree)
      .slice(0, 3);
    // Paper-introduced: lowest degree (≤2 papers ever activate it)
    const introduced = acts
      .filter(a => a.degree <= 2)
      .sort((a, b) => a.degree - b.degree)
      .slice(0, 3);

    return {
      foundations,
      introduced,
      total_concepts: acts.length,
      total_edges:    selected.pair_edges?.length || 0,
      corpus_size:    corpusSize,
    };
  }, [selected]);

  // Zoom camera to fit just the activated nodes whenever paper changes
  useEffect(() => {
    if (activatedGraphNodes.length === 0 || !graphRef.current) return;
    const t = setTimeout(() => {
      graphRef.current?.fitToSet?.(activatedSet, 120);
    }, 350);
    return () => clearTimeout(t);
  }, [selected?.id, activatedSet]);

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
      gridTemplateColumns: narrow ? "1fr" : "minmax(200px, 16%) minmax(0, 1fr) minmax(640px, 52%)",
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
        <button
          className="btn"
          onClick={() => setIngestOpen(true)}
          style={{
            padding: "6px 14px", fontSize: 12,
            background: "var(--c-bridge)", color: "var(--c-bg)",
            borderRadius: 999, fontWeight: 600,
          }}>
          + Ingest paper
        </button>
        <span style={{ fontFamily: "var(--f-mono)", fontSize: 11, opacity: 0.6 }}>
          {filtered.length} papers · {stats.concepts_in_vocab} concept manifold · {stats.papers_with_acts} activated of {stats.total_papers_scanned} scanned
        </span>
      </div>
      {ingestOpen && <IngestModal onClose={() => setIngestOpen(false)} />}

      {/* LEFT — paper list */}
      <aside style={{
        borderRight: narrow ? "none" : "1px solid var(--c-line)",
        borderBottom: narrow ? "1px solid var(--c-line)" : "none",
        overflow: "hidden", display: "flex", flexDirection: "column",
        background: "var(--c-bg-elev)",
        maxHeight: narrow ? 280 : "none",
      }}>
        <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--c-line)" }}>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="🔎 Search by concept or claim…"
            style={{
              width: "100%", padding: "8px 12px", fontSize: 12.5,
              fontFamily: "var(--f-sans)",
              border: "1px solid var(--c-line-strong)",
              borderRadius: 999,
              background: "var(--c-bg)", color: "var(--c-ink)",
              outline: "none",
            }} />
        </div>
        <div style={{
          padding: "10px 14px", borderBottom: "1px solid var(--c-line)",
          display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center",
        }}>
          <span style={{ fontSize: 11, opacity: 0.55, fontFamily: "var(--f-mono)" }}>SORT</span>
          {["composite", "novelty", "rigor", "year"].map(s => (
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
                <span title="composite (novelty + rigor)" style={{
                  fontFamily: "var(--f-mono)", fontSize: 11, opacity: 0.9,
                }}>
                  ◆ {(p.composite ?? p.novelty_bits ?? 0).toFixed(1)}
                </span>
              </div>
              <div style={{ fontSize: 13.5, lineHeight: 1.35, fontWeight: 500 }}>
                {p.title}
              </div>
              <div style={{ fontSize: 11, opacity: 0.55, marginTop: 4 }}>
                {p.concepts.slice(0, 3).map(c => c.name).join(" · ")}
              </div>
              {p.rigor && (
                <div style={{
                  marginTop: 6,
                  display: "flex", gap: 6, alignItems: "center", flexWrap: "wrap",
                  fontFamily: "var(--f-mono)", fontSize: 10,
                }}>
                  <span style={{ color: "#60FFA8" }}>● {p.rigor.flags.green.length}</span>
                  <span style={{ color: "#F96167" }}>● {p.rigor.flags.red.length}</span>
                  <span style={{ opacity: 0.45 }}>
                    {p.rigor.scores.peer_reviewed ? "peer-reviewed" : "preprint"}
                    {p.rigor.scores.replication?.code ? " · code" : ""}
                  </span>
                </div>
              )}
            </button>
          ))}
        </div>
      </aside>

      {/* CENTER — 3D graph (arXivis concept universe, not BU_DATA hubs) */}
      <div style={{ position: "relative" }}>
        <BrainGraph3D
          ref={graphRef}
          customNodes={customNodes}
          customLinks={customLinks}
          tourPath={activatedGraphNodes}
          highlightSet={activatedSet}
          currentNode={activatedGraphNodes[flyIdx] || null}
          showLabels="hubs"
          cinematic={!flythrough}
          signalFlow={true}
          linkOpacity={0.55}
          linkWidth={1.6}
          linkColor="#0a0e22"
          background="var(--c-bg)"
        />

        {/* Helper card pinned top-left when a paper is selected — explains
            what the activated subgraph means in plain words.
            Foundations = concepts the paper RESTS ON (high paper-degree across
            the corpus, not echoing title). Introduced = concepts only this
            paper (or 1-2 others) activate. Both colors chosen for
            light-palette legibility — no fluorescent on cream. */}
        {selected && activatedGraphNodes.length > 0 && !flythrough && connectionsBlurb && (
          <div style={{
            position: "absolute", top: 16, left: 16,
            maxWidth: 400,
            padding: "12px 16px",
            background: "color-mix(in oklch, var(--c-bg-elev) 94%, transparent)",
            backdropFilter: "blur(10px)",
            border: "1px solid var(--c-line)",
            borderRadius: 12,
            fontFamily: "var(--f-sans)", fontSize: 12,
            lineHeight: 1.5,
            color: "var(--c-ink)",
          }}>
            <div style={{
              fontFamily: "var(--f-mono)", fontSize: 10,
              opacity: 0.55, letterSpacing: "0.10em",
              textTransform: "uppercase", marginBottom: 8,
            }}>
              Brain · where this paper sits
            </div>

            <div style={{ marginBottom: 8 }}>
              <span style={{ fontWeight: 600, color: "#c66a00" }}>
                {activatedGraphNodes.length} concept{activatedGraphNodes.length === 1 ? "" : "s"}
              </span>
              {" lit, "}
              <span style={{ fontWeight: 600, color: "#c66a00" }}>
                {connectionsBlurb.total_edges}
              </span>
              {" inferred edges. "}
            </div>

            {connectionsBlurb.foundations.length > 0 && (
              <div style={{ marginBottom: 6 }}>
                <span style={{
                  fontFamily: "var(--f-mono)", fontSize: 10,
                  color: "#1e6fa8", letterSpacing: "0.06em",
                  textTransform: "uppercase", fontWeight: 700, marginRight: 6,
                }}>Builds on</span>
                {connectionsBlurb.foundations.map((c, i) => (
                  <span key={c.id}>
                    {i > 0 ? ", " : ""}
                    <span style={{ fontWeight: 600 }}>{c.name}</span>
                    <span style={{ opacity: 0.55, fontSize: 11 }}>
                      {" "}({c.degree}/{connectionsBlurb.corpus_size} papers)
                    </span>
                  </span>
                ))}
                .
              </div>
            )}

            {connectionsBlurb.introduced.length > 0 && (
              <div style={{ marginBottom: 6 }}>
                <span style={{
                  fontFamily: "var(--f-mono)", fontSize: 10,
                  color: "#a04a14", letterSpacing: "0.06em",
                  textTransform: "uppercase", fontWeight: 700, marginRight: 6,
                }}>Introduces</span>
                {connectionsBlurb.introduced.map((c, i) => (
                  <span key={c.id}>
                    {i > 0 ? ", " : ""}
                    <span style={{ fontWeight: 600 }}>{c.name}</span>
                    {c.degree > 1 && (
                      <span style={{ opacity: 0.55, fontSize: 11 }}>
                        {" "}(also seen in {c.degree - 1} other{c.degree - 1 === 1 ? "" : "s"})
                      </span>
                    )}
                  </span>
                ))}
                .
              </div>
            )}

            <div style={{
              fontFamily: "var(--f-mono)", fontSize: 9.5,
              opacity: 0.55, letterSpacing: "0.04em",
              marginTop: 8, paddingTop: 6, borderTop: "1px solid var(--c-line)",
            }}>
              <span style={{ color: "#1e6fa8" }}>builds on</span> = foundational concepts elsewhere in corpus
              {" · "}
              <span style={{ color: "#a04a14" }}>introduces</span> = first or near-first use in our corpus
            </div>
          </div>
        )}

        {/* Bottom HUD: KEY FINDING (one-liner) + flythrough controls.
            Long pitch text moved to the paper card so the brain stays the focus. */}
        {selected && (
          <div style={{
            position: "absolute", bottom: 0, left: 0, right: 0,
            padding: "18px 22px",
            background: "linear-gradient(0deg, color-mix(in oklch, var(--c-bg) 92%, transparent) 0%, transparent 100%)",
            pointerEvents: "none",
          }}>
            <div style={{
              maxWidth: 720, margin: "0 auto",
              background: "color-mix(in oklch, var(--c-bg-elev) 88%, transparent)",
              backdropFilter: "blur(10px)",
              border: "1px solid var(--c-line)",
              borderRadius: "var(--r-lg, 12px)",
              padding: "10px 16px",
              pointerEvents: "auto",
              display: "flex", alignItems: "center", gap: 14,
            }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{
                  fontFamily: "var(--f-mono)", fontSize: 9,
                  color: "#60FFA8", letterSpacing: "0.12em",
                  textTransform: "uppercase", marginBottom: 3,
                }}>
                  Key finding
                </div>
                <div style={{
                  fontSize: 13.5, lineHeight: 1.35, fontWeight: 500,
                  whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
                }} title={selected.key_finding || selected.pitch}>
                  {selected.key_finding || (selected.pitch || "").split(/[.!?]/)[0]}
                </div>
              </div>
              <button className="btn"
                onClick={() => setFlythrough(f => !f)}
                style={{ padding: "5px 14px", fontSize: 11.5, flex: "0 0 auto" }}>
                {flythrough ? "⏸ Pause" : "▶ Fly through"}
              </button>
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

      {/* RIGHT — video-first paper card. Video sits at the top, prominent,
          and the rest of the metadata scrolls below as supplement. */}
      <aside style={{
        borderLeft: narrow ? "none" : "1px solid var(--c-line)",
        borderTop:  narrow ? "1px solid var(--c-line)" : "none",
        background: "var(--c-bg-elev)",
        overflowY: "auto",
        padding: 0,
        maxHeight: narrow ? 320 : "none",
      }}>
        {selected && (
          <div style={{
            display: "grid",
            gridTemplateColumns: narrow ? "1fr" : "minmax(320px, 50%) minmax(0, 1fr)",
            alignItems: "start",
          }}>

          {/* LEFT COLUMN — video, sticky so it stays visible while text scrolls.
              Sized to fill the viewport height under the topbar so the 9:16
              video has room to breathe. */}
          <div style={{
            position: narrow ? "static" : "sticky",
            top: 0,
            height: narrow ? "auto" : "calc(100vh - 56px)",
            borderRight: narrow ? "none" : "1px solid var(--c-line)",
            borderBottom: narrow ? "1px solid var(--c-line)" : "none",
            background: "var(--c-bg-elev-2, var(--c-bg-elev))",
            alignSelf: "start",
            display: "flex", flexDirection: "column",
          }}>
            <PaperVideo paperId={selected.id} hero fillHeight={!narrow} />
          </div>

          {/* RIGHT COLUMN — all word details */}
          <div>

            {/* Title + key finding strip */}
            <div style={{ padding: "16px 20px 6px" }}>
              <div style={{
                fontFamily: "var(--f-mono)", fontSize: 10,
                color: badgeColor(selected.source), letterSpacing: "0.10em",
                marginBottom: 6,
              }}>
                {selected.source}{selected.year ? ` · ${selected.year}` : ""}
                {selected.category_hint ? ` · ${selected.category_hint}` : ""}
              </div>
              <h2 style={{
                fontSize: 17, lineHeight: 1.3, margin: "0 0 10px 0",
                fontFamily: "var(--f-display, var(--f-sans))",
              }}>
                {selected.title}
              </h2>

              {selected.key_finding && (
                <div style={{
                  padding: "10px 12px", marginBottom: 12,
                  border: "1px solid #60FFA8",
                  borderLeft: "3px solid #60FFA8",
                  borderRadius: 8,
                  background: "color-mix(in oklch, #60FFA8 6%, transparent)",
                  fontSize: 13, lineHeight: 1.5,
                }}>
                  <span style={{
                    fontFamily: "var(--f-mono)", fontSize: 9,
                    color: "#60FFA8", letterSpacing: "0.12em",
                    textTransform: "uppercase", display: "block", marginBottom: 4,
                  }}>
                    Key finding
                  </span>
                  {selected.key_finding}
                </div>
              )}
            </div>

            <div style={{ padding: "0 20px 18px" }}>

            {selected.url && (
              <a href={selected.url} target="_blank" rel="noreferrer"
                 style={{ fontSize: 12, color: "var(--c-bridge, #1e6fa8)" }}>
                Open source ↗
              </a>
            )}

            {/* Body — single column inside the text panel now that
                video lives in its own outer column. */}
            <div style={{ marginTop: 16 }}>

            {/* Novelty + concepts */}
            <div>

            {/* Novelty breakdown */}
            <div style={{
              padding: 14,
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
            <div style={{ marginTop: 16 }}>
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

            </div>{/* /Novelty + concepts */}

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

            {/* Research-assistant panel — 10-criteria rigor scoring */}
            {selected.rigor && (
              <ResearchAssistantPanel rigor={selected.rigor} composite={selected.composite} />
            )}

            {/* Full pitch — supplement only, after video */}
            {selected.pitch && (
              <details style={{
                marginTop: 14, fontSize: 12, lineHeight: 1.55,
              }}>
                <summary style={{
                  cursor: "pointer", opacity: 0.55,
                  fontFamily: "var(--f-mono)", fontSize: 10,
                  letterSpacing: "0.10em", textTransform: "uppercase",
                  marginBottom: 6,
                }}>Abstract excerpt</summary>
                <div style={{ opacity: 0.75 }}>{selected.pitch}</div>
              </details>
            )}

            </div>

            {/* Activation edges count */}
            <div style={{ marginTop: 18, fontSize: 11.5, opacity: 0.55 }}>
              <strong>{selected.pair_edges?.length || 0}</strong> concept-pair edges activated
              · highlighted amber in brain
            </div>
            </div>
          </div>
          </div>
        )}
      </aside>
    </div>
  );
}

function ResearchAssistantPanel({ rigor, composite }) {
  const [open, setOpen] = useState(true);
  return (
    <div style={{
      marginTop: 18,
      border: "1px solid var(--c-line)",
      borderRadius: 10,
      background: "color-mix(in oklch, var(--c-bg) 60%, transparent)",
      overflow: "hidden",
    }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          display: "flex", width: "100%", padding: "10px 14px",
          justifyContent: "space-between", alignItems: "center",
          background: "transparent", border: "none", cursor: "pointer",
          color: "var(--c-ink)",
        }}>
        <span style={{
          fontFamily: "var(--f-mono)", fontSize: 10,
          color: "var(--c-ink-muted)", letterSpacing: "0.10em",
          textTransform: "uppercase",
        }}>
          Research assistant · 10-criteria check
        </span>
        <span style={{
          fontFamily: "var(--f-mono)", fontSize: 11,
        }}>
          <span style={{ color: "#60FFA8" }}>● {rigor.flags.green.length}</span>{" "}
          <span style={{ color: "#F96167" }}>● {rigor.flags.red.length}</span>
          {" · "}
          <span style={{ opacity: 0.55 }}>rigor {rigor.total}</span>
        </span>
      </button>

      {open && (
        <div style={{ padding: "10px 14px", borderTop: "1px solid var(--c-line)" }}>
          <div style={{ fontSize: 12.5, lineHeight: 1.5, marginBottom: 10 }}>
            {rigor.summary}
          </div>

          {rigor.flags.green.length > 0 && (
            <div style={{ marginBottom: 6 }}>
              {rigor.flags.green.map((g, i) => (
                <div key={i} style={{
                  display: "flex", gap: 6, alignItems: "flex-start",
                  fontSize: 11.5, lineHeight: 1.4, marginBottom: 3,
                }}>
                  <span style={{ color: "#60FFA8", flex: "0 0 auto" }}>●</span>
                  <span>{g}</span>
                </div>
              ))}
            </div>
          )}
          {rigor.flags.red.length > 0 && (
            <div>
              {rigor.flags.red.map((r, i) => (
                <div key={i} style={{
                  display: "flex", gap: 6, alignItems: "flex-start",
                  fontSize: 11.5, lineHeight: 1.4, marginBottom: 3,
                }}>
                  <span style={{ color: "#F96167", flex: "0 0 auto" }}>●</span>
                  <span>{r}</span>
                </div>
              ))}
            </div>
          )}

          {/* 10-criteria grid */}
          <div style={{
            marginTop: 12, padding: "10px 0 0",
            borderTop: "1px solid var(--c-line)",
            display: "grid", gridTemplateColumns: "1fr 1fr",
            gap: "4px 12px",
            fontFamily: "var(--f-mono)", fontSize: 10.5,
          }}>
            {[
              ["evidence",       rigor.scores.evidence_label],
              ["preliminary",    rigor.scores.preliminary ? "yes (flag)" : "no"],
              ["causation",      rigor.scores.causation_note],
              ["ablations",      rigor.scores.ablation ? "present" : "—"],
              ["industry",       (rigor.scores.industry_affiliations || []).join(", ") || "—"],
              ["venue",          rigor.scores.venue],
              ["replication",    rigor.scores.replication?.code ? "code released" : (rigor.scores.replication?.data ? "data released" : "—")],
              ["sample size",    rigor.scores.sample_label || "—"],
              ["risk framing",   rigor.scores.risk_framing_ok ? "ok" : "relative-only"],
              ["p-value",        rigor.scores.pvalue_reported ? "reported" : (rigor.scores.significance_claimed ? "claimed (no p)" : "—")],
            ].map(([k, v], i) => (
              <React.Fragment key={k}>
                <span style={{ opacity: 0.55 }}>{i + 1}. {k}</span>
                <span style={{ textAlign: "right" }}>{v}</span>
              </React.Fragment>
            ))}
          </div>

          {rigor.scores.replication?.url && (
            <a href={rigor.scores.replication.url} target="_blank" rel="noreferrer"
               style={{ display: "block", marginTop: 10, fontSize: 11,
                        color: "#60FFA8", fontFamily: "var(--f-mono)" }}>
              ↗ {rigor.scores.replication.url}
            </a>
          )}
        </div>
      )}
    </div>
  );
}

function PaperVideo({ paperId, hero = false, fillHeight = false }) {
  const src = window.ARXIVIS_VIDEOS?.[paperId];
  // Theme-matched soft surface — no more hard black.
  const SURFACE = "var(--c-bg-elev-2, var(--c-bg-elev))";

  if (!src) {
    return (
      <div style={{
        margin: hero ? "0" : "18px 0 0",
        padding: hero ? "60px 20px" : 14,
        border: hero ? "none" : "1px dashed var(--c-line)",
        borderBottom: hero ? "1px solid var(--c-line)" : undefined,
        background: SURFACE,
        color: "var(--c-ink-muted)",
        borderRadius: hero ? 0 : 10,
        fontSize: 12, opacity: 0.85, textAlign: "center",
        flex: fillHeight ? 1 : "0 0 auto",
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
      background: SURFACE,
      borderBottom: hero ? "1px solid var(--c-line)" : "none",
      borderRadius: hero ? 0 : 12,
      border: hero ? "none" : "1px solid var(--c-line)",
      overflow: "hidden",
      display: "flex", flexDirection: "column",
      flex: fillHeight ? 1 : "0 0 auto",
      minHeight: 0,
    }}>
      <div style={{
        padding: "8px 14px",
        fontFamily: "var(--f-mono)", fontSize: 10,
        color: "#5BD3A1", letterSpacing: "0.10em",
        textTransform: "uppercase",
        background: "color-mix(in oklch, var(--c-cs, #60FFA8) 10%, transparent)",
        borderBottom: "1px solid color-mix(in oklch, var(--c-cs, #60FFA8) 24%, transparent)",
        display: "flex", justifyContent: "space-between", alignItems: "center",
        flex: "0 0 auto",
      }}>
        <span>30-sec explainer · 9:16</span>
        <span style={{ opacity: 0.5 }}>tap to learn</span>
      </div>
      <video src={src} controls autoPlay loop muted playsInline
             style={{
               display: "block",
               width: "100%",
               height: fillHeight ? "100%" : "auto",
               maxHeight: fillHeight ? "none" : (hero ? 640 : 520),
               objectFit: "contain",
               background: SURFACE,
               flex: fillHeight ? 1 : "0 0 auto",
               minHeight: 0,
             }} />
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

// ─────────────────────────────────────────────────────────────────
// INGEST MODAL — drop an arXiv URL, watch the cascade.
// Streams /paper/drop SSE if backend up at :8090, else animates demo.
// ─────────────────────────────────────────────────────────────────

const INGEST_STAGES = [
  { id: "resolved",   label: "Resolve arXiv ID",        detail: "Extract canonical paper ID from URL." },
  { id: "fetched",    label: "Fetch metadata",          detail: "Pull title, abstract, authors via arXiv API." },
  { id: "enriched",   label: "Semantic Scholar lookup", detail: "SPECTER2 embedding + TLDR + citation graph." },
  { id: "classified", label: "Classify into cluster",   detail: "Embedding cosine vs cluster centroids; keyword fallback." },
  { id: "ingested",   label: "Add to corpus",            detail: "Append to defense_corpus_samples.json." },
  { id: "podcast_ready", label: "Generate 30s video",    detail: "Render activation pattern over the brain manifold." },
];

function IngestModal({ onClose }) {
  const [url, setUrl] = useState("");
  const [running, setRunning] = useState(false);
  const [stage, setStage] = useState(-1);
  const [log, setLog] = useState([]);

  const run = async () => {
    if (!url.trim()) return;
    setRunning(true); setStage(0); setLog([{ stage: "resolve", msg: `Resolving "${url.trim()}"…` }]);
    let usedBackend = false;
    try {
      const resp = await fetch("http://localhost:8090/paper/drop", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url.trim() }),
      });
      if (resp.ok && resp.body) {
        usedBackend = true;
        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        let buf = "";
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          const events = buf.split("\n\n");
          buf = events.pop();
          for (const evt of events) {
            const m = evt.match(/data:\s*(.+)/);
            if (!m) continue;
            try {
              const j = JSON.parse(m[1]);
              const kind = j.kind || j.stage;
              const data = j.data || {};
              const idx = INGEST_STAGES.findIndex(s => s.id === kind);
              if (idx >= 0) setStage(idx);
              const msg = summarizeIngestEvent(kind, data);
              setLog(prev => [...prev, { stage: kind, msg }]);
            } catch {}
          }
        }
      }
    } catch {}
    if (!usedBackend) {
      for (let i = 0; i < INGEST_STAGES.length; i++) {
        await new Promise(r => setTimeout(r, 700));
        setStage(i);
        setLog(prev => [...prev, { stage: INGEST_STAGES[i].id, msg: INGEST_STAGES[i].detail }]);
      }
      setLog(prev => [...prev, { stage: "done", msg: "Demo finished — start uvicorn api.server:app --port 8090 to ingest for real." }]);
    }
    setRunning(false);
  };

  return (
    <div
      onClick={(e) => { if (e.target === e.currentTarget && !running) onClose(); }}
      style={{
        position: "fixed", inset: 0, zIndex: 200,
        background: "rgba(8, 12, 24, 0.7)",
        backdropFilter: "blur(8px)",
        display: "grid", placeItems: "center", padding: 24,
      }}>
      <div style={{
        width: "min(640px, 100%)",
        background: "var(--c-bg-elev)",
        border: "1px solid var(--c-line-strong)",
        borderRadius: 12,
        padding: 24,
        boxShadow: "0 20px 60px rgba(0,0,0,0.4)",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
          <div>
            <div className="t-tag" style={{ color: "var(--c-bridge)" }}>INGEST NEW PAPER</div>
            <h2 className="t-h1" style={{ margin: "6px 0 4px", fontSize: 22 }}>Drop a paper. Watch it land.</h2>
          </div>
          <button className="btn ghost" onClick={onClose} disabled={running} style={{ padding: "4px 10px" }}>✕</button>
        </div>
        <p className="t-cap" style={{ margin: "0 0 16px" }}>
          Paste any arXiv URL. The system resolves it, classifies it into the closest cluster on the manifold,
          adds it to the corpus, and renders a 30-second activation video.
        </p>

        <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
          <input
            type="text"
            placeholder="https://arxiv.org/abs/2310.06825"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={running}
            style={{
              flex: 1, padding: "10px 14px",
              background: "var(--c-bg)",
              border: "1px solid var(--c-line)",
              borderRadius: 6, color: "var(--c-ink)",
              fontFamily: "var(--f-mono)", fontSize: 13,
              outline: "none",
            }}
          />
          <button
            onClick={run}
            disabled={running || !url.trim()}
            style={{
              padding: "10px 18px", fontSize: 13, fontWeight: 600,
              background: running ? "var(--c-line)" : "var(--c-bridge)",
              color: running ? "var(--c-ink-muted)" : "var(--c-bg)",
              border: "none", borderRadius: 6,
              cursor: running ? "not-allowed" : "pointer",
            }}>
            {running ? "Running…" : "▸ Drop"}
          </button>
        </div>

        {(running || stage >= 0) && (
          <>
            <div style={{ display: "flex", gap: 6, marginBottom: 14 }}>
              {INGEST_STAGES.map((s, i) => {
                const done = (i < stage) || (!running && i <= stage);
                const active = i === stage && running;
                return (
                  <div key={s.id} style={{ flex: 1 }}>
                    <div style={{
                      height: 5, borderRadius: 3,
                      background: done ? "var(--c-cs)" : active ? "var(--c-bridge)" : "var(--c-line)",
                      transition: "background 200ms",
                    }} />
                    <div style={{
                      fontSize: 10, marginTop: 6, lineHeight: 1.3,
                      color: done || active ? "var(--c-ink)" : "var(--c-ink-muted)",
                      fontFamily: "var(--f-mono)",
                    }}>
                      {String(i + 1).padStart(2, "0")} {s.label}
                    </div>
                  </div>
                );
              })}
            </div>
            <div style={{
              background: "var(--c-bg)", padding: 12, borderRadius: 6,
              border: "1px solid var(--c-line)",
              fontFamily: "var(--f-mono)", fontSize: 11.5, lineHeight: 1.6,
              maxHeight: 180, overflowY: "auto",
            }}>
              {log.map((l, i) => (
                <div key={i}>
                  <span style={{ color: "var(--c-ink-muted)" }}>[{l.stage}]</span>{" "}
                  <span style={{ color: "var(--c-ink)" }}>{l.msg}</span>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

// Pull a human one-liner out of each cascade SSE event.
function summarizeIngestEvent(kind, data) {
  if (!data) return kind;
  switch (kind) {
    case "resolved":  return `paper id: ${data.paper_id}`;
    case "fetched":   return `${data.title || "(no title)"} — ${data.authors || ""}`;
    case "enriched": {
      const bits = [];
      if (data.tldr_excerpt) bits.push(`TLDR: ${data.tldr_excerpt.slice(0, 140)}`);
      if (data.citations != null) bits.push(`${data.citations} citations (${data.influential || 0} influential)`);
      if (data.venue) bits.push(`venue: ${data.venue}`);
      if (data.n_refs) bits.push(`${data.n_refs} refs`);
      if (data.has_embedding) bits.push("SPECTER2 ✓");
      return bits.join(" · ") || "no SemSch data";
    }
    case "classified":
      return `${data.cluster_name || "unclassified"} · score=${data.match_score} · method=${data.method}`;
    case "ingested":   return data.new_entry ? `added: ${data.paper_id}` : `already in corpus: ${data.paper_id}`;
    case "podcast_starting": return `generating ${data.length || "short"} podcast…`;
    case "podcast_ready":    return `podcast script: ${data.turns || 0} turns`;
    case "warn":      return `⚠ ${data.step}: ${data.error}`;
    case "error":     return `✗ ${data.reason || JSON.stringify(data)}`;
    case "done":      return `done — ${data.paper_id} → ${data.cluster_id || "unclassified"}`;
    case "final":     return data.ok ? `complete: ${data.paper?.title || ""}` : `failed: ${data.error}`;
    default:          return JSON.stringify(data).slice(0, 200);
  }
}

window.ArXivis = ArXivis;
