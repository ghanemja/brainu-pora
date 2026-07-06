"""
Org-scoped identity for Brain University — Phase 2 (docs/TENANCY.md).

Three ways to obtain a session:
  1. POST /auth/login {email, password}          — local accounts (argon2id)
  2. GET  /auth/oidc/login → GET /auth/oidc/callback — OIDC authorization-code
     flow (issuer/client from env; endpoints 404 when OIDC_ISSUER is unset)
  3. Legacy POST /login (api/server.py)          — single-admin HMAC token;
     api.auth.verify_token() maps it to org 'org-demo' with role 'admin', so
     the deployed demo keeps working with zero new env.

Session = JWT (HS256 over BU_AUTH_SECRET), claims {sub, org_id, role, exp}.
`sub` is users.user_id (the identity spec's `id` — see migrations/004).

Env (all optional; partial sets fail loudly, P0 style):
  BU_BOOTSTRAP_ADMIN_EMAIL   — with _PASSWORD: provision this local admin in
  BU_BOOTSTRAP_ADMIN_PASSWORD  org 'org-demo' on first use if absent.
                               One without the other = RuntimeError.
  OIDC_ISSUER                — enables /auth/oidc/*; discovery at
                               {OIDC_ISSUER}/.well-known/openid-configuration
  OIDC_CLIENT_ID             — REQUIRED once OIDC_ISSUER is set
  OIDC_CLIENT_SECRET         — REQUIRED once OIDC_ISSUER is set
  OIDC_REDIRECT_URL          — REQUIRED once OIDC_ISSUER is set; must match
                               the IdP-registered callback
                               (https://host/auth/oidc/callback)

OIDC org resolution: user linked by (iss, sub); on first login the verified
email's domain must match an orgs.domain row, else 403 'no org for domain'.
OIDC users default to role 'viewer'.

Mounted by api/server.py:
    from api.identity import router as identity_router
    app.include_router(identity_router)
"""

from __future__ import annotations

import os
import secrets
import threading
import time
from urllib.parse import urlencode

import httpx
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from api import auth as _auth  # BU_AUTH_SECRET / TTL; auth does NOT import us at module level

BOOTSTRAP_ORG_ID = "org-demo"   # seeded by migrations/004
ROLES = ("admin", "sme", "viewer")

SESSION_ALGO = "HS256"
STATE_TTL_S = 600               # OIDC state/nonce validity: 10 minutes
_STATE_AUD = "bu-oidc-state"    # aud claim keeps state JWTs unusable as sessions
_ID_TOKEN_ALGOS = ["RS256", "RS384", "RS512", "ES256", "ES384", "PS256"]

# ── Env (validated at import — P0 fail-loud style) ──────────────────────────

OIDC_ISSUER        = os.environ.get("OIDC_ISSUER", "").strip()
OIDC_CLIENT_ID     = os.environ.get("OIDC_CLIENT_ID", "").strip()
OIDC_CLIENT_SECRET = os.environ.get("OIDC_CLIENT_SECRET", "")
OIDC_REDIRECT_URL  = os.environ.get("OIDC_REDIRECT_URL", "").strip()

if OIDC_ISSUER:
    _missing = [name for name, val in (
        ("OIDC_CLIENT_ID", OIDC_CLIENT_ID),
        ("OIDC_CLIENT_SECRET", OIDC_CLIENT_SECRET),
        ("OIDC_REDIRECT_URL", OIDC_REDIRECT_URL),
    ) if not val]
    if _missing:
        raise RuntimeError(
            "Refusing to start: OIDC_ISSUER is set but required OIDC env "
            "var(s) unset: " + ", ".join(_missing)
            + ". Set them all, or unset OIDC_ISSUER to disable OIDC "
            "(local + legacy logins keep working without it)."
        )


