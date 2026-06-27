"""
Orchestrator — runs the multi-specialist debate loop.

Public surface:
  AgentTurn          # one agent's contribution
  DebateHistory      # ordered list of turns
  run_debate(...)    # full debate + wiki processing
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Callable

from .specialists import Specialist, SPECIALISTS
from .wiki_io import WikiScratchpad, WikiProposal, parse_wiki_proposal
from .backend import get_backend


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class AgentTurn:
    agent: str
    round: int
    raw_text: str
    citations: list[str] = field(default_factory=list)
    wiki_proposal: WikiProposal | None = None
    confidence: str = "medium"   # low | medium | high
    tool_calls: list[dict] = field(default_factory=list)   # executed tool results
    turn_id: str = ""            # uuid — identifier for RL feedback lookup
    spec_key: str = ""           # short key (aero/mech/cs) for lifecycle tracking
    cohort_id: str = ""          # which cohort of the specialist served this turn


@dataclass
class DebateHistory:
    turns: list[AgentTurn] = field(default_factory=list)
    problem: str = ""

    def append(self, turn: AgentTurn):
        self.turns.append(turn)

    def render_for_prompt(self, max_turns: int = 8) -> str:
        """Format recent turns for an agent's context window."""
        recent = self.turns[-max_turns:]
        if not recent:
            return "(no prior turns)"
        lines = []
        for t in recent:
            cites = (" " + " ".join(t.citations)) if t.citations else ""
            lines.append(f"[round {t.round} · {t.agent}]{cites}\n{t.raw_text.strip()}")
            if t.tool_calls:
                tool_lines = "\n  ".join(tc["short"] for tc in t.tool_calls)
                lines.append(f"  TOOL RESULTS:\n  {tool_lines}")
            lines.append("")
        return "\n".join(lines)


# ── Anthropic client (lazy) ──────────────────────────────────────────────────

_client = None
def _get_client():
    global _client
    if _client is None:
        import anthropic
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def _call_local_llm(system: str, user: str, max_tokens: int = 1500,
                    retries: int = 3) -> str:
    """Call a local OpenAI-compatible chat endpoint.

    Works with any server exposing POST ${LOCAL_LLM_BASE}/chat/completions:
      - Ollama          (LOCAL_LLM_BASE=http://localhost:11434/v1)
      - llama-cpp-python (LOCAL_LLM_BASE=http://localhost:8000/v1)
      - llama.cpp llama-server (its own --port)

    Env vars:
      LOCAL_LLM_BASE   base URL incl. /v1 (no trailing /chat/completions)
      LOCAL_LLM_MODEL  model name the server knows (default "gemma")
      LOCAL_LLM_KEY    optional bearer token (local servers usually need none)
    """
    import requests

    base = os.environ.get("LOCAL_LLM_BASE", "").rstrip("/")
    if not base:
        raise RuntimeError("LOCAL_LLM_BASE not set")
    model = os.environ.get("LOCAL_LLM_MODEL", "gemma")
    url = f"{base}/chat/completions"

    headers = {"Content-Type": "application/json"}
    key = os.environ.get("LOCAL_LLM_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"

    # Reasoning models (e.g. the gemma-4 coder) spend tokens "thinking" before
    # emitting the answer, and llama.cpp puts that thinking in a separate
    # `reasoning_content` field. With a tight max_tokens the budget is consumed
    # by reasoning and `content` comes back empty/truncated. Give generous
    # headroom — the cap is harmless for short answers (the model stops at
    # finish_reason=stop) and prevents truncation on big JSON generations.
    # Capped to stay within the endpoint context window (8192).
    eff_max = min(5000, max(max_tokens, 4000))
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": eff_max,
        "temperature": 0.3,
    }

    # A scale-to-zero endpoint (HF Inference Endpoint) returns 502/503/504
    # while it cold-starts (reloads the model, ~30-60s). Retry those patiently
    # so the first request after idle succeeds instead of surfacing a 503.
    retries = max(retries, 6)
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=headers, json=body, timeout=300)
            if r.status_code in (502, 503, 504):
                last_err = RuntimeError(f"endpoint warming up ({r.status_code})")
                time.sleep(min(30, 10 * (attempt + 1)))   # 10,20,30,30,… s
                continue
            r.raise_for_status()
            payload = r.json()
            msg = payload["choices"][0]["message"]
            content = (msg.get("content") or "").strip()
            # Fallback: if the model emitted only reasoning (ran out of budget
            # mid-answer), use that so callers get something parseable.
            if not content:
                content = (msg.get("reasoning_content") or "").strip()
            return content
        except (requests.ConnectionError, requests.Timeout) as e:
            last_err = e
            time.sleep(5 * (attempt + 1))
            continue
    raise RuntimeError(
        f"Local LLM call to {url} failed after {retries} retries: {last_err}"
    )


