"""
Lightweight background job queue.

Heavy work (podcast/video render, local TTS) should not block the HTTP
request — it can take 30-120s. This runs such work on a bounded in-process
thread pool and tracks status in the shared database (atp.db) so any
request — on any instance — can poll it.

The fn itself still executes in the submitting process (the closure can't
cross instances), but every status transition is a guarded UPDATE
(`WHERE job_id = :id AND status = :expected`), so with multiple instances
sharing one database a job can never be claimed or double-transitioned
twice. For fully distributed execution, swap the executor for Redis/RQ —
the public API (submit / get) stays the same.

Public:
  submit(kind, fn, *args, **kwargs) -> job_id      # runs fn in background
  get(job_id) -> dict | None                        # status + result/error

Job dict:
  {job_id, kind, status: queued|running|done|error,
   result: <json>|None, error: str|None, created_at, updated_at}

The fn's return value MUST be JSON-serializable (dicts/lists/str/num).

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

from atp import db

from .persistence import ensure_schema

ensure_schema()  # jobs table lives in migrations/001_core

_EXECUTOR = ThreadPoolExecutor(
    max_workers=int(os.environ.get("BU_JOB_WORKERS", "2")),
    thread_name_prefix="bu-job",
)


def _transition(job_id: str, *, expect: str, to: str,
                result=None, error: str | None = None) -> bool:
    """Move a job expect→to atomically. True iff THIS call made the change.

    The `status = :expect` guard means a second worker/instance racing on
    the same row loses (rowcount 0) instead of overwriting the winner.
    """
    res = db.execute(
        """UPDATE jobs
              SET status = :to, result = :result, error = :error,
                  updated_at = :now
            WHERE job_id = :job_id AND status = :expect""",
        {"to": to,
         "result": json.dumps(result) if result is not None else None,
         "error": error, "now": time.time(),
         "job_id": job_id, "expect": expect},
    )
    return res.rowcount > 0


def submit(kind: str, fn, *args, **kwargs) -> str:
    """Enqueue fn(*args, **kwargs) to run in the background. Returns job_id."""
    job_id = "job_" + uuid.uuid4().hex[:12]
    now = time.time()
    db.execute(
        """INSERT INTO jobs (job_id, kind, status, created_at, updated_at)
           VALUES (:job_id, :kind, 'queued', :created_at, :updated_at)""",
        {"job_id": job_id, "kind": kind, "created_at": now, "updated_at": now},
    )

    def _run():
        if not _transition(job_id, expect="queued", to="running"):
            return  # already claimed elsewhere — never run the same job twice
        try:
            result = fn(*args, **kwargs)
            _transition(job_id, expect="running", to="done", result=result)
        except Exception as e:  # noqa: BLE001 — capture everything for the poller
            _transition(
                job_id, expect="running", to="error",
                error=f"{type(e).__name__}: {e}\n{traceback.format_exc()[-1500:]}",
            )

    _EXECUTOR.submit(_run)
    return job_id


def get(job_id: str) -> dict | None:
    """Return the job's current status dict, or None if unknown."""
    rows = db.query(
        """SELECT job_id, kind, status, result, error, created_at, updated_at
             FROM jobs WHERE job_id = :job_id""",
        {"job_id": job_id},
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
