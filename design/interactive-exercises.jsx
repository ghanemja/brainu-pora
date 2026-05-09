/* global React, BU_DATA */

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────────
// INTERACTIVE EXERCISES
// Embed simulations & playgrounds in lesson cards
// ─────────────────────────────────────────────────────────────────

/**
 * SpanningTreeSimulator — Build a spanning tree by selecting edges.
 * Visual graph, click edges to add them, see feedback on cycles & connectivity.
 */
function SpanningTreeSimulator() {
  const canvasRef = useRef(null);
  const [selectedEdges, setSelectedEdges] = useState([]);
  const [message, setMessage] = useState("Click edges to build a spanning tree (5 vertices = 4 edges)");
  const [isComplete, setIsComplete] = useState(false);

  // Simple 5-node graph: nodes 0-4, pre-defined edges
  const nodes = [
    { id: 0, x: 150, y: 100, label: "A" },
    { id: 1, x: 300, y: 80, label: "B" },
    { id: 2, x: 380, y: 200, label: "C" },
    { id: 3, x: 250, y: 320, label: "D" },
    { id: 4, x: 80, y: 260, label: "E" },
  ];

  const edges = [
    { id: "0-1", from: 0, to: 1, label: "e1" },
    { id: "0-4", from: 0, to: 4, label: "e2" },
    { id: "1-2", from: 1, to: 2, label: "e3" },
    { id: "1-3", from: 1, to: 3, label: "e4" },
    { id: "2-3", from: 2, to: 3, label: "e5" },
    { id: "3-4", from: 3, to: 4, label: "e6" },
    { id: "2-4", from: 2, to: 4, label: "e7" },
  ];

  const handleEdgeClick = (edgeId) => {
    setIsComplete(false);
    if (selectedEdges.includes(edgeId)) {
      setSelectedEdges(selectedEdges.filter(e => e !== edgeId));
      setMessage("Edge removed.");
      return;
    }
    const newSelected = [...selectedEdges, edgeId];
    setSelectedEdges(newSelected);

    if (newSelected.length === 4) {
      // Check if forms spanning tree (connected + 4 edges for 5 nodes)
      const edgeObjs = newSelected.map(id => edges.find(e => e.id === id));
      if (isConnected(edgeObjs, nodes.length)) {
        setMessage("✓ Perfect! You built a valid spanning tree.");
        setIsComplete(true);
      } else {
        setMessage("✗ 4 edges but not connected. Try again.");
      }
    } else if (newSelected.length > 4) {
      setMessage("✗ Spanning tree can only have 4 edges (n-1 for 5 vertices). Deselect one.");
    } else {
      setMessage(`${newSelected.length} of 4 edges selected...`);
    }
  };

  const isConnected = (edgeList, n) => {
    const adj = Array.from({ length: n }, () => []);
    edgeList.forEach(e => {
      adj[e.from].push(e.to);
      adj[e.to].push(e.from);
    });
    const visited = new Set();
    const dfs = (v) => {
      visited.add(v);
      adj[v].forEach(u => !visited.has(u) && dfs(u));
    };
    dfs(0);
    return visited.size === n;
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "var(--c-bg-elev)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw edges
    edges.forEach(edge => {
      const from = nodes[edge.from];
      const to = nodes[edge.to];
      const isSelected = selectedEdges.includes(edge.id);

      ctx.strokeStyle = isSelected ? "var(--c-bridge)" : "var(--c-line)";
      ctx.lineWidth = isSelected ? 3 : 2;
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.lineTo(to.x, to.y);
      ctx.stroke();

      if (isSelected) {
        ctx.fillStyle = "var(--c-bridge)";
        ctx.font = "bold 11px monospace";
        ctx.textAlign = "center";
        ctx.fillText(edge.label, (from.x + to.x) / 2 + 12, (from.y + to.y) / 2 - 6);
      }
    });

    // Draw nodes
    nodes.forEach(node => {
      ctx.fillStyle = "var(--c-bg)";
      ctx.strokeStyle = "var(--c-line-strong)";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(node.x, node.y, 18, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "var(--c-ink)";
      ctx.font = "600 13px system-ui";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(node.label, node.x, node.y);
    });
  }, [selectedEdges]);

  const handleCanvasClick = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Hit test edges (clickable area around edge midpoint)
    for (const edge of edges) {
      const from = nodes[edge.from];
      const to = nodes[edge.to];
      const mx = (from.x + to.x) / 2;
      const my = (from.y + to.y) / 2;
      const dist = Math.sqrt((x - mx) ** 2 + (y - my) ** 2);
      if (dist < 20) {
        handleEdgeClick(edge.id);
        return;
      }
    }
  };

  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div className="t-tag" style={{ color: "var(--c-bridge)", marginBottom: 12 }}>INTERACTIVE EXERCISE</div>
      <div style={{ fontWeight: 500, fontSize: 14.5, marginBottom: 12 }}>Build a Spanning Tree</div>
      <p style={{ fontSize: 13.5, color: "var(--c-ink-muted)", marginBottom: 12 }}>
        Click edges in the graph to form a spanning tree. Remember: 5 vertices require exactly 4 edges, and all vertices must be connected.
      </p>
      <canvas
        ref={canvasRef}
        width={480}
        height={380}
        onClick={handleCanvasClick}
        style={{
          border: "1px solid var(--c-line)",
          borderRadius: 6,
          cursor: "pointer",
          backgroundColor: "var(--c-bg-elev)",
          display: "block",
          marginBottom: 12,
        }}
      />
      <div style={{
        padding: 10,
        borderRadius: 6,
        background: isComplete ? "color-mix(in oklch, var(--c-cs) 12%, transparent)"
                               : "color-mix(in oklch, var(--c-bridge) 12%, transparent)",
        border: `1px solid ${isComplete ? "var(--c-cs)" : "var(--c-bridge)"}55`,
        fontSize: 13,
      }}>
        <strong>{message.startsWith("✓") ? "✓" : message.startsWith("✗") ? "✗" : "→"}</strong> {message}
      </div>
      <button className="btn ghost" style={{ marginTop: 8 }}
        onClick={() => { setSelectedEdges([]); setIsComplete(false); setMessage("Reset. Click edges to build..."); }}>
        Reset
      </button>
    </div>
  );
}

