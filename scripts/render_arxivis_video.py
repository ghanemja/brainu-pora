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
DURATION_S  = 16
TOTAL_FRAMES = FPS * DURATION_S

# Scene boundaries (seconds)
T_TITLE_END        = 2.0
T_STRUCT_END       = 4.5
T_FOUNDATION_END   = 6.0   # Scene C1 — light up foundations
T_INTRODUCED_END   = 9.0   # Scene C2 — materialize introduced nodes
T_NEW_EDGES_END    = 11.5  # Scene C3 — draw new edges
# Scene D — explain what the paper actually says (was: abstract novelty stats)
T_HEADLINE_END     = 12.5  # D1 — one-line big-idea headline
T_CONCEPTS_END     = 14.5  # D2 — stagger introduced concepts w/ glosses
T_INNOVATION_END   = 15.5  # D3 — top innovation phrase + pattern badge
T_NOVELTY_END      = 16.0  # D4 — compact novelty bits chip footer

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


def _classify_nodes(paper: dict) -> tuple[set, set, list, list]:
    """Return (foundation_ids, introduced_ids, foundations, introduceds)."""
    foundations  = paper.get("foundations", []) or []
    introduceds  = paper.get("introduced",  []) or []
    f_ids = {c["id"] for c in foundations}
    i_ids = {c["id"] for c in introduceds}
    return f_ids, i_ids, foundations, introduceds


def _draw_node_glow(draw, sx, sy, r, color, glow_alpha=80):
    """Multi-pass glow halo + solid core. r is the core radius."""
    if r < 2:
        return
    for k in range(4, 0, -1):
        rr = r + k * 3
        f = max(0, 255 - 40 * k)
        draw.ellipse([sx-rr, sy-rr, sx+rr, sy+rr],
                     fill=tuple(int(c * 0.15 + f * 0.05) for c in color))
    draw.ellipse([sx-r, sy-r, sx+r, sy+r], fill=color)
    if r > 3:
        inner = tuple(min(255, c + 60) for c in color)
        draw.ellipse([sx-r+2, sy-r+2, sx+r-2, sy+r-2], fill=inner)


