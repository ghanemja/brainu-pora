"""
Company-knowledge API routes — Phase 6 (docs/HARDENING.md first-customer UX).

Mounted by api/server.py:
    from api.knowledge import router as knowledge_router
    app.include_router(knowledge_router)

Endpoints (bearer-gated by the default auth middleware — api/auth.py):
    POST /knowledge/docs                — multipart upload (md/txt/pdf,
                                          <= 5 MB) → doc dict   [admin|sme]
    GET  /knowledge/docs                — org's docs, summaries only [any role]
    GET  /knowledge/docs/{id}           — full decrypted text    [admin|sme]
    POST /knowledge/drafts              — {docIds, title} → generated L5
                                          draft (blueprint + decrypted items
                                          for review)            [admin|sme]
    GET  /knowledge/drafts              — org's drafts [any role; items (T2)
                                          included only for admin|sme]
    POST /knowledge/drafts/{id}/approve — {note} → sign-off dict [sme ONLY]
    POST /knowledge/drafts/{id}/reject  — {note} → sign-off dict [sme ONLY]
    POST /knowledge/drafts/{id}/exam    — {candidateSpec?, agentId?,
                                          dryRun=true} → {jobId}; job-backed
                                          like /atp/exams/run    [admin|sme]

Tenancy (docs/TENANCY.md — this is T2 "crown jewels" data):
  * org_id comes ONLY from verified request state (request.state.org_id, set
    by the auth middleware from the JWT) — never from body/query. All storage
    is org-scoped + encrypted at rest in atp/knowledge.py.
  * Uploads are stored as encrypted DB columns ONLY — no file ever lands on
    disk, and in particular never under the public /videos or /media
    prefixes (leak surface #4).
  * Cross-tenant/unknown ids → the same 404 (no existence oracle, #6).

Separation of duties: admins (or SMEs) manage docs and generate drafts, but
ONLY role 'sme' can approve/reject — an admin must not be able to sign off
the exam content they themselves assembled. The BU_AUTH_DISABLED=1 dev
bypass (which runs every request as org-demo with role 'admin') is exempted
from that one gate so the demo flow keeps working end-to-end; with auth
enabled there is no exemption.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from pydantic import BaseModel

from api.auth import require_role
from atp import knowledge

router = APIRouter(prefix="/knowledge")

#: Upload size cap (bytes) — Phase 6 contract: 5 MB.
MAX_UPLOAD_BYTES = 5 * 1024 * 1024


# ── Helpers ──────────────────────────────────────────────────────────────────

def _org(request: Request) -> str:
    """Org for this request — ONLY from verified auth state (TENANCY.md §4
    layer 1). 'org-demo' when auth is disabled / legacy single-admin token."""
    return getattr(request.state, "org_id", None) or "org-demo"


def _user(request: Request) -> str:
    return getattr(request.state, "user", None) or "anon"


def require_sme(request: Request) -> str:
    """Sign-off gate: role 'sme' ONLY (separation of duties — admins manage,
    SMEs sign). Dev exception: the BU_AUTH_DISABLED=1 bypass carries role
    'admin' for every request (api/auth.py), so it is allowed through here —
    otherwise the demo could never exercise approval. With auth enabled the
    gate is strict."""
    role = getattr(request.state, "role", None)
    if role is None:
        raise HTTPException(
            status_code=401, detail="authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    from api import auth as _auth
    if role != "sme" and not _auth.AUTH_DISABLED:
        raise HTTPException(
            403, "draft sign-off requires role 'sme' (separation of duties: "
                 "admins manage documents and drafts; SMEs sign)")
    return role


def _http_errors(fn, *args, **kwargs):
    """Run a knowledge-module call, translating its typed errors to HTTP.

    UnsupportedDocumentError → 415, KnowledgeError → 400, DraftStateError →
    409. The fail-loud missing-DATA_ENCRYPTION_KEY RuntimeError from
    atp/crypto.py becomes a 503 with an actionable message (T2 content is
    NEVER written or served as plaintext instead)."""
    try:
        return fn(*args, **kwargs)
    except knowledge.UnsupportedDocumentError as e:
        raise HTTPException(415, str(e)) from None
    except knowledge.KnowledgeError as e:
        raise HTTPException(400, str(e)) from None
    except knowledge.DraftStateError as e:
        raise HTTPException(409, str(e)) from None
    except RuntimeError as e:
        if "DATA_ENCRYPTION_KEY" in str(e):
            raise HTTPException(
                503, "DATA_ENCRYPTION_KEY is not configured on this "
                     "deployment — company-knowledge content is T2 and is "
                     "only ever stored/served encrypted (docs/TENANCY.md)",
            ) from None
        raise


# ── Documents ────────────────────────────────────────────────────────────────

@router.post("/docs", dependencies=[Depends(require_role("admin", "sme"))])
async def upload_doc(request: Request, file: UploadFile = File(...)):
    """Upload one company document (md/txt/pdf, <= 5 MB) into the org vault.

    Content is encrypted under the org's subkey before it touches the DB; the
    response returns metadata + the heuristic summary, not the full text.
    """
    if knowledge.doc_kind(file.filename, file.content_type) is None:
        raise HTTPException(
            415, f"unsupported document type (filename={file.filename!r}, "
                 f"content-type={file.content_type!r}) — allowed: .md, .txt, "
                 f".pdf")
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            413, f"file exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB "
                 f"upload cap")
    if not data:
        raise HTTPException(400, "empty upload")
    return _http_errors(
        knowledge.ingest_doc, _org(request), file.filename,
        file.content_type, data, uploaded_by=_user(request))


@router.get("/docs", dependencies=[Depends(require_role())])
def get_docs(request: Request):
    """Org's vault docs, latest first — decrypted SUMMARIES only (any
    authenticated role; full text stays behind the admin|sme route)."""
    return {"docs": _http_errors(knowledge.list_docs, _org(request))}


@router.get("/docs/{doc_id}",
            dependencies=[Depends(require_role("admin", "sme"))])
def get_doc(doc_id: str, request: Request):
    """One doc with the full decrypted text (admin|sme). Cross-tenant ids
    404 with the SAME message as unknown ids (TENANCY.md #6)."""
    doc = _http_errors(knowledge.get_doc, _org(request), doc_id)
    if doc is None:
        raise HTTPException(404, f"doc {doc_id} not found")
    return doc


# ── L5 drafts ────────────────────────────────────────────────────────────────

class DraftBody(BaseModel):
    docIds: list[str]
    title: str = ""


@router.post("/drafts", dependencies=[Depends(require_role("admin", "sme"))])
def create_draft(body: DraftBody, request: Request):
    """Generate a deterministic L5 exam draft from the given vault docs
    (blueprint sections = doc titles; >= 8 recall/apply items). The response
    includes the DECRYPTED items so the reviewer can read them — this route
    is admin|sme for exactly that reason."""
    return _http_errors(
        knowledge.generate_l5_draft, _org(request), body.docIds,
        created_by=_user(request), title=body.title)


@router.get("/drafts")
def get_drafts(request: Request, role: str = Depends(require_role())):
    """Org's drafts, latest first (any authenticated role). The decrypted
    items (T2 — verbatim company passages) are included only for admin|sme;
    viewers get blueprint + status metadata."""
    include_items = role in ("admin", "sme")
    return {"drafts": _http_errors(
        knowledge.list_drafts, _org(request), include_items=include_items)}


class ReviewBody(BaseModel):
    note: str = ""


@router.post("/drafts/{draft_id}/approve",
             dependencies=[Depends(require_sme)])
def approve_draft(draft_id: str, body: ReviewBody, request: Request):
    """SME sign-off (role sme ONLY): flips the draft to 'approved', appends a
    signed 'sme_signoff' evidence row to the org chain, and returns the
    evidence id + examCertRef + examRunnable flag."""
    out = _http_errors(
        knowledge.approve_draft, _org(request), draft_id,
        reviewer=_user(request), note=body.note)
    if out is None:
        raise HTTPException(404, f"draft {draft_id} not found")
    return out


@router.post("/drafts/{draft_id}/reject",
             dependencies=[Depends(require_sme)])
def reject_draft(draft_id: str, body: ReviewBody, request: Request):
    """SME rejection (role sme ONLY) — same evidence trail as approval,
    payload outcome 'rejected'."""
    out = _http_errors(
        knowledge.reject_draft, _org(request), draft_id,
        reviewer=_user(request), note=body.note)
    if out is None:
        raise HTTPException(404, f"draft {draft_id} not found")
    return out


# ── Exam over the approved draft bank ────────────────────────────────────────

class DraftExamBody(BaseModel):
    candidateSpec: str | None = None   # agents/backend.get_backend spec string
    agentId: str | None = None
    dryRun: bool = True                # deterministic stub model (CI-safe)


@router.post("/drafts/{draft_id}/exam",
             dependencies=[Depends(require_role("admin", "sme"))])
def run_draft_exam(draft_id: str, body: DraftExamBody, request: Request):
    """Run the certification exam against the org's APPROVED draft bank.

    Job-backed exactly like POST /atp/exams/run: returns {jobId}; poll
    GET /jobs/{jobId} — when status='done' the result is the award dict.
    The bank is resolved through atp/exams.py's Phase 6 loader path
    (ORG_CERT_PREFIX ref → atp/knowledge.py in-memory bank; judge/candidate
    separation and evidence signing apply unchanged).
    """
    from agents import jobs

    org = _org(request)
    draft = _http_errors(knowledge.get_draft, org, draft_id)
    if draft is None:
        raise HTTPException(404, f"draft {draft_id} not found")
    if draft["status"] != "approved":
        raise HTTPException(
            409, f"draft {draft_id} is '{draft['status']}' — only an "
                 f"SME-approved draft can be examined")

    cert_ref = knowledge.EXAM_CERT_PREFIX + draft_id
    candidate_spec = body.candidateSpec
    agent_id = body.agentId
    dry_run = body.dryRun

    def _task():
        from atp import exams
        return exams.run_exam(
            cert_ref,
            candidate_spec,
            org_id=org,
            dry_run=dry_run,
            agent_id=agent_id,
        )

    job_id = jobs.submit("l5_draft_exam", _task, org_id=org)
    # jobId is the documented key; job_id keeps BU_API.runJob() compatible.
    return {"jobId": job_id, "job_id": job_id, "certRef": cert_ref}
