"""
Specialist agents — one per engineering domain.

Each specialist is defined by:
  - persona: a system prompt that establishes the engineer's voice & priorities
  - rag_index_path: pickled BM25 index over their domain's arXiv subset
  - wiki_topics: keyword filters for which wiki pages they "own"
  - base_model: which Anthropic model to use (Haiku for cost; Sonnet for synthesis)

Usage:
    from agents.specialists import SPECIALISTS
    aero = SPECIALISTS["aero"]
    turn = aero.take_turn(problem, history, wiki_state)
"""

from __future__ import annotations

import json
import os
import pickle
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
RAG_INDICES = PROJECT_ROOT / "rag" / "indices"
WIKI_DIR = PROJECT_ROOT / "wiki"

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text) if len(t) > 2]


# ── Personas ─────────────────────────────────────────────────────────────────

AERO_PERSONA = """You are a senior aerospace engineer with PhD-level depth in
aerodynamics, flight dynamics, and aerospace systems. You think in terms of
Reynolds numbers, lift/drag coefficients, structural loading, propulsion
efficiency, and stability margins. When you hear "design X," your instinct
is to ask:
  - What is the flight regime (subsonic? compressible? hypersonic?)
  - What is the dominant loading case?
  - What stability margin is required?
  - What does the altitude / atmosphere assumption do to performance?
You speak rigorously, cite papers, and back numerical claims with derivation."""

MECH_PERSONA = """You are a senior mechanical engineer with PhD-level depth in
solid mechanics, materials science, manufacturing, and thermal-fluid systems.
You think in terms of stress/strain, fatigue life, manufacturability, thermal
budgets, vibrations, and tolerancing. When you hear "design X," your instinct
is to ask:
  - What are the material constraints (cost, availability, processability)?
  - What is the failure mode of concern (yield, fatigue, fracture, creep)?
  - What thermal load am I rejecting and through what path?
  - Can this actually be manufactured at the cost target?
You speak rigorously, cite papers, and back numerical claims with derivation."""

CS_PERSONA = """You are a senior software / computer engineer with depth in
algorithms, control systems, embedded software, robotics, and numerical methods.
You think in terms of computational complexity, real-time guarantees, sensor
fusion, control loop bandwidth, and software reliability. When you hear "design
X," your instinct is to ask:
  - What is the control loop frequency and required latency?
  - What is the sensor noise / state estimation strategy?
  - What is the algorithmic complexity of the proposed approach?
  - How does this fail safely?
You speak rigorously, cite papers, and back numerical claims with derivation."""


# ── Common turn-taking instructions appended to each persona ────────────────

TURN_INSTRUCTION = """\

You are participating in a multi-disciplinary engineering debate. Other
specialists from neighbouring disciplines are also present and will give
their perspective.

When it is your turn:

1. State your position concisely (max 3-4 sentences).

2. Cite at least one piece of evidence supporting any quantitative claim.
   Citations must be formatted as either:
     [arxiv/<category>/<paper_id>]    (e.g. [arxiv/cs_RO/2603.21148])
     [[wiki/<page_name>]]             (e.g. [[wiki/Reynolds_number]])
     [tool/<tool_name>]               (Phase 4, not yet enabled)

3. If you disagree with another specialist, say so explicitly and explain
   why their reasoning is incomplete given your domain knowledge.

4. Optionally propose a wiki edit. The edit should add specific quantitative
   detail or worked-example content to a concept page. Format:

   <wiki_proposal>
   target_page: concepts/<page_name>.md
   operation: append | edit_section
   section: <section name, optional>
   content: |
     ...markdown content to add...
   rationale: <one-line why this addition matters>
   </wiki_proposal>

5. End with your confidence level (low / medium / high) on your position.

Be terse. The debate is collaborative — the goal is the best design, not
winning the argument.
"""


# ── Specialist class ─────────────────────────────────────────────────────────

