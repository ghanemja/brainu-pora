// Brain University — frontend API client.
//
// Talks to api/server.py (FastAPI). When BU_API_BASE is unset OR an endpoint
// errors, read-only methods fall back to the local BU_DATA mock so the UI
// keeps working in design / static demo mode.
//
// Configure once at boot:
//   window.BU_API_BASE = "http://localhost:8090";
//   window.BU_USER_ID  = "anon-" + crypto.randomUUID();
//
// Auth: every request attaches Authorization: Bearer <token> read from
// sessionStorage.bu_auth_token (set by the login gate). If a request returns
// 401 the gate is re-shown.
//
// All methods are async + return plain JS objects.

(function () {
  const log = (...a) => console.log("[BU_API]", ...a);
  const base = () => (window.BU_API_BASE || "").replace(/\/+$/, "");
  const user = () => window.BU_USER_ID || "anon";
  const live = () => Boolean(base());

  function authHeader() {
    try {
      const tok = sessionStorage.getItem("bu_auth_token");
      return tok ? { "Authorization": `Bearer ${tok}` } : {};
    } catch (_) { return {}; }
  }

  function handle401(r) {
    if (r.status !== 401) return r;
    try { sessionStorage.removeItem("bu_auth_token"); } catch (_) {}
    // Re-show the gate by reloading; sessionStorage flag clears the auth too.
    if (typeof window !== "undefined") {
      try { sessionStorage.removeItem("bu_auth"); } catch (_) {}
      window.location.reload();
    }
    throw new Error("401 — session expired, re-authenticate");
  }

  async function jget(path, params) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const url = new URL(base() + path);
    if (params) Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, v);
    });
    const r = await fetch(url.toString(), { headers: authHeader() });
    handle401(r);
    if (!r.ok) throw new Error(`GET ${path} → ${r.status}`);
    return r.json();
  }

  async function jpost(path, body) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const r = await fetch(base() + path, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify(body || {}),
    });
    handle401(r);
    if (!r.ok) throw new Error(`POST ${path} → ${r.status}`);
    return r.json();
  }

  async function jpostMultipart(path, formData) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const r = await fetch(base() + path, {
      method: "POST", headers: authHeader(), body: formData,
    });
    handle401(r);
    if (!r.ok) throw new Error(`POST ${path} → ${r.status}`);
    return r.json();
  }

  function mediaUrl(p) {
    if (!p) return null;
    if (p.startsWith("http")) return p;
    return base() + "/media/" + p.replace(/^data\/sessions\/media\//, "");
  }

  const API = {
    live,
    mediaUrl,

    // ─── Health / graph ─────────────────────────────────────────────
    health:    () => jget("/health"),
    graph:     () => jget("/graph"),

    // ─── Trailhead / lesson ─────────────────────────────────────────
    async trailhead({ interest = "", n = 5 } = {}) {
      try { return await jget("/trailhead", { user_id: user(), interest, n }); }
      catch (e) {
        log("trailhead fallback", e.message);
        if (!window.BU_DATA) throw e;
        return { cards: (window.BU_DATA.FOUNDATION_PICKS || []).slice(0, n) };
      }
    },

    async lesson({ node, mode = "auto", interest = "", level = "" }) {
      try { return await jget("/lesson", { node, mode, interest, level }); }
      catch (e) {
        log("lesson fallback", e.message);
        if (!window.BU_DATA) throw e;
        return window.BU_DATA.lessonFor(node);
      }
    },

    // ─── Walks ──────────────────────────────────────────────────────
    walkStart: (start_node, planned) =>
      jpost("/walks/start", { user_id: user(), start_node, planned }),

    walkEvent: (walk_id, body) =>
      jpost(`/walks/${walk_id}/event`, { user_id: user(), ...body }),

    walkComplete: (walk_id) => jpost(`/walks/${walk_id}/complete`),

    // ─── Podcast ────────────────────────────────────────────────────
    podcastScript: ({ topic, length = "medium",
                       source_kind = "wiki", source_id = null,
                       angle = "" }) =>
      jget("/podcast/script", { topic, length, source_kind, source_id, angle }),

    podcastRender: (script, voice_backend = null) =>
      jpost("/podcast/render", { script, voice_backend }),

    podcastInterject: ({ script, turn_index, question }) =>
      jpost("/podcast/interject", { script, turn_index, question }),

    briefing: (node, interest = "") =>
      jget("/briefing", { node, interest }),

    // ─── Socratic ───────────────────────────────────────────────────
    socraticStart: (node) =>
      jpost("/socratic/start", { user_id: user(), node }),

    socraticStep: (session_id, answer) =>
      jpost("/socratic/step", { session_id, answer }),

    // ─── Spaced repetition / heatmap ────────────────────────────────
    srReview: (node, quality) =>
      jpost("/sr/review", { user_id: user(), node, quality }),

    srDue: (limit = 10) =>
      jget("/sr/due", { user_id: user(), limit }),

    heatmap: () => jget("/heatmap", { user_id: user() }),

    // ─── Feedback / propose / voice / citation / ingest ────────────
    feedback: (target_kind, target_id, thumb, note = "") =>
      jpost("/feedback", { user_id: user(), target_kind, target_id, thumb, note }),

    propose: (text) => jpost("/propose", { user_id: user(), text }),

    async voice(blob, lang = "en") {
      const fd = new FormData();
      fd.append("audio", blob, "voice.webm");
      fd.append("lang", lang);
      return jpostMultipart("/voice", fd);
    },

    citation: (claim, paperIds, k = 3) =>
      jget("/citation", { claim, papers: (paperIds || []).join(","), k }),

    arxivIngest: (interests, lookback_days = 1, max_per_interest = 5) =>
      jpost("/ingest/arxiv", { interests, lookback_days, max_per_interest }),

    // ─── Animated explainer (3b1b style) ─────────────────────────────
    animationScript: ({ passage, voiceover_hint = "", try_manim = false }) =>
      jpost("/animation/script", { passage, voiceover_hint, try_manim }),

    // ─── Papers library ──────────────────────────────────────────────
    papers: ({ q = "", limit = 200 } = {}) => jget("/papers", { q, limit }),
    paper:  (paper_id) => jget("/papers/" + encodeURIComponent(paper_id)),

    // ─── Local podcast (offline / no-API NotebookLM clone) ──────────
    podcastLocal: ({ source, mode = "auto", length = "medium", tts = "edge" }) =>
      jpost("/podcast/local", { source, mode, length, tts }),
    podcastLocalStatus: () => jget("/podcast/local/status"),
    podcastLocalInterject: ({ mp3, question, recent_quote = "", voice_backend = "kokoro" }) =>
      jpost("/podcast/local/interject",
            { mp3, question, recent_quote, voice_backend }),

    // ─── Background jobs (async render so the request doesn't block) ─
    podcastRenderAsync: (script, voice_backend = null) =>
      jpost("/podcast/render/async", { script, voice_backend }),
    podcastLocalAsync: ({ source, mode = "auto", length = "medium", tts = "edge" }) =>
      jpost("/podcast/local/async", { source, mode, length, tts }),
    jobStatus: (id) => jget("/jobs/" + encodeURIComponent(id)),

    // Submit an async job, poll until done/error, return the result payload.
    // onTick(status) fires each poll for progress UI.
    async runJob(submitFn, { interval = 2000, timeoutMs = 600000, onTick } = {}) {
      const { job_id } = await submitFn();
      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        await new Promise(r => setTimeout(r, interval));
        let s;
        try { s = await API.jobStatus(job_id); } catch { continue; }
        if (onTick) onTick(s);
        if (s.status === "done") return s.result;
        if (s.status === "error") throw new Error(s.error || "job failed");
      }
      throw new Error("job timed out");
    },
  };

  window.BU_API = API;
  log("ready, live=" + live());
})();
