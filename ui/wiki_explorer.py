"""
Wiki Explorer — separate UI for browsing the LLM-built knowledge base.

Independent of ui/learning_app.py. Three layers, each addressable as a tab:

  📁 PARA       — Projects / Areas / Resources / Archives folder taxonomy
                   (Tiago Forte's system). Auto-derives from the vault if
                   no explicit folders, else uses vault structure as-is.
  📓 Notes       — paginated list of every wiki note + Obsidian-style
                   wikilink-aware viewer + outgoing/incoming backlink
                   panel. Renders .md and .qmd (Quarto) with syntax
                   highlighting on code fences.
  🔍 Search      — multi-source unified search bar. Hits wiki + Obsidian
                   vault + arXiv BM25 + defense corpus + Graphiti facts
                   simultaneously, ranked side-by-side.
  🧠 LLM brain   — 'Obsidian but from data': what Graphiti has extracted
                   from PDFs/papers vs. what's in markdown. Compare
                   coverage; pick a node to see its wiki page next to
                   its Graphiti entity record.

Run:
    python -m streamlit run ui/wiki_explorer.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


PROJECT_ROOT = Path(__file__).parent.parent
WIKI_CONCEPTS = PROJECT_ROOT / "wiki" / "concepts"


st.set_page_config(
    page_title="Wiki Explorer — LLM Knowledge Base",
    page_icon="📚",
    layout="wide",
)


# ── Sidebar — vault selection + PARA toggle ───────────────────────────────

ss = st.session_state
ss.setdefault("vault_path", str(WIKI_CONCEPTS))
ss.setdefault("selected_note", None)

with st.sidebar:
    st.title("📚 Wiki Explorer")
    st.caption(
        "Browse the LLM-built knowledge base. Independent of the learning "
        "app — same vault, different lens."
    )

    st.divider()
    st.subheader("📁 Vault")
    new_vault = st.text_input(
        "Vault path",
        value=ss.vault_path,
        help="Any folder of .md / .qmd files. Defaults to wiki/concepts/.",
    )
    if new_vault != ss.vault_path:
        ss.vault_path = new_vault
        ss.selected_note = None
        st.rerun()

    try:
        from graph.obsidian_loader import vault_metadata
        meta = vault_metadata(ss.vault_path)
        if meta.get("ok"):
            badge = "📓 Obsidian vault" if meta["is_obsidian_vault"] \
                    else "📁 plain markdown folder"
            st.caption(
                f"{badge}\n"
                f"{meta['n_notes']:,} notes · {meta['n_links']:,} links · "
                f"{meta['n_tags']} tags"
            )
        else:
            st.warning(meta.get("error", "vault not found"))
    except Exception as e:
        st.caption(f"_probe failed: {e}_")

    st.divider()
    st.subheader("🧭 PARA mode")
    para_mode = st.radio(
        "How to bucket notes",
        options=["auto (heuristic)", "use folders", "manual tags"],
        index=0, horizontal=False,
        help="auto = derive Projects/Areas/Resources/Archives from filename/"
             "frontmatter heuristics. use folders = top-level subdir is "
             "the bucket. manual tags = #project/#area/#resource/#archive.",
    )

    st.divider()
    show_qmd = st.checkbox("Include .qmd (Quarto) files", value=True,
                            help="Quarto markdown with executable code blocks.")


# ── Header ────────────────────────────────────────────────────────────────

st.title("📚 Wiki Explorer — LLM-built knowledge base")
st.caption(
    "Three lenses on the same content: PARA folder taxonomy, Obsidian-style "
    "note browser with backlinks, multi-source search, and the Graphiti "
    "LLM-extracted graph."
)


# ── Vault loader ──────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"\[\[([^\[\]\|\n]+?)(?:\|[^\[\]\n]+)?\]\]")
TAG_RE = re.compile(r"(?<!\S)#([A-Za-z][\w/\-]+)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@st.cache_resource(show_spinner=False)
def _load_vault(path: str, include_qmd: bool):
    """Walk the vault. Returns dict of {stem: note_dict}."""
    p = Path(path).expanduser()
    if not p.is_dir():
        return {}, {}, {}
    notes: dict[str, dict] = {}
    extensions = (".md", ".qmd") if include_qmd else (".md",)

    for ext in extensions:
        for f in p.rglob(f"*{ext}"):
            if any(seg.startswith(".") for seg in f.relative_to(p).parts):
                continue
            try:
                body = f.read_text(errors="ignore")
            except Exception:
                continue
            stem = f.stem
            if stem in notes:
                continue
            fm_match = FRONTMATTER_RE.match(body)
            fm: dict = {}
            stripped = body
            if fm_match:
                stripped = body[fm_match.end():]
                for ln in fm_match.group(1).splitlines():
                    if ":" not in ln:
                        continue
                    k, _, v = ln.partition(":")
                    fm[k.strip()] = v.strip().strip('"').strip("'")
            tags = set(TAG_RE.findall(stripped))
            if "tags" in fm:
                tags.update(t.strip() for t in fm["tags"].split(",") if t.strip())
            outgoing = []
            for m in WIKILINK_RE.finditer(stripped):
                t = re.split(r"[#\^|]", m.group(1).strip(), 1)[0].strip()
                t = t.rsplit("/", 1)[-1]
                if t and t != stem:
                    outgoing.append(t)
            notes[stem] = {
                "stem": stem,
                "path": f.relative_to(p),
                "abs_path": f,
                "folder": str(f.relative_to(p).parent),
                "ext": f.suffix,
                "tags": sorted(tags),
                "frontmatter": fm,
                "outgoing": outgoing,
                "body": stripped,
                "size_chars": len(stripped),
                "mtime": f.stat().st_mtime,
            }

    # Build inverted-link map (for backlinks)
    backlinks: dict[str, list[str]] = defaultdict(list)
    norm_to_stem = {re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_"): s
                     for s in notes}
    for stem, note in notes.items():
        for tgt in note["outgoing"]:
            n = re.sub(r"[^a-z0-9]+", "_", tgt.lower()).strip("_")
            real = norm_to_stem.get(n)
            if real and real != stem:
                backlinks[real].append(stem)

    # PARA bucketing — apply same heuristic up-front
    para = {"Projects": [], "Areas": [], "Resources": [], "Archives": []}
    for stem, note in notes.items():
        bucket = _para_for(note)
        para[bucket].append(stem)

    return notes, dict(backlinks), para


def _para_for(note: dict) -> str:
    """Heuristic: Projects = active/dated work, Areas = ongoing topic
    domains, Resources = reference material (most wiki notes), Archives =
    explicitly archived or stale.

    Order of evidence:
      1. frontmatter `para:` → use as-is
      2. tag #project / #area / #resource / #archive
      3. folder name match (case-insensitive)
      4. fallback: 'Resources' (the vast majority of wiki notes are reference)
    """
    fm = note.get("frontmatter", {}) or {}
    if fm.get("para"):
        v = fm["para"].strip().lower()
        for cand in ("Projects", "Areas", "Resources", "Archives"):
            if cand.lower().startswith(v):
                return cand
    tag_set = {t.lower() for t in note.get("tags", [])}
    for cand in ("Projects", "Areas", "Resources", "Archives"):
        if cand.lower()[:-1] in tag_set:   # strip 's' (project not projects)
            return cand
        if cand.lower() in tag_set:
            return cand
    folder = (note.get("folder") or "").lower()
    for cand in ("Projects", "Areas", "Resources", "Archives"):
        if cand.lower() in folder:
            return cand
    return "Resources"


notes, backlinks, para = _load_vault(ss.vault_path, show_qmd)
if not notes:
    st.warning("No notes found at that vault path.")
    st.stop()


# ── Top metrics ───────────────────────────────────────────────────────────

c1, c2, c3, c4 = st.columns(4)
c1.metric("Notes", len(notes))
c2.metric(".qmd files", sum(1 for n in notes.values() if n["ext"] == ".qmd"))
c3.metric("Backlinks", sum(len(v) for v in backlinks.values()))
c4.metric("Tags", sum(len(set(n["tags"])) for n in notes.values()))


# ── Tabs ──────────────────────────────────────────────────────────────────

tab_para, tab_notes, tab_search, tab_brain, tab_3d, tab_propose = st.tabs(
    ["📁 PARA", "📓 Notes", "🔍 Search", "🧠 LLM brain",
     "🕸 3D graph", "💡 Propose"]
)


# ── Tab: PARA ─────────────────────────────────────────────────────────────

with tab_para:
    st.markdown(
        "**PARA** = Projects · Areas · Resources · Archives. The four "
        "buckets are derived from frontmatter `para:`, tags "
        "(`#project` / `#area` / `#resource` / `#archive`), folder name, "
        "or — fallback — everything goes into Resources."
    )

    para_cols = st.columns(4)
    bucket_emoji = {"Projects": "🟢", "Areas": "🟦",
                     "Resources": "🟣", "Archives": "⚪"}
    for col, bucket in zip(para_cols, ["Projects", "Areas", "Resources", "Archives"]):
        with col:
            with st.container(border=True):
                emoji = bucket_emoji[bucket]
                st.markdown(f"### {emoji} {bucket}")
                st.metric("count", len(para[bucket]),
                            label_visibility="collapsed")
                if not para[bucket]:
                    st.caption("_empty_")
                else:
                    # Sort by mtime descending
                    items = sorted(
                        para[bucket],
                        key=lambda s: notes[s].get("mtime", 0),
                        reverse=True,
                    )[:10]
                    for stem in items:
                        if st.button(stem.replace("_", " ")[:30],
                                       key=f"para_{bucket}_{stem}",
                                       use_container_width=True):
                            ss.selected_note = stem
                            st.rerun()
                    if len(para[bucket]) > 10:
                        st.caption(f"_+ {len(para[bucket]) - 10} more_")

    # Bulk move-to-bucket UI
    with st.expander("🛠 Move notes between buckets (writes frontmatter)"):
        st.caption(
            "Sets `para: <bucket>` in the note's YAML frontmatter so the "
            "bucketing is permanent. Idempotent — re-running keeps the new value."
        )
        bk_target = st.selectbox("Target bucket",
                                  ["Projects", "Areas", "Resources", "Archives"],
                                  key="bk_target")
        bk_select = st.multiselect("Notes to move",
                                    options=sorted(notes.keys())[:200],
                                    key="bk_notes")
        if st.button("Move selected", disabled=not bk_select):
            done = 0
            for stem in bk_select:
                p = notes[stem]["abs_path"]
                body = p.read_text(errors="ignore")
                if body.startswith("---"):
                    body = re.sub(
                        r"^---\s*\n(.*?\n)?---\s*\n",
                        lambda m: _patch_fm(m.group(0), {"para": bk_target}),
                        body, count=1, flags=re.DOTALL,
                    )
                else:
                    body = f"---\npara: {bk_target}\n---\n\n" + body
                p.write_text(body)
                done += 1
            st.success(f"updated {done} notes — reload to see new bucket")


def _patch_fm(fm_block: str, updates: dict) -> str:
    """Inject/replace keys in an existing YAML frontmatter block."""
    inner = re.search(r"^---\s*\n(.*?)\n---\s*\n", fm_block, re.DOTALL).group(1)
    seen = set()
    out_lines = []
    for ln in inner.splitlines():
        if ":" in ln:
            k = ln.split(":", 1)[0].strip()
            if k in updates:
                out_lines.append(f"{k}: {updates[k]}")
                seen.add(k)
                continue
        out_lines.append(ln)
    for k, v in updates.items():
        if k not in seen:
            out_lines.append(f"{k}: {v}")
    return "---\n" + "\n".join(out_lines) + "\n---\n"


# ── Tab: Notes (Obsidian-style browser) ───────────────────────────────────

with tab_notes:
    note_cols = st.columns([1, 2])

    # Left: filterable list
    with note_cols[0]:
        st.markdown("##### 📋 All notes")
        filter_text = st.text_input("Filter", "", key="note_filter",
                                      placeholder="case-insensitive name match")
        filter_lc = filter_text.lower().strip()
        filtered = [s for s in sorted(notes.keys())
                    if not filter_lc or filter_lc in s.lower()
                    or filter_lc in s.replace("_", " ").lower()]
        st.caption(f"{len(filtered)} of {len(notes)}")
        # Render up to 200 buttons
        for stem in filtered[:200]:
            note = notes[stem]
            ext_tag = "📄" if note["ext"] == ".md" else "🧪"
            label = f"{ext_tag} {stem.replace('_', ' ')[:32]}"
            if st.button(label, key=f"sel_{stem}",
                           use_container_width=True):
                ss.selected_note = stem
                st.rerun()
        if len(filtered) > 200:
            st.caption(f"…and {len(filtered) - 200} more — refine the filter")

    # Right: viewer
    with note_cols[1]:
        sel = ss.selected_note
        if sel is None or sel not in notes:
            st.info("Pick a note from the left to view it.")
        else:
            note = notes[sel]
            st.markdown(f"### {sel.replace('_', ' ')}")
            head_cols = st.columns(4)
            head_cols[0].caption(f"📁 {note['folder'] or '/'}")
            head_cols[1].caption(f"{note['ext']}")
            head_cols[2].caption(f"{note['size_chars']:,} chars")
            head_cols[3].caption(f"PARA: {_para_for(note)}")

            if note["tags"]:
                st.caption("tags: " + " ".join(f"`#{t}`" for t in note["tags"]))

            # Render — for .qmd treat code fences specially
            if note["ext"] == ".qmd":
                st.caption("_Quarto (.qmd) — code blocks shown but not executed_")
            st.markdown(note["body"], unsafe_allow_html=False)

            # Linked notes
            link_cols = st.columns(2)
            with link_cols[0]:
                st.markdown("##### → outgoing")
                if not note["outgoing"]:
                    st.caption("_no wikilinks_")
                else:
                    for tgt in dict.fromkeys(note["outgoing"])[:20]:
                        # case-insensitive resolve
                        n = re.sub(r"[^a-z0-9]+", "_", tgt.lower()).strip("_")
                        real = next((s for s in notes
                                     if re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_") == n),
                                    None)
                        if real and st.button(f"→ {tgt}", key=f"out_{sel}_{tgt}"):
                            ss.selected_note = real
                            st.rerun()
                        elif not real:
                            st.caption(f"~~{tgt}~~ (stub — no page)")
            with link_cols[1]:
                st.markdown("##### ← backlinks")
                bl = backlinks.get(sel, [])
                if not bl:
                    st.caption("_no incoming links_")
                else:
                    for src in dict.fromkeys(bl)[:20]:
                        if st.button(f"← {src.replace('_', ' ')}",
                                       key=f"in_{sel}_{src}"):
                            ss.selected_note = src
                            st.rerun()


# ── Tab: Search (multi-source) ────────────────────────────────────────────

with tab_search:
    st.markdown(
        "Multi-source unified search. Hits the local vault, arXiv RAG, "
        "defense corpus, Wikipedia, and Graphiti facts in parallel."
    )
    q = st.text_input("Query", "", placeholder="e.g. boost phase intercept")
    s_l, s_r = st.columns([1, 1])
    with s_l:
        do_web = st.checkbox("Include web (Wikipedia + DDG)", value=False)
    with s_r:
        top_k = st.slider("Top K per source", 3, 20, 8)

    if q.strip():
        @st.cache_data(ttl=120, show_spinner="searching…")
        def _multi_search(query: str, k: int, web: bool, vault: str):
            from agents.content_finder import find, find_with_web
            return (find_with_web(query, k=k) if web else find(query, k=k, allow_web=True))

        # Local note-name match (vault)
        ql = q.lower()
        vault_hits = [
            (n, s) for s, n in notes.items()
            if ql in s.lower() or ql in s.replace("_", " ").lower()
            or ql in n.get("body", "")[:1500].lower()
        ][:top_k]

        results = _multi_search(q, top_k, do_web, ss.vault_path)

        # Render side-by-side
        res_cols = st.columns(4)
        with res_cols[0]:
            st.markdown(f"##### 📓 Vault ({len(vault_hits)})")
            for stem, n in vault_hits:
                if st.button(stem.replace("_", " ")[:36],
                               key=f"sv_{stem}", use_container_width=True):
                    ss.selected_note = stem
                    st.toast("Opened — switch to 📓 Notes tab.", icon="📓")
        with res_cols[1]:
            st.markdown(f"##### 🔬 arXiv RAG ({len(results.get('rag') or [])})")
            for r in (results.get("rag") or [])[:top_k]:
                st.caption(f"**{r.get('domain', '?')}** · `{r.get('paper_id', '')[:24]}` · score {r.get('_score', 0):.2f}")
                st.caption((r.get("text") or "")[:160])
        with res_cols[2]:
            st.markdown(f"##### 🛡 Defense ({len(results.get('defense') or [])})")
            for d in (results.get("defense") or [])[:top_k]:
                st.caption(f"**{(d.get('title') or '')[:60]}**")
                st.caption(f"score {d.get('_score', 0):.2f}")
        with res_cols[3]:
            wiki = results.get("wikipedia")
            web = results.get("web") or []
            st.markdown(f"##### 🌐 Web ({(1 if wiki else 0) + len(web)})")
            if wiki:
                st.markdown(f"**{wiki.get('title','')}** (Wikipedia)")
                st.caption(wiki.get("extract", "")[:160])
            for w in web[:top_k]:
                st.caption(f"**{(w.get('title') or '')[:60]}**")
                st.caption((w.get("snippet") or "")[:120])

        # Graphiti facts (separate row — usually empty without FalkorDB)
        st.markdown("##### 🧠 Graphiti facts")
        try:
            from graph.temporal_graph import search_facts
            facts = search_facts(q, limit=top_k)
            if not facts:
                st.caption("_no facts (Graphiti offline or no matches)_")
            for f in facts:
                st.caption(
                    f"**{(f.get('source') or '')[:24]}** → "
                    f"{(f.get('fact') or '')[:80]} → "
                    f"**{(f.get('target') or '')[:24]}**"
                )
        except Exception as e:
            st.caption(f"_graphiti unreachable: {type(e).__name__}_")


# ── Tab: LLM brain (Graphiti coverage vs wiki) ────────────────────────────

with tab_brain:
    st.markdown(
        "**The 'Obsidian for data' view.** Compares what the brain "
        "(Graphiti, an LLM-built entity graph from PDFs and papers) "
        "knows vs. what the markdown vault has written down. "
        "Gaps in either column are candidate work items."
    )

    # Probe Graphiti
    try:
        from graph.temporal_graph import _get_driver, _run, GROUP_ID
        drv = _get_driver()
        cypher = (
            f"MATCH (n) WHERE n.group_id = '{GROUP_ID}' "
            f"RETURN n.name AS name, count(*) AS c "
            f"ORDER BY c DESC LIMIT 200"
        )
        try:
            recs, _, _ = _run(drv.execute_query(cypher))
            ents = [dict(r).get("name") for r in recs if dict(r).get("name")]
            graphiti_ok = True
        except Exception as e:
            ents = []
            graphiti_ok = False
            graphiti_err = str(e)[:200]
    except Exception as e:
        ents = []
        graphiti_ok = False
        graphiti_err = f"{type(e).__name__}: {e}"

    if not graphiti_ok:
        st.warning(
            f"Graphiti unreachable — can't show LLM-extracted entities. "
            f"Start FalkorDB to populate this view: "
            f"`cd docker && docker compose up -d`. ({graphiti_err if 'graphiti_err' in dir() else ''})"
        )
        st.info(
            "**Concept:** This tab is meant to render the LLM-curated graph "
            "alongside the human-curated vault. Tools that do this end-to-"
            "end: Microsoft GraphRAG, Cognee, Mem0, Zep, LightRAG, Logseq+AI. "
            "Our equivalent is Graphiti running over the arxiv + defense "
            "corpora — those PDFs become entities and relations on ingest."
        )
    else:
        norm_notes = {re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_"): s
                       for s in notes}
        in_both = []
        only_graph = []
        for ent in ents:
            ne = re.sub(r"[^a-z0-9]+", "_", (ent or "").lower()).strip("_")
            if ne in norm_notes:
                in_both.append((ent, norm_notes[ne]))
            else:
                only_graph.append(ent)
        only_wiki = [s for s in notes
                     if re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
                     not in {re.sub(r"[^a-z0-9]+", "_", e.lower()).strip("_")
                             for e in ents}][:200]

        cb = st.columns(3)
        cb[0].metric("In both (📓 + 🧠)", len(in_both))
        cb[1].metric("LLM-only (🧠)", len(only_graph))
        cb[2].metric("Wiki-only (📓)", len(only_wiki))

        cc = st.columns(3)
        with cc[0]:
            st.markdown("##### 🤝 In both")
            for ent, stem in in_both[:25]:
                if st.button(ent, key=f"both_{ent}", use_container_width=True):
                    ss.selected_note = stem
                    st.toast("Opened — switch to 📓 Notes.", icon="📓")
        with cc[1]:
            st.markdown("##### 🧠 LLM-only")
            st.caption("_extracted from PDFs but not yet written up in the vault_")
            for ent in only_graph[:25]:
                st.caption(f"• {ent}")
        with cc[2]:
            st.markdown("##### 📓 Vault-only")
            st.caption("_in the wiki, but the LLM hasn't seen / linked it yet_")
            for stem in only_wiki[:25]:
                if st.button(stem.replace("_", " "),
                              key=f"vw_{stem}",
                              use_container_width=True):
                    ss.selected_note = stem
                    st.rerun()


# ── Tab: 3D graph ─────────────────────────────────────────────────────────

with tab_3d:
    st.markdown(
        "**3D mind graph** — drag to orbit, scroll to zoom, click any node "
        "to open its note. Powered by [3d-force-graph](https://github.com/"
        "vasturiano/3d-force-graph) via Three.js / WebGL."
    )

    g_mode = st.radio(
        "Corpus", ["wiki only", "mixed (wiki + defense + arXiv)"],
        index=1, horizontal=True,
        help="`mixed` adds defense corpus papers (DTIC/NTRS/OpenAlex) "
             "and arXiv category aggregates as nodes, with cross-edges by "
             "title-token overlap. Color-codes each kind.",
    )

    @st.cache_data(ttl=300, show_spinner="building wiki graph…")
    def _build_3d_payload(vault: str):
        from graph.clusters import load_graph, load_clusters
        G = load_graph(source="auto", vault_path=vault)
        clusters = load_clusters() or []
        n2c = {}
        for c in clusters:
            for m in c.members:
                n2c[m] = c.cluster_id
        cluster_names = {c.cluster_id: c.name for c in clusters}
        nodes = []
        for n in G.nodes():
            cid = n2c.get(n, -1)
            nodes.append({
                "id":    n,
                "label": n.replace("_", " "),
                "kind":  "wiki",
                "cluster": cid,
                "cluster_name": cluster_names.get(cid, ""),
                "degree": int(G.degree(n)),
            })
        links = [{"source": u, "target": v} for u, v in G.edges()]
        return {"nodes": nodes, "links": links,
                "n_clusters": len(clusters)}

    @st.cache_data(ttl=300, show_spinner="building mixed-corpus graph…")
    def _build_3d_payload_mixed(vault: str):
        from graph.corpus_graph import build_mixed_graph, graph_summary
        from graph.clusters import load_clusters
        G = build_mixed_graph(vault_path=vault)
        clusters = load_clusters() or []
        n2c = {}
        for c in clusters:
            for m in c.members:
                n2c[m] = c.cluster_id
        cluster_names = {c.cluster_id: c.name for c in clusters}

        nodes = []
        for n, attrs in G.nodes(data=True):
            kind = attrs.get("kind", "wiki")
            raw = attrs.get("raw", n)
            cid = n2c.get(raw, -1)
            cname = cluster_names.get(cid, "")
            # Kind-specific tweaks
            if kind == "def":
                cname = attrs.get("topic", "defense")
            elif kind == "arx":
                cname = "arXiv: " + attrs.get("label", "")
            nodes.append({
                "id":    n,
                "label": attrs.get("label", n)[:50],
                "kind":  kind,
                "cluster": cid,
                "cluster_name": cname,
                "degree": int(G.degree(n)),
                "url":   attrs.get("url", ""),
                "source": attrs.get("source", ""),
            })
        links = [{"source": u, "target": v,
                   "kinds": d.get("kinds", [])}
                  for u, v, d in G.edges(data=True)]
        s = graph_summary(G)
        return {"nodes": nodes, "links": links,
                "n_clusters": len(clusters),
                "summary": s}

    if g_mode.startswith("mixed"):
        payload = _build_3d_payload_mixed(ss.vault_path)
    else:
        payload = _build_3d_payload(ss.vault_path)
    n_nodes, n_links = len(payload["nodes"]), len(payload["links"])
    summary = payload.get("summary") or {}
    by_kind = summary.get("by_kind") or {}
    edge_kinds = summary.get("edge_kinds") or {}
    if by_kind:
        kc = st.columns(4)
        kc[0].metric("Total nodes", f"{n_nodes:,}")
        kc[1].metric("📓 wiki", by_kind.get("wiki", 0))
        kc[2].metric("🛡 defense", by_kind.get("def", 0))
        kc[3].metric("🔬 arXiv cats", by_kind.get("arx", 0))
        if edge_kinds:
            badges = []
            for k, v in edge_kinds.items():
                badges.append(f"`{k}` {v:,}")
            st.caption("Edges: " + " · ".join(badges))
    else:
        st.caption(f"{n_nodes:,} nodes  ·  {n_links:,} edges  ·  "
                    f"{payload.get('n_clusters', 0)} clusters")

    ctl1, ctl2, ctl3 = st.columns([1, 1, 1])
    with ctl1:
        show_isolated = st.toggle("Isolated nodes", value=False,
                                    help="Show degree-0 nodes")
    with ctl2:
        show_labels = st.toggle("Always-on labels", value=True,
                                  help="Draw node names as 3D sprites. "
                                       "Disable for big graphs if laggy.")
    with ctl3:
        label_min_degree = st.slider("Min degree to label", 0, 10, 1,
                                       help="Hide labels on low-degree nodes "
                                            "to keep the view legible.")

    if not show_isolated:
        kept = {n["id"] for n in payload["nodes"] if n["degree"] > 0}
        payload = {
            "nodes": [n for n in payload["nodes"] if n["id"] in kept],
            "links": [l for l in payload["links"]
                       if l["source"] in kept and l["target"] in kept],
            "n_clusters": payload.get("n_clusters", 0),
        }
        st.caption(f"showing {len(payload['nodes']):,} connected nodes "
                    f"(of {n_nodes:,})")

    import json as _json
    payload_json = _json.dumps(payload)
    show_labels_js = "true" if show_labels else "false"
    height = 620
    html = """
