"""
atp/reportcard.py — Phase 6 (docs/HARDENING.md): official report-card PDF.

    build_report_card_pdf(agent_id, org_id='org-demo') -> bytes

Server-side PDF export of one agent's report card, written for a
NON-TECHNICAL stakeholder: who the agent is, what it is certified for,
where it is strong, and — deliberately IN the document, per the ATP
'failure transparency' principle — where it will break.

Data sources:
  * Seed catalog (atp/store.get_data()) — T0 public: agent profile,
    reportCard prose, skills, failure modes, cert metadata + seed awards.
  * Live cert awards for the agent from atp_cert_awards, org-scoped through
    atp/tenant_db.py ONLY (docs/TENANCY.md layer 2; org_id comes from the
    verified request state at the route). Live awards whose evidence was
    produced by the deterministic dry-run backend are marked DRY-RUN so a
    stub exam can never read like a real certification.

The PDF mirrors the Agent-view aesthetic (design/styles.css "university +
standards-body tone"): navy header band, gold rules, mono labels, layer
palette. reportlab only — built-in Helvetica/Courier faces, no external
assets. Rendering is pure (bytes out, no files written); tenant files are
NEVER involved and nothing is served from /videos or /media (TENANCY.md
leak surface #4).

Raises UnknownAgentError for an agent id that is not in the seed roster —
the API route maps it to 404.
"""

from __future__ import annotations

import io
import json
import threading
import time
from xml.sax.saxutils import escape as _xml_escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm  # noqa: F401  (kept: handy for tweaks)
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from atp import store, tenant_db

# ── Palette — mirrors design/styles.css (ATP / Agent view tokens) ───────────

NAVY = colors.HexColor("#0a0e22")        # --c-bg (header band)
NAVY_ELEV = colors.HexColor("#0f1733")   # --c-bg-elev
GOLD = colors.HexColor("#e8c268")        # --c-cert (on navy)
GOLD_PAPER = colors.HexColor("#a3801f")  # --c-cert, paper palette (rules)
INK = colors.HexColor("#1c2237")
INK_MUTED = colors.HexColor("#5d6688")
LINE = colors.HexColor("#c9cede")
PANEL = colors.HexColor("#f4f5f9")
CORAL = colors.HexColor("#c2403f")       # revoked / weak (paper-legible)
AMBER = colors.HexColor("#b45309")       # developing
GREEN = colors.HexColor("#2f7d4a")       # strong
GREY = colors.HexColor("#9ca3af")        # untested

#: layer palette (--c-atp-l1..l7), darkened where needed for white paper.
LAYER_COLORS = {
    1: colors.HexColor("#2f7fae"), 2: colors.HexColor("#1f8a63"),
    3: colors.HexColor("#b45309"), 4: colors.HexColor("#c2410c"),
    5: colors.HexColor("#c2403f"), 6: colors.HexColor("#7c5cbf"),
    7: GOLD_PAPER,
}

_STATUS_COLORS = {
    "strong": GREEN, "developing": AMBER, "weak": CORAL,
    "untested": GREY, "active": GREEN, "training": AMBER, "revoked": CORAL,
}

PAGE_W, PAGE_H = A4
MARGIN = 48
BAND_H = 92          # first-page navy header band
BAND_H_LATER = 24    # thin band on later pages
FOOTER_H = 78

_MONO, _MONO_B = "Courier", "Courier-Bold"
_SANS, _SANS_B, _SANS_I = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


class UnknownAgentError(ValueError):
    """agent_id is not in the seed roster (atp/seed.py AGENTS)."""


# ── DB readiness (same lazy idiom as api/atp.py) ────────────────────────────

_DB_READY = False
_DB_LOCK = threading.Lock()


def _ensure_db() -> None:
    global _DB_READY
    if _DB_READY:
        return
    with _DB_LOCK:
        if not _DB_READY:
            from atp import db
            db.run_migrations()
            _DB_READY = True


# ── Data assembly ───────────────────────────────────────────────────────────

def _find_agent(data: dict, agent_id: str) -> dict:
    for a in data.get("AGENTS", []):
        if a.get("id") == agent_id:
            return a
    raise UnknownAgentError(
        f"agent {agent_id!r} not found in the seed roster (atp/seed.py)")


