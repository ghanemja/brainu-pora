"""
Wiki I/O — the live "scratchpad" agents read from and propose edits to.

This is the novel layer of the system: agent debates aren't ephemeral, they
modify a persistent, structured knowledge base. The wiki grows over time,
disputes get logged, and the system's collective beliefs become inspectable.

Public surface:
  WikiScratchpad         # the runtime context for one debate
  WikiProposal           # an agent's proposed edit
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

PROJECT_ROOT = Path(__file__).parent.parent
WIKI_DIR = PROJECT_ROOT / "wiki"
CONCEPTS_DIR = WIKI_DIR / "concepts"
DRAFTS_DIR = WIKI_DIR / "drafts"
DISPUTES_DIR = WIKI_DIR / "disputes"
CONSENSUS_LOG = WIKI_DIR / "consensus.md"


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class WikiProposal:
    """An edit one agent wants to make to a concept page."""
    target_page: str                       # "concepts/Reynolds_number.md"
    operation: Literal["append", "edit_section", "create"]
    content: str                           # markdown to add
    rationale: str                         # one-line why
    proposed_by: str                       # agent name
    section: str | None = None             # for edit_section


# ── Wiki page selection (which pages does an agent see) ──────────────────────

def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


def _read_page(path: Path, max_chars: int = 4000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return text[:max_chars] + ("\n...[truncated]" if len(text) > max_chars else "")


def get_relevant_pages(query: str, topic_hints: list[str], max_pages: int = 3) -> list[dict]:
    """Find wiki concept pages relevant to the query, biased toward topic_hints.

    Simple keyword scoring — works well enough for prototype. Could swap for
    embedding-based search later.
    """
    if not CONCEPTS_DIR.exists():
        return []

    query_terms = set(re.findall(r"[a-z]+", query.lower()))
    hint_terms = set(t.lower() for t in topic_hints)

    scored = []
    for path in CONCEPTS_DIR.glob("*.md"):
        name_terms = set(re.findall(r"[a-z]+", path.stem.lower()))
        # Score: keyword overlap with query + hint bonus
        q_overlap = len(query_terms & name_terms)
        h_overlap = sum(1 for h in hint_terms if h in path.stem.lower())
        score = q_overlap * 2 + h_overlap
        if score > 0:
            scored.append((score, path))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {
            "path": str(p.relative_to(WIKI_DIR)),
            "name": p.stem.replace("_", " "),
            "content": _read_page(p),
            "_score": int(s),
        }
        for s, p in scored[:max_pages]
    ]


# ── Scratchpad runtime ───────────────────────────────────────────────────────

@dataclass
class WikiScratchpad:
    """Runtime container for a single debate's wiki interactions."""

    proposals: list[WikiProposal] = field(default_factory=list)
    merged: list[str] = field(default_factory=list)        # paths merged
    disputes: list[str] = field(default_factory=list)       # paths created
    debate_id: str = field(default_factory=lambda: datetime.now(
        timezone.utc).strftime("%Y%m%d_%H%M%S"))

    def __post_init__(self):
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
        DISPUTES_DIR.mkdir(parents=True, exist_ok=True)

    def add_proposal(self, p: WikiProposal):
        self.proposals.append(p)

    def read_only_view(self, query: str, topic_hints: list[str], max_pages: int = 3) -> list[dict]:
        return get_relevant_pages(query, topic_hints, max_pages)

    # ── Merge logic ──────────────────────────────────────────────────────────

    def process_proposals(self) -> dict:
        """Group proposals by target page and either merge consensus or create dispute."""
        by_page: dict[str, list[WikiProposal]] = {}
        for p in self.proposals:
            by_page.setdefault(p.target_page, []).append(p)

        report = {"merged": [], "disputes": [], "skipped": []}
        for page, props in by_page.items():
            if len(props) == 1:
                # Single proposal — merge
                self._merge_one(props[0])
                report["merged"].append(page)
            elif self._compatible(props):
                # Multiple but compatible — append all
                for p in props:
                    self._merge_one(p)
                report["merged"].append(f"{page} (×{len(props)})")
            else:
                # Genuine disagreement → dispute page
                disp_path = self._create_dispute(page, props)
                report["disputes"].append(str(disp_path))

        self.merged.extend(report["merged"])
        self.disputes.extend(report["disputes"])
        return report

    def _compatible(self, proposals: list[WikiProposal]) -> bool:
        """Heuristic: if all proposals are 'append', they're compatible.
        If any wants to 'edit_section' on the same section, they conflict."""
        ops = [p.operation for p in proposals]
        if all(o == "append" for o in ops):
            return True
        # Same-section edits = conflict
        edit_sections = [p.section for p in proposals if p.operation == "edit_section"]
        if len(edit_sections) != len(set(edit_sections)):
            return False
        return False  # default to dispute when in doubt

    def _merge_one(self, p: WikiProposal):
        target = WIKI_DIR / p.target_page
        target.parent.mkdir(parents=True, exist_ok=True)
        block = (
            f"\n\n<!-- merged {self.debate_id} by {p.proposed_by}: {p.rationale} -->\n"
            f"{p.content.strip()}\n"
        )
        if p.operation == "create" and not target.exists():
            target.write_text(f"# {target.stem.replace('_', ' ')}\n{block}")
        elif p.operation == "append":
            with open(target, "a", encoding="utf-8") as f:
                f.write(block)
        elif p.operation == "edit_section":
            # Simple impl: append with a section marker. A smarter version
            # would parse markdown and insert at the right section.
            with open(target, "a", encoding="utf-8") as f:
                f.write(f"\n## {p.section or 'Notes'}\n{block}")
        # Also append to consensus log
        self._append_consensus_log(p)

    def _create_dispute(self, page: str, proposals: list[WikiProposal]) -> Path:
        topic = Path(page).stem
        out = DISPUTES_DIR / f"{self.debate_id}_{topic}.md"
        body = [
            f"# Dispute: {topic.replace('_', ' ')}",
            f"\n*Debate {self.debate_id} — agents disagreed on this concept page.*\n",
            f"\nTarget page: `{page}`\n",
        ]
        for p in proposals:
            body.append(f"\n## View from {p.proposed_by}\n")
            body.append(f"**Rationale:** {p.rationale}\n")
            body.append(f"**Proposed operation:** `{p.operation}`")
            if p.section:
                body.append(f" on section `{p.section}`")
            body.append(f"\n\n{p.content.strip()}\n")
            body.append("\n---\n")
        out.write_text("\n".join(body))
        return out

    def _append_consensus_log(self, p: WikiProposal):
        if not CONSENSUS_LOG.exists():
            CONSENSUS_LOG.write_text("# Consensus log\n\n")
        with open(CONSENSUS_LOG, "a", encoding="utf-8") as f:
            f.write(
                f"- [{self.debate_id}] {p.proposed_by} → `{p.target_page}` "
                f"({p.operation}): {p.rationale}\n"
            )

    # ── Diff utilities ───────────────────────────────────────────────────────

    def summary(self) -> str:
        return (
            f"Wiki scratchpad for debate {self.debate_id}: "
            f"{len(self.proposals)} proposals, "
            f"{len(self.merged)} merged, "
            f"{len(self.disputes)} dispute pages."
        )


