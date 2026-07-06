"""
Agent licensing — issue / verify / revoke / meter (Phase 4, docs/HARDENING.md).

Licenses are T1 org-scoped data (docs/TENANCY.md): every read/write goes
through atp/tenant_db.py (org from the verified request principal, NEVER from
a payload), and on Postgres migration 006 adds FORCE row-level security with
the 005 policy pattern. Stripe is OPTIONAL by design: without STRIPE_API_KEY
the platform still issues 'manual' licenses (design partners pay by invoice)
— stripe_customer/stripe_subscription stay NULL and gating/metering/
revocation work identically. Stripe only adds self-serve checkout on top.

License-key format (shown ONCE at issue time; only key_id is persisted):

    atpk_<key_id>.<sig>
    key_id = 24 hex chars (secrets.token_hex(12))
    sig    = HMAC-SHA256(LICENSE_SIGNING_KEY, key_id) hex, first 32 chars

Verification model — the key alone NEVER suffices:

    check_license() first verifies the HMAC in constant time (cheap, no DB
    hit for forged keys), then loads the row by key_id and enforces
    status == 'active' AND (expires_at IS NULL OR in the future). Revocation
    and expiry are DB STATE — a revoked/expired row fails on the very next
    call regardless of a validly signed key. Rows whose expires_at has passed
    are auto-flipped to status='expired' on check (`licenses` is mutable by
    design; `usage_events` + the atp_evidence chain are the append-only
    billing/audit record).

Key resolution (mirrors atp/signing.py, fail-loud):

    LICENSE_SIGNING_KEY       required whenever keys are issued/verified with
                              auth enabled — LicenseSigningKeyError if unset.
    BU_AUTH_DISABLED=1 (dev)  fallback: derive a stable key from
                              BU_AUTH_SECRET when set, else a process-
                              ephemeral random key with a loud warning
                              (keys then don't verify across restarts).

Public:
    issue_license(org_id, agent_id, kind, expires_at=None,
                  stripe_customer=None, stripe_subscription=None)
                                        -> {license, licenseKey}
    check_license(license_key)          -> {ok, license?, reason?}
    revoke_license(org_id, license_id, reason) -> license dict (idempotent)
    record_usage(org_id, license_id, agent_id, endpoint,
                 tokens_in, tokens_out, status) -> usage-event dict
    usage_summary(org_id, license_id=None)
                                        -> {calls, tokensIn, tokensOut, byAgent}
    list_licenses(org_id)               -> [license dict] latest-first

Returned license dicts are camelCase and NEVER contain key material: the
secret half of the key is not stored anywhere; `keyId` (the public identifier
half, useless without LICENSE_SIGNING_KEY) is included so an admin can match
a key in hand to its row. Like atp/store.py, returned dicts do not grow an
org key.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import sys
import time
import uuid
from datetime import datetime, timezone

from sqlalchemy import text

from atp import db, store, tenant_db

#: License-key prefix (public, greppable — like Stripe's sk_/pk_).
KEY_PREFIX = "atpk_"

#: Hex chars of the HMAC kept in the key (128 bits of the 256-bit MAC).
_SIG_LEN = 32

#: Domain-separation tag for the BU_AUTH_SECRET-derived dev key — distinct
#: from atp/signing.py's tag so evidence and license keys never share a key.
_DERIVE_TAG = b"bu-license-signing-v1:"

VALID_KINDS = frozenset({"evaluation", "production"})

_EPHEMERAL_KEY: bytes | None = None
_WARNED = False
_MIGRATIONS_DONE = False


class LicensingError(RuntimeError):
    """Base class for licensing failures."""


class LicenseSigningKeyError(LicensingError):
    """Key issue/verify was requested but no usable signing key is set."""


class UnknownAgentError(LicensingError):
    """agent_id does not exist in the marketplace seed."""


class AgentNotLicensableError(LicensingError):
    """Agent exists but its seed says licensing.available is false."""


class LicenseNotFoundError(LicensingError):
    """No license with that id is visible to the caller's org."""


