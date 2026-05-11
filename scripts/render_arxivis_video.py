"""
arXivis paper video generator.

Output per paper: 9:16 portrait mp4 (720x1280), ~12s, black background,
cyan/teal palette, big green callouts — mimics the @joshuaaalampour
protein-viz aesthetic supplied as reference.

Scenes (12s @ 24fps = 288 frames):
  A. 0.0 – 2.5s : title card — source badge, paper title, fade in.
  B. 2.5 – 7.0s : 3D rotating subgraph of activated concepts +
                  big green callout "N concepts activated".
  C. 7.0 – 10.0s: innovation panel — cycle through top 3 named
                  innovations w/ "proposes" / "connects" pills.
  D. 10.0 – 12s : novelty card — huge green bits number, pitch line.

Frames are rendered with PIL only (no matplotlib / moviepy / cairo).
Frames are stitched into mp4 via ffmpeg.

Usage:
  python3 scripts/render_arxivis_video.py                # top 10 papers
  python3 scripts/render_arxivis_video.py --top 30
  python3 scripts/render_arxivis_video.py --paper-id arx:2602.14625v1
  python3 scripts/render_arxivis_video.py --paper-id <id> --no-cleanup

Outputs:
  design/videos/<sanitised-id>.mp4
  design/videos/manifest.js       (window.ARXIVIS_VIDEOS map)
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import networkx as nx

ARXIVIS_JS  = PROJECT_ROOT / "design" / "arxivis_data.js"
VIDEOS_DIR  = PROJECT_ROOT / "design" / "videos"
MANIFEST_JS = VIDEOS_DIR / "manifest.js"

# ── Style — mirrors the protein-viz reference ────────────────────────────
W, H        = 720, 1280
FPS         = 24
DURATION_S  = 12
TOTAL_FRAMES = FPS * DURATION_S

BG_COLOR    = (0, 0, 0)
INK_BRIGHT  = (245, 247, 251)
INK_DIM     = (155, 168, 195)
CYAN        = (60, 200, 230)      # primary structure colour
CYAN_GLOW   = (90, 220, 250)
TEAL        = (40, 160, 180)
GREEN       = (96, 255, 168)      # callout accent (big numbers)
GREEN_DIM   = (62, 200, 135)
AMBER       = (251, 176, 54)      # secondary callout
CORAL       = (249, 97, 103)

# ── Fonts ────────────────────────────────────────────────────────────────

def load_font(size: int, mono: bool = False, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    candidates = []
    if mono:
        candidates = [
            "/System/Library/Fonts/SFNSMono.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/Monaco.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "/Library/Fonts/Arial.ttf",
        ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ── Data loader ──────────────────────────────────────────────────────────

def load_papers() -> list[dict]:
    text = ARXIVIS_JS.read_text()
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start: end + 1])["papers"]


# ── 3D layout helpers ────────────────────────────────────────────────────

def layout_3d(paper: dict) -> dict[str, tuple[float, float, float]]:
    """spring-layout the activated concept subgraph in 3D."""
    G = nx.Graph()
    for c in paper["concepts"]:
        G.add_node(c["id"], weight=c["weight"], name=c["name"])
    for a, b in paper["pair_edges"]:
        if a in G and b in G:
            G.add_edge(a, b)
    if G.number_of_nodes() == 0:
        return {}
    if G.number_of_nodes() == 1:
        n = next(iter(G.nodes))
        return {n: (0.0, 0.0, 0.0)}
    pos = nx.spring_layout(G, dim=3, seed=7, k=1.6 / math.sqrt(G.number_of_nodes()))
    # Normalize into unit sphere
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    zs = [p[2] for p in pos.values()]
    mx, my, mz = sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)
    cx, cy, cz = (max(xs)-min(xs)) or 1, (max(ys)-min(ys)) or 1, (max(zs)-min(zs)) or 1
    s = 0.65 / max(cx, cy, cz)
    return {n: ((x-mx)*s, (y-my)*s, (z-mz)*s) for n,(x,y,z) in pos.items()}


def project(p, theta, scale=320, cx=W/2, cy=H/2):
    """Rotate around Y, perspective-project onto 2D."""
    x, y, z = p
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    xr = x * cos_t - z * sin_t
    zr = x * sin_t + z * cos_t
    persp = 1 / (1.4 - zr * 0.7)
    sx = cx + xr * scale * persp
    sy = cy + y * scale * persp
    return sx, sy, persp


# ── Text helpers ─────────────────────────────────────────────────────────

def fit_text(draw, text, font, max_w):
    """Greedy word-wrap to max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if draw.textlength(candidate, font=font) > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = candidate
    if cur:
        lines.append(cur)
    return lines


