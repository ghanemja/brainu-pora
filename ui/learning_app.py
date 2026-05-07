"""
Learning Architecture — turn the brain graph into a self-paced "university".

Each cluster of the temporal graph is a "course". Each high-degree node is a
lesson. Bridge nodes connect courses, so a learner can follow their interest
across departments.

Run:
    python -m streamlit run ui/learning_app.py

Independent of the existing apps — does not modify agents_app, graph_evolution,
live_brain, retrieval_inspector, or feedback_panel.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


PROJECT_ROOT = Path(__file__).parent.parent
LEARNERS_DIR = PROJECT_ROOT / "data" / "sessions" / "learners"
LEARNERS_DIR.mkdir(parents=True, exist_ok=True)


st.set_page_config(
    page_title="Brain University",
    page_icon="🎓",
    layout="wide",
)


# ── Session state ─────────────────────────────────────────────────────────

ss = st.session_state
ss.setdefault("learner_id", f"learner-{uuid.uuid4().hex[:8]}")
ss.setdefault("interest", "")
ss.setdefault("current_cluster", None)
ss.setdefault("current_node", None)
ss.setdefault("history", [])           # list of {ts, node, cluster_id, action}
ss.setdefault("mastery", {})           # node → {visits, correct, attempts}
ss.setdefault("tour", None)            # list of TourStop dicts for active session
ss.setdefault("tour_idx", 0)           # current step in the tour
ss.setdefault("graph_source", "auto")  # auto | graphiti | wiki | obsidian
ss.setdefault("vault_path", "")        # populated lazily from env/default
ss.setdefault("quiz_answer", {})       # node→idx (the user's last answer)


def _learner_path() -> Path:
    return LEARNERS_DIR / f"{ss.learner_id}.json"


def _save_learner():
    _learner_path().write_text(json.dumps({
        "learner_id": ss.learner_id,
        "interest":  ss.interest,
        "history":   ss.history[-200:],
        "mastery":   ss.mastery,
        "current_cluster": ss.current_cluster,
        "current_node":    ss.current_node,
    }, indent=2, default=str))


def _load_learner(lid: str) -> bool:
    p = LEARNERS_DIR / f"{lid}.json"
    if not p.exists():
        return False
    try:
        blob = json.loads(p.read_text())
    except json.JSONDecodeError:
        return False
    ss.learner_id       = blob.get("learner_id", lid)
    ss.interest         = blob.get("interest", "")
    ss.history          = blob.get("history", []) or []
    ss.mastery          = blob.get("mastery", {}) or {}
    ss.current_cluster  = blob.get("current_cluster")
    ss.current_node     = blob.get("current_node")
    return True


# ── Sidebar ────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🎓 Brain University")
    st.caption(
        "Wander the knowledge graph cluster-by-cluster. Pick a course, "
        "absorb a lesson, take a quiz, then jump to a related course via "
        "a bridge node."
    )

    st.divider()
    st.subheader("👤 Learner")
    new_lid = st.text_input("Learner ID", value=ss.learner_id,
                             help="Change this to switch learner profiles.")
    if new_lid != ss.learner_id:
        ss.learner_id = new_lid
        _load_learner(new_lid)

    interest = st.text_area(
        "What interests you?", value=ss.interest, height=70,
        placeholder="e.g. 'rocket aerodynamics' or 'graph algorithms for "
                    "robot path planning'",
        help="Drives lesson framing + reorders next-step recommendations.",
    )
    if interest != ss.interest:
        ss.interest = interest
        _save_learner()

    st.divider()
    st.subheader("⚙ Lesson mode")
    lesson_mode = st.radio(
        "Generation",
        options=["auto", "fast", "rich"],
        horizontal=True, index=0,
        help="auto = rich if ANTHROPIC_API_KEY set else fast. "
             "fast = wiki-only, free. rich = Claude tutor, ~1¢/lesson.",
    )

    st.divider()
    st.subheader("🧠 Brain graph")

    # Probe Graphiti reachability — shows which graph the learning app
    # is actually looking at. If FalkorDB is offline, the wiki-only
    # fallback is used and the defense-corpus + classes ingest is invisible.
    @st.cache_data(ttl=15, show_spinner=False)
    def _graph_source_status():
        try:
            from graph.clusters import _load_from_graphiti
            g = _load_from_graphiti()
            if g is None:
                return {"graphiti": False, "n_nodes": 0, "n_edges": 0}
            return {"graphiti": True,
                    "n_nodes": g.number_of_nodes(),
                    "n_edges": g.number_of_edges()}
        except Exception as e:
            return {"graphiti": False, "error": str(e)[:80]}

    status = _graph_source_status()
    if status.get("graphiti"):
        st.success(
            f"Graphiti online · {status['n_nodes']:,}n / {status['n_edges']:,}e "
            f"(includes defense corpus + classes)"
        )
    else:
        st.warning(
            "Graphiti / FalkorDB offline — using wiki cross-links only "
            "(defense corpus + classes invisible). Start FalkorDB:\n"
            "`cd docker && docker compose up -d`"
        )

    ss.graph_source = st.radio(
        "Source",
        options=["auto", "graphiti", "obsidian", "wiki"],
        index=["auto", "graphiti", "obsidian", "wiki"].index(ss.graph_source),
        horizontal=True,
        help="auto = graphiti → obsidian → wiki fallback chain. "
             "graphiti = force-fail if offline. "
             "obsidian = local vault (no Docker, no API key). "
             "wiki = bare wiki/concepts/ folder.",
    )

    # Obsidian vault picker — only show controls when relevant
    if ss.graph_source in ("auto", "obsidian"):
        from graph.obsidian_loader import (
            find_default_vault, vault_metadata, init_vault_for_existing_wiki,
        )
        if not ss.vault_path:
            default = find_default_vault()
            ss.vault_path = str(default) if default else ""
        new_vault = st.text_input(
            "Obsidian vault path",
            value=ss.vault_path,
            placeholder="~/Documents/MyVault or wiki/concepts",
            help="Any folder of .md files works — no `.obsidian/` required. "
                 "Leave blank to fall back to wiki/concepts/.",
        )
        if new_vault != ss.vault_path:
            ss.vault_path = new_vault
        # Quick stats
        if ss.vault_path:
            try:
                meta = vault_metadata(ss.vault_path)
                if meta.get("ok"):
                    badge = "📓 Obsidian vault" if meta["is_obsidian_vault"] \
                            else "📁 plain markdown folder"
                    st.caption(
                        f"{badge} · {meta['n_notes']:,} notes · "
                        f"{meta['n_links']:,} wikilinks · "
                        f"{meta['n_tags']} tags"
                    )
                    if meta["top_tags"]:
                        st.caption("top tags: " + " ".join(
                            f"`#{t}`" for t, _ in meta["top_tags"][:6]
                        ))
                else:
                    st.caption(f"⚠ {meta.get('error','vault not found')}")
            except Exception as e:
                st.caption(f"⚠ vault probe failed: {e}")
        if st.button("📓 Mark this folder as an Obsidian vault",
                       help="Creates `.obsidian/` so you can open the same "
                            "folder in the Obsidian app and browse natively.",
                       use_container_width=True):
            try:
                r = init_vault_for_existing_wiki(ss.vault_path)
                if r.get("ok"):
                    st.success(f"vault marker → {r['marker']}")
                else:
                    st.error(r.get("error", "failed"))
            except Exception as e:
                st.error(f"init failed: {e}")

    if st.button("🔄 Rebuild course catalog", use_container_width=True,
                 help="Re-runs community detection on the live graph."):
        with st.spinner("clustering..."):
            try:
                from graph.clusters import build_clusters
                cs = build_clusters(
                    force=True,
                    source=ss.graph_source,
                    vault_path=ss.vault_path or None,
                )
                st.success(f"detected {len(cs)} courses")
            except Exception as e:
                st.error(f"build failed: {e}")
        st.rerun()

    if st.button("🧹 Reset my progress", use_container_width=True):
        ss.history.clear()
        ss.mastery.clear()
        ss.current_cluster = None
        ss.current_node = None
        _save_learner()
        st.rerun()


# ── Header ────────────────────────────────────────────────────────────────

st.title("🎓 Brain University")
st.caption(f"Learner `{ss.learner_id}`  ·  {len(ss.history)} steps walked  "
            f"·  {len(ss.mastery)} concepts visited")


# ── Load (or build) the course catalog ────────────────────────────────────

@st.cache_data(ttl=120, show_spinner=False)
def _get_clusters():
    from graph.clusters import build_clusters, load_clusters
    cs = load_clusters()
    if cs is None or len(cs) == 0:
        cs = build_clusters(force=False)
    # Also return as plain dicts for cache safety
    return [c.to_dict() for c in cs]


def _restore_clusters(blobs):
    """Reinflate Cluster dataclasses from cache dicts."""
    from graph.clusters import Cluster
    return [
        Cluster(
            cluster_id=int(b["cluster_id"]),
            name=str(b["name"]),
            members=list(b["members"]),
            top_nodes=[(str(n), int(d)) for n, d in b["top_nodes"]],
            bridges=[(str(n), [int(c) for c in cids]) for n, cids in b["bridges"]],
        )
        for b in blobs
    ]


cluster_blobs = _get_clusters()
if not cluster_blobs:
    st.warning(
        "No clusters built yet. The graph might be empty — try running "
        "`scripts/wiki_to_graphiti.py` to seed it, then click 'Rebuild "
        "course catalog' in the sidebar. For now we'll fall back to "
        "wiki-only clustering automatically."
    )
    st.stop()

clusters = _restore_clusters(cluster_blobs)


# ── Visualization helpers (defined here so the entry hero can use them) ──

@st.cache_resource(show_spinner=False)
def _get_nx_graph_cached(source: str, vault_path: str):
    """Keyed cache so swapping source/vault busts it automatically."""
    from graph.clusters import load_graph
    return load_graph(source=source, vault_path=vault_path or None)


def _get_nx_graph():
    return _get_nx_graph_cached(ss.graph_source, ss.vault_path)


def _humanize(s: str) -> str:
    return s.replace("_", " ").strip()


def _net_html(net) -> str:
    out = Path("/tmp/learning_graph.html")
    net.write_html(str(out), notebook=False, open_browser=False)
    return out.read_text()


def _node_color(node: str, *, current: str, visited: set, cluster_color: str,
                is_bridge: bool) -> str:
    if node == current:
        return "#F96167"   # coral pulse — current location
    if node in visited:
        return "#FBB036"   # amber — already learned
    if is_bridge:
        return "#7DD3FC"   # sky — cross-course bridge
    return cluster_color


# Distinct color per cluster (cycle through a 12-color palette)
PALETTE = [
    "#1E2761", "#3B5BA5", "#9B59B6", "#16A085", "#27AE60",
    "#E67E22", "#C0392B", "#8E44AD", "#2C3E50", "#D35400",
    "#7F8C8D", "#2980B9",
]


def _macro_html(clusters, current_cid: int) -> str:
    """One super-node per cluster, edge thickness = bridge count."""
    from pyvis.network import Network
    net = Network(height="540px", width="100%", bgcolor="#0F1733",
                  font_color="#FAFBFE", directed=False, notebook=False)
    net.barnes_hut(gravity=-12000, central_gravity=0.3,
                    spring_length=200, spring_strength=0.04, damping=0.85)
    import math
    for c in clusters:
        col = PALETTE[c.cluster_id % len(PALETTE)]
        is_current = c.cluster_id == current_cid
        net.add_node(
            f"c{c.cluster_id}",
            label=c.name[:24],
            title=f"{c.name}\n{len(c.members)} concepts · {len(c.bridges)} bridges",
            color={
                "background": "#F96167" if is_current else col,
                "border": "#FAFBFE",
            },
            size=18 + 4 * math.sqrt(max(1, len(c.members))),
            font={"color": "#FAFBFE", "size": 14},
        )
    pair_count: dict[tuple[int, int], int] = {}
    for c in clusters:
        for _, other_cids in c.bridges:
            for ocid in other_cids:
                a, b = sorted((c.cluster_id, ocid))
                pair_count[(a, b)] = pair_count.get((a, b), 0) + 1
    for (a, b), n in pair_count.items():
        net.add_edge(f"c{a}", f"c{b}", value=n,
                     color={"color": "#7DD3FC", "opacity": 0.5},
                     width=1 + min(6, n / 2))
    return _net_html(net)


def _course_html(clusters, current_cid: int, current_node: str,
                  visited: set) -> str:
    """All nodes in the current cluster + 1-hop bridge stubs to other clusters."""
    from pyvis.network import Network
    G = _get_nx_graph()
    if G is None:
        return ""
    cur = next((c for c in clusters if c.cluster_id == current_cid), None)
    if cur is None:
        return ""
    cur_col = PALETTE[current_cid % len(PALETTE)]
    bridge_names = {n for n, _ in cur.bridges}
    net = Network(height="540px", width="100%", bgcolor="#0F1733",
                  font_color="#FAFBFE", directed=False, notebook=False)
    net.barnes_hut(gravity=-15000, central_gravity=0.25,
                    spring_length=160, spring_strength=0.04, damping=0.85)
    members_set = set(cur.members)
    def _orig(n):
        return n.replace(" ", "_")
    cur_orig = _orig(current_node) if current_node else ""
    for n in cur.members:
        is_bridge = n in bridge_names or _humanize(n) in bridge_names
        color = _node_color(
            n, current=cur_orig, visited=visited, cluster_color=cur_col,
            is_bridge=is_bridge,
        )
        net.add_node(
            n, label=_humanize(n)[:22], title=_humanize(n),
            color={"background": color, "border": "#FAFBFE"},
            size=22 if n == cur_orig else (16 if is_bridge else 12),
            font={"color": "#FAFBFE", "size": 12},
        )
    for u, v, _ in G.edges(data=True):
        if u in members_set and v in members_set:
            net.add_edge(u, v, color={"color": cur_col, "opacity": 0.6}, width=1.0)
    other_added: set[int] = set()
    for bridge_node, ocids in cur.bridges:
        b_orig = _orig(bridge_node)
        if b_orig not in members_set:
            continue
        for ocid in ocids:
            if ocid in other_added:
                continue
            other = next((c for c in clusters if c.cluster_id == ocid), None)
            if other is None:
                continue
            ocol = PALETTE[ocid % len(PALETTE)]
            stub_id = f"c{ocid}_stub"
            net.add_node(
                stub_id, label=f"→ {other.name[:18]}",
                title=f"course: {other.name}",
                color={"background": ocol, "border": "#FAFBFE"},
                size=16, shape="diamond",
                font={"color": "#FAFBFE", "size": 11, "italic": True},
            )
            net.add_edge(b_orig, stub_id,
                          color={"color": "#7DD3FC", "opacity": 0.7},
                          width=2.0, dashes=True)
            other_added.add(ocid)
    return _net_html(net)


def _neighborhood_html(clusters, current_cid: int, current_node: str,
                        visited: set, hops: int = 2) -> str:
    """Current node + N-hop neighbours in the underlying graph."""
    from pyvis.network import Network
    import networkx as nx
    G = _get_nx_graph()
    if G is None or not current_node:
        return ""
    cur_orig = current_node.replace(" ", "_")
    if cur_orig not in G:
        return ""
    sub = nx.ego_graph(G, cur_orig, radius=hops, undirected=True)
    cur_col = PALETTE[current_cid % len(PALETTE)]
    node_to_cid = {}
    for c in clusters:
        for m in c.members:
            node_to_cid[m] = c.cluster_id
    net = Network(height="540px", width="100%", bgcolor="#0F1733",
                  font_color="#FAFBFE", directed=False, notebook=False)
    net.barnes_hut(gravity=-22000, central_gravity=0.4,
                    spring_length=140, spring_strength=0.05, damping=0.85)
    for n in sub.nodes():
        cid = node_to_cid.get(n, current_cid)
        col = PALETTE[cid % len(PALETTE)]
        is_current = (n == cur_orig)
        size = 28 if is_current else (16 if cid == current_cid else 12)
        background = (
            "#F96167" if is_current else
            "#FBB036" if n in visited else
            col
        )
        net.add_node(
            n, label=_humanize(n)[:22],
            title=f"{_humanize(n)} · cluster {cid}",
            color={"background": background, "border": "#FAFBFE"},
            size=size,
            font={"color": "#FAFBFE", "size": 12, "bold": is_current},
        )
    for u, v in sub.edges():
        net.add_edge(u, v, color={"color": "#FAFBFE", "opacity": 0.4}, width=0.8)
    return _net_html(net)


# ── Entry hero ────────────────────────────────────────────────────────────
# When the learner has nothing in progress, show the brain-graph hero
# (macro view) and a "Start here" recommendation strip — derived from
# graph-foundation scoring (degree + cluster-span + pagerank + RL feedback).
# Once a current_node is set, this whole block collapses into an expander.

@st.cache_data(ttl=300, show_spinner=False)
def _foundation_picks(interest: str, limit: int = 5):
    from graph.foundations import recommend, recommend_for_interest
    if interest.strip():
        return [f.to_dict() for f in recommend_for_interest(interest, limit=limit)]
    return [f.to_dict() for f in recommend(limit=limit)]


def _enter_node(node: str, cluster_id: int, action: str = "start_here",
                with_tour: bool = True):
    ss.current_cluster = cluster_id
    ss.current_node = node
    ss.history.append({
        "ts": time.time(),
        "action": action,
        "cluster_id": cluster_id,
        "node": node,
    })
    ss.mastery.setdefault(node, {"visits": 0, "correct": 0, "attempts": 0})\
        ["visits"] = ss.mastery.setdefault(node, {}).get("visits", 0) + 1
    # Auto-build a 6-stop lesson tour from this node so the learner sees
    # the planned traversal path before they dive in.
    if with_tour:
        try:
            from agents.lesson_plan import plan_tour
            stops = plan_tour(node, max_stops=6)
            ss.tour = [s.to_dict() for s in stops]
            ss.tour_idx = 0
        except Exception:
            ss.tour = None
            ss.tour_idx = 0
    _save_learner()


def _advance_tour(delta: int = 1):
    """Move the tour cursor by ±1 and update current_node accordingly."""
    if not ss.tour:
        return
    new_idx = max(0, min(len(ss.tour) - 1, ss.tour_idx + delta))
    if new_idx == ss.tour_idx:
        return
    ss.tour_idx = new_idx
    stop = ss.tour[new_idx]
    ss.current_cluster = stop["cluster_id"]
    ss.current_node = stop["node"]
    ss.history.append({
        "ts": time.time(),
        "action": f"tour_step_{stop.get('kind','?')}",
        "cluster_id": stop["cluster_id"],
        "node": stop["node"],
    })
    m = ss.mastery.setdefault(stop["node"],
                                {"visits": 0, "correct": 0, "attempts": 0})
    m["visits"] = m.get("visits", 0) + 1
    _save_learner()


def _render_entry_hero(clusters, picks):
    """The hero panel shown when nothing is selected yet."""
    st.markdown("### 🧠 Your brain map")
    st.caption(
        "Each cluster on the map is a course. Bigger nodes = bigger courses; "
        "blue edges connect courses through shared bridge concepts. "
        "Ranked recommendations below are auto-picked starting points "
        "based on graph centrality + your stated interest."
    )

    hero_l, hero_r = st.columns([3, 2], gap="large")

    with hero_l:
        try:
            html = _macro_html(clusters, current_cid=-1)
            st.components.v1.html(html, height=520, scrolling=False)
        except Exception as e:
            st.warning(f"map render failed: {e}")

    with hero_r:
        st.markdown("#### 🎯 Start here")
        if not picks:
            st.caption("_no recommendations yet — try 'Rebuild course catalog' "
                        "in the sidebar_")
        for i, p in enumerate(picks):
            with st.container(border=True):
                head = st.columns([4, 1])
                with head[0]:
                    st.markdown(f"**{p['name']}**")
                    st.caption(f"course: {p['cluster_name']}")
                with head[1]:
                    st.metric("score", f"{p['score']:.2f}",
                                label_visibility="collapsed")
                st.caption(p["rationale"])
                m = p.get("metrics", {})
                badges = []
                if m.get("degree"):       badges.append(f"⛓ {m['degree']}")
                if m.get("cluster_span"): badges.append(f"🌉 {m['cluster_span']}")
                if m.get("cluster_size"): badges.append(f"📚 {m['cluster_size']}")
                if m.get("has_wiki"):     badges.append("📄 wiki")
                if m.get("rl_weight", 0) > 0:
                    badges.append(f"🌟 +{m['rl_weight']:.2f}")
                if badges:
                    st.caption(" · ".join(badges))
                if st.button("Start with this concept",
                              key=f"start_{i}_{p['raw_name']}",
                              use_container_width=True, type="primary"):
                    _enter_node(p["raw_name"], p["cluster_id"], "start_here")
                    st.rerun()


if ss.current_node is None:
    picks = _foundation_picks(ss.interest, limit=5)
    _render_entry_hero(clusters, picks)
    with st.expander(f"📚 Browse all {len(clusters)} courses"):
        df_rows = []
        for c in clusters:
            df_rows.append({
                "course": c.name,
                "concepts": len(c.members),
                "bridges": len(c.bridges),
                "top concepts": ", ".join(n for n, _ in c.top_nodes[:5]),
            })
        import pandas as pd
        st.dataframe(pd.DataFrame(df_rows), use_container_width=True,
                      hide_index=True)
        st.caption("Pick a course by clicking 'Enter' below.")
        catalog_cols = st.columns(min(4, len(clusters)) or 1)
        for i, c in enumerate(clusters[: 4 * 3]):
            col = catalog_cols[i % len(catalog_cols)]
            with col:
                with st.container(border=True):
                    st.markdown(f"**{c.name}**")
                    st.caption(f"{len(c.members)} concepts · {len(c.bridges)} bridges")
                    top = ", ".join(n for n, _ in c.top_nodes[:3])
                    st.caption(top)
                    if st.button("Enter", key=f"enter_{c.cluster_id}",
                                  use_container_width=True):
                        _enter_node(
                            c.top_nodes[0][0] if c.top_nodes else c.members[0],
                            c.cluster_id, "enter_cluster",
                        )
                        st.rerun()
else:
    # Once a lesson is in progress, hide the hero behind an expander
    with st.expander("📚 Course catalog (browse)", expanded=False):
        catalog_cols = st.columns(min(4, len(clusters)) or 1)
        for i, c in enumerate(clusters[: 4 * 3]):
            col = catalog_cols[i % len(catalog_cols)]
            with col:
                with st.container(border=True):
                    is_current = ss.current_cluster == c.cluster_id
                    st.markdown(f"{'🟢 ' if is_current else ''}**{c.name}**")
                    st.caption(f"{len(c.members)} concepts · {len(c.bridges)} bridges")
                    if st.button("Enter", key=f"catalog_{c.cluster_id}",
                                  use_container_width=True):
                        _enter_node(
                            c.top_nodes[0][0] if c.top_nodes else c.members[0],
                            c.cluster_id, "enter_cluster",
                        )
                        st.rerun()


# ── Active lesson ─────────────────────────────────────────────────────────

if ss.current_cluster is None or ss.current_node is None:
    # Hero already rendered above with recommended starting points;
    # nothing more to show until the learner picks one.
    st.stop()

active = next((c for c in clusters if c.cluster_id == ss.current_cluster), None)
if active is None:
    st.error("Current cluster vanished — pick another above.")
    st.stop()

st.divider()
st.subheader(f"📖 Lesson — {ss.current_node}")
st.caption(f"Course: **{active.name}**  ·  cluster id `{active.cluster_id}`")


@st.cache_data(ttl=300, show_spinner="Building lesson…")
def _build_lesson(node: str, cluster_id: int, interest: str, mode: str,
                  catalog_blobs):
    from agents.curriculum import lesson_for
    cs = _restore_clusters(catalog_blobs)
    cluster = next((c for c in cs if c.cluster_id == cluster_id), None)
    if cluster is None:
        return None
    return lesson_for(node, cluster, cs, interest=interest, mode=mode)


lesson = _build_lesson(
    ss.current_node, active.cluster_id, ss.interest, lesson_mode,
    cluster_blobs,
)
if lesson is None:
    st.error("Failed to build lesson — try a different node.")
    st.stop()


def _record_attempt(node: str, picked: str | None, choices: list[str],
                    correct_idx: int, why: str):
    if picked is None:
        st.warning("pick a choice first")
        return
    correct = choices[correct_idx] if 0 <= correct_idx < len(choices) else ""
    is_right = (picked == correct)
    m = ss.mastery.setdefault(node, {"visits": 0, "correct": 0, "attempts": 0})
    m["attempts"] = m.get("attempts", 0) + 1
    if is_right:
        m["correct"] = m.get("correct", 0) + 1
        st.success(f"✓ Correct. {why}")
    else:
        st.error(f"✗ Not quite. Correct: {correct} — {why}")
    ss.history.append({
        "ts": time.time(),
        "action": "quiz",
        "node": node,
        "correct": is_right,
    })
    _save_learner()


# ── Tabs ──────────────────────────────────────────────────────────────────

tab_tour, tab_lesson, tab_watch, tab_sources, tab_map, tab_next, tab_progress = st.tabs([
    "🎬 Tour", "📖 Lesson", "🎬 Watch", "📚 Sources",
    "🗺️ Map", "🧭 Next", "📊 Progress",
])


# ── Tab: Tour (lesson plan storyline + animated traversal) ─────────────────

with tab_tour:
    if not ss.tour:
        st.info(
            "No tour yet. Pick a starting concept on the entry page (or "
            "click 'Start with this concept' on a recommendation card) — "
            "a 6-stop tour is auto-generated."
        )
    else:
        n = len(ss.tour)
        idx = ss.tour_idx
        cur = ss.tour[idx]

        # Progress
        st.progress((idx + 1) / n,
                     text=f"Stop {idx + 1} of {n}  ·  {cur['kind']} → "
                          f"{cur['name']}  ·  course: {cur['cluster_name']}")

        # Storyline overview (collapsible)
        with st.expander("📜 Full tour overview", expanded=(idx == 0)):
            for i, stop in enumerate(ss.tour):
                marker = "🟢" if i == idx else ("✅" if i < idx else "⚪")
                kind_emoji = {"start": "🚀", "deepen": "🔬",
                                "bridge": "🌉", "capstone": "🏁"}.get(stop["kind"], "•")
                st.markdown(
                    f"{marker} **{i + 1}.** {kind_emoji} **{stop['name']}** "
                    f"_(course: {stop['cluster_name']})_"
                )
                st.caption(stop["rationale"])

        # Tour graph viz — the path animated/highlighted
        st.markdown("##### 🗺 Tour path on the graph")
        try:
            from pyvis.network import Network
            G = _get_nx_graph()
            net = Network(height="480px", width="100%", bgcolor="#0F1733",
                          font_color="#FAFBFE", directed=True, notebook=False)
            net.barnes_hut(gravity=-18000, central_gravity=0.3,
                            spring_length=160, spring_strength=0.05, damping=0.85)

            # Build node→cluster lookup for cluster coloring
            node_to_cid = {}
            for c in clusters:
                for m in c.members:
                    node_to_cid[m] = c.cluster_id

            # Render every visited & upcoming tour stop + 1-hop context
            tour_nodes = [s["node"] for s in ss.tour]
            shown: set[str] = set()
            for i, stop in enumerate(ss.tour):
                node = stop["node"]
                if node not in G:
                    continue
                shown.add(node)
                col_pal = PALETTE[stop["cluster_id"] % len(PALETTE)]
                if i == idx:
                    bg, size = "#F96167", 30           # current — coral
                elif i < idx:
                    bg, size = "#FBB036", 22           # past — amber
                else:
                    bg, size = col_pal, 18             # future — cluster color
                net.add_node(
                    node, label=f"{i+1}. {stop['name'][:18]}",
                    title=f"{stop['name']}\n{stop['kind']}",
                    color={"background": bg, "border": "#FAFBFE"},
                    size=size,
                    font={"color": "#FAFBFE", "size": 12 + (4 if i == idx else 0),
                           "bold": (i == idx)},
                )
                # Add 1-hop context for the current stop (small grey nodes)
                if i == idx:
                    for nbr in list(G.neighbors(node))[:8]:
                        if nbr in tour_nodes or nbr in shown:
                            continue
                        net.add_node(
                            nbr, label=_humanize(nbr)[:18],
                            color={"background": "#3B5BA5",
                                    "border": "#7DD3FC"},
                            size=10,
                            font={"color": "#FAFBFE", "size": 10},
                        )
                        net.add_edge(node, nbr,
                                       color={"color": "#7DD3FC", "opacity": 0.4},
                                       width=0.6, dashes=True)
                        shown.add(nbr)

            # Tour-order arrows between consecutive stops
            for i in range(len(ss.tour) - 1):
                a, b = ss.tour[i]["node"], ss.tour[i + 1]["node"]
                if a not in shown or b not in shown:
                    continue
                col = "#FBB036" if i < idx else (
                      "#F96167" if i == idx else "#5A6478")
                net.add_edge(a, b, arrows="to",
                              color={"color": col, "opacity": 0.95},
                              width=2.5, smooth={"type": "curvedCW"})

            html = _net_html(net)
            st.components.v1.html(html, height=500, scrolling=False)
            st.caption(
                "🟢 you are here  ·  ✅ done  ·  ⚪ upcoming  ·  arrows show "
                "tour order. Drag/zoom to explore."
            )
        except Exception as e:
            st.warning(f"tour viz error: {e}")

        # Current-stop card + nav
        with st.container(border=True):
            st.markdown(f"### Stop {idx + 1}: {cur['name']}")
            kind_label = {
                "start":    "🚀 Starting point",
                "deepen":   "🔬 Going deeper in the same course",
                "bridge":   "🌉 Bridging to a related course",
                "capstone": "🏁 Capstone — wrap up",
            }.get(cur["kind"], cur["kind"])
            st.caption(f"{kind_label}  ·  course: {cur['cluster_name']}")
            st.markdown(cur["rationale"])
            if cur.get("metrics"):
                m = cur["metrics"]
                badges = []
                if m.get("degree"):   badges.append(f"⛓ degree {m['degree']}")
                if m.get("pagerank"): badges.append(f"📊 pagerank {m['pagerank']:.3f}")
                if badges:
                    st.caption(" · ".join(badges))

        nav = st.columns(3)
        with nav[0]:
            if st.button("‹ Previous stop", disabled=(idx == 0),
                          use_container_width=True, key="tour_prev"):
                _advance_tour(-1)
                st.rerun()
        with nav[1]:
            if st.button("📖 Read this lesson", use_container_width=True,
                          type="primary", key="tour_read"):
                # Already on this node; just nudge user toward Lesson tab
                st.toast("Switch to the 📖 Lesson tab to read.", icon="📖")
        with nav[2]:
            if st.button("Next stop ›", disabled=(idx == n - 1),
                          use_container_width=True, key="tour_next"):
                _advance_tour(1)
                st.rerun()

        if st.button("🔁 Replan tour from current concept",
                      help="Throw out the current tour and plan a fresh one "
                           "starting from the current concept."):
            try:
                from agents.lesson_plan import plan_tour
                stops = plan_tour(ss.current_node, max_stops=6)
                ss.tour = [s.to_dict() for s in stops]
                ss.tour_idx = 0
                _save_learner()
                st.rerun()
            except Exception as e:
                st.error(f"replan failed: {e}")


# ── Tab: Lesson ───────────────────────────────────────────────────────────

with tab_lesson:
    with st.container(border=True):
        st.markdown(f"### {lesson['title']}")
        st.caption(f"_lesson mode: {lesson.get('mode', '?')}_")
        st.write(lesson["summary"])

        if lesson.get("key_ideas"):
            st.markdown("**Key ideas**")
            for k in lesson["key_ideas"]:
                st.markdown(f"- {k}")

        if lesson.get("worked_example"):
            st.markdown("**Worked example**")
            st.info(lesson["worked_example"])

        if lesson.get("evidence"):
            st.caption("Evidence: " + " · ".join(lesson["evidence"]))

    quiz = lesson.get("quiz") or []
    if quiz:
        st.markdown("#### ✅ Comprehension check")
        for qi, item in enumerate(quiz):
            with st.container(border=True):
                st.markdown(f"**Q{qi+1}.** {item['q']}")
                choices = item.get("a_choices") or []
                key = f"q_{ss.current_node}_{qi}"
                picked = st.radio(
                    "Pick one:", choices, key=key,
                    index=None, label_visibility="collapsed",
                )
                check_key = f"check_{ss.current_node}_{qi}"
                if st.button("Check", key=check_key):
                    _record_attempt(ss.current_node, picked, choices,
                                    item.get("correct_idx", 0),
                                    item.get("why", ""))
                    st.rerun()

    eng = lesson.get("engagement_question")
    if eng:
        st.markdown("#### 🤔 Reflect")
        response = st.text_area(
            "Your answer", key=f"eng_{ss.current_node}",
            height=80, label_visibility="collapsed",
        )
        if response and st.button("Save reflection",
                                    key=f"eng_save_{ss.current_node}"):
            ss.history.append({
                "ts": time.time(),
                "action": "reflection",
                "node": ss.current_node,
                "text": response[:500],
            })
            _save_learner()
            st.success("Saved.")


# ── Tab: Watch (videos + auto-narrated slides) ────────────────────────────

with tab_watch:
    st.markdown("**Auto-explainer slideshow** + curated YouTube videos. "
                 "All sourced fresh per topic; everything cached.")

    watch_cols = st.columns([1, 1])

    # Slideshow + AI-generated mp4
    with watch_cols[0]:
        st.markdown("##### 🎞 Auto explainer")
        sub_a, sub_b = st.tabs(["HTML slideshow", "Render mp4"])

        # ── HTML slideshow (browser-only, instant) ──
        with sub_a:
            slide_secs = st.slider("Seconds per slide", 4, 15, 7,
                                     key="slide_secs")
            narrate_on = st.checkbox(
                "Narrate (TTS)", value=False,
                help="gTTS online → pyttsx3 offline fallback",
            )
            try:
                from agents.media import slides_html, narrate, narration_script
                audio_url = None
                if narrate_on:
                    with st.spinner("Generating narration…"):
                        script = narration_script(lesson)
                        audio_path = narrate(script)
                    if audio_path and audio_path.exists():
                        st.audio(str(audio_path))
                    else:
                        st.caption("_narration unavailable — install gTTS or "
                                    "pyttsx3, or check internet_")
                html = slides_html(lesson, audio_url=audio_url,
                                    seconds_per_slide=slide_secs)
                st.components.v1.html(html, height=460, scrolling=False)
            except Exception as e:
                st.warning(f"slideshow error: {e}")

        # ── Real mp4 render (PIL + gTTS + moviepy) ──
        with sub_b:
            try:
                from agents.video_generator import (
                    generate, cached_path_for, stack_ready,
                )
                ready = stack_ready()
                missing = [k for k in ("PIL", "moviepy", "ffmpeg")
                           if not ready.get(k)]
                if missing:
                    st.warning(
                        f"Missing: {', '.join(missing)}. Install:\n"
                        "`pip install --user moviepy gTTS Pillow`"
                    )
                else:
                    style_pick = st.selectbox(
                        "Style", options=["dark", "light"], index=0,
                        key="vid_style",
                    )
                    voice_pick = st.selectbox(
                        "Narration", options=["auto", "gtts", "pyttsx3", "none"],
                        index=0, key="vid_voice",
                        help="auto = gtts online → pyttsx3 fallback",
                    )

                    cached = cached_path_for(lesson, voice=voice_pick,
                                              style=style_pick)
                    if cached:
                        st.success(f"Cached render available "
                                    f"({cached.stat().st_size // 1024} KB)")
                        st.video(str(cached))
                        st.download_button(
                            "⬇ Download mp4",
                            data=cached.read_bytes(),
                            file_name=f"{ss.current_node.replace(' ','_')}.mp4",
                            mime="video/mp4",
                            key=f"dl_{cached.stem}",
                        )
                    else:
                        if st.button("🎬 Generate mp4 (~25–60s)",
                                       use_container_width=True,
                                       key="gen_mp4"):
                            prog = st.progress(0.0, text="Starting…")
                            stage_total = 4   # render+narrate+stitch+encode
                            n_slides = (
                                1 + (1 if lesson.get("summary") else 0)
                                  + len(lesson.get("key_ideas") or [])
                                  + (1 if lesson.get("worked_example") else 0)
                                  + (1 if lesson.get("engagement_question") else 0)
                                  + 1
                            )
                            seen = {"render": 0, "narrate": 0}

                            def _cb(evt):
                                kind, i, total = evt
                                if kind == "render_slide":
                                    seen["render"] = i
                                    prog.progress(
                                        0.1 + 0.40 * (i / max(total, 1)),
                                        text=f"Rendering slide {i}/{total}…",
                                    )
                                elif kind == "narrate_slide":
                                    seen["narrate"] = i
                                    prog.progress(
                                        0.50 + 0.30 * (i / max(total, 1)),
                                        text=f"Narrating slide {i}/{total}…",
                                    )
                                elif kind == "stitching":
                                    prog.progress(0.85, text="Stitching video…")
                                elif kind == "encoding":
                                    prog.progress(0.95, text="Encoding mp4…")

                            v_voice = voice_pick if voice_pick != "none" else "gtts"
                            with st.spinner("Building video…"):
                                out = generate(
                                    lesson, voice=v_voice, style=style_pick,
                                    progress_cb=_cb,
                                )
                            prog.progress(1.0, text="Done")
                            if out and out.exists():
                                st.success(
                                    f"Rendered ({out.stat().st_size // 1024} KB)"
                                )
                                st.video(str(out))
                                st.download_button(
                                    "⬇ Download mp4",
                                    data=out.read_bytes(),
                                    file_name=f"{ss.current_node.replace(' ','_')}.mp4",
                                    mime="video/mp4",
                                    key=f"dl_{out.stem}",
                                )
                            else:
                                st.error(
                                    "Render failed. Check the terminal for "
                                    "moviepy / ffmpeg errors."
                                )
            except Exception as e:
                st.warning(f"video gen error: {e}")

    # YouTube
    with watch_cols[1]:
        st.markdown("##### ▶ YouTube")
        topic_for_search = (ss.interest + " " if ss.interest else "") + ss.current_node
        st.caption(f"Searching: `{topic_for_search}`")
        try:
            from agents.media import find_videos
            with st.spinner("Searching YouTube…"):
                vids = find_videos(topic_for_search, k=3)
            if not vids:
                st.caption("_no videos found (or YouTube blocked the scrape)_")
            for v in vids:
                with st.container(border=True):
                    st.markdown(f"**{v['title']}**")
                    st.caption(f"{v.get('channel','')} · {v.get('duration','')}")
                    st.video(v["watch_url"])
        except Exception as e:
            st.warning(f"video search error: {e}")


# ── Tab: Sources (RAG-first, web-fallback) ────────────────────────────────

with tab_sources:
    st.markdown("**Where this concept appears.** Local first (wiki + arXiv "
                 "BM25 + defense corpus), web fallback only if asked.")
    web_on = st.toggle(
        "Also fetch from web (Wikipedia + DuckDuckGo)", value=False,
        help="Off by default to keep things fast and local.",
    )

    @st.cache_data(ttl=120, show_spinner="Searching corpus…")
    def _fetch_sources(topic: str, with_web: bool) -> dict:
        from agents.content_finder import find, find_with_web
        return (find_with_web(topic) if with_web else find(topic, allow_web=True))

    src = _fetch_sources(ss.current_node, web_on)

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Wiki",       1 if src.get("wiki") else 0)
    s2.metric("arXiv RAG",  len(src.get("rag") or []))
    s3.metric("Defense",    len(src.get("defense") or []))
    s4.metric("Web",        (1 if src.get("wikipedia") else 0)
                              + len(src.get("web") or []))

    if src.get("wiki"):
        with st.expander("📄 Local wiki page", expanded=True):
            st.caption(src["wiki"]["path"])
            st.markdown(src["wiki"]["text"][:2500])

    if src.get("rag"):
        with st.expander(f"🔬 arXiv BM25 hits ({len(src['rag'])})"):
            for r in src["rag"][:8]:
                st.markdown(
                    f"- **{r.get('domain','?')}** · `{r.get('paper_id','')}` "
                    f"· score {r.get('_score',0):.2f}"
                )
                snippet = (r.get("text") or "")[:240]
                if snippet:
                    st.caption(snippet)

    if src.get("defense"):
        with st.expander(f"🛡 Defense corpus ({len(src['defense'])})"):
            for d in src["defense"]:
                st.markdown(f"- **{d.get('title','(untitled)')[:90]}** "
                              f"· `{d.get('source','')}` · score {d.get('_score',0):.2f}")
                if d.get("url"):
                    st.markdown(f"  [{d['url']}]({d['url']})")

    if src.get("wikipedia"):
        with st.expander("🌐 Wikipedia (web)"):
            wiki = src["wikipedia"]
            st.markdown(f"**{wiki.get('title','')}**")
            st.write(wiki.get("extract", ""))
            if wiki.get("url"):
                st.markdown(f"[Read on Wikipedia →]({wiki['url']})")

    if src.get("web"):
        with st.expander(f"🔍 Web search ({len(src['web'])})"):
            for w in src["web"]:
                st.markdown(f"- **{w.get('title','')}**")
                if w.get("snippet"):
                    st.caption(w["snippet"])
                if w.get("url"):
                    st.markdown(f"  [{w['url']}]({w['url']})")


# ── Tab: Map (the existing 3-zoom viz) ────────────────────────────────────

with tab_map:
    view_cols = st.columns([3, 1])
    with view_cols[0]:
        zoom = st.radio(
            "Zoom level",
            options=["macro (all courses)", "course (this cluster)", "neighborhood (this concept)"],
            index=1, horizontal=True, label_visibility="collapsed",
        )
    with view_cols[1]:
        show_viz = st.toggle("Show map", value=True,
                              help="Pyvis graph render — turn off if slow")


    if show_viz:
        visited_set = set(ss.mastery.keys()) | {h.get("node", "") for h in ss.history}
        visited_set = {v.replace(" ", "_") for v in visited_set if v}
        try:
            if zoom.startswith("macro"):
                html = _macro_html(clusters, ss.current_cluster)
            elif zoom.startswith("course"):
                html = _course_html(clusters, ss.current_cluster,
                                     ss.current_node, visited_set)
            else:
                html = _neighborhood_html(clusters, ss.current_cluster,
                                           ss.current_node, visited_set)
            if html:
                st.components.v1.html(html, height=560, scrolling=False)
                st.caption(
                    "🔴 here  ·  🟡 visited  ·  🔵 cross-course bridge  ·  "
                    "node colors = cluster colors. Drag to pan, scroll to zoom."
                )
            else:
                st.caption("_no graph available for this view_")
        except ImportError:
            st.warning("pyvis not installed: `pip install pyvis networkx`")
        except Exception as e:
            st.warning(f"viz error: {e}")


# ── Tab: Next ─────────────────────────────────────────────────────────────

with tab_next:
    nav_cols = st.columns(3)

    # Deeper in this course
    with nav_cols[0]:
        st.markdown("**Stay in this course**")
        next_in = lesson.get("next_in_cluster") or []
        if not next_in:
            st.caption("_no more lessons here — move on_")
        for i, nxt in enumerate(next_in[:5]):
            if st.button(nxt, key=f"deep_{i}", use_container_width=True):
                ss.current_node = nxt
                ss.history.append({
                    "ts": time.time(),
                    "action": "deeper_in_cluster",
                    "node": nxt,
                    "cluster_id": ss.current_cluster,
                })
                ss.mastery.setdefault(nxt, {"visits": 0, "correct": 0, "attempts": 0})\
                    ["visits"] = ss.mastery.setdefault(nxt, {}).get("visits", 0) + 1
                _save_learner()
                st.rerun()

    # Bridge to a related course
    with nav_cols[1]:
        st.markdown("**Bridge to a related course**")
        bridges = lesson.get("bridge_options") or []
        if not bridges:
            st.caption("_no cross-course bridges from this concept_")
        for i, (bnode, cid, cname) in enumerate(bridges[:5]):
            if st.button(f"➜ {cname}\n_via {bnode}_", key=f"bridge_{i}",
                         use_container_width=True):
                ss.current_cluster = cid
                ss.current_node = bnode
                ss.history.append({
                    "ts": time.time(),
                    "action": "bridge",
                    "from_cluster": active.cluster_id,
                    "to_cluster": cid,
                    "node": bnode,
                })
                _save_learner()
                st.rerun()

    # Surprise me
    with nav_cols[2]:
        st.markdown("**Surprise me**")
        if st.button("Random connected concept", use_container_width=True):
            candidates = [m for m in active.members
                          if m != ss.current_node]
            if candidates:
                random.shuffle(candidates)
                unvisited = [m for m in candidates if m not in ss.mastery]
                pick = (unvisited or candidates)[0]
                ss.current_node = pick
                ss.history.append({
                    "ts": time.time(),
                    "action": "surprise",
                    "node": pick,
                    "cluster_id": ss.current_cluster,
                })
                _save_learner()
                st.rerun()
            else:
                st.caption("nothing else here")
        if st.button("Random course", use_container_width=True):
            c = random.choice(clusters)
            ss.current_cluster = c.cluster_id
            ss.current_node = c.top_nodes[0][0] if c.top_nodes else None
            ss.history.append({
                "ts": time.time(),
                "action": "surprise_course",
                "cluster_id": c.cluster_id,
                "node": ss.current_node,
            })
            _save_learner()
            st.rerun()


# ── Tab: Progress ─────────────────────────────────────────────────────────

with tab_progress:
    if ss.mastery:
        m_rows = []
        for node, stats in sorted(ss.mastery.items(),
                                    key=lambda kv: kv[1].get("visits", 0),
                                    reverse=True):
            attempts = stats.get("attempts", 0)
            correct = stats.get("correct", 0)
            acc = (correct / attempts) if attempts else None
            m_rows.append({
                "concept": node,
                "visits":  stats.get("visits", 0),
                "quiz attempts": attempts,
                "correct":      correct,
                "accuracy":     "—" if acc is None else f"{acc:.0%}",
            })
        import pandas as pd
        st.dataframe(pd.DataFrame(m_rows[:25]), use_container_width=True,
                      hide_index=True)
    else:
        st.caption("_no concepts visited yet — start a lesson_")

    with st.expander("Recent path (last 15 steps)"):
        for h in reversed(ss.history[-15:]):
            ts = time.strftime("%H:%M:%S", time.localtime(h.get("ts", 0)))
            st.caption(f"`{ts}` · **{h.get('action')}** · {h.get('node') or '–'} "
                        f"(cluster {h.get('cluster_id', h.get('to_cluster', '–'))})")
