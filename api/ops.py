"""
Runtime ops for the Brain University API — Phase 5 (docs/HARDENING.md).

Three concerns, one middleware (`ops_middleware`) plus one renderer
(`metrics_response` for the /metrics route in api/server.py):

1. RATE LIMITING — in-process token bucket, keyed (client IP, token subject).
   * Env `BU_RATE_LIMIT` = "<requests>/<window_seconds>", default "120/60"
     (120 requests per rolling 60s per key). `BU_RATE_LIMIT=0` disables.
     Malformed values warn to stderr and fall back to the default (an ops
     typo must never boot an unlimited OR a bricked API).
   * The middleware is registered so it runs AFTER auth (see api/server.py):
     request.state.user is already populated, so one NATed office IP full of
     distinct authenticated users doesn't share a single bucket — but an
     unauthenticated scanner (no subject) still collapses to its IP.
   * Over-limit → 429 with a `Retry-After: <seconds>` header (seconds until
     the bucket next holds a full token).
   * Exempt: /health (liveness probes must never 429), /metrics (scrapers),
     and OPTIONS (CORS preflight carries no credentials to key on).
   * Buckets live in a bounded LRU (`MAX_BUCKET_KEYS` = 10k keys, least-
     recently-seen evicted) so hostile key churn can't grow memory unbounded.
   * Client IP is request.client.host — behind a reverse proxy (Render,
     Netlify redirects) that is the proxy's address unless uvicorn runs with
     --proxy-headers (or ProxyHeadersMiddleware) so X-Forwarded-For rewrites
     scope['client']. Without it, all remote clients share one IP and the
     bucket key degrades to per-token-subject — still functional, coarser.
   * SCOPE: single-instance only, by design. Buckets are per-process memory —
     N instances behind a load balancer enforce N×limit, and a restart resets
     all buckets. Good enough for the current single-box Render deploy; for
     multi-instance, swap `TokenBucketLimiter` for a Redis-backed bucket
     (INCR + EXPIRE, or a Lua token bucket) — the middleware contract
     (`acquire(key) -> (allowed, retry_after_s)`) is the seam.
   * BU_AUTH_DISABLED=1 demo mode is untouched: the limiter still runs (it
     needs no auth), keyed on (ip, dev-admin); set BU_RATE_LIMIT=0 to switch
     it off entirely.

2. /metrics — Prometheus text exposition format 0.0.4, HAND-ROLLED on
   purpose: no `prometheus-client` dependency (documented decision — the
   series below are counters/gauges/one histogram with a small fixed label
   set; a registry library buys nothing and requirements.txt is heavy
   enough). Series:
     bu_up 1                                     — process serving requests
     bu_requests_total{method,path,status}       — counter
     bu_request_duration_seconds*{path,status}   — histogram (+_sum/_count)
     bu_rate_limited_total                       — counter (429s issued here)
     bu_jobs{status}                             — gauge, DB, cached 5s
     bu_evidence_chain_length                    — gauge, DB, cached 30s
     bu_licenses{status}                         — gauge, DB, cached 30s
   Label cardinality is BOUNDED: `path` is always the ROUTE TEMPLATE
   (`/atp/evidence/{evidence_id}`, never the raw id), and any path that
   matches no registered route collapses to the single sentinel
   `/_unmatched` — a scanner spraying random URLs cannot mint new series.
   DB-backed gauges query through atp/tenant_db (org-demo scope — cheap
   bootstrap-org aggregates, NOT cross-tenant sums) and every failure is
   swallowed: a broken DB drops those series from the scrape, it never 500s
   /metrics.
   VISIBILITY TRADEOFF: /metrics is added to the auth allowlist by default
   because Prometheus scrapers don't hold bearers and the payload carries no
   tenant data (aggregate counts + route templates only). It DOES leak
   coarse operational shape (traffic volume, error rates, license counts) to
   anyone who can reach the port — set `BU_METRICS_PUBLIC=0` to keep it
   behind the bearer gate and give the scraper a token instead.

3. STRUCTURED REQUEST LOGS — one JSON object per line to stdout:
     {"ts", "method", "path", "status", "ms", "org", "user", "ip"}
   * `path` is the route template (same bounded collapse as metrics).
   * Opt-in via `BU_LOG_JSON=1` (default OFF so `uvicorn --reload` dev logs
     stay human-readable). Read per-request, so tests can flip it.
   * REDACTION BY CONSTRUCTION: the log record is built from the fixed field
     list above — request bodies, query strings, and headers (Authorization,
     X-ATP-License-Key, cookies, ...) are never read by the logger at all.
     Keep it that way: add fields to `_JSON_LOG_FIELDS`, never dump
     request.headers / body. Covered by a redaction test.

Wiring (api/server.py): `app.middleware("http")(ops_middleware)` registered
BETWEEN the access-log middleware and auth_middleware. Starlette runs the
last-registered http middleware first, so the runtime order is
auth → ops → tenant-access-log → CORS → routes: identity is available for
the bucket key, and a 429 short-circuits BEFORE the tenant access log, so a
flood can't amplify into per-request DB writes.
"""

