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
// 401 the gate is re-shown. A 403 (authenticated, insufficient role) NEVER
// clears the session — helpers throw an error tagged {forbidden:true} and
// write methods surface {ok:false, forbidden:true} to the caller.
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

  // 403 = authenticated but lacking role (e.g. viewer submitting HITL).
  // Unlike 401 this must NOT nuke the session: throw a tagged error so
  // callers can render a role message instead of the offline fallback.
  function handleForbidden(r) {
    if (r.status !== 403) return r;
    const e = new Error("403 — forbidden (requires a higher role)");
    e.forbidden = true;
    e.status = 403;
    throw e;
  }

  async function jget(path, params) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const url = new URL(base() + path);
    if (params) Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, v);
    });
    const r = await fetch(url.toString(), { headers: authHeader() });
    handle401(r);
    handleForbidden(r);
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
    handleForbidden(r);
    if (!r.ok) throw new Error(`POST ${path} → ${r.status}`);
    return r.json();
  }

  async function jpostMultipart(path, formData) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const r = await fetch(base() + path, {
      method: "POST", headers: authHeader(), body: formData,
    });
    handle401(r);
    handleForbidden(r);
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

    // ─── ATP (Agent University) ──────────────────────────────────────
    // Read methods fall back to the window.ATP_DATA seed blob when the
    // backend is unreachable (same pattern as trailhead()).
    async atpData() {
      try { return await jget("/atp/data"); }
      catch (e) {
        log("atpData fallback", e.message);
        if (!window.ATP_DATA) throw e;
        return window.ATP_DATA;
      }
    },

    async atpAgents() {
      try { return await jget("/atp/agents"); }
      catch (e) {
        log("atpAgents fallback", e.message);
        if (!window.ATP_DATA) throw e;
        return { agents: window.ATP_DATA.AGENTS || [] };
      }
    },

    async atpAgent(id) {
      try { return await jget("/atp/agents/" + encodeURIComponent(id)); }
      catch (e) {
        log("atpAgent fallback", e.message);
        if (!window.ATP_DATA) throw e;
        const a = window.ATP_DATA.agentById
          ? window.ATP_DATA.agentById(id)
          : (window.ATP_DATA.AGENTS || []).find(x => x.id === id);
        if (!a) throw e;
        return a;
      }
    },

    async atpCerts() {
      try { return await jget("/atp/certs"); }
      catch (e) {
        log("atpCerts fallback", e.message);
        if (!window.ATP_DATA) throw e;
        return { certs: window.ATP_DATA.CERTS || [] };
      }
    },

    async atpStandard() {
      try { return await jget("/atp/standard"); }
      catch (e) {
        log("atpStandard fallback", e.message);
        if (!window.ATP_DATA) throw e;
        return window.ATP_DATA.STANDARD || {};
      }
    },

    async atpMarketplace() {
      try { return await jget("/atp/marketplace"); }
      catch (e) {
        log("atpMarketplace fallback", e.message);
        if (!window.ATP_DATA) throw e;
        return window.ATP_DATA.MARKETPLACE || { listings: [] };
      }
    },

    // POST — no local fallback; signal offline so the UI degrades gracefully.
    // A 403 (role too low) is surfaced as {forbidden:true}, NOT offline.
    async atpHitl(payload) {
      try { return await jpost("/atp/hitl", payload); }
      catch (e) {
        if (e && e.forbidden) {
          log("atpHitl forbidden", e.message);
          return { ok: false, forbidden: true };
        }
        log("atpHitl offline", e.message);
        return { ok: false, offline: true };
      }
    },

    async atpHitlLog(limit = 100) {
      try { return await jget("/atp/hitl", { limit }); }
      catch (e) {
        log("atpHitlLog fallback", e.message);
        if (!window.ATP_DATA) throw e;
        const rows = ((window.ATP_DATA.RL || {}).hitlLog || []);
        // Log is stored oldest → newest; serve latest first.
        return { events: rows.slice(-limit).reverse() };
      }
    },

    // ─── Expert composition / train-to-order (docs/ATP.md §7) ────────
    async atpRequests(limit = 100) {
      try { return await jget("/atp/requests", { limit }); }
      catch (e) {
        log("atpRequests fallback", e.message);
        if (!window.ATP_DATA) throw e;
        return { requests: (window.ATP_DATA.EXPERT_REQUESTS || []).slice(0, limit) };
      }
    },

    // Commission an expert: payload {major, specialty, badgeIds, packId}.
    // Offline fallback runs the client-side matcher (ATP_DATA.matchExperts)
    // and returns a local, non-persisted request object marked {offline:true}
    // so the wizard still renders a result panel in static demo mode.
    async atpCompose(payload) {
      const p = payload || {};
      try { return await jpost("/atp/requests", p); }
      catch (e) {
        log("atpCompose offline", e.message);
        if (!window.ATP_DATA || !window.ATP_DATA.matchExperts) throw e;
        const match = window.ATP_DATA.matchExperts({
          course:          p.major ?? p.course,
          concentrationId: p.specialty ?? p.concentrationId,
          badgeIds:        p.badgeIds || [],
          packId:          p.packId ?? null,
        });
        const exact   = (match.exact || [])[0] || null;
        const partial = match.partial || [];
        const now     = new Date().toISOString().slice(0, 10);
        const stages  = ["requested", "corpus-mapped", "fine-tuning",
                         "certifying", "listed"];
        return {
          id: "req-local-" + Date.now().toString(36),
          ts: now,
          major:     p.major ?? p.course ?? "",
          specialty: p.specialty ?? p.concentrationId ?? "",
          badgeIds:  p.badgeIds || [],
          packId:    p.packId ?? null,
          layers:  [],
          corpora: [],
          status: exact ? "matched" : (partial.length ? "gap" : "training"),
          matchedAgentId: exact,
          gap: (!exact && partial.length) ? {
            covered: partial[0].covered || [],
            missing: partial[0].missing || [],
            coveringAgentIds: partial.map(x => x.agentId),
          } : null,
          pipeline: stages.map((stage, i) =>
            ({ stage, ts: i === 0 ? now : null, done: i === 0 })),
          resultAgentId: null,
          match,
          offline: true,
        };
      }
    },

    // ─── Certification engine (docs/HARDENING.md Phase 3) ────────────
    // Enqueue an exam run: payload {certId, candidateSpec?, agentId?,
    // dryRun}. Returns {jobId} — poll with jobStatus()/runJob(); the job
    // result is the award dict. 403 (role too low) surfaces
    // {forbidden:true}, any other failure {offline:true} (atpHitl idiom).
    async atpExamRun(payload) {
      try { return await jpost("/atp/exams/run", payload); }
      catch (e) {
        if (e && e.forbidden) {
          log("atpExamRun forbidden", e.message);
          return { ok: false, forbidden: true };
        }
        log("atpExamRun offline", e.message);
        return { ok: false, offline: true };
      }
    },

    // Org-scoped cert awards, latest first. Awards only exist server-side
    // (signed exam runs), so offline mode has none to show.
    async atpAwards(limit = 100) {
      try { return await jget("/atp/awards", { limit }); }
      catch (e) {
        log("atpAwards fallback", e.message);
        return { awards: [] };
      }
    },

    // One signed evidence row. Offline fallback serves the seed evidence
    // record from window.ATP_DATA marked {seed:true} (no sig/prevHash —
    // seed rows predate the signing chain).
    async atpEvidence(id) {
      try { return await jget("/atp/evidence/" + encodeURIComponent(id)); }
      catch (e) {
        log("atpEvidence fallback", e.message);
        if (!window.ATP_DATA) throw e;
        const ev = window.ATP_DATA.evidenceById
          ? window.ATP_DATA.evidenceById(id)
          : (window.ATP_DATA.EVIDENCE || []).find(x => x.id === id);
        if (!ev) throw e;
        return { ...ev, seed: true };
      }
    },

    // Verification needs the server-held signing key + chain — there is no
    // meaningful offline answer, so failures report {ok:false, offline:true}.
    async atpEvidenceVerify(id) {
      try {
        return await jget("/atp/evidence/" + encodeURIComponent(id) + "/verify");
      } catch (e) {
        log("atpEvidenceVerify offline", e.message);
        return { ok: false, offline: true };
      }
    },

    async atpChainVerify() {
      try { return await jget("/atp/chain/verify"); }
      catch (e) {
        log("atpChainVerify offline", e.message);
        return { ok: false, offline: true };
      }
    },

    // ─── Billing & licensing (docs/HARDENING.md Phase 4) ─────────────
    // Licenses only exist server-side, so there is no seed fallback:
    // failures degrade to {ok:false, offline:true}; a 403 (role too low)
    // surfaces {ok:false, forbidden:true} (atpHitl idiom).
    async billingLicenses() {
      try { return await jget("/billing/licenses"); }
      catch (e) {
        if (e && e.forbidden) return { ok: false, forbidden: true };
        log("billingLicenses offline", e.message);
        return { ok: false, offline: true, licenses: [] };
      }
    },

    // Issue a manual license: payload {agentId, kind}. The response's
    // licenseKey is shown ONCE — the server stores only a hash.
    async billingIssue(payload) {
      try { return await jpost("/billing/licenses", payload); }
      catch (e) {
        if (e && e.forbidden) return { ok: false, forbidden: true };
        log("billingIssue offline", e.message);
        return { ok: false, offline: true };
      }
    },

    async billingRevoke(id, reason = "") {
      try {
        return await jpost(
          "/billing/licenses/" + encodeURIComponent(id) + "/revoke",
          { reason });
      } catch (e) {
        if (e && e.forbidden) return { ok: false, forbidden: true };
        log("billingRevoke offline", e.message);
        return { ok: false, offline: true };
      }
    },

    async billingUsage(licenseId = null) {
      try { return await jget("/billing/usage", { licenseId }); }
      catch (e) {
        if (e && e.forbidden) return { ok: false, forbidden: true };
        log("billingUsage offline", e.message);
        return { ok: false, offline: true };
      }
    },

    // Stripe self-serve checkout → {url}. 404s when the backend has no
    // STRIPE_API_KEY (manual licensing still works) — that surfaces here
    // as {ok:false, offline:true} and the UI should fall back to the
    // "contact us / invoice" path.
    async billingCheckout(payload) {
      try { return await jpost("/billing/checkout", payload); }
      catch (e) {
        if (e && e.forbidden) return { ok: false, forbidden: true };
        log("billingCheckout offline", e.message);
        return { ok: false, offline: true };
      }
    },

    // Licensed expert chat. Auth is the LICENSE KEY (X-ATP-License-Key),
    // not the session bearer, and licensing is server-truth: NO offline
    // fallback, and a 401/403 here is about the key — it must never clear
    // the session or reload the gate, so this bypasses handle401().
    async expertChat(agentId, messages, licenseKey) {
      if (!live()) throw new Error("BU_API_BASE not set");
      const r = await fetch(
        base() + "/experts/" + encodeURIComponent(agentId) + "/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...authHeader(),
            ...(licenseKey ? { "X-ATP-License-Key": licenseKey } : {}),
          },
          body: JSON.stringify({ messages: messages || [] }),
        });
      if (!r.ok) {
        let detail = "";
        try { detail = (await r.json()).detail || ""; } catch (_) {}
        const e = new Error(`POST /experts/${agentId}/chat → ${r.status}` +
                            (detail ? ` — ${detail}` : ""));
        e.status = r.status;
        e.licenseError = r.status === 401 || r.status === 403;
        throw e;
      }
      return r.json();
    },
  };

  window.BU_API = API;
  log("ready, live=" + live());
})();
