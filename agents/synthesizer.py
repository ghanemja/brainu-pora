"""
Synthesizer agent — reads the full debate, produces the final design proposal.

The synthesizer uses a smarter model than the individual specialists
(Claude Sonnet vs Haiku) because integrating multiple perspectives is the
hardest cognitive step in the pipeline.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .specialists import SYNTHESIZER_MODEL
from .orchestrator import DebateHistory, _call_claude
from .wiki_io import WikiScratchpad


@dataclass
class FinalDesign:
    proposal: str
    citations: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    raw_text: str = ""


SYNTHESIZER_SYSTEM = """You are the project lead synthesizing a multi-disciplinary
engineering debate into a final design proposal.

Your job is NOT to pick a winner. Your job is to integrate the perspectives:

1. Read the entire debate.
2. Identify the points of consensus across specialists.
3. Identify the genuine disagreements (where domain experts differ on technical
   grounds, not stylistic ones) and surface them as open questions.
4. Produce a concrete design proposal that respects all domain constraints
   identified by the specialists.
5. Cite the strongest pieces of evidence each specialist brought in.

Output structure:

# Final design proposal

## Summary
<2-3 sentence elevator description>

## Design decisions
<numbered list of concrete decisions with citations>

## Multi-disciplinary trade-offs
<which specialist contributed which constraint>

## Open questions
<things the specialists genuinely disagreed on, marked clearly>

## Recommended next steps
<what work needs to happen to validate this design>
"""


def synthesize(history: DebateHistory, wiki: WikiScratchpad) -> FinalDesign:
    """Run the synthesizer over the completed debate."""

    debate_text = history.render_for_prompt(max_turns=999)
    wiki_summary = wiki.summary()

    user = f"""\
Engineering problem: {history.problem}

--- FULL DEBATE TRANSCRIPT ---
{debate_text}

--- WIKI ACTIVITY ---
{wiki_summary}
Disputes: {wiki.disputes}
Merged contributions: {wiki.merged}

Now produce the final design proposal."""

    raw = _call_claude(
        model=SYNTHESIZER_MODEL,
        system=SYNTHESIZER_SYSTEM,
        user=user,
        max_tokens=2500,
    )

    # Pull citations and open questions from output
    citations = re.findall(r"\[(?:arxiv|wiki|tool)/[^\]]+\]", raw)

    # Try to extract the "Open questions" section
    open_q_match = re.search(
        r"##+\s*Open questions\s*\n(.*?)(?=\n##+|\Z)",
        raw, re.DOTALL | re.IGNORECASE,
    )
    open_questions = []
    if open_q_match:
        open_questions = [
            line.strip("- *• \t")
            for line in open_q_match.group(1).split("\n")
            if line.strip("- *• \t")
        ]

    return FinalDesign(
        proposal=raw,
        citations=list(set(citations)),
        open_questions=open_questions,
        raw_text=raw,
    )
