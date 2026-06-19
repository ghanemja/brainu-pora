/* global React, BU_DATA, BrainGraph3D, CourseChip, KindGlyph,
          MiniMap, Altitude, Evidence, Compass,
          SpanningTreeSimulator, BFSVisualizer, ApproximationRatioTuner,
          ConceptInteractive */

const { useState, useMemo, useEffect, useRef } = React;

// ─────────────────────────────────────────────────────────────────
// EXERCISE MAPPING — which interactive exercise per concept
//
// A handful of nodes get a bespoke, richly-crafted interactive. Every
// other node falls back to the universal ConceptInteractive (an Active
// Recall drill built from the lesson's own data), so EVERY lesson shows
// an interactive example — never a dead end.
// ─────────────────────────────────────────────────────────────────
function getExerciseForNode(nodeId) {
  // Map specific nodes to their bespoke interactive exercises.
  const exercises = {
    "spanning_tree": SpanningTreeSimulator,
    "Minimum_Spanning_Tree_MST": SpanningTreeSimulator,
    "breadth-first_search_BFS": BFSVisualizer,
    "distributed_graph_algorithms": BFSVisualizer,
    "2-approximation_algorithm": ApproximationRatioTuner,
    "Approximation_algorithms": ApproximationRatioTuner,
  };
  // Return the rich exercise if mapped; otherwise the "generic" sentinel.
  return exercises[nodeId] || "generic";
}

// Render the right interactive for a stop: bespoke component when one is
// mapped, otherwise the universal ConceptInteractive driven by `lesson`.
function renderExercise(nodeId, lesson) {
  const Comp = getExerciseForNode(nodeId);
  if (Comp === "generic") {
    return React.createElement(ConceptInteractive, { lesson });
  }
  return React.createElement(Comp);
}

// ─────────────────────────────────────────────────────────────────
// SCREEN 2 — THE WALK
// Lesson "postcard" with locked mini-map, next-stop preview, bridge button.
// Layout variants exposed as Tweak: postcard | split | full-bleed
// ─────────────────────────────────────────────────────────────────