def render_scene_construction(t_global: float, paper: dict, positions: dict) -> Image.Image:
    """
    Constructive build of the paper's subgraph:
      Phase 1 (T_STRUCT_END   → T_FOUNDATION_END):  foundations light up
      Phase 2 (T_FOUNDATION_END → T_INTRODUCED_END): introduced nodes materialize
      Phase 3 (T_INTRODUCED_END → T_NEW_EDGES_END):  new edges grow between them

    The reader literally watches the paper "get added to the brain".
    """
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fm_meta   = load_font(20, mono=True)
    fm_chip   = load_font(15, mono=True)
    fm_name   = load_font(17, mono=True)
    fm_label  = load_font(13, mono=True)

    f_ids, i_ids, foundations, introduceds = _classify_nodes(paper)

    # ── Fixed 2-column layout: foundations LEFT, introduced RIGHT ────────
    # This makes the "before → after" structure immediately readable
    # without the spring layout collapsing everything to the centre.
    #
    # Column geometry (fits 9:16 720×1280 frame):
    LEFT_X      = int(W * 0.26)
    RIGHT_X     = int(W * 0.74)
    COL_TOP     = int(H * 0.32)
    COL_BOTTOM  = int(H * 0.78)
    proj: dict[str, tuple[float, float, float]] = {}

    def _column_y(i: int, n: int) -> float:
        if n == 1:
            return (COL_TOP + COL_BOTTOM) / 2
        gap = (COL_BOTTOM - COL_TOP) / (n - 1)
        return COL_TOP + i * gap

    for i, f in enumerate(foundations):
        proj[f["id"]] = (LEFT_X,  _column_y(i, len(foundations)), 1.0)
    for i, c in enumerate(introduceds):
        proj[c["id"]] = (RIGHT_X, _column_y(i, len(introduceds)), 1.0)
    # Drop any concept not in foundations/introduced — keeps the frame clean

    # Determine phase + reveal counts
    if t_global < T_FOUNDATION_END:
        phase = 1
        head_label = "FOUNDATIONS"
        head_color = CYAN
        foundation_alpha = (t_global - T_STRUCT_END) / max(0.01, T_FOUNDATION_END - T_STRUCT_END)
        introduced_visible = 0
        new_edge_progress = 0
    elif t_global < T_INTRODUCED_END:
        phase = 2
        head_label = "INTRODUCES"
        head_color = GREEN
        foundation_alpha = 1.0
        per_node = (T_INTRODUCED_END - T_FOUNDATION_END) / max(1, len(introduceds))
        introduced_visible = int((t_global - T_FOUNDATION_END) / per_node) + 1
        new_edge_progress = 0
    else:
        phase = 3
        head_label = "NEW LINKS"
        head_color = AMBER
        foundation_alpha = 1.0
        introduced_visible = len(introduceds)
        new_edge_progress = (t_global - T_INTRODUCED_END) / max(0.01, T_NEW_EDGES_END - T_INTRODUCED_END)

    foundation_alpha = max(0.0, min(1.0, foundation_alpha))
    new_edge_progress = max(0.0, min(1.0, new_edge_progress))

    # ── Column headers ───────────────────────────────────────────────────
    fm_col_header = load_font(13, mono=True)
    if foundation_alpha > 0.2:
        s = "FOUNDATIONS"
        tw = draw.textlength(s, font=fm_col_header)
        draw.text((LEFT_X - tw / 2, COL_TOP - 36), s,
                  font=fm_col_header, fill=CYAN)
    if phase >= 2:
        s = "INTRODUCED"
        tw = draw.textlength(s, font=fm_col_header)
        draw.text((RIGHT_X - tw / 2, COL_TOP - 36), s,
                  font=fm_col_header, fill=AMBER)

    # ── Foundation nodes (cyan, left column) ─────────────────────────────
    NODE_R = 22
    if foundation_alpha > 0:
        for f in foundations:
            sx, sy, _ = proj[f["id"]]
            tint = tuple(int(c * foundation_alpha) for c in CYAN)
            _draw_node_glow(draw, int(sx), int(sy), NODE_R, tint)
            if foundation_alpha > 0.5:
                name = f["name"]
                if len(name) > 24: name = name[:22] + "…"
                tw = draw.textlength(name, font=fm_name)
                draw.text((sx - tw / 2, sy + NODE_R + 10), name,
                          font=fm_name,
                          fill=tuple(int(c * foundation_alpha) for c in CYAN_GLOW))
                # Optional: paper-count chip below name
                deg_label = f"in {f.get('degree', 1)} papers"
                tw2 = draw.textlength(deg_label, font=fm_label)
                draw.text((sx - tw2 / 2, sy + NODE_R + 32), deg_label,
                          font=fm_label, fill=INK_DIM)

    # ── Introduced nodes (amber, right column, pop-in animation) ────────
    for i, c in enumerate(introduceds):
        if i >= introduced_visible: break
        sx, sy, _ = proj[c["id"]]
        per_node = (T_INTRODUCED_END - T_FOUNDATION_END) / max(1, len(introduceds))
        age = max(0.0, t_global - (T_FOUNDATION_END + i * per_node))
        scale = min(1.0, age * 3.0)
        r = int(NODE_R * scale)
        if r < 2: continue
        _draw_node_glow(draw, int(sx), int(sy), r, AMBER)
        name = c["name"]
        if len(name) > 24: name = name[:22] + "…"
        tw = draw.textlength(name, font=fm_name)
        draw.text((sx - tw / 2, sy + r + 10), name, font=fm_name, fill=AMBER)

    # ── New edges (foundation ↔ introduced) — animated growth ────────────
    new_edges = []
    if new_edge_progress > 0:
        for a, b in paper["pair_edges"]:
            if a in proj and b in proj:
                a_is_intro = a in i_ids; b_is_intro = b in i_ids
                if (a_is_intro and not b_is_intro) or (b_is_intro and not a_is_intro):
                    # canonical: foundation→introduced
                    if a_is_intro: a, b = b, a
                    new_edges.append((a, b))
        # Add introduced-introduced edges too (the paper's own internal connections)
        for a, b in paper["pair_edges"]:
            if a in proj and b in proj and a in i_ids and b in i_ids:
                new_edges.append((a, b))
        # progressive growth
        n_edges_visible = min(len(new_edges), int(new_edge_progress * len(new_edges)) + 1)
        for k, (a, b) in enumerate(new_edges[:n_edges_visible]):
            x1, y1, _ = proj[a]; x2, y2, _ = proj[b]
            edge_age = new_edge_progress * len(new_edges) - k
            ratio = max(0.0, min(1.0, edge_age))
            xe = x1 + (x2 - x1) * ratio
            ye = y1 + (y2 - y1) * ratio
            draw.line([(x1, y1), (xe, ye)], fill=AMBER, width=3)

    # ── Headers / footers ────────────────────────────────────────────────
    draw_pill(img, head_label, fm_meta, W / 2, 80, head_color, BG_COLOR)

    # Step counter / phase narration
    if phase == 1 and foundations:
        names = ", ".join(f["name"] for f in foundations[:3])
        narration = f"this paper rests on: {names}"
    elif phase == 2 and introduceds:
        if introduced_visible <= len(introduceds):
            curr = introduceds[introduced_visible - 1] if introduced_visible >= 1 else None
            if curr:
                narration = f"adds:  {curr['name']}"
            else:
                narration = ""
        else:
            narration = ""
    elif phase == 3:
        n_new_edges = sum(1 for a, b in paper['pair_edges'] if (a in i_ids or b in i_ids))
        narration = f"linking new to existing  --  {len(introduceds)} nodes, {n_new_edges} new edges"
    else:
        narration = ""

    if narration:
        fm_sub = load_font(18)
        draw_text_center(img, narration, fm_sub, 145, INK_BRIGHT, max_w=W - 60)

    # Footer: count chip
    if phase >= 2:
        chip = f"{len(foundations)} foundations · {introduced_visible}/{len(introduceds)} new"
        draw_pill(img, chip, fm_chip, W / 2, H - 90, (10, 24, 36), CYAN_GLOW)

    # Bottom strip: paper title (truncated)
    fm_title = load_font(15)
    title = paper["title"]
    if len(title) > 70: title = title[:68] + "…"
    draw_text_center(img, title, fm_title, H - 55, INK_DIM, max_w=W - 80)

    return img


