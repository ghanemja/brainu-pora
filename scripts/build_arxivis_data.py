"""
arXivis pipeline — project papers onto the brain-university concept manifold.

For each paper (arXiv slice + defense corpus):
  1. Extract activated concepts via case-insensitive concept-name match.
  2. Score activations by TF-IDF over the concept vocabulary.
  3. Compute information-theoretic novelty:
        novelty_concept_bits = sum(-log p(c)) over activated concepts
        novelty_edge_bits    = #activated pairs never co-occurring before
                               in chronological-prior corpus
  4. Emit `design/arxivis_data.js` with PAPERS array ranked by total novelty.

Output schema (window.ARXIVIS):
  {
    papers: [{
      id, title, source, year, url,
      concepts: [{id, weight}],          # top-k activated wiki concept ids
      new_terms: [str],                  # high-tfidf terms not in vocab
      pair_edges: [[id_a, id_b], ...],   # activated concept pairs
      novelty_bits: float,
      pitch: str,                        # 30-sec elevator pitch
      category_hint: str,                # arxiv cat or defense topic
    }],
    concept_freq: {wiki_id: count},
    edge_freq:    {"a|b": count},
    generated_at: iso8601
  }

Run:
  python3 scripts/build_arxivis_data.py
  python3 scripts/build_arxivis_data.py --max-papers 800 --top-k 12
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.arxivis_innovations import extract_innovations, classify_against_vocab
from agents.arxivis_rigor import score_paper as score_rigor

WIKI_DIR        = PROJECT_ROOT / "wiki" / "concepts"
ARXIV_DIR       = PROJECT_ROOT / "data" / "raw" / "arxiv"
DEFENSE_MANI    = PROJECT_ROOT / "data" / "defense_corpus" / "MANIFEST.jsonl"
OUT_PATH        = PROJECT_ROOT / "design" / "arxivis_data.js"

TOKEN_RE   = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
STOP = {
    "the","and","for","from","with","this","that","via","into","based","using",
    "study","studies","approach","method","methods","model","models","system",
    "systems","analysis","data","paper","novel","new","review","survey",
    "introduction","framework","general","applied","applications","such","also",
    "show","shown","first","work","works","results","result","case","cases",
    "problem","problems","number","time","function","functions","theorem",
    "section","figure","table","note","notes","proof","proofs","corollary",
    "lemma","appendix","section","arxiv","abstract","keywords","conclusion",
    "however","therefore","hence","while","since","still","both","either",
    "many","most","more","much","very","each","some","when","where","what",
    "which","than","then","there","these","those","upon","over","under","above",
    "below","between","across","through","within","without","along","around",
    "another","others","may","can","could","would","should","might","must",
}


# ── Concept vocabulary ───────────────────────────────────────────────────

def load_concept_vocab() -> tuple[dict[str, dict], dict[str, str]]:
    """
    Return (concepts, name_index).

    concepts[wiki_id] = {
        id, display, slug, tokens, name_lc, page_terms (Counter)
    }
    name_index[name_lc] = wiki_id
    """
    concepts: dict[str, dict] = {}
    name_index: dict[str, str] = {}
    for p in sorted(WIKI_DIR.glob("*.md")):
        slug = p.stem                              # raw filename stem
        display = slug.replace("_", " ")
        name_lc = display.lower()
        wiki_id = f"wiki:{slug}"
        # page body terms
        text = p.read_text(errors="ignore")
        page_terms = Counter(
            t.lower() for t in TOKEN_RE.findall(text)
            if t.lower() not in STOP and len(t) > 3
        )
        # synonyms = parenthetical aliases in name e.g. "(MST)"
        aliases: list[str] = []
        if "(" in display and ")" in display:
            inner = display[display.find("(") + 1: display.rfind(")")]
            aliases.append(inner.lower().strip())
        concepts[wiki_id] = {
            "id":        wiki_id,
            "display":   display,
            "slug":      slug,
            "name_lc":   name_lc,
            "aliases":   aliases,
            "page_terms": page_terms,
        }
        name_index[name_lc] = wiki_id
        for a in aliases:
            if a and a not in name_index:
                name_index[a] = wiki_id
    return concepts, name_index


# ── Paper loaders ────────────────────────────────────────────────────────

def load_arxiv_papers(max_per_cat: int) -> list[dict]:
    """arXiv text papers; use first ~2000 chars."""
    out = []
    if not ARXIV_DIR.exists():
        return out
    for cat_dir in sorted(ARXIV_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        n = 0
        for p in sorted(cat_dir.glob("*.txt")):
            if n >= max_per_cat:
                break
            try:
                text = p.read_text(errors="ignore")
            except Exception:
                continue
            # first line ~ title (until blank), rest = body
            head = text[:200].strip()
            title = (head.splitlines()[0] or p.stem).strip()
            out.append({
                "id":            f"arx:{p.stem}",
                "title":         title,
                "source":        "arXiv",
                "year":          _parse_year_from_arxiv(p.stem),
                "url":           f"https://arxiv.org/abs/{p.stem}",
                "category_hint": cat_dir.name,
                "text":          text[:2500],
            })
            n += 1
    return out


def _parse_year_from_arxiv(stem: str) -> int | None:
    m = re.match(r"^(\d{2})(\d{2})", stem)
    if not m:
        return None
    yy = int(m.group(1))
    # arXiv yyMM: 25 → 2025, 95 → 1995 (heuristic; arXiv runs from 2007)
    return 2000 + yy if yy < 90 else 1900 + yy


def load_defense_papers() -> list[dict]:
    if not DEFENSE_MANI.exists():
        return []
    out = []
    for line in DEFENSE_MANI.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        title = (o.get("title") or "").strip()
        abstract = (o.get("abstract") or "").strip()
        if not title and not abstract:
            continue
        year = None
        if o.get("date"):
            m = re.match(r"(\d{4})", str(o["date"]))
            if m:
                year = int(m.group(1))
        src = o.get("source", "defense")
        # Normalize: arxiv-defense → "arXiv"; everything else uppercase
        src_label = "arXiv" if src.lower() == "arxiv" else src.upper()
        out.append({
            "id":            f"def:{o.get('id')}",
            "title":         title,
            "source":        src_label,
            "year":          year,
            "url":           o.get("url"),
            "category_hint": o.get("topic", ""),
            "text":          f"{title}\n\n{abstract}"[:2500],
        })
    return out


# ── Activation extractor ─────────────────────────────────────────────────

def build_term_idf(papers: list[dict]) -> dict[str, float]:
    df = Counter()
    for p in papers:
        seen = {t.lower() for t in TOKEN_RE.findall(p["text"])
                if t.lower() not in STOP and len(t) > 3}
        df.update(seen)
    N = len(papers) or 1
    return {t: math.log((N + 1) / (c + 1)) + 1.0 for t, c in df.items()}


def activations_for_paper(
    paper: dict,
    concepts: dict[str, dict],
    name_index: dict[str, str],
    idf: dict[str, float],
    top_k: int,
) -> tuple[list[tuple[str, float]], list[dict]]:
    """
    Return (top concepts with weight, innovations).
    """
    text = paper["text"]
    text_lc = text.lower()
    title_lc = paper["title"].lower()

    # 1. concept-name match (multiword: phrase substring search;
    #    single-word: word-boundary regex on the whole text)
    hits: dict[str, float] = {}
    for name_lc, wid in name_index.items():
        if len(name_lc) < 4 or name_lc in STOP:
            continue
        if " " in name_lc:
            n = text_lc.count(name_lc)
            if n:
                hits[wid] = hits.get(wid, 0.0) + n * 2.0  # phrase weight
                if name_lc in title_lc:
                    hits[wid] += 3.0
        else:
            # word-boundary regex (cached cheaply via str.split)
            tokens = TOKEN_RE.findall(text_lc)
            if not tokens:
                continue
            n = sum(1 for t in tokens if t == name_lc)
            if n:
                hits[wid] = hits.get(wid, 0.0) + n * 1.0
                if name_lc in title_lc.split():
                    hits[wid] += 2.0

    # 2. boost by IDF of concept slug (rare concepts → higher weight)
    scored = []
    for wid, raw in hits.items():
        slug_tokens = concepts[wid]["name_lc"].split()
        idf_score = sum(idf.get(tok, 1.0) for tok in slug_tokens) / max(len(slug_tokens), 1)
        scored.append((wid, raw * idf_score))
    scored.sort(key=lambda t: -t[1])
    top = scored[:top_k]

    # 3. Innovation extraction (named, claim-pattern, hyphen, k-prefix)
    raw_innov = extract_innovations(text, max_n=8)
    innovations = classify_against_vocab(raw_innov, name_index)

    return top, innovations


# ── Novelty metric ───────────────────────────────────────────────────────

def compute_novelty(
    papers_with_acts: list[tuple[dict, list[tuple[str, float]]]],
) -> tuple[Counter, Counter]:
    """Compute global concept_freq + co-occurrence edge_freq over all papers."""
    concept_freq: Counter = Counter()
    edge_freq:    Counter = Counter()
    for _, acts in papers_with_acts:
        ids = [a[0] for a in acts]
        for a in ids:
            concept_freq[a] += 1
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = sorted([ids[i], ids[j]])
                edge_freq[f"{a}|{b}"] += 1
    return concept_freq, edge_freq


def novelty_bits(
    acts: list[tuple[str, float]],
    innovations: list[dict],
    concept_freq: Counter,
    edge_freq: Counter,
    total_papers: int,
) -> tuple[float, dict]:
    if not acts:
        return 0.0, {"concept_bits": 0.0, "edge_bits": 0.0, "innovation_bonus": 0.0}
    ids = [a[0] for a in acts]
    # Concept rarity bits: -log p(c) summed, normalised
    concept_bits = 0.0
    for c in ids:
        p = (concept_freq[c] + 1) / (total_papers + len(concept_freq))
        concept_bits += -math.log2(p)
    concept_bits /= len(ids)
    # Edge novelty bits: pairs that have NEVER co-occurred elsewhere
    new_edges = 0
    rare_edges = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = sorted([ids[i], ids[j]])
            f = edge_freq.get(f"{a}|{b}", 0)
            if f <= 1:
                new_edges += 1
            elif f <= 3:
                rare_edges += 1
    edge_bits = new_edges * 1.5 + rare_edges * 0.5
    # Innovation bonus: weight "proposes" higher than "connects"
    innov_bonus = 0.0
    for i in innovations:
        innov_bonus += 0.8 if i["kind"] == "proposes" else 0.3
    total = concept_bits + edge_bits + innov_bonus
    return total, {
        "concept_bits":     round(concept_bits, 2),
        "edge_bits":        round(edge_bits, 2),
        "innovation_bonus": round(innov_bonus, 2),
    }


# ── Elevator pitch ───────────────────────────────────────────────────────

_RE_EMAIL  = re.compile(r"\S+@\S+\.\S+")
_RE_AFFIL  = re.compile(r"\b(?:university|institute|college|laboratory|laboratoire|inc\.?|llc|gmbh|ltd\.?|corp\.?|hospital|department|école|universität|università|universidad)\b", re.I)
_RE_DAGGER = re.compile(r"[\*†‡§¶#0-9]{1,3}\s*$")
_RE_NAME_BIB = re.compile(r"^[A-Z][a-zA-Z'.-]+(?:\s+[A-Z][a-zA-Z'.-]+){0,3}$")


_RE_TOC_LINE  = re.compile(r"^\s*\d+(\.\d+)*(\s+[A-Z][\w\s-]+)?\s*$")
_RE_PAGE_NUM  = re.compile(r"^\s*\d{1,3}\s*$")
_RE_SECTION_H = re.compile(r"^\s*\d+(\.\d+)*\s+[A-Z]")  # "1 Introduction" / "2.3 Method"


_TOC_KEYWORDS = {
    "contents", "abstract", "introduction", "references", "bibliography",
    "acknowledgments", "acknowledgements", "appendix", "notation",
    "preliminaries", "background", "related work", "conclusion",
    "discussion", "results", "methods", "method", "table of contents",
    "future work",
}


def _clean_body(text: str) -> str:
    """Drop TOC entries, page numbers, lone section headers / keywords."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            out.append("")
            continue
        if _RE_TOC_LINE.match(s) or _RE_PAGE_NUM.match(s):
            continue
        if len(s) < 30 and _RE_SECTION_H.match(s):
            continue
        # Drop lone TOC keywords
        if s.lower().rstrip(".:") in _TOC_KEYWORDS:
            continue
        out.append(line)
    return "\n".join(out)