# ── Signing key (mirrors atp/signing.py) ────────────────────────────────────

def _signing_key() -> bytes:
    """Resolve the HMAC key (see module docstring for the precedence)."""
    global _EPHEMERAL_KEY, _WARNED
    key = os.environ.get("LICENSE_SIGNING_KEY", "").strip()
    if key:
        return key.encode("utf-8")

    if os.environ.get("BU_AUTH_DISABLED", "") == "1":
        # Dev mode: never block the loop, but never sign with a hardcoded
        # default either — derive from the auth secret when one exists.
        auth_secret = os.environ.get("BU_AUTH_SECRET", "").strip()
        if auth_secret:
            return hashlib.sha256(_DERIVE_TAG + auth_secret.encode("utf-8")).digest()
        if _EPHEMERAL_KEY is None:
            _EPHEMERAL_KEY = secrets.token_bytes(32)
        if not _WARNED:
            _WARNED = True
            print(
                "WARNING: LICENSE_SIGNING_KEY unset (BU_AUTH_DISABLED=1 dev "
                "mode) — signing license keys with a process-EPHEMERAL key. "
                "Issued keys will NOT verify after a restart. Set "
                "LICENSE_SIGNING_KEY (see .env.example).",
                file=sys.stderr,
            )
        return _EPHEMERAL_KEY

    raise LicenseSigningKeyError(
        "LICENSE_SIGNING_KEY is not set. License-key signing is mandatory "
        "when auth is enabled (docs/HARDENING.md Phase 4) — generate one with "
        "python3 -c \"import secrets; print(secrets.token_hex(32))\" and "
        "export it, or export BU_AUTH_DISABLED=1 for local dev only."
    )


def _key_sig(key_id: str) -> str:
    """Secret half of a license key: truncated hex HMAC-SHA256 over key_id."""
    return hmac.new(
        _signing_key(), key_id.encode("utf-8"), hashlib.sha256
    ).hexdigest()[:_SIG_LEN]


def _parse_key(license_key) -> tuple[str, str] | None:
    """Split 'atpk_<key_id>.<sig>' → (key_id, sig); None when malformed."""
    if not isinstance(license_key, str) or not license_key.startswith(KEY_PREFIX):
        return None
    key_id, dot, sig = license_key[len(KEY_PREFIX):].partition(".")
    if not dot or not key_id or not sig:
        return None
    return key_id, sig


# ── Row plumbing ─────────────────────────────────────────────────────────────

# camelCase API key ↔ snake_case column; declaration order = SELECT order.
_LICENSE_COLS = {
    "id": "id",
    "agentId": "agent_id",
    "kind": "kind",
    "status": "status",
    "keyId": "key_id",           # public identifier half only — never secret
    "createdAt": "created_at",
    "expiresAt": "expires_at",
    "revokedAt": "revoked_at",
    "revokedReason": "revoked_reason",
    "stripeCustomer": "stripe_customer",
    "stripeSubscription": "stripe_subscription",
    "seats": "seats",
}
_LICENSE_SELECT = ", ".join(_LICENSE_COLS.values())


def _to_camel(row: dict) -> dict:
    """Map a licenses row to the public camelCase shape (org_id dropped —
    same convention as atp/store.py: returned dicts don't grow an org key)."""
    return {camel: row.get(col) for camel, col in _LICENSE_COLS.items()}


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _parse_ts(value) -> datetime | None:
    """ISO-8601 → aware UTC datetime; None when unparseable."""
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc)
    except ValueError:
        pass
    try:
        dt = datetime.fromisoformat(value)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _ensure_migrations() -> None:
    """Lazily apply pending migrations once per process (idempotent — the
    startup run stays authoritative; this covers direct library use/tests)."""
    global _MIGRATIONS_DONE
    if not _MIGRATIONS_DONE:
        db.run_migrations()
        _MIGRATIONS_DONE = True