function Walk({ tour, idx, onAdvance, onJumpTo, onBranch, onSummit, layout = "postcard", onShow3D }) {
  const stop = tour?.[idx];
  const lesson = useMemo(() => stop ? BU_DATA.lessonFor(stop.node) : null, [stop?.node]);
  const next = tour?.[idx + 1];
  const prev = tour?.[idx - 1];
  const [quizPicked, setQuizPicked] = useState(null);
  const [quizChecked, setQuizChecked] = useState(false);

  useEffect(() => {
    setQuizPicked(null);
    setQuizChecked(false);
  }, [stop?.node]);

  if (!stop || !lesson) {
    return <div style={{ padding: 60, textAlign: "center", color: "var(--c-ink-muted)" }}>
      No active tour. <button className="btn" onClick={onJumpTo}>Pick a starting concept →</button>
    </div>;
  }

  const cluster = BU_DATA.CLUSTERS[stop.cluster];
  const isCapstone = stop.kind === "capstone";

  // Trigger summit on capstone "Continue"
  const handleNext = () => {
    if (isCapstone) onSummit?.();
    else onAdvance?.(1);
  };

  return (
    <div style={{ position: "relative", minHeight: "calc(100vh - 56px)" }}>
      {/* TOP STRIP — altitude, course, kind */}
      <div style={{
        position: "sticky", top: 56, zIndex: 5,
        background: "color-mix(in oklch, var(--c-bg) 85%, transparent)",
        backdropFilter: "blur(12px)",
        borderBottom: "1px solid var(--c-line)",
        padding: "12px 28px",
        display: "grid",
        gridTemplateColumns: "auto 1fr auto",
        alignItems: "center",
        gap: 20,
      }}>
        <KindGlyph kind={stop.kind} />
        <Altitude idx={idx} total={tour.length} />
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <CourseChip clusterId={stop.cluster} />
          <span className="t-mono" style={{ color: "var(--c-ink-dim)", fontSize: 11 }}>
            {stop.node.replace(/_/g, " ").toLowerCase()}
          </span>
        </div>
      </div>

      {/* RATIONALE BAR — "why we go here next" */}
      <div style={{
        padding: "16px 28px",
        background: `linear-gradient(180deg, ${cluster.color}10, transparent)`,
        borderBottom: "1px solid var(--c-line)",
      }}>
        <div style={{ maxWidth: 920, margin: "0 auto", display: "flex", gap: 16, alignItems: "flex-start" }}>
          <div style={{
            flexShrink: 0, marginTop: 2,
            padding: "3px 9px", borderRadius: 4,
            background: cluster.color + "22",
            border: `1px solid ${cluster.color}55`,
            fontFamily: "var(--f-mono)", fontSize: 10.5,
            color: cluster.color, letterSpacing: "0.08em", textTransform: "uppercase",
          }}>
            TRAIL MARKER
          </div>
          <p className="t-body" style={{ margin: 0, color: "var(--c-ink)", maxWidth: 700 }}>
            {stop.rationale}
          </p>
        </div>
      </div>

      {/* LESSON BODY — variant-driven */}
      {layout === "postcard" && (
        <PostcardLayout lesson={lesson} stop={stop}
                        quizPicked={quizPicked} quizChecked={quizChecked}
                        setQuizPicked={setQuizPicked} setQuizChecked={setQuizChecked} />
      )}
      {layout === "split" && (
        <SplitLayout lesson={lesson} stop={stop} tour={tour} idx={idx}
                     quizPicked={quizPicked} quizChecked={quizChecked}
                     setQuizPicked={setQuizPicked} setQuizChecked={setQuizChecked}
                     onShow3D={onShow3D} />
      )}
      {layout === "full-bleed" && (
        <FullBleedLayout lesson={lesson} stop={stop} tour={tour} idx={idx}
                         quizPicked={quizPicked} quizChecked={quizChecked}
                         setQuizPicked={setQuizPicked} setQuizChecked={setQuizChecked} />
      )}

      {/* BOTTOM — nav strip with prev/next + bridge */}
      <div style={{
        position: "sticky", bottom: 0, zIndex: 6,
        background: "color-mix(in oklch, var(--c-bg) 90%, transparent)",
        backdropFilter: "blur(14px)",
        borderTop: "1px solid var(--c-line)",
        padding: "14px 28px",
        display: "grid", gridTemplateColumns: "1fr auto 1fr",
        gap: 16, alignItems: "center",
      }}>
        <div>
          {prev && (
            <button className="btn ghost" onClick={() => onAdvance(-1)}>
              ‹ {prev.node.replace(/_/g, " ")}
            </button>
          )}
        </div>
        <div style={{ display: "flex", gap: 8, justifyContent: "center" }}>
          <button className="btn" onClick={() => onBranch(stop.node)}>
            <span style={{ color: "var(--c-bridge)" }}>≈</span> Bridge to another course
          </button>
          <button className="btn ghost" onClick={onShow3D}>
            ◳ Open 3D
          </button>
        </div>
        <div style={{ textAlign: "right" }}>
          <button className="btn primary" onClick={handleNext}>
            {isCapstone ? "Reach the summit ★" : (next ? <>{next.node.replace(/_/g, " ")} ›</> : "Finish ›")}
          </button>
        </div>
      </div>

      {/* MINI-MAP — locked bottom-right */}
      <div style={{
        position: "fixed", bottom: 80, right: 22, zIndex: 5,
      }}>
        <MiniMap tour={tour} idx={idx} onJump={onJumpTo} />
      </div>

      {/* NEXT-STOP PREVIEW — locked top-right */}
      {next && (
        <div style={{
          position: "fixed", top: 130, right: 22, zIndex: 5,
          width: 220,
          background: "color-mix(in oklch, var(--c-bg-elev) 92%, transparent)",
          backdropFilter: "blur(10px)",
          border: "1px solid var(--c-line)",
          borderRadius: "var(--r-md)",
          padding: 12,
        }}>
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 6 }}>
            NEXT STOP
          </div>
          <div style={{ display: "flex", alignItems: "baseline", gap: 6, marginBottom: 4 }}>
            <KindGlyph kind={next.kind} />
          </div>
          <div className="t-h3" style={{ marginBottom: 4 }}>{next.node.replace(/_/g, " ")}</div>
          <div className="t-cap" style={{ color: "var(--c-ink-muted)", fontSize: 11.5, lineHeight: 1.4 }}>
            {next.rationale.slice(0, 110)}{next.rationale.length > 110 ? "…" : ""}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Postcard layout — single column, deliberately spare ─────────────
function PostcardLayout({ lesson, stop, quizPicked, quizChecked, setQuizPicked, setQuizChecked }) {
  return (
    <div style={{
      maxWidth: 720, margin: "0 auto",
      padding: "48px 28px 80px", paddingRight: 280, paddingLeft: 28,
    }}>
      <div className="reading-col fade-in">
        <h2 style={{ margin: "0 0 4px" }}>{lesson.title}</h2>
        <Evidence items={lesson.evidence} />
        <div style={{ height: 24 }} />
        <p style={{ fontSize: 17, lineHeight: 1.6, color: "var(--c-ink)" }}>
          {lesson.summary}
        </p>

        <div className="topo-rule" style={{ margin: "24px 0" }} />
        <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 12 }}>KEY IDEAS</div>
        {lesson.key_ideas.map((k, i) => (
          <div key={i} style={{
            display: "grid", gridTemplateColumns: "auto 1fr",
            gap: 16, marginBottom: 18,
          }}>
            <div style={{
              fontFamily: "var(--f-mono)", fontSize: 11,
              color: "var(--c-bridge)",
              borderRight: "1px solid var(--c-line-strong)",
              paddingRight: 16, paddingTop: 4,
              textAlign: "right", minWidth: 28,
            }}>{String(i + 1).padStart(2, "0")}</div>
            <div>
              <div style={{ fontWeight: 600, fontSize: 15.5, marginBottom: 4, letterSpacing: "-0.01em" }}>
                {k.h}
              </div>
              <div style={{ color: "var(--c-ink-muted)", lineHeight: 1.55 }}>{k.b}</div>
            </div>
          </div>
        ))}

        {lesson.worked_example && <>
          <div className="topo-rule" style={{ margin: "24px 0" }} />
          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 12 }}>WORKED EXAMPLE</div>
          <div className="card recessed" style={{
            fontFamily: "var(--f-mono)", fontSize: 13, lineHeight: 1.6,
            padding: 18,
          }}>
            {lesson.worked_example}
          </div>
        </>}

        {lesson.quiz?.[0] && <Quiz q={lesson.quiz[0]}
          picked={quizPicked} checked={quizChecked}
          setPicked={setQuizPicked} setChecked={setQuizChecked} />}

        {renderExercise(stop.node, lesson)}
      </div>
    </div>
  );
}

