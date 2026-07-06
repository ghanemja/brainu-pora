"""
Bearer-token authentication for the Brain University FastAPI app.

Token format (URL-safe base64):
    <username>|<expiry_unix>|<hmac_sha256(username|expiry, BU_SECRET)>

Stateless, no DB. Verification recomputes the HMAC and checks expiry.

Env vars (read at process start):
    BU_AUTH_USER       — single allowed username (default "admin")
    BU_AUTH_PASSWORD   — REQUIRED; process refuses to start without it
                         (unless BU_AUTH_DISABLED=1)
    BU_AUTH_SECRET     — HMAC key; REQUIRED; process refuses to start without
                         it (unless BU_AUTH_DISABLED=1, which uses an ephemeral
                         random key — tokens invalidate on restart)
    BU_AUTH_TTL_HOURS  — token lifetime, default 24
    BU_AUTH_DISABLED   — "1" to bypass auth entirely (dev only; used by
                         scripts/demo_start.sh)

Routes protected by middleware are everything except an allowlist:
    /health, /login, /docs, /openapi.json, /redoc, /videos/{...}, /media/{...},
    OPTIONS preflight.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import sys
import time

from fastapi import HTTPException, Request


# ── Env-driven config ──────────────────────────────────────────────────────

AUTH_USER     = os.environ.get("BU_AUTH_USER", "admin")
AUTH_PASSWORD = os.environ.get("BU_AUTH_PASSWORD", "")
AUTH_SECRET   = os.environ.get("BU_AUTH_SECRET", "").encode("utf-8")
AUTH_TTL_S    = int(os.environ.get("BU_AUTH_TTL_HOURS", "24")) * 3600
AUTH_DISABLED = os.environ.get("BU_AUTH_DISABLED", "") == "1"

if AUTH_DISABLED:
    # Explicit dev/demo opt-in (scripts/demo_start.sh, .claude/launch.json).
    # Keep usable defaults so the login gate (which always POSTs /login)
    # works in demo mode without any env setup.
    print(
        "=" * 72 + "\n"
        "WARNING: BU_AUTH_DISABLED=1 — AUTHENTICATION IS BYPASSED (dev/demo\n"
        "only). The login gate accepts the dev default credentials, and the\n"
        "HMAC key is ephemeral (all tokens invalidate on restart). NEVER set\n"
        "BU_AUTH_DISABLED in production. Unset it and provide\n"
        "BU_AUTH_PASSWORD + BU_AUTH_SECRET to re-enable auth.\n"
        + "=" * 72,
        file=sys.stderr,
    )
    if not AUTH_SECRET:
        AUTH_SECRET = secrets.token_bytes(32)  # ephemeral; fine for dev
    if not AUTH_PASSWORD:
        AUTH_PASSWORD = "password"  # dev-only default; enabled path has NO default
else:
    _missing = [name for name, val in (
        ("BU_AUTH_PASSWORD", AUTH_PASSWORD),
        ("BU_AUTH_SECRET", AUTH_SECRET),
    ) if not val]
    if _missing:
        raise RuntimeError(
            "Refusing to start: required auth env var(s) unset: "
            + ", ".join(_missing)
            + ". Set them in the deployment environment (see render.yaml / "
            "DEPLOY.md), or export BU_AUTH_DISABLED=1 for local dev only "
            "(scripts/demo_start.sh does this)."
        )


# ── Token mint / verify ────────────────────────────────────────────────────

def mint_token(username: str, ttl_s: int | None = None) -> str:
    """Issue a fresh bearer token."""
    ttl = ttl_s or AUTH_TTL_S
    expiry = int(time.time()) + ttl
    payload = f"{username}|{expiry}"
    sig = hmac.new(AUTH_SECRET, payload.encode("utf-8"), hashlib.sha256).digest()
    raw = f"{payload}|{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def verify_token(token: str) -> str | None:
    """Return username if token valid + unexpired; else None."""
    if not token:
        return None
    try:
        # Re-pad base64 (urlsafe encoding may strip = padding)
        pad = "=" * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(token + pad).decode("utf-8")
        username, expiry_s, sig_b64 = raw.rsplit("|", 2)
        expiry = int(expiry_s)
    except Exception:
        return None
    if time.time() > expiry:
        return None
    expected = hmac.new(AUTH_SECRET, f"{username}|{expiry}".encode(), hashlib.sha256).digest()
    pad2 = "=" * (-len(sig_b64) % 4)
    try:
        provided = base64.urlsafe_b64decode(sig_b64 + pad2)
    except Exception:
        return None
    if not hmac.compare_digest(expected, provided):
        return None
    return username


def check_password(username: str, password: str) -> bool:
    """Constant-time comparison."""
    if not username or not password:
        return False
    u_ok = hmac.compare_digest(username, AUTH_USER)
    p_ok = hmac.compare_digest(password, AUTH_PASSWORD)
    return u_ok and p_ok


# ── ASGI middleware — gate every request except the allowlist ──────────────

PUBLIC_PATHS = {
    "/", "/health", "/login",
    "/docs", "/openapi.json", "/redoc",
}
PUBLIC_PREFIXES = ("/videos/", "/media/")  # static cached media


def is_public(path: str, method: str) -> bool:
    if method == "OPTIONS":  # CORS preflight
        return True
    if path in PUBLIC_PATHS:
        return True
    for p in PUBLIC_PREFIXES:
        if path.startswith(p):
            return True
    return False


async def auth_middleware(request: Request, call_next):
    """FastAPI ASGI middleware — reject unauthenticated requests."""
    if AUTH_DISABLED:
        return await call_next(request)
    if is_public(request.url.path, request.method):
        return await call_next(request)

    auth_hdr = request.headers.get("authorization", "")
    if not auth_hdr.lower().startswith("bearer "):
        from fastapi.responses import JSONResponse
        return JSONResponse(
            {"detail": "missing bearer token"}, status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_hdr.split(" ", 1)[1].strip()
    user = verify_token(token)
    if not user:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            {"detail": "invalid or expired token"}, status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Pass username through so downstream routes can read it
    request.state.user = user
    return await call_next(request)
