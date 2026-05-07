"""
Retrieval Inspector — debug what each retriever actually surfaces for a query.

Three columns side-by-side:
  ① BM25 (aero/mech/cs/defense)     specialist indices + defense_corpus manifest
  ② Wiki concept pages              simple keyword/title scorer
  ③ Graphiti                        search_facts + search_nodes

Plus a "Merged top-K" panel showing what the specialist would actually see
when its context is stuffed.

Run:
    python -m streamlit run ui/retrieval_inspector.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


st.set_page_config(
    page_title="Retrieval Inspector",
    page_icon="🔍",
    layout="wide",
)


PROJECT_ROOT = Path(__file__).parent.parent
WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"
DEFENSE_MANIFEST = PROJECT_ROOT / "data" / "defense_corpus" / "MANIFEST.jsonl"
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")


def _tokens(s: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(s) if len(t) > 2]


# ── Defense corpus BM25 (built once, cached) ───────────────────────────────

@st.cache_resource(show_spinner="Building defense-corpus BM25 (one-time)…")
def _defense_index():
    """Build BM25 over data/defense_corpus/MANIFEST.jsonl on first use."""
    if not DEFENSE_MANIFEST.exists():
        return {"bm25": None, "chunks": [], "error": f"{DEFENSE_MANIFEST} not found"}
    chunks = []
    for line in DEFENSE_MANIFEST.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        title = obj.get("title", "") or ""
        abstract = obj.get("abstract", "") or ""
        if not (title or abstract):
            continue
        chunks.append({
            "id": obj.get("id", ""),
            "source": obj.get("source", ""),
            "topic": obj.get("topic", ""),
            "title": title,
            "abstract": abstract,
            "url": obj.get("url", ""),
            "date": obj.get("date", ""),
            # combined searchable text
            "text": f"{title}\n\n{abstract}",
        })
    if not chunks:
        return {"bm25": None, "chunks": [], "error": "manifest empty"}
    try:
        from rank_bm25 import BM25Okapi
    except ImportError as e:
        return {"bm25": None, "chunks": chunks, "error": f"rank_bm25 not installed: {e}"}
    tokenized = [_tokens(c["text"]) for c in chunks]
    return {"bm25": BM25Okapi(tokenized), "chunks": chunks}


# ── Sidebar controls ───────────────────────────────────────────────────────

with st.sidebar:
    st.title("🔍 Retrieval Inspector")
    st.caption(
        "What does each retriever actually surface for a given query? "
        "Use this to sanity-check what the specialist context window will hold."
    )

    st.divider()
    st.subheader("Domains (BM25)")
    domains = st.multiselect(
        "Domains to query",
        options=["aero", "mech", "cs", "defense"],
        default=["aero", "mech", "cs", "defense"],
        help="`defense` covers data/defense_corpus/MANIFEST.jsonl "
             "(DTIC + NTRS + OpenAlex + arXiv-defense, ~2k docs). "
             "The other three are the per-domain arXiv slices.",
    )

    st.divider()
    st.subheader("Settings")
    top_k = st.slider("Top K", 5, 50, 10)
    show_full = st.checkbox("Show full chunk text", value=False,
                            help="Off by default — chunks are noisy.")

    st.divider()
    st.subheader("🔌 Connections")
    if os.environ.get("ANTHROPIC_API_KEY"):
        st.caption("✓ ANTHROPIC_API_KEY set")
    else:
        st.caption("⚠ ANTHROPIC_API_KEY not set (Graphiti ingestion needs it)")
    try:
        import socket
        s = socket.create_connection(("localhost", 6379), timeout=1)
        s.close()
        st.success("FalkorDB reachable")
    except Exception:
        st.warning("FalkorDB unreachable — Graphiti column will show setup hint")


# ── Header / query bar ────────────────────────────────────────────────────

st.title("🔍 Retrieval Inspector")
st.caption(
    "Run any query through all three retrievers in parallel. "
    "Compare what each returns — and what the merged top-K context looks like."
)

col_q, col_btn = st.columns([6, 1])
with col_q:
    query = st.text_input("Query", value="", placeholder="e.g. boost phase intercept")
with col_btn:
    st.write("")
    st.write("")
    run = st.button("Run", type="primary", use_container_width=True)

if not query.strip():
    st.info("Enter a query above to inspect retrieval.")
    st.stop()


# ── Retriever wrappers (cached) ────────────────────────────────────────────

@st.cache_data(ttl=60, show_spinner=False)
def bm25_retrieve(query: str, top_k: int, domain: str) -> dict:
    """Run BM25 for a single domain. Returns {results|error}."""
    try:
        if domain == "defense":
            return _defense_retrieve(query, top_k)

        from agents.specialists import SPECIALISTS
        spec = SPECIALISTS.get(domain)
        if spec is None:
            return {"error": f"unknown domain {domain!r}", "results": []}
        results = spec.retrieve(query, top_k=top_k)
        # Hint if index missing
        if not results and not spec.rag_index_path.exists():
            return {
                "results": [],
                "error": f"index not built: {spec.rag_index_path.name} "
                         f"(run `python rag/build_split_indices.py`)",
            }
        return {"results": results}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "results": [],
                "trace": traceback.format_exc()}


def _defense_retrieve(query: str, top_k: int) -> dict:
    """BM25 over data/defense_corpus/MANIFEST.jsonl (built lazily, cached)."""
    idx = _defense_index()
    if idx.get("error") and idx.get("bm25") is None:
        return {"results": [], "error": idx["error"]}
    bm25, chunks = idx["bm25"], idx["chunks"]
    if bm25 is None or not chunks:
        return {"results": []}
    toks = _tokens(query)
    if not toks:
        return {"results": []}
    scores = bm25.get_scores(toks)
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
    out = []
    for score, ch in ranked[:top_k]:
        if score <= 0:
            continue
        out.append({
            **ch,
            "_score": float(score),
            # render keys to align w/ specialist chunk schema
            "source": f"{ch['source']}/{ch['id']}",
        })
    return {"results": out}


@st.cache_data(ttl=60, show_spinner=False)
def wiki_retrieve(query: str, top_k: int) -> dict:
    """Keyword/title-match retriever over wiki/concepts/*.md.

    Score = sum over query tokens of:
      filename hit count * 5  +  body (first 500 chars) hit count
    """
    try:
        if not WIKI_CONCEPTS.exists():
            return {"error": f"{WIKI_CONCEPTS} not found", "results": []}
        toks = _tokens(query)
        if not toks:
            return {"results": []}
        scored = []
        for p in WIKI_CONCEPTS.glob("*.md"):
            try:
                head = p.read_text(errors="ignore")[:2000]
            except Exception:
                continue
            name_lc = p.stem.lower().replace("_", " ")
            head_lc = head[:500].lower()
            score = 0
            for t in toks:
                score += name_lc.count(t) * 5
                score += head_lc.count(t)
            if score > 0:
                scored.append((score, p, head))
        scored.sort(key=lambda x: x[0], reverse=True)
        out = []
        for score, path, head in scored[:top_k]:
            # body preview = strip first heading line if present
            body = head
            lines = head.splitlines()
            if lines and lines[0].startswith("#"):
                body = "\n".join(lines[1:]).strip()
            out.append({
                "title": path.stem.replace("_", " "),
                "path": str(path.relative_to(PROJECT_ROOT)),
                "abs_path": str(path),
                "score": score,
                "preview": body[:300],
            })
        return {"results": out}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "results": [],
                "trace": traceback.format_exc()}


@st.cache_data(ttl=60, show_spinner=False)
def graph_retrieve(query: str, top_k: int) -> dict:
    """Hit Graphiti for facts + entities. Returns {facts, nodes, error?}.

    Runs in a dedicated thread with its own event loop to avoid
    `RuntimeError: This event loop is already running` when streamlit's
    tornado loop is active.
    """
    import threading
    result: dict = {}

    def worker():
        import asyncio
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                from graph.temporal_graph import search_facts, search_nodes
                facts = search_facts(query, limit=top_k)
                nodes = search_nodes(query, limit=top_k)
                result.update({"facts": facts, "nodes": nodes})
            finally:
                try:
                    loop.close()
                except Exception:
                    pass
        except ImportError as e:
            result.update({"error": f"graphiti not installed: {e}",
                           "facts": [], "nodes": []})
        except Exception as e:
            result.update({"error": f"{type(e).__name__}: {e}",
                           "facts": [], "nodes": []})

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(timeout=30)
    if t.is_alive():
        return {"error": "graphiti query timed out (30s)",
                "facts": [], "nodes": []}
    return result or {"facts": [], "nodes": []}


# ── Run all three retrievers (independently — failure isolated) ───────────

if run or query:  # auto-run on text submit
    bm25_per_domain = {d: bm25_retrieve(query, top_k, d) for d in domains}
    wiki_out = wiki_retrieve(query, top_k)
    graph_out = graph_retrieve(query, top_k)
else:
    bm25_per_domain, wiki_out, graph_out = {}, {"results": []}, {"facts": [], "nodes": []}


# ── Three-column layout ────────────────────────────────────────────────────

col1, col2, col3 = st.columns(3)


# ── ① BM25 column ─────────────────────────────────────────────────────────

with col1:
    st.subheader("① BM25 per-domain")
    st.caption("`agents.specialists.Specialist.retrieve()` over each domain's arXiv slice")

    if not domains:
        st.info("Pick at least one domain in the sidebar.")
    for d in domains:
        out = bm25_per_domain.get(d, {})
        results = out.get("results", [])
        err = out.get("error")
        with st.expander(f"**{d}** — {len(results)} hits" + (f" · ⚠ {err}" if err and not results else ""),
                         expanded=True):
            if err and not results:
                st.warning(err)
            if not results:
                st.caption("_no results_")
                continue
            for i, r in enumerate(results, 1):
                score = r.get("_score", 0)
                src = r.get("source", "")
                src_short = Path(src).name if src else ""

                if d == "defense":
                    # richer rendering for defense corpus: title · topic · url
                    title = r.get("title", "") or "(untitled)"
                    topic = r.get("topic", "") or ""
                    url = r.get("url", "")
                    src_kind = r.get("source", "").split("/", 1)[0] if "/" in r.get("source", "") else ""
                    abstract = r.get("abstract", "") or ""
                    preview = abstract if show_full else (abstract[:240] + ("…" if len(abstract) > 240 else ""))
                    head = f"**{i}. {title[:90]}** · score {score:.2f}"
                    if src_kind:
                        head += f" · `{src_kind}`"
                    if topic:
                        head += f" · _{topic}_"
                    st.markdown(head)
                    if preview:
                        st.caption(preview)
                    if url:
                        st.markdown(f"[{url}]({url})")
                else:
                    text = r.get("text", "") or ""
                    preview = text if show_full else (text[:240] + ("…" if len(text) > 240 else ""))
                    st.markdown(f"**{i}. score {score:.2f}** · `{src_short}`")
                    if preview:
                        st.caption(preview)


# ── ② Wiki column ─────────────────────────────────────────────────────────

with col2:
    st.subheader("② Wiki concepts")
    st.caption(f"keyword/title match over `wiki/concepts/*.md` ({len(list(WIKI_CONCEPTS.glob('*.md')))} pages)")

    if wiki_out.get("error"):
        st.warning(wiki_out["error"])
    results = wiki_out.get("results", [])
    if not results:
        st.caption("_no results_")
    else:
        for i, r in enumerate(results, 1):
            with st.container(border=True):
                st.markdown(f"**{i}. {r['title']}** · score {r['score']}")
                preview = r["preview"]
                if not show_full:
                    preview = preview[:300] + ("…" if len(r["preview"]) >= 300 else "")
                st.caption(preview)
                st.markdown(f"`{r['path']}`")


# ── ③ Graphiti column ─────────────────────────────────────────────────────

with col3:
    st.subheader("③ Graphiti")
    st.caption("`search_facts` + `search_nodes` against FalkorDB")

    if graph_out.get("error"):
        st.warning(graph_out["error"])
        st.info("Setup steps:\n"
                "1. `cd docker && docker compose up -d`\n"
                "2. `pip install graphiti-core falkordb pyvis nest_asyncio pymupdf`\n"
                "3. `python3 scripts/wiki_to_graphiti.py` (one-time seed)")
    else:
        facts = graph_out.get("facts", [])
        nodes = graph_out.get("nodes", [])

        st.markdown(f"**Facts** ({len(facts)})")
        if facts:
            import pandas as pd
            df = pd.DataFrame([
                {
                    "source": (f.get("source") or "")[:30],
                    "fact": (f.get("fact") or "")[:80],
                    "target": (f.get("target") or "")[:30],
                    "valid": (f.get("valid_at") or "")[:10],
                    "invalid": (f.get("invalid_at") or "—")[:10] if f.get("invalid_at") else "—",
                }
                for f in facts
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.caption("_no facts_")

        st.markdown(f"**Entities** ({len(nodes)})")
        if nodes:
            for n in nodes:
                name = n.get("name", "")
                labels = ", ".join(n.get("labels", []) or []) or "—"
                summary = (n.get("summary") or "")[:140]
                st.markdown(f"• **{name}** · _{labels}_")
                if summary:
                    st.caption(summary)
        else:
            st.caption("_no entities_")


# ── Merged top-K panel ────────────────────────────────────────────────────

st.divider()
st.subheader("🧠 Merged top-K — what the specialist would actually see")
st.caption(
    "Top 5 from each retriever, tagged with source. This is the rough shape "
    "of the context that gets stuffed into the LLM for this query."
)

merged: list[dict] = []

for d in domains:
    for r in bm25_per_domain.get(d, {}).get("results", [])[:5]:
        if d == "defense":
            title = (r.get("title") or "(untitled)")[:90]
            preview = (r.get("abstract") or "")[:240]
        else:
            title = Path(r.get("source", "")).name or f"({d}) chunk"
            text = r.get("text", "") or ""
            preview = text[:240] + ("…" if len(text) > 240 else "")
        merged.append({
            "tag": f"BM25:{d}",
            "score": float(r.get("_score", 0)),
            "title": title,
            "preview": preview,
        })

for r in wiki_out.get("results", [])[:5]:
    merged.append({
        "tag": "Wiki",
        "score": float(r.get("score", 0)),
        "title": r.get("title", ""),
        "preview": r.get("preview", "")[:240],
    })

for f in graph_out.get("facts", [])[:5]:
    merged.append({
        "tag": "Graph:fact",
        "score": 0.0,
        "title": f"{(f.get('source') or '')[:24]} → {(f.get('target') or '')[:24]}",
        "preview": (f.get("fact") or "")[:240],
    })

if not merged:
    st.caption("_no merged results — every retriever returned empty_")
else:
    # sort by tag group then score desc within each
    tag_order = {"BM25:aero": 0, "BM25:mech": 1, "BM25:cs": 2, "BM25:defense": 3,
                 "Wiki": 4, "Graph:fact": 5}
    merged.sort(key=lambda x: (tag_order.get(x["tag"], 99), -x["score"]))
    for m in merged:
        with st.container(border=True):
            cols = st.columns([1, 4])
            with cols[0]:
                st.markdown(f"`[{m['tag']}]`")
                if m["score"]:
                    st.caption(f"score {m['score']:.2f}")
            with cols[1]:
                st.markdown(f"**{m['title']}**")
                if m["preview"]:
                    st.caption(m["preview"])
