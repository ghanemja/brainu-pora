/* global React, ATP_DATA, StatCard, SectionTitle */

const { useState, useMemo, useEffect, useRef } = React;

// ─────────────────────────────────────────────────────────────────
// Guarded BU_API extension — Phase 6 company-knowledge methods
// (docs/HARDENING.md Phase 6).
//
// WHY HERE: design/api.js (owned by earlier phases) exposes only its
// finished methods plus live()/mediaUrl() — the jget/jpost/jpostMultipart
// helpers are closure-private and NOT exported. So this screen adds the
// knowledge methods itself through local fetch helpers that mirror the
// api.js idiom byte-for-byte: base from window.BU_API_BASE, bearer from
// sessionStorage.bu_auth_token, 401 → clear session + reload (the gate
// re-shows), 403 → error tagged {forbidden:true} carrying the server's
// VERBATIM `detail` string (e.g. "requires SME role") so the UI can show
// role errors as sent. The Object.assign is guarded: the moment api.js
// ships its own knowledgeUpload, this whole block becomes a no-op.
//
// Endpoint contract (api/knowledge.py — Phase 6 backend):
//   POST /knowledge/docs                   multipart "file" (md/txt/pdf,
//                                          ≤5 MB) → doc record. Org-scoped,
//                                          T2: encrypted at rest; NEVER
//                                          under /videos or /media —
//                                          TENANCY.md leak surface #4.
//                                          [admin|sme]
//   GET  /knowledge/docs                   → {docs:[{id,title,filename,
//                                          status,createdAt,summary,…}]}
//   POST /knowledge/drafts                 {docIds, title?} → draft dict
//                                          (sync; decrypted items included
//                                          for the reviewer)  [admin|sme]
//   POST /knowledge/drafts/{id}/approve    {note?}  [role=sme ONLY]
//   POST /knowledge/drafts/{id}/reject     {note?}  [role=sme ONLY]
//   POST /knowledge/drafts/{id}/exam       {dryRun, candidateSpec?,
//                                          agentId?} → {jobId}; poll
//                                          /jobs/{id} → award dict
//                                          [admin|sme]
// ─────────────────────────────────────────────────────────────────
(function () {
  if (!window.BU_API || window.BU_API.knowledgeUpload) return;

  const base = () => (window.BU_API_BASE || "").replace(/\/+$/, "");
  const live = () => Boolean(base());

  function authHeader() {
    try {
      const tok = sessionStorage.getItem("bu_auth_token");
      return tok ? { "Authorization": `Bearer ${tok}` } : {};
    } catch (_) { return {}; }
  }

  // 401 handling forks on WHO asked. User-initiated calls (upload, draft,
  // sign-off) mirror api.js: clear the session + reload so the gate
  // re-shows. PASSIVE calls (the on-mount doc-list read) must NOT do that:
  // a screen that reloads on a 401 it triggered itself remounts, re-fires
  // the read, 401s again — an infinite reload loop (seen live against the
  // deployed backend when the stored token is stale/absent). Passive reads
  // throw a tagged error and the section renders a signed-out state.
  function handle401(r, opts) {
    if (r.status !== 401) return r;
    if (opts && opts.passive) {
      const e = new Error("401 — not authorized");
      e.status = 401;
      e.unauthorized = true;
      throw e;
    }
    try { sessionStorage.removeItem("bu_auth_token"); } catch (_) {}
    try { sessionStorage.removeItem("bu_auth"); } catch (_) {}
    if (typeof window !== "undefined") window.location.reload();
    throw new Error("401 — session expired, re-authenticate");
  }

  // Unlike api.js's sync handler this one reads the body: the server's
  // `detail` (e.g. "requires SME role") must reach the UI verbatim.
  async function handleForbidden(r) {
    if (r.status !== 403) return r;
    let detail = "";
    try { detail = ((await r.json()) || {}).detail || ""; } catch (_) {}
    const e = new Error(detail || "403 — forbidden (requires a higher role)");
    e.forbidden = true;
    e.status = 403;
    throw e;
  }

  async function fail(r, label) {
    let detail = "";
    try { detail = ((await r.json()) || {}).detail || ""; } catch (_) {}
    const e = new Error(`${label} → ${r.status}` + (detail ? ` — ${detail}` : ""));
    e.status = r.status;
    throw e;
  }

  async function kget(path, params, opts) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const url = new URL(base() + path);
    if (params) Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, v);
    });
    const r = await fetch(url.toString(), { headers: authHeader() });
    handle401(r, opts);
    await handleForbidden(r);
    if (!r.ok) await fail(r, `GET ${path}`);
    return r.json();
  }

  async function kpost(path, body) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const r = await fetch(base() + path, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify(body || {}),
    });
    handle401(r);
    await handleForbidden(r);
    if (!r.ok) await fail(r, `POST ${path}`);
    return r.json();
  }

  async function kmultipart(path, formData) {
    if (!live()) throw new Error("BU_API_BASE not set");
    const r = await fetch(base() + path, {
      method: "POST", headers: authHeader(), body: formData,
    });
    handle401(r);
    await handleForbidden(r);
    if (!r.ok) await fail(r, `POST ${path}`);
    return r.json();
  }

  // Error → caller shape, following the api.js atpHitl idiom: 403 surfaces
  // {forbidden:true} with the verbatim message, an HTTP error keeps its
  // message, anything else (no base, network down) is {offline:true}.
  function degrade(e) {
    if (e && e.forbidden) return { ok: false, forbidden: true, error: e.message };
    if (e && typeof e.status === "number") return { ok: false, error: e.message };
    return { ok: false, offline: true, error: e && e.message };
  }

  Object.assign(window.BU_API, {
    // Upload one company document (md/txt/pdf) → org-scoped vault doc.
    async knowledgeUpload(file) {
      try {
        const fd = new FormData();
        fd.append("file", file, file.name);
        return await kmultipart("/knowledge/docs", fd);
      } catch (e) { return degrade(e); }
    },

    // The org's uploaded docs, latest first → {docs:[…]}. This is the one
    // PASSIVE (on-mount) call, so it must degrade instead of redirecting:
    //   401     → {unauthorized:true}  (signed-out state, NO reload loop)
    //   404/405 → {unavailable:true}   (backend predates Phase 6 → explainer)
    async knowledgeDocs() {
      try { return await kget("/knowledge/docs", null, { passive: true }); }
      catch (e) {
        if (e && e.unauthorized) {
          return { ok: false, unauthorized: true, docs: [] };
        }
        if (e && (e.status === 404 || e.status === 405)) {
          return { ok: false, offline: true, unavailable: true, docs: [] };
        }
        return { ...degrade(e), docs: [] };
      }
    },

    // Draft an L5 exam (blueprint + items) from the selected docs.
    // Synchronous on the current backend; {jobId} answers are handled
    // anyway in case drafting ever moves to the job queue.
    async knowledgeDraft(payload) {
      try { return await kpost("/knowledge/drafts", payload || {}); }
      catch (e) { return degrade(e); }
    },

    // SME sign-off (role=sme ONLY server-side; 403 details surface
    // verbatim — e.g. "draft sign-off requires role 'sme' …").
    async knowledgeApprove(draftId, note = "") {
      try {
        return await kpost(
          "/knowledge/drafts/" + encodeURIComponent(draftId) + "/approve",
          { note });
      } catch (e) { return degrade(e); }
    },

    async knowledgeReject(draftId, note = "") {
      try {
        return await kpost(
          "/knowledge/drafts/" + encodeURIComponent(draftId) + "/reject",
          { note });
      } catch (e) { return degrade(e); }
    },

    // Run the exam against an APPROVED draft's bank → {jobId}; poll
    // /jobs/{id} — the job result is the award dict (atp/exams.py shape).
    async knowledgeExamRun(draftId, payload) {
      try {
        return await kpost(
          "/knowledge/drafts/" + encodeURIComponent(draftId) + "/exam",
          payload || { dryRun: true });
      } catch (e) { return degrade(e); }
    },
  });
})();

