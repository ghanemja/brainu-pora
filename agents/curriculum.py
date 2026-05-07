"""
Curriculum builder — turn a cluster of graph nodes into an interactive
lesson plan.

Two-tier:
  fast (no-LLM): pull the wiki page for each top node, slice intro paragraph
                 + key bullet points. Free, instant, but plain.
  rich (Claude): given a cluster's top_nodes + a learner's stated interest,
                 generate a structured lesson card (objective · prerequisites
                 · key idea · worked example · 3 quiz questions · "what's
                 next" recommendations). Cached per (node, interest) tuple.

Lesson card shape:
{
  "title":        str,
  "summary":      str,         # 2–3 sentences
  "key_ideas":    [str, …],
  "evidence":     [str, …],    # citations / urls
  "worked_example": str | None,
  "quiz":         [{"q": str, "a_choices":[…], "correct_idx": int, "why": str}],
  "next_in_cluster":   [str, …],   # other nodes user could go to
  "bridge_options":    [(node, cluster_id, cluster_name), …],
}

Cached to data/sessions/curriculum_cache.json keyed by (node, interest_hash).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"
LESSON_CACHE_PATH = PROJECT_ROOT / "data" / "sessions" / "curriculum_cache.json"
LESSON_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)


# ── Cache ──────────────────────────────────────────────────────────────────

def _load_cache() -> dict:
    if LESSON_CACHE_PATH.exists():
        try:
            return json.loads(LESSON_CACHE_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def _save_cache(c: dict) -> None:
    LESSON_CACHE_PATH.write_text(json.dumps(c, indent=2, default=str))


def _cache_key(node: str, interest: str, mode: str) -> str:
    h = hashlib.sha1(f"{node}|{interest}|{mode}".encode()).hexdigest()[:16]
    return h


# ── Wiki helpers ───────────────────────────────────────────────────────────

def _wiki_path_for(node_name: str) -> Path | None:
    """Best-effort mapping from a graph node label back to a wiki file."""
    candidates = [
        node_name,
        node_name.replace(" ", "_"),
        node_name.replace(" ", "-"),
        node_name.replace(" ", ""),
    ]
    for c in candidates:
        p = WIKI_CONCEPTS / f"{c}.md"
        if p.exists():
            return p
    # Case-insensitive fallback
    target = node_name.replace(" ", "_").lower()
    for p in WIKI_CONCEPTS.glob("*.md"):
        if p.stem.lower() == target:
            return p
    return None


def _wiki_intro(path: Path, max_chars: int = 1500) -> dict:
    """Return {summary, full} from a wiki page."""
    body = path.read_text(errors="ignore")
    # First paragraph that isn't a heading or empty
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    summary = ""
    for p in paras:
        # Skip pure-heading paragraphs (lines that all start with #)
        non_heading_lines = [
            ln for ln in p.splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")
        ]
        if non_heading_lines:
            summary = "\n".join(non_heading_lines).strip()
            break
    if not summary:
        summary = paras[0] if paras else body[:300]
    return {"summary": summary[:600], "full": body[:max_chars]}


def _extract_bullets(text: str, max_bullets: int = 5) -> list[str]:
    """Pull markdown bullet points (- foo, * foo) — quick "key ideas"."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("- ", "* ", "• ")):
            out.append(s[2:].strip())
            if len(out) >= max_bullets:
                break
    return out


# ── Fast (no-LLM) lesson card ──────────────────────────────────────────────

def fast_lesson(node: str, cluster, all_clusters: list = None,
                interest: str = "") -> dict:
    """Build a lesson card from wiki content alone, no API calls."""
    wiki = _wiki_path_for(node)
    if wiki is None:
        return _stub_lesson(node, cluster, all_clusters)

    intro = _wiki_intro(wiki)
    bullets = _extract_bullets(intro["full"])

    # Quiz: trivial completion-style q's from the intro paragraph
    quiz = _trivial_quiz(intro["summary"], node)

    next_in_cluster = [n for n, _ in (cluster.top_nodes or [])
                        if n.lower() != node.lower()][:5]
    bridge_options = []
    for bridge_node, other_cids in (cluster.bridges or []):
        for cid in other_cids:
            other = next((c for c in (all_clusters or []) if c.cluster_id == cid), None)
            if other:
                bridge_options.append((bridge_node, cid, other.name))

    return {
        "title":  node,
        "summary": intro["summary"],
        "key_ideas": bullets or [
            "Read the full wiki page for the formal definition.",
            "Work through one quantitative example.",
            "Note any open research questions in the page footer.",
        ],
        "evidence": [f"wiki/concepts/{wiki.name}"],
        "worked_example": None,
        "quiz": quiz,
        "next_in_cluster": next_in_cluster,
        "bridge_options": bridge_options[:5],
        "mode": "fast",
    }


def _trivial_quiz(text: str, node: str) -> list[dict]:
    """Generate one fill-in-the-blank style question + two distractors."""
    # Take a sentence containing the node name
    sentences = re.split(r"(?<=[.!?])\s+", text)
    target = next((s for s in sentences if node.lower() in s.lower()), None) \
             or (sentences[0] if sentences else "")
    if not target:
        return []
    return [{
        "q": f"True/false: this statement matches the wiki definition of {node!r}",
        "a_choices": [
            target.strip()[:200],
            f"{node} has no formal definition.",
            f"{node} is unrelated to the rest of this cluster.",
        ],
        "correct_idx": 0,
        "why": "Source statement is pulled directly from the wiki page intro.",
    }]


