"""
atp/exams.py — Phase 3 certification engine (docs/HARDENING.md).

Turns the ATP standard's promises (docs/ATP.md §2) into enforced code:

  blueprint → item bank (atp/items/<cert_id>.json, human-editable)
            → candidate answers via agents.backend.get_backend(candidate_spec)
            → judge from a DIFFERENT model family — family_of(judge) !=
              family_of(candidate) is checked BEFORE any model call, else
              SeparationError (principle 2)
            → verdict vs the cert's passCriteria (overall + perSection)
            → evidence rows, append-only + HMAC-signed with a per-org
              prev_hash chain via atp/signing.py (principles 1 & 3)
            → award row in atp_cert_awards.

Reproducibility semantics: every evidence payload records the cert's
passCriteria seed and temperature (0). Backends are expected to decode
deterministically (greedy/temperature-0 — the HF/local backends already pin
do_sample=False / temperature 0.0); a run's `runs` repeats exist to surface
any residual nondeterminism, and each repeat's judged score is kept in
run_scores with the item score as their mean. runs = min(passCriteria.runs, 3)
to keep real exams affordable.

Dry-run mode (CI): `dry_run=True` routes the judge to 'dryrun:judge' and a
missing candidate to 'dryrun:candidate' — both DryRunBackend, deterministic
pure functions of the prompts, mapped to distinct synthetic families so the
separation check passes. Same inputs → same payloads → same sigs (given the
same EVIDENCE_SIGNING_KEY and chain position).

All DB access goes through atp/tenant_db.py (org-scoped; RLS on Postgres).

Public:
    run_exam(cert_id, candidate_spec=None, org_id='org-demo',
             dry_run=False, agent_id=None) -> award dict
    SeparationError / UnknownCertError / MissingItemBankError

CLI:
    BU_AUTH_DISABLED=1 python3 -m atp.exams atp-l4-math --dry-run --verify-chain
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

from agents.backend import family_of, get_backend
from atp import db, signing, store, tenant_db

ITEMS_DIR = Path(__file__).parent / "items"
HARNESS_VERSION = "atp-exams@2026.1-p3"
DEFAULT_JUDGE_SPEC = "claude-haiku-4-5"   # env ATP_JUDGE_SPEC overrides
MAX_RUNS = 3                              # cap on passCriteria.runs per item

_ITEM_KEYS = ("id", "section", "type", "prompt", "expected", "points")

_MIGRATED = False
_MIGRATE_LOCK = threading.Lock()


class SeparationError(RuntimeError):
    """Judge and candidate resolve to the same model family (principle 2)."""


class UnknownCertError(ValueError):
    """cert_id does not exist in the seed (atp/seed.py CERTS)."""


class MissingItemBankError(FileNotFoundError):
    """No usable item bank for the cert — blueprints-before-commissioning."""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _ensure_db() -> None:
    """Idempotently apply migrations so a fresh SQLite file just works."""
    global _MIGRATED
    if _MIGRATED:
        return
    with _MIGRATE_LOCK:
        if not _MIGRATED:
            db.run_migrations()
            _MIGRATED = True


# ── Cert + item bank loading ─────────────────────────────────────────────────

def _load_cert(cert_id: str) -> dict:
    for cert in store.get_data()["CERTS"]:
        if cert["id"] == cert_id:
            return cert
    raise UnknownCertError(
        f"unknown cert {cert_id!r} — certs are defined in atp/seed.py CERTS"
    )


def _load_item_bank(cert: dict) -> list[dict]:
    """Load + validate atp/items/<cert_id>.json against the cert blueprint."""
    cert_id = cert["id"]
    path = ITEMS_DIR / f"{cert_id}.json"
    if not path.is_file():
        raise MissingItemBankError(
            f"no item bank at {path} — a cert cannot be examined before its "
            f"blueprint has a bank (blueprints-before-commissioning, "
            f"docs/ATP.md §7). See atp/items/README.md."
        )
    bank = json.loads(path.read_text(encoding="utf-8"))
    items = bank.get("items") or []
    if not items:
        raise MissingItemBankError(f"item bank {path} has an empty 'items' list")

    section_names = {s["name"] for s in cert["blueprint"]["sections"]}
    for item in items:
        missing = [k for k in _ITEM_KEYS if k not in item]
        if missing:
            raise ValueError(
                f"item bank {path}: item {item.get('id', '?')!r} is missing "
                f"key(s) {missing} (format: atp/items/README.md)"
            )
        if item["section"] not in section_names:
            raise ValueError(
                f"item bank {path}: item {item['id']!r} names unknown section "
                f"{item['section']!r} — blueprint sections are "
                f"{sorted(section_names)}"
            )
    uncovered = section_names - {i["section"] for i in items}
    if uncovered:
        raise ValueError(
            f"item bank {path} has no items for blueprint section(s) "
            f"{sorted(uncovered)} — passCriteria.perSection would be "
            f"unverifiable"
        )
    return items


# ── Judge prompt + defensive parsing ─────────────────────────────────────────

_JUDGE_SYSTEM = (
    "You are the certification judge for the ATP (Agentic Training Platform) "
    "exam harness. Grade the candidate's answer strictly against the "
    "reference answer/criteria and the rubric. Respond with ONLY a strict "
    "JSON object — no prose, no code fences: "
    '{"score": <float between 0 and 1>, "rationale": "<one short sentence>"}'
)
_JUDGE_SYSTEM_RETRY = (
    _JUDGE_SYSTEM
    + " Your previous reply was not parseable JSON. Output the JSON object "
      "and NOTHING else."
)


def _judge_user(cert: dict, item: dict, answer: str) -> str:
    rubric = "; ".join(
        f"{r['axis']} (weight {r['weight']}): {r['desc']}"
        for r in cert.get("rubric", [])
    )
    return (
        f"Exam: {cert['label']}\n"
        f"Rubric: {rubric}\n\n"
        f"Question [{item['section']} / {item['type']}]:\n{item['prompt']}\n\n"
        f"Reference answer / grading criteria (not shown to candidate):\n"
        f"{item['expected']}\n\n"
        f"Candidate answer:\n{answer}\n\n"
        'Return strict JSON only: {"score": <float 0..1>, "rationale": "<one sentence>"}'
    )


def _parse_judge(raw: str) -> dict | None:
    """Defensive parse: first '{' .. last '}', score must be a number in 0..1."""
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        obj = json.loads(raw[start:end])
        score = float(obj["score"])
    except (ValueError, KeyError, TypeError, AttributeError):
        return None
    if not (0.0 <= score <= 1.0):
        return None
    return {"score": score, "rationale": str(obj.get("rationale", ""))}


# ── Evidence writing (signed, chained, org-scoped) ───────────────────────────
# All evidence rows for a run are accumulated in memory during the (slow)
# model-call loop and appended in ONE signing.append_chain() call — a single
# serialized transaction, so concurrent runs can't interleave the chain and
# a crash mid-run leaves no partially signed exam on disk.


# ── The exam loop ────────────────────────────────────────────────────────────

def run_exam(cert_id: str, candidate_spec: str | None = None,
             org_id: str = tenant_db.DEFAULT_ORG, dry_run: bool = False,
             agent_id: str | None = None) -> dict:
    """Run a full certification exam and return the award dict.

    Raises UnknownCertError / MissingItemBankError / SeparationError before
    any model call; SigningKeyError surfaces from atp/signing.py if evidence
    cannot be signed.
    """
    cert = _load_cert(cert_id)
    items = _load_item_bank(cert)

    candidate = candidate_spec or "dryrun:candidate"
    judge = "dryrun:judge" if dry_run else os.environ.get(
        "ATP_JUDGE_SPEC", DEFAULT_JUDGE_SPEC)

    # Principle 2 — judge/candidate separation, enforced BEFORE any model call.
    if family_of(judge) == family_of(candidate):
        raise SeparationError(
            f"judge/candidate separation violated: judge {judge!r} and "
            f"candidate {candidate!r} both resolve to model family "
            f"{family_of(judge)!r} (docs/ATP.md §2 principle 2). Set "
            f"ATP_JUDGE_SPEC to a different family, or pass a different "
            f"candidate."
        )

    pc = cert["passCriteria"]
    runs = max(1, min(int(pc.get("runs", 1)), MAX_RUNS))
    seed = int(pc.get("seed", 0))
    temperature = pc.get("temperature", 0)

    _ensure_db()
    candidate_backend = get_backend(candidate)
    judge_backend = get_backend(judge)

    candidate_system = (
        f"You are sitting the {cert['label']} certification exam "
        f"({cert['domain']}, layer L{cert['layer']}). Answer each question "
        f"precisely and show your work. Reproducibility: decoding is pinned "
        f"to temperature {temperature}, seed {seed} "
        f"(harness {HARNESS_VERSION})."
    )

    agent = agent_id or candidate
    ev_records: list[dict] = []          # appended to the chain in one txn
    graded: list[tuple[dict, list[float], bool]] = []

    for item in items:
        run_scores: list[float] = []
        flagged = False
        for _ in range(runs):
            answer = candidate_backend.complete(
                candidate_system, item["prompt"], max_tokens=800)
            judge_prompt = _judge_user(cert, item, answer)
            verdict = _parse_judge(
                judge_backend.complete(_JUDGE_SYSTEM, judge_prompt,
                                       max_tokens=300))
            if verdict is None:   # retry once, stricter instruction
                verdict = _parse_judge(
                    judge_backend.complete(_JUDGE_SYSTEM_RETRY, judge_prompt,
                                           max_tokens=300))
            if verdict is None:   # still unparseable → item flagged
                flagged = True
                run_scores.append(0.0)
            else:
                run_scores.append(round(verdict["score"], 4))

        payload = {
            "certId": cert_id,
            "itemId": item["id"],
            "run_scores": run_scores,
            "judge": judge,
            "candidate": candidate,
            "seed": seed,
            "temperature": temperature,
        }
        ev_records.append({"ts": _now(), "agent_id": agent,
                           "cert_id": cert_id, "kind": "exam_item",
                           "payload": payload})
        graded.append((item, run_scores, flagged))

    # ── Aggregate: points-weighted per section, blueprint-weighted overall ──
    item_bar = float(pc.get("perSection", 0.7))   # per-item pass bar
    per_section: dict[str, list[tuple[float, float]]] = {}
    breakdown = {"passed": 0, "failed": 0, "flagged": 0}
    for item, run_scores, flagged in graded:
        mean = sum(run_scores) / len(run_scores)
        per_section.setdefault(item["section"], []).append(
            (mean, float(item["points"])))
        if flagged:
            breakdown["flagged"] += 1
        elif mean >= item_bar:
            breakdown["passed"] += 1
        else:
            breakdown["failed"] += 1

    section_scores = {
        name: round(sum(s * p for s, p in vals) / sum(p for _, p in vals), 4)
        for name, vals in per_section.items()
    }
    weights = {s["name"]: float(s["weight"])
               for s in cert["blueprint"]["sections"]}
    weight_sum = sum(weights[name] for name in section_scores)
    overall = round(
        sum(section_scores[name] * weights[name] for name in section_scores)
        / weight_sum, 4)

    verdict_str = (
        "pass"
        if overall >= float(pc["overall"])
        and all(v >= float(pc["perSection"]) for v in section_scores.values())
        and breakdown["flagged"] == 0
        else "fail"
    )

    # ── Summary evidence row (kind=benchmark_run) ───────────────────────────
    summary_payload = {
        "certId": cert_id,
        "overall": overall,
        "sectionScores": section_scores,
        "verdict": verdict_str,
        "itemBreakdown": breakdown,
        "judge": judge,
        "candidate": candidate,
        "seed": seed,
        "temperature": temperature,
        "runs": runs,
        "harness": HARNESS_VERSION,
    }
    ev_records.append({"ts": _now(), "agent_id": agent, "cert_id": cert_id,
                       "kind": "benchmark_run", "payload": summary_payload})

    # One serialized, atomic chain append for the whole run.
    evidence_ids = [row_id for row_id, _sig in
                    signing.append_chain(org_id, ev_records)]

    # ── Award row ───────────────────────────────────────────────────────────
    ts = _now()
    res = tenant_db.insert_scoped("atp_cert_awards", {
        "ts": ts,
        "agent_id": agent,
        "cert_id": cert_id,
        "score": overall,
        "section_scores": json.dumps(section_scores, sort_keys=True),
        "item_breakdown": json.dumps(breakdown, sort_keys=True),
        "evidence_ids": json.dumps(evidence_ids),
    }, org_id)

    return {
        "agentId": agent,
        "certId": cert_id,
        "ts": ts,
        "score": overall,
        "verdict": verdict_str,
        "sectionScores": section_scores,
        "itemBreakdown": breakdown,
        "evidenceIds": evidence_ids,
        "judge": judge,
        "candidate": candidate,
        "runs": runs,
        "seed": seed,
        "temperature": temperature,
        "harness": HARNESS_VERSION,
        "awardRowId": res.lastrowid,
        "dryRun": bool(dry_run),
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run an ATP certification exam (Phase 3 engine).")
    parser.add_argument("cert_id", help="e.g. atp-l4-math")
    parser.add_argument("--candidate", default=None,
                        help="candidate backend spec (default: dryrun:candidate)")
    parser.add_argument("--org", default=tenant_db.DEFAULT_ORG)
    parser.add_argument("--agent-id", default=None,
                        help="agent id recorded on evidence/award rows "
                             "(default: the candidate spec)")
    parser.add_argument("--dry-run", action="store_true",
                        help="deterministic stub judge/candidate — no model "
                             "calls, no cost (CI mode)")
    parser.add_argument("--verify-chain", action="store_true",
                        help="verify the org's evidence chain after the run")
    args = parser.parse_args()

    award = run_exam(args.cert_id, args.candidate, org_id=args.org,
                     dry_run=args.dry_run, agent_id=args.agent_id)
    print(json.dumps(award, indent=2))
    if args.verify_chain:
        print(json.dumps(signing.verify_chain(args.org), indent=2))
