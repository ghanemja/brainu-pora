"""
RL Feedback Panel — give thumbs/comments on past agent turns and watch the
brain's weights, agent EWMAs, and lifespans in real time.

Run:
    python -m streamlit run ui/feedback_panel.py

Three tabs:
  ① Roster      — live agents + dead cohort cemetery
  ② Recent turns — last N turns with thumbs-up/down + comment
  ③ Graph weights — top-weighted entities (what the brain currently "cares" about)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


PROJECT_ROOT = Path(__file__).parent.parent
SESSIONS_DIR = PROJECT_ROOT / "data" / "sessions"
TURNS_LOG    = SESSIONS_DIR / "turns.jsonl"
SESS_LOG     = SESSIONS_DIR / "sessions.jsonl"


st.set_page_config(
    page_title="RL Feedback Panel",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 RL Feedback Panel")
st.caption(
    "Tune the brain. Thumbs ↑ / ↓ on past turns reweight graph edges. "
    "Agents with low rolling quality get killed; their citation history is "
    "negative-replayed against the graph (eligibility-trace penalty)."
)


# ── Sidebar — global RL controls ──────────────────────────────────────────

with st.sidebar:
    st.subheader("⚙ Tunables (env)")
    import os
    st.caption(f"`RL_KILL_THRESHOLD` = {os.environ.get('RL_KILL_THRESHOLD', '0.30')}")
    st.caption(f"`RL_BAD_STREAK_KILL` = {os.environ.get('RL_BAD_STREAK_KILL', '5')}")
    st.caption(f"`RL_POS_DELTA` = {os.environ.get('RL_POS_DELTA', '0.20')}")
    st.caption(f"`RL_NEG_DELTA` = {os.environ.get('RL_NEG_DELTA', '-0.20')}")
    st.caption(f"`RL_HEBBIAN_DELTA` = {os.environ.get('RL_HEBBIAN_DELTA', '0.05')}")
    st.caption(f"`RL_DECAY_RATE` = {os.environ.get('RL_DECAY_RATE', '0.99')}")

    st.divider()
    st.subheader("🧹 Maintenance")
    if st.button("Decay all weights once", help="Apply RL_DECAY_RATE multiplier"):
        try:
            from agents.feedback import decay_idle
            r = decay_idle()
            st.success(f"decay run: {r}")
        except Exception as e:
            st.error(f"decay failed: {e}")


# ── Tabs ──────────────────────────────────────────────────────────────────

tab_roster, tab_turns, tab_weights = st.tabs(
    ["① Roster", "② Recent turns", "③ Graph weights"]
)


# ── ① Roster ──────────────────────────────────────────────────────────────

with tab_roster:
    try:
        from agents.lifecycle import ROSTER
        snap = ROSTER.snapshot()
    except Exception as e:
        st.error(f"Lifecycle module failed: {e}")
        snap = {"live": {}, "dead_recent": [], "dead_total": 0}

    c1, c2, c3 = st.columns(3)
    c1.metric("Live agents", len(snap["live"]))
    c2.metric("Dead total", snap.get("dead_total", 0))
    c3.metric("Recent kills (last 20)", len(snap.get("dead_recent", [])))

    st.subheader("Live cohort")
    if not snap["live"]:
        st.caption("_no live agents yet — run a debate first_")
    else:
        import pandas as pd
        df = pd.DataFrame([
            {
                "spec":    a["spec_key"],
                "cohort":  a["cohort_id"],
                "turns":   a["n_turns"],
                "ewma":    round(a["quality_ewma"], 3),
                "bad_streak": a["bad_streak"],
                "lifespan_s": round(time.time() - a["spawn_at"], 1),
                "cum_reward": round(a["cumulative_reward"], 2),
            }
            for a in snap["live"].values()
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Cemetery (recent)")
    if not snap.get("dead_recent"):
        st.caption("_no kills yet — feedback below to start scoring agents_")
    else:
        import pandas as pd
        df = pd.DataFrame([
            {
                "spec":    a["spec_key"],
                "cohort":  a["cohort_id"],
                "lived_turns": a["n_turns"],
                "ewma_at_death": round(a["quality_ewma"], 3),
                "cause": a.get("death_cause") or "?",
                "lifespan_s": round((a.get("died_at") or 0) - a["spawn_at"], 1),
            }
            for a in reversed(snap["dead_recent"])
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)


# ── ② Recent turns + feedback ─────────────────────────────────────────────

@st.cache_data(ttl=5)
def _load_recent_turns(n: int = 25) -> list[dict]:
    if not TURNS_LOG.exists():
        return []
    out = []
    with TURNS_LOG.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out[-n:][::-1]   # most recent first


with tab_turns:
    n_show = st.slider("Show last N turns", 5, 50, 15, key="n_turns_slider")
    turns = _load_recent_turns(n_show)

    if not turns:
        st.info(
            "No turns logged yet. Run a debate via the agents app — "
            "every turn will be recorded to `data/sessions/turns.jsonl`."
        )
    for t in turns:
        with st.container(border=True):
            head_cols = st.columns([3, 1, 1])
            head_cols[0].markdown(
                f"**{t['spec_key']}** · turn `{t['turn_id']}` · "
                f"_{t.get('n_arxiv', 0)}arxiv / {t.get('n_wiki', 0)}wiki / "
                f"{t.get('n_entities', 0)}entities_"
            )
            head_cols[1].caption(
                time.strftime("%H:%M:%S", time.localtime(t["ts"]))
            )
            head_cols[2].caption(f"sess `{t.get('session_id') or '–'}`")

            with st.expander("prompt + response"):
                st.markdown(f"**Prompt:** {t.get('prompt', '')[:600]}")
                st.markdown(
                    f"**Response:**\n\n```\n{t.get('response', '')[:2000]}\n```"
                )

            comment_key = f"comment_{t['turn_id']}"
            comment = st.text_input(
                "Comment (optional)", key=comment_key,
                placeholder="why was this good/bad?",
            )

            btns = st.columns(4)
            if btns[0].button("👍 +1", key=f"up_{t['turn_id']}"):
                _apply_fb(t["turn_id"], +1.0, comment)
                st.rerun()
            if btns[1].button("👎 −1", key=f"dn_{t['turn_id']}"):
                _apply_fb(t["turn_id"], -1.0, comment)
                st.rerun()
            if btns[2].button("🤷 0", key=f"nt_{t['turn_id']}"):
                _apply_fb(t["turn_id"], 0.0, comment)
                st.rerun()
            btns[3].caption("score → graph + EWMA")


def _apply_fb(turn_id: str, score: float, comment: str) -> None:
    try:
        from agents.feedback import record_feedback
        r = record_feedback(turn_id, score, comment or "")
        if r.get("error"):
            st.error(r["error"])
            return
        if r.get("killed"):
            st.warning(f"💀 agent killed — {r['reason']}")
        else:
            st.success(
                f"applied score={score:+.0f} · ewma={r['ewma']:.2f} · "
                f"edges_updated={r['edges_updated']}"
            )
    except Exception as e:
        st.error(f"feedback failed: {e}")


# ── ③ Graph weights ───────────────────────────────────────────────────────

with tab_weights:
    st.caption(
        "Top edges by current `weight` property. Higher = brain considers "
        "this connection more salient (positive feedback path)."
    )
    limit = st.slider("Top N edges", 10, 200, 40, key="weights_topn")

    @st.cache_data(ttl=5)
    def _top_edges(limit: int) -> dict:
        try:
            from graph.temporal_graph import _get_driver, _run
        except ImportError:
            return {"error": "graph module missing", "rows": []}
        try:
            drv = _get_driver()
        except Exception as e:
            return {"error": f"falkordb: {e}", "rows": []}

        cypher = f"""
        MATCH (s)-[r:RELATES_TO]->(o)
        WHERE r.weight IS NOT NULL
        RETURN s.name AS source, r.fact AS fact, o.name AS target,
               r.weight AS weight, r.last_credit_at AS last_credit_at
        ORDER BY r.weight DESC
        LIMIT {int(limit)}
        """
        try:
            rs, _, _ = _run(drv.execute_query(cypher))
            return {"error": None, "rows": [dict(x) for x in rs]}
        except Exception as e:
            return {"error": f"{type(e).__name__}: {e}", "rows": []}

    res = _top_edges(limit)
    if res.get("error"):
        st.warning(res["error"])
        st.info(
            "No edges have a `weight` yet — weights are added the first time "
            "an entity is credited (positive or negative). Run a debate, "
            "give feedback, then refresh."
        )
    else:
        if not res["rows"]:
            st.caption("_no weighted edges yet — give feedback to seed weights_")
        else:
            import pandas as pd
            df = pd.DataFrame([
                {
                    "weight": round(float(r.get("weight") or 1.0), 3),
                    "source": (r.get("source") or "")[:30],
                    "fact":   (r.get("fact") or "")[:60],
                    "target": (r.get("target") or "")[:30],
                    "last_credit_at": r.get("last_credit_at"),
                }
                for r in res["rows"]
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
