"""
Company-knowledge ingestion + L5 exam drafting — Phase 6 (docs/HARDENING.md).

Pipeline (first-customer UX contract):

    upload (md/txt/pdf) ──> vault_docs row              [T2: content encrypted]
                     │
                     └──> generate_l5_draft()           [deterministic heuristic
                          blueprint + >=8 items          — NO LLM dependency]
                     │
    SME sign-off ────┴──> approve_draft()               ['sme_signoff' evidence
                          │                              on the signed chain]
                          └──> load_org_item_bank()     [in-memory bank consumed
                               by atp/exams.py           via its Phase 6 loader
                               ORG_CERT_PREFIX path]     -> run_exam -> award

Tenancy & data class (docs/TENANCY.md — T2 "crown jewels"):

  * Every row is org-scoped; all SQL here goes through atp/tenant_db.py
    scoped helpers and carries a `:org` bind by construction (`_scoped()`
    below asserts it). vault_docs / l5_drafts are not (yet) listed in
    tenant_db.TENANT_TABLES — that registry lives in a file owned by the
    tenancy workstream — so the DAL's parse guard does not fire for them;
    the local assert plus Postgres FORCE RLS (migration 007) close the gap.
  * Document content, summaries, and draft ITEMS are encrypted at rest via
    atp/crypto.py encrypt_for_org (per-org HKDF subkey, 'enc1:' envelope).
    The draft BLUEPRINT (section names/weights only) stays plaintext so
    listings render without a decrypt.
  * Approved banks are materialized IN MEMORY only. They are NEVER written
    to atp/items/ or any shared directory (leak surfaces #4 and #7: no
    plaintext T2 on disk, nothing under public media prefixes).

Separation of duties: admins manage docs and drafts; only SMEs sign.
approve_draft / reject_draft record the reviewer decision as a signed
'sme_signoff' evidence row (atp/signing.py append_chain), making sign-off
tamper-evident even though l5_drafts itself is mutable by design.

Public:
  ingest_doc(org_id, filename, mime, content_bytes, uploaded_by) -> doc dict
  list_docs(org_id)                          -> [doc dict]  (summaries only)
  get_doc(org_id, doc_id)                    -> doc dict | None (full text)
  generate_l5_draft(org_id, doc_ids, created_by, title='') -> draft dict
  list_drafts(org_id, include_items=False)   -> [draft dict]
  get_draft(org_id, draft_id, include_items=False) -> draft dict | None
  approve_draft(org_id, draft_id, reviewer, note='') -> sign-off dict
  reject_draft(org_id, draft_id, reviewer, note='')  -> sign-off dict
  load_org_item_bank(org_id, cert_ref)       -> {cert, items} | None
  UnsupportedDocumentError / KnowledgeError / DraftStateError
"""

from __future__ import annotations

import io
import json
import re
import threading
import time
import uuid
from pathlib import Path

from atp import crypto, db, signing, tenant_db

#: Cert refs for approved drafts: f"{EXAM_CERT_PREFIX}{draft_id}". Must equal
#: atp/exams.py ORG_CERT_PREFIX (defined there — the loader checks the prefix
#: BEFORE importing this module; asserted equal in load_org_item_bank).
EXAM_CERT_PREFIX = "org-l5-draft:"

#: Seed cert whose passCriteria/rubric an org draft inherits — the L5
#: company-knowledge archetype in atp/seed.py.
L5_TEMPLATE_CERT_ID = "atp-l5-company-ops"

SUMMARY_WORDS = 40      # heuristic summary length (first N words)
MIN_ITEMS = 8           # a draft bank must have at least this many items
MIN_SECTIONS = 2        # ... spread across at least this many sections
MAX_UNITS_PER_DOC = 8   # cap: at most this many (heading, passage) units/doc
MIN_UNIT_CHARS = 40     # passages shorter than this are too thin to examine
MAX_EXPECTED_CHARS = 1200  # cap pasted passage length in judge references

_MIGRATED = False
_MIGRATE_LOCK = threading.Lock()

# (org_id, draft_id) -> materialized bank dict. In-memory ONLY (T2: approved
# banks never land as plaintext on shared disk); repopulated lazily from the
# encrypted l5_drafts row after a restart. Entries are only ever created for
# status='approved' drafts, and approve/reject are terminal transitions, so
# no invalidation is needed.
_BANK_CACHE: dict[tuple[str, str], dict] = {}
_BANK_LOCK = threading.Lock()


