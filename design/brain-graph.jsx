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
  highlightSet = null,    // Set<id> — when set, dim everything not in set and brighten those that are
  highlightCluster = null,
  showLabels = "hubs",    // "all" | "hubs" | "none"
  cinematic = true,
  background = "#0a0e22",
  linkOpacity = 0.7,      // edge visibility (0.55 = faded, 0.8+ = bold)
  linkWidth = 1.5,        // edge thickness
  linkColor = "#7DD3FC",  // edge color (sky blue by default)
  signalFlow = false,     // animate signals/weights along edges (brain mode)
  customNodes = null,     // array of {id, name, cluster, degree, kind} — override BU_DATA.NODES
  customLinks = null,     // array of [src, tgt, weight?] — override BU_DATA.EDGES
  onNodeClick = () => {},
  onNodeHover = () => {},
  className = "",
  style = {},
}, ref) {
  const containerRef = useRef(null);
  const fgRef = useRef(null);
  const highlightSetRef = useRef(highlightSet);
  highlightSetRef.current = highlightSet;
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

    const baseNodes = customNodes || BU_DATA.NODES;
    const baseLinks = customLinks || BU_DATA.EDGES;
    const nodes = baseNodes.map(n => ({
      ...n,
      val: 1 + (n.degree || 1) * 0.4,
    }));
    const links = baseLinks.map(e => ({
      source: e[0],
      target: e[1],
      weight: e[2] || 1,
    }));

    // 3d-force-graph passes the bg color through `polished`, which can't
    // parse CSS variables. Resolve to a real hex by reading the live
    // computed style. The palette can flip at runtime via the tweaks
    // panel (light <-> dark), so we also re-resolve whenever the
    // documentElement's data-palette attribute changes.
    function resolveBg() {
      let v = background;
      if (typeof v === "string" && v.includes("var(")) {
        const name = v.match(/var\(([^,)]+)/)?.[1]?.trim();
        if (name) {
          const got = getComputedStyle(document.documentElement)
            .getPropertyValue(name).trim();
          if (got) v = got;
        }
      }
      if (!v || (typeof v === "string" && v.startsWith("var("))) {
        // Final fallback — read the live --c-bg directly. If still empty,
        // default to the brief's PAPER palette (light) since that's the
        // app's chosen default.
        const liveBg = getComputedStyle(document.documentElement)
          .getPropertyValue("--c-bg").trim();
        v = liveBg || "#efebe2";
      }
      return v;
    }
    let bgResolved = resolveBg();
    // Re-apply background whenever data-palette flips (light <-> dark).
    const paletteObserver = new MutationObserver(() => {
      try { Graph.backgroundColor(resolveBg()); } catch (_) {}
    });
    paletteObserver.observe(document.documentElement, {
      attributes: true, attributeFilter: ["data-palette"],
    });

    Graph
      .graphData({ nodes, links })
      .backgroundColor(bgResolved)
      .showNavInfo(false)
      .nodeRelSize(6)
      .nodeOpacity(0.95)
      .nodeVal(node => {
        const hs = highlightSetRef.current;
        if (hs && hs.size > 0 && hs.has(node.id)) {
          return Math.max(8, 3 + (node.degree || 1) * 1.2);
        }
        return 1 + (node.degree || 1) * 0.4;
      })
      .linkOpacity(linkOpacity)
      .linkWidth(linkWidth)
      .linkColor(() => {
        // Convert hex to rgba with opacity
        const hex = linkColor.replace("#", "");
        const r = parseInt(hex.substring(0, 2), 16);
        const g = parseInt(hex.substring(2, 4), 16);
        const b = parseInt(hex.substring(4, 6), 16);
        return `rgba(${r},${g},${b},${linkOpacity})`;
      })
      .nodeColor(node => colorForNode(node, { currentNode, visited, tourPath, highlightCluster, highlightSet }))
      .nodeLabel(node => `<div style="font-family:'JetBrains Mono',monospace;font-size:11px;background:#0f1733;color:#f5f7fb;padding:4px 8px;border-radius:4px;border:1px solid rgba(125,211,252,0.4)">${node.name}<br/><span style="opacity:0.6">course: ${BU_DATA.CLUSTERS[node.cluster].name}</span></div>`)
      .onNodeClick(node => {
        focusOn(node);
        onNodeClick(node);
      })
      .onNodeHover(node => onNodeHover(node))
      .cooldownTicks(120);

    // Signal-flow mode: animate moving particles along edges (neural firing)
    if (signalFlow) {
      Graph
        .linkDirectionalParticles(link => {
          // Vary particle count by edge — denser hubs = more activity
          const sId = typeof link.source === "object" ? link.source.id : link.source;
          const tId = typeof link.target === "object" ? link.target.id : link.target;
          const sNode = nodes.find(n => n.id === sId);
          const tNode = nodes.find(n => n.id === tId);
          const avgDeg = ((sNode?.degree || 1) + (tNode?.degree || 1)) / 2;
          return Math.max(2, Math.min(6, Math.round(avgDeg / 3)));
        })
        .linkDirectionalParticleWidth(2.5)
        .linkDirectionalParticleSpeed(link => {
          // Random speed per edge — feels like asynchronous neural traffic
          return 0.004 + Math.random() * 0.012;
        })
        .linkDirectionalParticleColor(link => {
          // Particle color = source cluster color (signal "from" tint)
          const sId = typeof link.source === "object" ? link.source.id : link.source;
          const sNode = nodes.find(n => n.id === sId);
          if (!sNode) return "#7DD3FC";
          if (sNode.kind === "defense") return "#FBB036";
          return BU_DATA.CLUSTERS[sNode.cluster]?.color || "#7DD3FC";
        });
    }

    // Three-pass: add per-node sprite labels for hubs
    Graph.nodeThreeObjectExtend(true);
    Graph.nodeThreeObject(node => makeLabelSprite(node, showLabels));

    // Slow auto-rotate when idle. If a highlightSet is active, orbit the
    // CENTROID of those nodes at close range; otherwise orbit the origin.
    let lastInteract = Date.now();
    const onUserInput = () => { lastInteract = Date.now(); };
    containerRef.current.addEventListener("mousedown", onUserInput);
    containerRef.current.addEventListener("wheel", onUserInput);
    containerRef.current.addEventListener("touchstart", onUserInput);

    let rotateAngle = 0;
    const tick = () => {
      if (!fgRef.current) return;
      if (cinematic && Date.now() - lastInteract > 3000) {
        rotateAngle += 0.0022;
        const data = fgRef.current.graphData();
        const hs = highlightSetRef.current;
        let cx = 0, cy = 0, cz = 0, radius = 360;
        if (hs && hs.size > 0 && data?.nodes) {
          let n = 0, maxR = 0;
          for (const node of data.nodes) {
            if (!hs.has(node.id)) continue;
            cx += node.x || 0; cy += node.y || 0; cz += node.z || 0;
            n++;
          }
          if (n > 0) {
            cx /= n; cy /= n; cz /= n;
            for (const node of data.nodes) {
              if (!hs.has(node.id)) continue;
              const dx = (node.x || 0) - cx;
              const dy = (node.y || 0) - cy;
              const dz = (node.z || 0) - cz;
              maxR = Math.max(maxR, Math.hypot(dx, dy, dz));
            }
            radius = Math.max(140, maxR * 2.6);
          }
        }
        Graph.cameraPosition({
          x: cx + radius * Math.sin(rotateAngle),
          y: cy + 40 * Math.sin(rotateAngle * 0.7),
          z: cz + radius * Math.cos(rotateAngle),
        }, { x: cx, y: cy, z: cz });
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
      try { paletteObserver.disconnect(); } catch (_) {}
      window.removeEventListener("resize", sizeFromContainer);
      containerRef.current?.removeEventListener("mousedown", onUserInput);
    };
  }, []); // build once

  // Re-color when state changes
  useEffect(() => {
    if (!fgRef.current) return;
    fgRef.current.nodeColor(node => colorForNode(node, { currentNode, visited, tourPath, highlightCluster, highlightSet }));
    fgRef.current.linkColor(link => linkColorFor(link, { tourPath, currentNode, defaultColor: linkColor, defaultOpacity: linkOpacity, highlightSet }));
    fgRef.current.linkWidth(link => linkWidthFor(link, { tourPath, defaultWidth: linkWidth, highlightSet }));
    fgRef.current.nodeThreeObject(node => makeLabelSprite(node, showLabels, { highlightSet }));
    fgRef.current.nodeVal(node => {
      if (highlightSet && highlightSet.size > 0 && highlightSet.has(node.id)) {
        return Math.max(8, 3 + (node.degree || 1) * 1.2);
      }
      return 1 + (node.degree || 1) * 0.4;
    });
  }, [currentNode, visited, tourPath, highlightCluster, showLabels, ready, linkColor, linkOpacity, linkWidth, highlightSet]);

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
    fitToSet(idSet, padding = 80) {
      // Zoom camera to fit just the nodes in idSet
      try {
        fgRef.current?.zoomToFit(1200, padding, n => idSet.has(n.id));
      } catch (_) {}
    },
    refresh() { fgRef.current?.refresh(); },
  }));

  return <div ref={containerRef} className={className} style={{ width: "100%", height: "100%", ...style }} />;
});

