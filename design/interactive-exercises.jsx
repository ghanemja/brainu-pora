/* global React, BU_DATA */

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────────
// INTERACTIVE EXERCISES — 3blue1brown style
// Color-coded mathematical objects, warm narrator voice,
// smooth transitions, "let's build intuition" framing.
// ─────────────────────────────────────────────────────────────────

// 3b1b palette anchors — resolved from CSS vars at draw time so
// theme switches (dark/light) propagate automatically.
function readVar(name, fallback) {
  if (typeof document === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

function palette() {
  return {
    bg:        readVar("--c-bg-elev",    "#0f1733"),
    surface:   readVar("--c-bg-elev-2",  "#161e3f"),
    ink:       readVar("--c-ink",        "#f5f7fb"),
    inkMuted:  readVar("--c-ink-muted",  "#9aa3c0"),
    line:      readVar("--c-line-strong","rgba(125,211,252,0.28)"),
    // 3b1b semantic colors
    node:      "#ffd166",   // yellow — primary objects (vertices)
    edge:      "#5d6688",   // muted gray — default edges
    highlight: "#3b8eea",   // blue — selection / focus
    success:   "#5ee2a0",   // teal-green — correct / tree edges
    error:     "#ff6b8a",   // rose — invalid
    accent:    "#c792ea",   // lavender — queue / pending
  };
}

// ─────────────────────────────────────────────────────────────────

/**
 * SpanningTreeSimulator — minimum spanning tree intuition.
 * Click edges to assemble a tree connecting all 5 vertices.
 */
function SpanningTreeSimulator() {
  const canvasRef = useRef(null);
  const [selectedEdges, setSelectedEdges] = useState([]);
  const [message, setMessage] = useState("Pick edges one at a time. We need exactly 4 — one less than the 5 vertices.");
  const [isComplete, setIsComplete] = useState(false);

  const nodes = [
    { id: 0, x: 150, y: 100, label: "A" },
    { id: 1, x: 330, y: 80,  label: "B" },
    { id: 2, x: 400, y: 210, label: "C" },
    { id: 3, x: 250, y: 320, label: "D" },
    { id: 4, x: 90,  y: 250, label: "E" },
  ];

  const edges = [
    { id: "0-1", from: 0, to: 1 },
    { id: "0-4", from: 0, to: 4 },
    { id: "1-2", from: 1, to: 2 },
    { id: "1-3", from: 1, to: 3 },
    { id: "2-3", from: 2, to: 3 },
    { id: "3-4", from: 3, to: 4 },
    { id: "2-4", from: 2, to: 4 },
  ];

  const isConnected = (edgeList, n) => {
    const adj = Array.from({ length: n }, () => []);
    edgeList.forEach(e => { adj[e.from].push(e.to); adj[e.to].push(e.from); });
    const seen = new Set();
    const dfs = (v) => { seen.add(v); adj[v].forEach(u => !seen.has(u) && dfs(u)); };
    dfs(0);
    return seen.size === n;
  };

  const hasCycle = (edgeList, n) => {
    // Union-find — if both endpoints already share a root, this edge closes a cycle.
    const parent = Array.from({ length: n }, (_, i) => i);
    const find = (x) => parent[x] === x ? x : (parent[x] = find(parent[x]));
    for (const e of edgeList) {
      const ra = find(e.from), rb = find(e.to);
      if (ra === rb) return true;
      parent[ra] = rb;
    }
    return false;
  };

  const handleEdgeClick = (edgeId) => {
    setIsComplete(false);
    if (selectedEdges.includes(edgeId)) {
      setSelectedEdges(selectedEdges.filter(e => e !== edgeId));
      setMessage("Edge released. Notice how the picture relaxes — one less commitment to keep.");
      return;
    }
    const next = [...selectedEdges, edgeId];
    const edgeObjs = next.map(id => edges.find(e => e.id === id));

    if (hasCycle(edgeObjs, nodes.length)) {
      setMessage("That edge would close a cycle. A tree, by definition, has none — pick a different edge.");
      return;
    }
    setSelectedEdges(next);

    if (next.length === 4) {
      if (isConnected(edgeObjs, nodes.length)) {
        setMessage("Beautiful. Four edges, every vertex reachable, no cycles — that's exactly a spanning tree.");
        setIsComplete(true);
      } else {
        setMessage("Four edges, no cycles — but one vertex is stranded. A spanning tree must reach all of them.");
      }
    } else if (next.length > 4) {
      setMessage("Too many edges. A spanning tree on n vertices uses exactly n − 1 edges.");
    } else {
      const left = 4 - next.length;
      setMessage(`${next.length} of 4 chosen. ${left} to go — keep growing the tree without closing a loop.`);
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const p = palette();

    // Background
    ctx.fillStyle = p.bg;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Subtle grid for depth (3b1b uses faint background structure)
    ctx.strokeStyle = p.line;
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 40) {
      ctx.globalAlpha = 0.15;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 40) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }
    ctx.globalAlpha = 1;

    // Edges — selected first as glow, then unselected on top
    edges.forEach(edge => {
      const from = nodes[edge.from];
      const to = nodes[edge.to];
      const selected = selectedEdges.includes(edge.id);

      if (selected) {
        // glow
        ctx.strokeStyle = p.highlight;
        ctx.globalAlpha = 0.25;
        ctx.lineWidth = 10;
        ctx.beginPath(); ctx.moveTo(from.x, from.y); ctx.lineTo(to.x, to.y); ctx.stroke();
        ctx.globalAlpha = 1;
        ctx.strokeStyle = isComplete ? p.success : p.highlight;
        ctx.lineWidth = 3.5;
      } else {
        ctx.strokeStyle = p.edge;
        ctx.lineWidth = 1.8;
      }
      ctx.beginPath(); ctx.moveTo(from.x, from.y); ctx.lineTo(to.x, to.y); ctx.stroke();
    });

    // Nodes — yellow disks with dark stroke (3b1b signature)
    nodes.forEach(node => {
      ctx.beginPath(); ctx.arc(node.x, node.y, 22, 0, Math.PI * 2);
      ctx.fillStyle = p.node;
      ctx.fill();
      ctx.strokeStyle = p.bg;
      ctx.lineWidth = 3;
      ctx.stroke();

      ctx.fillStyle = "#1a1a2e";
      ctx.font = "700 14px 'Geist', system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(node.label, node.x, node.y);
    });
  }, [selectedEdges, isComplete]);

  const handleCanvasClick = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const sx = canvas.width / rect.width;
    const sy = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * sx;
    const y = (e.clientY - rect.top) * sy;

    // Distance from point to segment — accurate edge hit-test, not midpoint-only.
    let best = null, bestDist = 14;
    for (const edge of edges) {
      const a = nodes[edge.from], b = nodes[edge.to];
      const dx = b.x - a.x, dy = b.y - a.y;
      const len2 = dx * dx + dy * dy;
      const t = Math.max(0, Math.min(1, ((x - a.x) * dx + (y - a.y) * dy) / len2));
      const px = a.x + t * dx, py = a.y + t * dy;
      const d = Math.hypot(x - px, y - py);
      if (d < bestDist) { bestDist = d; best = edge.id; }
    }
    if (best) handleEdgeClick(best);
  };

  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div className="t-tag" style={{ color: "var(--c-bridge)", marginBottom: 12 }}>INTERACTIVE EXERCISE</div>
      <div style={{ fontWeight: 500, fontSize: 14.5, marginBottom: 8 }}>Build a Spanning Tree</div>
      <p style={{ fontSize: 13.5, color: "var(--c-ink-muted)", marginBottom: 12, lineHeight: 1.55 }}>
        Imagine five towns and a list of possible roads between them. You want every town reachable from every other,
        but no wasted road. Click an edge to commit to it; click again to release. Watch what makes a tree feel
        <em> taut</em> — no slack, no loops.
      </p>
      <canvas
        ref={canvasRef}
        width={480}
        height={380}
        onClick={handleCanvasClick}
        style={{
          border: "1px solid var(--c-line)",
          borderRadius: 8,
          cursor: "pointer",
          display: "block",
          marginBottom: 12,
          width: "100%",
          maxWidth: 480,
        }}
      />
      <div style={{
        padding: 12,
        borderRadius: 6,
        background: isComplete ? "color-mix(in oklch, var(--c-cs) 12%, transparent)"
                               : "color-mix(in oklch, var(--c-bridge) 12%, transparent)",
        border: `1px solid ${isComplete ? "var(--c-cs)" : "var(--c-bridge)"}55`,
        fontSize: 13.5,
        lineHeight: 1.5,
      }}>
        <strong>{isComplete ? "✓" : "→"}</strong> {message}
      </div>
      <button className="btn ghost" style={{ marginTop: 8 }}
        onClick={() => {
          setSelectedEdges([]); setIsComplete(false);
          setMessage("Cleared. Start fresh — pick the first edge and build from there.");
        }}>
        Reset
      </button>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────

