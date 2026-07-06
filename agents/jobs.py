"""
Lightweight background job queue.

Heavy work (podcast/video render, local TTS) should not block the HTTP
request — it can take 30-120s. This runs such work on a bounded in-process
thread pool and tracks status in the shared database so any request — on any
instance — can poll it.

The fn itself still executes in the submitting process (the closure can't
cross instances), but every status transition is a guarded UPDATE
(`WHERE job_id = :id AND status = :expected`), so with multiple instances
sharing one database a job can never be claimed or double-transitioned
twice. For fully distributed execution, swap the executor for Redis/RQ —
the public API (submit / get) stays the same.

Public:
  submit(kind, fn, *args, org_id="org-demo", **kwargs) -> job_id
  get(job_id, org_id="org-demo") -> dict | None     # status + result/error

Job dict:
  {job_id, kind, status: queued|running|done|error,
   result: <json>|None, error: str|None, created_at, updated_at}

The fn's return value MUST be JSON-serializable (dicts/lists/str/num).

Tenancy (Phase 2, docs/TENANCY.md leak surface #2): `jobs` is a tenant table
(migration 005 — org_id column, Postgres RLS deny-by-default), so ALL access
goes through the atp/tenant_db.py scoped helpers, never raw atp.db
query()/execute(). Every row carries the submitting org's id: `org_id` is
consumed by submit() itself (NOT forwarded to fn) and MUST come from the
verified request state. get() only sees rows belonging to the org it is
called with — the /jobs route in api/server.py turns a cross-tenant miss
into the same 404 as an unknown id.

Env:
  BU_JOB_WORKERS — thread-pool size (default 2; Render is RAM/CPU heavy,
                   keep concurrency low so the box doesn't OOM).
"""

from __future__ import annotations

import json
import os
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor

from atp import tenant_db
from atp.tenant_db import DEFAULT_ORG

from .persistence import ensure_schema

ensure_schema()  # jobs table lives in migrations/001_core (+ org_id in 005)

_EXECUTOR = ThreadPoolExecutor(
    max_workers=int(os.environ.get("BU_JOB_WORKERS", "2")),
    thread_name_prefix="bu-job",
)


def _transition(job_id: str, org_id: str, *, expect: str, to: str,
                result=None, error: str | None = None) -> bool:
    """Move a job expect→to atomically. True iff THIS call made the change.

    The `status = :expect` guard means a second worker/instance racing on
    the same row loses (rowcount 0) instead of overwriting the winner.
    """
    res = tenant_db.scoped_execute(
        org_id,
        """UPDATE jobs
              SET status = :to, result = :result, error = :error,
                  updated_at = :now
            WHERE job_id = :job_id AND status = :expect
              AND org_id = :org""",
        {"to": to,
         "result": json.dumps(result) if result is not None else None,
         "error": error, "now": time.time(),
         "job_id": job_id, "expect": expect, "org": org_id},
    )
    return res.rowcount > 0


def submit(kind: str, fn, *args, org_id: str = DEFAULT_ORG, **kwargs) -> str:
    """Enqueue fn(*args, **kwargs) to run in the background. Returns job_id.

    org_id tags the row with the submitting tenant (docs/TENANCY.md); it is
    consumed here and never forwarded to fn.
    """
    org_id = org_id or DEFAULT_ORG
    job_id = "job_" + uuid.uuid4().hex[:12]
    now = time.time()
    tenant_db.insert_scoped("jobs", {
        "job_id": job_id, "kind": kind, "status": "queued",
        "created_at": now, "updated_at": now,
    }, org_id)

    def _run():
        if not _transition(job_id, org_id, expect="queued", to="running"):
            return  # already claimed elsewhere — never run the same job twice
        try:
            result = fn(*args, **kwargs)
            _transition(job_id, org_id, expect="running", to="done", result=result)
        except Exception as e:  # noqa: BLE001 — capture everything for the poller
            _transition(
                job_id, org_id, expect="running", to="error",
                error=f"{type(e).__name__}: {e}\n{traceback.format_exc()[-1500:]}",
            )

    _EXECUTOR.submit(_run)
    return job_id


def get(job_id: str, org_id: str = DEFAULT_ORG) -> dict | None:
    """Return the job's current status dict, or None if unknown.

    Org-scoped: a job belonging to another org is indistinguishable from a
    nonexistent one (None) — no cross-tenant existence oracle (TENANCY.md #6).
    """
    rows = tenant_db.scoped_query(
        org_id or DEFAULT_ORG,
        """SELECT job_id, kind, status, result, error, created_at, updated_at
             FROM jobs WHERE job_id = :job_id AND org_id = :org""",
        {"job_id": job_id, "org": org_id or DEFAULT_ORG},
    )
    if not rows:
        return None
    row = rows[0]
    return {
        "job_id":     row["job_id"],
        "kind":       row["kind"],
        "status":     row["status"],
        "result":     json.loads(row["result"]) if row["result"] else None,
        "error":      row["error"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
