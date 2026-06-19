"""
Lightweight background job queue.

Heavy work (podcast/video render, local TTS) should not block the HTTP
request — it can take 30-120s. This runs such work on a bounded thread pool
and tracks status in SQLite so any request can poll it.

In-process + single-instance by design (matches a single Render web service).
For multi-instance horizontal scaling, swap the store for Redis/RQ — the
public API (submit / get) stays the same.

Public:
  submit(kind, fn, *args, **kwargs) -> job_id      # runs fn in background
  get(job_id) -> dict | None                        # status + result/error

Job dict:
  {job_id, kind, status: queued|running|done|error,
   result: <json>|None, error: str|None, created_at, updated_at}

The fn's return value MUST be JSON-serializable (dicts/lists/str/num).
"""

from __future__ import annotations

import json
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor

from .persistence import open_db

# Render is RAM/CPU heavy — keep concurrency low so the box doesn't OOM.
_EXECUTOR = ThreadPoolExecutor(max_workers=2, thread_name_prefix="bu-job")


def _ensure_table(db) -> None:
    db.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
          job_id     TEXT PRIMARY KEY,
          kind       TEXT NOT NULL,
          status     TEXT NOT NULL,
          result     TEXT,
          error      TEXT,
          created_at REAL NOT NULL,
          updated_at REAL NOT NULL
        )
    """)


def _set(job_id: str, *, status: str, result=None, error: str | None = None) -> None:
    db = open_db()
    _ensure_table(db)
    db.execute(
        """UPDATE jobs SET status=?, result=?, error=?, updated_at=?
             WHERE job_id=?""",
        (status,
         json.dumps(result) if result is not None else None,
         error, time.time(), job_id),
    )
    db.commit()


def submit(kind: str, fn, *args, **kwargs) -> str:
    """Enqueue fn(*args, **kwargs) to run in the background. Returns job_id."""
    job_id = "job_" + uuid.uuid4().hex[:12]
    now = time.time()
    db = open_db()
    _ensure_table(db)
    db.execute(
        """INSERT INTO jobs (job_id, kind, status, created_at, updated_at)
           VALUES (?, ?, 'queued', ?, ?)""",
        (job_id, kind, now, now),
    )
    db.commit()

    def _run():
        _set(job_id, status="running")
        try:
            result = fn(*args, **kwargs)
            _set(job_id, status="done", result=result)
        except Exception as e:  # noqa: BLE001 — capture everything for the poller
            _set(job_id, status="error",
                 error=f"{type(e).__name__}: {e}\n{traceback.format_exc()[-1500:]}")

    _EXECUTOR.submit(_run)
    return job_id


def get(job_id: str) -> dict | None:
    """Return the job's current status dict, or None if unknown."""
    db = open_db()
    _ensure_table(db)
    row = db.execute(
        """SELECT job_id, kind, status, result, error, created_at, updated_at
             FROM jobs WHERE job_id=?""",
        (job_id,),
    ).fetchone()
    if not row:
        return None
    return {
        "job_id":     row[0],
        "kind":       row[1],
        "status":     row[2],
        "result":     json.loads(row[3]) if row[3] else None,
        "error":      row[4],
        "created_at": row[5],
        "updated_at": row[6],
    }