def _stub_lesson(node: str, cluster, all_clusters) -> dict:
    return {
        "title":  node,
        "summary": f"No wiki page found for {node!r}. This concept exists "
                   f"in the brain graph but lacks a synthesized writeup.",
        "key_ideas": [
            "Click 'open wiki' below — if missing, this is a candidate "
            "for a new wiki page.",
            "Look at neighbours in this cluster for related concepts.",
        ],
        "evidence": [],
        "worked_example": None,
        "quiz": [],
        "next_in_cluster": [n for n, _ in (cluster.top_nodes or [])
                             if n.lower() != node.lower()][:5],
        "bridge_options": [],
        "mode": "fast_stub",
    }


# ── Rich (Claude) lesson card ──────────────────────────────────────────────

RICH_SYSTEM = """You are an interactive engineering tutor. Given:
  - a topic (a node in our knowledge graph)
  - the topic's wiki content
  - a list of related topics in the same cluster
  - the learner's stated interest

…produce a one-screen lesson card. Be concrete and specific to the topic.
Output ONLY valid JSON with this shape (no preface, no markdown fence):

{
  "title": "<topic, human-readable>",
  "summary": "<2-3 sentence elevator description>",
  "key_ideas": ["<bullet>", ...],
  "evidence": ["<arxiv/wiki citation strings>", ...],
  "worked_example": "<one paragraph worked numeric example or null>",
  "quiz": [
    {"q": "<question>", "a_choices": ["<a>", "<b>", "<c>", "<d>"], "correct_idx": 0, "why": "<one-liner>"}
  ],
  "engagement_question": "<one open-ended prompt to keep the learner thinking>"
}

Rules:
  - 3 quiz questions, 4 choices each, varied correct_idx
  - quiz must be answerable from key_ideas alone
  - tie summary explicitly to the learner's interest if non-empty
  - worked_example must contain a number with units"""


def rich_lesson(node: str, cluster, all_clusters: list = None,
                interest: str = "", force: bool = False) -> dict:
    """Build a lesson card via Claude. Cached. Falls back to fast_lesson on error."""
    cache = _load_cache()
    key = _cache_key(node, interest, "rich")
    if not force and key in cache:
        cached = dict(cache[key])
        cached["mode"] = "rich_cached"
        # Merge in dynamic next/bridges (cluster might have changed since cache)
        cached.update({
            "next_in_cluster": _next_in_cluster(node, cluster),
            "bridge_options":  _bridge_options(cluster, all_clusters),
        })
        return cached

    wiki = _wiki_path_for(node)
    wiki_body = ""
    evidence_seed = []
    if wiki is not None:
        wiki_body = wiki.read_text(errors="ignore")[:3500]
        evidence_seed = [f"[[wiki/{wiki.stem}]]"]

    related = ", ".join(n for n, _ in (cluster.top_nodes or [])
                         if n.lower() != node.lower())[:400]
    user = f"""TOPIC: {node}
LEARNER INTEREST: {interest or '(unspecified)'}
RELATED TOPICS IN CLUSTER: {related}

--- WIKI CONTENT ---
{wiki_body or '(no wiki page; lean on the topic label and related topics)'}"""

    try:
        from .specialists import SYNTHESIZER_MODEL
        from .orchestrator import _call_claude
        raw = _call_claude(
            model=SYNTHESIZER_MODEL,
            system=RICH_SYSTEM,
            user=user,
            max_tokens=1200,
            retries=2,
        )
        parsed = _parse_lesson_json(raw)
        if not parsed:
            return fast_lesson(node, cluster, all_clusters, interest)
        # Merge dynamic cluster info
        parsed["next_in_cluster"] = _next_in_cluster(node, cluster)
        parsed["bridge_options"]  = _bridge_options(cluster, all_clusters)
        if evidence_seed and not parsed.get("evidence"):
            parsed["evidence"] = evidence_seed
        parsed["mode"] = "rich"
        # Cache the LLM-generated portion only (not the dynamic fields)
        to_cache = {k: v for k, v in parsed.items()
                    if k not in {"next_in_cluster", "bridge_options", "mode"}}
        cache[key] = to_cache
        _save_cache(cache)
        return parsed
    except Exception as e:
        fb = fast_lesson(node, cluster, all_clusters, interest)
        fb["mode"] = f"fast_fallback ({type(e).__name__})"
        return fb


def _parse_lesson_json(raw: str) -> dict | None:
    """Extract the JSON object from raw model output. Tolerates code fences."""
    raw = raw.strip()
    if raw.startswith("```"):
        # strip ``` fence
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def _next_in_cluster(node: str, cluster) -> list[str]:
    return [n for n, _ in (cluster.top_nodes or [])
             if n.lower() != node.lower()][:5]


def _bridge_options(cluster, all_clusters) -> list:
    out = []
    if not all_clusters:
        return out
    for bridge_node, other_cids in (cluster.bridges or []):
        for cid in other_cids:
            other = next((c for c in all_clusters if c.cluster_id == cid), None)
            if other:
                out.append((bridge_node, cid, other.name))
    return out[:5]


# ── Lesson dispatcher ──────────────────────────────────────────────────────

def lesson_for(node: str, cluster, all_clusters: list = None,
               interest: str = "", mode: str = "auto",
               force: bool = False) -> dict:
    """Dispatcher. mode ∈ {auto, fast, rich}.

    auto: rich if ANTHROPIC_API_KEY is set, else fast.
    """
    if mode == "fast":
        return fast_lesson(node, cluster, all_clusters, interest)
    if mode == "rich":
        return rich_lesson(node, cluster, all_clusters, interest, force=force)
    # auto
    if os.environ.get("ANTHROPIC_API_KEY"):
        return rich_lesson(node, cluster, all_clusters, interest, force=force)
    return fast_lesson(node, cluster, all_clusters, interest)