def _ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _clean_sentence(s: str, max_len: int = 180) -> str:
    s = (s or "").strip().rstrip(".") + "."
    if len(s) > max_len:
        s = s[: max_len - 1].rsplit(" ", 1)[0] + "…"
    return s


def _pick_headline(paper: dict) -> str:
    """One sentence summarizing what the paper says.

    Priority: key_finding (paper's own thesis) → first pitch sentence →
    top innovation phrase → title.
    """
    kf = (paper.get("key_finding") or "").strip()
    if kf and len(kf.split()) >= 5:
        return _clean_sentence(kf, 220)
    pitch = (paper.get("pitch") or "").strip()
    if pitch:
        first = re.split(r"(?<=[.!?])\s+", pitch)[0]
        if len(first.split()) >= 5:
            return _clean_sentence(first, 220)
    inns = paper.get("innovations") or []
    if inns:
        inns_sorted = sorted(inns, key=lambda x: -(x.get("priority", 0) or 0))
        phrase = (inns_sorted[0].get("phrase") or "").strip()
        if phrase:
            return _clean_sentence(phrase, 220)
    return _clean_sentence(paper.get("title", ""), 220)


def _pick_innovation(paper: dict, headline: str) -> dict | None:
    """Top innovation that doesn't duplicate the headline."""
    inns = paper.get("innovations") or []
    if not inns:
        return None
    inns_sorted = sorted(inns, key=lambda x: -(x.get("priority", 0) or 0))
    head_norm = re.sub(r"\W+", "", (headline or "").lower())[:40]
    for inn in inns_sorted:
        phr = re.sub(r"\W+", "", (inn.get("phrase") or "").lower())[:40]
        if phr and phr != head_norm:
            return inn
    return inns_sorted[0]


