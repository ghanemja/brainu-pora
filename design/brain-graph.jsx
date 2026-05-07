/* global React, BU_DATA */

// BrainGraph3D — real WebGL 3D force-directed graph.
// Wraps the `3d-force-graph` library (which uses Three.js under the hood).
// Exposes imperative-ish API via ref forwarding so parent screens can:
//  - focus the camera on a node
//  - highlight a tour path
//  - toggle label density
//  - record an orbit clip

const { useEffect, useRef, useImperativeHandle, forwardRef, useState } = React;

const BrainGraph3D = forwardRef(function BrainGraph3D({
  currentNode = null,
  visited = new Set(),
  tourPath = [],          // array of node ids in order
  highlightCluster = null,
  showLabels = "hubs",    // "all" | "hubs" | "none"
  cinematic = true,
  background = "#0a0e22",
  onNodeClick = () => {},
  onNodeHover = () => {},
  className = "",
  style = {},
}, ref) {
  const containerRef = useRef(null);
  const fgRef = useRef(null);
  const [ready, setReady] = useState(false);

  // Initial graph build
  useEffect(() => {
    if (!containerRef.current) return;
    if (!window.ForceGraph3D) {
      console.warn("3d-force-graph not loaded yet");
      return;
    }
    const Graph = window.ForceGraph3D()(containerRef.current);
    fgRef.current = Graph;

    // 3d-force-graph snapshots container size at construct time. If our
    // parent is mid-fade-in (0×0 during React mount) the graph stays 0×0
    // forever and the canvas appears blank. Set an explicit size now and
    // keep it in sync via a ResizeObserver — this is what makes the canvas
    // actually fill the viewport across page/tab transitions.
    const sizeFromContainer = () => {
      const r = containerRef.current?.getBoundingClientRect();
      const w = Math.max(320, Math.floor(r?.width || window.innerWidth));
      const h = Math.max(240, Math.floor(r?.height || window.innerHeight));
      Graph.width(w).height(h);
    };
    sizeFromContainer();
    const ro = new ResizeObserver(sizeFromContainer);
    ro.observe(containerRef.current);
    window.addEventListener("resize", sizeFromContainer);

    const nodes = BU_DATA.NODES.map(n => ({
      ...n,
      val: 1 + n.degree * 0.4,
    }));
    const links = BU_DATA.EDGES.map(([s,t]) => ({ source: s, target: t }));

    // 3d-force-graph passes the bg color through `polished`, which can't
    // parse CSS variables like `var(--c-bg)`. Resolve to a real hex first.
    let bgResolved = background;
    if (typeof bgResolved === "string" && bgResolved.includes("var(")) {
      const varName = bgResolved.match(/var\(([^,)]+)/)?.[1]?.trim();
      if (varName) {
        const got = getComputedStyle(document.documentElement)
          .getPropertyValue(varName).trim();
        if (got) bgResolved = got;
      }
    }
    if (!bgResolved || bgResolved.startsWith("var(")) bgResolved = "#0a0e22";

    Graph
      .graphData({ nodes, links })
      .backgroundColor(bgResolved)
      .showNavInfo(false)
      .nodeRelSize(6)
      .nodeOpacity(0.95)
      .linkOpacity(0.55)
      .linkWidth(1.0)
      .linkColor(() => "rgba(82,121,193,0.55)")
      .nodeColor(node => colorForNode(node, { currentNode, visited, tourPath, highlightCluster }))
      .nodeLabel(node => `<div style="font-family:'JetBrains Mono',monospace;font-size:11px;background:#0f1733;color:#f5f7fb;padding:4px 8px;border-radius:4px;border:1px solid rgba(125,211,252,0.4)">${node.name}<br/><span style="opacity:0.6">course: ${BU_DATA.CLUSTERS[node.cluster].name}</span></div>`)
      .onNodeClick(node => {
        focusOn(node);
        onNodeClick(node);
      })
      .onNodeHover(node => onNodeHover(node))
      .cooldownTicks(120);

    // Three-pass: add per-node sprite labels for hubs
    Graph.nodeThreeObjectExtend(true);
    Graph.nodeThreeObject(node => makeLabelSprite(node, showLabels));

    // Slow auto-rotate when idle
    let lastInteract = Date.now();
    const onUserInput = () => { lastInteract = Date.now(); };
    containerRef.current.addEventListener("mousedown", onUserInput);
    containerRef.current.addEventListener("wheel", onUserInput);
    containerRef.current.addEventListener("touchstart", onUserInput);

    let rotateAngle = 0;
    const tick = () => {
      if (!fgRef.current) return;
      if (cinematic && Date.now() - lastInteract > 4000) {
        rotateAngle += 0.0015;
        const dist = 360;
        Graph.cameraPosition({
          x: dist * Math.sin(rotateAngle),
          y: 60 + 30 * Math.sin(rotateAngle * 0.7),
          z: dist * Math.cos(rotateAngle),
        });
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);

    setReady(true);

    // Initial camera position
    setTimeout(() => {
      Graph.cameraPosition({ x: 0, y: 80, z: 380 }, { x: 0, y: 0, z: 0 }, 1500);
    }, 100);

    // Fit-all once the force layout settles so we never render an empty
    // viewport. Runs ~3s after mount; safe to no-op if user already moved
    // the camera before then.
    setTimeout(() => {
      try { Graph.zoomToFit(1200, 60); } catch (_) {}
    }, 3200);

    return () => {
      try { Graph._destructor && Graph._destructor(); } catch (_) {}
      try { ro.disconnect(); } catch (_) {}
      window.removeEventListener("resize", sizeFromContainer);
      containerRef.current?.removeEventListener("mousedown", onUserInput);
    };
  }, []); // build once

  // Re-color when state changes
  useEffect(() => {
    if (!fgRef.current) return;
    fgRef.current.nodeColor(node => colorForNode(node, { currentNode, visited, tourPath, highlightCluster }));
    fgRef.current.linkColor(link => linkColorFor(link, { tourPath, currentNode }));
    fgRef.current.linkWidth(link => linkWidthFor(link, { tourPath }));
    fgRef.current.nodeThreeObject(node => makeLabelSprite(node, showLabels));
  }, [currentNode, visited, tourPath, highlightCluster, showLabels, ready]);

  function focusOn(node, distance = 90) {
    if (!fgRef.current || !node) return;
    const dist = distance;
    const norm = Math.hypot(node.x || 1, node.y || 1, node.z || 1) || 1;
    const ratio = 1 + dist / norm;
    fgRef.current.cameraPosition(
      { x: node.x * ratio, y: node.y * ratio, z: node.z * ratio },
      node, 1500
    );
  }

  useImperativeHandle(ref, () => ({
    focusOn(nodeId, distance) {
      const node = fgRef.current?.graphData().nodes.find(n => n.id === nodeId);
      if (node) focusOn(node, distance);
    },
    cameraPosition(...args) { return fgRef.current?.cameraPosition(...args); },
    pulseNode(nodeId) {
      // The color update will pulse via tourPath; this is a hook for future tweens.
    },
    refresh() { fgRef.current?.refresh(); },
  }));

  return <div ref={containerRef} className={className} style={{ width: "100%", height: "100%", ...style }} />;
});

// ───── helpers ─────

function colorForNode(node, { currentNode, visited, tourPath, highlightCluster }) {
  if (node.id === currentNode) return "#f96167"; // coral
  if (tourPath?.includes(node.id)) return "#fbb036"; // amber for tour
  if (visited?.has(node.id)) return "#fbb036"; // amber for visited
  if (highlightCluster != null && node.cluster !== highlightCluster) {
    return "rgba(155,170,200,0.25)";
  }
  // default: cluster color, mildly darkened
  const c = BU_DATA.CLUSTERS[node.cluster];
  return c?.color || "#7dd3fc";
}

function linkColorFor(link, { tourPath, currentNode }) {
  if (!tourPath || tourPath.length < 2) return "rgba(125,211,252,0.18)";
  const sId = typeof link.source === "object" ? link.source.id : link.source;
  const tId = typeof link.target === "object" ? link.target.id : link.target;
  for (let i = 0; i < tourPath.length - 1; i++) {
    if ((tourPath[i] === sId && tourPath[i+1] === tId) ||
        (tourPath[i] === tId && tourPath[i+1] === sId)) {
      return "rgba(251,176,54,0.85)";
    }
  }
  return "rgba(125,211,252,0.12)";
}

function linkWidthFor(link, { tourPath }) {
  if (!tourPath || tourPath.length < 2) return 0.6;
  const sId = typeof link.source === "object" ? link.source.id : link.source;
  const tId = typeof link.target === "object" ? link.target.id : link.target;
  for (let i = 0; i < tourPath.length - 1; i++) {
    if ((tourPath[i] === sId && tourPath[i+1] === tId) ||
        (tourPath[i] === tId && tourPath[i+1] === sId)) {
      return 2.5;
    }
  }
  return 0.6;
}

function makeLabelSprite(node, mode) {
  if (mode === "none") return null;
  if (mode === "hubs" && node.degree < 9) return null;

  const SpriteText = window.SpriteText;
  if (!SpriteText) return null;

  const sprite = new SpriteText(node.name);
  sprite.color = "#f5f7fb";
  sprite.backgroundColor = "rgba(15,23,51,0.65)";
  sprite.padding = 2;
  sprite.borderRadius = 2;
  sprite.fontFace = "JetBrains Mono, monospace";
  sprite.fontWeight = "500";
  sprite.textHeight = mode === "all" ? 3 : (4 + Math.min(3, (node.degree - 9) * 0.4));
  sprite.material.depthWrite = false;
  return sprite;
}

window.BrainGraph3D = BrainGraph3D;
