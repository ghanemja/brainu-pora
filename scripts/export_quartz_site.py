"""
Static-site exporter for the wiki vault — Quartz-style 'graphify'.

Takes any folder of markdown (.md / .qmd) + the cluster catalog and
produces a self-contained, deployable HTML site:

  out/
    index.html           interactive 3D graph + searchable note list
    notes/<stem>.html    one rendered page per note with backlinks
    static/graph.json    {nodes, links} payload for the 3D viz
    static/style.css     dark theme

Why: Obsidian-Publish costs $$ and wants its own format. Quartz is great
but needs Node. This script is pure Python + jinja-free template strings,
runs in 2 seconds, output uploads anywhere static (gh-pages, Netlify, S3).

Usage:
    python3 scripts/export_quartz_site.py
    python3 scripts/export_quartz_site.py --vault wiki/concepts --out site
    python3 scripts/export_quartz_site.py --serve   # serve on :8516 after build
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


WIKILINK_RE = re.compile(r"\[\[([^\[\]\|\n]+?)(?:\|([^\[\]\n]+))?\]\]")
TAG_RE = re.compile(r"(?<!\S)#([A-Za-z][\w/\-]+)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"```([\w]*)\n(.*?)```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
BOLD_RE = re.compile(r"\*\*([^*\n]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
LIST_RE = re.compile(r"^(\s*)[-*•]\s+(.+)$", re.MULTILINE)


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9_-]+", "_", s.lower()).strip("_")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _md_to_html(body: str, link_resolver) -> str:
    """Tiny markdown → HTML. Good enough for our wiki notes; not full CommonMark."""
    # Strip frontmatter
    body = FRONTMATTER_RE.sub("", body, count=1)

    # Code fences (replace before other markup)
    code_blocks: list[str] = []
    def _fence(m):
        lang = m.group(1) or ""
        code = m.group(2).strip()
        # Escape HTML inside code
        code = (code.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;"))
        idx = len(code_blocks)
        code_blocks.append(
            f'<pre class="code"><code class="lang-{lang}">{code}</code></pre>'
        )
        return f"\x00CODEBLOCK{idx}\x00"
    body = CODE_FENCE_RE.sub(_fence, body)

    # Wikilinks
    def _wl(m):
        target = re.split(r"[#\^|]", m.group(1).strip(), 1)[0].rsplit("/", 1)[-1]
        alias = m.group(2) or m.group(1)
        href = link_resolver(target)
        if href is None:
            return f'<span class="stub">{alias}</span>'
        return f'<a href="{href}" class="wikilink">{alias}</a>'
    body = WIKILINK_RE.sub(_wl, body)

    # Tags
    body = TAG_RE.sub(r'<span class="tag">#\1</span>', body)

    # Headings (top-down so '######' matches before '#')
    body = re.sub(r"^######\s+(.+)$", r"<h6>\1</h6>", body, flags=re.MULTILINE)
    body = re.sub(r"^#####\s+(.+)$",  r"<h5>\1</h5>", body, flags=re.MULTILINE)
    body = re.sub(r"^####\s+(.+)$",   r"<h4>\1</h4>", body, flags=re.MULTILINE)
    body = re.sub(r"^###\s+(.+)$",    r"<h3>\1</h3>", body, flags=re.MULTILINE)
    body = re.sub(r"^##\s+(.+)$",     r"<h2>\1</h2>", body, flags=re.MULTILINE)
    body = re.sub(r"^#\s+(.+)$",      r"<h1>\1</h1>", body, flags=re.MULTILINE)

    # Lists (very simple — single-level)
    def _list(m):
        items = []
        for line in m.group(0).splitlines():
            mm = LIST_RE.match(line)
            if mm:
                items.append(f"<li>{mm.group(2)}</li>")
        return "<ul>" + "\n".join(items) + "</ul>"
    body = re.sub(r"(?:^[\s]*[-*•]\s+.+\n?)+", _list, body, flags=re.MULTILINE)

    # Inline
    body = BOLD_RE.sub(r"<strong>\1</strong>", body)
    body = ITALIC_RE.sub(r"<em>\1</em>", body)
    body = INLINE_CODE_RE.sub(r"<code>\1</code>", body)

    # Paragraphs
    parts = []
    for chunk in re.split(r"\n\s*\n", body):
        c = chunk.strip()
        if not c:
            continue
        if c.startswith("<") and not c.startswith("<em") and not c.startswith("<strong"):
            parts.append(c)
        else:
            parts.append(f"<p>{c}</p>")
    html = "\n\n".join(parts)

    # Restore code blocks
    for i, blk in enumerate(code_blocks):
        html = html.replace(f"\x00CODEBLOCK{i}\x00", blk)
    return html


def _write_index(out: Path, notes: dict, clusters: list, graph_json: dict):
    """Index.html: top-bar search + 3D force graph + note list."""
    cluster_summary = [
        {"id": c.cluster_id, "name": c.name, "members": len(c.members)}
        for c in (clusters or [])
    ]
    # Pre-render note metadata as JSON for client-side filter
    note_meta = [
        {"stem": s, "title": s.replace("_", " "),
         "href": f"notes/{_slug(s)}.html",
         "tags": list(n.get("tags") or [])[:6],
         "para": n.get("para", "Resources")}
        for s, n in sorted(notes.items())
    ]
    payload = {
        "graph": graph_json,
        "notes": note_meta,
        "clusters": cluster_summary,
    }

    index_html = (INDEX_TPL
        .replace("__PAYLOAD__", json.dumps(payload))
    )
    (out / "index.html").write_text(index_html)


INDEX_TPL = """<!doctype html>
<html><head><meta charset="utf-8">
<title>Brain — vault explorer</title>
<link rel="stylesheet" href="static/style.css">
<script src="https://unpkg.com/3d-force-graph"></script>
</head>
<body>
<header>
  <div class="brand">🧠 Brain</div>
  <input id="q" placeholder="Filter notes…" oninput="filterNotes()">
  <span id="counts"></span>