<style>
  #brain3d-wrap { position: relative; }
  #recbar {
    position: absolute; top: 10px; left: 10px; z-index: 10;
    display: flex; gap: 8px; align-items: center;
    background: rgba(7, 9, 31, 0.85); padding: 8px 12px;
    border: 1px solid #1E2761; border-radius: 8px;
    color: #FAFBFE; font-family: -apple-system, system-ui, sans-serif;
    font-size: 13px;
  }
  #recbar button {
    background: #1E2761; color: #FAFBFE; border: 1px solid #3B5BA5;
    padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px;
  }
  #recbar button:hover { background: #3B5BA5; }
  #recbar button:disabled { opacity: 0.4; cursor: not-allowed; }
  #recstatus { color: #7DD3FC; }
  #recdot {
    width: 10px; height: 10px; border-radius: 50%;
    background: #5A6478; transition: background .2s;
  }
  #recdot.live { background: #F96167; animation: pulse 1s infinite; }
  @keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(249,97,103,0.6); }
    50%      { box-shadow: 0 0 0 8px rgba(249,97,103,0); }
  }
</style>
<div id="brain3d-wrap">
  <div id="recbar">
    <span id="recdot"></span>
    <button id="rec-tour">🎥 Record auto-tour</button>
    <button id="rec-toggle">⏺ Record manual</button>
    <button id="rec-stop" disabled>⏹ Stop</button>
    <a id="rec-download" style="display:none;color:#7DD3FC;text-decoration:none;
        background:#1E2761;border:1px solid #F96167;padding:6px 14px;
        border-radius:6px;">⬇ Download .webm</a>
    <span id="recstatus">idle</span>
  </div>
  <div id="brain3d" style="width:100%;height:""" + str(height) + """px;
                            background:#0F1733;"></div>
</div>
<script src="https://unpkg.com/three@0.149.0/build/three.min.js"></script>
<script src="https://unpkg.com/three-spritetext@1.6.5/dist/three-spritetext.min.js"></script>
<script src="https://unpkg.com/3d-force-graph@1.73.4/dist/3d-force-graph.min.js"></script>
<script>
  const PAL = ['#1E2761','#3B5BA5','#9B59B6','#16A085','#27AE60',
               '#E67E22','#C0392B','#8E44AD','#2C3E50','#D35400',
               '#7F8C8D','#2980B9'];
  const SHOW_LABELS = """ + show_labels_js + """;
  const LABEL_MIN_DEG = """ + str(label_min_degree) + """;
  const data = """ + payload_json + """;
  const el = document.getElementById('brain3d');
  // Kind-based color overrides cluster color when present
  const KIND_COLOR = {
    'def': '#FBB036',   // amber — defense corpus
    'arx': '#7DD3FC',   // sky    — arxiv aggregates
  };
  function nodeColor(n) {
    if (n.kind && KIND_COLOR[n.kind]) return KIND_COLOR[n.kind];
    return PAL[((n.cluster||0) + 12) % PAL.length];
  }
  // Edge color depends on its kind tag (wiki↔def, def↔arx, etc.)
  function linkColor(l) {
    const ks = (l.kinds || []).join(',');
    if (ks.includes('wiki↔def') || ks.includes('def↔arx')) return '#FBB036';
    if (ks.includes('wiki↔arx'))                            return '#7DD3FC';
    if (ks.includes('def↔def'))                             return '#5A6478';
    return '#7DD3FC';
  }
  const G = ForceGraph3D()(el)
    .graphData(data)
    .backgroundColor('#0F1733')
    .nodeLabel(n => `<b>${n.label}</b><br>${n.cluster_name||''} · ${n.kind||'wiki'} · deg ${n.degree}`)
    .nodeColor(nodeColor)
    .nodeVal(n => {
      const base = Math.max(1.5, Math.sqrt(Math.max(1, n.degree)));
      // arxiv aggregates much bigger to reflect they each represent many papers
      if (n.kind === 'arx') return base * 3.5;
      if (n.kind === 'def') return base * 1.1;
      return base;
    })
    .linkColor(linkColor)
    .linkOpacity(0.30)
    .linkWidth(l => (l.kinds || []).join(',').includes('def↔arx') ? 1.2 : 0.6)
    .cooldownTicks(120);

  // Always-visible labels via SpriteText sprites
  if (SHOW_LABELS && typeof SpriteText !== 'undefined') {
    G.nodeThreeObject(n => {
      if ((n.degree || 0) < LABEL_MIN_DEG) return null;
      const sprite = new SpriteText(n.label);
      sprite.material.depthWrite = false;
      sprite.color = '#FAFBFE';
      sprite.backgroundColor = 'rgba(15,23,51,0.6)';
      sprite.padding = 2;
      sprite.borderRadius = 3;
      sprite.textHeight = Math.max(2.2, Math.sqrt(Math.max(1, n.degree)) * 1.5);
      return sprite;
    }).nodeThreeObjectExtend(true);
  }

  G.onNodeClick(n => {
    const dist = 100;
    const ratio = 1 + dist / Math.hypot(n.x, n.y, n.z);
    G.cameraPosition(
      { x: n.x * ratio, y: n.y * ratio, z: n.z * ratio },
      n, 1500);
  });

  // ── Recording ──────────────────────────────────────────────────────
  const recDot = document.getElementById('recdot');
  const recStatus = document.getElementById('recstatus');
  const btnTour = document.getElementById('rec-tour');
  const btnToggle = document.getElementById('rec-toggle');
  const btnStop = document.getElementById('rec-stop');
  const dlLink = document.getElementById('rec-download');
  let recorder = null, chunks = [];

  function getCanvas() {
    return el.querySelector('canvas');
  }

  function startRecorder() {
    const canvas = getCanvas();
    if (!canvas) { recStatus.textContent = 'no canvas yet'; return false; }
    const stream = canvas.captureStream(30);
    chunks = [];
    let mt = 'video/webm;codecs=vp9';
    if (!MediaRecorder.isTypeSupported(mt)) mt = 'video/webm;codecs=vp8';
    if (!MediaRecorder.isTypeSupported(mt)) mt = 'video/webm';
    recorder = new MediaRecorder(stream, { mimeType: mt, videoBitsPerSecond: 2_500_000 });
    recorder.ondataavailable = e => { if (e.data && e.data.size > 0) chunks.push(e.data); };
    recorder.onstop = () => {
      const blob = new Blob(chunks, { type: mt });
      const url = URL.createObjectURL(blob);
      dlLink.href = url;
      dlLink.download = 'brain-tour-' + Date.now() + '.webm';
      dlLink.style.display = 'inline-block';
      dlLink.textContent = '⬇ Download .webm (' +
        Math.round(blob.size/1024) + ' KB)';
      recDot.classList.remove('live');
      recStatus.textContent = 'ready to download';
      btnTour.disabled = false; btnToggle.disabled = false;
      btnStop.disabled = true;
    };
    recorder.start(250);
    recDot.classList.add('live');
    btnTour.disabled = true; btnToggle.disabled = true;
    btnStop.disabled = false;
    dlLink.style.display = 'none';
    return true;
  }

  function stopRecorder() {
    if (recorder && recorder.state === 'recording') recorder.stop();
  }

  btnToggle.onclick = () => {
    if (!startRecorder()) return;
    recStatus.textContent = 'recording — drag/zoom freely, hit Stop when done';
  };

  btnStop.onclick = () => {
    stopRecorder();
  };

  // Auto-tour: fly camera through top-N hubs (highest degree, varied clusters)
  function pickTourNodes(n) {
    const sorted = data.nodes.slice().sort((a,b) => (b.degree||0)-(a.degree||0));
    const seenClusters = new Set();
    const out = [];
    for (const node of sorted) {
      if (out.length >= n) break;
      // Diversity: at most 2 per cluster
      const c = node.cluster || -1;
      const count = out.filter(x => (x.cluster||-1) === c).length;
      if (count >= 2) continue;
      out.push(node);
      seenClusters.add(c);
    }
    return out;
  }

  async function flyTo(node, ms) {
    const dist = 110;
    const r = 1 + dist / Math.max(1, Math.hypot(node.x, node.y, node.z));
    G.cameraPosition(
      { x: node.x * r, y: node.y * r, z: node.z * r },
      node, ms);
    await new Promise(res => setTimeout(res, ms + 200));
  }

  btnTour.onclick = async () => {
    if (!startRecorder()) return;
    const stops = pickTourNodes(10);
    recStatus.textContent = `flying through ${stops.length} stops…`;
    // Pull camera back first to show whole graph
    G.cameraPosition({ x: 0, y: 0, z: 600 }, { x:0, y:0, z:0 }, 1500);
    await new Promise(res => setTimeout(res, 1700));
    for (let i = 0; i < stops.length; i++) {
      recStatus.textContent = `stop ${i+1}/${stops.length}: ${stops[i].label}`;
      await flyTo(stops[i], 2200);
    }
    // Pull back out at end
    recStatus.textContent = 'pulling back…';
    G.cameraPosition({ x: 0, y: 0, z: 600 }, { x:0, y:0, z:0 }, 1800);
    await new Promise(res => setTimeout(res, 2000));
    stopRecorder();
  };
</script>
"""
    st.components.v1.html(html, height=height + 80, scrolling=False)
    st.caption("🖱 drag = orbit  ·  scroll = zoom  ·  click a node to focus  "
                "·  🎥 = auto-tour 10 hubs and record  ·  ⏺ = record while you "
                "drive")