def _seed_cert_rows(data: dict, agent_id: str) -> list[dict]:
    """Seed awards for the agent: one row per cert grant, oldest first."""
    rows = []
    for cert in data.get("CERTS", []):
        for award in cert.get("awards", []):
            if award.get("agentId") != agent_id:
                continue
            rows.append({
                "label": cert["label"],
                "domain": cert["domain"],
                "layer": cert["layer"],
                "score": award.get("score"),
                "ts": award.get("ts", ""),
                "revoked": award.get("status") == "revoked",
                "revokedTs": award.get("revokedTs"),
                "live": False,
                "dryRun": False,
            })
    rows.sort(key=lambda r: r["ts"])
    return rows


def _loads_maybe(v):
    if not isinstance(v, str):
        return v
    try:
        return json.loads(v)
    except (json.JSONDecodeError, ValueError):
        return v


def _live_cert_rows(data: dict, agent_id: str, org_id: str) -> list[dict]:
    """Live atp_cert_awards rows for the agent (org-scoped), oldest first.

    DRY-RUN detection: an award's evidence rows (written in the same exam
    run by atp/exams.py) record the candidate spec in their payload; if any
    resolves to the deterministic dry-run backend ('dryrun:*'), the award is
    marked so the table can never present a stub exam as a real one.
    """
    _ensure_db()
    awards = tenant_db.scoped_query(
        org_id,
        "SELECT id, ts, cert_id, score, evidence_ids FROM atp_cert_awards"
        " WHERE org_id = :org AND agent_id = :aid ORDER BY id ASC",
        {"org": org_id, "aid": agent_id})
    if not awards:
        return []

    ev_rows = tenant_db.scoped_query(
        org_id,
        "SELECT id, payload FROM atp_evidence"
        " WHERE org_id = :org AND agent_id = :aid",
        {"org": org_id, "aid": agent_id})
    candidate_by_id: dict[str, str] = {}
    for row in ev_rows:
        payload = _loads_maybe(row.get("payload"))
        if isinstance(payload, dict):
            candidate_by_id[str(row["id"])] = str(payload.get("candidate", ""))

    certs_by_id = {c["id"]: c for c in data.get("CERTS", [])}
    out = []
    for aw in awards:
        cert = certs_by_id.get(aw.get("cert_id"), {})
        evidence_ids = _loads_maybe(aw.get("evidence_ids")) or []
        dry = any(
            candidate_by_id.get(str(eid), "").startswith("dryrun")
            for eid in evidence_ids)
        out.append({
            "label": cert.get("label", aw.get("cert_id", "?")),
            "domain": cert.get("domain", "—"),
            "layer": cert.get("layer", "—"),
            "score": aw.get("score"),
            # Live award ts is a full ISO stamp; the table shows the date
            # (seed award dates are already date-only).
            "ts": str(aw.get("ts") or "")[:10],
            "revoked": False,
            "revokedTs": None,
            "live": True,
            "dryRun": dry,
        })
    return out


def _live_evidence_count(agent_id: str, org_id: str) -> int:
    _ensure_db()
    rows = tenant_db.scoped_query(
        org_id,
        "SELECT COUNT(*) AS n FROM atp_evidence"
        " WHERE org_id = :org AND agent_id = :aid",
        {"org": org_id, "aid": agent_id})
    return int(rows[0]["n"]) if rows else 0


def _citation(data: dict, agent: dict) -> str:
    """The citable sentence (STANDARD.sentence grammar); honest on revoke."""
    domain = (agent.get("domains") or ["—"])[0]
    if agent.get("status") == "revoked":
        return (f"{agent['name']} is NOT currently ATP-certified in {domain}: "
                f"its L{agent['level']} certification was revoked.")
    template = data.get("STANDARD", {}).get(
        "sentence", "{agent} is an ATP L{n}-certified agent in {domain}.")
    return (template.replace("{agent}", agent["name"])
                    .replace("{n}", str(agent["level"]))
                    .replace("{domain}", domain))


# ── Small flowables ─────────────────────────────────────────────────────────

class _MasteryBar(Flowable):
    """Simple filled-rect mastery bar (per the UI's mastery meters)."""

    def __init__(self, fraction: float, status: str,
                 width: float = 108, height: float = 7):
        super().__init__()
        self.fraction = max(0.0, min(1.0, float(fraction or 0.0)))
        self.fill = _STATUS_COLORS.get(status, GREY)
        self.width, self.height = width, height

    def wrap(self, availWidth, availHeight):  # noqa: N803 (reportlab API)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(PANEL)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        if self.fraction > 0:
            c.setFillColor(self.fill)
            c.rect(0, 0, self.width * self.fraction, self.height,
                   stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=0)


