"""
Obsidian vault → networkx graph loader.

Treats any folder of markdown files as a knowledge graph:
  - one node per .md file (filename stem = node id)
  - edges from `[[wikilinks]]` (with [[Note|alias]] alias support)
  - edges from `[[folder/Note]]` (Obsidian's nested-link syntax)
  - tags (`#tag`) collected as node attributes
  - YAML frontmatter parsed when present and exposed as node attrs
  - co-occurrence inside the same folder gets a small edge weight bump
    (Obsidian users tend to colocate related notes)

Why this exists:
  - Obsidian is local-first, no Docker, no LLM key required.
  - Vault structure already matches our wiki/concepts/*.md layout —
    same files work with both Obsidian and our learning app.
  - Tags are a natural alternative to Louvain clusters (tag-based
    clustering = explicit human curation instead of derived).

Public:
  load_vault(path)       → networkx.Graph with rich attrs
  vault_metadata(path)   → {n_notes, n_links, n_tags, top_tags, sample_path}
  find_default_vault()   → best-guess path or None
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

WIKILINK_RE  = re.compile(r"\[\[([^\[\]\|\n]+?)(?:\|([^\[\]\n]+))?\]\]")
TAG_RE       = re.compile(r"(?<!\S)#([A-Za-z][\w/\-]+)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(body: str) -> dict:
    """Cheap YAML-ish parser. Handles `key: value` and `key: [a, b]`.
    Falls back to {} on anything weird — we don't need full YAML."""
    m = FRONTMATTER_RE.match(body)
    if not m:
        return {}
    out: dict = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        # Inline list: [a, b, c]
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            out[k] = [s.strip().strip('"').strip("'")
                      for s in inner.split(",") if s.strip()]
        else:
            out[k] = v.strip().strip('"').strip("'")
    return out


def _strip_frontmatter(body: str) -> str:
    return FRONTMATTER_RE.sub("", body, count=1)


def find_default_vault() -> Path | None:
    """Look for a likely Obsidian vault.
    Order: env var → wiki/concepts/ if present → ~/Documents/Obsidian/* → None."""
    env = os.environ.get("OBSIDIAN_VAULT") or os.environ.get("BU_VAULT")
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p

    # Our own wiki dir doubles as a usable vault
    wiki = PROJECT_ROOT / "wiki" / "concepts"
    if wiki.is_dir():
        return wiki

    # Scan ~/Documents and ~/ for an .obsidian folder (vault marker)
    for home in (Path.home() / "Documents", Path.home()):
        if not home.is_dir():
            continue
        try:
            for child in home.iterdir():
                if not child.is_dir():
                    continue
                if (child / ".obsidian").is_dir():
                    return child
        except Exception:
            continue
    return None