</header>
<main>
  <aside id="sidebar">
    <h3>Clusters</h3>
    <ul id="clusters"></ul>
    <h3 style="margin-top:18px">Notes</h3>
    <ul id="notes"></ul>
  </aside>
  <section id="graph"></section>
</main>
<script id="payload" type="application/json">__PAYLOAD__</script>
<script>
  const data = JSON.parse(document.getElementById('payload').textContent);
  // Cluster panel
  const cl = document.getElementById('clusters');
  data.clusters.slice(0, 30).forEach(c => {
    const li = document.createElement('li');
    li.textContent = `${c.name}  (${c.members})`;
    cl.appendChild(li);
  });
  // Notes panel
  const nl = document.getElementById('notes');
  function renderNotes(filter='') {
    nl.innerHTML = '';
    const f = filter.toLowerCase();
    let n = 0;
    for (const note of data.notes) {
      if (f && !note.title.toLowerCase().includes(f) && !note.stem.toLowerCase().includes(f)) continue;
      n++;
      if (n > 200) break;
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = note.href;
      a.textContent = note.title;
      li.appendChild(a);
      nl.appendChild(li);
    }
    document.getElementById('counts').textContent = `${n} of ${data.notes.length}`;
  }
  function filterNotes() { renderNotes(document.getElementById('q').value); }
  renderNotes();

  // 3D force graph
  const PALETTE = ['#1E2761','#3B5BA5','#9B59B6','#16A085','#27AE60',
                   '#E67E22','#C0392B','#8E44AD','#2C3E50','#D35400','#7F8C8D','#2980B9'];
  const G = ForceGraph3D()(document.getElementById('graph'))
    .graphData(data.graph)
    .backgroundColor('#0F1733')
    .nodeLabel(n => `${n.label}\\n(${n.cluster_name || ''})`)
    .nodeColor(n => PALETTE[(n.cluster || 0) % PALETTE.length])
    .nodeVal(n => Math.max(2, n.degree || 1))
    .linkColor(() => '#7DD3FC')
    .linkOpacity(0.35)
    .linkWidth(0.6)
    .onNodeClick(n => { if (n.href) window.location.href = n.href; });
</script>
</body></html>"""


STYLE_CSS = """
:root { --bg:#0F1733; --fg:#FAFBFE; --accent:#F96167; --side:#1E2761; --link:#7DD3FC; }
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,system-ui,Segoe UI,sans-serif;
     background:var(--bg);color:var(--fg);}