class KnowledgeError(ValueError):
    """Invalid ingestion/drafting input (unknown doc ids, corpus too thin)."""


class UnsupportedDocumentError(KnowledgeError):
    """Unsupported document type — the API maps this to HTTP 415."""


class DraftStateError(RuntimeError):
    """A draft transition was attempted from the wrong status (HTTP 409)."""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _ensure_db() -> None:
    """Idempotently apply migrations so a fresh SQLite file just works
    (same idiom as atp/exams.py)."""
    global _MIGRATED
    if _MIGRATED:
        return
    with _MIGRATE_LOCK:
        if not _MIGRATED:
            db.run_migrations()
            _MIGRATED = True


def _scoped(sql: str) -> str:
    """Belt-and-braces layer-2 check for THIS module's tenant tables.

    vault_docs / l5_drafts are not in tenant_db.TENANT_TABLES (that frozenset
    lives in atp/tenant_db.py, owned by the tenancy workstream — follow-up:
    add both there), so scoped_query/scoped_execute would not force the
    ':org' bind for them. Assert it locally instead; on Postgres the
    migration-007 FORCE RLS policies are the deny-by-default backstop.
    """
    if ":org" not in sql:
        raise tenant_db.TenantScopeError(
            f"knowledge-module statement lacks an ':org' bind: {sql!r}")
    return sql


# ── Text extraction (md/txt native; pdf via pypdf when importable) ──────────

_EXT_KIND = {".md": "md", ".markdown": "md", ".txt": "txt", ".pdf": "pdf"}
_MIME_KIND = {
    "text/markdown": "md",
    "text/x-markdown": "md",
    "text/plain": "txt",
    "application/pdf": "pdf",
}


def doc_kind(filename: str | None, mime: str | None) -> str | None:
    """'md' | 'txt' | 'pdf' from the filename extension (authoritative),
    falling back to the declared MIME type; None when neither is allowed."""
    ext = Path(filename or "").suffix.lower()
    if ext in _EXT_KIND:
        return _EXT_KIND[ext]
    if ext:  # an extension we do NOT allow — don't let MIME override it
        return None
    return _MIME_KIND.get((mime or "").split(";")[0].strip().lower())


def _extract_text(filename: str | None, mime: str | None,
                  content_bytes: bytes) -> str:
    kind = doc_kind(filename, mime)
    if kind is None:
        raise UnsupportedDocumentError(
            f"unsupported document type (filename={filename!r}, "
            f"mime={mime!r}) — allowed: .md, .txt, .pdf")
    if kind == "pdf":
        try:
            from pypdf import PdfReader  # optional dep (requirements.txt)
        except ImportError:
            raise UnsupportedDocumentError(
                "PDF ingestion requires the 'pypdf' package, which is not "
                "installed on this deployment — upload .md or .txt instead"
            ) from None
        try:
            reader = PdfReader(io.BytesIO(content_bytes))
            text = "\n\n".join((page.extract_text() or "")
                               for page in reader.pages)
        except Exception as e:  # noqa: BLE001 — pypdf raises many types
            raise KnowledgeError(f"could not parse PDF: {e}") from None
    else:
        text = content_bytes.decode("utf-8", errors="replace")
    text = text.strip()
    if not text:
        raise KnowledgeError("document contains no extractable text")
    return text


_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(?P<h>.+?)\s*#*\s*$")


def _title_from(text: str, filename: str | None) -> str:
    """First markdown heading, else the cleaned filename stem."""
    for line in text.splitlines()[:20]:
        m = _HEADING_RE.match(line)
        if m:
            return m.group("h").strip()
    stem = Path(filename or "document").stem
    return re.sub(r"[_\-]+", " ", stem).strip() or "document"


def _summarize(text: str) -> str:
    """Deterministic heuristic summary: the first SUMMARY_WORDS words of the
    body (heading markers stripped)."""
    words = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.MULTILINE).split()
    out = " ".join(words[:SUMMARY_WORDS])
    return out + (" …" if len(words) > SUMMARY_WORDS else "")


def _split_units(text: str) -> list[tuple[str, str]]:
    """Split a document into (heading, passage) units, deterministically.

    Blocks are separated by blank lines; a block that is a single markdown
    heading line sets the current heading for the passages that follow.
    Headingless documents fall back to positional labels ('passage N').
    Passages shorter than MIN_UNIT_CHARS are skipped as unexaminable.
    """
    units: list[tuple[str, str]] = []
    heading: str | None = None
    n_anon = 0
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        m = _HEADING_RE.match(lines[0])
        if m:
            heading = m.group("h").strip()[:80]
            block = "\n".join(lines[1:]).strip()
            if not block:
                continue
        if len(block) < MIN_UNIT_CHARS:
            continue
        if heading is None:
            n_anon += 1
            label = f"passage {n_anon}"
        else:
            label = heading
        units.append((label, block))
    return units