def _load_by_key_id(key_id: str) -> dict | None:
    """Load one licenses row by key_id — the key-based lookup path.

    check_license() authenticates by license KEY, not by org (the caller of
    the gated proxy may be a machine holding only the key); the org comes
    FROM the row. On Postgres the `key_lookup` SELECT policy (migration 006)
    makes exactly this one row visible after pinning the verified key_id:
        SELECT set_config('app.license_key_id', :kid, true)   -- == SET LOCAL
    in the same transaction. Writes still require the org GUC, so everything
    that follows (expiry flip, metering) goes back through atp/tenant_db.py
    scoped to the row's org.
    """
    engine = db.get_engine()
    with engine.begin() as conn:
        if engine.dialect.name == "postgresql":
            conn.execute(
                text("SELECT set_config('app.license_key_id', :kid, true)"),
                {"kid": key_id},
            )
        row = conn.execute(
            text(f"SELECT org_id, {_LICENSE_SELECT} FROM licenses "
                 "WHERE key_id = :kid"),
            {"kid": key_id},
        ).mappings().first()
        return dict(row) if row else None


# ── Public API ───────────────────────────────────────────────────────────────

def issue_license(org_id: str, agent_id: str, kind: str,
                  expires_at: str | None = None,
                  stripe_customer: str | None = None,
                  stripe_subscription: str | None = None) -> dict:
    """Issue a license for a marketplace agent to `org_id`.

    Returns {"license": <camelCase dict>, "licenseKey": "atpk_..."} — the
    licenseKey is shown exactly ONCE here; only its key_id half is stored.
    Manual (invoice-billed) licenses simply pass no stripe_* values.

    Raises UnknownAgentError / AgentNotLicensableError when the agent is not
    in the seed or its seed licensing says available=false; ValueError on a
    bad kind or unparseable expires_at.
    """
    agent = next(
        (a for a in store.get_data()["AGENTS"] if a.get("id") == agent_id),
        None)
    if agent is None:
        raise UnknownAgentError(f"unknown agent {agent_id!r}")
    if not (agent.get("licensing") or {}).get("available"):
        raise AgentNotLicensableError(
            f"agent {agent_id!r} is not available for licensing")
    if kind not in VALID_KINDS:
        raise ValueError(
            f"kind must be one of {sorted(VALID_KINDS)}, got {kind!r}")
    if expires_at is not None and _parse_ts(expires_at) is None:
        raise ValueError(
            f"expires_at must be ISO-8601 UTC ('%Y-%m-%dT%H:%M:%SZ'), "
            f"got {expires_at!r}")

    _ensure_migrations()
    key_id = secrets.token_hex(12)  # 96 bits; UNIQUE constraint is backstop
    license_key = f"{KEY_PREFIX}{key_id}.{_key_sig(key_id)}"
    row = {
        "id": f"lic-{uuid.uuid4().hex[:12]}",
        "agent_id": agent_id,
        "kind": kind,
        "status": "active",
        "key_id": key_id,
        "created_at": _now_iso(),
        "expires_at": expires_at,
        "revoked_at": None,
        "revoked_reason": None,
        "stripe_customer": stripe_customer,
        "stripe_subscription": stripe_subscription,
        "seats": 1,
    }
    tenant_db.scoped_execute(
        org_id,
        "INSERT INTO licenses "
        "  (id, org_id, agent_id, kind, status, key_id, created_at, "
        "   expires_at, revoked_at, revoked_reason, stripe_customer, "
        "   stripe_subscription, seats) "
        "VALUES (:id, :org, :agent_id, :kind, :status, :key_id, :created_at, "
        "        :expires_at, :revoked_at, :revoked_reason, :stripe_customer, "
        "        :stripe_subscription, :seats)",
        {"org": org_id, **row},
    )
    return {"license": _to_camel(row), "licenseKey": license_key}