// ─────────────────────────────────────────────────────────────────
// AGENT SCREEN 06 — VAULT-LD
// The institution's long-term memory. Four planes stacked like
// strata: markdown wiki ↔ knowledge graph + ontology ↔ linked-data
// bindings ↔ recursive memory consolidation loop (which writes back
// to the top — drawn as the return arrow on the right). Below: the
// playbook library, the certifiable unit of L5 company knowledge.
// Cross-screen convention: window.ATP_CERT_FOCUS = certId then
// goto('certs') opens that cert's meaning+evidence view.
// ─────────────────────────────────────────────────────────────────

const GOLD = "var(--c-cert, #e8c268)";

// One accent per plane, wiki → loop.
const PLANE_COLORS = ["var(--c-bridge)", "var(--c-cs)", "var(--c-atp-l6, #c5a3ff)", GOLD];

function AtpDataMissing() {
  return (
    <div style={{ maxWidth: 720, margin: "80px auto", padding: "0 28px" }}>
      <div className="card" style={{
        padding: 24,
        borderColor: "color-mix(in oklch, var(--c-here) 50%, transparent)",
      }}>
        <div className="t-tag" style={{ color: "var(--c-here)", marginBottom: 8 }}>
          ATP DATA MISSING
        </div>
        <div className="t-body">
          <span className="t-mono">window.ATP_DATA</span> is not loaded. Check that{" "}
          <span className="t-mono">design/atp_data.js</span> is included before the
          screen scripts (it is generated by{" "}
          <span className="t-mono">scripts/build_atp_data.py</span>).
        </div>
      </div>
    </div>
  );
}

function findAgent(id) {
  const d = window.ATP_DATA;
  if (!d) return null;
  if (typeof d.agentById === "function") return d.agentById(id) || null;
  return (d.AGENTS || []).find(a => a.id === id) || null;
}

const fmt = n => (n == null ? "—" : Number(n).toLocaleString());

// ── Architecture: one plane ──────────────────────────────────────
function VaultPlane({ plane, i }) {
  const c = PLANE_COLORS[i % PLANE_COLORS.length];
  return (
    <div className="card" style={{
      padding: "14px 18px",
      borderLeft: `3px solid ${c}`,
      display: "grid", gridTemplateColumns: "34px 1fr", gap: 14, alignItems: "start",
    }}>
      <div style={{
        width: 34, height: 34, borderRadius: "50%",
        display: "grid", placeItems: "center",
        border: `1.5px solid color-mix(in oklch, ${c} 60%, transparent)`,
        background: `color-mix(in oklch, ${c} 10%, var(--c-bg-elev))`,
        color: c, fontFamily: "var(--f-mono)", fontSize: 12, fontWeight: 600,
      }}>
        {String(i + 1).padStart(2, "0")}
      </div>
      <div style={{ minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
          <span className="t-h3">{plane.layer}</span>
          <span className="t-mono" style={{ fontSize: 11, color: c }}>{plane.tech}</span>
        </div>
        <div className="t-cap" style={{ marginTop: 3, lineHeight: 1.5 }}>{plane.role}</div>
      </div>
    </div>
  );
}

// Vertical two-way connector between planes.
function PlaneLink() {
  return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center",
      gap: 2, padding: "1px 0", color: "var(--c-ink-dim)",
    }} aria-hidden="true">
      <span style={{ width: 1, height: 7, background: "var(--c-line-strong)" }} />
      <span style={{ fontSize: 11, lineHeight: 1 }}>⇅</span>
      <span style={{ width: 1, height: 7, background: "var(--c-line-strong)" }} />
    </div>
  );
}