def _call_claude(model: str, system: str, user: str, max_tokens: int = 1500,
                 retries: int = 5) -> str:
    """Robust generation call with retries on rate limits.

    Global LLM switch: if LLM_BACKEND=local or LOCAL_LLM_BASE is set, route
    every generation through the local OpenAI-compatible endpoint first. On
    local failure, fall back to Anthropic if ANTHROPIC_API_KEY is present;
    otherwise raise a clear error. When local is not configured, the original
    Anthropic path runs unchanged.
    """
    use_local = (
        os.environ.get("LLM_BACKEND") == "local"
        or bool(os.environ.get("LOCAL_LLM_BASE"))
    )
    if use_local:
        try:
            return _call_local_llm(system, user, max_tokens=max_tokens)
        except Exception as local_err:
            if not os.environ.get("ANTHROPIC_API_KEY"):
                raise RuntimeError(
                    "Local LLM failed and no Anthropic fallback available. "
                    "Set LOCAL_LLM_BASE (e.g. http://localhost:11434/v1) and "
                    "LOCAL_LLM_MODEL for local serving, or set "
                    f"ANTHROPIC_API_KEY to fall back to Claude. Cause: {local_err}"
                ) from local_err
            # fall through to the Anthropic path below

    client = _get_client()
    for attempt in range(retries):
        try:
            msg = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return msg.content[0].text
        except Exception as e:
            err = str(e)
            if "rate_limit" in err or "429" in err or "overloaded" in err:
                wait = 10 * (attempt + 1)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"Claude call failed after {retries} retries")


# ── Citation extraction ──────────────────────────────────────────────────────

import re
CITATION_PATTERNS = [
    re.compile(r"\[arxiv/[a-z_-]+/[\w.-]+(?:#\d+)?\]"),
    re.compile(r"\[\[wiki/[\w/_.-]+\]\]"),
    re.compile(r"\[tool/[\w_]+\]"),
]


def _extract_citations(text: str) -> list[str]:
    out = []
    for pat in CITATION_PATTERNS:
        out.extend(pat.findall(text))
    return out


def _extract_confidence(text: str) -> str:
    m = re.search(r"confidence[:\s]*\b(low|medium|high)\b", text, re.IGNORECASE)
    return (m.group(1).lower() if m else "medium")


# ── Tool call extraction & execution ─────────────────────────────────────────

import json as _json
TOOL_CALL_RE = re.compile(
    r"<tool_call>(.*?)</tool_call>", re.DOTALL | re.IGNORECASE
)


def _extract_and_run_tools(agent_text: str) -> list[dict]:
    """Find every <tool_call>name: ..., args: {...}</tool_call> block and execute it."""
    try:
        from tools.base import call_tool
    except ImportError:
        return []
    results = []
    for match in TOOL_CALL_RE.finditer(agent_text):
        body = match.group(1).strip()
        # Parse name + args
        name_match = re.search(r"name:\s*(\S+)", body)
        args_match = re.search(r"args:\s*(\{.*?\})", body, re.DOTALL)
        if not name_match:
            continue
        name = name_match.group(1).strip()
        args = {}
        if args_match:
            try:
                args = _json.loads(args_match.group(1))
            except _json.JSONDecodeError:
                pass
        result = call_tool(name, **args)
        results.append({
            "name": result.name,
            "inputs": result.inputs,
            "output": result.output,
            "units": result.units,
            "error": result.error,
            "short": result.short(),
        })
    return results


# ── Single agent turn ────────────────────────────────────────────────────────

