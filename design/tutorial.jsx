/* global React */

const { useState: useTutState, useEffect: useTutEffect, useRef: useTutRef, useCallback: useTutCallback } = React;

// ─────────────────────────────────────────────────────────────────
// WALKTHROUGH — the first-visit tour of the learning path
//
// Five short steps that follow what a learner actually does: answer two
// questions on Courses, read the course map, take one lesson on The Walk,
// and come back later. Each step moves the app to the screen it describes
// and spotlights the real element (inside the Courses iframe too), so the
// learner sees the thing instead of reading about it.
//
// Auto-opens once per browser (localStorage flag); "?" in the top bar
// reopens it.
// ─────────────────────────────────────────────────────────────────

const TUT_FLAG = "bu.tutorial.seen.v2";   // v2: new walkthrough, shown once to everyone

const STEPS = [
  {
    screen: "courses",
    kicker: "Welcome",
    title: "Learn robot autonomy, one lesson at a time.",
    body: "Brain University turns Stanford's free Principles of Robot Autonomy course into a path built for you. Here is how it works. It takes about 30 seconds.",
    next: "Show me",
  },
  {
    screen: "courses",
    target: { frame: "pora-atlas", selector: "#main .card" },
    kicker: "Your path",
    title: "Answer two questions.",
    body: "Where you are starting from, and what you want to be able to do. Brain University skips what you already know and puts the rest in order.",
  },
  {
    screen: "courses",
    target: { frame: "pora-atlas", selector: ".graph" },
    kicker: "The map",
    title: "See the whole course.",
    body: "Every concept in the book, by part. Your path lights up in order as you answer, and green means you already know it. Click any concept to make it your goal.",
  },
  {
    screen: "walk-sample",
    target: { selector: ".walk-body" },
    place: "corner",
    kicker: "Lessons",
    title: "One lesson per screen.",
    body: "Each lesson has the key ideas, the Stanford lecture, a notebook you can run, and a quick check. The bar at the top shows every lesson on your walk; Next moves you on.",
  },
  {
    screen: "courses",
    target: { selector: 'nav.nav [data-nav="courses"]', pad: 6, minTop: 0 },
    kicker: "Coming back",
    title: "Pick up where you left off.",
    body: "Lessons you pass are ticked on your path and on the map, saved in this browser. Come back to Courses to continue or choose a new goal. The rest of the top bar (3D graph, arXivis, Podcast) is there when you want to explore.",
    next: "Start learning",
  },
];

// Find a step's target element (in the page, or inside the Courses iframe).
function tutTargetEl(target) {
  if (!target) return null;
  try {
    let doc = document;
    if (target.frame) {
      const f = document.querySelector(`iframe[src*="${target.frame}"]`);
      if (!f || !f.contentDocument) return null;
      doc = f.contentDocument;
    }
    return doc.querySelector(target.selector);
  } catch (e) { return null; }
}

// Return the target's box in page coordinates.
function tutTargetRect(target) {
  if (!target) return null;
  try {
    let doc = document, dx = 0, dy = 0;
    if (target.frame) {
      const f = document.querySelector(`iframe[src*="${target.frame}"]`);
      if (!f || !f.contentDocument) return null;
      const fr = f.getBoundingClientRect();
      doc = f.contentDocument; dx = fr.left; dy = fr.top;
    }
    const el = doc.querySelector(target.selector);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return null;
    const pad = target.pad ?? 10;
    // Clip to the visible window so a tall target still frames sensibly.
    const top = Math.max(target.minTop ?? 64, r.top + dy - pad), bottom = Math.min(window.innerHeight - 8, r.bottom + dy + pad);
    return { left: r.left + dx - pad, top, width: r.width + pad * 2, height: Math.max(40, bottom - top) };
  } catch (e) { return null; }
}

