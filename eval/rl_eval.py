"""
RL eval harness — measure whether the learned weights actually improve
debate quality.

Protocol:
  1. Snapshot existing weights (so we can restore them after).
  2. Reset weights to neutral (1.0 for all).
  3. **Run A — baseline**: run all eval prompts with RL_USE_PRIOR=0,
     RL_AUTO_JUDGE=heuristic, no exploration. Record auto-judge score per turn.
  4. **Train**: replay the auto-judge feedback so weights actually learn.
  5. **Run B — RL on**: run the same prompts with RL_USE_PRIOR=1,
     RL_PRIOR_ALPHA=0.5, RL_EPSILON=0.10. Record auto-judge scores again.
  6. Restore the snapshotted weights.
  7. Print A vs B mean / median / win-rate per specialist + overall.

The same prompts are used for A and B, so this is paired eval — the
relevant statistic is mean(B - A), not mean(A) vs mean(B) independently.

Usage:
    python3 eval/rl_eval.py
    python3 eval/rl_eval.py --rounds 1 --prompts eval/prompts.txt
    python3 eval/rl_eval.py --quick                # 3 prompts, 1 round
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


DEFAULT_PROMPTS = [
    "Design a kinetic boost-phase intercept system for a 1500 km range threat.",
    "Specify a high-pressure turbine blade material for a 1700 K inlet temperature.",
    "Design a hovering-rotor drone autopilot tolerant of 30 m/s gusts.",
    "Choose between Kalman filter and particle filter for hypersonic re-entry GNC.",
    "Cool a 50 kW solid-state laser at high-altitude (20 km) atmospheric conditions.",
    "Design a microsat reaction-wheel array — failure-tolerant attitude control.",
    "Pick a printable alloy for a turbopump impeller running on LOX/methane.",
    "Specify a flight-software architecture for a 1 ms control-loop autopilot.",
    "Aerodynamic analysis: 60° swept-wing transonic buffet onset.",
    "Trade study: hybrid-electric vs turbofan for a 200 nmi UAM corridor.",
]


def load_prompts(path: str | None) -> list[str]:
    if not path:
        return DEFAULT_PROMPTS
    p = Path(path)
    return [ln.strip() for ln in p.read_text().splitlines() if ln.strip()]


def _save_weight_snapshot() -> dict:
    from rag.weights import _load
    return json.loads(json.dumps(_load(), default=str))


def _restore_weight_snapshot(snap: dict) -> None:
    from rag.weights import WEIGHTS_PATH
    WEIGHTS_PATH.write_text(json.dumps(snap, indent=2, default=str))
    # Bust module cache
    import rag.weights as W
    W._cache = None


def _wipe_session_logs() -> tuple[Path, Path]:
    """Move turns.jsonl and sessions.jsonl out of the way so the eval starts
    clean. Returns the tmp paths for restore."""
    from agents.feedback import TURNS_LOG, SESSIONS_LOG
    ts = int(time.time())
    moved = []
    for p in (TURNS_LOG, SESSIONS_LOG):
        if p.exists():
            tmp = p.with_suffix(p.suffix + f".eval-bak.{ts}")
            p.rename(tmp)
            moved.append((p, tmp))
        else:
            moved.append((p, None))
    return moved


def _restore_session_logs(moves: list) -> None:
    for orig, tmp in moves:
        if orig.exists():
            orig.unlink()
        if tmp and tmp.exists():
            tmp.rename(orig)


def run_one(prompt: str, rounds: int) -> list[dict]:
    """Run a single debate; return per-turn auto-judge scores."""
    from agents.orchestrator import run_debate
    from agents.judge import score_turn

    history, _ = run_debate(prompt, rounds=rounds)
    out = []
    prior = ""
    for t in history.turns:
        s = score_turn(t, prompt, prior)
        out.append({
            "spec":  t.spec_key,
            "score": float(s.get("score", 0.0)),
            "n_cites": len(t.citations),
            "cohort": t.cohort_id,
        })
        prior = (prior + "\n" + t.raw_text)[-3000:]
    return out


def replay_for_training():
    """After Run A, the auto-judge has appended feedback events to
    sessions.jsonl. Replay them so the prior store learns."""
    from agents.feedback import _apply_credit_safe, POS_DELTA, NEG_DELTA, TURNS_LOG, SESSIONS_LOG
    if not (TURNS_LOG.exists() and SESSIONS_LOG.exists()):
        return 0
    # Index turns
    turns = {}
    for line in TURNS_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if o.get("turn_id"):
            turns[o["turn_id"]] = o
    n = 0
    for line in SESSIONS_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if o.get("kind") != "feedback":
            continue
        t = turns.get(o.get("turn_id"))
        if t is None:
            continue
        score = o.get("score", 0.0)
        delta = POS_DELTA * score if score > 0 else NEG_DELTA * abs(score)
        _apply_credit_safe(t.get("citations", []), delta)
        n += 1
    return n


def summarize(label: str, results: list[list[dict]]) -> dict:
    """Flatten + per-spec stats."""
    flat = [t for run in results for t in run]
    if not flat:
        return {"label": label, "n": 0}
    by_spec: dict[str, list[float]] = {}
    for t in flat:
        by_spec.setdefault(t["spec"], []).append(t["score"])
    out = {"label": label, "n": len(flat),
           "mean": round(statistics.mean(t["score"] for t in flat), 3),
           "median": round(statistics.median(t["score"] for t in flat), 3),
           "by_spec": {k: round(statistics.mean(v), 3) for k, v in by_spec.items()},
           }
    return out


def paired_winrate(a: list[list[dict]], b: list[list[dict]]) -> float:
    """Per-prompt mean score B vs A, return fraction where B > A."""
    if not a or not b:
        return 0.0
    wins = 0
    n = 0
    for a_run, b_run in zip(a, b):
        if not a_run or not b_run:
            continue
        a_mean = statistics.mean(t["score"] for t in a_run)
        b_mean = statistics.mean(t["score"] for t in b_run)
        if b_mean > a_mean:
            wins += 1
        n += 1
    return wins / max(1, n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=1,
                    help="Debate rounds per prompt (default 1 — eval is slow)")
    ap.add_argument("--prompts", default=None,
                    help="Path to a prompts.txt (one per line)")
    ap.add_argument("--quick", action="store_true",
                    help="3 prompts, 1 round — smoke test")
    ap.add_argument("--keep_logs", action="store_true",
                    help="Don't move existing session logs aside")
    ap.add_argument("--no_restore", action="store_true",
                    help="Don't restore weight snapshot after — keep learned weights")
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("✗ ANTHROPIC_API_KEY not set — run_debate needs it")

    prompts = load_prompts(args.prompts)
    if args.quick:
        prompts = prompts[:3]
        args.rounds = 1
    print(f"[eval] {len(prompts)} prompts × {args.rounds} round(s)")

    # Snapshot state we'll restore
    snapshot = _save_weight_snapshot()
    moves = [] if args.keep_logs else _wipe_session_logs()

    try:
        from rag.weights import reset
        reset()

        # ── Run A — baseline ──────────────────────────────────────────
        print("\n[A/2] Baseline run (RL_USE_PRIOR=0, auto-judge writes feedback)")
        os.environ["RL_USE_PRIOR"] = "0"
        os.environ["RL_AUTO_JUDGE"] = "heuristic"
        os.environ["RL_EPSILON"] = "0"
        a_results = []
        for i, p in enumerate(prompts, 1):
            print(f"  [{i}/{len(prompts)}] {p[:60]}...", flush=True)
            t0 = time.time()
            a_results.append(run_one(p, args.rounds))
            print(f"     {time.time()-t0:.1f}s · {len(a_results[-1])} turns")

        # ── Train ─────────────────────────────────────────────────────
        print("\n[Train] Replaying auto-judge feedback into weight store...")
        n = replay_for_training()
        print(f"  replayed {n} feedback events")

        # ── Run B — RL on ─────────────────────────────────────────────
        print("\n[B/2] RL-on run (RL_USE_PRIOR=1, RL_PRIOR_ALPHA=0.5, RL_EPSILON=0.10)")
        os.environ["RL_USE_PRIOR"] = "1"
        os.environ["RL_PRIOR_ALPHA"] = "0.5"
        os.environ["RL_EPSILON"] = "0.10"
        os.environ["RL_AUTO_JUDGE"] = "heuristic"
        b_results = []
        for i, p in enumerate(prompts, 1):
            print(f"  [{i}/{len(prompts)}] {p[:60]}...", flush=True)
            t0 = time.time()
            b_results.append(run_one(p, args.rounds))
            print(f"     {time.time()-t0:.1f}s · {len(b_results[-1])} turns")

        # ── Report ────────────────────────────────────────────────────
        sa = summarize("A · baseline", a_results)
        sb = summarize("B · RL on",   b_results)
        wr = paired_winrate(a_results, b_results)

        print("\n" + "=" * 70)
        print(f"  Baseline   mean={sa['mean']:.3f} median={sa['median']:.3f}  by_spec={sa['by_spec']}")
        print(f"  RL on      mean={sb['mean']:.3f} median={sb['median']:.3f}  by_spec={sb['by_spec']}")
        delta = sb['mean'] - sa['mean']
        print(f"  Δ mean      {delta:+.3f}")
        print(f"  win-rate    {wr:.1%}  (B beats A on N/{len(prompts)} prompts)")
        verdict = "✓ RL helps" if delta > 0 and wr >= 0.5 else "✗ no clear lift"
        print(f"  verdict    {verdict}")
        print("=" * 70)

        # Persist results JSON for later analysis
        out_path = PROJECT_ROOT / "eval" / "results" / f"rl_eval_{int(time.time())}.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps({
            "prompts":  prompts,
            "rounds":   args.rounds,
            "baseline": a_results,
            "rl_on":    b_results,
            "summary":  {"a": sa, "b": sb, "delta": delta, "winrate": wr},
        }, indent=2, default=str))
        print(f"\n  results → {out_path.relative_to(PROJECT_ROOT)}")

    finally:
        # Restore (default) so eval doesn't pollute prod state
        if not args.no_restore:
            _restore_weight_snapshot(snapshot)
            print("\n[restore] weight snapshot restored")
        if moves and not args.keep_logs:
            _restore_session_logs(moves)
            print("[restore] session logs restored")


if __name__ == "__main__":
    main()