# ── Paragraph styles ────────────────────────────────────────────────────────

def _styles() -> dict[str, ParagraphStyle]:
    return {
        "h1": ParagraphStyle("h1", fontName=_SANS_B, fontSize=17,
                             leading=21, textColor=INK),
        "section": ParagraphStyle("section", fontName=_MONO_B, fontSize=9.5,
                                  leading=12, textColor=NAVY_ELEV,
                                  spaceBefore=6),
        "body": ParagraphStyle("body", fontName=_SANS, fontSize=9.5,
                               leading=13.5, textColor=INK),
        "bullet": ParagraphStyle("bullet", fontName=_SANS, fontSize=9.5,
                                 leading=13.5, textColor=INK,
                                 leftIndent=10, bulletIndent=2),
        "cell": ParagraphStyle("cell", fontName=_SANS, fontSize=8.5,
                               leading=11, textColor=INK),
        "cellMono": ParagraphStyle("cellMono", fontName=_MONO, fontSize=8,
                                   leading=10.5, textColor=INK),
        "labelMono": ParagraphStyle("labelMono", fontName=_MONO, fontSize=7,
                                    leading=9, textColor=INK_MUTED),
        "note": ParagraphStyle("note", fontName=_SANS_I, fontSize=8.5,
                               leading=11.5, textColor=INK_MUTED),
    }


def _esc(s) -> str:
    return _xml_escape(str(s if s is not None else "—"))


def _rule(color=GOLD_PAPER, thickness=1.1):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=1, spaceAfter=6)


def _section(title: str, story: list, st: dict) -> None:
    story.append(Spacer(1, 10))
    story.append(Paragraph(_esc(title.upper()), st["section"]))
    story.append(_rule())


# ── Page decoration (header band + footer, drawn on the canvas) ────────────

def _make_page_decorators(agent: dict, citation: str, n_evidence: int,
                          generated_at: str):
    agent_name = agent.get("name", agent["id"])
    deep_link = f"#/agent/{agent['id']}"

    def _footer(canv, doc):
        canv.saveState()
        y = FOOTER_H - 20
        canv.setStrokeColor(GOLD_PAPER)
        canv.setLineWidth(1)
        canv.line(MARGIN, y, PAGE_W - MARGIN, y)
        canv.setFont(_SANS_I, 8)
        canv.setFillColor(INK)
        canv.drawString(MARGIN, y - 11, f"“{citation}”")
        canv.setFont(_MONO, 6.8)
        canv.setFillColor(INK_MUTED)
        canv.drawString(
            MARGIN, y - 22,
            f"{deep_link} · generated {generated_at} · "
            f"evidence: {n_evidence} signed records — "
            f"verify at /atp/chain/verify")
        canv.setFont(_MONO, 7)
        canv.drawRightString(PAGE_W - MARGIN, y - 11,
                             f"PAGE {canv.getPageNumber()}")
        canv.restoreState()

    def first_page(canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY)
        canv.rect(0, PAGE_H - BAND_H, PAGE_W, BAND_H, stroke=0, fill=1)
        canv.setFillColor(GOLD)
        canv.setFont(_MONO_B, 8.5)
        canv.drawString(MARGIN, PAGE_H - 30,
                        "ATP — AGENTIC TRAINING PLATFORM")
        canv.setFont(_MONO, 7)
        canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 30,
                             "STANDARD ATP@2026.1")
        canv.setFillColor(colors.white)
        canv.setFont(_SANS_B, 19)
        canv.drawString(MARGIN, PAGE_H - 56, "Official Report Card")
        canv.setFillColor(colors.HexColor("#9aa3c0"))
        canv.setFont(_MONO, 7.5)
        canv.drawString(MARGIN, PAGE_H - 72,
                        "EVIDENCE-LINKED · REPRODUCIBLE · "
                        "FAILURE-TRANSPARENT · REVOCABLE")
        canv.setStrokeColor(GOLD)
        canv.setLineWidth(2)
        canv.line(0, PAGE_H - BAND_H, PAGE_W, PAGE_H - BAND_H)
        canv.restoreState()
        _footer(canv, doc)

    def later_pages(canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY)
        canv.rect(0, PAGE_H - BAND_H_LATER, PAGE_W, BAND_H_LATER,
                  stroke=0, fill=1)
        canv.setFillColor(GOLD)
        canv.setFont(_MONO_B, 7.5)
        canv.drawString(MARGIN, PAGE_H - 16,
                        f"ATP — OFFICIAL REPORT CARD · "
                        f"{agent_name.upper()}")
        canv.setStrokeColor(GOLD)
        canv.setLineWidth(1.2)
        canv.line(0, PAGE_H - BAND_H_LATER, PAGE_W, PAGE_H - BAND_H_LATER)
        canv.restoreState()
        _footer(canv, doc)

    return first_page, later_pages


