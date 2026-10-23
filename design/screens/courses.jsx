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
      const steps = m.steps.filter((s) => typeof s === "string").slice(0, 40);
      if (steps.length && typeof BU_DATA.poraTour === "function") onWalk(steps);
    };
    window.addEventListener("message", onMsg);
    return () => window.removeEventListener("message", onMsg);
  }, [onWalk]);

  return (
    <div style={{ position: "relative", width: "100%", height: "calc(100vh - 64px)" }}>
      <iframe
        ref={frameRef}
        title="PoRA Atlas: Principles of Robot Autonomy"
        src="courses/pora-atlas.html?embed=bu"
        style={{ border: 0, width: "100%", height: "100%", display: "block" }}
      />
    </div>
  );
}

window.Courses = Courses;
