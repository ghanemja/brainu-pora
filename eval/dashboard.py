"""
RL eval dashboard data — reads eval/results/*.json produced by rl_eval.py
and returns KPI-shaped metrics ready for the frontend.

Surfaced metrics:
  baseline_mean         mean judge score, A run
  rl_mean               mean judge score, B run
  lift_abs              rl_mean - baseline_mean
  lift_pct              (rl_mean / baseline_mean - 1) * 100
  paired_winrate        fraction of prompts where B > A
  per_spec_lift         { spec_name: lift_abs }
  series                [ {ts, baseline_mean, rl_mean, lift_pct} ]
                        (one entry per result file, chronological)
  latest_file           filename of most recent result

If no eval results exist yet, returns demo synthetic data so the dashboard
demos cleanly. Generate real data via:  python3 eval/rl_eval.py --quick
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RESULTS_DIR = PROJECT_ROOT / "eval" / "results"


def dashboard() -> dict:
    """Return KPI dict suitable for the React dashboard."""
    files = sorted(RESULTS_DIR.glob("rl_eval_*.json")) if RESULTS_DIR.exists() else []
    if not files:
        return _demo_payload()

    series = []
    for f in files:
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        a_flat = [t for run in data.get("baseline", []) for t in run]
        b_flat = [t for run in data.get("rl_on", []) for t in run]
        if not a_flat or not b_flat:
            continue
        a_mean = statistics.mean(t["score"] for t in a_flat)
        b_mean = statistics.mean(t["score"] for t in b_flat)
        ts = _ts_from_name(f.name)
        series.append({
            "ts":            ts,
            "baseline_mean": round(a_mean, 3),
            "rl_mean":       round(b_mean, 3),
            "lift_pct":      round((b_mean / a_mean - 1) * 100, 1) if a_mean else 0.0,
        })

    if not series:
        return _demo_payload()

    latest = json.loads(files[-1].read_text())
    a_flat = [t for run in latest.get("baseline", []) for t in run]
    b_flat = [t for run in latest.get("rl_on", []) for t in run]

    a_mean = statistics.mean(t["score"] for t in a_flat) if a_flat else 0.0
    b_mean = statistics.mean(t["score"] for t in b_flat) if b_flat else 0.0

    by_spec: dict[str, dict] = {}
    for t in a_flat:
        by_spec.setdefault(t["spec"], {"a": [], "b": []})["a"].append(t["score"])
    for t in b_flat:
        by_spec.setdefault(t["spec"], {"a": [], "b": []})["b"].append(t["score"])

    per_spec_lift = {
        spec: round(
            (statistics.mean(v["b"]) if v["b"] else 0)
            - (statistics.mean(v["a"]) if v["a"] else 0),
            3,
        )
        for spec, v in by_spec.items()
    }

    winrate = _paired_winrate(latest.get("baseline", []), latest.get("rl_on", []))

    return {
        "baseline_mean":  round(a_mean, 3),
        "rl_mean":        round(b_mean, 3),
        "lift_abs":       round(b_mean - a_mean, 3),
        "lift_pct":       round((b_mean / a_mean - 1) * 100, 1) if a_mean else 0.0,
        "paired_winrate": round(winrate, 3),
        "per_spec_lift":  per_spec_lift,
        "series":         series,
        "latest_file":    files[-1].name,
        "n_prompts":      len(latest.get("prompts", [])),
        "is_demo":        False,
    }


def _ts_from_name(name: str) -> int:
    import re
    m = re.search(r"rl_eval_(\d+)\.json", name)
    return int(m.group(1)) if m else 0


def _paired_winrate(a, b) -> float:
    wins = n = 0
    for a_run, b_run in zip(a, b):
        if not a_run or not b_run:
            continue
        a_mean = statistics.mean(t["score"] for t in a_run)
        b_mean = statistics.mean(t["score"] for t in b_run)
        if b_mean > a_mean:
            wins += 1
        n += 1
    return wins / max(1, n)


def _demo_payload() -> dict:
    """Synthetic-but-plausible numbers so the dashboard demos before
    real eval runs exist. Marked is_demo=True so UI can label it."""
    return {
        "baseline_mean":  0.61,
        "rl_mean":        0.78,
        "lift_abs":       0.17,
        "lift_pct":       27.9,
        "paired_winrate": 0.84,
        "per_spec_lift": {
            "Aero":  0.21, "Bio":  0.09, "CS":   0.18,
            "Math":  0.22, "Mech": 0.14, "Sys":  0.19,
        },
        "series": [
            {"ts": 1700000000, "baseline_mean": 0.58, "rl_mean": 0.62, "lift_pct":  6.9},
            {"ts": 1702000000, "baseline_mean": 0.60, "rl_mean": 0.69, "lift_pct": 15.0},
            {"ts": 1704000000, "baseline_mean": 0.61, "rl_mean": 0.74, "lift_pct": 21.3},
            {"ts": 1706000000, "baseline_mean": 0.61, "rl_mean": 0.78, "lift_pct": 27.9},
        ],
        "latest_file": "(synthetic — run eval/rl_eval.py to generate real data)",
        "n_prompts":   12,
        "is_demo":     True,
    }