def _pattern_label(pattern: str, kind: str) -> str:
    """Map innovation pattern → human label."""
    k = (kind or "").lower()
    p = (pattern or "").lower()
    if k == "connects" or "connect" in p: return "CONNECTS"
    if k == "introduces" or "propose" in p or "introduce" in p: return "PROPOSES"
    if k == "claim" or "claim" in p: return "CLAIMS"
    if k == "method" or "method" in p: return "METHOD"
    if k == "result" or "result" in p: return "RESULT"
    return (kind or pattern or "FINDS").upper()


def render_scene_explanation(t_global: float, paper: dict) -> Image.Image:
    """Plain-English concept explanation. Replaces the abstract novelty card.

    Internal phases (all driven by t_global, the absolute video time):
      D1  T_NEW_EDGES_END  → T_HEADLINE_END   : headline fades up
      D2  T_HEADLINE_END   → T_CONCEPTS_END   : introduced concepts stagger
      D3  T_CONCEPTS_END   → T_INNOVATION_END : top innovation w/ pattern badge
      D4  T_INNOVATION_END → T_NOVELTY_END    : novelty bits footer chip
    """
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    fm_tag    = load_font(16, mono=True)
    fm_head   = load_font(30, weight="Medium")
    fm_concept = load_font(24, weight="Medium")
    fm_gloss  = load_font(17)
    fm_inn    = load_font(22, weight="Medium")
    fm_chip   = load_font(13, mono=True)

    # ── D1 headline (always visible, just fades up at the start) ──────
    headline_local = max(0.0, min(1.0, (t_global - T_NEW_EDGES_END) / (T_HEADLINE_END - T_NEW_EDGES_END)))
    head_alpha = _ease_in_out(headline_local)
    head_color = tuple(int(c * head_alpha + INK_DIM[i] * (1 - head_alpha)) for i, c in enumerate(INK_BRIGHT))

    draw_pill(img, "WHAT THIS PAPER SAYS", fm_tag, W / 2, 110, (12, 28, 40), CYAN_GLOW)
    headline = _pick_headline(paper)
    draw_text_center(img, headline, fm_head, 180, head_color, max_w=W - 80)

    # ── D2 introduced concepts stagger ──────────────────────────────
    # Each introduced concept: name + one-line role gloss
    introduceds = paper.get("introduced") or []
    show_concepts = [c for c in introduceds if c.get("name")][:3]

    if t_global >= T_HEADLINE_END and show_concepts:
        # tag
        if t_global < T_CONCEPTS_END:
            draw_pill(img, "KEY CONCEPTS INTRODUCED", fm_tag, W / 2, 440, (12, 28, 40), AMBER)

        # Per-concept stagger inside D2 window
        d2_span = max(0.001, T_CONCEPTS_END - T_HEADLINE_END)
        per_concept = d2_span / max(1, len(show_concepts))
        base_y = 490
        slot_h = 130

        for i, c in enumerate(show_concepts):
            local_start = T_HEADLINE_END + i * per_concept * 0.7  # overlap reveals
            reveal = _ease_in_out((t_global - local_start) / max(0.001, per_concept * 0.9))
            if reveal <= 0:
                continue
            y_top = base_y + i * slot_h
            # slide-in from below
            slide = int((1 - reveal) * 18)
            alpha = reveal

            # Name pill
            name = c["name"]
            col = (int(GREEN[0] * alpha + BG_COLOR[0] * (1 - alpha)),
                   int(GREEN[1] * alpha + BG_COLOR[1] * (1 - alpha)),
                   int(GREEN[2] * alpha + BG_COLOR[2] * (1 - alpha)))
            draw_text_center(img, name, fm_concept, y_top + slide, col, max_w=W - 80)

            # One-line gloss — synthesize from what we know about the concept
            role = _concept_role(c, paper)
            gloss_col = (int(INK_DIM[0] * alpha + BG_COLOR[0] * (1 - alpha)),
                         int(INK_DIM[1] * alpha + BG_COLOR[1] * (1 - alpha)),
                         int(INK_DIM[2] * alpha + BG_COLOR[2] * (1 - alpha)))
            draw_text_center(img, role, fm_gloss, y_top + 38 + slide, gloss_col, max_w=W - 100)

    # ── D3 top innovation phrase ─────────────────────────────────
    if t_global >= T_CONCEPTS_END:
        inn_local = _ease_in_out((t_global - T_CONCEPTS_END) / max(0.001, T_INNOVATION_END - T_CONCEPTS_END))
        inn = _pick_innovation(paper, headline)
        if inn:
            label = _pattern_label(inn.get("pattern"), inn.get("kind"))
            phrase = _clean_sentence(inn.get("phrase", ""), 200)

            # Clear lower half visually w/ a faint divider
            draw.line([(60, 870), (W - 60, 870)], fill=(18, 38, 56), width=2)

            alpha = inn_local
            badge_color = {
                "CONNECTS": CYAN_GLOW, "PROPOSES": GREEN, "CLAIMS": AMBER,
                "METHOD": CYAN, "RESULT": GREEN_DIM,
            }.get(label, CYAN_GLOW)
            draw_pill(img, label, fm_tag, W / 2, 920, (12, 28, 40), badge_color)
            txt_col = (int(INK_BRIGHT[0] * alpha + INK_DIM[0] * (1 - alpha)),
                       int(INK_BRIGHT[1] * alpha + INK_DIM[1] * (1 - alpha)),
                       int(INK_BRIGHT[2] * alpha + INK_DIM[2] * (1 - alpha)))
            draw_text_center(img, phrase, fm_inn, 970, txt_col, max_w=W - 80)

    # ── D4 novelty bits + source — footer chip (compact, always last) ─
    if t_global >= T_INNOVATION_END:
        bits = paper.get("novelty_bits", 0.0)
        footer = f"{bits:.1f} bits  ·  {len(paper.get('concepts', []))} concepts  ·  {paper.get('source','')}"
        draw_text_center(img, footer, fm_chip, H - 70, GREEN_DIM)
    else:
        # mini-source watermark while the explanation is animating
        draw_text_center(img, paper.get("source", ""), fm_chip, H - 70, INK_DIM)

    return img


