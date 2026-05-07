"""
Media helpers — YouTube search + TTS narration for the learning app.

Two paths to "video-ish" content without paying for generative video:

  1. YouTube search (`find_videos`) — scrapes the public watch page with no
     API key. Returns top N results as {title, video_id, channel, duration,
     embed_url, thumbnail}. Embed via st.video or an iframe. Free.

  2. TTS narration (`narrate`) — pyttsx3 (offline, fast, robotic) or gTTS
     (online, natural Google voices, requires internet). Writes mp3 to disk
     and returns the path. Cached per script-hash so re-narrations are free.

Plus an "explainer slides" generator that takes a list of key_ideas + an
optional TTS path and emits an HTML auto-advance slideshow that *feels*
like a watch experience.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).parent.parent
MEDIA_DIR = PROJECT_ROOT / "data" / "sessions" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


# ── YouTube search (no API key) ───────────────────────────────────────────

YT_INITIAL_DATA_RE = re.compile(
    r"var ytInitialData = ({.*?});\s*</script>", re.DOTALL,
)


def _yt_extract(html: str, k: int) -> list[dict]:
    """Pull video results out of YouTube's initial data blob."""
    m = YT_INITIAL_DATA_RE.search(html)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return []
    out: list[dict] = []
    # Walk the contents tree looking for videoRenderer entries
    def walk(obj):
        if isinstance(obj, dict):
            if "videoRenderer" in obj:
                vr = obj["videoRenderer"]
                vid = vr.get("videoId")
                title_runs = (vr.get("title") or {}).get("runs") or []
                title = "".join(r.get("text", "") for r in title_runs)
                channel_runs = ((vr.get("ownerText") or {}).get("runs") or [])
                channel = "".join(r.get("text", "") for r in channel_runs)
                duration = (vr.get("lengthText") or {}).get("simpleText", "")
                thumbnails = ((vr.get("thumbnail") or {}).get("thumbnails") or [])
                thumb = thumbnails[-1]["url"] if thumbnails else ""
                if vid and title:
                    out.append({
                        "video_id": vid,
                        "title":    title,
                        "channel":  channel,
                        "duration": duration,
                        "thumbnail": thumb,
                        "embed_url": f"https://www.youtube.com/embed/{vid}",
                        "watch_url": f"https://www.youtube.com/watch?v={vid}",
                    })
                    if len(out) >= k:
                        return
            for v in obj.values():
                if len(out) >= k:
                    return
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                if len(out) >= k:
                    return
                walk(v)
    walk(data)
    return out[:k]


def find_videos(topic: str, k: int = 4) -> list[dict]:
    """Search YouTube for `topic`. Returns up to k video metadata dicts.

    No API key required (scrapes the public search page). YouTube changes
    its markup occasionally — best-effort. Caches per-topic for 1 day.
    """
    cache_path = MEDIA_DIR / f"yt_{_safe_slug(topic)}.json"
    if cache_path.exists():
        try:
            blob = json.loads(cache_path.read_text())
            if blob.get("results"):
                return blob["results"][:k]
        except json.JSONDecodeError:
            pass

    try:
        import urllib.request as _u
        url = f"https://www.youtube.com/results?search_query={quote_plus(topic)}"
        req = _u.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120",
            "Accept-Language": "en-US,en;q=0.9",
        })
        with _u.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
        results = _yt_extract(html, k)
    except Exception:
        results = []

    if results:
        cache_path.write_text(json.dumps({"results": results}, indent=2))
    return results


def _safe_slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower())[:64]


# ── TTS narration ─────────────────────────────────────────────────────────

def narrate(text: str, voice: str = "auto") -> Path | None:
    """Generate an mp3/wav narration of `text`. Cached per text-hash.

    voice ∈ {"auto", "gtts", "pyttsx3"}. auto = gtts if online, else pyttsx3.
    Returns Path to the audio file or None on failure.
    """
    if not text or not text.strip():
        return None
    h = hashlib.sha1(text.encode()).hexdigest()[:16]
    if voice == "pyttsx3":
        out = MEDIA_DIR / f"tts_{h}.wav"
    else:
        out = MEDIA_DIR / f"tts_{h}.mp3"
    if out.exists():
        return out

    if voice in ("auto", "gtts"):
        # gTTS = online, natural voices
        try:
            from gtts import gTTS
            gTTS(text=text, lang="en", slow=False).save(str(out))
            return out
        except Exception:
            if voice == "gtts":
                return None
            # else fall through to pyttsx3

    # pyttsx3 = offline, robotic but reliable
    try:
        import pyttsx3
        eng = pyttsx3.init()
        eng.setProperty("rate", 175)
        out = MEDIA_DIR / f"tts_{h}.wav"
        eng.save_to_file(text, str(out))
        eng.runAndWait()
        return out if out.exists() else None
    except Exception:
        return None


