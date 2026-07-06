"""
Evidence signing — HMAC-SHA256 over canonical payloads, per-org hash chain.

Phase 3 (docs/HARDENING.md): every evidence row written by atp/exams.py is
signed so the append-only tables (migration 002 triggers) become
tamper-EVIDENT, not just append-only:

    sig       = HMAC-SHA256(key, prev_hash || canonical(payload))
    prev_hash = sig of the previous atp_evidence row for the SAME org
                ('genesis' for an org's first row)

Editing any historical payload breaks that row's sig; deleting or reordering
rows breaks the prev_hash linkage — verify_chain() catches both.

Key resolution (fail-loud, mirrors api/auth.py's posture):

    EVIDENCE_SIGNING_KEY      required whenever signing/verification happens
                              with auth enabled — RuntimeError if unset.
    BU_AUTH_DISABLED=1 (dev)  fallback: derive a stable key from
                              BU_AUTH_SECRET when set, else a process-
                              ephemeral random key with a loud warning
                              (sigs then don't verify across restarts).

Public:
    canonical(payload) -> bytes           stable JSON bytes (sorted keys,
                                          no whitespace drift)
    sign(payload, prev_hash) -> str       hex HMAC-SHA256
    verify_row(row) -> bool               recompute + constant-time compare
    last_sig(org_id) -> str               chain head for an org ('genesis'
                                          when the org has no evidence yet)
    verify_chain(org_id) -> dict          {ok, length, first_bad} walking
                                          atp_evidence in id order (org-scoped
                                          via atp/tenant_db.py)
    GENESIS                               the chain-root sentinel string
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import sys
import threading

from sqlalchemy import text

from atp import db, tenant_db

#: prev_hash sentinel for the first evidence row of an org's chain.
GENESIS = "genesis"

#: Domain-separation tag for the BU_AUTH_SECRET-derived dev key.
_DERIVE_TAG = b"bu-evidence-signing-v1:"

_EPHEMERAL_KEY: bytes | None = None
_WARNED = False


class SigningKeyError(RuntimeError):
    """Signing was requested but no usable key is configured."""


def _signing_key() -> bytes:
    """Resolve the HMAC key (see module docstring for the precedence)."""
    global _EPHEMERAL_KEY, _WARNED
    key = os.environ.get("EVIDENCE_SIGNING_KEY", "").strip()
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
                "WARNING: EVIDENCE_SIGNING_KEY unset (BU_AUTH_DISABLED=1 dev "
                "mode) — signing evidence with a process-EPHEMERAL key. "
                "Signatures will NOT verify after a restart. Set "
                "EVIDENCE_SIGNING_KEY (see .env.example).",
                file=sys.stderr,
            )
        return _EPHEMERAL_KEY

    raise SigningKeyError(
        "EVIDENCE_SIGNING_KEY is not set. Evidence signing is mandatory when "
        "auth is enabled (docs/HARDENING.md Phase 3) — generate one with "
        "python3 -c \"import secrets; print(secrets.token_hex(32))\" and "
        "export it, or export BU_AUTH_DISABLED=1 for local dev only."
    )


# ── Canonicalisation + signing ───────────────────────────────────────────────

def canonical(payload: dict) -> bytes:
    """Stable byte serialisation of a payload dict.

    json.dumps with sorted keys, compact separators, and ensure_ascii=True:
    key order, whitespace, and non-ASCII escaping can never drift between the
    signer and a later verifier (including across Python versions).
    """
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def sign(payload: dict, prev_hash: str) -> str:
    """Hex HMAC-SHA256 over prev_hash || canonical(payload)."""
    msg = (prev_hash or GENESIS).encode("utf-8") + canonical(payload)
    return hmac.new(_signing_key(), msg, hashlib.sha256).hexdigest()


def verify_row(row: dict) -> bool:
    """Recompute a row's sig from its stored payload + prev_hash.

    `row` needs keys payload (JSON text or dict), sig, prev_hash — i.e. an
    atp_evidence row as returned by the DAL. Constant-time compare.
    """
    payload = row.get("payload")
    if isinstance(payload, (str, bytes)):
        try:
            payload = json.loads(payload)
        except (ValueError, TypeError):
            return False
    if not isinstance(payload, dict):
        return False
    expected = sign(payload, row.get("prev_hash") or GENESIS)
    return hmac.compare_digest(expected, str(row.get("sig") or ""))


# ── Chain access (org-scoped, via the tenant DAL only) ──────────────────────

def last_sig(org_id: str) -> str:
    """Current chain head for an org: sig of its newest evidence row,
    or GENESIS when the org has no evidence yet."""
    rows = tenant_db.scoped_query(
        org_id,
        "SELECT sig FROM atp_evidence WHERE org_id = :org "
        "ORDER BY id DESC LIMIT 1",
        {"org": org_id},
    )
    return rows[0]["sig"] if rows and rows[0].get("sig") else GENESIS


# ── Serialized chain append (the ONLY sanctioned way to write evidence) ─────

_CHAIN_LOCKS: dict[str, threading.Lock] = {}
_CHAIN_LOCKS_GUARD = threading.Lock()


def _chain_lock(org_id: str) -> threading.Lock:
    with _CHAIN_LOCKS_GUARD:
        return _CHAIN_LOCKS.setdefault(org_id, threading.Lock())


def append_chain(org_id: str, records: list[dict]) -> list[tuple[int, str]]:
    """Append `records` to an org's evidence chain atomically, in order.

    records: [{ts, agent_id, cert_id, kind, payload(dict)}, ...]
    returns: [(row_id, sig), ...] in the same order.

    Why this exists: the chain head (prev_hash) must be read and written
    under mutual exclusion or two concurrent exam runs interleave and
    permanently fork the ledger. Serialization is layered:
      - per-org threading.Lock — serializes writers within one process
        (the jobs pool runs multiple worker threads);
      - Postgres: pg_advisory_xact_lock(hashtext(org)) inside the same
        transaction — serializes across processes AND instances;
      - SQLite: single-file DB, and multi-process SQLite is already
        unsupported (Dockerfile: WORKERS>1 requires Postgres).
    The whole batch is one transaction, so an exam's evidence lands
    all-or-nothing — no partially signed runs on crash.
    """
    out: list[tuple[int, str]] = []
    with _chain_lock(org_id):
        with tenant_db.scoped_txn(org_id) as conn:
            if db.is_postgres():
                conn.execute(
                    text("SELECT pg_advisory_xact_lock(hashtext(:org))"),
                    {"org": org_id},
                )
            row = conn.execute(
                text("SELECT sig FROM atp_evidence WHERE org_id = :org "
                     "ORDER BY id DESC LIMIT 1"),
                {"org": org_id},
            ).first()
            prev = row[0] if row and row[0] else GENESIS
            for rec in records:
                sig = sign(rec["payload"], prev)
                r = conn.execute(
                    text("INSERT INTO atp_evidence "
                         "  (ts, agent_id, cert_id, kind, payload, sig, "
                         "   prev_hash, org_id) "
                         "VALUES (:ts, :agent_id, :cert_id, :kind, :payload, "
                         "        :sig, :prev_hash, :org) "
                         "RETURNING id"),
                    {
                        "ts": rec["ts"],
                        "agent_id": rec["agent_id"],
                        "cert_id": rec["cert_id"],
                        "kind": rec["kind"],
                        "payload": canonical(rec["payload"]).decode("utf-8"),
                        "sig": sig,
                        "prev_hash": prev,
                        "org": org_id,
                    },
                ).first()
                out.append((r[0], sig))
                prev = sig
    return out


def verify_chain(org_id: str) -> dict:
    """Walk an org's whole evidence chain in id order.

    Returns {ok: bool, length: int, first_bad: int | None} where first_bad is
    the id of the first row whose sig doesn't verify OR whose prev_hash
    doesn't equal the previous row's sig (GENESIS for the first row).
    """
    rows = tenant_db.scoped_query(
        org_id,
        "SELECT id, payload, sig, prev_hash FROM atp_evidence "
        "WHERE org_id = :org ORDER BY id ASC",
        {"org": org_id},
    )
    prev = GENESIS
    for row in rows:
        if (row.get("prev_hash") or GENESIS) != prev or not verify_row(row):
            return {"ok": False, "length": len(rows), "first_bad": row["id"]}
        prev = row["sig"]
    return {"ok": True, "length": len(rows), "first_bad": None}