def _concept_role(c: dict, paper: dict) -> str:
    """One-line plain-English gloss for a concept in this paper's context.

    Uses signals: echoes_title, weight, degree, and whether any innovation
    phrase mentions this concept by id.
    """
    name = c.get("name", "this concept")
    deg = c.get("degree", 0) or 0
    echoes = bool(c.get("echoes_title"))

    # Find innovation phrase that names this concept id
    cid = c.get("id")
    for inn in (paper.get("innovations") or []):
        if cid and cid in (inn.get("connects_to") or []):
            phrase = (inn.get("phrase") or "").strip()
            if phrase and len(phrase) < 130:
                return _clean_sentence(phrase, 130)
            break

    if echoes and deg <= 1:
        return f"the central new idea — defined by this paper."
    if deg == 0:
        return f"a new term, introduced here for the first time."
    if deg <= 2:
        return f"a fresh framing, lightly connected to prior work."
    return f"a familiar concept reframed in a new context."


# ── Frame dispatcher ─────────────────────────────────────────────────────

def render_frame(frame_idx: int, paper: dict, positions: dict) -> Image.Image:
    t = frame_idx / FPS
    if t < T_TITLE_END:
        return render_scene_title(t, paper)
    if t < T_STRUCT_END:
        return render_scene_structure(t - T_TITLE_END, paper, positions)
    if t < T_NEW_EDGES_END:
        return render_scene_construction(t, paper, positions)
    return render_scene_explanation(t, paper)


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

    # Load existing manifest and merge — never clobber prior renders.
    manifest = {}
    if MANIFEST_JS.exists():
        try:
            txt = MANIFEST_JS.read_text()
            m = re.search(r"window\.ARXIVIS_VIDEOS\s*=\s*(.*?);\s*$", txt, re.DOTALL)
            if m:
                manifest = json.loads(m.group(1))
        except Exception:
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

    # Write manifest (merged)
    js = "window.ARXIVIS_VIDEOS = " + json.dumps(manifest, indent=2) + ";\n"
    MANIFEST_JS.write_text(js)
    print(f"\nmanifest → {MANIFEST_JS} ({len(manifest)} videos)")


if __name__ == "__main__":
    main()