# ── Tab: Propose (idea-to-brain connector) ────────────────────────────────

with tab_propose:
    st.markdown(
        "**Drop an idea, proposal, or question here.** The brain will:\n"
        "1. find every concept it already has that touches your text,\n"
        "2. trace the shortest paths between those concepts,\n"
        "3. surface any non-obvious bridge nodes,\n"
        "4. write a one-paragraph grounded synthesis you can use as "
        "the seed of a real answer.\n\n"
        "_This is the value-add over plain Obsidian: the graph "
        "*responds* instead of just storing._"
    )

    proposal = st.text_area(
        "Your idea / proposal / question",
        placeholder=("e.g. 'I want to design a low-cost boost-phase "
                     "intercept system that uses ML for trajectory "
                     "prediction instead of a Kalman filter — what "
                     "trade-offs should I consider?'"),
        height=140,
        key="proposal_input",
    )

    p_cols = st.columns([1, 1, 1])
    with p_cols[0]:
        prop_mode = st.radio(
            "Synthesis mode",
            options=["auto", "heuristic", "llm"], index=0,
            horizontal=True,
            help="auto = llm if ANTHROPIC_API_KEY set else heuristic.",
        )
    with p_cols[1]:
        prop_k = st.slider("Top concepts", 5, 30, 12, key="prop_k")
    with p_cols[2]:
        st.write(""); st.write("")
        run_btn = st.button("💡 Connect to brain",
                              type="primary", use_container_width=True)

    if run_btn and proposal.strip():
        with st.spinner("Asking the brain…"):
            try:
                from agents.proposal_responder import respond
                result = respond(proposal, k=prop_k,
                                  vault_path=ss.vault_path or None,
                                  mode=prop_mode)
            except Exception as e:
                st.error(f"proposal failed: {e}")
                result = None

        if result:
            # Synthesis card
            with st.container(border=True):
                st.markdown(f"### 🧠 What the brain says ({result['mode']})")
                st.write(result["synthesis"])

            # Two-column: matched concepts + bridge paths
            mc_col, bp_col = st.columns([1, 1])

            with mc_col:
                st.markdown("##### 🎯 Matched concepts")
                if not result["matched_concepts"]:
                    st.caption("_no graph nodes match your text_")
                for m in result["matched_concepts"][:10]:
                    with st.container(border=True):
                        st.markdown(
                            f"**{m['label']}** · score {m['score']}"
                        )
                        st.caption(
                            f"course: {m['cluster_name']} · "
                            f"degree {m['degree']}"
                        )
                        if st.button("Open note",
                                       key=f"prop_open_{m['name']}",
                                       use_container_width=True):
                            if m["name"] in notes:
                                ss.selected_note = m["name"]
                                st.toast("Open the 📓 Notes tab.", icon="📓")
                            else:
                                st.caption("(no wiki page yet)")

            with bp_col:
                st.markdown("##### 🌉 Bridge paths through the graph")
                if not result["bridge_paths"]:
                    st.caption("_no graph paths between matched concepts — "
                                "either the matches are too distant or "
                                "the graph is sparse here_")
                for b in result["bridge_paths"][:5]:
                    with st.container(border=True):
                        path_str = "  →  ".join(
                            f"**{p.replace('_', ' ')}**" for p in b["path"]
                        )
                        st.markdown(path_str)
                        st.caption(
                            f"length {b['length']} · novelty {b['novelty']}"
                        )

            # Related corpus
            related = result.get("related_corpus", {})
            if any(related.get(k) for k in ("rag", "defense", "wiki", "wikipedia")):
                with st.expander("📚 Related corpus content"):
                    if related.get("wiki"):
                        st.markdown(f"**Wiki:** {related['wiki']['path']}")
                    if related.get("rag"):
                        st.markdown(f"**arXiv RAG ({len(related['rag'])}):**")
                        for r in related["rag"][:5]:
                            st.caption(
                                f"  · `{r.get('paper_id','')[:24]}` · "
                                f"score {r.get('_score',0):.2f}"
                            )
                    if related.get("defense"):
                        st.markdown(f"**Defense corpus ({len(related['defense'])}):**")
                        for d in related["defense"][:5]:
                            st.caption(
                                f"  · {(d.get('title') or '')[:60]} · "
                                f"score {d.get('_score',0):.2f}"
                            )