# ── Parsing helper for agent output ──────────────────────────────────────────

WIKI_PROPOSAL_RE = re.compile(
    r"<wiki_proposal>(.*?)</wiki_proposal>",
    re.DOTALL | re.IGNORECASE,
)


def parse_wiki_proposal(agent_text: str, agent_name: str) -> WikiProposal | None:
    """Extract a WikiProposal from an agent's response, if present."""
    m = WIKI_PROPOSAL_RE.search(agent_text)
    if not m:
        return None

    body = m.group(1).strip()
    fields: dict[str, str] = {}
    current_key = None
    content_lines: list[str] = []

    for line in body.split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if k in {"target_page", "operation", "section", "rationale"}:
                fields[k] = v
                current_key = k
                continue
            if k == "content":
                current_key = "content"
                if v and v != "|":
                    content_lines.append(v)
                continue
        if current_key == "content":
            content_lines.append(line)

    target = fields.get("target_page", "").strip()
    operation = fields.get("operation", "append").strip().lower()
    if operation not in {"append", "edit_section", "create"}:
        operation = "append"
    if not target or not content_lines:
        return None

    return WikiProposal(
        target_page=target,
        operation=operation,  # type: ignore
        section=fields.get("section") or None,
        content="\n".join(content_lines).strip(),
        rationale=fields.get("rationale", ""),
        proposed_by=agent_name,
    )
