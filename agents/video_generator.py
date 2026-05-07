"""
Programmatic text→video generator for Brain University.

Free, deterministic, edu-fit. Each lesson becomes a Khan-Academy-tier
mp4: title slide → key idea slides → worked example → reflection. Each
slide is a PIL-rendered 1280×720 frame paired with gTTS narration; the
stack is then stitched together by moviepy into a single mp4.

Output:
  data/sessions/media/video_<hash>.mp4

Caching:
  Hash = sha1(json.dumps(lesson, sorted_keys) + voice + style)
  If the mp4 already exists for that hash, return its path immediately.

Public:
  generate(lesson, voice='auto', style='dark', force=False) → Path | None
  cached_path_for(lesson, voice, style)                      → Path | None  (no I/O if absent)

Heavy dependencies are imported lazily so the rest of the app keeps
working when moviepy / gTTS aren't installed; in that case generate()
returns None and the caller can show a friendly install hint.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import textwrap
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
MEDIA_DIR = PROJECT_ROOT / "data" / "sessions" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


# ── Style ─────────────────────────────────────────────────────────────────

STYLES = {
    "dark": {
        "bg":         (15, 23, 51),       # #0F1733
        "title":      (249, 97, 103),     # #F96167 coral
        "header":     (251, 176, 54),     # #FBB036 amber
        "body":       (250, 251, 254),    # #FAFBFE
        "caption":    (125, 211, 252),    # #7DD3FC sky
        "accent":     (30, 39, 97),       # #1E2761 navy
    },
    "light": {
        "bg":         (255, 255, 255),
        "title":      (200, 50, 50),
        "header":     (180, 110, 0),
        "body":       (15, 23, 51),
        "caption":    (40, 110, 180),
        "accent":     (220, 220, 235),
    },
}

CANVAS = (1280, 720)


# ── Font loader (best-effort across platforms) ────────────────────────────

def _font(size: int):
    """Return a TTF font; falls back to PIL default at the requested size."""
    from PIL import ImageFont
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Helvetica.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ── Slide rendering ───────────────────────────────────────────────────────

def _wrap(text: str, font, max_width_px: int) -> list[str]:
    """Word-wrap text to fit max_width_px under `font`."""
    if not text:
        return [""]
    words = text.split()
    out: list[str] = []
    line: list[str] = []
    for w in words:
        trial = (" ".join(line + [w]))
        bbox = font.getbbox(trial)
        if bbox[2] - bbox[0] > max_width_px and line:
            out.append(" ".join(line))
            line = [w]
        else:
            line.append(w)
    if line:
        out.append(" ".join(line))
    return out


def _render_slide(*, head: str, body: str, kind: str, style: dict,
                   slide_num: int, total: int):
    """Render one frame as a PIL.Image."""
    from PIL import Image, ImageDraw

    img = Image.new("RGB", CANVAS, color=style["bg"])
    draw = ImageDraw.Draw(img)

    # Header strip
    draw.rectangle([(0, 0), (CANVAS[0], 64)], fill=style["accent"])
    f_caption = _font(20)
    draw.text((40, 22), head.upper(), font=f_caption, fill=style["caption"])

    # Slide counter
    counter = f"{slide_num} / {total}"
    cb = f_caption.getbbox(counter)
    draw.text((CANVAS[0] - 40 - (cb[2] - cb[0]), 22),
               counter, font=f_caption, fill=style["caption"])

    # Body
    margin = 80
    cy = 130
    if kind == "title":
        f = _font(72)
        for ln in _wrap(body, f, CANVAS[0] - margin * 2):
            draw.text((margin, cy), ln, font=f, fill=style["title"])
            cy += 86
    elif kind == "key_idea":
        f_h = _font(40)
        f_b = _font(36)
        # First line bigger, rest smaller — let the body shape itself
        lines = body.split("\n", 1)
        first, rest = lines[0], lines[1] if len(lines) > 1 else ""
        for ln in _wrap(first, f_h, CANVAS[0] - margin * 2):
            draw.text((margin, cy), ln, font=f_h, fill=style["header"])
            cy += 58
        if rest:
            cy += 14
            for ln in _wrap(rest, f_b, CANVAS[0] - margin * 2):
                draw.text((margin, cy), ln, font=f_b, fill=style["body"])
                cy += 50
    else:  # body / worked / reflect
        f = _font(34)
        for ln in _wrap(body, f, CANVAS[0] - margin * 2):
            draw.text((margin, cy), ln, font=f, fill=style["body"])
            cy += 48
            if cy > CANVAS[1] - 90:
                draw.text((margin, cy), "…", font=f, fill=style["caption"])
                break

    # Footer brand strip
    draw.rectangle([(0, CANVAS[1] - 36), (CANVAS[0], CANVAS[1])],
                   fill=style["accent"])
    draw.text((40, CANVAS[1] - 30), "🎓 Brain University", font=f_caption,
               fill=style["caption"])

    return img


# ── Slide planning ────────────────────────────────────────────────────────

def _plan_slides(lesson: dict) -> list[dict]:
    """Convert a lesson dict into an ordered slide spec."""
    slides: list[dict] = [{
        "head": "Today's topic",
        "kind": "title",
        "text": lesson.get("title", "?"),
        "narrate": f"Today we'll cover {lesson.get('title', 'this topic')}.",
    }]
    if lesson.get("summary"):
        slides.append({
            "head": "Why it matters",
            "kind": "body",
            "text": lesson["summary"],
            "narrate": lesson["summary"],
        })
    for i, idea in enumerate(lesson.get("key_ideas") or [], 1):
        slides.append({
            "head": f"Key idea {i}",
            "kind": "key_idea",
            "text": idea,
            "narrate": idea,
        })
    if lesson.get("worked_example"):
        slides.append({
            "head": "Worked example",
            "kind": "body",
            "text": lesson["worked_example"],
            "narrate": "Here's a worked example. " + lesson["worked_example"],
        })
    if lesson.get("engagement_question"):
        slides.append({
            "head": "Reflect",
            "kind": "body",
            "text": lesson["engagement_question"],
            "narrate": "Something to think about: " + lesson["engagement_question"],
        })
    slides.append({
        "head": "End of lesson",
        "kind": "title",
        "text": "Keep exploring.",
        "narrate": "That wraps up this lesson. Keep exploring.",
    })
    return slides


# ── Cache helpers ─────────────────────────────────────────────────────────

def _cache_key(lesson: dict, voice: str, style: str) -> str:
    blob = json.dumps({
        "title":   lesson.get("title", ""),
        "summary": lesson.get("summary", ""),
        "ideas":   lesson.get("key_ideas") or [],
        "worked":  lesson.get("worked_example") or "",
        "engage":  lesson.get("engagement_question") or "",
        "voice":   voice,
        "style":   style,
    }, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def _cache_path(key: str) -> Path:
    return MEDIA_DIR / f"video_{key}.mp4"


def cached_path_for(lesson: dict, voice: str = "auto",
                    style: str = "dark") -> Path | None:
    p = _cache_path(_cache_key(lesson, voice, style))
    return p if p.exists() else None


# ── Audio generation ──────────────────────────────────────────────────────

def _narrate_segment(text: str, idx: int, key: str, voice: str) -> Path | None:
    """Generate audio for one slide. Returns mp3 path or None."""
    if not text or not text.strip():
        return None
    out = MEDIA_DIR / f"video_{key}_seg_{idx:02d}.mp3"
    if out.exists():
        return out
    # gTTS first
    if voice in ("auto", "gtts"):
        try:
            from gtts import gTTS
            gTTS(text=text[:1500], lang="en", slow=False).save(str(out))
            return out
        except Exception:
            if voice == "gtts":
                return None
    # pyttsx3 fallback
    try:
        import pyttsx3
        out_wav = out.with_suffix(".wav")
        eng = pyttsx3.init()
        eng.setProperty("rate", 175)
        eng.save_to_file(text[:1500], str(out_wav))
        eng.runAndWait()
        return out_wav if out_wav.exists() else None
    except Exception:
        return None


# ── Main pipeline ─────────────────────────────────────────────────────────

def generate(lesson: dict, voice: str = "auto", style: str = "dark",
             force: bool = False, fps: int = 24,
             min_seconds_per_slide: float = 3.5,
             max_seconds_per_slide: float = 12.0,
             progress_cb=None) -> Path | None:
    """Render a lesson dict to an mp4. Cached. Returns Path or None."""
    key = _cache_key(lesson, voice, style)
    out_path = _cache_path(key)
    if out_path.exists() and not force:
        return out_path

    # Lazy imports — failure here returns None (caller shows install hint)
    try:
        from PIL import Image  # noqa
        from moviepy import (
            ImageClip, AudioFileClip, concatenate_videoclips,
            concatenate_audioclips, CompositeAudioClip, AudioArrayClip,
        )
    except ImportError:
        return None

    style_pal = STYLES.get(style, STYLES["dark"])
    slides = _plan_slides(lesson)
    total = len(slides)

    # Render each slide image to disk so moviepy can stream them
    img_paths: list[Path] = []
    audio_paths: list[Path | None] = []
    durations: list[float] = []
    for i, sl in enumerate(slides, 1):
        if progress_cb:
            try:
                progress_cb(("render_slide", i, total))
            except Exception:
                pass
        img = _render_slide(
            head=sl["head"], body=sl["text"], kind=sl["kind"],
            style=style_pal, slide_num=i, total=total,
        )
        ip = MEDIA_DIR / f"video_{key}_slide_{i:02d}.png"
        img.save(ip, format="PNG")
        img_paths.append(ip)

        # Narrate
        if progress_cb:
            try:
                progress_cb(("narrate_slide", i, total))
            except Exception:
                pass
        ap = _narrate_segment(sl["narrate"], i, key, voice)
        audio_paths.append(ap)

        # Duration: audio length + 0.6s breathing room, clamped
        if ap and ap.exists():
            try:
                ac = AudioFileClip(str(ap))
                dur = max(min_seconds_per_slide,
                           min(max_seconds_per_slide, ac.duration + 0.6))
                ac.close()
            except Exception:
                dur = min_seconds_per_slide
        else:
            dur = min_seconds_per_slide
        durations.append(dur)

    # Build video clips
    clips = []
    for ip, dur in zip(img_paths, durations):
        clip = ImageClip(str(ip)).with_duration(dur).with_fps(fps)
        clips.append(clip)
    if not clips:
        return None
    if progress_cb:
        try:
            progress_cb(("stitching", 1, 1))
        except Exception:
            pass
    video = concatenate_videoclips(clips, method="compose")

    # Build audio track — concatenate, padding silence to match clip durations
    audio_clips = []
    for ap, dur in zip(audio_paths, durations):
        if ap and ap.exists():
            try:
                a = AudioFileClip(str(ap))
                if a.duration > dur:
                    a = a.subclipped(0, dur)
                # pad silence after audio if shorter than slide
                if a.duration < dur:
                    pad = _silence_clip(dur - a.duration)
                    a = concatenate_audioclips([a, pad]) if pad else a
                audio_clips.append(a)
            except Exception:
                audio_clips.append(_silence_clip(dur))
        else:
            sil = _silence_clip(dur)
            if sil:
                audio_clips.append(sil)

    if audio_clips:
        try:
            audio = concatenate_audioclips(audio_clips)
            video = video.with_audio(audio)
        except Exception:
            pass

    # Encode mp4
    if progress_cb:
        try:
            progress_cb(("encoding", 1, 1))
        except Exception:
            pass
    try:
        video.write_videofile(
            str(out_path),
            fps=fps,
            codec="libx264",
            audio_codec="aac",
            logger=None,
        )
    except Exception:
        return None
    finally:
        try:
            video.close()
        except Exception:
            pass

    # Clean up per-slide pngs (keep audio segs — they're tiny + reusable)
    for ip in img_paths:
        try:
            ip.unlink()
        except Exception:
            pass

    return out_path if out_path.exists() else None


def _silence_clip(seconds: float):
    """Return a silent AudioClip for padding. Best-effort."""
    try:
        from moviepy import AudioArrayClip
        import numpy as np
        rate = 22050
        n = max(1, int(seconds * rate))
        arr = np.zeros((n, 2), dtype=float)
        return AudioArrayClip(arr, fps=rate)
    except Exception:
        return None


# ── Convenience: probe whether the stack is usable ────────────────────────

def stack_ready() -> dict:
    """Report whether each dependency is importable. UI uses this to show
    a 'install foo' hint before triggering generate()."""
    out = {"PIL": False, "moviepy": False, "gtts": False, "pyttsx3": False,
           "ffmpeg": False}
    try:
        import PIL
        out["PIL"] = True
    except ImportError:
        pass
    try:
        import moviepy  # noqa
        out["moviepy"] = True
    except ImportError:
        pass
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
        import imageio_ffmpeg
        if Path(imageio_ffmpeg.get_ffmpeg_exe()).exists():
            out["ffmpeg"] = True
    except Exception:
        pass
    return out
