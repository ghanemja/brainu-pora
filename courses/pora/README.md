# PoRA Atlas

An unofficial, interactive study map for [Principles of Robot Autonomy](https://porabook.com/) (Gammelli, Lorenzetti, Luo, Zardini, Pavone; Cambridge University Press, 2026), built into Brain University.

The book teaches the autonomy stack as a whole: dynamics and control, planning, perception, estimation, and decision making. The Atlas draws that stack directly. It has 69 concepts across all 19 chapters, each linked to its chapter, the matching runnable notebooks from [StanfordASL/pora-exercises](https://github.com/StanfordASL/pora-exercises), and the related Stanford AA174A and AA203 lecture recordings. Every one of the 40 published notebooks is mapped to a concept.

## What it does

One clear path, one question per screen:

1. **Where are you starting from?** New to robotics, or coming from ML, controls, or software.
2. **What do you want to be able to do?** Eight plain-language goals (follow a path, plan around obstacles, know where the robot is, build a map, and so on), or the whole book in order.
3. **Your path.** A short ordered list of lessons that skips what your background already covers. Inside Brain University, **Start the walk** hands it to The Walk, one lesson per stop: key ideas, the Stanford lecture (played inline), the notebook (one click to Colab), the chapter to read, and a quick check. Standalone, the same lessons open on the page.

Two optional extras sit below the card: a refresher walk through the book's assumed background (linear algebra, calculus and ODEs, optimization, neural networks), which also has its own cluster in the Brain University graph, and a collapsed list to open any single chapter. Progress is saved in the browser and shared with The Walk.

The Agent view's L3 curriculum includes a Robot autonomy track (PORA-I to PORA-IV).

## Files

| Path | What it is |
| --- | --- |
| `courses/pora/pora.json` | Concepts, prerequisites, chapters, notebooks, lectures, backgrounds, goals, resource links |
| `courses/pora/study.json` | Per concept: three key ideas, a four-option concept check with explanation, and a try-it prompt |
| `courses/pora/atlas.template.html` | The Courses screen (two questions, then a path); data is inlined at build time |
| `courses/pora/build.py` | Validates the data and generates every output below |
| `design/courses/pora-atlas.html` | Standalone course page, served by Brain University |
| `design/courses/pora_bu.js` | Adds the course cluster, lessons (with materials and checks), and tours to `BU_DATA` |
| `design/screens/courses.jsx` | The Courses tab that embeds the page and starts tours |
| `wiki/concepts/*.md` | 63 concept pages plus a PoRA section on 6 existing pages |

Rebuild after editing `pora.json` or `study.json`:

```
python3 courses/pora/build.py          # validate and write outputs
python3 courses/pora/build.py --check  # validate and fail if outputs are stale (runs in CI)
```

Validation rejects unknown prerequisites, prerequisite cycles, missing study notes, malformed checks (four distinct choices, one correct), bad notebook paths, non-YouTube lecture links, and non-https URLs. The build is idempotent. Existing Brain University pages are only touched between `<!-- pora:begin -->` and `<!-- pora:end -->`.

## Accuracy

Chapter placement follows the book's published section headings. Concept summaries, key ideas, concept checks, prerequisite links, and the lecture-to-concept mapping are an independent reading of the material, not the authors' own, and have not been reviewed by them. Corrections are welcome; the book is the authoritative reference.

## License

Atlas code is MIT; concept summaries and graph data are CC BY 4.0. See [LICENSE](LICENSE). The book, its exercises, and its lectures are not covered and belong to their authors and publishers.