def check_license(license_key) -> dict:
    """Verify a presented license key. -> {ok, license?, reason?}

    Order of enforcement:
      1. parse — malformed keys fail without touching the signing key or DB;
      2. constant-time HMAC verify (hmac.compare_digest) — forged keys fail
         without a DB hit;
      3. DB state — the row must exist, have status 'active', and not be past
         expires_at. Revoked/expired rows fail REGARDLESS of a valid
         signature: revocation is DB state, the key alone never suffices.
    Rows expired by date but still marked 'active' are flipped to 'expired'
    here (scoped to the row's own org).

    reason ∈ {'malformed', 'invalid-signature', 'unknown', 'revoked',
    'expired'}; on success the license dict is returned (no key material).
    """
    parsed = _parse_key(license_key)
    if parsed is None:
        return {"ok": False, "reason": "malformed"}
    key_id, sig = parsed
    expected = _key_sig(key_id)
    if not hmac.compare_digest(expected.encode("utf-8"), sig.encode("utf-8")):
        return {"ok": False, "reason": "invalid-signature"}

    _ensure_migrations()
    row = _load_by_key_id(key_id)
    if row is None:
        return {"ok": False, "reason": "unknown"}
    if row["status"] == "revoked":
        return {"ok": False, "reason": "revoked"}

    expires = _parse_ts(row.get("expires_at")) if row.get("expires_at") else None
    past_expiry = row.get("expires_at") is not None and (
        expires is None  # unparseable date in DB → fail safe (deny)
        or expires <= datetime.now(timezone.utc))
    if row["status"] == "expired" or past_expiry:
        if row["status"] == "active":
            # Auto-transition: expiry-by-date becomes durable DB state.
            # `licenses` is mutable by design (only usage/evidence are
            # append-only); guard on status for concurrent checks.
            tenant_db.scoped_execute(
                row["org_id"],
                "UPDATE licenses SET status = 'expired' "
                "WHERE org_id = :org AND id = :id AND status = 'active'",
                {"org": row["org_id"], "id": row["id"]},
            )
        return {"ok": False, "reason": "expired"}

    return {"ok": True, "license": _to_camel(row)}


def revoke_license(org_id: str, license_id: str, reason: str) -> dict:
    """Revoke a license (idempotent). Returns the camelCase license dict.

    Org-scoped: a license belonging to another org is simply not visible, so
    cross-org revocation raises LicenseNotFoundError. Takes effect on the
    very next check_license() call — the gate re-reads DB state every time.
    """
    _ensure_migrations()
    rows = tenant_db.scoped_query(
        org_id,
        f"SELECT {_LICENSE_SELECT} FROM licenses "
        "WHERE org_id = :org AND id = :id",
        {"org": org_id, "id": license_id},
    )
    if not rows:
        raise LicenseNotFoundError(
            f"no license {license_id!r} in org {org_id!r}")
    row = rows[0]
    if row["status"] == "revoked":
        return _to_camel(row)  # already revoked — idempotent no-op
    row["status"] = "revoked"
    row["revoked_at"] = _now_iso()
    row["revoked_reason"] = str(reason or "")
    tenant_db.scoped_execute(
        org_id,
        "UPDATE licenses SET status = 'revoked', revoked_at = :ts, "
        "revoked_reason = :reason WHERE org_id = :org AND id = :id",
        {"org": org_id, "id": license_id,
         "ts": row["revoked_at"], "reason": row["revoked_reason"]},
    )
    return _to_camel(row)


