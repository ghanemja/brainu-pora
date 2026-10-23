#!/usr/bin/env python3
"""
CI smoke — docs/HARDENING.md Phase 5 (login → 6 agent screens render).

Boots the real stack the way the demo runs it, then drives a browser
through the frontend AND exercises the hardened API paths end-to-end:

  1. uvicorn api.server:app          — fresh tmp sqlite DATABASE_URL,
                                       BU_AUTH_DISABLED=1 (dev demo mode)
  2. python -m http.server design/   — the zero-build frontend, exactly as
                                       published (in-browser Babel; the CI
                                       run IS the dev-mode regression test)
  3. API smoke (urllib, no browser):
       login → dry-run exam e2e (POST /atp/exams/run → poll /jobs/{id} →
       award) → evidence + chain verify → license lifecycle
       (issue → gated /experts chat → revoke → 403)
  4. Playwright chromium:
       login gate (admin/password) → all 6 agent-view tabs render
       non-empty main content → zero console errors → Human view toggle
       renders the trailhead.

Runnable locally and in CI (identical behavior):

    pip install playwright && playwright install chromium
    python3 scripts/ci_smoke.py

Exit 0 = green. Any assertion prints a ✗ line and exits 1.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN_DIR = ROOT / "design"
INDEX = "Brain%20University.html"

EXAM_CERT = "atp-l4-math"       # seed cert with a commissioned item bank
LICENSED_AGENT = "gemma-math"   # licensable marketplace agent (seed)
AGENT_TABS = ["university", "agents", "certs", "marketplace", "governance", "vault"]

#: Resource URLs that may 4xx without failing the smoke. Keep this SHORT and
#: explained:
#:   favicon.ico             — not shipped; browsers auto-request it
#:   .compiled/manifest.json — the prod-build probe (HARDENING.md Phase 5);
#:                             404 IS the zero-build dev mode working as
#:                             designed (page falls back to in-browser Babel)
RESOURCE_404_ALLOWLIST = ("favicon.ico", ".compiled/manifest.json")

_STEPS: list[str] = []


def ok(msg: str) -> None:
    _STEPS.append(msg)
    print(f"  ✓ {msg}")


def die(msg: str) -> None:
    print(f"  ✗ {msg}", file=sys.stderr)
    sys.exit(1)


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ── HTTP helpers (stdlib only — the API smoke needs no client deps) ────────

def request(method: str, url: str, body: dict | None = None,
            headers: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read() or b"{}")
        except json.JSONDecodeError:
            payload = {}
        return e.code, payload


def wait_for(url: str, timeout_s: float = 60.0, label: str = "") -> None:
    deadline = time.monotonic() + timeout_s
    last_err: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3):
                return
        except urllib.error.HTTPError:
            return  # server is up; status is the endpoint's business
        except Exception as e:  # noqa: BLE001 — conn refused while booting
            last_err = e
            time.sleep(0.4)
    die(f"{label or url} did not come up within {timeout_s:.0f}s ({last_err})")


# ── API smoke ────────────────────────────────────────────────────────────────

def poll_job(api: str, job_id: str, auth: dict,
             timeout_s: float = 180.0) -> dict:
    """Poll /jobs/{id} until done/error; die on timeout. Returns job result."""
    if not job_id:
        die("poll_job called without a job id")
    deadline = time.monotonic() + timeout_s
    job: dict = {}
    while time.monotonic() < deadline:
        status, job = request("GET", f"{api}/jobs/{job_id}", headers=auth)
        if status != 200:
            die(f"GET /jobs/{job_id} → {status} {job}")
        if job.get("status") in ("done", "error"):
            break
        time.sleep(0.5)
    if job.get("status") != "done":
        die(f"job {job_id} did not finish: {job}")
    return job.get("result") or {}


def api_smoke(api: str) -> None:
    print("API smoke:")
    status, body = request("POST", f"{api}/login",
                           {"username": "admin", "password": "password"})
    if status != 200 or not body.get("token"):
        die(f"POST /login admin/password → {status} {body}")
    auth = {"Authorization": f"Bearer {body['token']}"}
    ok("login admin/password → bearer token")

    # dry-run certification exam, end to end through the job queue
    status, body = request("POST", f"{api}/atp/exams/run",
                           {"certId": EXAM_CERT, "dryRun": True}, auth)
    if status != 200 or not body.get("jobId"):
        die(f"POST /atp/exams/run → {status} {body}")
    job_id = body["jobId"]
    deadline = time.monotonic() + 180
    job: dict = {}
    while time.monotonic() < deadline:
        status, job = request("GET", f"{api}/jobs/{job_id}", headers=auth)
        if status != 200:
            die(f"GET /jobs/{job_id} → {status} {job}")
        if job.get("status") in ("done", "error"):
            break
        time.sleep(0.5)
    if job.get("status") != "done":
        die(f"exam job did not finish: {job}")
    award = job.get("result") or {}
    if award.get("certId") != EXAM_CERT or award.get("verdict") not in ("pass", "fail"):
        die(f"exam award malformed: {award}")
    evidence_ids = award.get("evidenceIds") or []
    if not evidence_ids:
        die(f"exam award carries no evidence: {award}")
    ok(f"dry-run exam {EXAM_CERT} → verdict={award['verdict']} "
       f"score={award.get('score')} ({len(evidence_ids)} evidence rows)")

    status, body = request(
        "GET", f"{api}/atp/evidence/{evidence_ids[0]}/verify", headers=auth)
    if status != 200 or not body.get("ok") or not body.get("sigValid"):
        die(f"evidence verify → {status} {body}")
    status, body = request("GET", f"{api}/atp/chain/verify", headers=auth)
    if status != 200 or not body.get("ok") or body.get("length", 0) < len(evidence_ids):
        die(f"chain verify → {status} {body}")
    ok(f"evidence signature + org chain verify (length={body.get('length')})")

    # license lifecycle: issue → gated chat → revoke → 403
    status, body = request("POST", f"{api}/billing/licenses",
                           {"agentId": LICENSED_AGENT}, auth)
    if status != 200 or not body.get("licenseKey") or not (body.get("license") or {}).get("id"):
        die(f"POST /billing/licenses → {status} {body}")
    license_id, key = body["license"]["id"], body["licenseKey"]
    ok(f"license issued for {LICENSED_AGENT} (id={license_id})")

    chat_body = {"messages": [{"role": "user", "content": "What is 2 + 2?"}]}
    chat_url = f"{api}/experts/{LICENSED_AGENT}/chat"
    status, body = request("POST", chat_url, chat_body,
                           {"X-ATP-License-Key": key})
    if status != 200 or not body.get("reply"):
        die(f"licensed chat → {status} {body}")
    ok("licensed /experts chat replied (usage metered)")

    status, body = request("POST", chat_url, chat_body,
                           {"X-ATP-License-Key": "atpk_forged.deadbeef"})
    if status != 401:
        die(f"forged key must 401, got {status} {body}")

    status, body = request("POST", f"{api}/billing/licenses/{license_id}/revoke",
                           {"reason": "ci smoke"}, auth)
    if status != 200:
        die(f"revoke → {status} {body}")
    status, body = request("POST", chat_url, chat_body,
                           {"X-ATP-License-Key": key})
    if status != 403:
        die(f"revoked key must 403 on the very next call, got {status} {body}")
    ok("revoked license → 403 on the next chat call (forged key → 401)")

    # ── Phase 6: report-card PDF + knowledge ingestion → SME sign-off → exam ──
    pdf_req = urllib.request.Request(f"{api}/atp/agents/atlas-ops/report.pdf",
                                     headers=auth)
    with urllib.request.urlopen(pdf_req, timeout=60) as resp:
        pdf_bytes = resp.read()
        if resp.status != 200 or not pdf_bytes.startswith(b"%PDF"):
            die(f"report.pdf → {resp.status}, magic {pdf_bytes[:8]!r}")
    ok(f"report-card PDF renders ({len(pdf_bytes)} bytes)")

    # generate_l5_draft needs >= 2 docs (blueprint sections = doc titles)
    boundary = "ciSmokeBoundary"
    docs_md = {
        # >= 2 headings per doc: the generator yields ~2 items per heading
        # and requires >= 8 items overall.
        "runbook.md": (
            "# Incident Runbook\n\n"
            "## Acknowledge\n\nAcknowledge the page within five minutes "
            "and open an incident channel named for the alert.\n\n"
            "## Escalate\n\nEscalate to the on-call lead when customer "
            "impact lasts longer than fifteen minutes.\n"),
        "rollback.md": (
            "# Rollback Policy\n\n"
            "## Snapshot first\n\nAlways snapshot the database before any "
            "rollback and record the snapshot id in the channel.\n\n"
            "## Notify\n\nNotify the on-call lead and the release owner "
            "before starting the rollback.\n"),
    }
    doc_ids = []
    for fname, doc_md in docs_md.items():
        mp = (f"--{boundary}\r\nContent-Disposition: form-data; "
              f"name=\"file\"; filename=\"{fname}\"\r\n"
              f"Content-Type: text/markdown\r\n\r\n"
              f"{doc_md}\r\n--{boundary}--\r\n").encode()
        up_req = urllib.request.Request(f"{api}/knowledge/docs", data=mp,
                                        method="POST", headers=auth)
        up_req.add_header("Content-Type",
                          f"multipart/form-data; boundary={boundary}")
        with urllib.request.urlopen(up_req, timeout=30) as resp:
            doc = json.loads(resp.read())
        doc_ids.append(doc.get("id") or die(f"knowledge upload returned {doc}"))
    status, draft = request("POST", f"{api}/knowledge/drafts",
                            {"docIds": doc_ids, "title": "CI L5 draft"},
                            headers=auth)
    if status != 200 or len(draft.get("items", [])) < 8:
        die(f"draft → {status}, items {len(draft.get('items', []))}")
    status, appr = request("POST",
                           f"{api}/knowledge/drafts/{draft['id']}/approve",
                           {"note": "ci smoke sign-off"}, headers=auth)
    if status != 200 or not appr.get("evidenceId"):
        die(f"approve → {status} {appr}")
    status, job = request("POST",
                          f"{api}/knowledge/drafts/{draft['id']}/exam",
                          {"dryRun": True}, headers=auth)
    if status != 200:
        die(f"draft exam → {status} {job}")
    award = poll_job(api, job.get("jobId") or job.get("job_id"), auth)
    if not award.get("verdict"):
        die(f"draft-exam award missing verdict: {award}")
    status, chain = request("GET", f"{api}/atp/chain/verify", headers=auth)
    if status != 200 or not chain.get("ok"):
        die(f"chain broken after knowledge flow: {chain}")
    ok("knowledge e2e: upload → draft → SME sign-off → dry-run exam → chain ok")


# ── Browser smoke ────────────────────────────────────────────────────────────

def browser_smoke(api: str, web: str) -> None:
    from playwright.sync_api import sync_playwright

    from playwright.sync_api import TimeoutError as PWTimeoutError

    print("Browser smoke (playwright chromium):")
    console_errors: list[str] = []
    page_errors: list[str] = []
    bad_responses: list[str] = []

    def note_response(resp) -> None:
        if resp.status >= 400 and not any(
                allowed in resp.url for allowed in RESOURCE_404_ALLOWLIST):
            bad_responses.append(f"HTTP {resp.status} {resp.url}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(120_000)

        # The deployed design/config.js points at the hosted backend; serve
        # the CI backend instead without touching the working tree.
        page.route("**/config.js", lambda route: route.fulfill(
            status=200, content_type="application/javascript",
            body=f'window.BU_API_BASE = "{api}";\n'))

        # 'Failed to load resource' console lines carry no resource URL, so
        # judge those via the response listener (which has status + URL and
        # can honor RESOURCE_404_ALLOWLIST); keep every other console error.
        page.on("console", lambda m: console_errors.append(m.text)
                if m.type == "error"
                and not m.text.startswith("Failed to load resource") else None)
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("response", note_response)

        page.goto(f"{web}/{INDEX}")

        # Login gate (BU_AUTH_DISABLED=1 dev creds — api/auth.py)
        page.fill("#bu-gate-u", "admin")
        page.fill("#bu-gate-p", "password")
        page.click("#bu-gate-form button[type=submit]")
        page.wait_for_selector("#bu-gate", state="hidden")
        ok("login gate accepted admin/password")

        # App shell up = in-browser Babel compiled every .jsx (zero-build
        # dev mode contract). Fresh profile defaults to the agent view.
        # One reload retry: the pinned React/Babel/three CDN fetches are the
        # only non-local resources and occasionally stall on a cold edge.
        try:
            page.wait_for_selector('nav.nav button[data-nav="university"]')
        except PWTimeoutError:
            print("  … app shell slow (CDN?) — reloading once", file=sys.stderr)
            page.reload()
            page.wait_for_selector('nav.nav button[data-nav="university"]')

        for tab in AGENT_TABS:
            page.click(f'button[data-nav="{tab}"]')
            page.wait_for_function(
                """(tab) => {
                    const btn  = document.querySelector(`button[data-nav="${tab}"]`);
                    const main = document.querySelector('main');
                    return btn && btn.classList.contains('active') &&
                           main && main.innerText.trim().length > 80;
                }""",
                arg=tab)
            chars = page.evaluate(
                "document.querySelector('main').innerText.trim().length")
            ok(f"agent tab '{tab}' rendered non-empty main ({chars} chars)")

        # Human ◦ Agent toggle → trailhead
        page.click('.view-toggle button:has-text("Human")')
        page.wait_for_function(
            """() => {
                const btn  = document.querySelector('button[data-nav="trailhead"]');
                const main = document.querySelector('main');
                return btn && btn.classList.contains('active') &&
                       main && main.innerText.trim().length > 40;
            }""")
        ok("human view toggle → trailhead rendered")

        # Courses → PoRA course page (iframe) → plan a route → walk it.
        page.click('button[data-nav="courses"]')
        page.wait_for_selector('iframe[src*="pora-atlas.html"]')
        atlas = page.frame_locator('iframe[src*="pora-atlas.html"]')
        atlas.locator("#v-syllabus .chap").first.wait_for()
        chapters = atlas.locator("#v-syllabus .chap").count()
        if chapters < 19:
            die(f"PoRA syllabus rendered {chapters} chapter cards, expected ≥ 19")
        atlas.locator('[data-go="kalman_filter"]').first.click()
        atlas.locator("#drawer.open [data-check] .opt").first.wait_for()
        ok(f"courses tab: PoRA syllabus ({chapters} cards) + concept drawer")
        atlas.locator("#dr-close").click()
        atlas.locator("#go").click()
        atlas.locator("[data-walkroute]").click()
        page.wait_for_function(
            """() => {
                const btn  = document.querySelector('button[data-nav="walk"]');
                const main = document.querySelector('main');
                return btn && btn.classList.contains('active') &&
                       main && /COMPREHENSION CHECK/.test(main.innerText);
            }""")
        ok("PoRA route handed to the Walk screen with a concept check")

        page.wait_for_timeout(1500)  # let late async fetches surface errors
        browser.close()

    real_errors = console_errors + page_errors + bad_responses
    if real_errors:
        for e in real_errors:
            print(f"  console/network error: {e}", file=sys.stderr)
        die(f"{len(real_errors)} console/network error(s) during the browser smoke")
    ok("zero console errors across login + 8 screens")


def main() -> int:
    api_port, web_port = free_port(), free_port()
    api = f"http://127.0.0.1:{api_port}"
    web = f"http://127.0.0.1:{web_port}"

    procs: list[subprocess.Popen] = []
    with tempfile.TemporaryDirectory(prefix="bu-ci-smoke-") as tmp:
        env = os.environ.copy()
        env.update({
            "BU_AUTH_DISABLED": "1",                     # demo mode contract
            "DATABASE_URL": f"sqlite:///{tmp}/ci.db",    # fresh throwaway DB
            "PYTHONUNBUFFERED": "1",
            # This is a functional smoke, not a rate-limit test: the exam
            # poll loop + browser traffic share one (IP, subject) bucket and
            # can exceed api/ops.py's default 120/60s. Explicitly off, per
            # its own env-tuning contract (BU_RATE_LIMIT=0 disables).
            "BU_RATE_LIMIT": "0",
            # Phase 6 surfaces: T2 encryption + evidence signing need keys
            # even in demo mode (knowledge routes 503 without them).
            "DATA_ENCRYPTION_KEY": "ci-smoke-data-key-0123456789abcdef",
            "EVIDENCE_SIGNING_KEY": "ci-smoke-evidence-key-0123456789ab",
        })
        try:
            procs.append(subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "api.server:app",
                 "--host", "127.0.0.1", "--port", str(api_port)],
                cwd=ROOT, env=env))
            procs.append(subprocess.Popen(
                [sys.executable, "-m", "http.server", str(web_port),
                 "--bind", "127.0.0.1", "--directory", str(DESIGN_DIR)],
                cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

            wait_for(f"{api}/health", 90, "uvicorn api.server:app")
            wait_for(f"{web}/{INDEX}", 30, "http.server design/")
            print(f"servers up: api={api} web={web}")

            api_smoke(api)
            browser_smoke(api, web)
        finally:
            for p in procs:
                p.terminate()
            for p in procs:
                try:
                    p.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    p.kill()

    print(f"ci_smoke: OK — {len(_STEPS)} checks green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