def _agent_take_turn(spec: Specialist, problem: str, history: DebateHistory,
                     wiki_state: WikiScratchpad, round_idx: int) -> AgentTurn:
    # 1. Retrieve evidence
    query = problem + " " + history.render_for_prompt(max_turns=3)
    rag_chunks = spec.retrieve(query, top_k=5)
    wiki_pages = wiki_state.read_only_view(query, spec.wiki_topics, max_pages=3)

    # 2. Build user prompt
    rag_block = "\n\n".join(
        f"[arxiv/{c.get('category','?')}/{c.get('paper_id','?')}#{c['source'].split('#')[-1] if '#' in c['source'] else 0}]\n"
        f"{c['text'][:600]}"
        for c in rag_chunks
    ) or "(no domain RAG matches)"

    wiki_block = "\n\n".join(
        f"[[wiki/{p['name']}]]\n{p['content'][:800]}"
        for p in wiki_pages
    ) or "(no relevant wiki pages)"

    history_block = history.render_for_prompt()

    user = f"""\
PROBLEM:
{problem}

--- DEBATE SO FAR ---
{history_block}

--- YOUR DOMAIN'S ARXIV EVIDENCE (top retrieved chunks) ---
{rag_block}

--- RELEVANT WIKI PAGES ---
{wiki_block}

--- YOUR TURN ({spec.name}, round {round_idx}) ---
Speak now. Cite at least one piece of evidence. Optionally propose a wiki
edit. End with your confidence level (low/medium/high)."""

    # 3. Call model (via pluggable backend — Claude / HF / etc)
    backend = get_backend(spec.base_model)
    raw = backend.complete(
        system=spec.system_prompt(),
        user=user,
        max_tokens=1200,
    )

    # 4. Parse structured pieces
    citations = _extract_citations(raw)
    confidence = _extract_confidence(raw)
    proposal = parse_wiki_proposal(raw, spec.name)
    tool_results = _extract_and_run_tools(raw)

    # 5. Add tool-call citations
    for tr in tool_results:
        if not tr["error"]:
            citations.append(f"[tool/{tr['name']}]")

    # 6. Pick spec_key (aero/mech/cs) — best-effort guess from name
    spec_key = spec._catalog_key() or spec.name.split("-")[0][:4]

    # 7. RL hook — register turn for credit assignment + lifecycle scoring
    import uuid as _uuid
    turn_id = str(_uuid.uuid4())[:12]
    cohort_id = ""
    try:
        from .feedback import record_response
        from .lifecycle import ROSTER
        record_response(turn_id, spec_key, problem, raw)
        cohort_id = ROSTER.get(spec_key).cohort_id
    except Exception:
        # RL system optional — debate must run even if it's broken
        pass

    turn_obj = AgentTurn(
        agent=spec.name,
        round=round_idx,
        raw_text=raw,
        citations=citations,
        wiki_proposal=proposal,
        confidence=confidence,
        tool_calls=tool_results,
        turn_id=turn_id,
        spec_key=spec_key,
        cohort_id=cohort_id,
    )

    # 8. Auto-judge — apply feedback automatically when no human is in the
    # loop. Off by default (RL_AUTO_JUDGE=heuristic|llm|hybrid to enable).
    if os.environ.get("RL_AUTO_JUDGE"):
        try:
            from .judge import judge_and_record
            judge_and_record(
                turn_obj, problem,
                prior_turns=history.render_for_prompt(max_turns=4),
            )
        except Exception:
            pass

    return turn_obj


# ── Debate loop ──────────────────────────────────────────────────────────────

def run_debate(
    problem: str,
    specialists: list[Specialist] | None = None,
    rounds: int = 3,
    on_turn: Callable[[AgentTurn], None] | None = None,
    session_id: str | None = None,
) -> tuple[DebateHistory, WikiScratchpad]:
    """Run a multi-agent debate over `rounds` rounds.

    Args:
      problem: the user's problem statement
      specialists: list of Specialist objects (defaults to all three)
      rounds: number of full rotations (each round, every agent speaks once)
      on_turn: optional callback (e.g. for live UI updates)
      session_id: optional session id for RL logs; auto-generated if None

    Returns:
      (DebateHistory, WikiScratchpad) — both fully populated.
    """
    if specialists is None:
        specialists = list(SPECIALISTS.values())

    history = DebateHistory(problem=problem)
    wiki = WikiScratchpad()

    # RL — register the user's prompt for Hebbian boost (best-effort)
    try:
        from .feedback import register_prompt, new_session_id
        if session_id is None:
            session_id = new_session_id()
        register_prompt(problem, session_id=session_id)
    except Exception:
        pass

    # Filter out specialists whose live agent has been killed (cohort respawns
    # automatically on first .get(), but this gives the orchestrator a chance
    # to skip a flatlined domain mid-debate if the user prefers).
    skip_dead = os.environ.get("RL_SKIP_DEAD_AGENTS", "0") == "1"
    if skip_dead:
        try:
            from .lifecycle import ROSTER
            specialists = [
                s for s in specialists
                if ROSTER.get(s._catalog_key() or s.name).alive
            ]
        except Exception:
            pass

    for round_idx in range(1, rounds + 1):
        for spec in specialists:
            turn = _agent_take_turn(spec, problem, history, wiki, round_idx)
            history.append(turn)
            if turn.wiki_proposal:
                wiki.add_proposal(turn.wiki_proposal)
            if on_turn:
                on_turn(turn)

    # Process all proposals at the end
    wiki.process_proposals()

    return history, wiki