def draw_text_center(img: Image.Image, text: str, font, y: int, color, max_w=W-80):
    draw = ImageDraw.Draw(img)
    for line in fit_text(draw, text, font, max_w):
        w = draw.textlength(line, font=font)
        draw.text(((W - w) / 2, y), line, font=font, fill=color)
        y += font.size + 6
    return y


def draw_pill(img: Image.Image, text: str, font, cx: int, cy: int,
              fill_color, text_color, pad_x=14, pad_y=6):
    draw = ImageDraw.Draw(img)
    tw = draw.textlength(text, font=font)
    th = font.size
    x0, y0 = cx - tw/2 - pad_x, cy - th/2 - pad_y
    x1, y1 = cx + tw/2 + pad_x, cy + th/2 + pad_y
    draw.rounded_rectangle([x0, y0, x1, y1], radius=th, fill=fill_color)
    draw.text((cx - tw/2, cy - th/2), text, font=font, fill=text_color)


# ── Source badge color ───────────────────────────────────────────────────

def badge_for(source: str):
    s = (source or "").upper()
    if "ARXIV" in s:    return CYAN
    if "NTRS" in s:     return AMBER
    if "DTIC" in s:     return CORAL
    if "OPENALEX" in s: return GREEN
    return INK_DIM


# ── Frame renderers ──────────────────────────────────────────────────────