/**
 * BFSVisualizer — Step through breadth-first search on a small graph.
 * See queue, visited set, tree edges forming in real time.
 */
function BFSVisualizer() {
  const canvasRef = useRef(null);
  const [step, setStep] = useState(0);
  const [paused, setPaused] = useState(true);

  const nodes = [
    { id: 0, x: 80, y: 100, label: "0" },
    { id: 1, x: 180, y: 60, label: "1" },
    { id: 2, x: 280, y: 100, label: "2" },
    { id: 3, x: 80, y: 200, label: "3" },
    { id: 4, x: 180, y: 260, label: "4" },
    { id: 5, x: 280, y: 200, label: "5" },
  ];

  const edges = [
    { from: 0, to: 1 }, { from: 0, to: 3 },
    { from: 1, to: 2 }, { from: 1, to: 4 },
    { from: 2, to: 5 }, { from: 3, to: 4 }, { from: 4, to: 5 },
  ];

  // BFS trace: [{ action, node, queue, visited, treeEdges }]
  const trace = useMemo(() => {
    const t = [];
    const visited = new Set();
    const queue = [0];
    const treeEdges = [];
    visited.add(0);

    t.push({ action: "start", node: null, queue: [0], visited: new Set([0]), treeEdges: [] });

    while (queue.length > 0) {
      const u = queue.shift();
      const neighbors = edges.filter(e => e.from === u).map(e => e.to)
                             .concat(edges.filter(e => e.to === u).map(e => e.from));

      for (const v of neighbors) {
        if (!visited.has(v)) {
          visited.add(v);
          queue.push(v);
          treeEdges.push({ from: u, to: v });
          t.push({
            action: "visit",
            node: v,
            queue: [...queue],
            visited: new Set(visited),
            treeEdges: [...treeEdges],
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
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const state = trace[Math.min(step, trace.length - 1)];

    // Draw edges
    edges.forEach(e => {
      const from = nodes[e.from];
      const to = nodes[e.to];
      const isTree = state.treeEdges.some(te => (te.from === e.from && te.to === e.to) ||
                                                   (te.from === e.to && te.to === e.from));

      ctx.strokeStyle = isTree ? "var(--c-cs)" : "var(--c-line)";
      ctx.lineWidth = isTree ? 3 : 1.5;
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.lineTo(to.x, to.y);
      ctx.stroke();
    });

    // Draw nodes
    nodes.forEach(node => {
      const isVisited = state.visited.has(node.id);
      const inQueue = state.queue.includes(node.id);

      ctx.fillStyle = isVisited ? "var(--c-cs)" : "var(--c-bg)";
      ctx.strokeStyle = inQueue ? "var(--c-bridge)" : "var(--c-line-strong)";
      ctx.lineWidth = inQueue ? 3 : 2;
      ctx.beginPath();
      ctx.arc(node.x, node.y, 16, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = isVisited ? "white" : "var(--c-ink)";
      ctx.font = "600 12px system-ui";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(node.label, node.x, node.y);
    });
  }, [step, trace]);

  useEffect(() => {
    if (!paused && step < trace.length - 1) {
      const timer = setTimeout(() => setStep(step + 1), 600);
      return () => clearTimeout(timer);
    }
  }, [paused, step, trace.length]);

  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div className="t-tag" style={{ color: "var(--c-cs)", marginBottom: 12 }}>INTERACTIVE EXERCISE</div>
      <div style={{ fontWeight: 500, fontSize: 14.5, marginBottom: 12 }}>Breadth-First Search (BFS) Step-Through</div>
      <p style={{ fontSize: 13.5, color: "var(--c-ink-muted)", marginBottom: 12 }}>
        Watch BFS unfold from node 0. Green nodes = visited, blue border = in queue, thick edges = tree edges.
      </p>
      <canvas
        ref={canvasRef}
        width={360}
        height={320}
        style={{
          border: "1px solid var(--c-line)",
          borderRadius: 6,
          backgroundColor: "var(--c-bg-elev)",
          display: "block",
          marginBottom: 12,
        }}
      />
      <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
        <button className="btn ghost" onClick={() => setStep(0)}>⏮ Reset</button>
        <button className="btn ghost" onClick={() => setPaused(!paused)}>
          {paused ? "▶ Play" : "⏸ Pause"}
        </button>
        <button className="btn ghost" onClick={() => setStep(Math.min(step + 1, trace.length - 1))}>⏭ Step</button>
      </div>
      <div style={{
        padding: 10, borderRadius: 6, background: "color-mix(in oklch, var(--c-ink) 8%, transparent)",
        border: "1px solid var(--c-line)", fontSize: 12.5, fontFamily: "var(--f-mono)",
      }}>
        Queue: [{(trace[step]?.queue || []).join(", ")}]<br />
        Visited: {Array.from(trace[step]?.visited || []).sort((a, b) => a - b).join(", ")}
      </div>
    </div>
  );
}

/**
 * ApproximationRatioTuner — Adjust approximation ratio, see how solution quality changes.
 * Simple visualization: adjust ρ, see cost bound update.
 */
function ApproximationRatioTuner() {
  const [rho, setRho] = useState(2);
  const optimalCost = 100;
  const algorithmCost = Math.floor(rho * optimalCost);

  return (
    <div style={{ marginTop: 28 }}>
      <div className="topo-rule" style={{ margin: "0 0 16px" }} />
      <div className="t-tag" style={{ color: "var(--c-here)", marginBottom: 12 }}>INTERACTIVE EXERCISE</div>
      <div style={{ fontWeight: 500, fontSize: 14.5, marginBottom: 12 }}>Approximation Ratio Explorer</div>
      <p style={{ fontSize: 13.5, color: "var(--c-ink-muted)", marginBottom: 16 }}>
        Adjust the approximation ratio ρ. See how it bounds the algorithm's solution cost relative to optimal.
      </p>

      <div style={{ background: "var(--c-bg-elev)", padding: 16, borderRadius: 6, marginBottom: 12 }}>
        <div style={{ marginBottom: 12 }}>
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
            <span style={{ fontFamily: "var(--f-mono)", fontSize: 13, minWidth: 40 }}>{rho.toFixed(1)}</span>
          </label>
        </div>

        <div style={{
          display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, fontSize: 12.5,
          padding: 12, background: "var(--c-bg)", borderRadius: 4,
        }}>
          <div>
            <div style={{ color: "var(--c-ink-muted)", marginBottom: 4 }}>Optimal</div>
            <div style={{ fontFamily: "var(--f-mono)", fontSize: 16, fontWeight: 600 }}>
              {optimalCost}
            </div>
          </div>
          <div>
            <div style={{ color: "var(--c-ink-muted)", marginBottom: 4 }}>Guaranteed bound</div>
            <div style={{ fontFamily: "var(--f-mono)", fontSize: 16, fontWeight: 600, color: "var(--c-here)" }}>
              {algorithmCost}
            </div>
          </div>
        </div>

        <div style={{ marginTop: 12, fontSize: 12.5, color: "var(--c-ink-muted)" }}>
          Polynomial-time algorithm: cost ≤ {rho.toFixed(1)} × OPT
        </div>
      </div>

      <div style={{
        padding: 10, borderRadius: 6, background: "color-mix(in oklch, var(--c-bridge) 12%, transparent)",
        border: "1px solid var(--c-bridge)55", fontSize: 13,
      }}>
        <strong>Insight:</strong> A ρ-approximation guarantees the algorithm's cost is within ρ× of optimal, even for worst-case inputs.
        Smaller ρ = better guarantee. Find the smallest ρ for which you can prove your algorithm works!
      </div>
    </div>
  );
}

// Export for use in lessons
window.SpanningTreeSimulator = SpanningTreeSimulator;
window.BFSVisualizer = BFSVisualizer;
window.ApproximationRatioTuner = ApproximationRatioTuner;