def reissue_key(org_id: str, license_id: str) -> dict:
    """Mint a NEW key for an existing ACTIVE license (old key stops working
    immediately — key_id is replaced, and check_license resolves by key_id).

    The in-product delivery path for Stripe self-serve licenses, whose
    webhook-issued plaintext key is discarded by design: an org admin
    re-issues and hands the fresh key to the customer. Returns
    {"license": ..., "licenseKey": ...}; the key appears exactly ONCE here.
    """
    _ensure_migrations()
    rows = tenant_db.scoped_query(
        org_id,
        f"SELECT {_LICENSE_SELECT} FROM licenses "
        "WHERE org_id = :org AND id = :id",
        {"org": org_id, "id": license_id},
    )
    if not rows:
        raise LicenseNotFoundError(
            f"no license {license_id!r} in org {org_id!r}")
    if rows[0]["status"] != "active":
        raise ValueError(
            f"only active licenses can be re-keyed "
            f"(status is {rows[0]['status']!r})")
    key_id = secrets.token_hex(12)
    license_key = f"{KEY_PREFIX}{key_id}.{_key_sig(key_id)}"
    tenant_db.scoped_execute(
        org_id,
        "UPDATE licenses SET key_id = :key_id "
        "WHERE org_id = :org AND id = :id",
        {"org": org_id, "id": license_id, "key_id": key_id},
    )
    rows[0]["key_id"] = key_id
    return {"license": _to_camel(rows[0]), "licenseKey": license_key}


def record_usage(org_id: str, license_id: str | None, agent_id: str,
                 endpoint: str, tokens_in: int, tokens_out: int,
                 status: str) -> dict:
    """Append one metering row to usage_events (append-only billing evidence).

    Returns the camelCase event including its row id.
    """
    _ensure_migrations()
    event = {
        "ts": _now_iso(),
        "license_id": license_id,
        "agent_id": agent_id,
        "endpoint": endpoint,
        "tokens_in": int(tokens_in or 0),
        "tokens_out": int(tokens_out or 0),
        "status": str(status),
    }
    result = tenant_db.scoped_execute(
        org_id,
        "INSERT INTO usage_events "
        "  (ts, org_id, license_id, agent_id, endpoint, tokens_in, "
        "   tokens_out, status) "
        "VALUES (:ts, :org, :license_id, :agent_id, :endpoint, :tokens_in, "
        "        :tokens_out, :status) "
        "RETURNING id",
        {"org": org_id, **event},
    )
    return {
        "id": result.lastrowid,
        "ts": event["ts"],
        "licenseId": license_id,
        "agentId": agent_id,
        "endpoint": endpoint,
        "tokensIn": event["tokens_in"],
        "tokensOut": event["tokens_out"],
        "status": event["status"],
    }


def usage_summary(org_id: str, license_id: str | None = None) -> dict:
    """Aggregate an org's metering rows (optionally for one license).

    -> {calls, tokensIn, tokensOut, byAgent: {agentId: {calls, tokensIn,
    tokensOut}}}. Values are plain ints on both dialects.
    """
    _ensure_migrations()
    sql = (
        "SELECT agent_id, COUNT(*) AS calls, "
        "       COALESCE(SUM(tokens_in), 0) AS tokens_in, "
        "       COALESCE(SUM(tokens_out), 0) AS tokens_out "
        "FROM usage_events WHERE org_id = :org"
    )
    params: dict = {"org": org_id}
    if license_id is not None:
        sql += " AND license_id = :license_id"
        params["license_id"] = license_id
    sql += " GROUP BY agent_id"
    by_agent: dict[str, dict] = {}
    totals = {"calls": 0, "tokensIn": 0, "tokensOut": 0}
    for r in tenant_db.scoped_query(org_id, sql, params):
        entry = {
            "calls": int(r["calls"]),
            "tokensIn": int(r["tokens_in"]),      # PG SUM → Decimal
            "tokensOut": int(r["tokens_out"]),
        }
        by_agent[r["agent_id"] or ""] = entry
        totals["calls"] += entry["calls"]
        totals["tokensIn"] += entry["tokensIn"]
        totals["tokensOut"] += entry["tokensOut"]
    return {**totals, "byAgent": by_agent}


def list_licenses(org_id: str) -> list[dict]:
    """All of `org_id`'s licenses, latest-first, camelCase — never any key
    material (only keyId, the public identifier half)."""
    _ensure_migrations()
    rows = tenant_db.scoped_query(
        org_id,
        f"SELECT {_LICENSE_SELECT} FROM licenses WHERE org_id = :org "
        "ORDER BY created_at DESC, id DESC",
        {"org": org_id},
    )
    return [_to_camel(r) for r in rows]
