"""
Org-scoped DAL — enforcement layer 2 of docs/TENANCY.md (Phase 2).

Tenant tables (atp_hitl, atp_requests, atp_evidence, atp_cert_awards, jobs,
access_log) must be read/written EXCLUSIVELY through the helpers here — never
through raw atp.db query()/execute() from routes (convention + CI grep, per
TENANCY.md layer 2).

What the helpers enforce:

  * Scope validation (both dialects): any statement that mentions a tenant
    table must (a) bind an `:org` parameter in its SQL and (b) pass
    params['org'] equal to the org_id argument — otherwise TenantScopeError.
    The check is a deliberately SIMPLE parse (word-boundary table-name match);
    false positives (a tenant table named in a string literal) just demand an
    `:org` bind, never weaker scoping.
  * Postgres (layer 3): every statement runs inside a transaction that first
    executes `SELECT set_config('app.org_id', :org, true)` — the exact
    equivalent of `SET LOCAL app.org_id` but bind-parameter safe. Migration
    005 enables FORCE ROW LEVEL SECURITY with policy
    `USING (org_id = current_setting('app.org_id', true))`, so a transaction
    that skips this wrapper sees ZERO tenant rows (deny by default — there is
    intentionally no permissive fallback when the setting is absent).
  * SQLite (dev/demo): no RLS — the `WHERE org_id = :org` the validation
    forces into every statement IS the isolation (layers 1-2 only,
    documented gap).

The org_id passed in must come from the verified JWT (route layer) — never
from a request body or query string.

Public:
  scoped_query(org_id, sql, params)   -> list[dict]   (SELECTs)
  scoped_execute(org_id, sql, params) -> db.ExecResult (writes)
  insert_scoped(table, row, org_id)   -> db.ExecResult (row['org_id'] forced)
  log_access(org_id, user, role, method, path, table, row_count, status)
  TENANT_TABLES, DEFAULT_ORG, TenantScopeError
"""

from __future__ import annotations

import re
import time
from contextlib import contextmanager

from sqlalchemy import text

from atp import db

#: Bootstrap org every pre-tenancy row belongs to (migration 005 default).
DEFAULT_ORG = "org-demo"

#: Tables that carry org_id and may only be touched through this module.
TENANT_TABLES = frozenset({
    "atp_hitl",
    "atp_requests",
    "atp_evidence",
    "atp_cert_awards",
    "jobs",
    "access_log",
})

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# ':org' bind — \b so ':org_id' / ':organization' don't satisfy the check.
_ORG_BIND_RE = re.compile(r":org\b")
_TABLE_RES = {t: re.compile(rf"\b{t}\b", re.IGNORECASE) for t in TENANT_TABLES}


class TenantScopeError(RuntimeError):
    """A statement touched a tenant table without correct org scoping."""


# ── Validation ──────────────────────────────────────────────────────────────

def _require_org(org_id: str) -> str:
    if not org_id or not isinstance(org_id, str):
        raise TenantScopeError("org_id must be a non-empty string")
    return org_id


def _tables_in(sql: str) -> set[str]:
    return {t for t, rx in _TABLE_RES.items() if rx.search(sql)}


def _validate(org_id: str, sql: str, params: dict) -> None:
    """Simple-parse scope check: tenant table named → ':org' bind required
    and params['org'] must equal the org the caller authenticated as."""
    _require_org(org_id)
    touched = _tables_in(sql)
    if not touched:
        return
    if not _ORG_BIND_RE.search(sql):
        raise TenantScopeError(
            f"statement touches tenant table(s) {sorted(touched)} without an "
            f"':org' bind — every tenant-table statement must scope by org "
            f"(docs/TENANCY.md layer 2): {sql!r}"
        )
    if params.get("org") != org_id:
        raise TenantScopeError(
            f"params['org'] ({params.get('org')!r}) does not match the "
            f"authenticated org_id ({org_id!r})"
        )


# ── Scoped connection (PG: SET LOCAL app.org_id) ────────────────────────────

