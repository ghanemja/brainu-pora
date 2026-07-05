/* global React */

// ── ATP shared atoms (Agent view) ────────────────────────────────
// Institutional aesthetic: university + standards body. Every atom
// guards against a missing window.ATP_DATA (renders null / falls back).

const { useState, useMemo, useEffect, useRef } = React;

const ATP_ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"];

function atpData() {
  return (typeof window !== "undefined" && window.ATP_DATA) || null;
}

// ── LevelGlyph — L1..L7 Roman-numeral seal chip ──────────────────
function LevelGlyph({ n = 1, size = 28 }) {
  const dim = typeof size === "number" ? size : ({ sm: 22, md: 28, lg: 40 }[size] || 28);
  const roman = ATP_ROMAN[n - 1] || "?";
  const color = `var(--c-atp-l${n}, var(--c-cert))`;
  return (
    <span
      className="lvl-glyph"
      title={`ATP Level ${n}`}
      style={{
        width: dim, height: dim,
        fontSize: Math.max(9, Math.round(dim * 0.34)),
        color,
      }}
    >
      {roman}
    </span>
  );
}

// ── CertBadge — institutional seal: double ring + glyph + mono label ──
function CertBadge({ cert, onClick, size = "md" }) {
  if (!cert) return null;
  const dim = typeof size === "number" ? size : ({ sm: 32, md: 46, lg: 62 }[size] || 46);
  const labelShort = (cert.label || `ATP-L${cert.layer}.${String(cert.domain || "").toLowerCase()}`).split("@")[0];
  const sealColor = cert.color || "var(--c-cert)";
  return (
    <button
      type="button"
      className="badge-seal"
      onClick={onClick}
      title={cert.sentence || labelShort}
      style={{ "--seal-c": sealColor }}
    >
      <span className="seal-ring" style={{ width: dim, height: dim, fontSize: Math.round(dim * 0.4) }}>
        <span className="seal-glyph">{cert.glyph || ATP_ROMAN[(cert.layer || 1) - 1]}</span>
      </span>
      <span className="seal-label" style={{ fontSize: dim < 40 ? 9 : 10 }}>{labelShort}</span>
    </button>
  );
}

// ── MasteryMeter — mastery bar + confidence halo; untested = hatched ──
function MasteryMeter({ value = 0, confidence = null, status = "developing" }) {
  const colors = {
    strong: "var(--c-cs)",
    developing: "var(--c-visited)",
    weak: "var(--c-here)",
    untested: "var(--c-ink-dim)",
  };
  const c = colors[status] || colors.developing;
  const untested = status === "untested";
  const tip = untested
    ? "untested — no exam evidence yet"
    : `${Math.round((value || 0) * 100)}% mastery` +
      (confidence != null ? ` · ${Math.round(confidence * 100)}% confidence` : "") +
      ` · ${status}`;
  return (
    <span className={"meter" + (untested ? " meter-untested" : "")} title={tip}>
      {!untested && confidence != null && (
        <span
          className="meter-conf"
          style={{
            width: `${Math.round(Math.min(1, Math.max(0, confidence)) * 100)}%`,
            background: `color-mix(in oklch, ${c} 30%, transparent)`,
          }}
        />
      )}
      {!untested && (
        <span
          className="meter-fill"
          style={{
            width: `${Math.round(Math.min(1, Math.max(0, value)) * 100)}%`,
            background: c,
            boxShadow: `0 0 6px color-mix(in oklch, ${c} 50%, transparent)`,
          }}
        />
      )}
    </span>
  );
}

// ── TierPill — Observer / Recommender / Executor with rank dots ──
function TierPill({ tier }) {
  const FALLBACK = {
    observer:    { name: "Observer",    rank: 1 },
    recommender: { name: "Recommender", rank: 2 },
    executor:    { name: "Executor",    rank: 3 },
  };
  const data = atpData();
  const t = (data && data.TIERS && data.TIERS[tier]) || FALLBACK[tier];
  if (!t) return null;
  return (
    <span className="tier-pill" data-tier={tier} title={t.sandbox ? `sandbox: ${t.sandbox}` : t.name}>
      <span className="tier-dots">
        {[1, 2, 3].map(i => (
          <span key={i} className={"dot-r" + (i <= t.rank ? " on" : "")} />
        ))}
      </span>
      {t.name}
    </span>
  );
}

