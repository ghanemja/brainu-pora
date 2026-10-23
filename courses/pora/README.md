# PoRA Atlas

An unofficial, interactive study map for [Principles of Robot Autonomy](https://porabook.com/) (Gammelli, Lorenzetti, Luo, Zardini, Pavone; Cambridge University Press, 2026), built into Brain University.

The book teaches the autonomy stack as a whole: dynamics and control, planning, perception, estimation, and decision making. The Atlas draws that stack directly. It has 69 concepts across all 19 chapters, each linked to its chapter, the matching runnable notebooks from [StanfordASL/pora-exercises](https://github.com/StanfordASL/pora-exercises), and the related Stanford AA174A and AA203 lecture recordings. Every one of the 40 published notebooks is mapped to a concept.

## What it does

- **Stack view.** Concepts sit in six lanes, foundations at the bottom, ordered left to right by prerequisite depth. Square boxes are classical methods and rounded boxes are learned ones, so you can see where the two halves of the field meet.
- **Route planner.** Pick a background (new to robotics, ML, controls, or software) and a goal concept. The Atlas removes what you already know and orders the rest by prerequisite links, then by chapter.
- **Concept cards.** What a concept needs, what it unlocks, and where to read, run, and watch it.
- **Brain University handoff.** Inside Brain University (Human view, Courses tab), any route can be walked as a guided tour, with a short quiz at each stop generated from the prerequisite graph.
- **Agent view.** ATP's L3 curriculum gains a Robot autonomy track (PORA-I to PORA-IV), and the open Controls & robotics expert request now lists the book as a training corpus.

## Files

| Path | What it is |
| --- | --- |
| `courses/pora/pora.json` | Source of truth: concepts, prerequisites, chapters, notebooks, lectures, backgrounds |
| `courses/pora/atlas.template.html` | The Atlas page; data is inlined at build time |
| `courses/pora/build.py` | Generates every output below |
| `design/courses/pora-atlas.html` | Standalone Atlas, served by Brain University |
| `design/courses/pora_bu.js` | Adds the course cluster, lessons, and quizzes to `BU_DATA` |
| `design/screens/courses.jsx` | The Courses tab that embeds the Atlas and starts tours |
| `wiki/concepts/*.md` | 63 new concept pages plus a PoRA section on 6 existing pages |

Rebuild after editing `pora.json`:

```
python3 courses/pora/build.py
```

The build is idempotent. Existing Brain University pages are only touched between `<!-- pora:begin -->` and `<!-- pora:end -->`.

## Accuracy

Chapter placement follows the book's published section headings. Concept summaries, prerequisite links, and the lecture-to-concept mapping are an independent reading of the material, not the authors' own. Corrections are welcome; the book is the authoritative reference.

## License

Atlas code is MIT; concept summaries and graph data are CC BY 4.0. See [LICENSE](LICENSE). The book, its exercises, and its lectures are not covered and belong to their authors and publishers.
