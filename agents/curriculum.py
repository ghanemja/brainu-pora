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
DEFENSE_CORPUS_PATH = PROJECT_ROOT / "data" / "defense_corpus_samples.json"
LESSON_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)


# ── Defense corpus helpers ─────────────────────────────────────────────────

def _load_defense_corpus() -> dict:
    """Load defense corpus samples for evidence enrichment."""
    if DEFENSE_CORPUS_PATH.exists():
        try:
            return json.loads(DEFENSE_CORPUS_PATH.read_text())
        except json.JSONDecodeError:
            return {"papers": []}
    return {"papers": []}


def _defense_papers_for_topics(topics: list[str], node: str = "") -> list[str]:
    """Find defense papers matching given topics or node keywords."""
    corpus = _load_defense_corpus()
    papers = corpus.get("papers", [])

    # Build keyword set: node name + topics
    keywords = set()
    keywords.add(node.lower())
    keywords.update(t.lower() for t in topics if t and len(t) > 3)
    # Extract word stems
    keywords.update(w for t in topics for w in t.lower().split() if len(w) > 3)

    matches = []
    for paper in papers:
        paper_topics = [t.lower() for t in paper.get("topics", [])]
        paper_title = paper.get("title", "").lower()

        # Score: how many keywords appear in paper topics or title
        score = sum(1 for kw in keywords
                   if any(kw in pt for pt in paper_topics) or kw in paper_title)
        if score > 0:
            matches.append((score, f"def/{paper['id']}"))

    # Sort by score, return top 2
    matches.sort(reverse=True, key=lambda x: x[0])
    return [m[1] for m in matches[:2]]


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

    # Build evidence: wiki + defense corpus papers
    evidence = [f"wiki/concepts/{wiki.name}"]
    # Extract topics from key ideas / bullets for matching defense papers
    topics = bullets + [node]
    defense_papers = _defense_papers_for_topics(topics, node)
    evidence.extend(defense_papers)

    return {
        "title":  node,
        "summary": intro["summary"],
        "key_ideas": bullets or [
            "Read the full wiki page for the formal definition.",
            "Work through one quantitative example.",
            "Note any open research questions in the page footer.",
        ],
        "evidence": evidence,
        "worked_example": None,
        "quiz": quiz,
        "next_in_cluster": next_in_cluster,
        "bridge_options": bridge_options[:5],
        "mode": "fast",
    }


def _validate_quiz(quiz, node: str, text: str = "") -> list[dict]:
    """Repair/validate an LLM-produced quiz so the frontend never receives a
    malformed item. Drops items that can't be repaired; falls back to the
    deterministic _trivial_quiz if nothing valid remains.

    Guarantees each returned item: q:str, a_choices:list[>=2 str],
    correct_idx:int in [0, len(a_choices)), why:str.
    """
    out: list[dict] = []
    for item in (quiz or []):
        if not isinstance(item, dict):
            continue
        q = str(item.get("q") or "").strip()
        choices = item.get("a_choices") or item.get("choices") or []
        if not isinstance(choices, list):
            continue
        choices = [str(c).strip() for c in choices if str(c).strip()]
        # de-dup while preserving order
        seen, deduped = set(), []
        for c in choices:
            if c.lower() not in seen:
                seen.add(c.lower())
                deduped.append(c)
        choices = deduped
        if not q or len(choices) < 2:
            continue
        idx = item.get("correct_idx", item.get("correct", 0))
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            idx = 0
        if not (0 <= idx < len(choices)):
            idx = 0  # clamp rather than mark nothing correct
        out.append({
            "q": q,
            "a_choices": choices[:4],
            "correct_idx": min(idx, len(choices[:4]) - 1),
            "why": str(item.get("why") or "").strip()
                   or "Grounded in the lesson's key ideas.",
        })
    if not out:
        return _trivial_quiz(text, node)
    return out[:3]


