"""
FastAPI bridge — exposes Brain University's Python engine to the React UI.

Run:
  uvicorn api.server:app --reload --port 8080

Endpoints:
  GET  /health                                   — liveness
  GET  /graph                                    — full graph payload (nodes + edges)
  GET  /trailhead?user_id=X&interest=Y           — ranked start cards
  GET  /lesson?node=X&mode=auto&level=undergrad  — lesson card (optional difficulty rewrite)
  POST /walks/start                              — body: {user_id, start_node, planned}
  POST /walks/{walk_id}/event                    — body: {node, step_idx, quiz_quality, ...}
  POST /walks/{walk_id}/complete                 — mark walk done
  GET  /podcast/script?topic=X&length=medium     — generate podcast script
  POST /podcast/render                           — body: {script_dict} → mp3+mp4 paths
  POST /podcast/interject                        — body: {script, turn_index, question}
  GET  /briefing?node=X                          — 60s lesson briefing audio
  POST /socratic/start                           — body: {user_id, node}
  POST /socratic/step                            — body: {session_id, answer}
  POST /sr/review                                — body: {user_id, node, quality}
  GET  /sr/due?user_id=X                         — due flashcards
  GET  /heatmap?user_id=X                        — per-cluster mastery
  POST /feedback                                 — body: {target_kind, target_id, thumb}
  POST /propose                                  — body: {user_id, text}
  POST /voice                                    — multipart: audio file → transcript
  GET  /citation?claim=X&papers=p1,p2            — top supporting paragraphs
  POST /ingest/arxiv                             — body: {interests:[...]} → new ids
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
    from pydantic import BaseModel
except ImportError as e:
    raise RuntimeError(
        "FastAPI not installed. Run: pip install fastapi uvicorn[standard]"
    ) from e

import asyncio
import queue
import threading

PROJECT_ROOT = Path(__file__).parent.parent

import os
# CORS_ORIGINS = comma-separated allowlist in prod (e.g. your Netlify URL);
# defaults to "*" for local dev when unset.
_cors = os.environ.get("CORS_ORIGINS", "*")
_origins = ["*"] if _cors.strip() == "*" else [o.strip() for o in _cors.split(",") if o.strip()]

app = FastAPI(title="Brain University", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Tenant access audit (Phase 2 — docs/TENANCY.md §4 layer 4) ────────────
# Starlette runs the LAST-registered http middleware FIRST, so registering
# this BEFORE auth_middleware (below) makes it the inner layer: on the
# request path it runs AFTER auth — request.state.{user,org_id,role} are
# already populated and 401-rejected requests never reach it. Rows are
# written fire-and-forget on a single-worker pool so the response is never
# blocked, and every failure (including atp/tenant_db.py not being deployed
# yet) is swallowed — the audit trail must never take the API down.
from concurrent.futures import ThreadPoolExecutor as _AccessLogPool

_ACCESS_LOG_POOL = _AccessLogPool(max_workers=1, thread_name_prefix="bu-accesslog")


@app.middleware("http")
async def access_log_middleware(request: Request, call_next):
    response = await call_next(request)
    try:
        import api.auth as _auth
        if _auth.AUTH_DISABLED:          # dev mode: no audit rows
            return response
        if _auth.is_public(request.url.path, request.method):
            return response              # public surface: not tenant data
        user = getattr(request.state, "user", None)
        if user is None:                 # unauthenticated (shouldn't happen
            return response              # behind the auth middleware)
        org_id = getattr(request.state, "org_id", None) or "org-demo"
        role = getattr(request.state, "role", None) or "admin"
        method, path = request.method, request.url.path
        status = response.status_code

        def _write() -> None:
            try:
                from atp import tenant_db
                tenant_db.log_access(
                    org_id=org_id, user=user, role=role,
                    method=method, path=path, status=status,
                )
            except Exception:  # noqa: BLE001 — fire-and-forget by contract
                pass

        _ACCESS_LOG_POOL.submit(_write)
    except Exception:  # noqa: BLE001 — auditing must never block a response
        pass
    return response


# Bearer-token auth on every route except an allowlist (/health, /login,
# /docs, /videos, /media, OPTIONS preflight). Configure via env vars
# BU_AUTH_USER / BU_AUTH_PASSWORD / BU_AUTH_SECRET. See api/auth.py.
from api.auth import auth_middleware, mint_token, check_password
app.middleware("http")(auth_middleware)

# ATP (Agent University) routes — /atp/* (see api/atp.py + docs/ATP.md §5).
from api.atp import router as atp_router
app.include_router(atp_router)

# Identity routes (Phase 2 — OIDC code flow, local org accounts, org-scoped
# JWT sessions; see api/identity.py + docs/TENANCY.md). Guarded import so the
# legacy single-admin demo keeps booting if this file ships first.
try:
    from api.identity import router as identity_router
except ImportError:  # pragma: no cover — api/identity.py not deployed yet
    identity_router = None
    import sys as _sys
    print("WARNING: api/identity.py not present — identity routes not "
          "mounted; legacy /login only.", file=_sys.stderr)
if identity_router is not None:
    app.include_router(identity_router)


def _request_org(request: Request) -> str:
    """Tenant for this request — ONLY ever from verified auth state
    (request.state.org_id, set by the auth middleware from the JWT; TENANCY.md
    §4 layer 1), never from client-supplied values. The 'org-demo' fallback
    covers BU_AUTH_DISABLED dev mode and legacy single-admin tokens."""
    return getattr(request.state, "org_id", None) or "org-demo"


class LoginBody(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(body: LoginBody):
    """Validate credentials and return a bearer token."""
    if not check_password(body.username, body.password):
        import time as _t
        _t.sleep(0.25)  # constant-time-ish delay to slow credential stuffing
        raise HTTPException(401, "invalid credentials")
    return {"token": mint_token(body.username), "username": body.username}


# ── Helpers — lazy graph build (cached) ────────────────────────────────────

_GRAPH_CACHE: dict[str, Any] = {}


def _graph():
    """Build the merged corpus graph + cluster list once and cache."""
    if "G" in _GRAPH_CACHE:
        return _GRAPH_CACHE
    from graph.clusters import build_clusters, load_graph
    from graph.foundations import recommend
    clusters = build_clusters()          # cached to data/sessions/clusters.json
    G = load_graph()
    foundations = recommend(limit=8)
    _GRAPH_CACHE.update(G=G, clusters=clusters, foundations=foundations)
    return _GRAPH_CACHE


# ── Pydantic bodies ────────────────────────────────────────────────────────

class WalkStartBody(BaseModel):
    user_id: str
    start_node: str
    planned: list[str]


class WalkEventBody(BaseModel):
    user_id: str
    node: str | None = None
    step_idx: int | None = None
    lesson_mode: str | None = None
    quiz_quality: int | None = None
    duration_s: float | None = None


class PodcastRenderBody(BaseModel):
    script: dict
    voice_backend: str | None = None


class InterjectBody(BaseModel):
    script: dict
    turn_index: int
    question: str


class SocraticStartBody(BaseModel):
    user_id: str
    node: str


class SocraticStepBody(BaseModel):
    session_id: str
    answer: str


class SRReviewBody(BaseModel):
    user_id: str
    node: str
    quality: int


class FeedbackBody(BaseModel):
    user_id: str
    target_kind: str
    target_id: str
    thumb: int
    note: str | None = None


class ProposeBody(BaseModel):
    user_id: str
    text: str


class ArxivBody(BaseModel):
    interests: list[str]
    lookback_days: int = 1
    max_per_interest: int = 5


class PaperDropBody(BaseModel):
    url_or_id: str
    podcast_length: str = "short"


class PaperVideoBody(BaseModel):
    paper_id: str
    force: bool = False  # re-render even if cached


class DebateBody(BaseModel):
    topic: str
    rounds: int = 2
    paper_id: str | None = None


class CodeExtractBody(BaseModel):
    passage: str


class ConfusionSignalBody(BaseModel):
    user_id: str
    paragraph_hash: str
    signal_kind: str
    value: float = 1.0


class ConfusionELI5Body(BaseModel):
    paragraph_text: str


class AnimationBody(BaseModel):
    passage: str
    voiceover_hint: str = ""
    try_manim: bool = False


class LocalPodcastBody(BaseModel):
    source: str            # URL, file path, or raw text
    mode:   str = "auto"   # auto | podcastfy | kokoro_pipeline
    length: str = "medium"
    tts:    str = "edge"


class LocalInterjectBody(BaseModel):
    mp3:           str
    question:      str
    recent_quote:  str = ""
    voice_backend: str = "kokoro"


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.post("/podcast/local")
def podcast_local(body: LocalPodcastBody):
    """Generate a fully-local podcast (no cloud TTS). podcastfy if present,
    else Kokoro pipeline. Returns mp3 path."""
    from agents.local_podcast import generate_local, status
    p = generate_local(body.source, mode=body.mode, length=body.length, tts=body.tts)
    if not p:
        raise HTTPException(503, {"reason": "local podcast generation failed",
                                    "status": status()})
    return {"mp3": str(p.relative_to(PROJECT_ROOT))}


@app.get("/podcast/local/status")
def podcast_local_status():
    from agents.local_podcast import status
    from agents.voices import available_backends
    return {"local_podcast": status(), "tts_backends": available_backends()}


@app.post("/podcast/local/interject")
def podcast_local_interject(body: LocalInterjectBody):
    """Pause-and-ask for an opaque local podcast. Reads sidecar meta for the
    source text, asks Claude for 1-3 freeform turns, renders them locally."""
    from agents.local_podcast import lookup_mp3, load_meta
    from agents.interactive_podcast import (
        generate_interjection_freeform, render_interjection_audio,
    )
    mp3 = lookup_mp3(body.mp3)
    if not mp3:
        raise HTTPException(404, f"mp3 {body.mp3} not found")
    meta = load_meta(mp3)
    if not meta or not meta.get("source_text"):
        raise HTTPException(400, "no source meta found for this mp3")
    turns = generate_interjection_freeform(
        source_text=meta["source_text"],
        question=body.question,
        recent_quote=body.recent_quote,
    )
    if not turns:
        raise HTTPException(503, "interjection generation failed")
    audio = render_interjection_audio(turns, voice_backend=body.voice_backend)
    return {"turns": turns,
            "audio_path": str(audio.relative_to(PROJECT_ROOT)) if audio else None}

# ── Background jobs (async podcast render) ────────────────────────────────

@app.post("/podcast/render/async")
def podcast_render_async(body: PodcastRenderBody, request: Request):
    """Enqueue a cloud podcast render; returns a job_id to poll at /jobs/{id}."""
    from agents import jobs, podcast_video

    def task():
        r = podcast_video.render(body.script, voice_backend=body.voice_backend)
        if not r:
            raise RuntimeError("render failed (check moviepy/gTTS install)")
        return {k: str(v.relative_to(PROJECT_ROOT)) for k, v in r.items()}

    return {"job_id": jobs.submit("podcast_render", task,
                                  org_id=_request_org(request))}


@app.post("/podcast/local/async")
def podcast_local_async(body: LocalPodcastBody, request: Request):
    """Enqueue a fully-local podcast render; poll at /jobs/{id}."""
    from agents import jobs
    from agents.local_podcast import generate_local

    def task():
        p = generate_local(body.source, mode=body.mode,
                            length=body.length, tts=body.tts)
        if not p:
            raise RuntimeError("local podcast generation failed")
        return {"mp3": str(p.relative_to(PROJECT_ROOT))}

    return {"job_id": jobs.submit("podcast_local", task,
                                  org_id=_request_org(request))}


@app.get("/jobs/{job_id}")
def job_status(job_id: str, request: Request):
    """Job status, scoped to the caller's org (jobs.get only sees the org's
    own rows — RLS-backed on Postgres). A cross-tenant id 404s with the SAME
    message as an unknown id — no existence oracle (TENANCY.md #6)."""
    from agents import jobs
    j = jobs.get(job_id, org_id=_request_org(request))
    if not j:
        raise HTTPException(404, f"no such job {job_id}")
    return j


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/graph")
def graph_endpoint():
    g = _graph()["G"]
    nodes = [{"id": n, **dict(g.nodes[n])} for n in g.nodes]
    edges = [{"source": u, "target": v, **dict(d)} for u, v, d in g.edges(data=True)]
    return {"nodes": nodes, "edges": edges}


@app.get("/trailhead")
def trailhead(user_id: str = "anon", interest: str = "", n: int = 5):
    from agents.persistence import ensure_user
    ensure_user(user_id)
    gs = _graph()
    foundations = gs["foundations"]
    return {"cards": [_foundation_card(f) for f in foundations[:n]]}


def _foundation_card(f) -> dict:
    return {
        "node": getattr(f, "raw_name", None) or getattr(f, "name", str(f)),
        "score": getattr(f, "score", None),
        "rationale": getattr(f, "rationale", []),
        "cluster_id": getattr(f, "cluster_id", None),
    }


@app.get("/lesson")
def lesson_endpoint(node: str, mode: str = "auto",
                    interest: str = "", level: str = ""):
    from agents.curriculum import lesson_for
    gs = _graph()
    clusters = gs["clusters"]
    cluster = next(
        (c for c in clusters
         if node in [n for n, _ in (c.top_nodes or [])]),
        clusters[0] if clusters else None,
    )
    if cluster is None:
        raise HTTPException(404, "no cluster found")
    card = lesson_for(node, cluster, clusters, interest=interest, mode=mode)
    if level:
        from agents.difficulty import rewrite
        card = rewrite(card, level=level)
    return card


@app.post("/walks/start")
def walks_start(body: WalkStartBody):
    from agents.persistence import start_walk, ensure_user
    ensure_user(body.user_id)
    walk_id = start_walk(body.user_id, body.start_node, body.planned)
    return {"walk_id": walk_id}


@app.post("/walks/{walk_id}/event")
def walks_event(walk_id: int, body: WalkEventBody):
    from agents.persistence import log_walk_event
    log_walk_event(
        walk_id, body.user_id,
        node=body.node, step_idx=body.step_idx,
        lesson_mode=body.lesson_mode, quiz_quality=body.quiz_quality,
        duration_s=body.duration_s,
    )
    return {"ok": True}


@app.post("/walks/{walk_id}/complete")
def walks_complete(walk_id: int):
    from agents.persistence import complete_walk
    complete_walk(walk_id)
    return {"ok": True}


# ── Podcast ────────────────────────────────────────────────────────────────

@app.get("/podcast/script")
def podcast_script_endpoint(topic: str, length: str = "medium",
                             source_kind: str = "wiki",
                             source_id: str | None = None,
                             angle: str = ""):
    from agents import podcast_script as ps
    source_id = source_id or topic
    if source_kind == "wiki":
        source = ps.source_from_wiki(source_id)
    elif source_kind == "paper":
        source = ps.source_from_paper(source_id)
    elif source_kind == "cluster":
        gs = _graph()
        try:
            cid = int(source_id)
        except ValueError:
            cid = None
        cluster = next((c for c in gs["clusters"]
                        if getattr(c, "cluster_id", None) == cid), None)
        if cluster is None:
            raise HTTPException(404, "cluster not found")
        source = ps.source_from_cluster(cluster)
    else:
        raise HTTPException(400, f"unknown source_kind {source_kind}")
    script = ps.generate_script(topic=topic, source_text=source,
                                length=length, angle=angle)
    if not script:
        raise HTTPException(503, "script generation failed (Claude unavailable?)")
    return script


@app.post("/podcast/render")
def podcast_render_endpoint(body: PodcastRenderBody):
    from agents import podcast_video
    result = podcast_video.render(body.script, voice_backend=body.voice_backend)
    if not result:
        raise HTTPException(503, "render failed (check moviepy/gTTS install)")
    return {k: str(v.relative_to(PROJECT_ROOT)) for k, v in result.items()}


@app.post("/podcast/interject")
def podcast_interject_endpoint(body: InterjectBody):
    from agents import interactive_podcast
    turns = interactive_podcast.generate_interjection(
        body.script, body.turn_index, body.question
    )
    if not turns:
        raise HTTPException(503, "interjection generation failed")
    audio = interactive_podcast.render_interjection_audio(turns)
    return {
        "turns": turns,
        "audio_path": str(audio.relative_to(PROJECT_ROOT)) if audio else None,
    }


@app.get("/briefing")
def briefing_endpoint(node: str, interest: str = ""):
    from agents.curriculum import lesson_for
    from agents.audio_briefing import briefing_text, briefing_audio
    gs = _graph()
    cluster = next(
        (c for c in gs["clusters"]
         if node in [n for n, _ in (c.top_nodes or [])]),
        gs["clusters"][0] if gs["clusters"] else None,
    )
    lesson = lesson_for(node, cluster, gs["clusters"], interest=interest)
    text = briefing_text(lesson)
    audio = briefing_audio(lesson)
    return {
        "text": text,
        "audio_path": str(audio.relative_to(PROJECT_ROOT)) if audio else None,
    }


# ── Socratic ───────────────────────────────────────────────────────────────

@app.post("/socratic/start")
def socratic_start(body: SocraticStartBody):
    from agents.socratic import start_session
    from agents.persistence import save_socratic_session
    import uuid
    state = start_session(body.node)
    sid = f"soc_{uuid.uuid4().hex[:12]}"
    save_socratic_session(sid, body.user_id, body.node, state)
    return {"session_id": sid, "state": state}


@app.post("/socratic/step")
def socratic_step(body: SocraticStepBody):
    from agents.socratic import step
    from agents.persistence import (load_socratic_session,
                                    update_socratic_session)
    session = load_socratic_session(body.session_id)
    if not session:
        raise HTTPException(404, "session not found")
    new_state = step(session["state"], body.answer)
    update_socratic_session(body.session_id, new_state)
    return new_state


# ── Spaced repetition ──────────────────────────────────────────────────────

@app.post("/sr/review")
def sr_review(body: SRReviewBody):
    from agents.spaced_repetition import schedule_review
    due = schedule_review(body.user_id, body.node, body.quality)
    return {"due_ts": due}


@app.get("/sr/due")
def sr_due(user_id: str, limit: int = 10):
    from agents.spaced_repetition import due_cards
    return {"cards": due_cards(user_id, limit=limit)}


# ── Heatmap / feedback / propose ──────────────────────────────────────────

@app.get("/heatmap")
def heatmap_endpoint(user_id: str):
    from agents.heatmap import mastery_per_cluster
    gs = _graph()
    return {"mastery": mastery_per_cluster(user_id, gs["clusters"])}


@app.post("/feedback")
def feedback_endpoint(body: FeedbackBody):
    from agents.persistence import add_feedback
    add_feedback(body.user_id, body.target_kind, body.target_id,
                 body.thumb, body.note)
    return {"ok": True}


@app.post("/propose")
def propose_endpoint(body: ProposeBody):
    from agents.proposal_responder import respond
    result = respond(body.text)
    return result if isinstance(result, dict) else {"response": str(result)}


# ── Voice input ────────────────────────────────────────────────────────────

@app.post("/voice")
async def voice_endpoint(audio: UploadFile = File(...),
                         lang: str = Form("en")):
    import tempfile
    suffix = Path(audio.filename or "blob.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name
    from agents.voice_input import transcribe
    text = transcribe(tmp_path, lang=lang)
    return {"text": text}


# ── Citation / arxiv ──────────────────────────────────────────────────────

@app.get("/citation")
def citation_endpoint(claim: str, papers: str, k: int = 3):
    from agents.citation_backtrack import candidates
    paper_ids = [p.strip() for p in papers.split(",") if p.strip()]
    return {"candidates": candidates(claim, paper_ids, k=k)}


@app.post("/ingest/arxiv")
def ingest_arxiv(body: ArxivBody):
    from agents.arxiv_ingest import ingest
    added = ingest(body.interests, body.lookback_days, body.max_per_interest)
    return {"added": added, "count": len(added)}


# ── Media serving ──────────────────────────────────────────────────────────

# ── Paper drop (SSE cascade) ──────────────────────────────────────────────

@app.post("/paper/drop")
def paper_drop(body: PaperDropBody):
    """Stream the paper-drop cascade as SSE: resolved → fetched → classified
    → ingested → podcast_starting → podcast_ready → done."""
    from agents.paper_drop import cascade

    q: queue.Queue = queue.Queue()

    def emit(kind, data):
        q.put({"kind": kind, "data": data})

    def runner():
        try:
            result = cascade(body.url_or_id, emit=emit,
                             podcast_length=body.podcast_length)
            q.put({"kind": "final", "data": _trim_final(result)})
        except Exception as e:
            q.put({"kind": "error", "data": {"reason": str(e)}})
        finally:
            q.put(None)

    threading.Thread(target=runner, daemon=True).start()

    async def stream():
        loop = asyncio.get_event_loop()
        while True:
            evt = await loop.run_in_executor(None, q.get)
            if evt is None:
                break
            yield f"data: {json.dumps(evt)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


# ── On-demand arXivis video render (SSE) ───────────────────────────────────

@app.post("/paper/video/render")
def paper_video_render(body: PaperVideoBody):
    """Render the 30-sec explainer for a paper on demand.

    Streams SSE: cache_hit | layout | frames_start | frame (done/total) |
    encode | encoded | done | error. Re-uses the cache (videos/<safe>.mp4)
    unless force=True.
    """
    import re
    from pathlib import Path
    from scripts.render_arxivis_video import (
        safe_id, render_video, load_papers,
        VIDEOS_DIR, MANIFEST_JS,
    )

    pid = body.paper_id
    safe = safe_id(pid)
    rel_url = f"videos/{safe}.mp4"
    out_path = VIDEOS_DIR / f"{safe}.mp4"

    q: queue.Queue = queue.Queue()

    def emit(stage, data=None):
        q.put({"kind": stage, "data": data or {}})

    # Fast path: cache hit
    if out_path.exists() and not body.force:
        async def cached_stream():
            yield f"data: {json.dumps({'kind': 'cache_hit', 'data': {'url': rel_url}})}\n\n"
            yield f"data: {json.dumps({'kind': 'done', 'data': {'url': rel_url, 'cached': True}})}\n\n"
        return StreamingResponse(cached_stream(), media_type="text/event-stream")

    def runner():
        try:
            papers = load_papers()
            paper = next((p for p in papers if p["id"] == pid), None)
            if not paper:
                emit("error", {"reason": f"paper id not found in arxivis_data: {pid}"})
                return
            ok = render_video(paper, out_path, cleanup=True, progress=emit)
            if not ok:
                emit("error", {"reason": "render returned False (no positions?)"})
                return

            # Merge into manifest
            manifest = {}
            if MANIFEST_JS.exists():
                try:
                    txt = MANIFEST_JS.read_text()
                    m = re.search(r"window\.ARXIVIS_VIDEOS\s*=\s*(.*?);\s*$", txt, re.DOTALL)
                    if m:
                        manifest = json.loads(m.group(1))
                except Exception:
                    manifest = {}
            manifest[pid] = rel_url
            MANIFEST_JS.write_text(
                "window.ARXIVIS_VIDEOS = " + json.dumps(manifest, indent=2) + ";\n"
            )
            emit("done", {"url": rel_url, "cached": False})
        except Exception as e:
            emit("error", {"reason": str(e)})
        finally:
            q.put(None)

    threading.Thread(target=runner, daemon=True).start()

    async def stream():
        loop = asyncio.get_event_loop()
        while True:
            evt = await loop.run_in_executor(None, q.get)
            if evt is None:
                break
            yield f"data: {json.dumps(evt)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


# ── Serve cached videos so the frontend can <video src="..."> them ────────

@app.get("/videos/{filename}")
def serve_video(filename: str):
    from pathlib import Path
    from scripts.render_arxivis_video import VIDEOS_DIR
    p = VIDEOS_DIR / filename
    if not p.exists() or ".." in filename:
        raise HTTPException(404, "video not found")
    return FileResponse(str(p), media_type="video/mp4")


def _trim_final(result: dict) -> dict:
    """Shrink the cascade result for SSE delivery — drop full podcast turns,
    keep counts."""
    out = dict(result or {})
    script = out.get("podcast_script")
    if script:
        out["podcast_script"] = {
            "title":   script.get("title"),
            "summary": script.get("summary"),
            "n_turns": len(script.get("turns") or []),
        }
    return out


# ── Multi-agent debate (SSE) ──────────────────────────────────────────────

@app.post("/debate/stream")
def debate_stream(body: DebateBody):
    """Stream agent turns as they happen during a multi-agent debate."""
    from agents.orchestrator import run_debate
    from agents.specialists import SPECIALISTS

    q: queue.Queue = queue.Queue()

    def on_turn(turn):
        q.put({
            "kind": "turn",
            "data": {
                "agent":      turn.agent,
                "spec_key":   turn.spec_key,
                "round":      turn.round,
                "text":       (turn.raw_text or "")[:1200],
                "citations":  turn.citations,
                "confidence": turn.confidence,
            },
        })

    def runner():
        try:
            q.put({"kind": "specialists",
                   "data": {"names": list(SPECIALISTS.keys())}})
            history, _wiki = run_debate(
                problem=body.topic, rounds=body.rounds, on_turn=on_turn,
            )
            q.put({"kind": "done", "data": {"n_turns": len(history.turns)}})
        except Exception as e:
            q.put({"kind": "error", "data": {"reason": str(e)}})
        finally:
            q.put(None)

    threading.Thread(target=runner, daemon=True).start()

    async def stream():
        loop = asyncio.get_event_loop()
        while True:
            evt = await loop.run_in_executor(None, q.get)
            if evt is None:
                break
            yield f"data: {json.dumps(evt)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


# ── Time-travel ──────────────────────────────────────────────────────────

@app.get("/history/timeline")
def history_timeline(user_id: str):
    from agents.time_travel import timeline
    return {"events": timeline(user_id)}


@app.get("/history/snapshot")
def history_snapshot(user_id: str, ts: float | None = None):
    from agents.time_travel import graph_state
    gs = _graph()
    all_nodes = list(gs["G"].nodes)
    return graph_state(user_id, ts, all_nodes=all_nodes)


# ── Code-from-paper ──────────────────────────────────────────────────────

@app.post("/code/extract")
def code_extract(body: CodeExtractBody):
    from agents.code_extractor import extract
    out = extract(body.passage)
    if not out:
        raise HTTPException(503, "code extraction failed")
    return out


# ── Confusion ────────────────────────────────────────────────────────────

@app.post("/confusion/signal")
def confusion_signal(body: ConfusionSignalBody):
    from agents.confusion import log_signal, score
    log_signal(body.user_id, body.paragraph_hash, body.signal_kind, body.value)
    return {"score": score(body.user_id, body.paragraph_hash)}


@app.get("/confusion/score")
def confusion_score(user_id: str, paragraph_hash: str):
    from agents.confusion import score
    return {"score": score(user_id, paragraph_hash)}


@app.get("/confusion/hotspots")
def confusion_hotspots(user_id: str, top_k: int = 5):
    from agents.confusion import hotspots
    return {"hotspots": hotspots(user_id, top_k=top_k)}


@app.post("/confusion/eli5")
def confusion_eli5_endpoint(body: ConfusionELI5Body):
    from agents.confusion import eli5
    out = eli5(body.paragraph_text)
    if not out:
        raise HTTPException(503, "eli5 failed")
    return out


# ── Papers library ───────────────────────────────────────────────────────

@app.get("/papers")
def list_papers(q: str = "", limit: int = 200):
    """List all ingested papers (defense corpus + paper-drop additions)."""
    corpus_path = PROJECT_ROOT / "data" / "defense_corpus_samples.json"
    if not corpus_path.exists():
        return {"papers": []}
    try:
        corpus = json.loads(corpus_path.read_text())
    except json.JSONDecodeError:
        return {"papers": []}

    papers = corpus.get("papers", []) or []
    if q:
        qlow = q.lower()
        papers = [
            p for p in papers
            if qlow in (p.get("title", "") + " "
                        + p.get("abstract", "") + " "
                        + " ".join(p.get("topics", []) or [])).lower()
        ]
    # Sort: paper-drop additions first (have ingested_at), then originals
    papers = sorted(papers, key=lambda p: p.get("ingested_at", ""), reverse=True)
    return {"papers": papers[:limit], "total": len(papers)}


@app.get("/papers/{paper_id}")
def get_paper(paper_id: str):
    corpus_path = PROJECT_ROOT / "data" / "defense_corpus_samples.json"
    if not corpus_path.exists():
        raise HTTPException(404, "no corpus")
    corpus = json.loads(corpus_path.read_text())
    for p in corpus.get("papers", []):
        if p.get("id") == paper_id:
            return p
    raise HTTPException(404, f"paper {paper_id} not found")


# ── Animated explainer (3Blue1Brown / Math Motion style) ─────────────────

@app.post("/animation/script")
def animation_script_endpoint(body: AnimationBody):
    """Generate a SceneSpec for the browser SVG/KaTeX player. If try_manim
    is true AND manim is installed, also render an mp4 server-side."""
    from agents.animation_script import generate
    scene = generate(body.passage, body.voiceover_hint)
    if not scene:
        raise HTTPException(503, "scene generation failed (Claude unavailable?)")

    manim_path = None
    if body.try_manim:
        try:
            from agents.manim_renderer import render, manim_available
            if manim_available():
                p = render(scene)
                if p:
                    manim_path = str(p.relative_to(PROJECT_ROOT))
        except Exception:
            pass

    return {"scene": scene, "manim_path": manim_path,
            "manim_available": _manim_installed()}


def _manim_installed() -> bool:
    import shutil
    return shutil.which("manim") is not None


# ── Eval dashboard ───────────────────────────────────────────────────────

@app.get("/eval/dashboard")
def eval_dashboard_endpoint():
    from eval.dashboard import dashboard
    return dashboard()


@app.get("/media/{path:path}")
def media_serve(path: str):
    target = PROJECT_ROOT / "data" / "sessions" / "media" / path
    if not target.exists() or not target.is_file():
        raise HTTPException(404, "not found")
    return FileResponse(str(target))


def _now() -> float:
    import time
    return time.time()
