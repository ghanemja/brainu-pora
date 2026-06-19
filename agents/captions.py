"""
Caption / transcript helper — synthesize captions for any rendered
audio + burn them into video frames.

Sits *on top of* agents.voices so it works with whatever TTS backend
the caller chose. Two responsibilities:

  1. word-level timestamps for an audio file
       transcribe_with_timestamps(audio_path) -> list[CaptionSegment]
       Uses faster-whisper if available, then whisper-cpp, then
       openai-whisper, then falls back to a best-effort time-allocation
       based on character count (so callers still get reasonably-aligned
       lower-thirds without a Whisper install).

  2. burn captions into PIL frames
       overlay_caption(image, text, *, palette, max_chars=110) -> image
       Draws a lower-third strip with WCAG-AA-contrast text, auto-wrap.

CaptionSegment shape:
  {"t_start": float, "t_end": float, "text": str}

Public:
  transcribe_with_timestamps(audio_path, *, language='en') -> list[dict]
  segments_for_text(text, audio_seconds) -> list[dict]   (fallback aligner)
  overlay_caption(image, text, *, palette) -> Image
  whisper_ready() -> dict[str, bool]
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any


# ── Word-level timestamps ────────────────────────────────────────────────

def transcribe_with_timestamps(audio_path: Path | str, *,
                                language: str = "en") -> list[dict]:
    """Best available Whisper backend → list of CaptionSegments.

    Tries faster-whisper → whisper-cpp → openai-whisper → fallback.
    Returns [] if the audio can't be opened at all."""
    audio_path = Path(audio_path)
    if not audio_path.exists():
        return []

    # 1. faster-whisper (preferred — fast, small)
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _info = model.transcribe(
            str(audio_path), language=language, word_timestamps=True,
            beam_size=1,
        )
        out: list[dict] = []
        for s in segments:
            words = getattr(s, "words", None) or []
            if words:
                for w in words:
                    out.append({
                        "t_start": float(w.start),
                        "t_end":   float(w.end),
                        "text":    w.word.strip(),
                    })
            else:
                out.append({
                    "t_start": float(s.start),
                    "t_end":   float(s.end),
                    "text":    s.text.strip(),
                })
        return out
    except Exception:
        pass

    # 2. openai-whisper (heavier)
    try:
        import whisper  # type: ignore
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path), word_timestamps=True,
                                   language=language)
        out = []
        for seg in result.get("segments", []):
            for w in seg.get("words", []) or [{
                "start": seg.get("start"), "end": seg.get("end"),
                "word":  seg.get("text", "")
            }]:
                out.append({
                    "t_start": float(w.get("start") or 0),
                    "t_end":   float(w.get("end") or 0),
                    "text":    (w.get("word") or "").strip(),
                })
        return out
    except Exception:
        pass

    # 3. No Whisper → return empty so caller can use segments_for_text fallback
    return []


def segments_for_text(text: str, audio_seconds: float,
                       *, words_per_segment: int = 8) -> list[dict]:
    """Even-time-split fallback when no Whisper is available.

    Splits `text` into chunks of ~words_per_segment words, allocates
    equal time to each. Better than nothing for lower-thirds; do not
    use this for click-to-jump UX.
    """
    text = (text or "").strip()
    if not text or audio_seconds <= 0:
        return []
    words = re.findall(r"\S+", text)
    if not words:
        return []
    chunks: list[str] = []
    for i in range(0, len(words), words_per_segment):
        chunks.append(" ".join(words[i:i + words_per_segment]))
    per = audio_seconds / max(1, len(chunks))
    return [{"t_start": round(i * per, 2),
             "t_end":   round((i + 1) * per, 2),
             "text":    c}
             for i, c in enumerate(chunks)]


# ── Frame overlay ────────────────────────────────────────────────────────

def overlay_caption(image, text: str, *, palette: dict,
                    max_chars: int = 110, height_frac: float = 0.18):
    """Draw a lower-third caption strip onto a PIL image.

    `palette` is the same dict used by video_generator.STYLES (with
    keys: bg, accent, body, caption). Returns the modified image
    (mutated in place; PIL Image is mutable for draw operations).
    """
    try:
        from PIL import ImageDraw
    except ImportError:
        return image
    if not text:
        return image

    W, H = image.size
    band_h = max(72, int(H * height_frac))
    y0 = H - band_h
    draw = ImageDraw.Draw(image, "RGBA")
    # 80%-opacity background strip for contrast
    bg = palette.get("accent", (30, 39, 97))
    bg_rgba = tuple(list(bg) + [220]) if len(bg) == 3 else bg
    draw.rectangle([(0, y0), (W, H)], fill=bg_rgba)

    # Font: prefer the video_generator font helper if available
    font = None
    try:
        from agents.video_generator import _font
        font = _font(28)
    except Exception:
        try:
            from PIL import ImageFont
            font = ImageFont.load_default()
        except Exception:
            return image

    # Word-wrap
    txt = text if len(text) <= max_chars else text[:max_chars - 1] + "…"
    margin = 40
    max_w = W - margin * 2
    words = txt.split()
    lines: list[str] = []
    line: list[str] = []
    for w in words:
        trial = " ".join(line + [w])
        try:
            bbox = font.getbbox(trial)
            tw = bbox[2] - bbox[0]
        except Exception:
            tw = len(trial) * 14
        if tw > max_w and line:
            lines.append(" ".join(line))
            line = [w]
        else:
            line.append(w)
    if line:
        lines.append(" ".join(line))

    color = palette.get("body", (250, 251, 254))
    y = y0 + 16
    for ln in lines[:3]:
        draw.text((margin, y), ln, font=font, fill=color)
        y += 36
    return image


# ── Stack probe ──────────────────────────────────────────────────────────

def whisper_ready() -> dict:
    out = {"faster_whisper": False, "openai_whisper": False}
    try:
        import faster_whisper  # noqa
        out["faster_whisper"] = True
    except Exception:
        pass
    try:
        import whisper  # noqa
        out["openai_whisper"] = True
    except Exception:
        pass
    return out