# ── Documents ────────────────────────────────────────────────────────────────

_DOC_LIST_COLS = "id, title, filename, mime, uploaded_by, created_at, status"


def _doc_public(row: dict, org_id: str, *, content: bool = False) -> dict:
    out = {
        "id":         row["id"],
        "title":      row["title"],
        "filename":   row.get("filename"),
        "mime":       row.get("mime"),
        "status":     row["status"],
        "uploadedBy": row.get("uploaded_by"),
        "createdAt":  row.get("created_at"),
        "summary":    crypto.decrypt_text_for_org(org_id, row.get("summary_enc")),
    }
    if content:
        out["content"] = crypto.decrypt_text_for_org(org_id, row.get("content_enc"))
    return out


def ingest_doc(org_id: str, filename: str | None, mime: str | None,
               content_bytes: bytes, uploaded_by: str) -> dict:
    """Extract text, encrypt it under the org's subkey, store a vault_docs
    row, and return the public doc dict (summary decrypted for the caller).

    Raises UnsupportedDocumentError (bad type / pypdf missing → HTTP 415),
    KnowledgeError (unparseable/empty → 400), RuntimeError from atp/crypto.py
    when DATA_ENCRYPTION_KEY is unset (T2 is never written as plaintext).
    """
    _ensure_db()
    text = _extract_text(filename, mime, content_bytes)
    doc_id = "doc_" + uuid.uuid4().hex[:12]
    row = {
        "id": doc_id,
        "title": _title_from(text, filename),
        "filename": filename,
        "mime": mime,
        "content_enc": crypto.encrypt_for_org(org_id, text),
        "summary_enc": crypto.encrypt_for_org(org_id, _summarize(text)),
        "uploaded_by": uploaded_by,
        "created_at": _now(),
        "status": "uploaded",
    }
    tenant_db.scoped_execute(org_id, _scoped(
        "INSERT INTO vault_docs (id, org_id, title, filename, mime, "
        "  content_enc, summary_enc, uploaded_by, created_at, status) "
        "VALUES (:id, :org, :title, :filename, :mime, :content_enc, "
        "  :summary_enc, :uploaded_by, :created_at, :status)"),
        {"org": org_id, **row})
    return _doc_public({**row}, org_id)


def list_docs(org_id: str) -> list[dict]:
    """Org's vault docs, latest first — summaries decrypted, NO content."""
    _ensure_db()
    rows = tenant_db.scoped_query(org_id, _scoped(
        f"SELECT {_DOC_LIST_COLS}, summary_enc FROM vault_docs "
        f"WHERE org_id = :org ORDER BY created_at DESC, id DESC"),
        {"org": org_id})
    return [_doc_public(r, org_id) for r in rows]


def _doc_row(org_id: str, doc_id: str) -> dict | None:
    rows = tenant_db.scoped_query(org_id, _scoped(
        "SELECT * FROM vault_docs WHERE org_id = :org AND id = :id LIMIT 1"),
        {"org": org_id, "id": doc_id})
    return rows[0] if rows else None


def get_doc(org_id: str, doc_id: str) -> dict | None:
    """One doc with the FULL decrypted text, or None (cross-tenant ids are
    indistinguishable from unknown ones — TENANCY.md leak surface #6)."""
    _ensure_db()
    row = _doc_row(org_id, doc_id)
    return None if row is None else _doc_public(row, org_id, content=True)


# ── L5 draft generation (deterministic heuristic — no LLM dependency) ───────

