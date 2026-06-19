"""
Voice / TTS abstraction.

Single entry point: `synthesize(text, voice_id, out_path)` → Path | None.

Backends (selected via VOICES_BACKEND env var or per-call):
  gtts        — free, online, single voice per lang. Distinguishes hosts
                via lang variants (en-US for A, en-GB for B).
  pyttsx3     — free, offline. Distinguishes via system voice index.
  elevenlabs  — premium, distinct natural voices (needs ELEVENLABS_API_KEY)
  openai_tts  — premium, distinct voices (needs OPENAI_API_KEY)

The `voice_id` is logical ("host_a" | "host_b" | "narrator"). Each backend
maps logical→concrete in VOICE_MAP below.

All backends produce .mp3 at out_path. Returns None on failure.
"""

from __future__ import annotations

import os
from pathlib import Path

VOICE_MAP = {
    "gtts": {
        "host_a":   {"lang": "en", "tld": "com",   "slow": False},   # US
        "host_b":   {"lang": "en", "tld": "co.uk", "slow": False},   # UK
        "narrator": {"lang": "en", "tld": "com.au","slow": False},   # AU
    },
    "pyttsx3": {
        "host_a":   {"voice_idx": 0, "rate": 175},
        "host_b":   {"voice_idx": 1, "rate": 165},
        "narrator": {"voice_idx": 0, "rate": 170},
    },
    "elevenlabs": {
        "host_a":   {"voice": "Rachel"},
        "host_b":   {"voice": "Antoni"},
        "narrator": {"voice": "Bella"},
    },
    "openai_tts": {
        "host_a":   {"voice": "nova"},
        "host_b":   {"voice": "onyx"},
        "narrator": {"voice": "shimmer"},
    },
    # Kokoro-82M — local, offline, no API key, ~80MB model. CPU-friendly.
    # Voice IDs from the published Kokoro voice pack.
    "kokoro": {
        "host_a":   {"voice": "af_bella",   "speed": 1.0},
        "host_b":   {"voice": "am_michael", "speed": 1.0},
        "narrator": {"voice": "af_nicole",  "speed": 1.0},
    },
}


def synthesize(
    text: str,
    voice_id: str = "narrator",
    out_path: Path | str | None = None,
    backend: str | None = None,
) -> Path | None:
    """Synthesize `text` to an mp3 at `out_path`. Returns Path or None."""
    if not text or not text.strip():
        return None
    backend = backend or os.environ.get("VOICES_BACKEND", "gtts")
    out_path = Path(out_path) if out_path else None

    if backend == "gtts":
        return _tts_gtts(text, voice_id, out_path)
    if backend == "pyttsx3":
        return _tts_pyttsx3(text, voice_id, out_path)
    if backend == "elevenlabs":
        return _tts_elevenlabs(text, voice_id, out_path)
    if backend == "openai_tts":
        return _tts_openai(text, voice_id, out_path)
    if backend == "kokoro":
        return _tts_kokoro(text, voice_id, out_path)
    return None


def _tts_gtts(text: str, voice_id: str, out_path: Path | None) -> Path | None:
    try:
        from gtts import gTTS
    except ImportError:
        return None
    cfg = VOICE_MAP["gtts"].get(voice_id, VOICE_MAP["gtts"]["narrator"])
    out_path = out_path or Path(f"/tmp/tts_{voice_id}.mp3")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        gTTS(text=text[:2500], lang=cfg["lang"], tld=cfg["tld"],
             slow=cfg["slow"]).save(str(out_path))
        return out_path if out_path.exists() else None
    except Exception:
        return None


def _tts_pyttsx3(text: str, voice_id: str, out_path: Path | None) -> Path | None:
    try:
        import pyttsx3
    except ImportError:
        return None
    cfg = VOICE_MAP["pyttsx3"].get(voice_id, VOICE_MAP["pyttsx3"]["narrator"])
    out_path = out_path or Path(f"/tmp/tts_{voice_id}.wav")
    out_path = out_path.with_suffix(".wav")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices") or []
        if voices and cfg["voice_idx"] < len(voices):
            engine.setProperty("voice", voices[cfg["voice_idx"]].id)
        engine.setProperty("rate", cfg["rate"])
        engine.save_to_file(text[:2500], str(out_path))
        engine.runAndWait()
        return out_path if out_path.exists() else None
    except Exception:
        return None


