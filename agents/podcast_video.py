"""
Script → podcast .mp3 + video .mp4 renderer.

Takes a PodcastScript (from podcast_script.py) and produces:
  - podcast_<hash>.mp3       (audio-only, distributable as podcast)
  - podcast_<hash>.mp4       (video w/ beat-aligned visuals + captions)

Visual cues per turn (script.turns[i].visual):
  null              → keep previous frame (speaker indicator only)
  "title:<text>"    → big title card
  "eq:<latex>"      → equation card (uses matplotlib if available)
  "diagram:<name>"  → diagram placeholder (named concept)
  "graph:<node>"    → graph snapshot — TODO wire to 3D screenshot
  "quote:<id>"      → source-paper quote card

Each turn: synthesize voice (host A or B) → render its visual frame →
clip duration = audio length + 0.4s buffer. Concat → mp4.

Public:
  render(script, voice_backend='auto', force=False) → {'mp3': Path, 'mp4': Path}
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .voices import synthesize

PROJECT_ROOT = Path(__file__).parent.parent
MEDIA_DIR = PROJECT_ROOT / "data" / "sessions" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def render(script: dict, voice_backend: str | None = None,
           style: str = "dark", force: bool = False) -> dict | None:
    """Render a podcast script to mp3 + mp4. Returns paths dict or None."""
    key = _cache_key(script, voice_backend, style)
    mp3_path = MEDIA_DIR / f"podcast_{key}.mp3"
    mp4_path = MEDIA_DIR / f"podcast_{key}.mp4"
    if mp3_path.exists() and mp4_path.exists() and not force:
        return {"mp3": mp3_path, "mp4": mp4_path}

    try:
        from moviepy import (
            ImageClip, AudioFileClip, concatenate_videoclips,
            concatenate_audioclips,
        )
    except ImportError:
        return None
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None

    turns = script.get("turns") or []
    if not turns:
        return None

    # Persistent visual state — last visual carries forward
    last_visual_path: Path | None = None
    img_paths: list[Path] = []
    audio_paths: list[Path] = []
    durations: list[float] = []

    for idx, turn in enumerate(turns):
        speaker = turn.get("speaker", "A")
        text = turn.get("text", "")
        visual = turn.get("visual")
        voice_id = "host_a" if speaker == "A" else "host_b"

        # Audio
        ap = MEDIA_DIR / f"podcast_{key}_t{idx:03d}.mp3"
        if not ap.exists():
            synthesize(text, voice_id=voice_id, out_path=ap, backend=voice_backend)
        if not ap.exists():
            # silent fallback — short pause
            continue
        audio_paths.append(ap)

        # Visual — re-render only if changed
        if visual:
            ip = MEDIA_DIR / f"podcast_{key}_v{idx:03d}.png"
            _render_visual(visual, speaker, ip, style)
            last_visual_path = ip
        else:
            # speaker-indicator overlay on the persistent frame
            if last_visual_path is None:
                last_visual_path = MEDIA_DIR / f"podcast_{key}_v_intro.png"
                _render_visual(f"title:{script.get('title','')}", speaker,
                               last_visual_path, style)
        img_paths.append(last_visual_path)

        # Duration from audio
        try:
            ac = AudioFileClip(str(ap))
            durations.append(max(1.5, ac.duration + 0.3))
            ac.close()
        except Exception:
            durations.append(3.0)

    if not audio_paths:
        return None

    # Stitch audio → mp3
    try:
        audio_clips = [AudioFileClip(str(p)) for p in audio_paths]
        full_audio = concatenate_audioclips(audio_clips)
        full_audio.write_audiofile(str(mp3_path), logger=None)
    except Exception:
        return None

    # Build video
    try:
        clips = []
        for ip, dur in zip(img_paths, durations):
            clips.append(ImageClip(str(ip)).with_duration(dur).with_fps(24))
        video = concatenate_videoclips(clips, method="compose")
        video = video.with_audio(full_audio)
        video.write_videofile(str(mp4_path), fps=24, codec="libx264",
                              audio_codec="aac", logger=None)
    except Exception:
        return {"mp3": mp3_path}

    # cleanup per-turn pngs (keep audio segs for re-runs)
    for p in img_paths:
        try:
            if p.name.startswith(f"podcast_{key}_v"):
                p.unlink()
        except Exception:
            pass

    return {"mp3": mp3_path, "mp4": mp4_path}


# ── Visual rendering ───────────────────────────────────────────────────────

STYLES = {
    "dark": {"bg": (15, 23, 51), "fg": (250, 251, 254),
             "a": (249, 97, 103), "b": (125, 211, 252),
             "accent": (251, 176, 54)},
    "light": {"bg": (255, 255, 255), "fg": (15, 23, 51),
              "a": (200, 50, 50), "b": (40, 110, 180),
              "accent": (180, 110, 0)},
}
CANVAS = (1280, 720)


def _render_visual(visual: str, speaker: str, out: Path, style: str = "dark"):
    """Render a single frame for a visual cue."""
    from PIL import Image, ImageDraw
    pal = STYLES.get(style, STYLES["dark"])
    img = Image.new("RGB", CANVAS, color=pal["bg"])
    draw = ImageDraw.Draw(img)

    # Speaker indicator (left bar)
    bar_color = pal["a"] if speaker == "A" else pal["b"]
    draw.rectangle([(0, 0), (16, CANVAS[1])], fill=bar_color)
    f_small = _font(22)
    draw.text((30, 24), f"HOST {speaker}", font=f_small, fill=bar_color)

    # Parse visual cue
    kind, _, payload = visual.partition(":")
    payload = payload.strip() or visual
    margin = 100

    if kind == "title":
        f = _font(64)
        _wrapped_text(draw, payload, f, pal["accent"], margin, 200, CANVAS[0] - margin * 2, 80)
    elif kind == "eq":
        _render_equation(payload, out, pal)
        return  # _render_equation writes directly
    elif kind == "diagram":
        f_h = _font(28)
        f_b = _font(56)
        draw.text((margin, 180), "DIAGRAM", font=f_h, fill=pal["accent"])
        _wrapped_text(draw, payload, f_b, pal["fg"], margin, 230, CANVAS[0] - margin * 2, 72)
    elif kind == "graph":
        f_h = _font(28)
        f_b = _font(56)
        draw.text((margin, 180), "NODE IN MIND MAP", font=f_h, fill=pal["accent"])
        _wrapped_text(draw, payload, f_b, pal["fg"], margin, 230, CANVAS[0] - margin * 2, 72)
    elif kind == "quote":
        f_h = _font(28)
        f_b = _font(36)
        draw.text((margin, 180), f"SOURCE: {payload}", font=f_h, fill=pal["accent"])
    else:
        f = _font(48)
        _wrapped_text(draw, visual, f, pal["fg"], margin, 250, CANVAS[0] - margin * 2, 60)

    # Brand footer
    draw.rectangle([(0, CANVAS[1] - 40), (CANVAS[0], CANVAS[1])], fill=bar_color)
    draw.text((40, CANVAS[1] - 32), "Brain University · Podcast",
              font=f_small, fill=pal["bg"])
    img.save(out, format="PNG")


def _render_equation(latex: str, out: Path, pal: dict):
    """Render a latex equation. Uses matplotlib if available; else text."""
    from PIL import Image, ImageDraw
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12.8, 7.2),
                               facecolor=tuple(c / 255 for c in pal["bg"]))
        ax.set_facecolor(tuple(c / 255 for c in pal["bg"]))
        ax.axis("off")
        ax.text(0.5, 0.5, f"${latex}$", ha="center", va="center",
                fontsize=48, color=tuple(c / 255 for c in pal["accent"]))
        fig.savefig(str(out), dpi=100, facecolor=fig.get_facecolor())
        plt.close(fig)
        return
    except Exception:
        pass
    # fallback — plain text frame
    img = Image.new("RGB", CANVAS, color=pal["bg"])
    draw = ImageDraw.Draw(img)
    f = _font(40)
    draw.text((100, 320), latex, font=f, fill=pal["accent"])
    img.save(out, format="PNG")


def _font(size: int):
    import os
    from PIL import ImageFont
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrapped_text(draw, text, font, color, x, y, max_w, line_h):
    words = text.split()
    line: list[str] = []
    for w in words:
        trial = " ".join(line + [w])
        bbox = font.getbbox(trial)
        if (bbox[2] - bbox[0]) > max_w and line:
            draw.text((x, y), " ".join(line), font=font, fill=color)
            y += line_h
            line = [w]
        else:
            line.append(w)
    if line:
        draw.text((x, y), " ".join(line), font=font, fill=color)


def _cache_key(script: dict, backend: str | None, style: str) -> str:
    blob = json.dumps({
        "title": script.get("title", ""),
        "n_turns": len(script.get("turns") or []),
        "topic": script.get("topic", ""),
        "backend": backend or "",
        "style": style,
        "first_text": (script.get("turns") or [{}])[0].get("text", "")[:80],
    }, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def cached_paths(script: dict, backend: str | None = None,
                 style: str = "dark") -> dict | None:
    key = _cache_key(script, backend, style)
    mp3 = MEDIA_DIR / f"podcast_{key}.mp3"
    mp4 = MEDIA_DIR / f"podcast_{key}.mp4"
    if mp3.exists() and mp4.exists():
        return {"mp3": mp3, "mp4": mp4}
    if mp3.exists():
        return {"mp3": mp3}
    return None