def _items_for_doc(doc_idx: int, title: str, units: list[tuple[str, str]]
                   ) -> list[dict]:
    """Recall + apply item pair per (heading, passage) unit. Pure function of
    its inputs — same docs in the same order always produce the same items."""
    items: list[dict] = []
    for u_idx, (heading, passage) in enumerate(units[:MAX_UNITS_PER_DOC], 1):
        passage = passage[:MAX_EXPECTED_CHARS]
        base = f"l5d-{doc_idx:02d}-{u_idx:02d}"
        items.append({
            "id": f"{base}-r",
            "section": title,
            "type": "recall",
            "prompt": (f'According to "{title}", what is stated about '
                       f'"{heading}"?'),
            "expected": (f'Full credit requires accurately restating the '
                         f'substance of this passage from "{title}" '
                         f'(section: {heading}); contradicting it or '
                         f'inventing unstated policy is wrong:\n{passage}'),
            "points": 2,
        })
        items.append({
            "id": f"{base}-a",
            "section": title,
            "type": "apply",
            "prompt": (f'A teammate must follow the guidance in "{title}" '
                       f'regarding "{heading}". Explain, step by step, how '
                       f'to apply what the document states, and note when '
                       f'to escalate instead of guessing.'),
            "expected": (f'Full credit requires steps grounded ONLY in this '
                         f'passage from "{title}" (section: {heading}) — no '
                         f'invented policy; ambiguous cases must escalate:\n'
                         f'{passage}'),
            "points": 3,
        })
    return items


def _draft_public(row: dict, org_id: str, *, include_items: bool) -> dict:
    blueprint = json.loads(row["blueprint_json"])
    out = {
        "id":         row["id"],
        "certLabel":  row["cert_label"],
        "blueprint":  blueprint,
        "docIds":     json.loads(row["doc_ids_json"]),
        "status":     row["status"],
        "createdBy":  row.get("created_by"),
        "createdAt":  row.get("created_at"),
        "reviewedBy": row.get("reviewed_by"),
        "reviewedAt": row.get("reviewed_at"),
        "reviewNote": row.get("review_note"),
        "itemCount":  sum(int(s.get("items", 0))
                          for s in blueprint.get("sections", [])),
        "examCertRef": EXAM_CERT_PREFIX + row["id"],
    }
    if include_items:
        out["items"] = json.loads(
            crypto.decrypt_text_for_org(org_id, row["items_json_enc"]))
    return out


def generate_l5_draft(org_id: str, doc_ids: list[str], created_by: str,
                      title: str = "") -> dict:
    """Deterministic heuristic L5 exam draft from the org's vault docs.

    Blueprint sections = the docs' titles (one section per doc, weights
    proportional to item count, normalized to sum 1). Items = a recall +
    apply pair per (heading, passage) unit of each doc. Requires >= 2 docs
    with distinct titles and >= 8 items total, else KnowledgeError.

    Blueprint is stored plaintext; ITEMS (T2 — verbatim company passages)
    are encrypted under the org subkey. Returns the draft dict with items
    DECRYPTED for immediate SME review (the route role-gates that).
    """
    _ensure_db()
    if not doc_ids:
        raise KnowledgeError("docIds must be a non-empty list")
    if len(set(doc_ids)) != len(doc_ids):
        raise KnowledgeError("docIds contains duplicates")

    docs: list[dict] = []
    missing: list[str] = []
    for doc_id in doc_ids:
        row = _doc_row(org_id, doc_id)
        if row is None:
            missing.append(doc_id)
        else:
            docs.append(row)
    if missing:
        # Cross-tenant ids fail EXACTLY like unknown ones (TENANCY.md #6);
        # only ids the caller itself supplied are echoed back.
        raise KnowledgeError(f"unknown doc id(s): {sorted(missing)}")

    items: list[dict] = []
    sections: list[dict] = []
    seen_titles: set[str] = set()
    for d_idx, row in enumerate(docs, 1):
        title_d = row["title"]
        if title_d in seen_titles:
            raise KnowledgeError(
                f"two selected docs share the title {title_d!r} — blueprint "
                f"sections are doc titles and must be distinct")
        seen_titles.add(title_d)
        text = crypto.decrypt_text_for_org(org_id, row["content_enc"])
        units = _split_units(text)
        doc_items = _items_for_doc(d_idx, title_d, units)
        if not doc_items:
            raise KnowledgeError(
                f"doc {row['id']} ({title_d!r}) yields no examinable "
                f"passages (needs paragraphs of >= {MIN_UNIT_CHARS} chars)")
        items.extend(doc_items)
        sections.append({"name": title_d, "items": len(doc_items),
                         "itemTypes": ["recall", "apply"]})

    if len(sections) < MIN_SECTIONS:
        raise KnowledgeError(
            f"an L5 draft needs >= {MIN_SECTIONS} blueprint sections "
            f"(= distinct docs); got {len(sections)}")
    if len(items) < MIN_ITEMS:
        raise KnowledgeError(
            f"an L5 draft needs >= {MIN_ITEMS} items; these docs only "
            f"yield {len(items)} — upload richer documents")

    # Weights proportional to item count, normalized to sum exactly 1
    # (the last section absorbs the rounding remainder).
    total = len(items)
    for s in sections[:-1]:
        s["weight"] = round(s["items"] / total, 6)
    sections[-1]["weight"] = round(1.0 - sum(s["weight"]
                                             for s in sections[:-1]), 6)

    draft_id = "l5d_" + uuid.uuid4().hex[:12]
    blueprint = {"sections": sections, "totalItems": total}
    row = {
        "id": draft_id,
        "cert_label": (title or "").strip() or "ATP-L5 Company Knowledge (draft)",
        "blueprint_json": json.dumps(blueprint, sort_keys=True),
        "items_json_enc": crypto.encrypt_for_org(org_id, json.dumps(items)),
        "doc_ids_json": json.dumps(list(doc_ids)),
        "status": "draft",
        "created_by": created_by,
        "created_at": _now(),
    }
    tenant_db.scoped_execute(org_id, _scoped(
        "INSERT INTO l5_drafts (id, org_id, cert_label, blueprint_json, "
        "  items_json_enc, doc_ids_json, status, created_by, created_at) "
        "VALUES (:id, :org, :cert_label, :blueprint_json, :items_json_enc, "
        "  :doc_ids_json, :status, :created_by, :created_at)"),
        {"org": org_id, **row})

    # uploaded -> drafted (docs already 'drafted'/'signed' keep their status).
    for doc_id in doc_ids:
        tenant_db.scoped_execute(org_id, _scoped(
            "UPDATE vault_docs SET status = 'drafted' "
            "WHERE org_id = :org AND id = :id AND status = 'uploaded'"),
            {"org": org_id, "id": doc_id})

    return _draft_public(row, org_id, include_items=True)