def _strip_author_block(text: str) -> str:
    """Strip leading title/author/affil lines until we hit the abstract."""
    text = _clean_body(text)
    lines = text.splitlines()
    # Find "Abstract" line and start after it
    for i, line in enumerate(lines):
        if line.strip().lower() in ("abstract", "abstract.", "abstract:"):
            return "\n".join(lines[i+1:]).strip()
    # Otherwise drop the first ~12 lines if they look like author block
    out_start = 0
    for i, line in enumerate(lines[:25]):
        s = line.strip()
        if not s:
            continue
        if _RE_EMAIL.search(s) or _RE_AFFIL.search(s) or _RE_DAGGER.search(s):
            out_start = i + 1
            continue
        if _RE_NAME_BIB.match(s):
            out_start = i + 1
            continue
        # First substantive line — keep
        break
    return "\n".join(lines[out_start:]).strip()


def make_pitch(paper: dict, acts: list[tuple[str, float]],
               concepts: dict[str, dict], innovations: list[dict]) -> str:
    body = _strip_author_block(paper["text"])
    # First sentence that starts w/ "We ", "This paper", "Our ", "In this",
    # otherwise first 1-2 sentences >=40 chars
    sents_all = SENT_SPLIT.split(body)
    sents_clean = []
    for s in sents_all:
        s = re.sub(r"\s+", " ", s).strip(" ,.;:()[]")
        if 40 < len(s) < 280:
            sents_clean.append(s)
    # Prioritize sentences that look authorial
    authorial = [s for s in sents_clean if re.match(r"^(We |This (?:paper|work|study|note) |Our |In this |The (?:main|key|primary))", s)]
    picks = (authorial + sents_clean)[:2]
    pitch_core = " ".join(picks).strip()
    if not pitch_core:
        pitch_core = body[:240].strip()
    return pitch_core


