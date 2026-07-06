"""
DB access layer — SQLAlchemy Core engine, tiny SQL helpers, migration runner.

One engine per process (module-level singleton), configured by env:

  DATABASE_URL     — full SQLAlchemy URL. Unset → SQLite (see below).
                     Postgres: postgresql+psycopg2://user:pass@host:5432/db
                     (bare postgres:// / postgresql:// URLs, as handed out by
                     Render/Heroku, are normalized to the psycopg2 driver).
  BRAIN_DB         — SQLite path used when DATABASE_URL is unset
                     (default data/brain_university.db; parent dir created).
  BU_DB_POOL_SIZE  — Postgres pool size (default 5; max_overflow fixed at 5).

Public:
  get_engine() -> Engine             lazy singleton
  is_postgres() -> bool              True when the engine talks to Postgres
  query(sql, params) -> list[dict]   SELECTs; named params (:name), both dialects
  execute(sql, params) -> ExecResult (.rowcount, .lastrowid)
  run_migrations() -> list[str]      apply pending migrations/ files (idempotent)
  reset_engine()                     dispose the singleton (tests / env changes)

Writing SQL that works on BOTH dialects:
  * Bind values with SQLAlchemy named params (:name) — never string-format
    values into SQL. `query`/`execute` wrap the SQL in sqlalchemy.text().
  * For INSERT ids, append `RETURNING <id_col>` — both Postgres and SQLite
    >= 3.35 (Python 3.11's bundled build) support it, and `execute()` surfaces
    the first returned column as `.lastrowid`. Plain INSERTs also populate
    `.lastrowid` on SQLite; on Postgres use RETURNING.

Migrations live in migrations/ as `NNN_name[.pg|.sqlite].sql`. For a given
base name (`NNN_name`) the file suffixed with the current dialect wins over
the plain `.sql` one. Applied base names are tracked in `schema_migrations`;
each file is applied inside a single transaction, so a failed migration
leaves the DB untouched (Postgres; SQLite DDL is best-effort transactional).

Statement-separator convention (also documented at the top of each migration
file): a line containing only `--;;` splits the file into statements — needed
because trigger bodies contain ';'. Files without any `--;;` line are split
on plain ';'.
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import NamedTuple

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.pool import NullPool

PROJECT_ROOT = Path(__file__).parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / "migrations"
DEFAULT_SQLITE_DB = PROJECT_ROOT / "data" / "brain_university.db"

STATEMENT_MARKER = "--;;"

_ENGINE: Engine | None = None


class ExecResult(NamedTuple):
    """Outcome of a write statement.

    rowcount  — rows affected (UPDATE/DELETE; driver-dependent for INSERT).
    lastrowid — SQLite: rowid of the last INSERT. Postgres: only populated
                when the statement uses RETURNING (first column of the first
                returned row) — RETURNING also works on SQLite >= 3.35, so
                `INSERT ... RETURNING id` is the portable way to get new ids.
    """

    rowcount: int
    lastrowid: int | None


# ── Engine ──────────────────────────────────────────────────────────────────

def _database_url() -> str:
    url = os.environ.get("DATABASE_URL", "").strip()
    if url:
        # Render/Heroku hand out postgres:// — SQLAlchemy 2.x needs the
        # explicit driver segment.
        if url.startswith("postgres://"):
            url = "postgresql+psycopg2://" + url[len("postgres://"):]
        elif url.startswith("postgresql://"):
            url = "postgresql+psycopg2://" + url[len("postgresql://"):]
        return url
    # No DATABASE_URL → SQLite. Honour BRAIN_DB (already set by Dockerfile /
    # render.yaml) so deployments keep pointing at the same file as before.
    path = Path(os.environ.get("BRAIN_DB") or DEFAULT_SQLITE_DB)
    return f"sqlite:///{path}"


def get_engine() -> Engine:
    """Return the process-wide engine, creating it on first use."""
    global _ENGINE
    if _ENGINE is None:
        url = make_url(_database_url())
        if url.get_backend_name() == "sqlite":
            if url.database and url.database != ":memory:":
                Path(url.database).parent.mkdir(parents=True, exist_ok=True)
            # NullPool + check_same_thread=False: FastAPI serves requests on
            # a thread pool; a fresh short-lived connection per operation is
            # the safe pattern for SQLite.
            _ENGINE = create_engine(
                url,
                poolclass=NullPool,
                connect_args={"check_same_thread": False},
            )
        else:
            _ENGINE = create_engine(
                url,
                pool_pre_ping=True,   # survive dropped/idle-closed connections
                pool_size=int(os.environ.get("BU_DB_POOL_SIZE", "5")),
                max_overflow=5,
            )
    return _ENGINE


def is_postgres() -> bool:
    return get_engine().dialect.name == "postgresql"


def reset_engine() -> None:
    """Dispose the singleton so the next call rebuilds it from env (tests)."""
    global _ENGINE
    if _ENGINE is not None:
        _ENGINE.dispose()
        _ENGINE = None


# ── SQL helpers ─────────────────────────────────────────────────────────────

def query(sql: str, params: dict | None = None) -> list[dict]:
    """Run a SELECT (named params `:name`) and return rows as list[dict]."""
    with get_engine().connect() as conn:
        rows = conn.execute(text(sql), params or {}).mappings().all()
        return [dict(r) for r in rows]


def execute(sql: str, params: dict | None = None) -> ExecResult:
    """Run a write statement in its own transaction. See ExecResult."""
    with get_engine().begin() as conn:
        result = conn.execute(text(sql), params or {})
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
        return ExecResult(rowcount=result.rowcount, lastrowid=lastrowid)


# ── Migrations ──────────────────────────────────────────────────────────────

# NNN_name.sql | NNN_name.pg.sql | NNN_name.sqlite.sql
_MIGRATION_RE = re.compile(r"^(?P<base>\d+_\w+?)(?:\.(?P<dialect>pg|sqlite))?\.sql$")


def run_migrations() -> list[str]:
    """Apply every unapplied migration file, in order. Returns applied names.

    Idempotent: applied base names are recorded in schema_migrations, so a
    second call is a no-op. Each migration runs in a single transaction
    together with its schema_migrations bookkeeping row.
    """
    engine = get_engine()
    with engine.begin() as conn:
        conn.exec_driver_sql(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "  name       TEXT PRIMARY KEY,"
            "  applied_at DOUBLE PRECISION NOT NULL"
            ")"
        )
    already = {r["name"] for r in query("SELECT name FROM schema_migrations")}

    applied: list[str] = []
    for base, path in _discover_migrations():
        if base in already:
            continue
        statements = _split_statements(path.read_text())
        with engine.begin() as conn:
            # Raw DBAPI cursor, no parameters: exec_driver_sql() hands the
            # driver an (empty) params object, which makes psycopg2 run its
            # %-interpolation over the SQL — any literal '%' in a migration
            # (e.g. plpgsql RAISE '%' placeholders in 002_atp.pg.sql) then
            # raises TypeError. cursor.execute(sql) with no params skips
            # interpolation entirely, on both drivers.
            cursor = conn.connection.cursor()
            try:
                for stmt in statements:
                    cursor.execute(stmt)
            finally:
                cursor.close()
            conn.execute(
                text("INSERT INTO schema_migrations (name, applied_at)"
                     " VALUES (:name, :ts)"),
                {"name": base, "ts": time.time()},
            )
        applied.append(base)
    return applied


def _discover_migrations() -> list[tuple[str, Path]]:
    """Return [(base_name, path)] sorted by base name.

    For each base name, the file suffixed with the current dialect
    (.pg.sql / .sqlite.sql) is preferred over the shared .sql one. A base
    that only ships the OTHER dialect's file is an error — migrations must
    cover whichever dialect the deployment runs on.
    """
    if not MIGRATIONS_DIR.is_dir():
        return []
    dialect = "pg" if is_postgres() else "sqlite"
    by_base: dict[str, dict[str | None, Path]] = {}
    for p in MIGRATIONS_DIR.iterdir():
        m = _MIGRATION_RE.match(p.name)
        if not m:
            continue
        by_base.setdefault(m.group("base"), {})[m.group("dialect")] = p

    out: list[tuple[str, Path]] = []
    for base in sorted(by_base):
        files = by_base[base]
        path = files.get(dialect) or files.get(None)
        if path is None:
            raise RuntimeError(
                f"migration {base!r} has no file for dialect {dialect!r} "
                f"(found: {sorted(p.name for p in files.values())})"
            )
        out.append((base, path))
    return out


def _split_statements(sql: str) -> list[str]:
    """Split migration SQL into individual statements.

    If the file contains any line that is exactly `--;;`, those lines are the
    only separators (lets trigger/function bodies keep their internal ';').
    Otherwise the file is split on top-level ';' — ignoring ';' inside `--`
    line comments, `/* */` block comments, and 'quoted strings'. Files with
    BEGIN...END trigger bodies or $$-quoted function bodies MUST use the
    marker. Chunks that are empty or comment-only are dropped.
    """
    lines = sql.splitlines()
    if any(line.strip() == STATEMENT_MARKER for line in lines):
        chunks: list[str] = []
        current: list[str] = []
        for line in lines:
            if line.strip() == STATEMENT_MARKER:
                chunks.append("\n".join(current))
                current = []
            else:
                current.append(line)
        chunks.append("\n".join(current))
    else:
        chunks = _split_on_semicolons(sql)

    statements: list[str] = []
    for chunk in chunks:
        meaningful = "\n".join(
            line for line in chunk.splitlines()
            if line.strip() and not line.strip().startswith("--")
        )
        if meaningful.strip():
            statements.append(chunk.strip())
    return statements


def _split_on_semicolons(sql: str) -> list[str]:
    """Split on ';' outside comments and string literals (both dialects)."""
    chunks: list[str] = []
    buf: list[str] = []
    i, n = 0, len(sql)
    while i < n:
        two = sql[i:i + 2]
        if two == "--":  # line comment — runs to end of line
            j = sql.find("\n", i)
            j = n if j == -1 else j
            buf.append(sql[i:j])
            i = j
        elif two == "/*":  # block comment
            j = sql.find("*/", i + 2)
            j = n if j == -1 else j + 2
            buf.append(sql[i:j])
            i = j
        elif sql[i] == "'":  # string literal ('' is the escaped quote)
            j = i + 1
            while j < n:
                if sql[j] == "'":
                    if sql[j + 1:j + 2] == "'":
                        j += 2
                        continue
                    break
                j += 1
            j = min(j + 1, n)
            buf.append(sql[i:j])
            i = j
        elif sql[i] == ";":
            chunks.append("".join(buf))
            buf = []
            i += 1
        else:
            buf.append(sql[i])
            i += 1
    chunks.append("".join(buf))
    return chunks
