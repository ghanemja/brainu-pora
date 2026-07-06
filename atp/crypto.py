"""
Envelope encryption for T2 ("crown jewels") columns — docs/TENANCY.md.

Key model (leak surface #10 — one key must not unlock all orgs):

  * Master key: `DATA_ENCRYPTION_KEY` env var, read at CALL time (never at
    import). Any high-entropy string; its utf-8 bytes are the HKDF input key
    material. Only ever supplied via env — never stored in the repo or DB.
  * Per-org subkey: HKDF-SHA256(master, info=org_id) → 32 bytes → urlsafe-b64
    → Fernet key. Deterministic, so no key table is needed; compromise of one
    derived key does not reveal the master or any sibling org's key.
  * Rotation (re-wrap): stand up the new master alongside the old
    (`DATA_ENCRYPTION_KEY_OLD` by operator convention), then for each T2 row:
    decrypt with the old master's per-org subkey, encrypt with the new one,
    write back. `enc1:` is the version tag — a future algorithm/rotation
    scheme bumps to `enc2:` so mixed-version tables stay readable.

Wire format: `'enc1:' + Fernet token` stored in TEXT columns. Values WITHOUT
the prefix are legacy plaintext and read through unchanged — decryption of
legacy rows never requires a key, so pre-encryption databases keep working.

Fail-loud: encrypting anything, or decrypting an `enc1:` token, without
`DATA_ENCRYPTION_KEY` raises RuntimeError immediately (no silent plaintext
writes, no silent empty reads). A token that fails authentication (tampered,
or decrypted under the wrong org's subkey) raises ValueError.

Public:
  encrypt_for_org(org_id, data)        -> 'enc1:…' str  (data: bytes or str)
  decrypt_for_org(org_id, value)       -> bytes | None  (plaintext passthrough)
  decrypt_text_for_org(org_id, value)  -> str | None    (utf-8 convenience)
  is_encrypted(value)                  -> bool
"""

from __future__ import annotations

import base64
import os
import threading

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

ENC_PREFIX = "enc1:"

_LOCK = threading.Lock()
# (master_bytes, org_id) -> Fernet. Keyed by master so tests / rotation that
# change the env var never serve a stale subkey.
_FERNET_CACHE: dict[tuple[bytes, str], Fernet] = {}


def _master() -> bytes:
    """Return the master key bytes, failing loudly when encryption was
    requested but no key is configured."""
    key = os.environ.get("DATA_ENCRYPTION_KEY", "")
    if not key.strip():
        raise RuntimeError(
            "DATA_ENCRYPTION_KEY is not set but an encrypt/decrypt of T2 "
            "data was requested. Refusing to continue (docs/TENANCY.md data "
            "class T2). Set DATA_ENCRYPTION_KEY in the deployment "
            "environment (see .env.example); legacy plaintext values still "
            "read through without it."
        )
    return key.strip().encode("utf-8")


def _fernet_for_org(org_id: str) -> Fernet:
    """Per-org Fernet from HKDF-SHA256(master, info=org_id)."""
    if not org_id or not isinstance(org_id, str):
        raise ValueError("org_id must be a non-empty string")
    master = _master()
    cache_key = (master, org_id)
    f = _FERNET_CACHE.get(cache_key)
    if f is None:
        with _LOCK:
            f = _FERNET_CACHE.get(cache_key)
            if f is None:
                derived = HKDF(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,  # HKDF treats absent salt as zeros — fine:
                                # uniqueness comes from info=org_id
                    info=org_id.encode("utf-8"),
                ).derive(master)
                f = Fernet(base64.urlsafe_b64encode(derived))
                _FERNET_CACHE[cache_key] = f
    return f


def is_encrypted(value: str | bytes | None) -> bool:
    """True when `value` carries the enc1 envelope prefix."""
    if isinstance(value, bytes):
        return value.startswith(ENC_PREFIX.encode("ascii"))
    if isinstance(value, str):
        return value.startswith(ENC_PREFIX)
    return False


def encrypt_for_org(org_id: str, data: bytes | str) -> str:
    """Encrypt `data` under `org_id`'s subkey → 'enc1:<fernet token>'.

    Fails loudly (RuntimeError) when DATA_ENCRYPTION_KEY is unset — callers
    must never fall back to writing plaintext for T2 fields.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    if not isinstance(data, bytes):
        raise TypeError(f"encrypt_for_org expects bytes or str, got {type(data).__name__}")
    token = _fernet_for_org(org_id).encrypt(data)
    return ENC_PREFIX + token.decode("ascii")


def decrypt_for_org(org_id: str, value: str | bytes | None) -> bytes | None:
    """Decrypt an 'enc1:' envelope; pass legacy plaintext through as bytes.

    * None → None.
    * 'enc1:…' → decrypted bytes (RuntimeError without a key; ValueError if
      the token is tampered with or belongs to a different org's subkey).
    * anything else → returned unchanged as bytes (str is utf-8 encoded):
      pre-encryption rows keep reading without DATA_ENCRYPTION_KEY.
    """
    if value is None:
        return None
    if not is_encrypted(value):
        return value.encode("utf-8") if isinstance(value, str) else bytes(value)
    token = value[len(ENC_PREFIX):] if isinstance(value, str) else value[len(ENC_PREFIX):].decode("ascii")
    try:
        return _fernet_for_org(org_id).decrypt(token.encode("ascii") if isinstance(token, str) else token)
    except InvalidToken:
        raise ValueError(
            f"enc1 token failed to decrypt under org {org_id!r}: wrong org "
            "subkey, wrong master key, or tampered ciphertext"
        ) from None


def decrypt_text_for_org(org_id: str, value: str | bytes | None) -> str | None:
    """decrypt_for_org, decoded as utf-8 (T2 columns are TEXT)."""
    out = decrypt_for_org(org_id, value)
    return None if out is None else out.decode("utf-8")