def make_key_finding(innovations: list[dict], concepts: dict[str, dict],
                     acts: list[tuple[str, float]]) -> str:
    """One-line headline for video + UI — the single most-important claim."""
    # Prefer first "proposes" innovation, then any innovation, then top concept
    for innov in innovations:
        if innov.get("kind") == "proposes":
            return innov["phrase"]
    if innovations:
        return innovations[0]["phrase"]
    if acts:
        return concepts[acts[0][0]]["display"]
    return ""


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-per-cat",  type=int, default=80,
                    help="arXiv papers per category (default 80)")
    ap.add_argument("--top-k",        type=int, default=12,
                    help="top activated concepts per paper")
    ap.add_argument("--keep-top",     type=int, default=600,
                    help="papers to emit (ranked by novelty)")
    args = ap.parse_args()

    t0 = time.time()
    print("→ load concept vocab", flush=True)
    concepts, name_index = load_concept_vocab()
    print(f"  {len(concepts)} concepts, {len(name_index)} name aliases")

    print("→ load papers", flush=True)
    arx = load_arxiv_papers(args.max_per_cat)
    deff = load_defense_papers()
    papers = arx + deff
    print(f"  {len(arx)} arxiv + {len(deff)} defense = {len(papers)}")

    print("→ build idf", flush=True)
    idf = build_term_idf(papers)

    print("→ extract activations + innovations", flush=True)
    acts_per_paper: list[tuple[dict, list[tuple[str, float]], list[dict]]] = []
    for i, p in enumerate(papers):
        acts, innovations = activations_for_paper(p, concepts, name_index, idf, args.top_k)
        acts_per_paper.append((p, acts, innovations))
        if (i + 1) % 500 == 0:
            print(f"  {i+1}/{len(papers)}")

    print("→ compute corpus frequencies", flush=True)
    concept_freq, edge_freq = compute_novelty([(p, a) for p, a, _ in acts_per_paper])

    print("→ score novelty per paper", flush=True)
    enriched = []
    for p, acts, innovations in acts_per_paper:
        if not acts:
            continue
        score, breakdown = novelty_bits(acts, innovations, concept_freq, edge_freq, len(papers))
        pair_edges = []
        ids = [a[0] for a in acts]
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = sorted([ids[i], ids[j]])
                pair_edges.append([a, b])
        rigor = score_rigor(p)
        composite = round(score + rigor["total"], 2)
        enriched.append({
            "id":            p["id"],
            "title":         p["title"][:240],
            "source":        p["source"],
            "year":          p.get("year"),
            "url":           p.get("url"),
            "category_hint": p.get("category_hint", ""),
            "concepts": [
                {"id": a, "weight": round(w, 3),
                 "name": concepts[a]["display"]}
                for a, w in acts
            ],
            "innovations":   innovations,
            "pair_edges":    pair_edges,
            "novelty_bits":  round(score, 2),
            "novelty_breakdown": breakdown,
            "rigor":         rigor,
            "composite":     composite,
            "pitch":         make_pitch(p, acts, concepts, innovations),
            "key_finding":   make_key_finding(innovations, concepts, acts),
        })

    enriched.sort(key=lambda x: -x["composite"])
    keep = enriched[: args.keep_top]
    print(f"→ kept top {len(keep)}/{len(enriched)} by novelty")

    # Concept universe: every concept referenced by ANY kept paper.
    # Each node gets a degree (count of papers activating it) and a cluster
    # (cluster_id = id within first 12 clusters by paper count, else 11).
    universe_ids: set[str] = set()
    for p in keep:
        for c in p["concepts"]:
            universe_ids.add(c["id"])

    # Cluster-by-cooccurrence: simple greedy — pick top-12 most-frequent
    # concepts as cluster seeds; assign each remaining concept to the
    # seed it co-occurs most with.
    cf = Counter()
    for p in keep:
        for c in p["concepts"]:
            if c["id"] in universe_ids:
                cf[c["id"]] += 1
    seeds = [c for c, _ in cf.most_common(12)]
    seed_idx = {c: i for i, c in enumerate(seeds)}
    # Build co-occurrence
    cooc: dict[tuple[str,str], int] = defaultdict(int)
    for p in keep:
        ids = [c["id"] for c in p["concepts"]]
        for a in ids:
            for b in ids:
                if a != b:
                    cooc[(a, b)] += 1
    cluster_of: dict[str, int] = dict(seed_idx)
    for cid in universe_ids:
        if cid in cluster_of:
            continue
        best, best_count = 0, -1
        for s in seeds:
            c = cooc.get((cid, s), 0)
            if c > best_count:
                best, best_count = seed_idx[s], c
        cluster_of[cid] = best

    universe_nodes = []
    for cid in universe_ids:
        slug = cid.replace("wiki:", "")
        universe_nodes.append({
            "id":      slug,
            "name":    concepts.get(cid, {}).get("display") or slug.replace("_", " "),
            "cluster": cluster_of.get(cid, 0),
            "degree":  cf.get(cid, 1),
            "kind":    "wiki",
        })

    # Concept edges: every pair_edge across kept papers, deduplicated + weighted
    edge_weight: Counter = Counter()
    for p in keep:
        for a, b in p["pair_edges"]:
            key = tuple(sorted([a.replace("wiki:", ""), b.replace("wiki:", "")]))
            edge_weight[key] += 1
    universe_edges = [list(k) + [v] for k, v in edge_weight.items()]

    # Emit JS
    out = {
        "papers":          keep,
        "concept_universe": universe_nodes,
        "concept_edges":    universe_edges,
        "concept_freq":    dict(concept_freq.most_common(400)),
        "edge_freq":       dict(edge_freq.most_common(400)),
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total_papers_scanned":   len(papers),
            "papers_with_acts":       len(enriched),
            "concepts_in_vocab":      len(concepts),
            "concept_universe_size":  len(universe_nodes),
            "concept_edges_count":    len(universe_edges),
            "elapsed_s":              round(time.time() - t0, 1),
        },
    }
    js = "window.ARXIVIS = " + json.dumps(out, indent=2, ensure_ascii=False) + ";\n"
    OUT_PATH.write_text(js)
    sz_kb = OUT_PATH.stat().st_size / 1024
    print(f"→ wrote {OUT_PATH} ({sz_kb:.0f} KB) in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
