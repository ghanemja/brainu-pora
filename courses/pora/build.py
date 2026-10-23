"""
Build every PoRA artifact from the single source of truth, courses/pora/pora.json.

Outputs
  wiki/concepts/<Page>.md            one page per concept (new pages are fully
                                     generated; existing Brain University pages get
                                     a marked "In Principles of Robot Autonomy" block)
  wiki/concepts/Principles_of_Robot_Autonomy.md   course index page
  design/courses/pora-atlas.html     standalone Atlas page (served inside Brain University)
  design/courses/pora_bu.js          adds the PoRA course cluster, lessons, and quizzes
                                     to window.BU_DATA so routes can be walked as tours
  courses/pora/dist/pora-atlas.html  Atlas body for publishing as a hosted page

Inputs
  courses/pora/pora.json     concepts, prerequisites, chapters, notebooks, lectures, backgrounds
  courses/pora/study.json    per-concept key ideas, a concept check, and a try-it prompt

Run:    python3 courses/pora/build.py           validate, then write every output
        python3 courses/pora/build.py --check   validate, and fail if any output is stale (CI)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
WIKI = ROOT / "wiki" / "concepts"
DESIGN = ROOT / "design" / "courses"
DIST = HERE / "dist"

BEGIN = "<!-- pora:begin -->"
END = "<!-- pora:end -->"
CH_LABEL = {0: "Getting started: Robot Autonomy Software"}


def page_id(name: str) -> str:
    s = name.replace("&", "and").replace("*", "-star").replace(".", "")
    s = re.sub(r"[()]", "", s)
    s = re.sub(r"[^A-Za-z0-9\- ]+", " ", s)
    s = re.sub(r"\s+", "_", s.strip())
    return s[0].upper() + s[1:]


def load() -> dict:
    d = json.loads((HERE / "pora.json").read_text())
    study = json.loads((HERE / "study.json").read_text())
    for c in d["concepts"]:
        c.setdefault("wiki", page_id(c["name"]))
        c.setdefault("exercises", [])
        c.setdefault("lectures", [])
        c.setdefault("related", [])
        c.update(study.get(c["id"], {}))
    extra = set(study) - {c["id"] for c in d["concepts"]}
    if extra:
        fail([f"study.json has entries for unknown concepts: {sorted(extra)}"])
    return d


YT = re.compile(r"(?:youtu\.be/|v=|embed/)([\w-]{11})")


def fail(errors: list[str]) -> None:
    print("PoRA data is invalid:", file=sys.stderr)
    for e in errors:
        print("  - " + e, file=sys.stderr)
    sys.exit(1)


def validate(d: dict) -> None:
    """Catch every data mistake that would show up as a broken page, link, or quiz."""
    err = []
    ids = [c["id"] for c in d["concepts"]]
    C = {c["id"]: c for c in d["concepts"]}
    chapters = {ch["n"] for ch in d["chapters"]}
    layers = {l["id"] for l in d["layers"]}
    if len(ids) != len(set(ids)):
        err.append("duplicate concept ids: " + ", ".join(sorted({i for i in ids if ids.count(i) > 1})))
    wikis = [c["wiki"] for c in d["concepts"]]
    if len(wikis) != len(set(wikis)):
        err.append("two concepts map to the same wiki page")
    in_parts = [n for p in d["parts"] for n in p["chapters"]]
    if sorted(in_parts) != sorted(chapters):
        err.append("parts must list every chapter exactly once")
    for ch in d["chapters"]:
        if not ch["url"].startswith("https://"):
            err.append(f"chapter {ch['n']}: url must be https")
    for k, L in d["lectures"].items():
        if not YT.search(L["url"]):
            err.append(f"lecture {k}: not a YouTube url: {L['url']}")
    seen_nb = set()
    for c in d["concepts"]:
        i = c["id"]
        if c["layer"] not in layers:
            err.append(f"{i}: unknown layer {c['layer']}")
        if c["ch"] is not None and c["ch"] not in chapters:
            err.append(f"{i}: unknown chapter {c['ch']}")
        if c["kind"] not in ("classical", "learned", "foundation"):
            err.append(f"{i}: unknown kind {c['kind']}")
        for f in ("prereqs", "related"):
            for x in c[f]:
                if x not in C:
                    err.append(f"{i}: {f} references unknown concept {x}")
        for x in c["lectures"]:
            if x not in d["lectures"]:
                err.append(f"{i}: unknown lecture {x}")
        for x in c["exercises"]:
            if not re.fullmatch(r"ch\d{2}/[\w/]+\.ipynb", x):
                err.append(f"{i}: notebook path looks wrong: {x}")
            seen_nb.add(x)
        pts = c.get("points")
        if not (isinstance(pts, list) and len(pts) == 3 and all(isinstance(p, str) and p.strip() for p in pts)):
            err.append(f"{i}: study.json needs exactly 3 key ideas")
        k = c.get("check")
        if not (isinstance(k, dict) and k.get("q") and isinstance(k.get("choices"), list) and len(k["choices"]) == 4
                and len(set(k["choices"])) == 4 and k.get("correct") in range(4) and k.get("why")):
            err.append(f"{i}: study.json check needs q, 4 distinct choices, correct in 0..3, and why")
        if not c.get("tryIt"):
            err.append(f"{i}: study.json needs a tryIt prompt")
    # prerequisite graph must be acyclic
    state = {}

    def visit(x, path):
        if state.get(x) == 1:
            err.append("prerequisite cycle: " + " -> ".join(path + [x]))
            return
        if state.get(x) == 2:
            return
        state[x] = 1
        for p in C[x]["prereqs"]:
            if p in C:
                visit(p, path + [x])
        state[x] = 2
    for x in ids:
        visit(x, [])
    for b in d["backgrounds"]:
        for x in b["knows"]:
            if x not in C:
                err.append(f"background {b['id']}: unknown concept {x}")
    if not any(b["id"] == "new" for b in d["backgrounds"]):
        err.append("backgrounds must include id 'new' (the planner default)")
    for r in d["meta"].get("resources", []):
        if not r.get("url", "").startswith("https://"):
            err.append(f"resource {r.get('name')}: url must be https")
    if err:
        fail(err)


def ex_title(path: str) -> str:
    t = path.rsplit("/", 1)[-1].removesuffix(".ipynb").replace("_", " ").title()
    for w in ["Lqr", "Mpc", "Pid", "Rrt", "Prm", "Icp", "Cnn", "Ekf", "Ukf", "Slam", "Tpbvp", "Jax", "Sift"]:
        t = re.sub(rf"\b{w}\b", w.upper(), t)
    return t.replace("A Star", "A*").replace("PRM Star", "PRM*")


def ch_label(n, title: str) -> str:
    return CH_LABEL.get(n, f"Chapter {n}: {title}")


def materials(c: dict, d: dict) -> dict:
    """Everything a learner can open for one concept: reading, lectures, notebooks."""
    chap = {ch["n"]: ch for ch in d["chapters"]}
    out = {"book": d["meta"]["siteUrl"], "chapter": None, "lectures": [], "notebooks": []}
    if c["ch"] is not None:
        ch = chap[c["ch"]]
        out["chapter"] = {"n": c["ch"], "label": ch_label(c["ch"], ch["title"]), "url": ch["url"]}
    for k in c["lectures"]:
        L = d["lectures"][k]
        out["lectures"].append({"course": L["course"], "n": L["n"], "title": L["title"], "url": L["url"],
                                "yt": YT.search(L["url"]).group(1)})
    for e in c["exercises"]:
        out["notebooks"].append({"title": ex_title(e), "path": e, "exercise": "/exercises/" in e,
                                 "colab": d["exerciseBase"]["colab"] + e, "github": d["exerciseBase"]["github"] + e})
    return out


def pora_block(c: dict, d: dict, C: dict, kids: dict) -> str:
    layer = {l["id"]: l["name"] for l in d["layers"]}[c["layer"]]
    m = materials(c, d)
    lines = [BEGIN, "## In Principles of Robot Autonomy", ""]
    if m["chapter"]:
        lines.append(f"- Read: [{m['chapter']['label']}]({m['chapter']['url']})")
    else:
        lines.append("- Assumed background for the book.")
    lines.append(f"- Stack layer: {layer} · {c['kind']}")
    for n in m["notebooks"]:
        lines.append(f"- Run: [{n['title']}]({n['colab']}) ([source]({n['github']}))")
    for L in m["lectures"]:
        lines.append(f"- Watch: [{L['course']} lecture {L['n']}: {L['title']}]({L['url']})")
    lines += ["", "### Key ideas", ""] + [f"{i}. {p}" for i, p in enumerate(c["points"], 1)]
    lines += ["", f"Try it: {c['tryIt']}"]
    if c["prereqs"]:
        lines += ["", "Needs first: " + ", ".join(f"[[{C[p]['wiki']}]]" for p in c["prereqs"])]
    if kids[c["id"]]:
        lines += ["", "Unlocks: " + ", ".join(f"[[{C[k]['wiki']}]]" for k in kids[c["id"]])]
    if c["related"]:
        lines += ["", "Related: " + ", ".join(f"[[{C[r]['wiki']}]]" for r in c["related"])]
    lines += ["", "Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; "
              "the book is the authoritative reference.", END]
    return "\n".join(lines)


def wiki_pages(d: dict, C: dict, kids: dict) -> dict[Path, str]:
    out = {}
    for c in d["concepts"]:
        p = WIKI / f"{c['wiki']}.md"
        block = pora_block(c, d, C, kids)
        cur = p.read_text() if p.exists() else None
        if cur is not None and "source: pora" not in cur:
            # An existing Brain University page: only the marked block is ours.
            if BEGIN in cur:
                out[p] = cur[: cur.index(BEGIN)] + block + cur[cur.index(END) + len(END):]
            else:
                out[p] = cur.rstrip() + "\n\n" + block + "\n"
        else:
            front = ["---", "source: pora", f"chapter: {c['ch'] if c['ch'] is not None else 'background'}",
                     f"layer: {c['layer']}", f"kind: {c['kind']}",
                     f"tags: [pora, robot-autonomy, {c['kind']}]", "---", ""]
            out[p] = "\n".join(front) + f"# {c['name']}\n\n{c['summary']}\n\n{block}\n"
    lines = ["---", "source: pora", "tags: [pora, robot-autonomy, course]", "---", "",
             "# Principles of Robot Autonomy", "",
             f"Free textbook by {', '.join(d['meta']['authors'][:-1])}, and {d['meta']['authors'][-1]} "
             f"({d['meta']['publisher']}, {d['meta']['year']}). Read it at {d['meta']['bookUrl']}; "
             f"exercises at {d['meta']['exercisesRepo']}.", "",
             d["meta"]["disclaimer"], ""]
    if d["meta"].get("resources"):
        lines += ["## Course resources", ""] + [f"- [{r['name']}]({r['url']}): {r['blurb']}" for r in d["meta"]["resources"]] + [""]
    for part in d["parts"]:
        lines.append(f"## {part['name']}")
        for n in part["chapters"]:
            ch = next(x for x in d["chapters"] if x["n"] == n)
            items = [c for c in d["concepts"] if c["ch"] == n]
            lines.append(f"- [{ch['title']}]({ch['url']}): " + ", ".join(f"[[{c['wiki']}]]" for c in items))
        lines.append("")
    lines.append("## Assumed background")
    lines.append(", ".join(f"[[{c['wiki']}]]" for c in d["concepts"] if c["ch"] is None))
    out[WIKI / "Principles_of_Robot_Autonomy.md"] = "\n".join(lines) + "\n"
    return out


def bu_lessons(d: dict, C: dict, kids: dict) -> dict:
    """Lessons for the Walk screen, built from the course content in study.json."""
    lessons = {}
    for c in d["concepts"]:
        m = materials(c, d)
        ideas = [{"h": "", "b": p} for p in c["points"]]
        if kids[c["id"]]:
            ideas.append({"h": "Unlocks.", "b": ", ".join(C[k]["name"] for k in kids[c["id"]]) + "."})
        lessons[c["wiki"]] = {
            "title": c["name"], "summary": c["summary"], "key_ideas": ideas,
            "worked_example": c["tryIt"],
            "evidence": [f"wiki/{c['wiki']}", "Principles of Robot Autonomy (porabook.com)"],
            "quiz": [{"q": c["check"]["q"], "choices": c["check"]["choices"],
                      "correct": c["check"]["correct"], "why": c["check"]["why"]}],
            "pora": m,
        }
    return lessons


def bu_js(d: dict, C: dict, kids: dict) -> str:
    nodes = [{"id": c["wiki"], "name": c["name"], "degree": len(c["prereqs"]) + len(kids[c["id"]])} for c in d["concepts"]]
    edges = [[C[p]["wiki"], c["wiki"]] for c in d["concepts"] for p in c["prereqs"]]
    payload = {"nodes": nodes, "edges": edges, "lessons": bu_lessons(d, C, kids),
               "chapters": {c["wiki"]: c["ch"] for c in d["concepts"]},
               "ids": {c["wiki"]: c["id"] for c in d["concepts"]}}
    return f"""/* Generated by courses/pora/build.py. Do not edit by hand.
 * Adds the Principles of Robot Autonomy course to window.BU_DATA so routes
 * planned in the PoRA Atlas can be walked as Brain University tours, with the
 * course's lectures, notebooks, and concept checks inside each lesson. */