// ── Architecture diagram: planes + return loop on the right ─────
function VaultDiagram({ architecture }) {
  const planes = architecture || [];
  return (
    <div style={{ display: "flex", gap: 0, alignItems: "stretch" }}>
      {/* the four strata */}
      <div style={{ flex: 1, minWidth: 0, display: "flex", flexDirection: "column" }}>
        {planes.map((p, i) => (
          <React.Fragment key={i}>
            {i > 0 && <PlaneLink />}
            <VaultPlane plane={p} i={i} />
          </React.Fragment>
        ))}
      </div>

      {/* recursive consolidation loop: bottom plane writes back to the top */}
      <div aria-hidden="true" style={{ position: "relative", width: 64, flexShrink: 0 }}>
        <div style={{
          position: "absolute", top: 24, bottom: 24, left: 10, right: 22,
          borderTop: `1.5px dashed color-mix(in oklch, ${GOLD} 55%, transparent)`,
          borderRight: `1.5px dashed color-mix(in oklch, ${GOLD} 55%, transparent)`,
          borderBottom: `1.5px dashed color-mix(in oklch, ${GOLD} 55%, transparent)`,
          borderTopRightRadius: 16, borderBottomRightRadius: 16,
        }} />
        {/* arrowhead re-entering the top plane */}
        <span style={{
          position: "absolute", top: 17, left: 1,
          color: GOLD, fontSize: 12, lineHeight: 1,
        }}>◀</span>
        <span className="t-tag" style={{
          position: "absolute", top: "50%", right: 0,
          transform: "translateY(-50%)",
          writingMode: "vertical-rl",
          color: GOLD, letterSpacing: "0.14em",
          whiteSpace: "nowrap",
        }}>
          ↺ CONSOLIDATION WRITES BACK
        </span>
      </div>
    </div>
  );
}