from __future__ import annotations

import json
import math
import os
import sys
import threading
import time
from collections import OrderedDict
from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse, PlainTextResponse

# ── Config ─────────────────────────────────────────────────────────────────

DEFAULT_RATE_LIMIT = "120/60"
MAX_BUCKET_KEYS = 10_000

#: Paths the rate limiter never touches (liveness probes + scrapers).
RATE_LIMIT_EXEMPT_PATHS = frozenset({"/health", "/metrics"})

#: /metrics on the auth allowlist? Default yes — see module docstring
#: tradeoff. BU_METRICS_PUBLIC=0 keeps it behind the bearer gate.
METRICS_PUBLIC = os.environ.get("BU_METRICS_PUBLIC", "1") != "0"

METRICS_CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"

#: The ONLY fields a JSON request-log line may carry (redaction by
#: construction — see module docstring §3).
_JSON_LOG_FIELDS = ("ts", "method", "path", "status", "ms", "org", "user", "ip")


def _log_json_enabled() -> bool:
    """BU_LOG_JSON read per-request: costs ~µs, keeps tests/env flips live."""
    return os.environ.get("BU_LOG_JSON", "") == "1"


# ── Token-bucket rate limiter (bounded LRU of buckets) ─────────────────────

class TokenBucketLimiter:
    """Classic token bucket per key, stored in a size-bounded LRU.

    capacity = `limit` tokens, refilled continuously at limit/window per
    second — a full burst of `limit` is allowed instantly, sustained rate
    converges to limit/window. Single-process scope (module docstring §1).
    """

    def __init__(self, limit: int, window_s: int,
                 max_keys: int = MAX_BUCKET_KEYS):
        if limit <= 0 or window_s <= 0:
            raise ValueError("limit and window must be positive")
        self.limit = limit
        self.window_s = window_s
        self.capacity = float(limit)
        self.rate = limit / window_s          # tokens per second
        self.max_keys = max_keys
        self._buckets: OrderedDict[str, tuple[float, float]] = OrderedDict()
        self._lock = threading.Lock()         # sync routes run off-loop; be safe

    def acquire(self, key: str, now: float | None = None) -> tuple[bool, int]:
        """Try to take one token for `key` → (allowed, retry_after_seconds).

        retry_after is 0 when allowed, else the whole seconds until the
        bucket next holds >= 1 token (what we put in Retry-After).
        """
        if now is None:
            now = time.monotonic()
        with self._lock:
            tokens, last = self._buckets.get(key, (self.capacity, now))
            tokens = min(self.capacity, tokens + (now - last) * self.rate)
            if tokens >= 1.0:
                tokens -= 1.0
                allowed, retry = True, 0
            else:
                allowed = False
                retry = max(1, math.ceil((1.0 - tokens) / self.rate))
            self._buckets[key] = (tokens, now)
            self._buckets.move_to_end(key)
            while len(self._buckets) > self.max_keys:   # bounded memory
                self._buckets.popitem(last=False)       # evict least-recent
            return allowed, retry

    def __len__(self) -> int:
        return len(self._buckets)