# ── Story sections ──────────────────────────────────────────────────────────

def _identity_block(agent: dict, story: list, st: dict) -> None:
    status = agent.get("status", "—")
    status_color = _STATUS_COLORS.get(status, INK)
    story.append(Paragraph(_esc(agent.get("name", agent["id"])), st["h1"]))
    story.append(Spacer(1, 4))

    labels = ["AGENT ID", "BASE MODEL", "LEVEL", "CAREER STAGE", "TIER",
              "STATUS"]
    values = [
        Paragraph(_esc(agent["id"]), st["cellMono"]),
        Paragraph(_esc(agent.get("baseModel")), st["cell"]),
        Paragraph(
            f'<font name="{_MONO_B}" color="{LAYER_COLORS.get(agent.get("level"), INK).hexval()}">'
            f'L{_esc(agent.get("level"))}</font>', st["cell"]),
        Paragraph(_esc(agent.get("careerStage")), st["cell"]),
        Paragraph(_esc(agent.get("tier")), st["cell"]),
        Paragraph(
            f'<font name="{_SANS_B}" color="{status_color.hexval()}">'
            f'{_esc(status.upper())}</font>', st["cell"]),
    ]
    # AGENT ID gets the widest column so long slugs (gemma-physics-ocw)
    # never wrap mid-word in the mono face.
    w = PAGE_W - 2 * MARGIN
    col_w = [w * f for f in (0.21, 0.17, 0.10, 0.16, 0.15, 0.21)]
    table = Table(
        [[Paragraph(lbl, st["labelMono"]) for lbl in labels], values],
        colWidths=col_w)
    table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 1), (-1, 1), 0.5, LINE),
    ]))
    story.append(table)

    prov = agent.get("provenance") or {}
    if prov.get("origin") == "commissioned":
        corpora = ", ".join(prov.get("corpora") or []) or "—"
        req = prov.get("requestId") or "—"
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            f"PROVENANCE: COMMISSIONED (TRAIN-TO-ORDER) · "
            f"CORPORA: {_esc(corpora)} · REQUEST: {_esc(req)}",
            ParagraphStyle("prov", parent=st["cellMono"], fontSize=7.5,
                           textColor=GOLD_PAPER)))
        story.append(Paragraph(
            "This agent was trained to order for a specific corpus and "
            "certified through the identical exam blueprint as every "
            "pre-existing agent — there is no separate trust tier for "
            "commissioned experts.", st["note"]))

    if agent.get("status") == "revoked":
        story.append(Spacer(1, 7))
        warn = Table([[Paragraph(
            f'<font name="{_SANS_B}" color="{CORAL.hexval()}">'
            f'CERTIFICATION REVOKED.</font> '
            f'The ATP board has revoked this agent’s badge; the record '
            f'below stays public on purpose (the “revocable” '
            f'principle). See the certifications table and the failure '
            f'transparency section before relying on this agent for '
            f'anything.', st["cell"])]],
            colWidths=[PAGE_W - 2 * MARGIN])
        warn.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#faeceb")),
            ("BOX", (0, 0), (-1, -1), 0.8, CORAL),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(warn)


