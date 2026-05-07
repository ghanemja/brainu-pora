"""
Unified academic + defense corpus graph.

Builds one networkx graph with three node kinds, color-coded for the 3D
viz so a learner can see how the wiki, the defense corpus, and the arXiv
slice all relate.

Node kinds:
  wiki:<stem>        local concept page          (concept-level)
  def:<id>           defense corpus paper        (paper-level — DTIC,
                                                   NTRS, OpenAlex,
                                                   arXiv-defense)
  arx:<category>     arXiv category aggregate    (category-level — too
                                                   many individual papers
                                                   to render; show one
                                                   super-node per cat)

Edges:
  wiki ↔ wiki         existing wikilinks (from obsidian_loader)
  def  ↔ def          same `topic` field in MANIFEST.jsonl
  wiki ↔ def          title-token overlap (≥ 2 shared tokens)
  wiki ↔ arx          wiki page name appears in arxiv chunks
  def  ↔ arx          defense topic ↔ arxiv category map (hand-tuned)

All node attrs include `kind` (wiki/def/arx) so the 3D viz can color
by source. Colors:
  wiki: cluster color (existing palette)
  def:  amber #FBB036
  arx:  sky #7DD3FC

Public:
  build_mixed_graph(vault_path=None, max_def=1500, max_arx_papers_per_cat=20)
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"
DEFENSE_MANIFEST = PROJECT_ROOT / "data" / "defense_corpus" / "MANIFEST.jsonl"
ARXIV_DIR = PROJECT_ROOT / "data" / "raw" / "arxiv"

TOK = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")
STOP = {
    "the", "and", "for", "from", "with", "this", "that", "via", "into",
    "based", "using", "study", "studies", "approach", "method", "methods",
    "model", "models", "system", "systems", "analysis", "data", "paper",
    "novel", "new", "review", "survey", "introduction", "framework",
    "general", "applied", "applications",
}


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in TOK.findall(text or "")
            if len(t) > 3 and t.lower() not in STOP}


# ── Load defense manifest ─────────────────────────────────────────────────

def _load_defense() -> list[dict]:
    if not DEFENSE_MANIFEST.exists():
        return []
    out = []
    for line in DEFENSE_MANIFEST.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("title") or obj.get("abstract"):
            out.append(obj)
    return out


# ── Load arxiv summary ────────────────────────────────────────────────────

def _load_arxiv_categories(max_per_cat: int = 20) -> dict[str, dict]:
    """Return {category: {n_papers, sample_titles, all_tokens}}.

    Reads each .txt file's first ~1500 chars to grab the title + abstract
    region. Samples up to `max_per_cat` papers per category for the
    title-token bag (more = slower for cross-edges).
    """
    out: dict[str, dict] = {}
    if not ARXIV_DIR.exists():
        return out
    for cat_dir in sorted(ARXIV_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        cat = cat_dir.name
        files = sorted(cat_dir.glob("*.txt"))
        if not files:
            continue
        all_tokens: set[str] = set()
        sample_titles: list[str] = []
        for txt in files[:max_per_cat]:
            try:
                head = txt.read_text(errors="ignore")[:2000]
            except Exception:
                continue
            # First non-empty, non-author-list line → title heuristic
            for line in head.splitlines():
                line = line.strip()
                if line and len(line) > 6 and len(line) < 200:
                    sample_titles.append(line)
                    all_tokens |= _tokens(line)
                    break
        out[cat] = {
            "n_papers": len(files),
            "sample_titles": sample_titles[:5],
            "tokens": all_tokens,
        }
    return out


# ── Defense topic ↔ arxiv category hand map ───────────────────────────────

DEF_TOPIC_TO_ARX = {
    # boost / interceptor / hypersonics
    "boost_phase":              ["physics_flu-dyn", "physics_class-ph",
                                   "eess_SY"],
    "space_based_interceptor":  ["astro-ph_IM", "physics_class-ph",
                                   "eess_SY"],
    "salvo missile defense":    ["math_OC", "eess_SY", "cs_RO"],
    # GNC / autonomy
    "gnc":                      ["cs_RO", "eess_SY", "math_OC"],
    "autonomy":                 ["cs_RO", "math_OC"],
    "robotics":                 ["cs_RO"],
    # game theory / OR
    "game_theory_defense":      ["math_OC", "cs_DS"],
    "optimization":             ["math_OC", "math_NA", "cs_DS"],
    # materials / propulsion
    "materials":                ["cond-mat_mtrl-sci", "physics_class-ph"],
    "propulsion":               ["physics_flu-dyn", "physics_class-ph"],
    # software / systems
    "software":                 ["cs_PL", "cs_OS"],
    "control":                  ["eess_SY", "math_OC"],
}


def _arxiv_for_topic(topic: str) -> list[str]:
    """Map a defense topic string to arxiv category list. Substring match."""
    t = (topic or "").lower()
    for k, v in DEF_TOPIC_TO_ARX.items():
        if k in t or t.startswith(k.split("_")[0]):
            return v
    return []


# ── Main builder ──────────────────────────────────────────────────────────

def build_mixed_graph(vault_path: str | None = None,
                      max_def: int = 1500,
                      max_arx_papers_per_cat: int = 20) -> "networkx.Graph":
    """Compose wiki + defense + arxiv into one graph.

    Node attrs:
      kind:           "wiki" | "def" | "arx"
      label:          human-readable
      cluster_id:     louvain cluster (wiki only) or -1
      cluster_name:   string
      degree:         filled in by the consumer; not set here
      meta:           kind-specific dict (paper_id, topic, n_papers, …)
    """
    import networkx as nx

    G = nx.Graph()

    # 1. Wiki graph (re-uses the obsidian loader for fuzzy wikilinks)
    try:
        from graph.obsidian_loader import load_vault, find_default_vault
        v = vault_path or find_default_vault()
        Wiki = load_vault(v) if v else None
    except Exception:
        Wiki = None

    if Wiki is not None:
        for n in Wiki.nodes():
            G.add_node(f"wiki:{n}", kind="wiki", label=n.replace("_", " "),
                       raw=n, source="vault")
        for u, v_, d in Wiki.edges(data=True):
            G.add_edge(f"wiki:{u}", f"wiki:{v_}",
                       weight=d.get("weight", 1.0),
                       kinds=["wiki↔wiki"])

    # 2. Defense corpus (paper-level)
    def_papers = _load_defense()[:max_def]
    by_topic: dict[str, list[dict]] = defaultdict(list)
    for p in def_papers:
        topic = (p.get("topic") or "uncategorized").strip()
        node_id = f"def:{p.get('id') or p.get('title','')[:30]}"
        title = p.get("title", "")[:80] or "(untitled)"
        G.add_node(node_id, kind="def",
                   label=title,
                   raw=p.get("id", ""),
                   source=p.get("source", "defense"),
                   topic=topic,
                   url=p.get("url", ""))
        by_topic[topic].append({
            "node_id": node_id,
            "title": title,
            "tokens": _tokens(title) | _tokens(p.get("abstract", "")[:600]),
            "topic": topic,
        })

    # 2a. def↔def: same topic
    for topic, papers in by_topic.items():
        if len(papers) > 60:   # too dense → only star around first paper
            anchor = papers[0]["node_id"]
            for p in papers[1:]:
                G.add_edge(anchor, p["node_id"],
                           weight=0.6, kinds=["def↔def(same-topic)"])
            continue
        for i in range(len(papers)):
            for j in range(i + 1, len(papers)):
                G.add_edge(papers[i]["node_id"], papers[j]["node_id"],
                           weight=0.6, kinds=["def↔def(same-topic)"])

    # 3. ArXiv categories (aggregate to one super-node each)
    arx = _load_arxiv_categories(max_per_cat=max_arx_papers_per_cat)
    for cat, info in arx.items():
        node_id = f"arx:{cat}"
        G.add_node(node_id, kind="arx",
                   label=cat, raw=cat,
                   source="arxiv",
                   n_papers=info["n_papers"],
                   sample_titles=info["sample_titles"])

    # 4. Cross-edges
    # wiki ↔ def: title token overlap (≥2 shared tokens, len(name) ≥ 6)
    wiki_token_index: dict[str, set[str]] = {}
    if Wiki is not None:
        for n in Wiki.nodes():
            human = n.replace("_", " ")
            wiki_token_index[n] = _tokens(human)

    for topic, papers in by_topic.items():
        for p in papers:
            for wiki_stem, wtoks in wiki_token_index.items():
                if len(wtoks) < 2:
                    continue
                shared = wtoks & p["tokens"]
                if len(shared) >= 2:
                    G.add_edge(f"wiki:{wiki_stem}", p["node_id"],
                               weight=0.5 * len(shared),
                               kinds=["wiki↔def"])

    # def ↔ arx via topic→category map
    for topic, papers in by_topic.items():
        cats = _arxiv_for_topic(topic)
        for cat in cats:
            anode = f"arx:{cat}"
            if not G.has_node(anode):
                continue
            # Edge from each paper in topic to the arxiv aggregate
            for p in papers[:8]:    # cap to keep degree manageable
                G.add_edge(p["node_id"], anode,
                           weight=0.4, kinds=["def↔arx"])

    # wiki ↔ arx: wiki page name appears in any sampled arxiv title
    for cat, info in arx.items():
        cat_blob_tokens = info.get("tokens", set())
        if not cat_blob_tokens:
            continue
        anode = f"arx:{cat}"
        for wiki_stem, wtoks in wiki_token_index.items():
            if len(wtoks) < 2:
                continue
            shared = wtoks & cat_blob_tokens
            if len(shared) >= 2:
                G.add_edge(f"wiki:{wiki_stem}", anode,
                           weight=0.3 * len(shared),
                           kinds=["wiki↔arx"])

    return G


def graph_summary(G) -> dict:
    """Quick stats for UI metric strip."""
    by_kind: dict[str, int] = defaultdict(int)
    for _, attrs in G.nodes(data=True):
        by_kind[attrs.get("kind", "?")] += 1
    edge_kinds: dict[str, int] = defaultdict(int)
    for _, _, d in G.edges(data=True):
        for k in d.get("kinds", []):
            edge_kinds[k] += 1
    return {
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "by_kind": dict(by_kind),
        "edge_kinds": dict(edge_kinds),
    }
