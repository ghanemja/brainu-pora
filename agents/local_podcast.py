"""
Local podcast generator — one-shot URL/text → mp3 podcast, fully offline.

Two implementations under one interface:

  - "kokoro_pipeline"  Uses our existing podcast_script + podcast_video
                       with VOICES_BACKEND=kokoro. Best when you already
                       have a script in our shape.

  - "podcastfy"        Wraps the `podcastfy` library. Drop-in NotebookLM
                       clone. Accepts URLs / PDFs / text directly and
                       produces a polished 2-host mp3. Local mode uses
                       edge-tts (free, no API key) or kokoro.

Public:
  generate_local(source, mode='auto', length='medium', out_dir=None) -> Path | None
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MEDIA_DIR = PROJECT_ROOT / "data" / "sessions" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def _meta_path_for(mp3: Path) -> Path:
    """Sidecar JSON next to an mp3: stores source text + render config so
    /podcast/local/interject can recover the source without re-fetching."""
    return mp3.with_suffix(".meta.json")


def save_meta(mp3: Path, *, source_text: str, mode: str, length: str) -> None:
    meta = {
        "source_text": source_text[:8000],
        "mode":        mode,
        "length":      length,
    }
    _meta_path_for(mp3).write_text(json.dumps(meta))


def load_meta(mp3: Path) -> dict | None:
    p = _meta_path_for(mp3)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def lookup_mp3(filename: str) -> Path | None:
    """Resolve an mp3 filename (or relative path) to an absolute Path inside
    MEDIA_DIR. Used by the interject endpoint."""
    name = Path(filename).name
    p = MEDIA_DIR / name
    return p if p.exists() else None


def generate_local(
    source: str | list[str],
    *,
    mode: str = "auto",
    length: str = "medium",
    tts: str = "edge",
    out_dir: Path | None = None,
) -> Path | None:
    """One-shot local podcast generation.

    Args:
      source: URL, file path, PDF path, or raw text. List → multi-source.
      mode:   'auto' picks podcastfy if available, else kokoro_pipeline.
              'podcastfy' or 'kokoro_pipeline' force a path.
      length: 'short' / 'medium' / 'long'
      tts:    podcastfy TTS — 'edge' (free, online but no API key needed) or
              'openai' (paid). Use 'kokoro' if podcastfy ships a Kokoro
              binding in the installed version.
      out_dir: where to drop the .mp3 (defaults to MEDIA_DIR).

    Returns: Path to the .mp3 or None if generation failed.
    """
    out_dir = Path(out_dir) if out_dir else MEDIA_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    if mode == "auto":
        mode = "podcastfy" if _podcastfy_available() else "kokoro_pipeline"

    if mode == "podcastfy":
        result = _via_podcastfy(source, length=length, tts=tts, out_dir=out_dir)
    elif mode == "kokoro_pipeline":
        result = _via_kokoro_pipeline(source, length=length, out_dir=out_dir)
    else:
        return None

    if result and result.exists():
        src_text = source if isinstance(source, str) else "\n\n".join(source or [])
        save_meta(result, source_text=src_text, mode=mode, length=length)
    return result


# ── podcastfy path (NotebookLM-style one-shot) ────────────────────────────

def _podcastfy_available() -> bool:
    try:
        import podcastfy  # noqa
        return True
    except ImportError:
        return False


def _via_podcastfy(source, length: str, tts: str, out_dir: Path) -> Path | None:
    """Run podcastfy.client.generate_podcast and return the mp3 path."""
    try:
        from podcastfy.client import generate_podcast
    except ImportError:
        return None

    word_targets = {"short": 800, "medium": 2000, "long": 4000}
    conversation_config = {
        "word_count":        word_targets.get(length, 2000),
        "conversation_style": ["engaging", "educational", "thought-provoking"],
        "podcast_name":      "Brain University",
        "podcast_tagline":   "Papers, deconstructed.",
        "output_language":   "English",
        "dialogue_structure": ["Hook", "Setup", "Core insight",
                                "Worked example", "Tensions", "Wrap"],
        "creativity":        0.7,
    }

    # Build kwargs. podcastfy accepts urls= for web/PDF, text= for raw.
    src_list = source if isinstance(source, list) else [source]
    looks_like_url = any(
        (s.startswith("http") or s.endswith(".pdf")) for s in src_list
        if isinstance(s, str)
    )
    kwargs = {
        "tts_model":          tts,        # 'edge' is free + local
        "conversation_config": conversation_config,
    }
    if looks_like_url:
        kwargs["urls"] = src_list
    else:
        kwargs["text"] = "\n\n".join(src_list)

    # Anthropic preferred when key present (matches the rest of the app)
    if os.environ.get("ANTHROPIC_API_KEY"):
        kwargs["llm_model_name"] = "claude-haiku-4-5"
        kwargs["api_key_label"]  = "ANTHROPIC_API_KEY"

    try:
        result = generate_podcast(**kwargs)
    except Exception as e:
        # propagate to caller via None; logs go to stderr by default
        print(f"[local_podcast] podcastfy failed: {e}")
        return None

    # result may be a Path, str, or list of paths
    out_paths = result if isinstance(result, list) else [result]
    for p in out_paths:
        if not p:
            continue
        path = Path(p)
        if path.exists() and path.suffix.lower() in {".mp3", ".wav"}:
            # Copy to our media dir for serving
            dst = out_dir / path.name
            if path.resolve() != dst.resolve():
                dst.write_bytes(path.read_bytes())
            return dst
    return None


# ── Kokoro pipeline path (reuse our existing renderer w/ local voices) ────

def _via_kokoro_pipeline(source, length: str, out_dir: Path) -> Path | None:
    """Use our own podcast_script + podcast_video with VOICES_BACKEND=kokoro."""
    from . import podcast_script, podcast_video

    text = source if isinstance(source, str) else "\n\n".join(source)
    if text.startswith("http") or text.endswith(".pdf"):
        # We don't fetch URLs in this path — caller should pass extracted text
        return None

    script = podcast_script.generate_script(
        topic="Local podcast",
        source_text=text,
        length=length,
    )
    if not script:
        return None

    result = podcast_video.render(script, voice_backend="kokoro")
    if not result:
        return None
    return result.get("mp3")


# ── Capability probe ───────────────────────────────────────────────────────

def status() -> dict:
    """Report which local-podcast backends are usable right now."""
    out = {"podcastfy": _podcastfy_available()}
    try:
        import kokoro  # noqa
        out["kokoro"] = True
    except ImportError:
        out["kokoro"] = False
    try:
        import edge_tts  # noqa
        out["edge_tts"] = True
    except ImportError:
        out["edge_tts"] = False
    return out
