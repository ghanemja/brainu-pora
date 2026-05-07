"""
Build per-domain BM25 indices for the multi-specialist agent system.

Each specialist (aero, mech, cs) gets its own RAG index built from the
arXiv categories most relevant to that domain. There is intentional
overlap (physics_class-ph appears in both aero and mech) — it reflects
the real shared foundation.

Reads:
  data/raw/arxiv/<category>/*.txt    (8,325 papers)
  data/cleaned/transcripts.jsonl     (45,118 lecture chunks, optional fold-in)

Writes:
  rag/indices/aero.pkl
  rag/indices/mech.pkl
  rag/indices/cs.pkl

Usage:
    python rag/build_split_indices.py
    python rag/build_split_indices.py --include_transcripts
"""

from __future__ import annotations

import argparse
import json
import pickle
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

HERE = Path(__file__).parent
ARXIV_DIR = HERE.parent / "data" / "raw" / "arxiv"
TRANSCRIPTS = HERE.parent / "data" / "cleaned" / "transcripts.jsonl"
OUT_DIR = HERE / "indices"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")

# Domain → arXiv category slugs
# Overlap is intentional and physically real
DOMAIN_CATEGORIES = {
    "aero": [
        "physics_flu-dyn",      # fluid dynamics
        "physics_class-ph",     # classical physics (mechanics, EM)
        "astro-ph_IM",          # astro instrumentation
        "eess_SY",              # systems & control
        "physics_comp-ph",      # computational physics (CFD)
    ],
    "mech": [
        "physics_class-ph",     # classical physics (overlap with aero)
        "cond-mat_mtrl-sci",    # materials science
        "eess_SY",              # systems & control (overlap)
        "eess_SP",              # signal processing (overlap with cs)
    ],
    "cs": [
        "cs_RO",                # robotics
        "cs_DS",                # data structures & algorithms
        "cs_OS",                # operating systems
        "cs_PL",                # programming languages
        "cs_CE",                # computational engineering
        "math_OC",              # optimization & control
        "math_NA",              # numerical analysis
        "math_DS",              # dynamical systems
    ],
}


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text) if len(t) > 2]


def chunk_text(text: str, target_chars: int = 4000, min_chars: int = 800) -> list[str]:
    """Split a long arXiv paper into chunks, on paragraph breaks where possible."""
    paragraphs = re.split(r"\n\s*\n", text)
    out, buf, buf_len = [], [], 0
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if buf_len + len(para) > target_chars and buf_len >= min_chars:
            out.append("\n\n".join(buf))
            buf, buf_len = [para], len(para)
        else:
            buf.append(para)
            buf_len += len(para)
    if buf and buf_len >= min_chars:
        out.append("\n\n".join(buf))
    return out


def load_arxiv_chunks(categories: list[str]) -> list[dict]:
    """Load and chunk arXiv papers for a given list of categories."""
    chunks = []
    for cat in categories:
        cat_dir = ARXIV_DIR / cat
        if not cat_dir.exists():
            continue
        for txt_path in sorted(cat_dir.glob("*.txt")):
            try:
                text = txt_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for i, ck in enumerate(chunk_text(text)):
                chunks.append({
                    "text": ck,
                    "source_type": "arxiv",
                    "category": cat,
                    "paper_id": txt_path.stem,
                    "source": f"arxiv/{cat}/{txt_path.name}#{i}",
                    "id": f"arxiv-{cat}-{txt_path.stem}-{i}",
                })
    return chunks


def load_transcript_chunks() -> list[dict]:
    """Load already-chunked MIT/Stanford lecture transcripts."""
    rows = []
    if not TRANSCRIPTS.exists():
        return rows
    with open(TRANSCRIPTS) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            text = obj.get("text", "")
            if len(text) < 80:
                continue
            rows.append({
                "text": text,
                "source_type": "transcript",
                "category": "lecture",
                "paper_id": "",
                "source": str(obj.get("source", "")),
                "id": f"lec-{i}",
            })
    return rows


def build_index(chunks: list[dict], out_path: Path):
    if not chunks:
        print(f"  (no chunks for {out_path.stem} — skipping)")
        return
    print(f"  Tokenizing {len(chunks):,} chunks...")
    tokenized = [tokenize(c["text"]) for c in chunks]
    print(f"  Building BM25...")
    bm25 = BM25Okapi(tokenized)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks}, f)
    size_mb = out_path.stat().st_size / 1e6
    print(f"  → {out_path}  ({size_mb:.1f} MB, {len(chunks):,} chunks)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--include_transcripts",
        action="store_true",
        help="Include the 45k MIT/Stanford lecture chunks in EVERY domain index "
             "(transcripts are general engineering and useful to all specialists)",
    )
    args = ap.parse_args()

    transcript_chunks = load_transcript_chunks() if args.include_transcripts else []
    if transcript_chunks:
        print(f"[shared] {len(transcript_chunks):,} transcript chunks "
              f"(will be added to every domain)")

    for domain, categories in DOMAIN_CATEGORIES.items():
        print(f"\n[{domain}] categories: {categories}")
        chunks = load_arxiv_chunks(categories)
        print(f"  arXiv: {len(chunks):,} chunks")
        if transcript_chunks:
            chunks = chunks + transcript_chunks
        out = OUT_DIR / f"{domain}.pkl"
        build_index(chunks, out)

    print(f"\n[Done] indices in {OUT_DIR}")


if __name__ == "__main__":
    main()