// ── Playbook card (expands to steps + bound agents) ──────────────
function PlaybookCard({ pb, open, onToggle }) {
  const src = pb.source === "company"
    ? { label: "company", color: GOLD }
    : { label: "platform", color: "var(--c-bridge)" };
  return (
    <div className="card" style={{
      padding: 0, overflow: "hidden",
      borderColor: open ? `color-mix(in oklch, ${src.color} 45%, transparent)` : undefined,
    }}>
      <button onClick={onToggle} aria-expanded={open} style={{
        display: "block", width: "100%", textAlign: "left",
        padding: 16, background: "transparent", border: 0,
        color: "var(--c-ink)", cursor: "pointer", fontFamily: "var(--f-sans)",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8, flexWrap: "wrap" }}>
          <span className="tag" style={{
            color: src.color,
            borderColor: `color-mix(in oklch, ${src.color} 50%, transparent)`,
          }}>{src.label}</span>
          <span className="tag">{pb.domain}</span>
          <span style={{ marginLeft: "auto", color: "var(--c-ink-dim)", fontSize: 10 }}>
            {open ? "▾" : "▸"}
          </span>
        </div>
        <div className="t-h3" style={{ marginBottom: 4 }}>{pb.title}</div>
        <div className="t-cap" style={{ lineHeight: 1.5 }}>{pb.summary}</div>
        <div className="t-mono" style={{ fontSize: 10.5, color: "var(--c-ink-dim)", marginTop: 8,
                                          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {pb.vaultPath}
        </div>
      </button>

      {open && (
        <div style={{ padding: "0 16px 16px", borderTop: "1px solid var(--c-line)" }}>
          <div className="t-tag" style={{ color: "var(--c-ink-dim)", margin: "12px 0 8px" }}>
            STEPS · {(pb.steps || []).length}
          </div>
          <ol style={{ margin: 0, padding: 0, listStyle: "none",
                       display: "flex", flexDirection: "column", gap: 6 }}>
            {(pb.steps || []).map((s, i) => (
              <li key={i} style={{ display: "flex", gap: 10, fontSize: 12.5, lineHeight: 1.5 }}>
                <span className="t-mono" style={{ fontSize: 10.5, color: src.color,
                                                   flexShrink: 0, paddingTop: 2 }}>
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span>{s}</span>
              </li>
            ))}
          </ol>
          <div className="t-tag" style={{ color: "var(--c-ink-dim)", margin: "14px 0 8px" }}>
            BOUND AGENTS · {(pb.boundAgentIds || []).length}
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {(pb.boundAgentIds || []).map(id => {
              const a = findAgent(id);
              return (
                <span key={id} className="tag" title={a ? `${a.name} · L${a.level} · ${a.status}` : id}>
                  {a ? `${a.emoji} ${a.name}` : id}
                  {a && (
                    <span style={{ color: `var(--c-atp-l${a.level}, ${GOLD})`,
                                   fontFamily: "var(--f-mono)" }}> L{a.level}</span>
                  )}
                </span>
              );
            })}
            {!(pb.boundAgentIds || []).length && (
              <span className="t-cap" style={{ color: "var(--c-ink-dim)" }}>not yet bound</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────
// COMPANY KNOWLEDGE — Phase 6 ingestion pipeline (docs/HARDENING.md)
// upload (md/txt/pdf) → org-scoped Vault-LD pages (T2: encrypted at
// rest) → draft L5 exam (blueprint + items) → SME approve/reject →
// dry-run exam → award summary + #/cert/{id} deep link.
// Offline/demo mode renders an explainer with disabled controls.
// ─────────────────────────────────────────────────────────────────

const KNOWLEDGE_ACCEPT = ".md,.txt,.pdf";
const KNOWLEDGE_EXTS = ["md", "txt", "pdf"];

// Lifecycle on the backend: uploaded → drafted → signed (atp/knowledge.py);
// the extra keys keep the chip sensible if new states appear.
const DOC_STATUS_COLORS = {
  signed:     "var(--c-cs, #2ec4b6)",
  ingested:   "var(--c-cs, #2ec4b6)",
  ready:      "var(--c-cs, #2ec4b6)",
  drafted:    "var(--c-bridge, #7dd3fc)",
  uploaded:   "var(--c-visited, #fbb036)",
  processing: "var(--c-visited, #fbb036)",
  pending:    "var(--c-visited, #fbb036)",
  error:      "var(--c-here, #f96167)",
  failed:     "var(--c-here, #f96167)",
};

function DocStatusChip({ status }) {
  const s = String(status || "uploaded").toLowerCase();
  const c = DOC_STATUS_COLORS[s] || "var(--c-ink-dim)";
  return (
    <span className="tag" style={{
      color: c, borderColor: `color-mix(in oklch, ${c} 50%, transparent)`,
      fontFamily: "var(--f-mono)", fontSize: 10,
    }}>{s}</span>
  );
}

// Poll /jobs/{id} until done/error (api.js runJob idiom, local so it can
// accept either {jobId} or {job_id} submissions).
async function knowledgePollJob(jobId, onTick, { interval = 2000, timeoutMs = 600000 } = {}) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    await new Promise(r => setTimeout(r, interval));
    let s;
    try { s = await window.BU_API.jobStatus(jobId); } catch (_) { continue; }
    if (onTick) onTick(s);
    if (s.status === "done") return s.result;
    if (s.status === "error") throw new Error(s.error || "job failed");
  }
  throw new Error("job timed out");
}

function KnowledgeError({ msg }) {
  if (!msg) return null;
  return (
    <div className="t-cap" style={{
      color: "var(--c-here)", marginTop: 8, fontFamily: "var(--f-mono)", fontSize: 11.5,
    }}>
      ⚠ {msg}
    </div>
  );
}

// One draft item row (prompt clamped — SMEs expand nothing here, the full
// bank lands in atp/items/<certId>.json for real editing).
function DraftItemRow({ it }) {
  return (
    <div style={{
      display: "grid", gridTemplateColumns: "minmax(90px, 130px) 1fr 52px",
      gap: 10, padding: "8px 0", borderBottom: "1px solid var(--c-line)",
      alignItems: "start",
    }}>
      <div style={{ minWidth: 0 }}>
        <div className="t-mono" style={{ fontSize: 10.5, color: "var(--c-ink-muted)",
                                          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {it.id || "—"}
        </div>
        <div className="t-mono" style={{ fontSize: 10, color: "var(--c-ink-dim)", marginTop: 2 }}>
          {it.section || "—"}{it.type ? ` · ${it.type}` : ""}
        </div>
      </div>
      <div className="t-cap" style={{
        fontSize: 12.5, lineHeight: 1.5, minWidth: 0,
        display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden",
      }}>
        {it.prompt || "—"}
      </div>
      <div className="t-mono" style={{ fontSize: 11, textAlign: "right", color: "var(--c-ink-muted)" }}>
        {it.points != null ? `${it.points} pt` : ""}
      </div>
    </div>
  );
}

function CompanyKnowledgeSection({ l5Cert }) {
  const api = window.BU_API;
  const online = Boolean(api && typeof api.live === "function" && api.live());
  const l5CertId = (l5Cert && l5Cert.id) || "atp-l5-company-ops";

  const [docs, setDocs] = useState(null);        // null = loading, [] = none
  const [offline, setOffline] = useState(!online);
  const [signedOut, setSignedOut] = useState(false);
  const [listErr, setListErr] = useState(null);
  const [sel, setSel] = useState(() => new Set());
  const [uploadState, setUploadState] = useState({ busy: false, error: null });
  const [draft, setDraft] = useState(null);
  const [draftBusy, setDraftBusy] = useState(false);
  const [draftErr, setDraftErr] = useState(null);
  const [reviewBusy, setReviewBusy] = useState(false);
  const [reviewErr, setReviewErr] = useState(null);
  const [exam, setExam] = useState({ phase: "idle", tick: null, award: null, error: null });
  const fileRef = useRef(null);
  const alive = useRef(true);
  useEffect(() => () => { alive.current = false; }, []);

  const refreshDocs = async () => {
    if (!online) { setOffline(true); setDocs([]); return; }
    let res;
    try { res = await api.knowledgeDocs(); } catch (e) { res = { ok: false, offline: true }; }
    if (!alive.current) return;
    setSignedOut(false);
    if (res && Array.isArray(res.docs) && res.ok !== false) {
      setOffline(false); setListErr(null); setDocs(res.docs);
    } else if (res && res.unauthorized) {
      setOffline(false); setListErr(null); setSignedOut(true); setDocs([]);
    } else if (res && res.forbidden) {
      setOffline(false); setListErr(res.error || "insufficient role"); setDocs([]);
    } else if (res && res.offline) {
      setOffline(true); setDocs([]);
    } else {
      setOffline(false); setListErr((res && res.error) || "could not load documents"); setDocs([]);
    }
  };

  useEffect(() => { refreshDocs(); }, []);   // eslint-disable-line

  const toggleSel = (id) => setSel(prev => {
    const next = new Set(prev);
    if (next.has(id)) next.delete(id); else next.add(id);
    return next;
  });

  const onPickFile = async (e) => {
    const file = e.target.files && e.target.files[0];
    if (e.target) e.target.value = "";           // same file re-selectable
    if (!file) return;
    const ext = (file.name.split(".").pop() || "").toLowerCase();
    if (!KNOWLEDGE_EXTS.includes(ext)) {
      setUploadState({ busy: false, error: `unsupported type ".${ext}" — md, txt or pdf only` });
      return;
    }
    setUploadState({ busy: true, error: null });
    let res;
    try { res = await api.knowledgeUpload(file); } catch (err) { res = { ok: false, error: err && err.message }; }
    if (!alive.current) return;
    if (res && res.ok === false) {
      setUploadState({
        busy: false,
        error: res.offline
          ? "backend unreachable — upload needs the live API"
          : (res.error || "upload failed"),
      });
      return;
    }
    setUploadState({ busy: false, error: null });
    await refreshDocs();
  };

  const draftExam = async () => {
    if (!sel.size || draftBusy) return;
    setDraftBusy(true); setDraftErr(null); setDraft(null);
    setReviewErr(null); setExam({ phase: "idle", tick: null, award: null, error: null });
    try {
      let res = await api.knowledgeDraft({ docIds: [...sel] });
      if (res && res.ok === false) {
        throw Object.assign(new Error(
          res.offline ? "backend unreachable — drafting needs the live API"
                      : (res.error || "draft failed")), { surfaced: true });
      }
      const jobId = res && (res.jobId || res.job_id);
      if (jobId) res = await knowledgePollJob(jobId);
      if (!alive.current) return;
      setDraft(res || null);
      if (!res) setDraftErr("draft endpoint returned nothing");
    } catch (e) {
      if (alive.current) setDraftErr(e.message || "draft failed");
    } finally {
      if (alive.current) setDraftBusy(false);
    }
  };

  const review = async (action) => {
    if (!draft || reviewBusy) return;
    const draftId = draft.draftId || draft.id;
    if (!draftId) { setReviewErr("draft has no id — cannot review"); return; }
    setReviewBusy(true); setReviewErr(null);
    let res;
    try {
      res = action === "approve"
        ? await api.knowledgeApprove(draftId)
        : await api.knowledgeReject(draftId);
    } catch (e) { res = { ok: false, error: e && e.message }; }
    if (!alive.current) return;
    setReviewBusy(false);
    if (res && res.ok === false) {
      // 403 details (e.g. "requires SME role") surface VERBATIM.
      setReviewErr(res.offline
        ? "backend unreachable — SME sign-off needs the live API"
        : (res.error || `${action} failed`));
      return;
    }
    const merged = (res && (res.draft || (res.status ? res : null))) || null;
    setDraft(prev => ({ ...(prev || {}), ...(merged || {}), status: (merged && merged.status) || (action === "approve" ? "approved" : "rejected") }));
  };

  const runDryExam = async () => {
    if (exam.phase === "queued" || exam.phase === "running") return;
    const draftId = draft && (draft.draftId || draft.id);
    if (!draftId) return;
    setExam({ phase: "queued", tick: null, award: null, error: null });
    try {
      // Exam runs against the APPROVED draft's own bank (409 otherwise);
      // dryRun = deterministic stub models, zero model cost.
      const res = await api.knowledgeExamRun(draftId, { dryRun: true });
      if (res && res.ok === false) {
        throw new Error(res.forbidden
          ? (res.error || "insufficient role")
          : (res.offline
              ? "backend unreachable — exams need the live API"
              : (res.error || "exam enqueue failed")));
      }
      const jobId = res && (res.jobId || res.job_id);
      if (!jobId) throw new Error("exam enqueue returned no job id");
      if (alive.current) setExam({ phase: "running", tick: null, award: null, error: null });
      const award = await knowledgePollJob(jobId, (s) => {
        if (alive.current) setExam(prev => ({ ...prev, tick: s.status }));
      });
      if (alive.current) setExam({ phase: "done", tick: null, award, error: null });
    } catch (e) {
      if (alive.current) setExam({ phase: "error", tick: null, award: null, error: e.message || "exam failed" });
    }
  };

  const L5_RED = "var(--c-atp-l5, #f96167)";
  const blocked = offline || signedOut;   // controls disabled, section still renders
  const blueprintSections =
    (draft && draft.blueprint && (draft.blueprint.sections || draft.blueprint)) || [];
  const draftItems = (draft && draft.items) || [];
  const draftStatus = String((draft && draft.status) || "draft").toLowerCase();
  const award = exam.award;
  // Draft exams award against a synthetic per-org cert ref
  // ("org-l5-draft:<id>" — atp/knowledge.py EXAM_CERT_PREFIX), which the
  // seed certs screen can't resolve. Deep-link to the award's certId only
  // when it exists in the catalog; otherwise to the L5 template cert.
  const awardCertRef = (award && award.certId) || (draft && draft.examCertRef) || null;
  const awardLinkCert = (() => {
    try {
      const certs = (window.ATP_DATA && window.ATP_DATA.CERTS) || [];
      if (awardCertRef && certs.some(c => c.id === awardCertRef)) return awardCertRef;
    } catch (_) {}
    return l5CertId;
  })();

  return (
    <section style={{ marginBottom: 44 }}>
      <SectionTitle kicker="COMPANY KNOWLEDGE" title="Your documents, certifiable" />
      <p className="t-cap" style={{ margin: "0 0 16px", maxWidth: 680, lineHeight: 1.55 }}>
        Upload company documents (md / txt / pdf). They become org-scoped Vault-LD pages —
        encrypted at rest, visible only to your org — and the university drafts an L5
        company-knowledge exam from them for your SMEs to sign off.
      </p>

      {offline && (
        <div className="card recessed" style={{
          padding: "12px 16px", marginBottom: 16,
          borderLeft: "3px solid var(--c-ink-dim)",
        }}>
          <span className="t-tag" style={{ color: "var(--c-ink-dim)" }}>OFFLINE DEMO — </span>
          <span className="t-cap">
            the ingestion pipeline needs the live backend. Start it
            (<span className="t-mono">uvicorn api.server:app --port 8090</span>) and reload;
            in this static demo the controls below stay disabled.
          </span>
        </div>
      )}
      {signedOut && (
        <div className="card recessed" style={{
          padding: "12px 16px", marginBottom: 16,
          borderLeft: "3px solid var(--c-ink-dim)",
        }}>
          <span className="t-tag" style={{ color: "var(--c-ink-dim)" }}>NOT SIGNED IN — </span>
          <span className="t-cap">
            company documents are org-scoped: authenticate to load your organization's
            uploads. Controls stay disabled until then.
          </span>
        </div>
      )}
      {listErr && !offline && <KnowledgeError msg={listErr} />}

      {/* Upload + doc list */}
      <div className="card" style={{ padding: 16, marginBottom: 14 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
          <input ref={fileRef} type="file" accept={KNOWLEDGE_ACCEPT}
                 style={{ display: "none" }} onChange={onPickFile} />
          <button className="btn primary"
                  disabled={blocked || uploadState.busy}
                  title={offline ? "Backend offline — uploads disabled in the static demo"
                       : signedOut ? "Sign in first — uploads are org-scoped"
                       : "md / txt / pdf"}
                  onClick={() => fileRef.current && fileRef.current.click()}
                  style={{ opacity: blocked ? 0.5 : 1 }}>
            {uploadState.busy ? "… uploading" : "⤒ Upload document"}
          </button>
          <span className="t-mono" style={{ fontSize: 11, color: "var(--c-ink-dim)" }}>
            md · txt · pdf → org-scoped, encrypted at rest
          </span>
          <span className="t-mono" style={{ marginLeft: "auto", fontSize: 11, color: "var(--c-ink-dim)" }}>
            {docs ? `${docs.length} document${docs.length === 1 ? "" : "s"}` : "loading…"}
          </span>
        </div>
        <KnowledgeError msg={uploadState.error} />

        {docs && docs.length > 0 && (
          <div style={{ marginTop: 12 }}>
            {docs.map(d => {
              const id = d.id || d.docId || d.filename;
              return (
                <label key={id} title={d.summary || undefined} style={{
                  display: "flex", alignItems: "center", gap: 10, padding: "8px 0",
                  borderBottom: "1px solid var(--c-line)", cursor: blocked ? "default" : "pointer",
                }}>
                  <input type="checkbox" checked={sel.has(id)} disabled={blocked}
                         onChange={() => toggleSel(id)} />
                  <span style={{ fontWeight: 600, fontSize: 13, minWidth: 0,
                                 overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {d.title || d.name || d.filename || id}
                  </span>
                  <DocStatusChip status={d.status} />
                  <span className="t-mono" style={{ marginLeft: "auto", fontSize: 10.5, color: "var(--c-ink-dim)", whiteSpace: "nowrap" }}>
                    {(d.createdAt || d.ts || "").slice(0, 10)}
                  </span>
                </label>
              );
            })}
          </div>
        )}
        {docs && docs.length === 0 && !blocked && !listErr && (
          <div className="t-cap" style={{ color: "var(--c-ink-dim)", marginTop: 12 }}>
            No documents yet — upload the first one to begin.
          </div>
        )}

        <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 14, flexWrap: "wrap" }}>
          <button className="btn"
                  disabled={blocked || !sel.size || draftBusy}
                  onClick={draftExam}
                  title={offline ? "Backend offline"
                       : signedOut ? "Sign in first"
                       : (!sel.size ? "Select at least one document" : `Draft an L5 exam from ${sel.size} selected document${sel.size === 1 ? "" : "s"}`)}
                  style={{
                    color: L5_RED,
                    borderColor: `color-mix(in oklch, ${L5_RED} 50%, transparent)`,
                    opacity: (blocked || !sel.size) ? 0.5 : 1,
                  }}>
            {draftBusy ? "… drafting" : "▤ Draft L5 exam"}
          </button>
          <span className="t-cap" style={{ color: "var(--c-ink-dim)", fontSize: 12 }}>
            {sel.size ? `${sel.size} selected` : "select documents to include"}
          </span>
        </div>
        <KnowledgeError msg={draftErr} />
      </div>

      {/* Draft review panel */}
      {draft && (
        <div className="card slide-up" style={{ padding: 16, marginBottom: 14, borderLeft: `3px solid ${L5_RED}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", marginBottom: 8 }}>
            <span className="t-tag" style={{ color: L5_RED }}>DRAFT L5 EXAM · FOR SME REVIEW</span>
            <span className="t-mono" style={{ fontSize: 11, color: "var(--c-ink-muted)" }}>
              {draft.certLabel || draft.label || l5CertId}
              {draft.examCertRef ? ` · ${draft.examCertRef}` : ""}
            </span>
            <span className="tag" style={{
              marginLeft: "auto", fontFamily: "var(--f-mono)", fontSize: 10,
              color: draftStatus === "approved" ? "var(--c-cs, #2ec4b6)"
                   : draftStatus === "rejected" ? "var(--c-here)" : "var(--c-visited, #fbb036)",
            }}>
              {draftStatus}
            </span>
          </div>

          <div className="t-tag" style={{ color: "var(--c-ink-dim)", margin: "10px 0 6px" }}>
            BLUEPRINT · {blueprintSections.length} SECTIONS
          </div>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            {blueprintSections.map((s, i) => (
              <span key={i} className="tag" style={{ fontFamily: "var(--f-mono)", fontSize: 10.5 }}>
                {(s && s.name) || String(s)}
                {s && s.weight != null ? ` · ${Math.round(s.weight * 100)}%` : ""}
              </span>
            ))}
            {!blueprintSections.length && (
              <span className="t-cap" style={{ color: "var(--c-ink-dim)" }}>no blueprint returned</span>
            )}
          </div>

          <div className="t-tag" style={{ color: "var(--c-ink-dim)", margin: "14px 0 4px" }}>
            ITEMS · {draftItems.length}
          </div>
          {draftItems.map((it, i) => <DraftItemRow key={it.id || i} it={it} />)}
          {!draftItems.length && (
            <div className="t-cap" style={{ color: "var(--c-ink-dim)" }}>no items returned</div>
          )}

          {/* SME sign-off */}
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 14, flexWrap: "wrap" }}>
            {draftStatus !== "approved" && (
              <button className="btn" disabled={reviewBusy} onClick={() => review("approve")}
                      style={{ color: "var(--c-cs, #2ec4b6)",
                               borderColor: "color-mix(in oklch, var(--c-cs, #2ec4b6) 50%, transparent)" }}>
                ✓ Approve (SME sign-off)
              </button>
            )}
            {draftStatus !== "approved" && draftStatus !== "rejected" && (
              <button className="btn" disabled={reviewBusy} onClick={() => review("reject")}
                      style={{ color: "var(--c-here)",
                               borderColor: "color-mix(in oklch, var(--c-here) 50%, transparent)" }}>
                ✕ Reject
              </button>
            )}
            {draftStatus === "approved" && exam.phase !== "done" && (
              <button className="btn primary"
                      disabled={exam.phase === "queued" || exam.phase === "running"}
                      onClick={runDryExam}>
                {exam.phase === "queued" ? "… enqueueing"
                  : exam.phase === "running" ? `… running${exam.tick ? ` (${exam.tick})` : ""}`
                  : "▶ Run exam (dry)"}
              </button>
            )}
            <span className="t-cap" style={{ color: "var(--c-ink-dim)", fontSize: 12 }}>
              {draftStatus === "approved"
                ? "dry run: full engine, no model cost — judge/candidate separation still enforced"
                : "sign-off requires the SME role — no agent is L5-certified without it"}
            </span>
          </div>
          <KnowledgeError msg={reviewErr} />
          <KnowledgeError msg={exam.phase === "error" ? exam.error : null} />

          {/* Award summary */}
          {exam.phase === "done" && award && (
            <div className="card recessed slide-up" style={{
              marginTop: 14, padding: 14,
              borderLeft: `3px solid ${award.verdict === "pass" ? "var(--c-cs, #2ec4b6)" : "var(--c-here)"}`,
            }}>
              <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
                <span className="t-tag" style={{
                  color: award.verdict === "pass" ? "var(--c-cs, #2ec4b6)" : "var(--c-here)",
                }}>
                  {award.verdict === "pass" ? "✓ PASS" : "✕ FAIL"} · {award.dryRun ? "DRY RUN" : "LIVE"}
                </span>
                <span className="t-mono" style={{ fontSize: 12 }}>
                  overall <span style={{ color: GOLD, fontWeight: 600 }}>{Math.round((award.score || 0) * 100)}%</span>
                </span>
                {award.itemBreakdown && (
                  <span className="t-mono" style={{ fontSize: 12 }}>
                    <span style={{ color: "var(--c-cs, #2ec4b6)" }}>{award.itemBreakdown.passed} passed</span>{" · "}
                    <span style={{ color: "var(--c-here)" }}>{award.itemBreakdown.failed} failed</span>{" · "}
                    <span style={{ color: "var(--c-visited)" }}>{award.itemBreakdown.flagged} flagged</span>
                  </span>
                )}
                <span className="t-mono" style={{ fontSize: 11, color: "var(--c-ink-dim)" }}>
                  {(award.evidenceIds || []).length} signed evidence rows
                </span>
              </div>
              {award.sectionScores && (
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 10 }}>
                  {Object.entries(award.sectionScores).map(([name, sc]) => (
                    <span key={name} className="tag" style={{ fontFamily: "var(--f-mono)", fontSize: 10.5 }}>
                      {name} {Math.round((sc || 0) * 100)}%
                    </span>
                  ))}
                </div>
              )}
              <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", marginTop: 12 }}>
                <a className="btn ghost" href={"#/cert/" + encodeURIComponent(awardLinkCert)}
                   style={{ textDecoration: "none", fontSize: 12, padding: "4px 10px" }}>
                  Open the certification → <span className="t-mono" style={{ fontSize: 10.5 }}>#/cert/{awardLinkCert}</span>
                </a>
                {awardCertRef && awardCertRef !== awardLinkCert && (
                  <span className="t-mono" style={{ fontSize: 10.5, color: "var(--c-ink-dim)" }}>
                    examined as {awardCertRef}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

// ── Screen ───────────────────────────────────────────────────────
function ATPVault({ goto }) {
  const data = window.ATP_DATA;
  if (!data) return <AtpDataMissing />;

  const vault = data.VAULT || {};
  const stats = vault.stats || {};
  const playbooks = data.PLAYBOOKS || [];

  const [srcFilter, setSrcFilter] = useState("all");       // all | company | platform
  const [domFilter, setDomFilter] = useState("all");
  const [openId, setOpenId] = useState(null);

  const domains = useMemo(
    () => [...new Set(playbooks.map(p => p.domain).filter(Boolean))].sort(),
    [playbooks]
  );

  const shown = playbooks.filter(p =>
    (srcFilter === "all" || p.source === srcFilter) &&
    (domFilter === "all" || p.domain === domFilter)
  );

  // The playbook library IS the L5 evidence base — link to the L5 cert.
  const l5Cert = (data.CERTS || []).find(c => c.layer === 5) || null;
  const openL5 = () => {
    if (!l5Cert || !goto) return;
    window.ATP_CERT_FOCUS = l5Cert.id;
    goto("certs");
  };

  const statCards = [
    { label: "WIKI PAGES", value: fmt(stats.wikiPages), hint: "human-readable ground truth" },
    { label: "KG NODES", value: fmt(stats.kgNodes), hint: "entities in the graph" },
    { label: "KG EDGES", value: fmt(stats.kgEdges), hint: "typed relations" },
    { label: "ONTOLOGY CLASSES", value: fmt(stats.ontologyClasses), hint: "shared vocabulary" },
    { label: "PLAYBOOKS", value: fmt(stats.playbooks != null ? stats.playbooks : playbooks.length), hint: "operational procedures" },
  ];

  return (
    <div style={{ minHeight: "calc(100vh - 56px)", padding: "48px 28px 80px" }}>
      <div style={{ maxWidth: 1120, margin: "0 auto" }}>

        {/* Header */}
        <div style={{ marginBottom: 30, maxWidth: 760 }}>
          <div className="t-tag" style={{ color: GOLD }}>INSTITUTIONAL MEMORY</div>
          <h1 className="t-display" style={{ margin: "6px 0 8px" }}>
            {vault.name || "Vault-LD"}
          </h1>
          <p className="t-cap" style={{ fontSize: 14, lineHeight: 1.6, margin: 0 }}>
            {vault.description ||
              "The company's knowledge, kept in four linked planes: a markdown wiki humans can read, a knowledge graph and ontology machines can traverse, linked-data bindings that keep both in sync, and a recursive consolidation loop that distills every agent interaction back into durable memory."}
          </p>
        </div>

        {/* Stats row */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
          gap: 12, marginBottom: 40,
        }}>
          {statCards.map(s => (
            <StatCard key={s.label} label={s.label} value={s.value} hint={s.hint} />
          ))}
        </div>

        {/* Architecture */}
        <section style={{ marginBottom: 44 }}>
          <SectionTitle kicker="ARCHITECTURE" title="Four planes, one loop" />
          <p className="t-cap" style={{ margin: "0 0 16px", maxWidth: 680, lineHeight: 1.55 }}>
            Each plane stays legible to the one above it: the wiki grounds the graph, the graph
            structures the bindings, and the consolidation loop writes what agents learn back
            to the top — so memory compounds instead of fragmenting.
          </p>
          <div style={{ maxWidth: 780 }}>
            {(vault.architecture || []).length
              ? <VaultDiagram architecture={vault.architecture} />
              : <div className="t-cap" style={{ color: "var(--c-ink-dim)" }}>No architecture data.</div>}
          </div>
        </section>

        {/* Company knowledge — Phase 6 ingestion → L5 exam pipeline */}
        <CompanyKnowledgeSection l5Cert={l5Cert} />

        {/* Playbook library */}
        <section>
          <SectionTitle kicker="PLAYBOOK LIBRARY" title="Procedures agents are bound to" />

          {/* L5 note */}
          <div className="card recessed" style={{
            padding: "12px 16px", marginBottom: 16,
            borderLeft: `3px solid var(--c-atp-l5, #f96167)`,
            display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap",
          }}>
            <div style={{ flex: 1, minWidth: 240 }}>
              <span className="t-tag" style={{ color: "var(--c-atp-l5, #f96167)" }}>L5 · COMPANY KNOWLEDGE — </span>
              <span className="t-cap">
                playbooks are the certifiable unit of company knowledge: each one is provenance
                for L5 exam items, and no agent is L5-certified without SME sign-off on the
                playbooks it is bound to.
              </span>
            </div>
            {l5Cert && (
              <button className="btn ghost" onClick={openL5} style={{ fontSize: 12, padding: "4px 10px" }}>
                See the L5 certification →
              </button>
            )}
          </div>

          {/* Filters */}
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center", marginBottom: 14 }}>
            <span className="t-tag" style={{ color: "var(--c-ink-dim)", marginRight: 2 }}>SOURCE</span>
            {["all", "company", "platform"].map(s => (
              <button key={s} className="btn" onClick={() => setSrcFilter(s)} style={{
                fontSize: 12, padding: "4px 10px",
                color: srcFilter === s ? GOLD : "var(--c-ink-muted)",
                borderColor: srcFilter === s
                  ? `color-mix(in oklch, ${GOLD} 50%, transparent)` : "var(--c-line)",
                background: srcFilter === s
                  ? `color-mix(in oklch, ${GOLD} 8%, transparent)` : "transparent",
              }}>
                {s}
              </button>
            ))}
            <span className="t-tag" style={{ color: "var(--c-ink-dim)", margin: "0 2px 0 14px" }}>DOMAIN</span>
            {["all", ...domains].map(d => (
              <button key={d} className="btn" onClick={() => setDomFilter(d)} style={{
                fontSize: 12, padding: "4px 10px",
                color: domFilter === d ? "var(--c-bridge)" : "var(--c-ink-muted)",
                borderColor: domFilter === d
                  ? "color-mix(in oklch, var(--c-bridge) 50%, transparent)" : "var(--c-line)",
                background: domFilter === d
                  ? "color-mix(in oklch, var(--c-bridge) 8%, transparent)" : "transparent",
              }}>
                {d}
              </button>
            ))}
            <span className="t-mono" style={{ marginLeft: "auto", fontSize: 11, color: "var(--c-ink-dim)" }}>
              {shown.length}/{playbooks.length} shown
            </span>
          </div>

          {/* Cards */}
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
            gap: 14, alignItems: "start",
          }}>
            {shown.map(pb => (
              <PlaybookCard key={pb.id} pb={pb}
                open={openId === pb.id}
                onToggle={() => setOpenId(openId === pb.id ? null : pb.id)} />
            ))}
          </div>
          {!shown.length && (
            <div className="t-cap" style={{ color: "var(--c-ink-dim)", padding: "18px 0" }}>
              No playbooks match this filter.
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

Object.assign(window, { ATPVault });
