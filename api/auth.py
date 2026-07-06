"""
Bearer-token authentication for the Brain University FastAPI app.

Two token formats are accepted (Phase 2, docs/TENANCY.md):

  * Org session JWT (api/identity.py) — HS256 over BU_AUTH_SECRET, claims
    {sub, org_id, role, exp}. Tried FIRST by verify_token().
  * Legacy single-admin HMAC token (URL-safe base64):
        <username>|<expiry_unix>|<hmac_sha256(username|expiry, BU_SECRET)>
    Fallback — kept for backward compatibility with the deployed demo; a
    legacy token maps to the bootstrap org 'org-demo' with role 'admin'.

Stateless, no DB. Verification recomputes the HMAC / JWT signature and
checks expiry. On success the middleware sets request.state.user /
.user_id / .org_id / .role; route handlers gate roles with require_role().

Env vars (read at process start):
    BU_AUTH_USER       — single allowed username (default "admin")
    BU_AUTH_PASSWORD   — REQUIRED; process refuses to start without it
                         (unless BU_AUTH_DISABLED=1)
    BU_AUTH_SECRET     — HMAC key; REQUIRED; process refuses to start without
                         it (unless BU_AUTH_DISABLED=1, which uses an ephemeral
                         random key — tokens invalidate on restart)
    BU_AUTH_TTL_HOURS  — token lifetime, default 24
    BU_AUTH_DISABLED   — "1" to bypass auth entirely (dev only; used by
                         scripts/demo_start.sh). Requests run as
                         org-demo/admin so org-scoped routes keep working.

Routes protected by middleware are everything except an allowlist:
    /health, /login, /auth/login, /auth/oidc/{login,callback}, /docs,
    /openapi.json, /redoc, /videos/{...}, /media/{...}, OPTIONS preflight.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import sys
import time
from typing import NamedTuple

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
    if len(AUTH_SECRET) < 32:
        # HS256 signing key — short keys are brute-forceable. Same fail-loud
        # posture as the missing-var check above.
        raise RuntimeError(
            "Refusing to start: BU_AUTH_SECRET is shorter than 32 bytes. "
            "Generate one with: python3 -c \"import secrets; "
            "print(secrets.token_urlsafe(48))\""
        )


# ── Token mint / verify ────────────────────────────────────────────────────

# Bootstrap org for legacy single-admin tokens (seeded by migrations/004).
LEGACY_ORG_ID = "org-demo"
LEGACY_ROLE = "admin"


class Principal(NamedTuple):
    """Verified caller identity, copied onto request.state by the middleware.

    user    — display identifier (org users: user id / legacy: username)
    user_id — users.user_id for org sessions; None for legacy tokens
    org_id  — tenant id (legacy tokens map to 'org-demo')
    role    — admin | sme | viewer (legacy tokens map to 'admin')
    """

    user: str
    user_id: str | None
    org_id: str
    role: str


def mint_token(username: str, ttl_s: int | None = None) -> str:
    """Issue a fresh LEGACY bearer token (single-admin HMAC format)."""
    ttl = ttl_s or AUTH_TTL_S
    expiry = int(time.time()) + ttl
    payload = f"{username}|{expiry}"
    sig = hmac.new(AUTH_SECRET, payload.encode("utf-8"), hashlib.sha256).digest()
    raw = f"{payload}|{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def verify_token(token: str) -> Principal | None:
    """Verify a bearer token of either format → Principal, or None.

    Order: org session JWT (api.identity.verify_session) first, then the
    legacy single-admin HMAC token — which maps to org-demo/admin so the
    pre-Phase-2 deployed demo keeps working unchanged.
    """
    if not token:
        return None
    try:
        from api import identity
    except ImportError:  # identity deps not installed — legacy still works
        identity = None
    if identity is not None:
        claims = identity.verify_session(token)
        if claims:
            return Principal(
                user=claims["sub"],
                user_id=claims["sub"],
                org_id=claims["org_id"],
                role=claims["role"],
            )
    username = _verify_legacy_token(token)
    if username is not None:
        return Principal(user=username, user_id=None,
                         org_id=LEGACY_ORG_ID, role=LEGACY_ROLE)
    return None


def _verify_legacy_token(token: str) -> str | None:
    """Return username if the legacy HMAC token is valid + unexpired."""
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
    "/auth/login", "/auth/oidc/login", "/auth/oidc/callback",
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


def _set_principal(request: Request, principal: Principal) -> None:
    request.state.user = principal.user
    request.state.user_id = principal.user_id
    request.state.org_id = principal.org_id
    request.state.role = principal.role


async def auth_middleware(request: Request, call_next):
    """FastAPI ASGI middleware — reject unauthenticated requests."""
    if AUTH_DISABLED:
        # Dev bypass runs as the legacy admin principal so org-scoped
        # routes (request.state.org_id / require_role) keep working.
        _set_principal(request, Principal(
            user=AUTH_USER, user_id=None,
            org_id=LEGACY_ORG_ID, role=LEGACY_ROLE,
        ))
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
    principal = verify_token(token)
    if not principal:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            {"detail": "invalid or expired token"}, status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Pass identity through so downstream routes can read it
    _set_principal(request, principal)
    return await call_next(request)


# ── Role gating — FastAPI dependency factory ───────────────────────────────

def require_role(*roles: str):
    """Dependency factory: require the verified session role to be in `roles`.

    Usage:
        @router.post("/thing", dependencies=[Depends(require_role("admin"))])
        # or, to read the role:
        def handler(role: str = Depends(require_role("admin", "sme"))): ...

    Roles are matched exactly (no implicit hierarchy) — pass every role that
    may call the route. With no arguments it only requires authentication.
    Legacy tokens and the BU_AUTH_DISABLED=1 dev bypass carry role 'admin'.
    """

    def _dependency(request: Request) -> str:
        role = getattr(request.state, "role", None)
        if role is None:
            # Public/unauthenticated path — the middleware never ran a
            # verification for this request.
            raise HTTPException(
                status_code=401, detail="authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if roles and role not in roles:
            raise HTTPException(status_code=403, detail="insufficient role")
        return role

    return _dependency