def render_scene_title(t_in_scene: float, paper: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    # Fade-in alpha
    alpha = max(0.0, min(1.0, t_in_scene / 1.0))
    ink = tuple(int(c * alpha) for c in INK_BRIGHT)
    dim = tuple(int(c * alpha) for c in INK_DIM)
    badge = tuple(int(c * alpha) for c in badge_for(paper["source"]))

    fm_mono   = load_font(20, mono=True)
    fm_h1     = load_font(46)
    fm_meta   = load_font(18)

    badge_text = f"{paper['source']}{'  ·  ' + str(paper['year']) if paper.get('year') else ''}"
    draw_pill(img, badge_text, fm_mono, W/2, 220, badge, BG_COLOR)

    title = paper["title"]
    draw_text_center(img, title, fm_h1, 300, ink)

    tagline = "see through the hype · 30-second grok"
    draw_text_center(img, tagline.upper(), fm_meta, H - 200, dim)

    # arXivis brand
    fm_brand = load_font(28, mono=True)
    draw_text_center(img, "arXivis", fm_brand, H - 120, badge)
    return img


def render_scene_structure(t_in_scene: float, paper: dict, positions: dict) -> Image.Image:
    """Rotating 3D graph of activated concepts."""
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    theta = t_in_scene * 0.5 + 0.3  # slow rotation
    # Sort nodes by z so back-facing draw first
    items = []
    for n, p3 in positions.items():
        sx, sy, persp = project(p3, theta, scale=300, cy=H/2 - 60)
        items.append((persp, n, sx, sy))
    items.sort(key=lambda t: t[0])

    # Draw edges
    pos_2d = {n: (sx, sy, persp) for persp, n, sx, sy in items}
    for a, b in paper["pair_edges"]:
        if a in pos_2d and b in pos_2d:
            x1, y1, _ = pos_2d[a]
            x2, y2, _ = pos_2d[b]
            # Edge color: dim cyan; brighter for in-front edges
            draw.line([(x1, y1), (x2, y2)], fill=(35, 95, 110), width=1)

    # Draw nodes
    fm_label = load_font(13, mono=True)
    for persp, n, sx, sy in items:
        # Bigger when in front
        r = 6 + int(persp * 8)
        # Glow halo
        for k in range(3, 0, -1):
            a = 30 - 8 * k
            draw.ellipse([sx-r-k*2, sy-r-k*2, sx+r+k*2, sy+r+k*2],
                         fill=(0, 60, 80))
        draw.ellipse([sx-r, sy-r, sx+r, sy+r], fill=CYAN_GLOW)
        draw.ellipse([sx-r+2, sy-r+2, sx+r-2, sy+r-2], fill=CYAN)

    # Top callout
    n_concepts = len(paper["concepts"])
    fm_giant = load_font(110)
    fm_meta  = load_font(22, mono=True)
    draw_text_center(img, str(n_concepts), fm_giant, 60, GREEN)
    label = "CONCEPTS ACTIVATED"
    draw_text_center(img, label, fm_meta, 195, GREEN_DIM)

    # Bottom strip: top 3 concept names
    fm_small = load_font(17, mono=True)
    top3 = " · ".join(c["name"] for c in paper["concepts"][:3])
    draw_text_center(img, top3.upper(), fm_small, H - 220, INK_DIM, max_w=W-80)

    pair_count = len(paper["pair_edges"])
    fm_chip = load_font(14, mono=True)
    draw_pill(img, f"{pair_count} concept-pair edges",
              fm_chip, W/2, H - 160, (12, 28, 38), CYAN_GLOW)

    return img


def render_scene_innovations(t_in_scene: float, paper: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_COLOR)
    innovs = paper.get("innovations", [])[:3]
    if not innovs:
        # fall back to top concepts
        innovs = [{"phrase": c["name"], "kind": "connects",
                   "pattern": "concept", "connects_to": [c["id"]]}
                  for c in paper["concepts"][:3]]

    # Title
    fm_meta  = load_font(20, mono=True)
    fm_card  = load_font(30)
    fm_chip  = load_font(15, mono=True)

    draw_text_center(img, "WHAT'S NEW", fm_meta, 110, GREEN_DIM)

    # Reveal innovations one at a time (~1 second each)
    n_visible = min(len(innovs), int(t_in_scene / 0.9) + 1)
    y = 200
    for i, innov in enumerate(innovs[:n_visible]):
        phrase = innov["phrase"]
        if len(phrase) > 90: phrase = phrase[:88] + "…"
        kind = innov["kind"]
        kind_color = GREEN if kind == "proposes" else CYAN
        # Pill
        draw_pill(img, kind.upper(), fm_chip, 100, y + 30, kind_color, BG_COLOR)
        # Card body
        draw_text_center(img, phrase, fm_card, y + 70, INK_BRIGHT, max_w=W-80)
        # If connects, show targets
        if innov.get("connects_to"):
            connects_txt = "→ " + " · ".join(c.replace("wiki:", "")[:24]
                                              for c in innov["connects_to"][:2])
            draw_text_center(img, connects_txt.replace("_", " "),
                             fm_chip, y + 170, INK_DIM)
        y += 260

    return img


def render_scene_novelty(t_in_scene: float, paper: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), BG_COLOR)
    fm_giant  = load_font(160)
    fm_meta   = load_font(20, mono=True)
    fm_body   = load_font(22)

    # Big bits number, animated count-up
    bits_final = paper["novelty_bits"]
    progress = min(1.0, t_in_scene / 1.0)
    bits_now = bits_final * progress
    draw_text_center(img, f"{bits_now:.1f}", fm_giant, 200, GREEN)
    draw_text_center(img, "NOVELTY · BITS", fm_meta, 405, GREEN_DIM)

    # Breakdown chips
    bd = paper["novelty_breakdown"]
    fm_chip = load_font(15, mono=True)
    chips = [
        (f"concept rarity {bd.get('concept_bits',0):.1f}",   CYAN),
        (f"new edges {bd.get('edge_bits',0):.1f}",            GREEN),
        (f"innovations {bd.get('innovation_bonus',0):.1f}",   AMBER),
    ]
    y = 510
    for text, color in chips:
        draw_pill(img, text, fm_chip, W/2, y, (8, 22, 30), color)
        y += 56

    # Pitch
    fm_pitch = load_font(20)
    pitch = paper["pitch"].split("\n")[0]
    if len(pitch) > 320: pitch = pitch[:318] + "…"
    draw_text_center(img, pitch, fm_pitch, 770, INK_DIM, max_w=W-100)

    # Concept count, edge count
    fm_stat = load_font(16, mono=True)
    line = f"{len(paper['concepts'])} concepts  ·  {len(paper['pair_edges'])} edges  ·  {paper['source']}"
    draw_text_center(img, line, fm_stat, H - 120, INK_DIM)
    return img