/**
 * BFSVisualizer — watch a wavefront expand through a graph.
 */
function BFSVisualizer() {
  const canvasRef = useRef(null);
  const [step, setStep] = useState(0);
  const [paused, setPaused] = useState(true);

  const nodes = [
    { id: 0, x: 80,  y: 100, label: "0" },
    { id: 1, x: 180, y: 60,  label: "1" },
    { id: 2, x: 280, y: 100, label: "2" },
    { id: 3, x: 80,  y: 220, label: "3" },
    { id: 4, x: 180, y: 270, label: "4" },
    { id: 5, x: 280, y: 220, label: "5" },
  ];

  const edges = [
    { from: 0, to: 1 }, { from: 0, to: 3 },
    { from: 1, to: 2 }, { from: 1, to: 4 },
    { from: 2, to: 5 }, { from: 3, to: 4 }, { from: 4, to: 5 },
  ];

  const trace = useMemo(() => {
    const t = [];
    const visited = new Set();
    const queue = [0];
    const treeEdges = [];
    visited.add(0);

    t.push({ action: "start", node: 0, queue: [0], visited: new Set([0]), treeEdges: [], depth: 0 });

    const depth = { 0: 0 };
    while (queue.length > 0) {
      const u = queue.shift();
      const neighbors = edges.filter(e => e.from === u).map(e => e.to)
                             .concat(edges.filter(e => e.to === u).map(e => e.from));
      for (const v of neighbors) {
        if (!visited.has(v)) {
          visited.add(v);
          queue.push(v);
          depth[v] = depth[u] + 1;
          treeEdges.push({ from: u, to: v });
          t.push({
            action: "visit",
            node: v,
            queue: [...queue],
            visited: new Set(visited),
            treeEdges: [...treeEdges],
            depth: depth[v],
          });
        }
      }
    }
    return t;
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const p = palette();

    ctx.fillStyle = p.bg;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const state = trace[Math.min(step, trace.length - 1)];

    // Edges — tree edges glow green, frontier shimmer blue, rest faint
    edges.forEach(e => {
      const from = nodes[e.from];
      const to = nodes[e.to];
      const isTree = state.treeEdges.some(te =>
        (te.from === e.from && te.to === e.to) || (te.from === e.to && te.to === e.from));

      if (isTree) {
        ctx.strokeStyle = p.success;
        ctx.globalAlpha = 0.25; ctx.lineWidth = 9;
        ctx.beginPath(); ctx.moveTo(from.x, from.y); ctx.lineTo(to.x, to.y); ctx.stroke();
        ctx.globalAlpha = 1;
        ctx.lineWidth = 3;
      } else {
        ctx.strokeStyle = p.edge;
        ctx.lineWidth = 1.5;
      }
      ctx.beginPath(); ctx.moveTo(from.x, from.y); ctx.lineTo(to.x, to.y); ctx.stroke();
    });

    // Nodes — visited = teal, queued = lavender ring, unvisited = muted yellow outline
    nodes.forEach(node => {
      const isVisited = state.visited.has(node.id);
      const inQueue = state.queue.includes(node.id);
      const isCurrent = state.node === node.id;

      // queue ring
      if (inQueue) {
        ctx.strokeStyle = p.accent;
        ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.arc(node.x, node.y, 22, 0, Math.PI * 2); ctx.stroke();
      }

      ctx.beginPath(); ctx.arc(node.x, node.y, 17, 0, Math.PI * 2);
      ctx.fillStyle = isVisited ? p.success : p.node;
      ctx.globalAlpha = isVisited ? 1 : 0.35;
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.strokeStyle = isCurrent ? p.highlight : p.bg;
      ctx.lineWidth = isCurrent ? 3 : 2;
      ctx.stroke();

      ctx.fillStyle = isVisited ? "#0c2a1f" : "#1a1a2e";
      ctx.font = "700 12px 'Geist', system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(node.label, node.x, node.y);
    });
  }, [step, trace]);

  useEffect(() => {
    if (!paused && step < trace.length - 1) {
      const timer = setTimeout(() => setStep(step + 1), 750);
      return () => clearTimeout(timer);
    }
  }, [paused, step, trace.length]);

  const cur = trace[Math.min(step, trace.length - 1)] || {};

  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div className="t-tag" style={{ color: "var(--c-cs)", marginBottom: 12 }}>INTERACTIVE EXERCISE</div>
      <div style={{ fontWeight: 500, fontSize: 14.5, marginBottom: 8 }}>Breadth-First Search</div>
      <p style={{ fontSize: 13.5, color: "var(--c-ink-muted)", marginBottom: 12, lineHeight: 1.55 }}>
        Picture a wave spreading from node 0. At each tick, every node currently <em>in the queue</em> (lavender ring)
        wakes up its unvisited neighbors and joins the <em>visited set</em> (green). The thick green edges record the order
        of first discovery — that's the BFS tree.
      </p>
      <canvas
        ref={canvasRef}
        width={360}
        height={320}
        style={{
          border: "1px solid var(--c-line)",
          borderRadius: 8,
          display: "block",
          marginBottom: 12,
          width: "100%",
          maxWidth: 360,
        }}
      />
      <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
        <button className="btn ghost" onClick={() => { setStep(0); setPaused(true); }}>⏮ Reset</button>
        <button className="btn ghost" onClick={() => setPaused(!paused)}>
          {paused ? "▶ Play" : "⏸ Pause"}
        </button>
        <button className="btn ghost" onClick={() => setStep(Math.min(step + 1, trace.length - 1))}>⏭ Step</button>
      </div>
      <div style={{
        padding: 10, borderRadius: 6, background: "color-mix(in oklch, var(--c-ink) 8%, transparent)",
        border: "1px solid var(--c-line)", fontSize: 12.5, fontFamily: "var(--f-mono)", lineHeight: 1.7,
      }}>
        Queue:    [{(cur.queue || []).join(", ")}]<br />
        Visited:  {Array.from(cur.visited || []).sort((a, b) => a - b).join(", ")}<br />
        Depth:    {cur.depth ?? 0}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────

/**
 * ApproximationRatioTuner — slide ρ, feel the guarantee tighten.
 */
function ApproximationRatioTuner() {
  const [rho, setRho] = useState(2);
  const canvasRef = useRef(null);
  const optimalCost = 100;
  const algorithmCost = Math.floor(rho * optimalCost);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const p = palette();
    const W = canvas.width, H = canvas.height;

    ctx.fillStyle = p.bg;
    ctx.fillRect(0, 0, W, H);

    // Axis baseline
    const baseY = H - 30;
    const left = 40, right = W - 40;
    ctx.strokeStyle = p.line; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(left, baseY); ctx.lineTo(right, baseY); ctx.stroke();

    // Two bars: OPT (green) and ρ·OPT (yellow→rose as ρ grows)
    const maxRho = 4;
    const barW = 70;
    const optX = left + 60;
    const algX = left + 200;
    const optH = (1 / maxRho) * (baseY - 20);
    const algH = (rho / maxRho) * (baseY - 20);

    // OPT bar
    ctx.fillStyle = p.success;
    ctx.fillRect(optX, baseY - optH, barW, optH);
    ctx.fillStyle = p.ink;
    ctx.font = "600 12px 'Geist', system-ui";
    ctx.textAlign = "center";
    ctx.fillText("OPT", optX + barW / 2, baseY + 18);
    ctx.fillText(String(optimalCost), optX + barW / 2, baseY - optH - 8);

    // ρ·OPT bar — color interpolates yellow → rose with ρ
    const tFrac = Math.min(1, (rho - 1) / (maxRho - 1));
    ctx.fillStyle = tFrac < 0.5 ? p.node : p.error;
    ctx.fillRect(algX, baseY - algH, barW, algH);
    ctx.fillStyle = p.ink;
    ctx.fillText(`ρ·OPT`, algX + barW / 2, baseY + 18);
    ctx.fillText(String(algorithmCost), algX + barW / 2, baseY - algH - 8);

    // Bound line at top of ρ·OPT, dashed
    ctx.strokeStyle = p.highlight;
    ctx.setLineDash([6, 4]);
    ctx.beginPath();
    ctx.moveTo(left, baseY - algH); ctx.lineTo(right, baseY - algH);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = p.highlight;
    ctx.textAlign = "left";
    ctx.fillText("guaranteed ceiling", right - 130, baseY - algH - 6);
  }, [rho]);

  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div className="t-tag" style={{ color: "var(--c-here)", marginBottom: 12 }}>INTERACTIVE EXERCISE</div>
      <div style={{ fontWeight: 500, fontSize: 14.5, marginBottom: 8 }}>Approximation Ratio</div>
      <p style={{ fontSize: 13.5, color: "var(--c-ink-muted)", marginBottom: 12, lineHeight: 1.55 }}>
        Suppose the true best answer costs 100. A <em>ρ-approximation</em> algorithm promises to land at most ρ × 100
        — even on the worst input it'll ever see. Slide ρ and watch the ceiling drop. The closer ρ gets to 1, the
        sharper the promise.
      </p>

      <canvas
        ref={canvasRef}
        width={420}
        height={260}
        style={{
          border: "1px solid var(--c-line)",
          borderRadius: 8,
          display: "block",
          marginBottom: 12,
          width: "100%",
          maxWidth: 420,
        }}
      />

      <div style={{ background: "var(--c-bg-elev)", padding: 16, borderRadius: 8, marginBottom: 12 }}>
        <label style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span style={{ fontSize: 13, minWidth: 40 }}>ρ =</span>
          <input
            type="range"
            min="1"
            max="4"
            step="0.1"
            value={rho}
            onChange={(e) => setRho(parseFloat(e.target.value))}
            style={{ flex: 1 }}
          />
          <span style={{ fontFamily: "var(--f-mono)", fontSize: 14, minWidth: 40, fontWeight: 600 }}>{rho.toFixed(1)}</span>
        </label>
        <div style={{ marginTop: 10, fontSize: 12.5, color: "var(--c-ink-muted)" }}>
          cost(algorithm) ≤ {rho.toFixed(1)} × OPT = {algorithmCost}
        </div>
      </div>

      <div style={{
        padding: 12, borderRadius: 6, background: "color-mix(in oklch, var(--c-bridge) 12%, transparent)",
        border: "1px solid var(--c-bridge)55", fontSize: 13.5, lineHeight: 1.55,
      }}>
        <strong>The intuition:</strong> ρ = 1 means optimal. ρ = 2 means "at worst, twice as bad." The art of
        approximation theory is proving the smallest ρ your algorithm can survive on every input — not just the easy ones.
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────

