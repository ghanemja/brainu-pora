"""
Agent lifecycle — spawn, score, kill.

Each Specialist has a *cohort* of agent-instances over time. An "agent"
here is one (specialist_key, cohort_id) pair with:

  - spawn_at        : when this cohort instance came online
  - lifespan        : turns served (or seconds alive)
  - quality_ewma    : exponentially-weighted moving avg of feedback rewards
  - bad_streak      : consecutive low-feedback turns
  - died_at, cause  : termination metadata

When an agent dies, its full citation-history gets a final negative-replay
penalty applied to the graph (see `negative_replay`). Then a fresh cohort
spawns the next time that specialist is needed.

Persistence:
  data/sessions/roster.json  — current live roster + per-agent stats
  data/sessions/cemetery.jsonl — append-only log of every kill (for replay)

Public surface:
  ROSTER                      # singleton AgentRoster
  AgentRoster.get(spec_key)   # → live cohort (spawning if absent)
  AgentRoster.record_turn(...) # log a turn the agent took
  AgentRoster.score_turn(...)  # apply reward, evaluate kill threshold
  AgentRoster.snapshot()       # serializable view for UI
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
SESSIONS_DIR = PROJECT_ROOT / "data" / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

ROSTER_PATH = SESSIONS_DIR / "roster.json"
CEMETERY_PATH = SESSIONS_DIR / "cemetery.jsonl"

# ── Tunables (env-overridable) ─────────────────────────────────────────────
import os

EWMA_ALPHA       = float(os.environ.get("RL_EWMA_ALPHA", 0.30))
KILL_THRESHOLD   = float(os.environ.get("RL_KILL_THRESHOLD", 0.30))   # EWMA cutoff
BAD_STREAK_KILL  = int(os.environ.get("RL_BAD_STREAK_KILL", 5))       # turns
NEG_REPLAY_DELTA = float(os.environ.get("RL_NEG_REPLAY_DELTA", -0.20))
MIN_TURNS_BEFORE_KILL = int(os.environ.get("RL_MIN_TURNS_BEFORE_KILL", 8))


# ── Agent record ───────────────────────────────────────────────────────────

@dataclass
class Agent:
    spec_key: str                       # "aero" | "mech" | "cs"
    cohort_id: str                      # uuid4 for this incarnation
    spawn_at: float                     # unix seconds
    quality_ewma: float = 0.5           # neutral start (not 0!)
    n_turns: int = 0
    bad_streak: int = 0
    cumulative_reward: float = 0.0
    citation_history: list[dict] = field(default_factory=list)
    # death fields (filled when killed)
    died_at: float | None = None
    death_cause: str | None = None

    @property
    def lifespan_s(self) -> float:
        end = self.died_at if self.died_at else time.time()
        return end - self.spawn_at

    @property
    def alive(self) -> bool:
        return self.died_at is None

    def to_dict(self) -> dict:
        return asdict(self)


# ── Roster ─────────────────────────────────────────────────────────────────

class AgentRoster:
    """Thread-safe singleton tracking all live & dead agents."""

    _instance: "AgentRoster | None" = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                inst = super().__new__(cls)
                inst._lock = threading.RLock()
                inst.live: dict[str, Agent] = {}      # spec_key → live Agent
                inst.dead: list[Agent] = []           # full cemetery in mem
                inst._load()
                cls._instance = inst
            return cls._instance

    # ── Persistence ────────────────────────────────────────────────────

    def _load(self) -> None:
        if ROSTER_PATH.exists():
            try:
                blob = json.loads(ROSTER_PATH.read_text())
                for spec_key, d in blob.get("live", {}).items():
                    self.live[spec_key] = Agent(**d)
            except Exception:
                pass
        if CEMETERY_PATH.exists():
            try:
                for line in CEMETERY_PATH.read_text().splitlines():
                    line = line.strip()
                    if line:
                        self.dead.append(Agent(**json.loads(line)))
            except Exception:
                pass

    def _save_live(self) -> None:
        blob = {"live": {k: a.to_dict() for k, a in self.live.items()}}
        ROSTER_PATH.write_text(json.dumps(blob, indent=2, default=str))

    def _append_grave(self, agent: Agent) -> None:
        with CEMETERY_PATH.open("a") as f:
            f.write(json.dumps(agent.to_dict(), default=str) + "\n")

    # ── Spawn / get ────────────────────────────────────────────────────

    def get(self, spec_key: str) -> Agent:
        """Return the live agent for `spec_key`, spawning if absent or dead."""
        with self._lock:
            agent = self.live.get(spec_key)
            if agent is None or not agent.alive:
                agent = self._spawn(spec_key)
            return agent

    def _spawn(self, spec_key: str) -> Agent:
        agent = Agent(
            spec_key=spec_key,
            cohort_id=str(uuid.uuid4())[:8],
            spawn_at=time.time(),
        )
        self.live[spec_key] = agent
        self._save_live()
        return agent

    # ── Per-turn lifecycle ────────────────────────────────────────────

    def record_turn(self, spec_key: str, turn_id: str,
                    citations: list[tuple[str, str]]) -> None:
        """Log that an agent took a turn — citations preserved for credit assignment."""
        with self._lock:
            agent = self.get(spec_key)
            agent.n_turns += 1
            agent.citation_history.append({
                "turn_id": turn_id,
                "ts": time.time(),
                "citations": citations,
            })
            # Cap history to last 50 turns to bound memory
            if len(agent.citation_history) > 50:
                agent.citation_history = agent.citation_history[-50:]
            self._save_live()

    def score_turn(self, spec_key: str, reward: float) -> dict:
        """Apply a reward to this agent's EWMA and check kill conditions.

        Returns {killed: bool, reason: str, ewma: float, lifespan_turns: int}.
        """
        with self._lock:
            agent = self.get(spec_key)
            r = max(0.0, min(1.0, reward))   # clip to [0,1]
            agent.quality_ewma = (
                EWMA_ALPHA * r + (1 - EWMA_ALPHA) * agent.quality_ewma
            )
            agent.cumulative_reward += reward

            if r < 0.4:
                agent.bad_streak += 1
            else:
                agent.bad_streak = 0

            killed = False
            reason = ""
            if (
                agent.n_turns >= MIN_TURNS_BEFORE_KILL
                and agent.quality_ewma < KILL_THRESHOLD
            ):
                killed = True
                reason = f"EWMA {agent.quality_ewma:.2f} < {KILL_THRESHOLD}"
            elif agent.bad_streak >= BAD_STREAK_KILL:
                killed = True
                reason = f"bad streak = {agent.bad_streak}"

            if killed:
                self._kill(agent, reason)

            self._save_live()
            return {
                "killed": killed,
                "reason": reason,
                "ewma": agent.quality_ewma,
                "bad_streak": agent.bad_streak,
                "lifespan_turns": agent.n_turns,
                "lifespan_s": agent.lifespan_s,
            }

    # ── Kill ───────────────────────────────────────────────────────────

    def _kill(self, agent: Agent, cause: str) -> None:
        agent.died_at = time.time()
        agent.death_cause = cause
        self.dead.append(agent)
        # Fire negative-replay against the graph (best-effort, non-blocking)
        try:
            self._negative_replay(agent)
        except Exception:
            pass
        self._append_grave(agent)
        # Remove from live; next get() will respawn
        if self.live.get(agent.spec_key) is agent:
            del self.live[agent.spec_key]

    def _negative_replay(self, agent: Agent) -> None:
        """Penalize every edge the dying agent ever cited.

        Each turn's citations get a delta that decays the further back in
        history they are: most recent turn = full NEG_REPLAY_DELTA,
        oldest turn in the buffer = ~10% of that.
        """
        try:
            from graph.weight_update import apply_credit
        except ImportError:
            return
        history = agent.citation_history
        n = len(history)
        if n == 0:
            return
        # Linear decay: most recent turn gets weight 1.0, oldest 0.1
        for i, rec in enumerate(history):
            recency = 0.1 + 0.9 * (i / max(1, n - 1))
            delta = NEG_REPLAY_DELTA * recency
            try:
                apply_credit(rec.get("citations", []), delta)
            except Exception:
                continue

    # ── Snapshot for UI ────────────────────────────────────────────────

    def snapshot(self) -> dict:
        """Serializable view: live agents + recent cemetery entries."""
        with self._lock:
            return {
                "live": {k: a.to_dict() for k, a in self.live.items()},
                "dead_recent": [a.to_dict() for a in self.dead[-20:]],
                "dead_total": len(self.dead),
                "thresholds": {
                    "ewma_alpha": EWMA_ALPHA,
                    "kill_threshold": KILL_THRESHOLD,
                    "bad_streak_kill": BAD_STREAK_KILL,
                    "min_turns_before_kill": MIN_TURNS_BEFORE_KILL,
                    "neg_replay_delta": NEG_REPLAY_DELTA,
                },
            }


# Singleton
ROSTER = AgentRoster()