def _report_card_block(agent: dict, story: list, st: dict) -> None:
    rc = agent.get("reportCard") or {}
    _section("Report card — in plain language", story, st)
    if rc.get("summary"):
        story.append(Paragraph(_esc(rc["summary"]), st["body"]))
        story.append(Spacer(1, 6))
    if rc.get("strengths"):
        story.append(Paragraph("<b>Strengths</b>", st["body"]))
        for s in rc["strengths"]:
            story.append(Paragraph(_esc(s), st["bullet"],
                                   bulletText="–"))
        story.append(Spacer(1, 5))
    if rc.get("weaknesses"):
        story.append(Paragraph("<b>Weaknesses</b>", st["body"]))
        for w in rc["weaknesses"]:
            story.append(Paragraph(_esc(w), st["bullet"],
                                   bulletText="–"))
        story.append(Spacer(1, 5))
    if rc.get("recommendation"):
        rec = Table([[Paragraph(
            f"<b>Recommendation</b> — {_esc(rc['recommendation'])}",
            st["cell"])]], colWidths=[PAGE_W - 2 * MARGIN])
        rec.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PANEL),
            ("BOX", (0, 0), (-1, -1), 0.6, GOLD_PAPER),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(rec)


def _cert_table(rows: list[dict], story: list, st: dict) -> None:
    _section("Certifications", story, st)
    if not rows:
        story.append(Paragraph(
            "No certifications on record. This agent has not yet passed an "
            "ATP exam.", st["note"]))
        return

    header = ["CERTIFICATION", "DOMAIN", "LAYER", "SCORE", "DATE", "STATUS"]
    data = [[Paragraph(h, st["labelMono"]) for h in header]]
    styles = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ])
    header_lbl = ParagraphStyle("hdr", parent=st["labelMono"],
                                textColor=GOLD)
    data[0] = [Paragraph(h, header_lbl) for h in header]

    for i, r in enumerate(rows, start=1):
        layer_color = LAYER_COLORS.get(r["layer"], INK)
        if r["revoked"]:
            status_txt = (f'<font name="{_MONO_B}" color="{CORAL.hexval()}">'
                          f'REVOKED {_esc(r.get("revokedTs") or "")}</font>')
        elif r["live"] and r["dryRun"]:
            status_txt = (f'<font name="{_MONO_B}" '
                          f'color="{AMBER.hexval()}">LIVE · DRY-RUN'
                          f'</font>')
        elif r["live"]:
            status_txt = (f'<font name="{_MONO_B}" '
                          f'color="{GREEN.hexval()}">LIVE EXAM</font>')
        else:
            status_txt = (f'<font name="{_MONO}" '
                          f'color="{GREEN.hexval()}">granted</font>')
        score = r.get("score")
        data.append([
            Paragraph(_esc(r["label"]), st["cellMono"]),
            Paragraph(_esc(r["domain"]), st["cell"]),
            Paragraph(
                f'<font name="{_MONO_B}" color="{layer_color.hexval()}">'
                f'L{_esc(r["layer"])}</font>', st["cell"]),
            Paragraph("—" if score is None else f"{float(score):.2f}",
                      st["cellMono"]),
            Paragraph(_esc(r["ts"]), st["cellMono"]),
            Paragraph(status_txt, st["cellMono"]),
        ])
        if r["revoked"]:
            styles.add("BACKGROUND", (0, i), (-1, i),
                       colors.HexColor("#faeceb"))

    w = PAGE_W - 2 * MARGIN
    table = Table(data, colWidths=[w * 0.30, w * 0.17, w * 0.08, w * 0.10,
                                   w * 0.15, w * 0.20], repeatRows=1)
    table.setStyle(styles)
    story.append(table)
    if any(r["live"] and r["dryRun"] for r in rows):
        story.append(Spacer(1, 3))
        story.append(Paragraph(
            "DRY-RUN entries were produced by the deterministic CI stub "
            "backend, not a live model — they demonstrate the exam "
            "pipeline and are not real certifications.", st["note"]))