// ─── Split layout — neighborhood viz on left, lesson right ───────────
function SplitLayout({ lesson, stop, tour, idx, quizPicked, quizChecked, setQuizPicked, setQuizChecked, onShow3D }) {
  const visitedSet = useMemo(() => new Set(tour.slice(0, idx).map(s => s.node)), [tour, idx]);
  return (
    <div style={{
      display: "grid", gridTemplateColumns: "1.05fr 1fr",
      gap: 0, paddingRight: 280,
      minHeight: "calc(100vh - 240px)",
    }}>
      <div style={{
        position: "relative",
        borderRight: "1px solid var(--c-line)",
        background: "var(--c-bg-elev)",
        minHeight: 600,
      }}>
        <BrainGraph3D
          currentNode={stop.node}
          visited={visitedSet}
          tourPath={tour.map(s => s.node)}
          showLabels="all"
          highlightCluster={stop.cluster}
          cinematic={false}
          background="var(--c-bg-elev)"
        />
        <button className="btn" onClick={onShow3D} style={{
          position: "absolute", bottom: 14, left: 14,
        }}>◳ Fullscreen</button>
      </div>
      <div style={{ padding: "32px 28px 80px", overflow: "auto" }}>
        <h2 style={{ margin: "0 0 4px", fontSize: 26, letterSpacing: "-0.02em" }}>{lesson.title}</h2>
        <Evidence items={lesson.evidence} />
        <p style={{ marginTop: 16, fontSize: 15.5, lineHeight: 1.6 }}>{lesson.summary}</p>
        <div className="t-tag" style={{ color: "var(--c-ink-muted)", margin: "16px 0 8px" }}>KEY IDEAS</div>
        {lesson.key_ideas.map((k, i) => (
          <div key={i} style={{ marginBottom: 12 }}>
            <div style={{ fontWeight: 600, marginBottom: 2 }}>{k.h}</div>
            <div style={{ color: "var(--c-ink-muted)", fontSize: 13.5, lineHeight: 1.5 }}>{k.b}</div>
          </div>
        ))}
        {lesson.worked_example && (
          <div className="card recessed" style={{ fontFamily: "var(--f-mono)", fontSize: 12.5, lineHeight: 1.5, marginTop: 16 }}>
            {lesson.worked_example}
          </div>
        )}
        {lesson.quiz?.[0] && <Quiz q={lesson.quiz[0]}
          picked={quizPicked} checked={quizChecked}
          setPicked={setQuizPicked} setChecked={setQuizChecked} />}
        {renderExercise(stop.node, lesson)}
      </div>
    </div>
  );
}