function Tutorial({ open, onClose, onJumpTo, onPreview }) {
  const [idx, setIdx] = useTutState(0);
  const [rect, setRect] = useTutState(null);
  const nextRef = useTutRef(null);
  const step = STEPS[idx];
  const last = idx === STEPS.length - 1;

  useTutEffect(() => { if (open) setIdx(0); }, [open]);

  // Move the app to the screen this step describes.
  useTutEffect(() => {
    if (open && onPreview && step) onPreview(step.screen);
  }, [open, idx]);

  // Measure the spotlight target; keep it in place on resize and scroll, and
  // retry briefly while the screen (or the Courses iframe) is still loading.
  useTutEffect(() => {
    if (!open) { setRect(null); return; }
    let tries = 0, timer = null;
    const measure = () => setRect(tutTargetRect(step && step.target));
    let scrolled = false;
    const poll = () => {
      // Bring the target on screen first (on phones the map sits below the fold).
      const el = tutTargetEl(step && step.target);
      if (el && !scrolled) {
        scrolled = true;
        const r0 = el.getBoundingClientRect(), win = el.ownerDocument.defaultView;
        if (r0.top < 72 || r0.top > win.innerHeight * 0.6) el.scrollIntoView({ block: "start", behavior: "auto" });
      }
      const r = tutTargetRect(step && step.target);
      setRect(r);
      if (step && step.target && !r && tries++ < 20) timer = setTimeout(poll, 150);
    };
    timer = setTimeout(poll, 120);
    window.addEventListener("resize", measure);
    window.addEventListener("scroll", measure, true);
    return () => { clearTimeout(timer); window.removeEventListener("resize", measure); window.removeEventListener("scroll", measure, true); };
  }, [open, idx]);

  const close = useTutCallback((goHome) => {
    try { localStorage.setItem(TUT_FLAG, "1"); } catch (e) {}
    onClose();
    if (goHome && onJumpTo) onJumpTo("courses");
    // Land on the first question, not wherever the tour scrolled to.
    try { const f = document.querySelector('iframe[src*="pora-atlas"]'); if (f && f.contentWindow) f.contentWindow.scrollTo(0, 0); } catch (e) {}
    window.scrollTo(0, 0);
  }, [onClose, onJumpTo]);

  const next = () => (last ? close(true) : setIdx(i => i + 1));
  const back = () => setIdx(i => Math.max(0, i - 1));

  useTutEffect(() => {
    if (!open) return;
    const onKey = (e) => {
      if (e.key === "Escape") close(true);
      else if (e.key === "ArrowRight") setIdx(i => Math.min(STEPS.length - 1, i + 1));
      else if (e.key === "ArrowLeft") setIdx(i => Math.max(0, i - 1));
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, close]);

  useTutEffect(() => { if (open && nextRef.current) nextRef.current.focus({ preventScroll: true }); }, [open, idx]);

  if (!open || !step) return null;

  // Put the card where it does not cover the spotlight.
  const vw = window.innerWidth, vh = window.innerHeight;
  let place = "center";
  if (rect && step.place) place = step.place;
  else if (rect) {
    const roomRight = vw - (rect.left + rect.width), roomLeft = rect.left;
    if (vw > 900 && roomRight >= 400) place = "right";
    else if (vw > 900 && roomLeft >= 400) place = "left";
    else place = rect.top + rect.height / 2 > vh / 2 ? "top" : "bottom";
  }
  const cardPos = {
    center: { left: "50%", top: "50%", transform: "translate(-50%, -50%)" },
    right:  { left: rect ? Math.min(vw - 404, rect.left + rect.width + 20) : 0, top: rect ? Math.max(72, Math.min(vh - 300, rect.top)) : 0 },
    left:   { left: rect ? Math.max(16, rect.left - 404) : 0, top: rect ? Math.max(72, Math.min(vh - 300, rect.top)) : 0 },
    top:    { left: "50%", top: 72, transform: "translateX(-50%)" },
    bottom: { left: "50%", bottom: 20, transform: "translateX(-50%)" },
    corner: { right: 20, bottom: 88 },
  }[place];

  return (
    <div className="tut" role="dialog" aria-modal="true" aria-labelledby="tut-title" aria-describedby="tut-body">
      {/* Dim everything except the target */}
      {rect
        ? <div className="tut-spot" style={{ left: rect.left, top: rect.top, width: rect.width, height: rect.height }} />
        : <div className="tut-dim" onClick={() => close(true)} />}

      <div className="tut-card" style={cardPos}>
        <div className="tut-top">
          <span className="tut-kicker">{step.kicker}</span>
          <button className="tut-skip" onClick={() => close(true)}>Skip</button>
        </div>
        <h2 id="tut-title" className="tut-title">{step.title}</h2>
        <p id="tut-body" className="tut-body" aria-live="polite">{step.body}</p>
        <div className="tut-foot">
          <div className="tut-dots" aria-label={`Step ${idx + 1} of ${STEPS.length}`}>
            {STEPS.map((_, i) => (
              <button key={i} className={i === idx ? "on" : i < idx ? "past" : ""}
                aria-label={`Go to step ${i + 1}`} aria-current={i === idx ? "step" : undefined}
                onClick={() => setIdx(i)} />
            ))}
          </div>
          <div className="tut-actions">
            {idx > 0 && <button className="btn ghost sm" onClick={back}>Back</button>}
            <button ref={nextRef} className="btn primary" onClick={next}>{step.next || "Next"}</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function shouldAutoOpenTutorial() {
  try { return !localStorage.getItem(TUT_FLAG); } catch (e) { return true; }
}

window.Tutorial = Tutorial;
window.BUTutorial = { TUT_FLAG, shouldAutoOpenTutorial };