(function () {{
  var P = {json.dumps(payload, ensure_ascii=False)};
  var B = window.BU_DATA;
  if (!B) return;
  var cid = B.CLUSTERS.length;
  B.CLUSTERS.push({{ id: cid, name: "Robot autonomy (PoRA)", color: "#c2410c", emoji: "\\u2699",
    blurb: "Principles of Robot Autonomy: dynamics, control, planning, perception, estimation, and learning." }});
  var have = {{}};
  B.NODES.forEach(function (n) {{ have[n.id] = n; }});
  P.nodes.forEach(function (n) {{ if (!have[n.id]) B.NODES.push({{ id: n.id, name: n.name, degree: n.degree, cluster: cid }}); }});
  P.edges.forEach(function (e) {{ B.EDGES.push(e); }});
  var names = {{}};
  Object.keys(P.lessons).forEach(function (k) {{
    var L = P.lessons[k];
    var cur = B.LESSONS[k] || (have[k] ? B.lessonFor(k) : null);
    // An existing Brain University lesson keeps its own text; the course's key ideas,
    // concept check, and materials are added to it.
    B.LESSONS[k] = cur ? Object.assign({{}}, cur, {{
      key_ideas: (cur.key_ideas || []).concat(L.key_ideas),
      quiz: L.quiz.concat(cur.quiz || []),
      pora: L.pora
    }}) : L;
    names[k] = B.LESSONS[k].title || L.title;
  }});
  B.PORA = {{ clusterId: cid, lessons: P.lessons, names: names,
    // Shares progress with the Atlas (same origin, same localStorage key).
    isLearned: function (k) {{ try {{ return JSON.parse(localStorage.getItem("pora-done") || "[]").indexOf(P.ids[k]) >= 0; }} catch (e) {{ return false; }} }},
    markLearned: function (k) {{
      if (!P.ids[k]) return;
      try {{ var s = JSON.parse(localStorage.getItem("pora-done") || "[]"); if (!Array.isArray(s)) s = [];
        if (s.indexOf(P.ids[k]) < 0) {{ s.push(P.ids[k]); localStorage.setItem("pora-done", JSON.stringify(s)); }} }} catch (e) {{}}
    }} }};
  // Build a Walk-screen tour from an ordered list of PoRA wiki ids.
  B.poraTour = function (steps, key) {{
    var seen = {{}};
    var stops = (steps || []).filter(function (s) {{
      if (!P.lessons[s] || seen[s]) return false; seen[s] = 1; return true;
    }}).map(function (s, i, arr) {{
      var prev = arr[i - 1], ch = P.chapters[s];
      var where = ch === null || ch === undefined ? "assumed background" : ch === 0 ? "the software chapter" : "chapter " + ch;
      return {{
        node: s, cluster: have[s] ? have[s].cluster : cid,
        kind: arr.length === 1 ? "capstone" : i === 0 ? "start" : i === arr.length - 1 ? "capstone" : "deepen",
        rationale: i === 0
          ? "Start with " + names[s] + " (" + where + ")." + (arr.length > 1 ? " Everything later on this route builds on it." : "")
          : "Next is " + names[s] + " (" + where + "), which builds on " + names[prev] + " and the stops before it."
      }};
    }});
    if (!stops.length) return null;
    B.TOURS[key] = stops;
    return key;
  }};
}})();
"""


def atlas(d: dict) -> tuple[str, str]:
    tpl = (HERE / "atlas.template.html").read_text()
    body = tpl.replace("/*PORA_DATA*/null", json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    standalone = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
                  "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
                  "</head>\n<body>\n" + body + "\n</body>\n</html>\n")
    return body, standalone


def outputs(d: dict) -> dict[Path, str]:
    C = {c["id"]: c for c in d["concepts"]}
    kids = {c["id"]: [] for c in d["concepts"]}
    for c in d["concepts"]:
        for p in c["prereqs"]:
            kids[p].append(c["id"])
    out = wiki_pages(d, C, kids)
    out[DESIGN / "pora_bu.js"] = bu_js(d, C, kids)
    _, standalone = atlas(d)
    out[DESIGN / "pora-atlas.html"] = standalone
    return out


def main() -> None:
    check = "--check" in sys.argv[1:]
    d = load()
    validate(d)
    out = outputs(d)
    if check:
        stale = [str(p.relative_to(ROOT)) for p, t in out.items() if not p.exists() or p.read_text() != t]
        if stale:
            fail([f"{s} is out of date; run python3 courses/pora/build.py" for s in stale])
        print(f"PoRA: {len(d['concepts'])} concepts valid, {len(out)} outputs up to date")
        return
    for p, t in out.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_text() != t:
            p.write_text(t)
    body, _ = atlas(d)
    DIST.mkdir(exist_ok=True)
    (DIST / "pora-atlas.html").write_text(body)
    print(f"PoRA: {len(d['concepts'])} concepts valid; wiki, atlas, and Brain University course built")


if __name__ == "__main__":
    main()