def list_drafts(org_id: str, include_items: bool = False) -> list[dict]:
    """Org's L5 drafts, latest first. Items (T2) only when include_items —
    the route restricts that to admin|sme."""
    _ensure_db()
    rows = tenant_db.scoped_query(org_id, _scoped(
        "SELECT * FROM l5_drafts WHERE org_id = :org "
        "ORDER BY created_at DESC, id DESC"),
        {"org": org_id})
    return [_draft_public(r, org_id, include_items=include_items) for r in rows]


def _draft_row(org_id: str, draft_id: str) -> dict | None:
    rows = tenant_db.scoped_query(org_id, _scoped(
        "SELECT * FROM l5_drafts WHERE org_id = :org AND id = :id LIMIT 1"),
        {"org": org_id, "id": draft_id})
    return rows[0] if rows else None


def get_draft(org_id: str, draft_id: str,
              include_items: bool = False) -> dict | None:
    _ensure_db()
    row = _draft_row(org_id, draft_id)
    return None if row is None else _draft_public(
        row, org_id, include_items=include_items)


# ── SME sign-off (separation of duties; evidence on the signed chain) ───────

def _review(org_id: str, draft_id: str, reviewer: str, note: str,
            to_status: str, outcome: str) -> dict | None:
    """Shared approve/reject transition: guarded UPDATE from 'draft', then a
    signed 'sme_signoff' evidence row. Returns None for unknown/cross-org
    ids; DraftStateError when the draft is not in status 'draft'."""
    _ensure_db()
    row = _draft_row(org_id, draft_id)
    if row is None:
        return None
    if row["status"] != "draft":
        raise DraftStateError(
            f"draft {draft_id} is '{row['status']}' — only status 'draft' "
            f"can be {outcome}")
    ts = _now()
    res = tenant_db.scoped_execute(org_id, _scoped(
        "UPDATE l5_drafts SET status = :to, reviewed_by = :rev, "
        "  reviewed_at = :ts, review_note = :note "
        "WHERE org_id = :org AND id = :id AND status = 'draft'"),
        {"org": org_id, "id": draft_id, "to": to_status,
         "rev": reviewer, "ts": ts, "note": note})
    if res.rowcount == 0:  # lost a race — same answer as the pre-check
        raise DraftStateError(
            f"draft {draft_id} was reviewed concurrently — reload it")

    cert_ref = EXAM_CERT_PREFIX + draft_id
    doc_ids = json.loads(row["doc_ids_json"])
    # The sign-off itself is the tamper-evident record (l5_drafts is mutable
    # by design — migration 007 header): one HMAC-signed row on the org's
    # evidence chain. NOTE: payload carries reviewer/note/doc ids — metadata,
    # never document content or items (atp_evidence is not encrypted).
    payload = {"draftId": draft_id, "reviewer": reviewer, "note": note,
               "docIds": doc_ids, "certLabel": row["cert_label"],
               "outcome": outcome}
    (evidence_id, _sig), = signing.append_chain(org_id, [{
        "ts": ts, "agent_id": reviewer, "cert_id": cert_ref,
        "kind": "sme_signoff", "payload": payload,
    }])

    if to_status == "approved":
        for doc_id in doc_ids:  # drafted -> signed
            tenant_db.scoped_execute(org_id, _scoped(
                "UPDATE vault_docs SET status = 'signed' "
                "WHERE org_id = :org AND id = :id"),
                {"org": org_id, "id": doc_id})
        # Materialize the bank in memory now (also happens lazily on demand).
        load_org_item_bank(org_id, cert_ref)

    return {
        "draftId": draft_id,
        "status": to_status,
        "outcome": outcome,
        "reviewedBy": reviewer,
        "reviewedAt": ts,
        "note": note,
        "evidenceId": evidence_id,
        "examCertRef": cert_ref,
        "examRunnable": to_status == "approved",
    }