// ── StageChip — early / mid / late career ────────────────────────
function StageChip({ stage }) {
  const map = {
    early: { label: "early-career", color: "var(--c-bridge)" },
    mid:   { label: "mid-career",   color: "var(--c-visited)" },
    late:  { label: "late-career",  color: "var(--c-summit)" },
  };
  const s = map[stage];
  if (!s) return null;
  return (
    <span
      className="tag"
      style={{ color: s.color, borderColor: `color-mix(in oklch, ${s.color} 45%, transparent)` }}
    >
      {s.label}
    </span>
  );
}

// ── LineChart — inline SVG; single [{ts,value}] or multi [{label,points,color}] ──
function LineChart({ series = [], height = 160, yLabel }) {
  const norm = useMemo(() => {
    if (!Array.isArray(series) || series.length === 0) return [];
    const PALETTE = ["var(--c-cert)", "var(--c-bridge)", "var(--c-here)", "var(--c-summit)", "var(--c-cs)"];
    if (series[0] && Array.isArray(series[0].points)) {
      return series
        .filter(s => s && Array.isArray(s.points) && s.points.length)
        .map((s, i) => ({
          label: s.label || `series ${i + 1}`,
          color: s.color || PALETTE[i % PALETTE.length],
          points: s.points,
        }));
    }
    return [{ label: yLabel || "", color: PALETTE[0], points: series }];
  }, [series, yLabel]);

  if (!norm.length) return null;

  const W = 560, H = Math.max(80, height);
  const padL = 42, padR = 14, padT = 16, padB = 22;
  const innerW = W - padL - padR, innerH = H - padT - padB;

  const vals = norm.flatMap(s => s.points.map(p => Number(p.value) || 0));
  let ymin = Math.min(0, ...vals);
  let ymax = Math.max(...vals);
  if (ymax <= 1 && ymin >= 0) { ymax = 1; ymin = 0; }
  else if (ymax === ymin) ymax = ymin + 1;
  else ymax += (ymax - ymin) * 0.08;

  const y = v => padT + (1 - (v - ymin) / (ymax - ymin)) * innerH;
  const xAt = (s, i) => padL + (s.points.length === 1 ? innerW / 2 : (i / (s.points.length - 1)) * innerW);
  const fmt = v => {
    const a = Math.abs(v);
    if (a >= 100) return String(Math.round(v));
    if (a >= 10) return v.toFixed(0);
    if (a >= 1) return v.toFixed(1);
    return v.toFixed(2);
  };
  const ticks = [0, 1, 2, 3, 4].map(k => ymin + ((ymax - ymin) * k) / 4);
  const baseY = y(ymin >= 0 ? Math.max(0, ymin) : 0);

  // x labels from the longest series
  const ref = norm.reduce((a, b) => (b.points.length > a.points.length ? b : a), norm[0]);
  const xLabels = ref.points.length > 1
    ? [
        { p: ref.points[0], i: 0, anchor: "start" },
        { p: ref.points[Math.floor((ref.points.length - 1) / 2)], i: Math.floor((ref.points.length - 1) / 2), anchor: "middle" },
        { p: ref.points[ref.points.length - 1], i: ref.points.length - 1, anchor: "end" },
      ]
    : [{ p: ref.points[0], i: 0, anchor: "middle" }];

  return (
    <div style={{ width: "100%" }}>
      {norm.length > 1 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, marginBottom: 6 }}>
          {norm.map((s, i) => (
            <span key={i} style={{
              display: "inline-flex", alignItems: "center", gap: 6,
              fontFamily: "var(--f-mono)", fontSize: 10.5, color: "var(--c-ink-muted)",
              letterSpacing: "0.05em", textTransform: "uppercase",
            }}>
              <span style={{ width: 8, height: 8, borderRadius: 999, background: s.color }} />
              {s.label}
            </span>
          ))}
        </div>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: "auto", display: "block" }}>
        {yLabel && (
          <text x={2} y={10} fontSize="9" fontFamily="var(--f-mono)" fill="var(--c-ink-dim)"
                letterSpacing="0.08em" style={{ textTransform: "uppercase" }}>
            {yLabel}
          </text>
        )}
        {/* grid + y ticks */}
        {ticks.map((t, i) => (
          <g key={i}>
            <line x1={padL} y1={y(t)} x2={W - padR} y2={y(t)}
                  stroke="var(--c-line)" strokeWidth="1" />
            <text x={padL - 6} y={y(t) + 3} fontSize="9" fontFamily="var(--f-mono)"
                  fill="var(--c-ink-dim)" textAnchor="end">
              {fmt(t)}
            </text>
          </g>
        ))}
        {/* series: area fill + line + endpoint dot */}
        {norm.map((s, si) => {
          const pts = s.points.map((p, i) => `${xAt(s, i).toFixed(1)},${y(Number(p.value) || 0).toFixed(1)}`);
          const line = `M${pts.join(" L")}`;
          const area = `${line} L${xAt(s, s.points.length - 1).toFixed(1)},${baseY.toFixed(1)} L${xAt(s, 0).toFixed(1)},${baseY.toFixed(1)} Z`;
          const last = s.points[s.points.length - 1];
          return (
            <g key={si}>
              <path d={area} fill={s.color} fillOpacity={norm.length > 1 ? 0.06 : 0.12} stroke="none" />
              <path d={line} fill="none" stroke={s.color} strokeWidth="1.6"
                    strokeLinejoin="round" strokeLinecap="round" />
              <circle cx={xAt(s, s.points.length - 1)} cy={y(Number(last.value) || 0)} r="2.6"
                      fill={s.color} stroke="var(--c-bg-elev)" strokeWidth="1" />
            </g>
          );
        })}
        {/* x labels */}
        {xLabels.map((xl, i) => (
          <text key={i} x={xAt(ref, xl.i)} y={H - 6} fontSize="9" fontFamily="var(--f-mono)"
                fill="var(--c-ink-dim)" textAnchor={xl.anchor}>
            {xl.p.ts != null ? xl.p.ts : xl.i + 1}
          </text>
        ))}
        {/* baseline */}
        <line x1={padL} y1={baseY} x2={W - padR} y2={baseY}
              stroke="var(--c-line-strong)" strokeWidth="1" />
      </svg>
    </div>
  );
}

