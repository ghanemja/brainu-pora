"""
"Why am I confused" detector.

Frontend instruments every reading paragraph with fine-grained telemetry:
  - paragraph dwell time
  - scroll-back events (entered viewport, exited, re-entered)
  - re-read count
  - explicit "I'm stuck" clicks

We persist per (user, paragraph_hash) signals + compute a confusion score.
When the score crosses a threshold, the UI offers an auto-ELI5 of just
that paragraph — no whole-page restart.

Public:
  log_signal(user_id, paragraph_hash, signal_kind, value=1.0)
  score(user_id, paragraph_hash) -> float in [0, 1]
  eli5(paragraph_text)            -> str
  hotspots(user_id, top_k=5)      -> list[{paragraph_hash, score}]

Signal kinds + weights:
  dwell_s          0.04  per second beyond 30s
  reread           0.20  per re-entry into viewport after leaving
  scrollback       0.15  per scroll-up while in paragraph
  stuck_click      0.50  explicit "I'm stuck" press

Score clamps to [0,1]. Threshold for offering ELI5: 0.55.
"""

from __future__ import annotations

import hashlib


SIGNAL_WEIGHTS = {
    "dwell_s":     0.04,
    "reread":      0.20,
    "scrollback":  0.15,
    "stuck_click": 0.50,
}
THRESHOLD = 0.55


def paragraph_hash(text: str) -> str:
    return hashlib.sha1((text or "").strip().encode()).hexdigest()[:12]


# ── Persistence (lightweight table; lazy-creates) ─────────────────────────

def _ensure_table(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS confusion_signals (
          user_id        TEXT NOT NULL,
          paragraph_hash TEXT NOT NULL,
          signal_kind    TEXT NOT NULL,
          value          REAL NOT NULL,
          ts             REAL NOT NULL
        )
    """)
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_confusion_user_para
        ON confusion_signals(user_id, paragraph_hash)
    """)


def log_signal(user_id: str, paragraph_hash_str: str,
               signal_kind: str, value: float = 1.0) -> None:
    if signal_kind not in SIGNAL_WEIGHTS:
        return
    import time
    from .persistence import open_db
    db = open_db()
    _ensure_table(db)
    db.execute(
        """INSERT INTO confusion_signals
             (user_id, paragraph_hash, signal_kind, value, ts)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, paragraph_hash_str, signal_kind, float(value), time.time()),
    )
    db.commit()


def score(user_id: str, paragraph_hash_str: str) -> float:
    """Aggregate signals for one paragraph → score in [0, 1]."""
    from .persistence import open_db
    db = open_db()
    _ensure_table(db)
    rows = db.execute(
        """SELECT signal_kind, value FROM confusion_signals
             WHERE user_id = ? AND paragraph_hash = ?""",
        (user_id, paragraph_hash_str),
    ).fetchall()
    agg = 0.0
    for kind, value in rows:
        weight = SIGNAL_WEIGHTS.get(kind, 0.0)
        if kind == "dwell_s":
            extra = max(0.0, value - 30.0)
            agg += weight * extra
        else:
            agg += weight * value
    return max(0.0, min(1.0, agg))


def hotspots(user_id: str, top_k: int = 5) -> list[dict]:
    """List the user's most-confusing paragraphs across the corpus."""
    from .persistence import open_db
    db = open_db()
    _ensure_table(db)
    rows = db.execute(
        """SELECT paragraph_hash
             FROM confusion_signals
             WHERE user_id = ?
             GROUP BY paragraph_hash""",
        (user_id,),
    ).fetchall()
    out = []
    for (ph,) in rows:
        out.append({"paragraph_hash": ph, "score": score(user_id, ph)})
    out.sort(key=lambda d: -d["score"])
    return out[:top_k]


# ── ELI5 generator ────────────────────────────────────────────────────────

ELI5_SYSTEM = """You are a tutor unpacking ONE confusing paragraph.

Rules:
- The paragraph below tripped someone up. Don't explain the whole topic —
  just this paragraph.
- Output exactly 3 short outputs in this JSON shape:
  {
    "plain":   "<60-word plain-English rewrite, no jargon>",
    "concrete":"<one concrete example with numbers / units>",
    "trap":    "<the specific misconception this paragraph invites>"
  }

OUTPUT: valid JSON only, no preface, no fence."""


def eli5(paragraph_text: str) -> dict | None:
    """Generate a sentence-level ELI5 for one paragraph."""
    if not paragraph_text or not paragraph_text.strip():
        return None
    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=ELI5_SYSTEM,
            user=f"PARAGRAPH:\n\n{paragraph_text[:2000]}",
            max_tokens=500,
            retries=2,
        )
    except Exception:
        return None
    import json, re
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