def approve_draft(org_id: str, draft_id: str, reviewer: str,
                  note: str = "") -> dict | None:
    """SME approval: draft -> approved, 'sme_signoff' evidence appended,
    covered docs flip to 'signed', and the exam bank becomes loadable via
    load_org_item_bank (cert ref in the returned 'examCertRef')."""
    return _review(org_id, draft_id, reviewer, note, "approved", "approved")


def reject_draft(org_id: str, draft_id: str, reviewer: str,
                 note: str = "") -> dict | None:
    """SME rejection: draft -> rejected, with the SAME evidence trail
    (kind 'sme_signoff', payload.outcome = 'rejected')."""
    return _review(org_id, draft_id, reviewer, note, "rejected", "rejected")


# ── Exam extension point (consumed by atp/exams.py's Phase 6 loader path) ───

def _template_cert() -> dict:
    """passCriteria/rubric archetype for org L5 drafts, deep-copied from the
    seed L5 cert so the T0 seed is never mutated."""
    from atp import store
    for cert in store.get_data().get("CERTS", []):
        if cert.get("id") == L5_TEMPLATE_CERT_ID:
            return json.loads(json.dumps(cert))  # cheap deep copy
    # Defensive fallback — the seed always ships this cert.
    return {"passCriteria": {"overall": 0.9, "perSection": 0.85, "runs": 2,
                             "temperature": 0, "seed": 5051,
                             "judgeSeparation": True},
            "rubric": []}


def load_org_item_bank(org_id: str, cert_ref: str) -> dict | None:
    """Materialize an org's APPROVED draft bank in memory for atp/exams.py.

    cert_ref: f"{EXAM_CERT_PREFIX}<draft_id>". Returns
        {"cert": <synthetic cert dict>, "items": [item, ...]}
    or None when the ref does not name an approved draft of THIS org (a
    cross-tenant ref is indistinguishable from an unknown one — #6).

    The synthetic cert carries the draft's own blueprint (sections = doc
    titles) plus the passCriteria/rubric of the seed L5 template cert, so
    run_exam()'s aggregation and verdict logic work unchanged. Decrypted
    items live only in this process's memory (_BANK_CACHE) — never on disk.
    """
    if not cert_ref.startswith(EXAM_CERT_PREFIX):
        return None
    draft_id = cert_ref[len(EXAM_CERT_PREFIX):]
    key = (org_id, draft_id)
    with _BANK_LOCK:
        cached = _BANK_CACHE.get(key)
    if cached is not None:
        return cached

    _ensure_db()
    row = _draft_row(org_id, draft_id)
    if row is None or row["status"] != "approved":
        return None
    items = json.loads(crypto.decrypt_text_for_org(org_id, row["items_json_enc"]))
    template = _template_cert()
    cert = {
        "id": cert_ref,
        "label": row["cert_label"],
        "sentence": (f"Org-scoped L5 company-knowledge draft "
                     f"({row['cert_label']}), SME-approved."),
        "layer": 5,
        "domain": "Company Knowledge",
        "blueprint": json.loads(row["blueprint_json"]),
        "rubric": template.get("rubric", []),
        "passCriteria": template.get("passCriteria", {}),
        "smeSignoff": [{"name": row.get("reviewed_by"),
                        "ts": row.get("reviewed_at")}],
    }
    bank = {"cert": cert, "items": items, "draftId": draft_id}
    with _BANK_LOCK:
        _BANK_CACHE[key] = bank
    return bank