// ── PyramidSVG — 7 stacked trapezoids + infra slab ───────────────
function PyramidSVG({ layers, activeId, onSelect, compact = false }) {
  const data = atpData();
  const L = layers || (data && data.LAYERS);
  if (!L || !L.length) return null;

  const FALLBACK_W = [1.0, 0.88, 0.76, 0.64, 0.52, 0.40, 0.28];
  const widthOf = ly => (typeof ly.width === "number" ? ly.width : FALLBACK_W[(ly.n || 1) - 1] || 0.5);
  const rows = [...L].sort((a, b) => (b.n || 0) - (a.n || 0)); // top (L7) first
  const topOf = ly => {
    const above = L.find(x => x.n === (ly.n || 0) + 1);
    return above ? widthOf(above) : widthOf(ly) * 0.45; // apex taper
  };

  const infra = data && data.INFRA;
  const infraLabel = infra
    ? `${infra.model || "Gemma 5.5"} · ${((infra.clusters || []).map(c => c.name).join(" / ")) || "H100 / Spark"}`
    : "Gemma 5.5 · H100 / Spark";

  return (
    <div className={"atp-pyramid" + (compact ? " compact" : "")}>
      {rows.map(ly => (
        <div
          key={ly.id}
          className={"atp-layer" + (activeId === ly.id ? " active" : "")}
          role="button"
          tabIndex={onSelect ? 0 : -1}
          aria-pressed={activeId === ly.id}
          title={`${ly.title || ly.id}${ly.modeledOn ? " — modeled on " + ly.modeledOn : ""}`}
          style={{
            "--tw": `${(topOf(ly) * 100).toFixed(2)}%`,
            "--bw": `${(widthOf(ly) * 100).toFixed(2)}%`,
            "--lc": ly.color || "var(--c-cert)",
            cursor: onSelect ? "pointer" : "default",
          }}
          onClick={() => onSelect && onSelect(ly.id)}
          onKeyDown={e => {
            if (onSelect && (e.key === "Enter" || e.key === " ")) {
              e.preventDefault();
              onSelect(ly.id);
            }
          }}
        >
          {!compact && (
            <span className="atp-layer-label">
              <span className="t-tag" style={{ color: ly.color || "var(--c-cert)" }}>L{ly.n}</span>
              <span style={{ fontSize: 12.5, fontWeight: 600, color: "var(--c-ink)" }}>{ly.title}</span>
            </span>
          )}
        </div>
      ))}
      <div className="atp-infra" title={infra ? `${infra.title || "Infrastructure"}${infra.notes ? " — " + infra.notes : ""}` : "Infrastructure foundation"}>
        <span style={{ opacity: 0.65 }}>▤</span>
        <span>{infraLabel}</span>
      </div>
    </div>
  );
}

