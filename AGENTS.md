# AGENTS.md

Rules for any agent (Claude, Codex, Copilot, or anyone else) working in this repo.

## Design

- **Light mode only.** No dark themes, dark panels, dark cards, dark modals, dark
  graph or video backgrounds, and no dark-mode toggle. Every surface is paper or a
  light neutral. A dimmed backdrop behind a modal is fine; the modal itself is light.
  - The one exception is the lesson's chalkboard. It is slate on purpose, because it
    is a physical material (chalk on a board), not a dark theme. Don't extend it to
    other surfaces.
- **No generic fonts.** Don't use Inter, Roboto, Arial, Helvetica, system-ui,
  Open Sans, Work Sans, Nunito, Varela Round, or a bare `sans-serif` stack as the
  face people read. Pick each face for its job, and say why in a comment where it
  is set. The current set:
  - **Permanent Marker**: headings (Splatform's marker medium)
  - **Caveat** and **Kalam**: handwriting, notebook pages, chalk
  - **Newsreader**: anything you read (summaries, questions, explanations)
  - **Bricolage Grotesque**: interface (nav, buttons, labels, metadata)
- **Use the art-asset library (Splatform, `design/prototype/vendor/`)** for
  materials: marker for notebook pages and headings, charcoal for the chalkboard,
  cork and paper textures for maps and cards. Avoid the default "AI app" look:
  gradients, glassy cards, purple accents, emoji icons.
- **Keep it simple to follow.** Each screen has one clear next step. No hidden
  taps, no props without a job, no modal you have to discover.