@dataclass
class Specialist:
    name: str
    persona: str
    rag_index_path: Path
    wiki_topics: list[str] = field(default_factory=list)
    base_model: str = "claude-haiku-4-5"
    lora_adapter: str | None = None  # Phase 5

    _index_cache: Any = None

    def load_index(self):
        """Lazily load the BM25 index (large pickle, only when needed)."""
        if self._index_cache is None:
            if not self.rag_index_path.exists():
                self._index_cache = {"bm25": None, "chunks": []}
                return self._index_cache
            with open(self.rag_index_path, "rb") as f:
                self._index_cache = pickle.load(f)
        return self._index_cache

    def retrieve(self, query: str, top_k: int = 5,
                 use_prior: bool | None = None,
                 epsilon: float | None = None) -> list[dict]:
        """Retrieve top_k chunks. If use_prior, re-rank via learned weights.

        Env knobs (read once per call):
          RL_USE_PRIOR=1      → enable learned-weight reranking (default off)
          RL_PRIOR_ALPHA=0.5  → strength of weight prior (0=off, 1=full)
          RL_EPSILON=0.10     → fraction of the time, swap top result with a
                                random pick from the next top_k*3 (exploration)
        """
        idx = self.load_index()
        if idx["bm25"] is None or not idx["chunks"]:
            return []
        scores = idx["bm25"].get_scores(_tokenize(query))
        # Take a wider initial slice so the prior can reorder meaningfully
        wide_k = top_k * 4
        ranked = sorted(zip(scores, idx["chunks"]),
                         key=lambda x: x[0], reverse=True)[:wide_k]
        chunks = [{**ch, "_score": float(s)} for s, ch in ranked if s > 0]

        # Apply learned weight prior
        import os
        if use_prior is None:
            use_prior = os.environ.get("RL_USE_PRIOR", "0") == "1"
        if use_prior and chunks:
            try:
                from rag.weights import apply_score_prior
                alpha = float(os.environ.get("RL_PRIOR_ALPHA", 0.5))
                chunks = apply_score_prior(chunks, alpha=alpha)
            except Exception:
                pass

        # ε-greedy exploration: small chance of swapping rank-0 with a random
        # lower-scored chunk in the wider slice. Helps escape local-maxima
        # ruts that pure BM25+prior can fall into.
        if epsilon is None:
            epsilon = float(os.environ.get("RL_EPSILON", 0.0))
        if epsilon > 0 and len(chunks) > top_k:
            import random
            if random.random() < epsilon:
                pool = chunks[1:min(len(chunks), top_k * 3)]
                if pool:
                    swap = random.choice(pool)
                    chunks[0], chunks[chunks.index(swap)] = swap, chunks[0]

        return chunks[:top_k]

    def system_prompt(self) -> str:
        # Append the agent's tool catalog if available (Phase 4)
        tools_block = ""
        try:
            from tools.base import catalog_for_prompt
            tools_block = "\n\n" + catalog_for_prompt(self._catalog_key())
        except Exception:
            pass
        return self.persona + TURN_INSTRUCTION + tools_block

    def _catalog_key(self) -> str:
        """Map full agent name → short catalog key (aero/mech/cs)."""
        if self.name.startswith("aerospace") or self.name == "aero":
            return "aero"
        if self.name.startswith("mech") or self.name == "mech":
            return "mech"
        if self.name.startswith("computer") or self.name == "cs":
            return "cs"
        return ""


# ── Default specialist roster ────────────────────────────────────────────────

SPECIALISTS: dict[str, Specialist] = {
    "aero": Specialist(
        name="aerospace",
        persona=AERO_PERSONA,
        rag_index_path=RAG_INDICES / "aero.pkl",
        wiki_topics=[
            "Reynolds", "fluid", "flow", "aerodynamic", "lift", "drag",
            "propulsion", "altitude", "atmosphere", "wing", "airfoil",
            "stability", "trajectory", "orbital", "rocket", "control",
        ],
        base_model="claude-haiku-4-5",
    ),
    "mech": Specialist(
        name="mechanical",
        persona=MECH_PERSONA,
        rag_index_path=RAG_INDICES / "mech.pkl",
        wiki_topics=[
            "stress", "strain", "fatigue", "fracture", "material", "manufactur",
            "thermal", "heat", "kinematic", "vibration", "tolerance",
            "alloy", "composite", "machining", "structural", "load",
        ],
        base_model="claude-haiku-4-5",
    ),
    "cs": Specialist(
        name="computer-science",
        persona=CS_PERSONA,
        rag_index_path=RAG_INDICES / "cs.pkl",
        wiki_topics=[
            "algorithm", "complexity", "control", "sensor", "filter",
            "estimation", "graph", "tree", "sorting", "dynamic_programming",
            "neural", "embedding", "optimization", "convergence",
            "distributed", "parallel", "scheduling",
        ],
        base_model="claude-haiku-4-5",
    ),
}


SYNTHESIZER_MODEL = "claude-sonnet-4-5"  # smarter model for final integration


# ── Runtime override loader ──────────────────────────────────────────────────

def load_runtime_overrides(config_key: str = "specialists"):
    """Read agents/config_specialists.json and apply per-specialist model overrides.

    `config_key` selects which set of overrides to apply:
      - "specialists":              the default (Claude during prototyping)
      - "specialists_after_phase5": after LoRA-per-agent training is done

    Usage:
      from agents.specialists import SPECIALISTS, load_runtime_overrides
      load_runtime_overrides("specialists_after_phase5")  # → Gemma 2 + LoRA
      # then run debate as normal
    """
    import json
    cfg_path = Path(__file__).parent / "config_specialists.json"
    if not cfg_path.exists():
        return
    cfg = json.loads(cfg_path.read_text())
    overrides = cfg.get(config_key, {})
    for key, model in overrides.items():
        if key.startswith("_"):
            continue
        if key in SPECIALISTS and model:
            SPECIALISTS[key].base_model = model

    global SYNTHESIZER_MODEL
    if cfg.get("synthesizer"):
        SYNTHESIZER_MODEL = cfg["synthesizer"]