@contextmanager
def _scoped_conn(org_id: str):
    """One transaction with the org GUC pinned (Postgres) — commit on exit.

    set_config(..., is_local=true) == SET LOCAL: the setting dies with the
    transaction, so pooled connections can never leak one org's scope into
    the next request's transaction.
    """
    engine = db.get_engine()
    with engine.begin() as conn:
        if engine.dialect.name == "postgresql":
            conn.execute(
                text("SELECT set_config('app.org_id', :org, true)"),
                {"org": org_id},
            )
        yield conn


# ── Public helpers ──────────────────────────────────────────────────────────

@contextmanager
def scoped_txn(org_id: str):
    """Public multi-statement transaction with the org GUC pinned.

    For callers that must make several reads/writes ATOMICALLY (e.g. the
    evidence-chain append in atp/signing.py, which reads the chain head and
    inserts under it). Yields the SQLAlchemy connection; commit on exit,
    rollback on exception. Statement-level :org validation is the caller's
    responsibility inside the block — Postgres RLS remains the backstop.
    """
    _require_org(org_id)
    with _scoped_conn(org_id) as conn:
        yield conn


def scoped_query(org_id: str, sql: str, params: dict | None = None) -> list[dict]:
    """Org-scoped SELECT. Named params (:name); returns rows as list[dict]."""
    params = dict(params or {})
    _validate(org_id, sql, params)
    with _scoped_conn(org_id) as conn:
        rows = conn.execute(text(sql), params).mappings().all()
        return [dict(r) for r in rows]


def scoped_execute(org_id: str, sql: str, params: dict | None = None) -> db.ExecResult:
    """Org-scoped write. Same ExecResult contract as atp.db.execute()."""
    params = dict(params or {})
    _validate(org_id, sql, params)
    with _scoped_conn(org_id) as conn:
        result = conn.execute(text(sql), params)
        lastrowid: int | None = None
        if result.returns_rows:  # INSERT ... RETURNING <id> (both dialects)
            row = result.first()
            if row is not None:
                lastrowid = row[0]
        else:
            try:
                lastrowid = result.lastrowid  # meaningful on SQLite
            except Exception:  # noqa: BLE001 — drivers without lastrowid
                lastrowid = None
        return db.ExecResult(rowcount=result.rowcount, lastrowid=lastrowid)


def insert_scoped(table: str, row: dict, org_id: str) -> db.ExecResult:
    """INSERT `row` into tenant `table` with org_id forced to the caller's
    org (any org_id already present in `row` is overwritten — the verified
    org always wins over payload-supplied values)."""
    _require_org(org_id)
    if table not in TENANT_TABLES:
        raise TenantScopeError(
            f"insert_scoped only handles tenant tables {sorted(TENANT_TABLES)}, "
            f"got {table!r} — use atp.db.execute() for non-tenant tables"
        )
    row = dict(row)
    row["org_id"] = org_id
    for col in row:
        if not _IDENT_RE.match(col):
            raise TenantScopeError(f"invalid column name {col!r}")
    cols = ", ".join(row)
    marks = ", ".join(f":{c}" for c in row)
    with _scoped_conn(org_id) as conn:
        result = conn.execute(
            text(f"INSERT INTO {table} ({cols}) VALUES ({marks})"), row)
        try:
            lastrowid = result.lastrowid
        except Exception:  # noqa: BLE001
            lastrowid = None
        return db.ExecResult(rowcount=result.rowcount, lastrowid=lastrowid)


def log_access(org_id: str, user: str, role: str, method: str, path: str,
               table: str | None = None, row_count: int = 0,
               status: int = 200) -> None:
    """Append one audit row to access_log (TENANCY.md layer 4).

    access_log is append-only (triggers, migration 004) and itself org-scoped
    under RLS (migration 005), so the insert goes through the scoped path.
    Column names follow 004's schema and avoid reserved words: the `user`
    argument → column `user_id`, `table` → column `target_table`.
    """
    insert_scoped("access_log", {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_id": user,
        "role": role,
        "method": method,
        "path": path,
        "target_table": table,
        "row_count": int(row_count),
        "status": int(status),
    }, org_id)