// ─── Full-bleed layout — magazine spread w/ wide image-like header ───
function FullBleedLayout({ lesson, stop, tour, idx, quizPicked, quizChecked, setQuizPicked, setQuizChecked }) {
  const cluster = BU_DATA.CLUSTERS[stop.cluster];
  const visitedSet = useMemo(() => new Set(tour.slice(0, idx).map(s => s.node)), [tour, idx]);
  return (
    <div style={{ paddingRight: 280 }}>
      {/* Hero strip — graph fills width, title overlaid */}
      <div style={{ position: "relative", height: 320, overflow: "hidden",
                    borderBottom: "1px solid var(--c-line)" }}>
        <div style={{ position: "absolute", inset: 0 }}>
          <BrainGraph3D
            currentNode={stop.node}
            visited={visitedSet}
            tourPath={tour.map(s => s.node)}
            showLabels="hubs"
            highlightCluster={stop.cluster}
            cinematic={true}
            background="var(--c-bg)"
          />
        </div>
        <div style={{
          position: "absolute", inset: 0,
          background: `linear-gradient(180deg, transparent 30%, var(--c-bg) 100%)`,
        }} />
        <div style={{
          position: "absolute", left: 28, bottom: 24, right: 28,
          maxWidth: 800,
        }}>
          <h1 className="t-display" style={{ margin: 0 }}>{lesson.title}</h1>
          <div style={{ marginTop: 8, display: "flex", gap: 10, alignItems: "center" }}>
            <CourseChip clusterId={stop.cluster} size="md" />
            <Evidence items={lesson.evidence} />
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 720, margin: "0 auto", padding: "32px 28px 80px" }}>
        <p style={{ fontSize: 18, lineHeight: 1.6 }}>{lesson.summary}</p>
        <div className="topo-rule" style={{ margin: "20px 0" }} />
        <div style={{
          display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16,
        }}>
          {lesson.key_ideas.map((k, i) => (
            <div key={i} style={{
              padding: 14,
              borderTop: `2px solid ${cluster.color}`,
            }}>
              <div className="t-tag" style={{ color: cluster.color, marginBottom: 6 }}>
                IDEA {String(i + 1).padStart(2, "0")}
              </div>
              <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 4 }}>{k.h}</div>
              <div className="t-cap" style={{ fontSize: 12.5, lineHeight: 1.5 }}>{k.b}</div>
            </div>
          ))}
        </div>
        {lesson.worked_example && (
          <div className="card recessed" style={{
            marginTop: 20, padding: 18,
            fontFamily: "var(--f-mono)", fontSize: 13, lineHeight: 1.6,
          }}>{lesson.worked_example}</div>
        )}
        {lesson.quiz?.[0] && <Quiz q={lesson.quiz[0]}
          picked={quizPicked} checked={quizChecked}
          setPicked={setQuizPicked} setChecked={setQuizChecked} />}
        {renderExercise(stop.node, lesson)}
      </div>
    </div>
  );
}

// ─── Quiz module ────────────────────────────────────────────────────
function Quiz({ q, picked, checked, setPicked, setChecked }) {
  const correct = picked === q.choices[q.correct];
  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>COMPREHENSION CHECK</div>
      <div style={{ fontWeight: 500, fontSize: 14.5, marginBottom: 12 }}>{q.q}</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {q.choices.map((c, i) => {
          const isPicked = picked === c;
          const isRight = checked && i === q.correct;
          const isWrong = checked && isPicked && i !== q.correct;
          const cls = "quiz-opt" + (isPicked && !checked ? " picked" : "")
                      + (isRight ? " right" : "") + (isWrong ? " wrong" : "");
          return (
            <button key={i} className={cls}
              disabled={checked}
              onClick={() => setPicked(c)}>
              <span className="marker">{String.fromCharCode(65 + i)}</span>
              <span>{c}</span>
            </button>
          );
        })}
      </div>
      {!checked && picked && (
        <button className="btn" style={{ marginTop: 10 }}
          onClick={() => setChecked(true)}>Check answer</button>
      )}
      {checked && (
        <div style={{
          marginTop: 12, padding: 12, borderRadius: 6,
          background: correct ? "color-mix(in oklch, var(--c-cs) 12%, transparent)"
                              : "color-mix(in oklch, var(--c-here) 12%, transparent)",
          border: `1px solid ${correct ? "var(--c-cs)" : "var(--c-here)"}55`,
          fontSize: 13, lineHeight: 1.5,
        }}>
          <strong style={{ color: correct ? "var(--c-cs)" : "var(--c-here)" }}>
            {correct ? "✓ Correct." : "✗ Not quite."}
          </strong> {q.why}
        </div>
      )}
    </div>
  );
}

window.Walk = Walk;
