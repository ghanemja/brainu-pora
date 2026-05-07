"""
Citation parser — extracts everything an agent cited in a single turn.

Used by the RL system for credit assignment: when feedback arrives on a
response, the cited entities/edges/wiki-pages get a reward delta applied.

Three citation kinds are recognized:
  [arxiv/<category>/<paper_id>(#chunk)]    → arXiv chunk
  [[wiki/<page_name>]]                      → wiki concept page
  [tool/<tool_name>]                        → physics tool call

Plus a "loose entity" extractor: any TitleCase or ALLCAPS token sequence in
the agent's prose, which we'll fuzzy-match against Graphiti node names for
graph-edge credit assignment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


CITATION_PATTERNS = {
    "arxiv": re.compile(r"\[arxiv/([a-z_-]+)/([\w.-]+?)(?:#(\d+))?\]"),
    "wiki":  re.compile(r"\[\[wiki/([\w/_.-]+?)\]\]"),
    "tool":  re.compile(r"\[tool/([\w_-]+)\]"),
}

# TitleCase or ALLCAPS run, length ≥ 2 words, used for entity fuzzy-match.
ENTITY_PATTERN = re.compile(
    r"\b(?:[A-Z][a-z0-9]+(?:[\s\-_][A-Z][a-z0-9]+)+|[A-Z]{2,}(?:\s[A-Z]{2,})*)\b"
)


@dataclass
class TurnCitations:
    arxiv: list[dict] = field(default_factory=list)   # {category, paper_id, chunk}
    wiki:  list[str]  = field(default_factory=list)   # page slug
    tool:  list[str]  = field(default_factory=list)   # tool name
    entities: list[str] = field(default_factory=list) # loose TitleCase entities

    def is_empty(self) -> bool:
        return not (self.arxiv or self.wiki or self.tool or self.entities)

    def to_credit_targets(self) -> list[tuple[str, str]]:
        """Flat list of (kind, key) tuples for the credit-assignment loop."""
        out: list[tuple[str, str]] = []
        for c in self.arxiv:
            out.append(("arxiv", f"{c['category']}/{c['paper_id']}"))
        for w in self.wiki:
            out.append(("wiki", w))
        for t in self.tool:
            out.append(("tool", t))
        for e in self.entities:
            out.append(("entity", e))
        return out


def parse(text: str) -> TurnCitations:
    """Parse all citation kinds + loose entities from an agent's turn."""
    out = TurnCitations()
    for m in CITATION_PATTERNS["arxiv"].finditer(text):
        out.arxiv.append({
            "category": m.group(1),
            "paper_id": m.group(2),
            "chunk":    int(m.group(3)) if m.group(3) else None,
        })
    out.wiki = list(dict.fromkeys(CITATION_PATTERNS["wiki"].findall(text)))
    out.tool = list(dict.fromkeys(CITATION_PATTERNS["tool"].findall(text)))

    # Entity extraction — dedupe + filter junk
    seen = set()
    for m in ENTITY_PATTERN.finditer(text):
        # Collapse whitespace runs (regex \s matches \n) so multi-line entities
        # like "Proportional\nNavigation" become a single token.
        ent = re.sub(r"\s+", " ", m.group(0)).strip()
        if len(ent) < 4 or ent.lower() in _STOP_ENTITY:
            continue
        if ent in seen:
            continue
        seen.add(ent)
        out.entities.append(ent)
    # Cap entity list — long lists wash out credit signal
    out.entities = out.entities[:20]
    return out


_STOP_ENTITY = {
    # noisy first-words that often start sentences
    "the", "this", "that", "these", "those",
    "your", "our", "their",
    "what", "when", "where", "which", "who",
}