def _parse_rate_limit(spec: str) -> tuple[int, int] | None:
    """'120/60' → (120, 60); '0' → None (disabled). Raises on garbage."""
    spec = (spec or "").strip()
    if spec == "0":
        return None
    n, _, w = spec.partition("/")
    limit, window = int(n), int(w)
    if limit <= 0 or window <= 0:
        raise ValueError(spec)
    return limit, window


_LIMITER: TokenBucketLimiter | None = None


def set_rate_limit(spec: str | None = None) -> None:
    """(Re)configure the limiter from `spec`, or from env when None.

    Called once at import; exported so tests (and an ops REPL) can retune
    without reloading the module. Malformed spec → warn + default, never
    crash or silently disable.
    """
    global _LIMITER
    if spec is None:
        spec = os.environ.get("BU_RATE_LIMIT", DEFAULT_RATE_LIMIT)
    try:
        parsed = _parse_rate_limit(spec)
    except (ValueError, TypeError):
        print(f"WARNING: BU_RATE_LIMIT={spec!r} is malformed — expected "
              f"'<requests>/<seconds>' or '0'; using default "
              f"{DEFAULT_RATE_LIMIT!r}.", file=sys.stderr)
        parsed = _parse_rate_limit(DEFAULT_RATE_LIMIT)
    _LIMITER = None if parsed is None else TokenBucketLimiter(*parsed)


set_rate_limit()


# ── Metrics registry (stdlib, one lock, bounded labels) ────────────────────

#: Histogram bucket upper bounds (seconds). +Inf is implicit.
HIST_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)

