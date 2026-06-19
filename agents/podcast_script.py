"""
Podcast script generator — turn a paper, wiki concept, or cluster into a
two-host conversational dialogue (NotebookLM-style).

Inputs:
  - Source text (paper abstract+intro, wiki concept body, or merged cluster)
  - Topic name
  - Target length (short=3min / medium=8min / long=15min)

Output:
  PodcastScript {
    title: str
    summary: str
    duration_target_s: int
    chapters: [Chapter]
    turns: [Turn]              # ordered dialogue beats
  }

Turn shape (drives audio + visuals downstream):
  {
    "speaker": "A" | "B",      # A = curious learner, B = expert guide
    "text":    str,            # what they say
    "visual":  str | None,     # slide cue: "title", "eq:E=mc^2", "diagram:X"
    "beat":    str | None,     # "hook" | "explain" | "example" | "callback"
    "chapter": int             # index into chapters[]
  }

Cached: data/sessions/podcast_cache/<hash>.json
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "sessions" / "podcast_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


LENGTHS = {
    "short":  {"seconds": 180,  "turns": 24,  "tokens": 1500},
    "medium": {"seconds": 480,  "turns": 60,  "tokens": 3000},
    "long":   {"seconds": 900,  "turns": 110, "tokens": 5000},
}


SYSTEM_PROMPT = """You are a podcast scriptwriter for a research-explainer show.
Two hosts:
  HOST A — curious learner. Asks "why", flags confusion, prompts callbacks.
  HOST B — expert guide. Explains, grounds claims in source, builds intuition.

Given source material + topic, write a natural conversational episode.

RULES:
- Banter, not monologue. A and B trade turns frequently (3-15s per turn).
- Open with a HOOK turn from A ("ok so this paper claims X — that sounds wrong, right?").
- Every technical claim B makes is followed by A reacting (paraphrase, push back, or ask).
- Use callbacks ("wait, earlier you said...") — at least 2 across the episode.
- Worked numeric example with a real number + units, mid-episode.
- Close with a "what surprised me" reflection from A.

VISUAL CUES (visual field per turn, null if none):
  "title:<text>"        — flash a title card
  "eq:<latex>"          — render equation
  "diagram:<concept>"   — show a diagram of named concept
  "graph:<node>"        — pan to that node in the 3D mind map
  "quote:<paper_id>"    — overlay source quote
Use sparingly — 1 visual per 3-5 turns. Drop visual:null for most beats.

OUTPUT: valid JSON ONLY, no preface, no fence:
{
  "title": "<episode title>",
  "summary": "<one-paragraph episode description>",
  "chapters": [
    {"title": "<chapter title>", "summary": "<one sentence>"}
  ],
  "turns": [
    {"speaker": "A", "text": "<line>", "visual": null, "beat": "hook", "chapter": 0}
  ]
}
"""


def generate_script(
    *,
    topic: str,
    source_text: str,
    length: str = "medium",
    angle: str = "",
    force: bool = False,
) -> dict | None:
    """Generate a two-host podcast script for `topic` from `source_text`.

    Returns the script dict or None if Claude is unavailable.
    """
    cfg = LENGTHS.get(length, LENGTHS["medium"])
    key = _cache_key(topic, source_text, length, angle)
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists() and not force:
        try:
            return json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            pass

    user_msg = (
        f"TOPIC: {topic}\n"
        f"TARGET LENGTH: ~{cfg['seconds']}s (~{cfg['turns']} turns)\n"
        f"ANGLE: {angle or '(open — pick the most surprising thread)'}\n\n"
        f"--- SOURCE ---\n{source_text[:8000]}"
    )

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=SYSTEM_PROMPT,
            user=user_msg,
            max_tokens=cfg["tokens"],
            retries=2,
        )
    except Exception:
        return None

    parsed = _parse_json(raw)
    if not parsed or not parsed.get("turns"):
        return None
    parsed["duration_target_s"] = cfg["seconds"]
    parsed["topic"] = topic
    parsed["length"] = length

    cache_file.write_text(json.dumps(parsed, indent=2))
    return parsed


def _cache_key(topic: str, source: str, length: str, angle: str) -> str:
    blob = json.dumps({
        "topic": topic,
        "src_hash": hashlib.sha1(source.encode()).hexdigest()[:16],
        "length": length,
        "angle": angle,
    }, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def _parse_json(raw: str) -> dict | None:
    raw = raw.strip()
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


# ── Source builders ────────────────────────────────────────────────────────

def source_from_wiki(node: str) -> str:
    """Pull wiki page body for `node`."""
    from .curriculum import _wiki_path_for
    p = _wiki_path_for(node)
    if p is None:
        return ""
    return p.read_text(errors="ignore")[:6000]


def source_from_paper(paper_id: str) -> str:
    """Pull paper title+abstract+intro from defense corpus."""
    corpus_path = PROJECT_ROOT / "data" / "defense_corpus_samples.json"
    if not corpus_path.exists():
        return ""
    try:
        corpus = json.loads(corpus_path.read_text())
    except json.JSONDecodeError:
        return ""
    for paper in corpus.get("papers", []):
        if paper.get("id") == paper_id:
            parts = [
                f"TITLE: {paper.get('title', '')}",
                f"AUTHORS: {paper.get('authors', '')}",
                f"ABSTRACT: {paper.get('abstract', '')}",
                f"TOPICS: {', '.join(paper.get('topics', []))}",
            ]
            if paper.get("intro"):
                parts.append(f"INTRO: {paper['intro']}")
            return "\n\n".join(parts)
    return ""


def source_from_cluster(cluster, max_chars: int = 6000) -> str:
    """Merge top wiki pages from a cluster into one source blob."""
    from .curriculum import _wiki_path_for
    parts = [f"CLUSTER: {getattr(cluster, 'name', '?')}"]
    used = 0
    for node, _score in (cluster.top_nodes or [])[:6]:
        p = _wiki_path_for(node)
        if p is None:
            continue
        body = p.read_text(errors="ignore")[:1500]
        chunk = f"\n--- {node} ---\n{body}"
        if used + len(chunk) > max_chars:
            break
        parts.append(chunk)
        used += len(chunk)
    return "\n".join(parts)


# ── Validation ─────────────────────────────────────────────────────────────

def validate(script: dict) -> list[str]:
    """Sanity-check a parsed script. Returns list of issues (empty = ok)."""
    issues = []
    turns = script.get("turns") or []
    if len(turns) < 6:
        issues.append(f"too few turns ({len(turns)})")
    speakers = {t.get("speaker") for t in turns}
    if speakers - {"A", "B"}:
        issues.append(f"bad speakers: {speakers}")
    if "A" not in speakers or "B" not in speakers:
        issues.append("missing one host")
    # check for hook beat at start
    if turns and turns[0].get("beat") != "hook":
        issues.append("first turn isn't a hook")
    # chapter consistency
    chs = script.get("chapters") or []
    for t in turns:
        ci = t.get("chapter", 0)
        if ci >= len(chs):
            issues.append(f"turn references chapter {ci} but only {len(chs)} chapters")
            break
    return issues