def narration_script(lesson: dict) -> str:
    """Compose a narration script from a lesson dict."""
    parts = [f"Today's topic: {lesson.get('title', '')}.",
             lesson.get("summary", "")]
    if lesson.get("key_ideas"):
        parts.append("Key ideas to remember.")
        for k in lesson["key_ideas"][:5]:
            parts.append(k)
    if lesson.get("worked_example"):
        parts.append(f"Here's a worked example. {lesson['worked_example']}")
    if lesson.get("engagement_question"):
        parts.append(f"Something to think about: {lesson['engagement_question']}")
    return " ".join(p.strip() for p in parts if p and p.strip())


# ── Explainer slides (HTML auto-advance) ──────────────────────────────────

def slides_html(lesson: dict, audio_url: str | None = None,
                seconds_per_slide: int = 7) -> str:
    """Generate a self-contained HTML auto-advance slideshow.

    Each key_idea = one slide. Bottom progress bar, prev/next buttons.
    Optional inline audio player if audio_url given.
    """
    title = lesson.get("title", "")
    summary = lesson.get("summary", "")
    ideas   = lesson.get("key_ideas", []) or []
    worked  = lesson.get("worked_example") or ""
    engage  = lesson.get("engagement_question") or ""

    slides = [{"head": "📖 Today", "body": f"<h2>{title}</h2><p>{summary}</p>"}]
    for i, idea in enumerate(ideas[:6], 1):
        slides.append({"head": f"💡 Idea {i}", "body": f"<p>{idea}</p>"})
    if worked:
        slides.append({"head": "🧮 Worked example", "body": f"<p>{worked}</p>"})
    if engage:
        slides.append({"head": "🤔 Reflect", "body": f"<p><em>{engage}</em></p>"})

    audio_block = ""
    if audio_url:
        audio_block = (
            f'<audio id="aud" controls autoplay style="width:100%;'
            f'margin-top:14px;"><source src="{audio_url}"></audio>'
        )

    slides_json = json.dumps(slides)
    return f"""
<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
  body {{ margin:0; font-family: -apple-system, system-ui, sans-serif;
          background:#0F1733; color:#FAFBFE; padding:0; }}
  .deck {{ height:480px; padding:24px 36px; box-sizing:border-box;
           display:flex; flex-direction:column; }}
  .head {{ font-size:13px; color:#FBB036; letter-spacing:0.05em;
           text-transform: uppercase; margin-bottom:6px; }}
  .body {{ flex:1; font-size:18px; line-height:1.5;
           padding:14px 4px; }}
  .body h2 {{ font-size:30px; margin:0 0 12px 0; color:#F96167; }}
  .body p  {{ margin:0; max-width:760px; }}
  .bar {{ height:4px; background:#1E2761; border-radius:2px; }}
  .fill {{ height:4px; background:#F96167; width:0%;
           transition: width .25s linear; border-radius:2px; }}
  .nav {{ margin-top:14px; display:flex; gap:10px; align-items:center; }}
  button {{ background:#1E2761; color:#FAFBFE; border:1px solid #3B5BA5;
            padding:6px 14px; border-radius:6px; cursor:pointer;
            font-family: inherit; font-size:13px; }}
  button:hover {{ background:#3B5BA5; }}
  .ctr {{ font-size:12px; color:#7DD3FC; margin-left:auto; }}
</style></head>
<body>
<div class="deck">
  <div class="head" id="head"></div>
  <div class="body" id="body"></div>
  <div class="bar"><div class="fill" id="fill"></div></div>
  <div class="nav">
    <button onclick="step(-1)">‹ Prev</button>
    <button onclick="step(1)">Next ›</button>
    <button onclick="toggle()" id="play">⏸ Pause</button>
    <span class="ctr" id="ctr"></span>
  </div>
  {audio_block}
</div>
<script>
  const slides = {slides_json};
  const SECS = {seconds_per_slide};
  let i = 0; let playing = true; let elapsed = 0;
  function render() {{
    document.getElementById('head').innerText = slides[i].head;
    document.getElementById('body').innerHTML = slides[i].body;
    document.getElementById('ctr').innerText = (i+1)+' / '+slides.length;
  }}
  function step(d) {{
    i = (i + d + slides.length) % slides.length;
    elapsed = 0; render();
  }}
  function toggle() {{
    playing = !playing;
    document.getElementById('play').innerText = playing ? '⏸ Pause' : '▶ Play';
  }}
  setInterval(() => {{
    if (!playing) return;
    elapsed += 0.1;
    document.getElementById('fill').style.width =
      Math.min(100, 100 * elapsed / SECS) + '%';
    if (elapsed >= SECS) {{ elapsed = 0; i = (i+1) % slides.length; render();
      document.getElementById('fill').style.width = '0%'; }}
  }}, 100);
  render();
</script>
</body></html>"""