header{display:flex;align-items:center;gap:14px;padding:10px 16px;
       background:#0a0f24;border-bottom:1px solid #1E2761;}
header .brand{font-weight:700;color:var(--accent);}
header input{flex:1;padding:8px 12px;border:1px solid #3B5BA5;background:#07091F;
             color:var(--fg);border-radius:6px;font-size:14px}
header #counts{font-size:12px;color:var(--link);}
main{display:flex;height:calc(100vh - 50px);}
aside{width:260px;background:#07091F;padding:14px;overflow-y:auto;
       border-right:1px solid #1E2761;}
aside h3{margin:0 0 6px 0;font-size:12px;letter-spacing:0.05em;
         text-transform:uppercase;color:var(--link);}
aside ul{margin:0;padding:0;list-style:none;font-size:13px;}
aside li{padding:3px 0;}
aside a{color:var(--fg);text-decoration:none;}
aside a:hover{color:var(--accent);}
#graph{flex:1;}
.note-page{max-width:780px;margin:24px auto;padding:0 24px;}
.note-page h1{color:var(--accent);}
.note-page h2,.note-page h3{color:var(--link);}
.note-page a.wikilink{color:var(--link);text-decoration:none;border-bottom:1px dashed #7DD3FC;}
.note-page a.wikilink:hover{color:var(--accent);}
.note-page .stub{color:#888;text-decoration:line-through;}
.note-page .tag{color:#FBB036;font-size:0.85em;}
.note-page pre.code{background:#07091F;padding:12px;border-radius:6px;
                     overflow-x:auto;border:1px solid #1E2761;}
.note-page code{background:#1E2761;padding:1px 6px;border-radius:3px;}
.note-page .meta{color:#888;font-size:13px;margin-bottom:18px;
                  padding-bottom:10px;border-bottom:1px solid #1E2761;}
.backlinks{margin-top:30px;padding-top:14px;border-top:1px solid #1E2761;}
.backlinks h3{color:var(--link);font-size:13px;
              text-transform:uppercase;letter-spacing:0.05em;}
.backlinks ul{padding-left:18px;}
.backlinks a{color:var(--fg);}
"""


NOTE_TPL = """<!doctype html>
<html><head><meta charset="utf-8">
<title>__TITLE__ — Brain vault</title>
<link rel="stylesheet" href="../static/style.css">
</head>
<body>
<header>
  <div class="brand">🧠 Brain</div>
  <a href="../index.html" style="color:#FAFBFE;text-decoration:none">← back to graph</a>
</header>
<article class="note-page">
  <h1>__TITLE__</h1>
  <div class="meta">__META__</div>
  __BODY__
  <div class="backlinks">
    <h3>← Linked from</h3>
    <ul>__BACKLINKS__</ul>
  </div>
</article>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=str(PROJECT_ROOT / "wiki" / "concepts"))
    ap.add_argument("--out", default=str(PROJECT_ROOT / "site"))
    ap.add_argument("--serve", action="store_true",
                    help="After build, run http.server on :8516")
    ap.add_argument("--include-qmd", action="store_true",
                    help="Also export .qmd files (Quarto)")
    ap.add_argument("--port", type=int, default=8516)
    args = ap.parse_args()

    vault = Path(args.vault).expanduser()
    out = Path(args.out)
    if not vault.is_dir():
        sys.exit(f"✗ vault not found: {vault}")

    print(f"[1/5] Reading vault: {vault}")
    extensions = (".md", ".qmd") if args.include_qmd else (".md",)
    notes: dict[str, dict] = {}
    for ext in extensions:
        for f in vault.rglob(f"*{ext}"):
            if any(seg.startswith(".") for seg in f.relative_to(vault).parts):
                continue
            stem = f.stem
            if stem in notes:
                continue
            try:
                body = f.read_text(errors="ignore")
            except Exception:
                continue
            tags = list(set(TAG_RE.findall(body)))
            notes[stem] = {
                "stem": stem,
                "path": str(f.relative_to(vault)),
                "body": body,
                "tags": tags,
            }
    print(f"  {len(notes)} notes")

    print("[2/5] Building wikilink + backlink index")
    norm_to_stem = {_norm(s): s for s in notes}
    backlinks: dict[str, list[str]] = {s: [] for s in notes}
    edges: list[tuple[str, str]] = []
    for stem, n in notes.items():
        body = n["body"]
        seen_targets = set()
        for m in WIKILINK_RE.finditer(body):
            t = re.split(r"[#\^|]", m.group(1).strip(), 1)[0].rsplit("/", 1)[-1]
            real = norm_to_stem.get(_norm(t))
            if real and real != stem and real not in seen_targets:
                edges.append((stem, real))
                backlinks.setdefault(real, []).append(stem)
                seen_targets.add(real)
    print(f"  {len(edges)} edges, {sum(len(v) for v in backlinks.values())} backlinks")

    print("[3/5] Loading clusters (best-effort)")
    clusters = []
    node_to_cluster: dict[str, dict] = {}
    try:
        from graph.clusters import load_clusters, build_clusters
        clusters = load_clusters() or build_clusters(force=False)
        for c in clusters:
            for m in c.members:
                node_to_cluster[m] = {"id": c.cluster_id, "name": c.name}
        print(f"  {len(clusters)} clusters")
    except Exception as e:
        print(f"  skip clusters: {e}")

    print(f"[4/5] Writing site to {out}")
    out.mkdir(parents=True, exist_ok=True)
    (out / "static").mkdir(exist_ok=True)
    (out / "notes").mkdir(exist_ok=True)
    (out / "static" / "style.css").write_text(STYLE_CSS)

    # Per-note html
    def _resolver(target_stem: str) -> str | None:
        real = norm_to_stem.get(_norm(target_stem))
        if real is None:
            return None
        return f"../notes/{_slug(real)}.html"

    degree: dict[str, int] = {s: 0 for s in notes}
    for a, b in edges:
        degree[a] = degree.get(a, 0) + 1
        degree[b] = degree.get(b, 0) + 1

    for stem, n in notes.items():
        html_body = _md_to_html(n["body"], _resolver)
        bl_links = "".join(
            f'<li><a href="{_slug(s)}.html">{s.replace("_", " ")}</a></li>'
            for s in list(dict.fromkeys(backlinks.get(stem, [])))[:30]
        ) or "<li><em>no incoming links</em></li>"
        cluster_meta = node_to_cluster.get(stem, {})
        meta_bits = []
        if cluster_meta:
            meta_bits.append(f"cluster: {cluster_meta.get('name','?')}")
        if n["tags"]:
            meta_bits.append("tags: " + " ".join(f"#{t}" for t in n["tags"]))
        meta_bits.append(f"degree: {degree.get(stem, 0)}")
        html = (NOTE_TPL
            .replace("__TITLE__", stem.replace("_", " "))
            .replace("__BODY__", html_body)
            .replace("__BACKLINKS__", bl_links)
            .replace("__META__", " · ".join(meta_bits))
        )
        (out / "notes" / f"{_slug(stem)}.html").write_text(html)

    # Graph payload (3D)
    graph_json = {
        "nodes": [
            {
                "id": s,
                "label": s.replace("_", " "),
                "cluster": node_to_cluster.get(s, {}).get("id", -1),
                "cluster_name": node_to_cluster.get(s, {}).get("name", ""),
                "degree": degree.get(s, 0),
                "href": f"notes/{_slug(s)}.html",
            }
            for s in notes
        ],
        "links": [{"source": a, "target": b} for a, b in edges],
    }

    (out / "static" / "graph.json").write_text(json.dumps(graph_json))
    _write_index(out, notes, clusters, graph_json)

    print(f"[5/5] Done → {out}")
    print(f"  index: {out}/index.html")
    print(f"  notes: {len(notes)} pages")
    print(f"  size: {sum(p.stat().st_size for p in out.rglob('*') if p.is_file()) / 1e6:.1f} MB")

    if args.serve:
        import http.server
        import socketserver
        import os as _os
        _os.chdir(out)
        with socketserver.TCPServer(("", args.port),
                                     http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"\n  serving http://localhost:{args.port}/  (Ctrl-C to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n  stopped")


if __name__ == "__main__":
    main()
