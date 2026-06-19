# Plan 01 — ElevenLabs TTS + burn-in captions

**Status:** designed, not yet implemented
**Touches:** `agents/video_generator.py`, `agents/podcast_generator.py`,
new module `agents/tts.py`
**Estimated effort:** ~1 engineer-week

---

## Why

gTTS is the single biggest "this feels like 2014" tell in the current
video output. Replacing it with a modern neural voice (ElevenLabs,
Cartesia, OpenAI, Google Studio voices) is the highest-impact single
change for perceived quality. Captions are the cheap accessibility +
search-inside-video win that lands at the same time.

## Scope

In:
1. New unified TTS facade — `agents/tts.py` with `synthesize(text, *, voice, provider) → bytes` plus a `providers_ready()` probe.
2. ElevenLabs adapter (default when `ELEVENLABS_API_KEY` is set).
3. OpenAI TTS adapter (default when `OPENAI_API_KEY` is set).
4. Existing gTTS + pyttsx3 stay as the offline fallback chain.
5. SSML pass for ElevenLabs (`<break>`, `<emphasis>`, prosody).
6. Whisper-based caption generation per audio segment (word-level timestamps).
7. Burn-in captions on the PIL slide renderer (lower-third strip, auto-wrap, contrast-checked).
8. Plumb the new facade into both `agents/video_generator.py` and `agents/podcast_generator.py`.

Out (deferred):
- Voice cloning / cloned company-brand narrator (Phase 2).
- Subtitles as a sidecar `.vtt` track instead of burned-in (Phase 2).
- Translation of captions for i18n (Phase 6).

## API surface

```python
# agents/tts.py

def synthesize(
    text: str,
    *,
    voice:    str = "auto",      # 'auto' | 'gtts' | 'elevenlabs:<voice_id>' | 'openai:<voice>'
    provider: str = "auto",      # 'auto' picks first available
    out_path: Path | None = None,
    ssml:     bool = False,
) -> Path | None:
    """Render text to audio. Returns mp3 path or None."""

def providers_ready() -> dict[str, bool]:
    """{'elevenlabs': bool, 'openai': bool, 'gtts': bool, 'pyttsx3': bool}"""

def transcribe_with_timestamps(audio_path: Path) -> list[dict]:
    """Word-level timestamps: [{'word': str, 't_start': float, 't_end': float}]"""
```

## Data shape

Each rendered video also writes a sidecar `.captions.json`:

```json
[
  {"slide_idx": 1, "t_start": 0.0, "t_end": 2.4, "text": "Today we'll cover backpropagation."},
  {"slide_idx": 1, "t_start": 2.4, "t_end": 4.1, "text": "It's the algorithm that..."}
]
```

## Migration path

1. Add `agents/tts.py` with all four providers behind a single `synthesize()`.
2. Refactor `agents/video_generator.py::_narrate_segment` to call `tts.synthesize(...)` instead of inlining gTTS. Caching key already includes `voice`; extend it to include `provider`.
3. Add `BURN_CAPTIONS=true` env flag. When on, after rendering each slide PNG, overlay caption text in the bottom 1/6 of the frame using a contrast-checked color from the active style palette.
4. Update `stack_ready()` to include the new provider checks.
5. Default behavior: if no neural provider key is set, fall back to gTTS (no breaking change).
6. Update README's "Run" section to mention the optional env keys.

## Fallback / failure modes

- ElevenLabs 429 or 5xx → automatic single-retry with backoff, then fall to OpenAI, then gTTS.
- Whisper unavailable → captions disabled silently; video still renders.
- Caption text wider than 90% of frame → auto-shrink font; if still too wide, wrap to 2 lines.

## Acceptance checks

- [ ] Same lesson dict, with `ELEVENLABS_API_KEY` set, renders a video whose audio is recognisably ElevenLabs (manual ear test on a golden lesson).
- [ ] Same lesson dict with no API keys still renders via gTTS without error.
- [ ] `BURN_CAPTIONS=true` produces a video where captions sync to ±0.3s of the spoken word (Whisper timestamp comparison).
- [ ] No regression on cache hits: re-running with identical args returns the cached path in <100ms.
- [ ] Cost guardrail: a single 6-slide lesson rendered with ElevenLabs costs <$0.15 (log + assert).

## Risks

- ElevenLabs pricing — at scale this could be the largest line item; gate behind per-day cap.
- Whisper local model takes ~3GB RAM; offer Whisper API as alternative.
- Caption burn-in changes the PIL renderer's layout — must be opt-in for the first release.