/**
 * ConceptInteractive — a universal "Active Recall" exercise that any
 * lesson can render, driven purely by that lesson's own content.
 *
 * Flow per card (predict → reveal → grade):
 *   1. Show a key idea's HEADING (the prompt) and ask the learner to
 *      predict what it means before seeing the answer.
 *   2. They self-predict — free recall in a textarea, OR if the lesson
 *      carries a quiz, multiple-choice from those real choices.
 *   3. Reveal the answer (the key idea's body / quiz rationale), then
 *      grade their recall with SM-2-flavored buttons (Again / Hard /
 *      Good / Easy). Grading only updates local UI state — no backend.
 *
 * Degrades gracefully: with zero key_ideas it falls back to the summary
 * as a single card; with a quiz it threads the MCQ in as its own card.
 */
function ConceptInteractive({ lesson }) {
  // Build the deck from the lesson's own data — each card is one recall beat.
  const cards = useMemo(() => {
    const out = [];
    const ideas = (lesson && Array.isArray(lesson.key_ideas)) ? lesson.key_ideas : [];

    ideas.forEach((k, i) => {
      out.push({
        kind: "recall",
        prompt: k.h || `Key idea ${i + 1}`,
        answer: k.b || "",
      });
    });

    // If there are no key ideas, fall back to the summary so the card
    // deck is never empty — every lesson still gets something to recall.
    if (out.length === 0 && lesson && lesson.summary) {
      out.push({
        kind: "recall",
        prompt: lesson.title || "Recall this concept",
        answer: lesson.summary,
      });
    }

    // Thread the lesson's real quiz in as a final multiple-choice card.
    const q = lesson && Array.isArray(lesson.quiz) ? lesson.quiz[0] : null;
    if (q && Array.isArray(q.choices) && q.choices.length) {
      out.push({
        kind: "mcq",
        prompt: q.q,
        choices: q.choices,
        correct: q.correct,
        answer: q.why || "",
      });
    }

    return out;
  }, [lesson]);

  const total = cards.length;
  const [idx, setIdx] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [prediction, setPrediction] = useState("");
  const [picked, setPicked] = useState(null);       // mcq selection index
  const [grades, setGrades] = useState({});          // { cardIndex: "again"|"hard"|"good"|"easy" }
  const [done, setDone] = useState(false);

  // Reset everything if the lesson (and thus the deck) changes.
  useEffect(() => {
    setIdx(0); setRevealed(false); setPrediction(""); setPicked(null);
    setGrades({}); setDone(false);
  }, [cards]);

  if (total === 0) return null; // truly nothing to recall — render nothing.

  const card = cards[Math.min(idx, total - 1)];

  // SM-2-flavored grades. "good"/"easy" count as a successful recall.
  const GRADES = [
    { id: "again", label: "Again", hint: "blanked",       color: "var(--c-here)" },
    { id: "hard",  label: "Hard",  hint: "barely",        color: "#ffb454" },
    { id: "good",  label: "Good",  hint: "recalled",      color: "var(--c-bridge)" },
    { id: "easy",  label: "Easy",  hint: "instant",       color: "var(--c-cs)" },
  ];

  const recalledCount = Object.values(grades)
    .filter(g => g === "good" || g === "easy").length;

  const grade = (gid) => {
    const nextGrades = { ...grades, [idx]: gid };
    setGrades(nextGrades);
    if (idx + 1 >= total) {
      setDone(true);
    } else {
      setIdx(idx + 1);
      setRevealed(false);
      setPrediction("");
      setPicked(null);
    }
  };

  const restart = () => {
    setIdx(0); setRevealed(false); setPrediction(""); setPicked(null);
    setGrades({}); setDone(false);
  };

  // ── Summary screen ───────────────────────────────────────────────
  if (done) {
    const graded = Object.keys(grades).length;
    return (
      <div style={{ marginTop: 28 }}>
        <div className="topo-rule" style={{ margin: "0 0 16px" }} />
        <div className="t-tag" style={{ color: "var(--c-cs)", marginBottom: 12 }}>ACTIVE RECALL</div>
        <div className="card" style={{ padding: 20, textAlign: "center" }}>
          <div style={{ fontSize: 22, fontWeight: 600, letterSpacing: "-0.01em", marginBottom: 6 }}>
            You recalled {recalledCount}/{graded}
          </div>
          <div style={{ color: "var(--c-ink-muted)", fontSize: 13.5, lineHeight: 1.5, marginBottom: 16 }}>
            {recalledCount === graded
              ? "Clean sweep — every idea came back without a peek. That's the signal it's sticking."
              : "The ones you graded Again or Hard are exactly the ones worth a second pass. Retrieval, not rereading, is what builds memory."}
          </div>
          <button className="btn" onClick={restart}>↻ Run it again</button>
        </div>
      </div>
    );
  }

  // ── Recall / MCQ card ────────────────────────────────────────────
  const isMcq = card.kind === "mcq";

  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 12 }}>
        <div className="t-tag" style={{ color: "var(--c-cs)" }}>ACTIVE RECALL</div>
        <div className="t-tag" style={{ color: "var(--c-ink-muted)" }}>
          {idx + 1} / {total}
        </div>
      </div>

      <p style={{ fontSize: 13.5, color: "var(--c-ink-muted)", marginBottom: 14, lineHeight: 1.55 }}>
        {isMcq
          ? "Commit to an answer before checking. Predicting first — even when you're unsure — is what makes the correction stick."
          : "Read the prompt, then say it back in your own words before you reveal. The act of pulling it from memory is the lesson."}
      </p>

      {/* Prompt card */}
      <div className="card" style={{ padding: 18, marginBottom: 14 }}>
        <div style={{ fontWeight: 600, fontSize: 15.5, lineHeight: 1.45, letterSpacing: "-0.01em" }}>
          {card.prompt}
        </div>

        {/* PREDICT — free recall (textarea) for recall cards */}
        {!isMcq && (
          <textarea
            value={prediction}
            onChange={(e) => setPrediction(e.target.value)}
            placeholder="Predict: what does this mean? (optional — typing it out helps)"
            rows={3}
            disabled={revealed}
            style={{
              width: "100%", marginTop: 14, padding: "10px 12px",
              borderRadius: "var(--r-md)", resize: "vertical",
              background: "var(--c-bg-elev)", color: "var(--c-ink)",
              border: "1px solid var(--c-line)", fontFamily: "var(--f-sans)",
              fontSize: 13.5, lineHeight: 1.5, boxSizing: "border-box",
              opacity: revealed ? 0.6 : 1,
            }}
          />
        )}

        {/* PREDICT — multiple choice for the quiz card */}
        {isMcq && (
          <div style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 14 }}>
            {card.choices.map((c, i) => {
              const isPicked = picked === i;
              const isRight = revealed && i === card.correct;
              const isWrong = revealed && isPicked && i !== card.correct;
              const cls = "quiz-opt" + (isPicked && !revealed ? " picked" : "")
                          + (isRight ? " right" : "") + (isWrong ? " wrong" : "");
              return (
                <button key={i} className={cls}
                  disabled={revealed}
                  onClick={() => setPicked(i)}>
                  <span className="marker">{String.fromCharCode(65 + i)}</span>
                  <span>{c}</span>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* REVEAL button */}
      {!revealed && (
        <button className="btn"
          disabled={isMcq && picked === null}
          onClick={() => setRevealed(true)}>
          Reveal answer
        </button>
      )}

      {/* REVEAL — the answer + SM-2-flavored grading */}
      {revealed && (
        <div>
          <div style={{
            padding: 14, borderRadius: 6, marginBottom: 14,
            background: "color-mix(in oklch, var(--c-bridge) 12%, transparent)",
            border: "1px solid var(--c-bridge)55",
            fontSize: 13.5, lineHeight: 1.55,
          }}>
            {isMcq && (
              <div style={{
                fontWeight: 600, marginBottom: 6,
                color: picked === card.correct ? "var(--c-cs)" : "var(--c-here)",
              }}>
                {picked === card.correct ? "✓ Correct." : "✗ Not quite."}
              </div>
            )}
            {card.answer || "—"}
          </div>

          <div className="t-tag" style={{ color: "var(--c-ink-muted)", marginBottom: 8 }}>
            HOW WELL DID YOU RECALL IT?
          </div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {GRADES.map(g => (
              <button key={g.id}
                onClick={() => grade(g.id)}
                style={{
                  flex: "1 1 0", minWidth: 78,
                  padding: "9px 8px", borderRadius: "var(--r-md)",
                  background: "transparent",
                  border: `1px solid ${g.color}`,
                  color: g.color, cursor: "pointer",
                  fontFamily: "var(--f-sans)", fontSize: 13, fontWeight: 600,
                  display: "flex", flexDirection: "column", gap: 2, alignItems: "center",
                }}>
                <span>{g.label}</span>
                <span style={{ fontSize: 10.5, opacity: 0.8, fontWeight: 400 }}>{g.hint}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Export for use in lessons
window.SpanningTreeSimulator = SpanningTreeSimulator;
window.BFSVisualizer = BFSVisualizer;
window.ApproximationRatioTuner = ApproximationRatioTuner;
window.ConceptInteractive = ConceptInteractive;