# ── Frame dispatcher ─────────────────────────────────────────────────────

def render_frame(frame_idx: int, paper: dict, positions: dict) -> Image.Image:
    t = frame_idx / FPS
    if t < 2.5:
        return render_scene_title(t, paper)
    if t < 7.0:
        return render_scene_structure(t - 2.5, paper, positions)
    if t < 10.0:
        return render_scene_innovations(t - 7.0, paper)
    return render_scene_novelty(t - 10.0, paper)


# ── Pipeline ─────────────────────────────────────────────────────────────

def safe_id(pid: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", pid)


def render_video(paper: dict, out_path: Path, cleanup: bool = True):
    positions = layout_3d(paper)
    if not positions:
        return False

    tmp = tempfile.mkdtemp(prefix="arxivis_")
    tmp_path = Path(tmp)
    try:
        for i in range(TOTAL_FRAMES):
            img = render_frame(i, paper, positions)
            img.save(tmp_path / f"f_{i:04d}.png", optimize=False)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(FPS),
            "-i", str(tmp_path / "f_%04d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-crf", "22", "-preset", "medium",
            "-movflags", "+faststart",
            str(out_path),
        ]
        subprocess.run(cmd, check=True)
    finally:
        if cleanup:
            shutil.rmtree(tmp, ignore_errors=True)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top",      type=int, default=10,
                    help="generate videos for top N papers by novelty (default 10)")
    ap.add_argument("--paper-id", type=str, default=None,
                    help="render only this paper id (e.g. arx:2602.14625v1)")
    ap.add_argument("--no-cleanup", action="store_true",
                    help="keep PNG frame tmpdir for inspection")
    args = ap.parse_args()

    papers = load_papers()
    if args.paper_id:
        papers = [p for p in papers if p["id"] == args.paper_id]
    else:
        papers = papers[: args.top]

    if not papers:
        sys.exit("no papers matched")

    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for i, p in enumerate(papers, 1):
        out = VIDEOS_DIR / f"{safe_id(p['id'])}.mp4"
        print(f"[{i}/{len(papers)}] {p['id']} — {p['title'][:60]}")
        ok = render_video(p, out, cleanup=not args.no_cleanup)
        if ok:
            manifest[p["id"]] = f"videos/{out.name}"
            print(f"  → {out} ({out.stat().st_size//1024} KB)")
        else:
            print("  ✗ skipped (no positions)")

    # Write manifest
    js = "window.ARXIVIS_VIDEOS = " + json.dumps(manifest, indent=2) + ";\n"
    MANIFEST_JS.write_text(js)
    print(f"\nmanifest → {MANIFEST_JS} ({len(manifest)} videos)")


if __name__ == "__main__":
    main()
