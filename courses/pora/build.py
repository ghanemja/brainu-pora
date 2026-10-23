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

Run:  python3 courses/pora/build.py
"""

from __future__ import annotations

import json
import random
import re
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
    for c in d["concepts"]:
        c.setdefault("wiki", page_id(c["name"]))
        c.setdefault("exercises", [])
        c.setdefault("lectures", [])
        c.setdefault("related", [])
    return d


def ex_title(path: str) -> str:
    t = path.rsplit("/", 1)[-1].removesuffix(".ipynb").replace("_", " ").title()
    for w in ["Lqr", "Mpc", "Pid", "Rrt", "Prm", "Icp", "Cnn", "Ekf", "Ukf", "Slam", "Tpbvp", "Jax", "Sift"]:
        t = re.sub(rf"\b{w}\b", w.upper(), t)
    return t


def pora_block(c: dict, d: dict, C: dict, kids: dict) -> str:
    layer = {l["id"]: l["name"] for l in d["layers"]}[c["layer"]]
    chap = {ch["n"]: ch for ch in d["chapters"]}
    lines = [BEGIN, "## In Principles of Robot Autonomy", ""]
    if c["ch"] is not None:
        ch = chap[c["ch"]]
        label = CH_LABEL.get(c["ch"], f"Chapter {c['ch']}: {ch['title']}")
        lines.append(f"- Read: [{label}]({ch['url']})")
    else:
        lines.append("- Assumed background for the book.")
    lines.append(f"- Stack layer: {layer} · {c['kind']}")
    for e in c["exercises"]:
        lines.append(f"- Run: [{ex_title(e)}]({d['exerciseBase']['colab']}{e}) "
                     f"([source]({d['exerciseBase']['github']}{e}))")
    for l in c["lectures"]:
        L = d["lectures"][l]
        lines.append(f"- Watch: [{L['course']} lecture {L['n']}: {L['title']}]({L['url']})")
    if c["prereqs"]:
        lines += ["", "Needs first: " + ", ".join(f"[[{C[p]['wiki']}]]" for p in c["prereqs"])]
    if kids[c["id"]]:
        lines += ["", "Unlocks: " + ", ".join(f"[[{C[k]['wiki']}]]" for k in kids[c["id"]])]
    if c["related"]:
        lines += ["", "Related: " + ", ".join(f"[[{C[r]['wiki']}]]" for r in c["related"])]
    lines += ["", "Part of [[Principles_of_Robot_Autonomy]]. Summary and links from the unofficial PoRA Atlas; "
              "the book is the authoritative reference.", END]
    return "\n".join(lines)


def write_wiki(d: dict, C: dict, kids: dict) -> tuple[int, int]:
    created = updated = 0
    for c in d["concepts"]:
        p = WIKI / f"{c['wiki']}.md"
        block = pora_block(c, d, C, kids)
        if p.exists() and BEGIN not in p.read_text() and "source: pora" not in p.read_text():
            p.write_text(p.read_text().rstrip() + "\n\n" + block + "\n")
            updated += 1
        elif p.exists() and BEGIN in p.read_text() and "source: pora" not in p.read_text():
            body = p.read_text()
            body = body[: body.index(BEGIN)] + block + body[body.index(END) + len(END):]
            p.write_text(body)
            updated += 1
        else:
            front = ["---", "source: pora", f"chapter: {c['ch'] if c['ch'] is not None else 'background'}",
                     f"layer: {c['layer']}", f"kind: {c['kind']}",
                     f"tags: [pora, robot-autonomy, {c['kind']}]", "---", ""]
            p.write_text("\n".join(front) + f"# {c['name']}\n\n{c['summary']}\n\n{block}\n")
            created += 1
    # course index
    lines = ["---", "source: pora", "tags: [pora, robot-autonomy, course]", "---", "",
             "# Principles of Robot Autonomy", "",
             f"Free textbook by {', '.join(d['meta']['authors'][:-1])}, and {d['meta']['authors'][-1]} "
             f"({d['meta']['publisher']}, {d['meta']['year']}). Read it at {d['meta']['bookUrl']}; "
             f"exercises at {d['meta']['exercisesRepo']}.", "",
             d["meta"]["disclaimer"], ""]
    for part in d["parts"]:
        lines.append(f"## {part['name']}")
        for n in part["chapters"]:
            ch = next(x for x in d["chapters"] if x["n"] == n)
            items = [c for c in d["concepts"] if c["ch"] == n]
            lines.append(f"- [{ch['title']}]({ch['url']}): " + ", ".join(f"[[{c['wiki']}]]" for c in items))
        lines.append("")
    lines.append("## Assumed background")
    lines.append(", ".join(f"[[{c['wiki']}]]" for c in d["concepts"] if c["ch"] is None))
    (WIKI / "Principles_of_Robot_Autonomy.md").write_text("\n".join(lines) + "\n")
    return created, updated


def bu_lessons(d: dict, C: dict, kids: dict) -> dict:
    """Lessons for the Walk screen. Quizzes are built from the prerequisite graph."""
    chap = {ch["n"]: ch for ch in d["chapters"]}
    rng = random.Random(7)

    def ancestors(i):
        out, stack = set(), list(C[i]["prereqs"])
        while stack:
            x = stack.pop()
            if x not in out:
                out.add(x)
                stack += C[x]["prereqs"]
        return out

    lessons = {}
    for c in d["concepts"]:
        ideas = []
        if c["ch"] is not None:
            ideas.append({"h": "Read.", "b": f"{CH_LABEL.get(c['ch'], 'Chapter %d: %s' % (c['ch'], chap[c['ch']]['title']))} ({chap[c['ch']]['url']})"})
        if c["exercises"]:
            ideas.append({"h": "Run.", "b": "; ".join(f"{ex_title(e)} ({d['exerciseBase']['colab']}{e})" for e in c["exercises"])})
        if c["lectures"]:
            ideas.append({"h": "Watch.", "b": "; ".join(f"{d['lectures'][l]['course']} {d['lectures'][l]['n']}: {d['lectures'][l]['title']} ({d['lectures'][l]['url']})" for l in c["lectures"])})
        if kids[c["id"]]:
            ideas.append({"h": "Unlocks.", "b": ", ".join(C[k]["name"] for k in kids[c["id"]]) + "."})
        quiz = []
        if c["prereqs"]:
            right = rng.choice(c["prereqs"])
            excluded = ancestors(c["id"]) | {c["id"]}
            wrong = [x["id"] for x in d["concepts"] if x["id"] not in excluded and x["layer"] != "F"]
            rng.shuffle(wrong)
            choices = [right] + wrong[:3]
            rng.shuffle(choices)
            quiz.append({
                "q": f"Which of these do you need before {c['name']}?",
                "choices": [C[x]["name"] for x in choices],
                "correct": choices.index(right),
                "why": f"{C[right]['name']} is a direct prerequisite. The others sit elsewhere in the stack and are not needed first.",
            })
        lessons[c["wiki"]] = {
            "title": c["name"], "summary": c["summary"], "key_ideas": ideas,
            "worked_example": "Open the first notebook above and run it end to end before reading the derivation."
                              if c["exercises"] else "Work through the chapter's examples, then explain the idea in one paragraph without notes.",
            "evidence": [f"wiki/{c['wiki']}", "Principles of Robot Autonomy (porabook.com)"],
            "quiz": quiz,
        }
    return lessons


def write_bu_js(d: dict, C: dict, kids: dict) -> None:
    nodes = [{"id": c["wiki"], "name": c["name"], "degree": len(c["prereqs"]) + len(kids[c["id"]])} for c in d["concepts"]]
    edges = [[C[p]["wiki"], c["wiki"]] for c in d["concepts"] for p in c["prereqs"]]
    payload = {"nodes": nodes, "edges": edges, "lessons": bu_lessons(d, C, kids),
               "names": {c["wiki"]: c["name"] for c in d["concepts"]},
               "chapters": {c["wiki"]: c["ch"] for c in d["concepts"]}}
    js = f"""/* Generated by courses/pora/build.py. Do not edit by hand.
 * Adds the Principles of Robot Autonomy course to window.BU_DATA so routes
 * planned in the PoRA Atlas can be walked as Brain University tours. */
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
  Object.keys(P.lessons).forEach(function (k) {{
    var cur = B.LESSONS[k] || (have[k] ? B.lessonFor(k) : null);
    // Keep an existing Brain University lesson and add the PoRA reading, notebooks, and lectures to it.
    B.LESSONS[k] = cur ? Object.assign({{}}, cur, {{ key_ideas: (cur.key_ideas || []).concat(P.lessons[k].key_ideas) }}) : P.lessons[k];
  }});
  B.PORA = {{ clusterId: cid, lessons: P.lessons, names: P.names }};
  // Build a Walk-screen tour from an ordered list of PoRA wiki ids.
  B.poraTour = function (steps, key) {{
    var stops = steps.filter(function (s) {{ return P.lessons[s]; }}).map(function (s, i, arr) {{
      var prev = arr[i - 1], ch = P.chapters[s];
      var where = ch === null || ch === undefined ? "assumed background" : ch === 0 ? "the software chapter" : "chapter " + ch;
      return {{
        node: s, cluster: have[s] ? have[s].cluster : cid,
        kind: i === 0 ? "start" : i === arr.length - 1 ? "capstone" : "deepen",
        rationale: i === 0
          ? "Start with " + P.names[s] + " (" + where + "). Everything later on this route builds on it."
          : "Next is " + P.names[s] + " (" + where + "), which builds on " + P.names[prev] + " and the stops before it."
      }};
    }});
    B.TOURS[key] = stops;
    return key;
  }};
}})();
"""
    DESIGN.mkdir(parents=True, exist_ok=True)
    (DESIGN / "pora_bu.js").write_text(js)


def write_atlas(d: dict) -> None:
    tpl = (HERE / "atlas.template.html").read_text()
    body = tpl.replace("/*PORA_DATA*/null", json.dumps(d, ensure_ascii=False, separators=(",", ":")))
    DIST.mkdir(exist_ok=True)
    (DIST / "pora-atlas.html").write_text(body)
    standalone = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
                  "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
                  "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
                  "body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n"
                  "</head>\n<body>\n" + body + "\n</body>\n</html>\n")
    DESIGN.mkdir(parents=True, exist_ok=True)
    (DESIGN / "pora-atlas.html").write_text(standalone)


def main() -> None:
    d = load()
    C = {c["id"]: c for c in d["concepts"]}
    kids = {c["id"]: [] for c in d["concepts"]}
    for c in d["concepts"]:
        for p in c["prereqs"]:
            kids[p].append(c["id"])
    created, updated = write_wiki(d, C, kids)
    write_bu_js(d, C, kids)
    write_atlas(d)
    print(f"wiki: {created} pages created, {updated} existing pages linked; atlas + BU course built")


if __name__ == "__main__":
    main()