def _trivial_quiz(text: str, node: str) -> list[dict]:
    """Build a content-grounded multiple-choice question from wiki text.

    Deterministic, no LLM (this is the offline fallback). Picks a salient
    sentence about ``node``, turns it into a real "what is true about X"
    question, and synthesises three plausible distractors by mechanically
    altering the claim (negation, scope/cause-effect inversion, sibling swap).

    Returns the same shape as the rich quiz:
        [{"q", "a_choices": [4 strings], "correct_idx": int, "why": str}]
    correct_idx is chosen deterministically from the node name so it varies
    across nodes rather than always being 0.
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return []

    # Prefer a descriptive sentence that mentions the node and reads like a
    # claim about it ("X is/are/refers to/describes..."), else any sentence
    # mentioning the node, else the first sentence (usually the definition).
    nl = node.lower()
    def _score(s: str) -> int:
        sl = s.lower()
        sc = 0
        if nl in sl:
            sc += 2
        if re.search(r"\b(is|are|refers to|describes|means|consists of|"
                     r"enables|allows|provides|uses|defines)\b", sl):
            sc += 1
        if 40 <= len(s) <= 220:  # avoid stubs and runaway sentences
            sc += 1
        return sc

    target = max(sentences, key=_score)
    claim = target.rstrip(".!?").strip()
    claim = claim[:200]
    if not claim:
        return []

    # ── Distractor 1: negate the core verb of the claim ────────────────────
    negations = [
        (r"\bis not\b", "is"),
        (r"\bare not\b", "are"),
        (r"\bcannot\b", "can"),
        (r"\bis\b", "is not"),
        (r"\bare\b", "are not"),
        (r"\bcan\b", "cannot"),
        (r"\benables\b", "prevents"),
        (r"\ballows\b", "prevents"),
        (r"\bincreases\b", "decreases"),
        (r"\bdecreases\b", "increases"),
        (r"\brequires\b", "does not require"),
    ]
    negated = None
    for pat, repl in negations:
        new, n = re.subn(pat, repl, claim, count=1, flags=re.IGNORECASE)
        if n:
            negated = new
            break
    if negated is None:
        negated = f"{node} has no measurable effect on the systems it appears in"

    # ── Distractor 2: cause/effect or scope inversion ──────────────────────
    swapped = f"{node} is a downstream consequence of the concepts it actually drives"

    # ── Distractor 3: right-idea-wrong-scope (a sibling-style property) ─────
    wrong_scope = (f"{node} only applies in a single special case and does not "
                   f"generalize to the broader cluster")

    choices = [claim, negated.strip()[:200], swapped, wrong_scope]

    # Deterministically rotate which slot holds the correct answer so the
    # answer isn't always index 0 (varies per node, no randomness).
    correct_idx = (sum(ord(c) for c in node) % 4) if node else 0
    if correct_idx != 0:
        choices[0], choices[correct_idx] = choices[correct_idx], choices[0]

    return [{
        "q": f"Based on the source material, which statement about {node} is correct?",
        "a_choices": choices,
        "correct_idx": correct_idx,
        "why": (f"The correct choice is taken directly from the wiki description "
                f"of {node}. The most tempting distractor simply negates or "
                f"inverts that claim (e.g. flipping cause and effect or denying "
                f"the stated relationship), which is a common misreading."),
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
  - tie summary explicitly to the learner's interest if non-empty
  - worked_example must contain a number with units

Quiz rules (these are strict — weak quizzes are the #1 failure mode):
  - Exactly 3 questions. Each has exactly 4 choices. Vary correct_idx across
    the three questions (do NOT make them all the same index; use a mix).
  - Every question must probe a MECHANISM, a CONSEQUENCE, or a DISTINCTION —
    i.e. test whether the learner understands *why/how* something works or
    *how two things differ*. Good stems: "Why does X cause Y?", "What happens
    to Z if W increases?", "What distinguishes X from the related concept Y?",
    "Which step is responsible for <observed effect>?".
  - NEVER write meta/trivia questions. Forbidden: anything about whether a
    topic is on the exam, newest, oldest, easiest, hardest, most popular,
    most cited, or otherwise testing recall of labels rather than understanding.
  - All 4 choices must be domain-specific, on-topic, and individually plausible
    to someone who only half-understands the material. NO throwaway, joke, or
    obviously-wrong options ("none of the above", "it does nothing", etc.).
  - The 3 distractors must each encode a REALISTIC misconception a learner
    could actually hold — e.g. a subtly wrong mechanism, a swapped cause and
    effect, or a right-idea-applied-at-the-wrong-scope. Make them tempting.
  - Every question (and its correct answer + all distractors) must be
    answerable and judgeable from key_ideas alone. Do not require outside facts.
  - "why" must (a) explain why the correct choice is right, AND (b) explicitly
    name the misconception that the most tempting distractor encodes, so the
    learner sees the trap. Example shape: "<correct> because <mechanism>. The
    tempting wrong answer assumes <misconception>, which conflates <X> with <Y>."""


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
        # Validate/repair the quiz so a malformed LLM response can't reach the
        # frontend (out-of-range correct_idx breaks answer-marking + remediation).
        parsed["quiz"] = _validate_quiz(parsed.get("quiz"), node, text=wiki_body)
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