def _skills_table(agent: dict, story: list, st: dict) -> None:
    _section("Skills — measured mastery", story, st)
    skills = agent.get("skills") or []
    if not skills:
        story.append(Paragraph("No skills on record.", st["note"]))
        return
    header_lbl = ParagraphStyle("hdr2", parent=st["labelMono"],
                                textColor=GOLD)
    data = [[Paragraph(h, header_lbl)
             for h in ("SKILL", "LAYER", "MASTERY", "SCORE", "STATUS")]]
    for s in skills:
        status = s.get("status", "untested")
        color = _STATUS_COLORS.get(status, GREY)
        mastery = float(s.get("mastery") or 0.0)
        data.append([
            Paragraph(_esc(s.get("name")), st["cell"]),
            Paragraph(
                f'<font name="{_MONO}" '
                f'color="{LAYER_COLORS.get(s.get("layer"), INK).hexval()}">'
                f'L{_esc(s.get("layer"))}</font>', st["cell"]),
            _MasteryBar(mastery, status),
            Paragraph(f"{mastery:.2f}", st["cellMono"]),
            Paragraph(
                f'<font name="{_MONO}" color="{color.hexval()}">'
                f'{_esc(status)}</font>', st["cellMono"]),
        ])
    w = PAGE_W - 2 * MARGIN
    table = Table(data, colWidths=[w * 0.36, w * 0.09, w * 0.27, w * 0.10,
                                   w * 0.18], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(table)
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "“untested” means exactly that: the skill has not been "
        "measured yet. ATP shows uncertainty rather than hiding it.",
        st["note"]))


def _failure_table(agent: dict, story: list, st: dict) -> None:
    _section("Failure transparency — where this agent breaks", story, st)
    story.append(Paragraph(
        "The ATP standard publishes failure modes next to the passes. This "
        "section is part of the official record — a badge tells you not "
        "only what the agent can do, but concretely where it will fail.",
        st["note"]))
    story.append(Spacer(1, 4))
    failures = agent.get("failures") or []
    if not failures:
        story.append(Paragraph(
            "No failure modes recorded yet — usually a sign the agent "
            "is too new to have been stress-tested, not that it is perfect.",
            st["note"]))
        return
    header_lbl = ParagraphStyle("hdr3", parent=st["labelMono"],
                                textColor=GOLD)
    data = [[Paragraph(h, header_lbl)
             for h in ("FAILURE MODE", "RATE", "BOUNDARY — WHEN NOT TO "
                       "TRUST IT")]]
    for f in failures:
        rate = float(f.get("rate") or 0.0)
        data.append([
            Paragraph(f"<b>{_esc(f.get('mode'))}</b>", st["cell"]),
            Paragraph(
                f'<font name="{_MONO_B}" color="{CORAL.hexval()}">'
                f'{rate:.0%}</font>', st["cellMono"]),
            Paragraph(_esc(f.get("boundary")), st["cell"]),
        ])
    w = PAGE_W - 2 * MARGIN
    table = Table(data, colWidths=[w * 0.27, w * 0.09, w * 0.64],
                  repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)


# ── Public builder ──────────────────────────────────────────────────────────

def build_report_card_pdf(agent_id: str,
                          org_id: str = tenant_db.DEFAULT_ORG) -> bytes:
    """Render the official report-card PDF for `agent_id` → PDF bytes.

    Seed profile + prose from atp/store.get_data(); live awards/evidence for
    the caller's org via atp/tenant_db.py. Raises UnknownAgentError when the
    agent is not in the seed roster.
    """
    data = store.get_data()
    agent = _find_agent(data, agent_id)

    cert_rows = _seed_cert_rows(data, agent_id)
    cert_rows += _live_cert_rows(data, agent_id, org_id)

    seed_evidence = sum(
        1 for e in data.get("EVIDENCE", []) if e.get("agentId") == agent_id)
    n_evidence = seed_evidence + _live_evidence_count(agent_id, org_id)

    generated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    citation = _citation(data, agent)
    st = _styles()

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=BAND_H + 22, bottomMargin=FOOTER_H,
        title=f"ATP Official Report Card — {agent.get('name', agent_id)}",
        author="ATP — Agentic Training Platform")

    story: list = []
    _identity_block(agent, story, st)
    _report_card_block(agent, story, st)
    _cert_table(cert_rows, story, st)
    _skills_table(agent, story, st)
    _failure_table(agent, story, st)

    first_page, later_pages = _make_page_decorators(
        agent, citation, n_evidence, generated_at)
    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    return buf.getvalue()


# ── CLI (dev convenience) ───────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Render an agent's official report-card PDF (Phase 6).")
    parser.add_argument("agent_id", help="e.g. atlas-ops")
    parser.add_argument("out", help="output .pdf path")
    parser.add_argument("--org", default=tenant_db.DEFAULT_ORG)
    args = parser.parse_args()

    pdf = build_report_card_pdf(args.agent_id, org_id=args.org)
    with open(args.out, "wb") as fh:
        fh.write(pdf)
    print(f"wrote {len(pdf)} bytes to {args.out}")