_KNOWN_METHODS = frozenset(
    {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"})

_METRICS_LOCK = threading.Lock()
_STARTED_AT = time.time()
_REQUESTS: dict[tuple[str, str, int], int] = {}          # (method,path,status)
_HIST: dict[tuple[str, int], list] = {}                   # (path,status) →
#                                                  [bucket_counts, sum, count]
_RATE_LIMITED = 0


def _observe(method: str, path_tmpl: str, status: int, elapsed_s: float) -> None:
    method = method if method in _KNOWN_METHODS else "OTHER"
    rkey = (method, path_tmpl, status)
    hkey = (path_tmpl, status)
    with _METRICS_LOCK:
        _REQUESTS[rkey] = _REQUESTS.get(rkey, 0) + 1
        hist = _HIST.get(hkey)
        if hist is None:
            hist = _HIST[hkey] = [[0] * (len(HIST_BUCKETS) + 1), 0.0, 0]
        counts, _, _ = hist
        for i, le in enumerate(HIST_BUCKETS):
            if elapsed_s <= le:
                counts[i] += 1
        counts[-1] += 1                                    # +Inf
        hist[1] += elapsed_s
        hist[2] += 1


def _count_rate_limited() -> None:
    global _RATE_LIMITED
    with _METRICS_LOCK:
        _RATE_LIMITED += 1


# ── Path templating (bounded label set) ────────────────────────────────────

_ROUTE_TABLE: list | None = None


def _path_template(request: Request) -> str:
    """Collapse the raw path to its route template, else '/_unmatched'.

    Fast path: FastAPI puts the matched route in request.scope['route'].
    Fallback (unrouted: 429 short-circuits, 404s, OPTIONS): match against
    every registered route's compiled path_regex — one-time table build.
    Everything that matches nothing shares ONE sentinel label so arbitrary
    client paths can never mint new series.
    """
    route = request.scope.get("route")
    fmt = getattr(route, "path_format", None)
    if fmt:
        return fmt
    global _ROUTE_TABLE
    if _ROUTE_TABLE is None:
        table = []
        for r in request.app.routes:      # fully registered before 1st request
            rx = getattr(r, "path_regex", None)
            f = getattr(r, "path_format", None)
            if rx is not None and f:
                table.append((rx, f))
        _ROUTE_TABLE = table
    path = request.url.path
    for rx, f in _ROUTE_TABLE:
        if rx.match(path):
            return f
    return "/_unmatched"


# ── DB-backed gauges (cached; failures drop the series, never 500) ─────────

_DB_CACHE: dict[str, tuple[float, object]] = {}
_DB_CACHE_LOCK = threading.Lock()


def _cached(name: str, ttl_s: float, fn):
    """Value of fn(), refreshed at most every ttl_s. On error: serve the
    last good value if any (marked fresh again, so a broken DB is re-probed
    only once per ttl — /metrics never hammers or propagates)."""
    now = time.time()
    with _DB_CACHE_LOCK:
        hit = _DB_CACHE.get(name)
        if hit is not None and hit[0] > now:
            return hit[1]
    try:
        value = fn()
    except Exception:  # noqa: BLE001 — metrics must never take the API down
        value = hit[1] if hit is not None else None
    with _DB_CACHE_LOCK:
        _DB_CACHE[name] = (now + ttl_s, value)
    return value


def _jobs_by_status() -> dict[str, int]:
    from atp import tenant_db
    org = tenant_db.DEFAULT_ORG
    rows = tenant_db.scoped_query(
        org,
        "SELECT status, COUNT(*) AS n FROM jobs "
        "WHERE org_id = :org GROUP BY status",
        {"org": org},
    )
    out = {"queued": 0, "running": 0, "done": 0, "error": 0}
    for r in rows:
        out[str(r["status"])] = int(r["n"])
    return out


def _evidence_chain_length() -> int:
    from atp import tenant_db
    org = tenant_db.DEFAULT_ORG
    rows = tenant_db.scoped_query(
        org,
        "SELECT COUNT(*) AS n FROM atp_evidence WHERE org_id = :org",
        {"org": org},
    )
    return int(rows[0]["n"])


def _licenses_by_status() -> dict[str, int]:
    from atp import tenant_db
    org = tenant_db.DEFAULT_ORG
    rows = tenant_db.scoped_query(
        org,
        "SELECT status, COUNT(*) AS n FROM licenses "
        "WHERE org_id = :org GROUP BY status",
        {"org": org},
    )
    out = {"active": 0, "revoked": 0}     # always emit the two headline series
    for r in rows:
        out[str(r["status"])] = int(r["n"])
    return out


# ── Exposition (Prometheus text format 0.0.4) ──────────────────────────────

def _esc(v: str) -> str:
    """Escape a label value per the exposition format."""
    return v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def render_metrics() -> str:
    lines: list[str] = []
    add = lines.append

    add("# HELP bu_up 1 while the API process is up and serving.")
    add("# TYPE bu_up gauge")
    add("bu_up 1")
    add("# HELP bu_process_start_time_seconds Unix time the process started.")
    add("# TYPE bu_process_start_time_seconds gauge")
    add(f"bu_process_start_time_seconds {_STARTED_AT:.3f}")

    with _METRICS_LOCK:
        requests = dict(_REQUESTS)
        hist = {k: [list(v[0]), v[1], v[2]] for k, v in _HIST.items()}
        rate_limited = _RATE_LIMITED

    add("# HELP bu_requests_total HTTP requests by method, route template, "
        "and status.")
    add("# TYPE bu_requests_total counter")
    for (method, path, status), n in sorted(requests.items(),
                                            key=lambda kv: kv[0]):
        add(f'bu_requests_total{{method="{_esc(method)}",path="{_esc(path)}",'
            f'status="{status}"}} {n}')

    add("# HELP bu_request_duration_seconds HTTP request latency by route "
        "template and status.")
    add("# TYPE bu_request_duration_seconds histogram")
    for (path, status), (counts, total, count) in sorted(
            hist.items(), key=lambda kv: kv[0]):
        labels = f'path="{_esc(path)}",status="{status}"'
        for i, le in enumerate(HIST_BUCKETS):
            add(f'bu_request_duration_seconds_bucket{{{labels},le="{le}"}} '
                f"{counts[i]}")
        add(f'bu_request_duration_seconds_bucket{{{labels},le="+Inf"}} '
            f"{counts[-1]}")
        add(f"bu_request_duration_seconds_sum{{{labels}}} {total:.6f}")
        add(f"bu_request_duration_seconds_count{{{labels}}} {count}")

    add("# HELP bu_rate_limited_total Requests rejected with 429 by the "
        "token-bucket limiter.")
    add("# TYPE bu_rate_limited_total counter")
    add(f"bu_rate_limited_total {rate_limited}")

    jobs = _cached("jobs", 5.0, _jobs_by_status)
    if jobs is not None:
        add("# HELP bu_jobs Background jobs by status (org-demo scope, "
            "cached 5s).")
        add("# TYPE bu_jobs gauge")
        for status, n in sorted(jobs.items()):
            add(f'bu_jobs{{status="{_esc(status)}"}} {n}')

    chain = _cached("evidence_chain", 30.0, _evidence_chain_length)
    if chain is not None:
        add("# HELP bu_evidence_chain_length Rows in the signed evidence "
            "chain (org-demo scope, cached 30s).")
        add("# TYPE bu_evidence_chain_length gauge")
        add(f"bu_evidence_chain_length {chain}")

    licenses = _cached("licenses", 30.0, _licenses_by_status)
    if licenses is not None:
        add("# HELP bu_licenses Marketplace licenses by status (org-demo "
            "scope, cached 30s).")
        add("# TYPE bu_licenses gauge")
        for status, n in sorted(licenses.items()):
            add(f'bu_licenses{{status="{_esc(status)}"}} {n}')

    return "\n".join(lines) + "\n"


def metrics_response() -> PlainTextResponse:
    """Response for the /metrics route (api/server.py owns the route def)."""
    return PlainTextResponse(render_metrics(), media_type=METRICS_CONTENT_TYPE)


# ── JSON request log ───────────────────────────────────────────────────────

def _emit_json_log(request: Request, path_tmpl: str, status: int,
                   elapsed_s: float) -> None:
    """One JSON line to stdout. Fields fixed by _JSON_LOG_FIELDS — never add
    headers or bodies here (redaction by construction; see docstring §3)."""
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "method": request.method,
        "path": path_tmpl,
        "status": status,
        "ms": round(elapsed_s * 1000.0, 2),
        "org": getattr(request.state, "org_id", None),
        "user": getattr(request.state, "user", None),
        "ip": request.client.host if request.client else None,
    }
    assert set(record) == set(_JSON_LOG_FIELDS)
    print(json.dumps(record, separators=(",", ":")), file=sys.stdout,
          flush=True)


# ── The middleware ─────────────────────────────────────────────────────────

async def ops_middleware(request: Request, call_next):
    """Rate limit (post-auth identity) + metrics + optional JSON log.

    Runs INSIDE auth (api/server.py registration order), so
    request.state.user/org_id are set for authenticated requests and 401s
    never reach us. A 429 returns straight from here — inner layers (tenant
    access log, CORS, routes) never run for rate-limited requests.
    """
    start = time.perf_counter()
    method = request.method
    raw_path = request.url.path

    limiter = _LIMITER
    if (limiter is not None and method != "OPTIONS"
            and raw_path not in RATE_LIMIT_EXEMPT_PATHS):
        ip = request.client.host if request.client else "unknown"
        subject = getattr(request.state, "user", None) or "-"
        allowed, retry_after = limiter.acquire(f"{ip}|{subject}")
        if not allowed:
            _count_rate_limited()
            elapsed = time.perf_counter() - start
            tmpl = _path_template(request)
            _observe(method, tmpl, 429, elapsed)
            if _log_json_enabled():
                _emit_json_log(request, tmpl, 429, elapsed)
            return JSONResponse(
                {"detail": "rate limit exceeded"},
                status_code=429,
                headers={"Retry-After": str(retry_after)},
            )

    try:
        response = await call_next(request)
    except Exception:
        elapsed = time.perf_counter() - start
        tmpl = _path_template(request)
        _observe(method, tmpl, 500, elapsed)
        if _log_json_enabled():
            _emit_json_log(request, tmpl, 500, elapsed)
        raise
    elapsed = time.perf_counter() - start
    tmpl = _path_template(request)
    _observe(method, tmpl, response.status_code, elapsed)
    if _log_json_enabled():
        _emit_json_log(request, tmpl, response.status_code, elapsed)
    return response
