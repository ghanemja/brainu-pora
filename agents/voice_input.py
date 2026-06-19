"""
Voice input — Whisper transcription routed into the Propose tab.

Frontend records audio (webm/wav/mp3), POSTs it to /voice. This module
runs Whisper (faster-whisper preferred, openai-whisper fallback) and
returns the transcript. Caller then feeds the transcript to
proposal_responder.

Public:
  transcribe(audio_path, lang="en") → str
"""

from __future__ import annotations

import os
from pathlib import Path


def transcribe(audio_path: str | Path, lang: str = "en") -> str:
    """Transcribe audio file to text. Returns empty string on failure."""
    audio_path = Path(audio_path)
    if not audio_path.exists():
        return ""

    # Tier 1 — OpenAI whisper API (fastest if key present)
    if os.environ.get("OPENAI_API_KEY"):
        text = _openai_whisper(audio_path, lang)
        if text:
            return text

    # Tier 2 — local faster-whisper
    text = _faster_whisper(audio_path, lang)
    if text:
        return text

    # Tier 3 — local openai-whisper
    return _openai_whisper_local(audio_path, lang)


def _openai_whisper(audio_path: Path, lang: str) -> str:
    try:
        import requests
        with audio_path.open("rb") as f:
            r = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                data={"model": "whisper-1", "language": lang},
                files={"file": (audio_path.name, f, "audio/mpeg")},
                timeout=120,
            )
        if r.status_code == 200:
            return r.json().get("text", "").strip()
    except Exception:
        pass
    return ""


def _faster_whisper(audio_path: Path, lang: str) -> str:
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(audio_path), language=lang)
        return " ".join(s.text for s in segments).strip()
    except Exception:
        return ""


def _openai_whisper_local(audio_path: Path, lang: str) -> str:
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path), language=lang)
        return (result.get("text") or "").strip()
    except Exception:
        return ""


def available() -> dict:
    out = {"openai_api": False, "faster_whisper": False, "openai_whisper": False}
    out["openai_api"] = bool(os.environ.get("OPENAI_API_KEY"))
    try:
        import faster_whisper  # noqa
        out["faster_whisper"] = True
    except ImportError:
        pass
    try:
        import whisper  # noqa
        out["openai_whisper"] = True
    except ImportError:
        pass
    return out
