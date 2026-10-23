/* global React */

// ─────────────────────────────────────────────────────────────────
// SCREEN 11 — COURSES
// Curated textbook courses mapped onto the concept graph. The first
// is Principles of Robot Autonomy (PoRA): the Atlas page plans a
// prerequisite route and hands it back here to be walked as a tour.
// Source of truth: courses/pora/pora.json → courses/pora/build.py.
// ─────────────────────────────────────────────────────────────────

function Courses({ onWalk }) {
  const frameRef = React.useRef(null);

  React.useEffect(() => {
    const onMsg = (e) => {
      if (e.origin !== window.location.origin) return;
      if (!frameRef.current || e.source !== frameRef.current.contentWindow) return;
      const m = e.data || {};
      if (m.type !== "pora:walk" || !Array.isArray(m.steps) || !m.steps.length) return;
      const steps = m.steps.filter((s) => typeof s === "string").slice(0, 80);
      if (!steps.length || typeof BU_DATA.poraTour !== "function") return;
      const key = BU_DATA.poraTour(steps, "pora-route");
      if (key) onWalk(key);
    };
    window.addEventListener("message", onMsg);
    return () => window.removeEventListener("message", onMsg);
  }, [onWalk]);

  // Fill exactly the space below the app header, so the outer page never
  // scrolls and the course's own drawers and headers stay on screen.
  const boxRef = React.useRef(null);
  const [height, setHeight] = React.useState("calc(100vh - 64px)");
  React.useLayoutEffect(() => {
    const size = () => {
      if (!boxRef.current) return;
      const top = boxRef.current.getBoundingClientRect().top + window.scrollY;
      setHeight(Math.max(320, window.innerHeight - top) + "px");
    };
    window.scrollTo(0, 0);
    size();
    window.addEventListener("resize", size);
    return () => window.removeEventListener("resize", size);
  }, []);
  const [loaded, setLoaded] = React.useState(false);
  const [slow, setSlow] = React.useState(false);
  React.useEffect(() => {
    const t = setTimeout(() => setSlow(true), 8000);
    return () => clearTimeout(t);
  }, []);

  return (
    <div ref={boxRef} style={{ position: "relative", width: "100%", height }}>
      {!loaded && (
        <div role="status" style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center",
                                     color: "var(--c-ink-muted)", fontSize: 14, textAlign: "center", padding: 24 }}>
          {slow
            ? <span>The course is taking a while to load. <a href="courses/pora-atlas.html" target="_blank" rel="noopener noreferrer">Open it in a new tab</a> or reload the page.</span>
            : "Loading Principles of Robot Autonomy…"}
        </div>
      )}
      <iframe
        ref={frameRef}
        title="Principles of Robot Autonomy course"
        src="courses/pora-atlas.html?embed=bu&v=2"
        onLoad={() => setLoaded(true)}
        style={{ border: 0, width: "100%", height: "100%", display: "block",
                 opacity: loaded ? 1 : 0, transition: "opacity .2s" }}
      />
    </div>
  );
}

window.Courses = Courses;
