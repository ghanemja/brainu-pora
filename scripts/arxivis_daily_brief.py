"""
arXivis daily brief — rerun the activation+novelty pipeline restricted to
papers in a recent date window, and emit a small JSON the UI can show as
"Today's pivotal papers."

Usage:
  python3 scripts/arxivis_daily_brief.py                  # last 30 days
  python3 scripts/arxivis_daily_brief.py --days 7         # last week
  python3 scripts/arxivis_daily_brief.py --top 10

Output: design/arxivis_daily.js
  window.ARXIVIS_DAILY = { window_days, top: [...papers], generated_at }

The script reads design/arxivis_data.js (must be generated first) and just
filters / re-ranks — no re-extraction.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARXIVIS_JS   = PROJECT_ROOT / "design" / "arxivis_data.js"
OUT_PATH     = PROJECT_ROOT / "design" / "arxivis_daily.js"


def load_arxivis() -> dict:
    if not ARXIVIS_JS.exists():
        sys.exit(f"missing {ARXIVIS_JS} — run scripts/build_arxivis_data.py first")
    text = ARXIVIS_JS.read_text()
    # Strip `window.ARXIVIS = ` prefix and trailing `;`
    start = text.find("{")
    end   = text.rfind("}")
    return json.loads(text[start:end + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30,
                    help="window in days (default 30; arXiv slice is small "
                         "so use a wide window unless you've refreshed corpus)")
    ap.add_argument("--top",  type=int, default=10, help="papers to keep")
    args = ap.parse_args()

    data = load_arxivis()
    papers = data["papers"]

    # Latest paper year in corpus is the anchor — most arXiv slice papers
    # don't have a real date, just yy from the id. Use that as a proxy.
    years = [p.get("year") for p in papers if p.get("year")]
    if not years:
        sys.exit("no dated papers in corpus")
    anchor_year = max(years)
    cutoff = anchor_year - max(1, args.days // 365)  # crude year cutoff

    recent = [p for p in papers if (p.get("year") or 0) >= cutoff]
    recent.sort(key=lambda p: -p["novelty_bits"])
    top = recent[: args.top]

    out = {
        "window_days":   args.days,
        "anchor_year":   anchor_year,
        "year_cutoff":   cutoff,
        "candidates":    len(recent),
        "top":           top,
        "generated_at":  datetime.now(timezone.utc).isoformat(),
    }
    js = "window.ARXIVIS_DAILY = " + json.dumps(out, indent=2, ensure_ascii=False) + ";\n"
    OUT_PATH.write_text(js)
    print(f"→ wrote {OUT_PATH} ({OUT_PATH.stat().st_size // 1024} KB)")
    print(f"  anchor year {anchor_year}, kept top {len(top)} of {len(recent)} recent papers")
    for p in top[:5]:
        print(f"  ◆ {p['novelty_bits']:5.1f}  {p['source']} {p.get('year')} — {p['title'][:80]}")


if __name__ == "__main__":
    main()
