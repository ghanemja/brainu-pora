# PoRA Atlas

An unofficial, interactive study map for [Principles of Robot Autonomy](https://porabook.com/) (Gammelli, Lorenzetti, Luo, Zardini, Pavone; Cambridge University Press, 2026), built into Brain University.

The book teaches the autonomy stack as a whole: dynamics and control, planning, perception, estimation, and decision making. The Atlas draws that stack directly. It has 69 concepts across all 19 chapters, each linked to its chapter, the matching runnable notebooks from [StanfordASL/pora-exercises](https://github.com/StanfordASL/pora-exercises), and the related Stanford AA174A and AA203 lecture recordings. Every one of the 40 published notebooks is mapped to a concept.

## What it does

- **Syllabus.** The book's four parts and 19 chapters (plus the software chapter and assumed background) as cards: the concepts in each chapter, how many lectures and notebooks cover it, a link to read it, and progress.
- **Stack map.** Concepts in six lanes (foundations at the bottom), ordered left to right by prerequisite depth, with zoom and lane filters. Square boxes are classical methods, rounded boxes are learned ones.
- **Lectures.** All 33 Stanford recordings (AA174A and AA203), playable in the page, each tagged with the concepts it covers.
- **Notebooks.** All 40 notebooks from the exercises repo, grouped by chapter, marked exercise or demo, with one-click Colab and GitHub links.
- **Concept cards.** Three key ideas, the lectures (inline), notebooks, the chapter to read, a concept check with explanation, a try-it prompt, and what the concept needs and unlocks.
- **Route planner.** Pick a background and a goal; the Atlas skips what you know and orders the rest by prerequisites, then chapter.
- **Progress.** "I've learned this" (or a correct concept check) is saved in the browser and shared with the Walk screen.
- **Brain University handoff.** Inside Brain University (Human view, Courses tab) any route or chapter can be walked as a guided tour. Each stop shows the key ideas, plays the lecture inline, links the notebooks, and asks the concept check.
- **Agent view.** ATP's L3 curriculum includes a Robot autonomy track (PORA-I to PORA-IV), and the open Controls & robotics expert request lists the book as a training corpus.

## Files

| Path | What it is |
| --- | --- |
| `courses/pora/pora.json` | Concepts, prerequisites, chapters, notebooks, lectures, backgrounds, official resource links |
| `courses/pora/study.json` | Per concept: three key ideas, a four-option concept check with explanation, and a try-it prompt |
| `courses/pora/atlas.template.html` | The course page; data is inlined at build time |
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