def _bootstrap_env() -> tuple[str, str] | None:
    """(email, password) when both set, None when both unset; partial raises."""
    email = os.environ.get("BU_BOOTSTRAP_ADMIN_EMAIL", "").strip()
    password = os.environ.get("BU_BOOTSTRAP_ADMIN_PASSWORD", "")
    if not email and not password:
        return None
    if not (email and password):
        missing = "BU_BOOTSTRAP_ADMIN_PASSWORD" if email else "BU_BOOTSTRAP_ADMIN_EMAIL"
        raise RuntimeError(
            f"Refusing to start: {missing} unset while its counterpart is "
            "set. Set both BU_BOOTSTRAP_ADMIN_EMAIL and "
            "BU_BOOTSTRAP_ADMIN_PASSWORD, or neither."
        )
    return email.lower(), password


_bootstrap_env()  # fail loudly at import on partial env


# ── Password hashing (argon2id) ─────────────────────────────────────────────

_hasher = PasswordHasher()  # argon2id, library-default parameters


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(pw_hash: str, password: str) -> bool:
    try:
        return _hasher.verify(pw_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


# ── Session JWTs — claims {sub, org_id, role, exp} ──────────────────────────

def mint_session(user: dict, ttl_s: int | None = None) -> str:
    """Issue a session JWT for a users row (dict with id/org_id/role)."""
    exp = int(time.time()) + (ttl_s or _auth.AUTH_TTL_S)
    claims = {
        "sub": user["id"],
        "org_id": user["org_id"],
        "role": user["role"],
        "exp": exp,
    }
    return jwt.encode(claims, _auth.AUTH_SECRET, algorithm=SESSION_ALGO)


def verify_session(token: str) -> dict | None:
    """Return the session claims when `token` is a valid, unexpired org JWT.

    None for anything else (legacy HMAC tokens, state tokens, garbage) —
    api.auth.verify_token() then falls back to the legacy verifier.
    """
    if not token or token.count(".") != 2:  # fast path: not a JWT at all
        return None
    try:
        claims = jwt.decode(token, _auth.AUTH_SECRET, algorithms=[SESSION_ALGO])
    except jwt.InvalidTokenError:
        return None
    if not all(claims.get(k) for k in ("sub", "org_id", "role")):
        return None
    if claims["role"] not in ROLES:
        return None
    return claims


# ── DB helpers (users/orgs — migrations/004; users.user_id is the id) ───────

_USER_COLS = ("user_id, display_name, created_at, org_id, email, role, "
              "oidc_iss, oidc_sub, pw_hash")


def _db():
    from atp import db
    return db


_MIGRATED = False


def _ensure_db() -> None:
    """Idempotent lazy migration (same pattern as atp/store.py)."""
    global _MIGRATED
    if not _MIGRATED:
        _db().run_migrations()
        _MIGRATED = True


def _to_user(row: dict) -> dict:
    user = dict(row)
    user["id"] = user.pop("user_id")
    return user


def get_user_by_email(email: str) -> dict | None:
    rows = _db().query(
        f"SELECT {_USER_COLS} FROM users WHERE email = :email",
        {"email": email.strip().lower()},
    )
    return _to_user(rows[0]) if rows else None


def get_user_by_oidc(iss: str, sub: str) -> dict | None:
    rows = _db().query(
        f"SELECT {_USER_COLS} FROM users"
        " WHERE oidc_iss = :iss AND oidc_sub = :sub",
        {"iss": iss, "sub": sub},
    )
    return _to_user(rows[0]) if rows else None


def get_org_by_domain(domain: str) -> dict | None:
    rows = _db().query(
        "SELECT id, name, domain, created_at FROM orgs"
        " WHERE domain IS NOT NULL AND lower(domain) = lower(:domain)",
        {"domain": domain},
    )
    return dict(rows[0]) if rows else None


def create_user(*, email: str, org_id: str, role: str,
                oidc_iss: str | None = None, oidc_sub: str | None = None,
                pw_hash: str | None = None,
                display_name: str | None = None) -> dict:
    """Insert an identity user; returns the created (or racing-winner) row."""
    if role not in ROLES:
        raise ValueError(f"role must be one of {ROLES}, got {role!r}")
    email = email.strip().lower()
    try:
        _db().execute(
            "INSERT INTO users (user_id, display_name, created_at, org_id,"
            " email, role, oidc_iss, oidc_sub, pw_hash)"
            " VALUES (:id, :name, :ts, :org, :email, :role, :iss, :sub, :pw)",
            {
                "id": "u-" + secrets.token_hex(8),
                "name": display_name or email,
                "ts": time.time(),  # users.created_at is REAL (001)
                "org": org_id,
                "email": email,
                "role": role,
                "iss": oidc_iss,
                "sub": oidc_sub,
                "pw": pw_hash,
            },
        )
    except Exception:
        # Unique-email race: another worker inserted first — use theirs.
        existing = get_user_by_email(email)
        if existing is None:
            raise
        return existing
    user = get_user_by_email(email)
    assert user is not None
    return user


def link_user_oidc(user_id: str, iss: str, sub: str) -> None:
    _db().execute(
        "UPDATE users SET oidc_iss = :iss, oidc_sub = :sub"
        " WHERE user_id = :id",
        {"iss": iss, "sub": sub, "id": user_id},
    )


# ── Bootstrap admin (local fallback account, org-demo) ──────────────────────

def provision_bootstrap_admin() -> dict | None:
    """Create the BU_BOOTSTRAP_ADMIN_* local admin in org-demo if absent.

    Returns the user row (existing or created), or None when the env pair is
    unset. Partial env = RuntimeError (P0 fail-loud style). Idempotent.
    """
    pair = _bootstrap_env()
    if pair is None:
        return None
    email, password = pair
    _ensure_db()
    existing = get_user_by_email(email)
    if existing is not None:
        return existing
    return create_user(
        email=email,
        org_id=BOOTSTRAP_ORG_ID,
        role="admin",
        pw_hash=hash_password(password),
        display_name="Bootstrap admin",
    )


_READY = False
_READY_LOCK = threading.Lock()


def _ensure_ready() -> None:
    """Migrations + bootstrap provisioning, once per process, thread-safe."""
    global _READY
    if _READY:
        return
    with _READY_LOCK:
        if _READY:
            return
        _ensure_db()
        provision_bootstrap_admin()
        _READY = True


# ── OIDC — discovery, JWKS, signed state ────────────────────────────────────

_DISCOVERY_TTL_S = 3600
_discovery_cache: dict = {}
_jwks_clients: dict[str, jwt.PyJWKClient] = {}


def oidc_enabled() -> bool:
    return bool(OIDC_ISSUER)


def _discovery() -> dict:
    """Fetch (and cache) the issuer's openid-configuration."""
    now = time.time()
    if _discovery_cache.get("cfg") and now - _discovery_cache["fetched"] < _DISCOVERY_TTL_S:
        return _discovery_cache["cfg"]
    url = OIDC_ISSUER.rstrip("/") + "/.well-known/openid-configuration"
    try:
        resp = httpx.get(url, timeout=10.0)
        resp.raise_for_status()
        cfg = resp.json()
    except httpx.HTTPError as e:
        raise HTTPException(502, f"OIDC discovery failed: {e.__class__.__name__}") from e
    for key in ("authorization_endpoint", "token_endpoint", "jwks_uri", "issuer"):
        if key not in cfg:
            raise HTTPException(502, f"OIDC discovery document missing {key!r}")
    _discovery_cache.update(cfg=cfg, fetched=now)
    return cfg


def _jwks_client(jwks_uri: str) -> jwt.PyJWKClient:
    client = _jwks_clients.get(jwks_uri)
    if client is None:
        client = jwt.PyJWKClient(jwks_uri, cache_keys=True)
        _jwks_clients[jwks_uri] = client
    return client


def _mint_state(nonce: str) -> str:
    """Signed CSRF state, 10 min TTL. aud keeps it unusable as a session."""
    claims = {"aud": _STATE_AUD, "nonce": nonce,
              "exp": int(time.time()) + STATE_TTL_S}
    return jwt.encode(claims, _auth.AUTH_SECRET, algorithm=SESSION_ALGO)


def _verify_state(state: str) -> dict | None:
    if not state:
        return None
    try:
        return jwt.decode(state, _auth.AUTH_SECRET,
                          algorithms=[SESSION_ALGO], audience=_STATE_AUD)
    except jwt.InvalidTokenError:
        return None


# ── Routes ──────────────────────────────────────────────────────────────────

router = APIRouter()


def _public_user(user: dict) -> dict:
    return {"id": user["id"], "email": user["email"],
            "org_id": user["org_id"], "role": user["role"]}


class LoginBody(BaseModel):
    email: str
    password: str


@router.post("/auth/login")
def local_login(body: LoginBody):
    """Local-account login → session JWT with {sub, org_id, role, exp}."""
    _ensure_ready()
    user = get_user_by_email(body.email)
    ok = (user is not None and user.get("pw_hash")
          and verify_password(user["pw_hash"], body.password))
    if not ok:
        time.sleep(0.25)  # match legacy /login: slow credential stuffing
        raise HTTPException(401, "invalid credentials")
    return {"token": mint_session(user), "user": _public_user(user)}


@router.get("/auth/oidc/login")
def oidc_login():
    """Redirect to the IdP's authorization endpoint (code flow)."""
    if not oidc_enabled():
        raise HTTPException(404, "Not Found")
    cfg = _discovery()
    nonce = secrets.token_urlsafe(16)
    params = {
        "response_type": "code",
        "client_id": OIDC_CLIENT_ID,
        "redirect_uri": OIDC_REDIRECT_URL,
        "scope": "openid email profile",
        "state": _mint_state(nonce),
        "nonce": nonce,
    }
    return RedirectResponse(
        cfg["authorization_endpoint"] + "?" + urlencode(params),
        status_code=302,
    )


@router.get("/auth/oidc/callback")
def oidc_callback(code: str = "", state: str = "", error: str = "",
                  error_description: str = ""):
    """Exchange the code, verify the id_token, provision/link, mint session."""
    if not oidc_enabled():
        raise HTTPException(404, "Not Found")
    _ensure_ready()
    if error:
        raise HTTPException(400, f"OIDC error: {error} {error_description}".strip())
    st = _verify_state(state)
    if st is None:
        raise HTTPException(400, "invalid or expired state")
    if not code:
        raise HTTPException(400, "missing code")

    cfg = _discovery()
    try:
        resp = httpx.post(
            cfg["token_endpoint"],
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": OIDC_REDIRECT_URL,
                "client_id": OIDC_CLIENT_ID,
                "client_secret": OIDC_CLIENT_SECRET,
            },
            timeout=10.0,
        )
        resp.raise_for_status()
        id_token = resp.json().get("id_token", "")
    except httpx.HTTPError as e:
        raise HTTPException(502, f"OIDC token exchange failed: {e.__class__.__name__}") from e
    if not id_token:
        raise HTTPException(502, "OIDC token response had no id_token")

    try:
        signing_key = _jwks_client(cfg["jwks_uri"]).get_signing_key_from_jwt(id_token)
        claims = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=_ID_TOKEN_ALGOS,
            audience=OIDC_CLIENT_ID,
            issuer=cfg["issuer"],
            leeway=30,
        )
    except jwt.PyJWKClientError as e:
        raise HTTPException(502, f"OIDC JWKS fetch failed: {e.__class__.__name__}") from e
    except jwt.InvalidTokenError:
        raise HTTPException(401, "invalid id_token")
    if claims.get("nonce") != st["nonce"]:
        raise HTTPException(401, "nonce mismatch")

    iss, sub = claims["iss"], claims["sub"]
    user = get_user_by_oidc(iss, sub)
    if user is None:
        email = (claims.get("email") or "").strip().lower()
        if not email:
            raise HTTPException(403, "id_token has no email claim")
        if claims.get("email_verified") is False:
            raise HTTPException(403, "email not verified by identity provider")
        existing = get_user_by_email(email)
        if existing is not None:
            # Same verified email as an existing account → link identities.
            link_user_oidc(existing["id"], iss, sub)
            user = get_user_by_email(email)
        else:
            domain = email.split("@", 1)[1]
            org = get_org_by_domain(domain)
            if org is None:
                raise HTTPException(403, "no org for domain")
            user = create_user(
                email=email,
                org_id=org["id"],
                role="viewer",  # OIDC default; org admins promote later
                oidc_iss=iss,
                oidc_sub=sub,
                display_name=claims.get("name") or email,
            )
    return {"token": mint_session(user), "user": _public_user(user)}
