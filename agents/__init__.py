"""Multi-specialist engineering agent system.

See docs/ARCHITECTURE.md for the full system description.
"""

from .specialists import Specialist, SPECIALISTS
from .orchestrator import run_debate, AgentTurn, DebateHistory
from .synthesizer import synthesize, FinalDesign
from .wiki_io import WikiScratchpad, WikiProposal

__all__ = [
    "Specialist", "SPECIALISTS",
    "run_debate", "AgentTurn", "DebateHistory",
    "synthesize", "FinalDesign",
    "WikiScratchpad", "WikiProposal",
]