// ── StatCard ─────────────────────────────────────────────────────
function StatCard({ label, value, hint }) {
  return (
    <div className="card" style={{ display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
      <span className="t-tag" style={{ color: "var(--c-ink-dim)" }}>{label}</span>
      <span className="t-num">{value}</span>
      {hint && <span className="t-cap" style={{ fontSize: 11.5 }}>{hint}</span>}
    </div>
  );
}

// ── EvidenceList — resolves ids via ATP_DATA.evidenceById ────────
const ATP_EVIDENCE_KIND = {
  exam_item:            { icon: "✎", label: "exam item" },
  training_interaction: { icon: "⟲", label: "training" },
  benchmark_run:        { icon: "▦", label: "benchmark" },
  hitl_reward:          { icon: "★", label: "HITL reward" },
  sme_signoff:          { icon: "✓", label: "SME sign-off" },
};
const ATP_OUTCOME_COLOR = {
  pass:    "var(--c-cs)",
  fail:    "var(--c-here)",
  reward:  "var(--c-cert)",
  penalty: "var(--c-here)",
  signed:  "var(--c-bridge)",
};

function EvidenceList({ ids = [] }) {
  const [open, setOpen] = useState({});
  const data = atpData();
  if (!data || !data.evidenceById) return null;
  const resolve = typeof data.evidenceById === "function"
    ? id => data.evidenceById(id)
    : id => data.evidenceById[id];
  const items = (ids || []).map(resolve).filter(Boolean);
  if (!items.length) {
    return <div className="t-cap" style={{ color: "var(--c-ink-dim)" }}>No evidence linked.</div>;
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      {items.map(ev => {
        const kind = ATP_EVIDENCE_KIND[ev.kind] || { icon: "•", label: ev.kind || "evidence" };
        const oc = ATP_OUTCOME_COLOR[ev.outcome] || "var(--c-ink-muted)";
        const isOpen = !!open[ev.id];
        return (
          <div key={ev.id}>
            <button
              type="button"
              className={"evidence-item" + (isOpen ? " open" : "")}
              onClick={() => setOpen(o => ({ ...o, [ev.id]: !o[ev.id] }))}
              aria-expanded={isOpen}
            >
              <span className="ev-icon" title={kind.label}>{kind.icon}</span>
              <span style={{ flex: 1, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {ev.summary}
              </span>
              <span className="tag" style={{
                color: oc,
                borderColor: `color-mix(in oklch, ${oc} 45%, transparent)`,
                flexShrink: 0,
              }}>
                {ev.outcome}
              </span>
              <span className="t-mono" style={{ fontSize: 10.5, color: "var(--c-ink-dim)", flexShrink: 0 }}>
                {ev.ts}
              </span>
              <span style={{ color: "var(--c-ink-dim)", fontSize: 10, flexShrink: 0 }}>
                {isOpen ? "▾" : "▸"}
              </span>
            </button>
            {isOpen && (
              <div className="evidence-detail">
                <div>{ev.detail}</div>
                {ev.source && (
                  <div className="t-mono" style={{ fontSize: 10.5, color: "var(--c-ink-dim)", marginTop: 6 }}>
                    source: {ev.source}
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ── SectionTitle ─────────────────────────────────────────────────
function SectionTitle({ kicker, title }) {
  return (
    <div style={{ marginBottom: 12 }}>
      {kicker && (
        <div className="t-tag" style={{ color: "var(--c-cert)", marginBottom: 4 }}>{kicker}</div>
      )}
      <div className="t-h2">{title}</div>
    </div>
  );
}

Object.assign(window, {
  LevelGlyph, CertBadge, MasteryMeter, TierPill, StageChip,
  LineChart, PyramidSVG, StatCard, EvidenceList, SectionTitle,
});
