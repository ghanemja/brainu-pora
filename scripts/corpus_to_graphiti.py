"""
Stream the defense corpus (data/defense_corpus/MANIFEST.jsonl) into Graphiti
as temporal episodes.

For each manifest row:
  - Extract text: PDF via PyMuPDF, else use {title + abstract}
  - Chunk into ~1500-char windows (fits in one Anthropic call)
  - Per chunk → Graphiti add_episode with reference_time = doc.date
  - Each episode produces facts; contradictions invalidate older edges

This is the engine that makes the "live brain" actually evolve: as new
papers land, edges form; when newer papers contradict older claims,
Graphiti marks the older edges with t_invalid (preserved for the time-
slider but rendered dashed in the live view).

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 scripts/corpus_to_graphiti.py                       # all manifest rows
    python3 scripts/corpus_to_graphiti.py --topic boost_phase_intercept
    python3 scripts/corpus_to_graphiti.py --max 20 --metadata_only
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CORPUS_DIR = PROJECT_ROOT / "data" / "defense_corpus"
MANIFEST   = CORPUS_DIR / "MANIFEST.jsonl"
STATE      = CORPUS_DIR / ".ingested_ids.txt"  # incremental: skip what we already did

GROUP_ID = "defense_corpus"


def chunk_text(s: str, target: int = 1500, overlap: int = 150) -> list[str]:
    s = " ".join(s.split())
    if len(s) <= target:
        return [s] if s else []
    out, i = [], 0
    while i < len(s):
        chunk = s[i : i + target]
        # snap to sentence end if possible
        last_dot = chunk.rfind(". ")
        if last_dot > target * 0.6:
            chunk = chunk[: last_dot + 1]
        out.append(chunk)
        i += max(1, len(chunk) - overlap)
    return out


def extract_pdf_text(pdf_path: Path, max_chars: int = 60_000) -> str:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("    [warn] PyMuPDF not installed — using metadata only")
        return ""
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"    [warn] {pdf_path.name}: {e}")
        return ""
    parts = []
    chars = 0
    for page in doc:
        t = page.get_text("text") or ""
        parts.append(t)
        chars += len(t)
        if chars > max_chars:
            break
    doc.close()
    return "\n".join(parts)[:max_chars]


def parse_date(s: str | None) -> datetime:
    if not s:
        return datetime.now(timezone.utc)
    s = s[:10]
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return datetime.now(timezone.utc)


def load_done() -> set[str]:
    if not STATE.exists():
        return set()
    return set(STATE.read_text().splitlines())


def mark_done(nid: str) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    with STATE.open("a") as f:
        f.write(nid + "\n")


def iter_manifest():
    if not MANIFEST.exists():
        sys.exit(f"✗ {MANIFEST} not found — run scripts/download_defense_corpus.py first")
    for line in MANIFEST.read_text().splitlines():
        if line.strip():
            try:
                yield json.loads(line)
            except Exception:
                continue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default=None, help="Filter to one topic")
    ap.add_argument("--source", default=None, help="Filter to one source (ntrs|arxiv|openalex)")
    ap.add_argument("--max", type=int, default=None, help="Cap number of docs")
    ap.add_argument("--metadata_only", action="store_true",
                    help="Skip PDF text — use title+abstract only (much faster, cheaper)")
    ap.add_argument("--max_chunks_per_doc", type=int, default=4,
                    help="Cap chunks/doc to keep Anthropic costs sane")
    ap.add_argument("--sleep", type=float, default=2.0)
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("✗ ANTHROPIC_API_KEY not set")

    try:
        from graph.temporal_graph import add_episode
    except ImportError as e:
        sys.exit(f"✗ Graphiti not installed: {e}")

    done = load_done()
    rows = list(iter_manifest())
    if args.topic:
        rows = [r for r in rows if r.get("topic") == args.topic]
    if args.source:
        rows = [r for r in rows if r.get("source") == args.source]
    rows = [r for r in rows if r["id"] not in done]
    if args.max:
        rows = rows[: args.max]

    print(f"[Corpus→Graphiti] {len(rows)} new docs to ingest "
          f"(topic={args.topic or 'ALL'}, source={args.source or 'ALL'}, "
          f"already_done={len(done)})")

    stats = {"docs_ok": 0, "docs_err": 0, "episodes": 0,
             "nodes": 0, "edges": 0, "invalidated": 0}

    for i, row in enumerate(rows, 1):
        nid = row["id"]
        title = row.get("title", "") or ""
        abstract = row.get("abstract", "") or ""
        topic = row.get("topic", "")
        ref_time = parse_date(row.get("date"))

        # Build text body
        text_parts = []
        if title:
            text_parts.append(f"Title: {title}")
        if abstract:
            text_parts.append(f"Abstract: {abstract}")

        pdf_path_rel = row.get("pdf_path")
        if pdf_path_rel and not args.metadata_only:
            pdf_path = PROJECT_ROOT / pdf_path_rel
            if pdf_path.exists():
                pdf_text = extract_pdf_text(pdf_path)
                if pdf_text.strip():
                    text_parts.append(pdf_text)

        full_text = "\n\n".join(text_parts).strip()
        if not full_text:
            print(f"  [skip {i}/{len(rows)}] {nid} — no text")
            mark_done(nid)
            stats["docs_err"] += 1
            continue

        chunks = chunk_text(full_text)[: args.max_chunks_per_doc]
        print(f"  [{i}/{len(rows)}] {nid}  {len(chunks)} chunks  → ", end="", flush=True)

        try:
            for j, chunk in enumerate(chunks):
                ep_name = f"{nid}#{j}"
                body = f"[topic:{topic}] {chunk}"
                t0 = time.time()
                r = add_episode(
                    name=ep_name,
                    episode_body=body,
                    reference_time=ref_time,
                    source_description=f"{row.get('source')} :: {title[:80]}",
                    group_id=GROUP_ID,
                )
                stats["episodes"] += 1
                stats["nodes"] += r.get("n_nodes_added", 0)
                stats["edges"] += r.get("n_edges_added", 0)
                stats["invalidated"] += r.get("n_invalidated", 0)
                print(f"+{r.get('n_edges_added',0)}e({time.time()-t0:.1f}s)", end=" ", flush=True)
                time.sleep(args.sleep)

            mark_done(nid)
            stats["docs_ok"] += 1
            print(f" totals: {stats['nodes']}n {stats['edges']}e {stats['invalidated']}inv", flush=True)

        except Exception as e:
            stats["docs_err"] += 1
            print(f"  ✗ {nid}: {type(e).__name__}: {str(e)[:160]}")
            # Abort on auth errors — no point grinding through the rest
            if "api_key" in str(e).lower() or "ANTHROPIC_API_KEY" in str(e):
                print("\n✗ aborting — set ANTHROPIC_API_KEY and rerun")
                break

    print(f"\n[Done] {stats}")


if __name__ == "__main__":
    main()