def _tts_elevenlabs(text: str, voice_id: str, out_path: Path | None) -> Path | None:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        return None
    cfg = VOICE_MAP["elevenlabs"].get(voice_id, VOICE_MAP["elevenlabs"]["narrator"])
    out_path = out_path or Path(f"/tmp/tts_{voice_id}.mp3")
    try:
        import requests
        # Voice name → voice_id lookup
        vlist = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": api_key},
            timeout=30,
        ).json()
        vid = next(
            (v["voice_id"] for v in vlist.get("voices", [])
             if v.get("name", "").lower() == cfg["voice"].lower()),
            None,
        )
        if not vid:
            return None
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            json={"text": text[:2500],
                  "model_id": "eleven_turbo_v2_5",
                  "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}},
            timeout=120,
        )
        if r.status_code != 200:
            return None
        out_path.write_bytes(r.content)
        return out_path
    except Exception:
        return None


def _tts_openai(text: str, voice_id: str, out_path: Path | None) -> Path | None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    cfg = VOICE_MAP["openai_tts"].get(voice_id, VOICE_MAP["openai_tts"]["narrator"])
    out_path = out_path or Path(f"/tmp/tts_{voice_id}.mp3")
    try:
        import requests
        r = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": "tts-1", "voice": cfg["voice"], "input": text[:4000]},
            timeout=120,
        )
        if r.status_code != 200:
            return None
        out_path.write_bytes(r.content)
        return out_path
    except Exception:
        return None


_kokoro_pipeline = None  # cached pipeline (loads model once)


def _tts_kokoro(text: str, voice_id: str, out_path: Path | None) -> Path | None:
    """Kokoro-82M — local neural TTS, fully offline. Produces 24 kHz audio,
    saved as .wav (callers can transcode to .mp3 with moviepy/ffmpeg).
    """
    global _kokoro_pipeline
    try:
        from kokoro import KPipeline  # noqa
        import soundfile as sf
        import numpy as np
    except ImportError:
        return None
    cfg = VOICE_MAP["kokoro"].get(voice_id, VOICE_MAP["kokoro"]["narrator"])
    out_path = out_path or Path(f"/tmp/tts_{voice_id}.wav")
    out_path = out_path.with_suffix(".wav")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if _kokoro_pipeline is None:
            # 'a' = American English. Use 'b' for British, 'p' for prosody.
            _kokoro_pipeline = KPipeline(lang_code="a")
        generator = _kokoro_pipeline(
            text[:5000],
            voice=cfg["voice"],
            speed=cfg.get("speed", 1.0),
        )
        # KPipeline yields (gs, ps, audio_tensor) tuples per chunk
        audio_chunks = []
        for _, _, audio in generator:
            arr = audio.detach().cpu().numpy() if hasattr(audio, "detach") else audio
            audio_chunks.append(arr)
        if not audio_chunks:
            return None
        full = np.concatenate(audio_chunks).astype("float32")
        sf.write(str(out_path), full, samplerate=24000)
        return out_path if out_path.exists() else None
    except Exception:
        return None


def available_backends() -> dict:
    """Probe which backends are usable now."""
    out = {"gtts": False, "pyttsx3": False, "elevenlabs": False,
           "openai_tts": False, "kokoro": False}
    try:
        import gtts  # noqa
        out["gtts"] = True
    except ImportError:
        pass
    try:
        import pyttsx3  # noqa
        out["pyttsx3"] = True
    except ImportError:
        pass
    try:
        import kokoro  # noqa
        out["kokoro"] = True
    except ImportError:
        pass
    out["elevenlabs"] = bool(os.environ.get("ELEVENLABS_API_KEY"))
    out["openai_tts"] = bool(os.environ.get("OPENAI_API_KEY"))
    return out