def load_vault(path: str | Path) -> "networkx.Graph":
    """Walk a vault and build an undirected graph from wikilinks.

    Returns a graph where:
      - node id = file stem (e.g. 'Reynolds_number'), matching our existing
        clusters.py keys
      - node attrs = {path, folder, tags, frontmatter}
      - edge attr = {weight, kinds: ["wikilink", "folder"]}
    """
    import networkx as nx
    G = nx.Graph()
    p = Path(path).expanduser()
    if not p.is_dir():
        return G

    # Pass 1: collect every note + parse content
    notes: dict[str, dict] = {}
    for md in p.rglob("*.md"):
        # Skip Obsidian system files / templates / canvas
        if any(seg.startswith(".") for seg in md.relative_to(p).parts):
            continue
        try:
            body = md.read_text(errors="ignore")
        except Exception:
            continue
        stem = md.stem
        # Resolve aliases collisions: prefer first-seen, but keep multiple
        # under a 'duplicates' counter.
        if stem in notes:
            notes[stem]["duplicates"] = notes[stem].get("duplicates", 0) + 1
            continue
        fm = _parse_frontmatter(body)
        stripped = _strip_frontmatter(body)
        tags = set(TAG_RE.findall(stripped))
        # Frontmatter aliases / tags too
        if "tags" in fm:
            v = fm["tags"]
            if isinstance(v, list):
                tags.update(t.strip() for t in v if t.strip())
            elif isinstance(v, str):
                tags.update(t.strip() for t in v.split(",") if t.strip())
        notes[stem] = {
            "path": str(md.relative_to(p)),
            "folder": str(md.relative_to(p).parent),
            "tags": sorted(tags),
            "frontmatter": fm,
            "_body": stripped,
        }

    # Add nodes
    for stem, meta in notes.items():
        G.add_node(stem, path=meta["path"], folder=meta["folder"],
                   tags=meta["tags"], frontmatter=meta["frontmatter"])

    note_keys = set(notes.keys())

    # Build a normalized lookup so "Identifying Sets" → "Identifying_Sets",
    # "gkp algorithm" → "GKP_algorithm", etc. Obsidian wikilinks are
    # case-insensitive AND treat spaces as equivalent to underscores.
    def _norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    norm_to_stem: dict[str, str] = {}
    for k in note_keys:
        norm_to_stem.setdefault(_norm(k), k)

    def _resolve(target: str) -> str | None:
        """Map a wikilink target string to a real note stem, or None."""
        # Drop fragments / aliases / paths
        t = re.split(r"[#\^|]", target, 1)[0].strip()
        t = t.rsplit("/", 1)[-1]
        if not t:
            return None
        if t in note_keys:
            return t
        n = _norm(t)
        return norm_to_stem.get(n)

    # Pass 2: edges from wikilinks
    for stem, meta in notes.items():
        body = meta["_body"]
        for m in WIKILINK_RE.finditer(body):
            target_stem = _resolve(m.group(1).strip())
            if not target_stem or target_stem == stem:
                continue
            if G.has_edge(stem, target_stem):
                G[stem][target_stem]["weight"] = (
                    G[stem][target_stem].get("weight", 1) + 1
                )
                if "wikilink" not in G[stem][target_stem].get("kinds", []):
                    G[stem][target_stem].setdefault("kinds", []).append("wikilink")
            else:
                G.add_edge(stem, target_stem, weight=1, kinds=["wikilink"])

    # Pass 3: soft co-occurrence edges from folder colocation. Cheap signal —
    # don't add unless the folder is small (< 25 notes) so we don't densify
    # huge folders into cliques.
    by_folder: dict[str, list[str]] = {}
    for stem, meta in notes.items():
        by_folder.setdefault(meta["folder"], []).append(stem)
    for folder, members in by_folder.items():
        if folder in ("", "."):
            continue
        if len(members) < 2 or len(members) > 25:
            continue
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                if G.has_edge(a, b):
                    continue
                G.add_edge(a, b, weight=0.25, kinds=["folder"])

    return G


def vault_metadata(path: str | Path) -> dict:
    """Quick stats for the sidebar status panel. No graph build."""
    p = Path(path).expanduser()
    if not p.is_dir():
        return {"ok": False, "error": f"{p} is not a directory"}

    n_notes = 0
    n_links = 0
    tag_counter: Counter = Counter()
    sample_path = None
    for md in p.rglob("*.md"):
        if any(seg.startswith(".") for seg in md.relative_to(p).parts):
            continue
        try:
            body = md.read_text(errors="ignore")
        except Exception:
            continue
        n_notes += 1
        n_links += len(WIKILINK_RE.findall(body))
        for tag in TAG_RE.findall(body):
            tag_counter[tag] += 1
        if sample_path is None:
            sample_path = str(md.relative_to(p))

    return {
        "ok": True,
        "path": str(p),
        "n_notes": n_notes,
        "n_links": n_links,
        "n_tags": len(tag_counter),
        "top_tags": tag_counter.most_common(10),
        "sample_path": sample_path,
        "is_obsidian_vault": (p / ".obsidian").is_dir(),
    }


def is_obsidian_vault(path: str | Path) -> bool:
    p = Path(path).expanduser()
    return p.is_dir() and (p / ".obsidian").is_dir()


def init_vault_for_existing_wiki(path: str | Path) -> dict:
    """Tag a folder as an Obsidian vault by creating .obsidian/. Idempotent.

    Lets the user point Obsidian at our existing wiki/concepts/ folder
    and have it open instantly without re-importing — every note is
    already markdown with `[[wikilinks]]`.
    """
    p = Path(path).expanduser()
    if not p.is_dir():
        return {"ok": False, "error": f"{p} is not a directory"}
    obs = p / ".obsidian"
    obs.mkdir(parents=True, exist_ok=True)
    # Minimal config so Obsidian doesn't immediately overwrite with defaults
    cfg = obs / "app.json"
    if not cfg.exists():
        cfg.write_text(json.dumps({
            "alwaysUpdateLinks": True,
            "newLinkFormat": "shortest",
            "useMarkdownLinks": False,
        }, indent=2))
    return {"ok": True, "path": str(p), "marker": str(obs)}