// ───── helpers ─────

function colorForNode(node, { currentNode, visited, tourPath, highlightCluster, highlightSet }) {
  // highlightSet mode dominates: dim everything outside the set, brighten inside
  if (highlightSet && highlightSet.size > 0) {
    if (highlightSet.has(node.id)) {
      if (node.id === currentNode) return "#f96167"; // coral for the focal node
      return "#fbb036"; // amber for activated
    }
    return "rgba(120,140,170,0.08)"; // heavy dim for non-activated
  }
  if (node.id === currentNode) return "#f96167"; // coral
  if (tourPath?.includes(node.id)) return "#fbb036"; // amber for tour
  if (visited?.has(node.id)) return "#fbb036"; // amber for visited
  if (node.kind === "defense") return "#FBB036"; // defense corpus = amber
  if (highlightCluster != null && node.cluster !== highlightCluster) {
    return "rgba(155,170,200,0.25)";
  }
  // default: cluster color, mildly darkened
  const c = BU_DATA.CLUSTERS[node.cluster];
  return c?.color || "#7dd3fc";
}

function _hexToRgba(hex, alpha) {
  const h = hex.replace("#", "");
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

function linkColorFor(link, { tourPath, currentNode, defaultColor = "#7DD3FC", defaultOpacity = 0.7, highlightSet }) {
  const sId = typeof link.source === "object" ? link.source.id : link.source;
  const tId = typeof link.target === "object" ? link.target.id : link.target;
  // highlightSet mode: only edges that connect two activated nodes show — everything else fades
  if (highlightSet && highlightSet.size > 0) {
    if (highlightSet.has(sId) && highlightSet.has(tId)) {
      return "rgba(251,176,54,0.95)";
    }
    return "rgba(120,140,170,0.04)";
  }
  const baseColor = _hexToRgba(defaultColor, defaultOpacity);
  if (!tourPath || tourPath.length < 2) return baseColor;
  for (let i = 0; i < tourPath.length - 1; i++) {
    if ((tourPath[i] === sId && tourPath[i+1] === tId) ||
        (tourPath[i] === tId && tourPath[i+1] === sId)) {
      return "rgba(251,176,54,0.95)";
    }
  }
  return baseColor;
}

function linkWidthFor(link, { tourPath, defaultWidth = 1.5, highlightSet }) {
  const sId = typeof link.source === "object" ? link.source.id : link.source;
  const tId = typeof link.target === "object" ? link.target.id : link.target;
  if (highlightSet && highlightSet.size > 0) {
    if (highlightSet.has(sId) && highlightSet.has(tId)) return 3.5;
    return 0.3;
  }
  if (!tourPath || tourPath.length < 2) return defaultWidth;
  for (let i = 0; i < tourPath.length - 1; i++) {
    if ((tourPath[i] === sId && tourPath[i+1] === tId) ||
        (tourPath[i] === tId && tourPath[i+1] === sId)) {
      return Math.max(defaultWidth * 1.5, 3.0);
    }
  }
  return defaultWidth;
}

function makeLabelSprite(node, mode, opts = {}) {
  const SpriteText = window.SpriteText;
  if (!SpriteText) return null;
  const highlightSet = opts.highlightSet;
  const isHighlighted = highlightSet && highlightSet.has(node.id);

  // In highlightSet mode: always label highlighted nodes, never label others
  if (highlightSet && highlightSet.size > 0) {
    if (!isHighlighted) return null;
  } else {
    if (mode === "none") return null;
    if (mode === "hubs" && node.degree < 9) return null;
  }

  const sprite = new SpriteText(node.name);
  sprite.color = isHighlighted ? "#fbb036" : "#f5f7fb";
  sprite.backgroundColor = isHighlighted ? "rgba(15,23,51,0.85)" : "rgba(15,23,51,0.65)";
  sprite.padding = 2;
  sprite.borderRadius = 2;
  sprite.fontFace = "JetBrains Mono, monospace";
  sprite.fontWeight = isHighlighted ? "700" : "500";
  sprite.textHeight = isHighlighted ? 6.5 : (mode === "all" ? 3 : (4 + Math.min(3, (node.degree - 9) * 0.4)));
  sprite.material.depthWrite = false;
  return sprite;
}

window.BrainGraph3D = BrainGraph3D;
