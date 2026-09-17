# React Framework

Deep reference for React resources in `library/React/`. For the shared resource
model, required-file rules, and cross-framework comparison, start with
`agents/resources/resources.md`; for the QA layer, `agents/resources/qa.md`.

## Where React resources live

`library/React/` contains the three content types as sibling trees:

- `library/React/Components/` — 22 component families, 293 variants
  (Accordion, Alerts, Breadcrumbs, Buttons, Calendar, Cards, Checkboxes,
  DatePicker, Dialogs, Dropdowns, FormFields, Inputs, Navbar, Pagination,
  Radios, Selects, Sidebar, Switches, Tables, Tabs, Textareas, Tooltips).
- `library/React/Sections/` — 13 section families, 56 variants
  (CTA, Comparison, Contact, FAQ, Features, Hero, Integrations, Logo-Cloud,
  Newsletter, Pricing, Stats, Team, Testimonials).
- `library/React/Templates/` — 1 template (`spray-art-school`).

Framework-level documents:

- `library/React/DESIGN_TOKENS.md` — root `--ds-*` token specification.
- `library/React/Sections/DESIGN_TOKENS.md` — child spec governing the four
  section design directions (Minimal, Dark Premium, Bento, Neo-Brutalist).
- `library/React/index.html`, `library/React/Components/index.html`,
  `library/React/Sections/index.html` — browsable galleries that fetch
  `snippets-index.json`.

## Components — structure and files

Each variant folder contains exactly five files. Real example:
`library/React/Components/Buttons/split-button/`.

- `code.tsx` — PRIMARY authored implementation. TypeScript-first: proper prop
  interfaces (often extending `ButtonHTMLAttributes` and siblings), no `any`,
  Tailwind utility classes consuming the `--ds-*` tokens via arbitrary values
  (e.g. `bg-[var(--ds-color-primary)]`).
- `code.jsx` — JavaScript parity build of `code.tsx` (same API, classes, and
  behavior with TS syntax stripped). Verify parity when editing either side.
- `preview.html` — self-contained runnable demo: Tailwind CDN + React 18 UMD +
  Babel standalone, an inline `--ds-*` token block with a persisted no-flash
  light/dark toggle, the component itself, and a per-component `Showcase`.
- `metadata.json` — see schema below.
- `README.md` — per-variant documentation.

Component metadata (observed in `library/React/Components/Tabs/tabs/metadata.json`):
`id`, `name`, `slug`, `component`, `family`, `variant`, `description`,
`framework: "React"`, `language: "TSX"`, `languages: ["JSX","TSX"]`,
`technology: "react"` (lowercase here — see note under Sections),
`type: "component"`, `category`, `subcategory`, `styling: "Tailwind CSS"`,
`tags`, `features`, `related`.

Code conventions enforced by review/QA (not by a linter in-repo):

- No `any`; no inline `style=` in `code.tsx`/`code.jsx`.
- No hardcoded hex except `#000` inside the `color-mix(...88%,#000)` hover
  darkening recipe.
- Real native semantics (real `<button>`/`<input>`/`<table>`, ARIA roles,
  `aria-*` wiring, keyboard models) and `focus-visible` rings.
- `motion-reduce:transition-none` guards on transitions.

Observed examples: `library/React/Components/Buttons/solid-button/`,
`library/React/Components/Tabs/tabs/` (compound multi-export family),
`library/React/Components/Calendar/calendar/`.

## Sections — structure and files

Each variant folder contains exactly THREE files — no `code.jsx`, no
`README.md`. Real example: `library/React/Sections/Hero/minimal/`.

- `code.tsx` — the only authored file. Exports ONE component
  (`HeroSection`, `FeaturesSection`, …) with all content as overridable props
  (authored realistic defaults; invented products, no external images).
- `metadata.json`
- `preview.html` — generated-style page; sections mount FULL-BLEED via a
  `.ds-stage` escape from the showcase column.

Section metadata (observed in `library/React/Sections/Hero/minimal/metadata.json`):
`id` (e.g. `hero-minimal`), `name`, `technology: "React"`, `category: "Sections"`,
`subcategory` (= family name), `family`, `direction` (Minimal | Dark Premium |
Bento | Neo-Brutalist), `type: "section"`, `tags`, `responsive`,
`browserSupport`, `dependencies`.

Family composition: most families have exactly the four direction-named
variants; `Features` has 8 variants. See
`library/React/Sections/Features/` vs `library/React/Sections/Hero/`.

Known inconsistency (do not "fix" silently): section metadata uses
`technology: "React"` (capitalized) while component metadata uses
`technology: "react"`. The index builder tolerates this; verify against
`scripts/tooling/indexing/rebuild_index.py` before changing either.

## Templates

`library/React/Templates/spray-art-school/` is a complete Vite + TypeScript +
Tailwind application, not a snippet collection:

- Build setup: `package.json` (react 18, react-router-dom, framer-motion,
  vite, tailwindcss, typescript; scripts `dev`/`build`/`preview`),
  `tsconfig.json`, `tailwind.config.ts`, `postcss.config.js`.
- App code in `src/`: `main.tsx`, `App.tsx`, `pages/` (Home, Work, About,
  Contact routes), `sections/`, `components/`, `data/`, `styles/globals.css`.
- Root `index.html` (Vite entry) + `preview.html` + `README.md` +
  `metadata.json` (`type: "template"`, `pages: 4`,
  `style: "diy-zine-street-art"`) + `AGENTS.md` (required for templates —
  enforced by `scripts/tooling/validators/validate.py`).

## How React resources are validated

- Structure + metadata + index consistency:
  `scripts/tooling/validators/validate.py` (React is a scanned technology,
  `React/Sections/` is first-class; templates must ship `AGENTS.md`).
- Deeper audit: `scripts/tooling/validators/deep_check.py`.
- Per-family Playwright QA harnesses in `scripts/qa/resources/`:
  `_qa_react_button.py`, `_qa_react_tabs.py`, `_qa_react_dialogs.py`,
  `_qa_react_tables.py`, `_qa_react_sections_features.py`,
  `_qa_react_sections_testimonials.py`, etc. They serve `preview.html` from
  `library/React/...` at `http://localhost:8765` and are invoked per slug,
  e.g. `python3 scripts/qa/resources/_qa_react_button.py split-button`.
  Harnesses exist for most component and section families — but NOT for every
  one (e.g. no `_qa_react_sections_hero.py`); check the directory before
  assuming a harness exists.

Known drift risk: older docs reference root-level `_gen_react_*.py` generator
scripts with `--check` drift detection. Those generators are NOT present in
the current tree (`scripts/tooling/generators/` only contains Tailwind-section
builders and site generation). Treat the committed `code.tsx`/`preview.html`
files as canonical; there is no in-repo regenerator to re-run.

## CLI behavior

React resources are indexed in `snippets-index.json` under technology
`React` and installed by the CLI like any other resource:
resolution in `cli/src/registry/resolver.js`, writing in
`cli/src/install/writer.js`. CLI details: `agents/resources/cli.md`.

## Rules of thumb for agents

1. Changing `code.tsx`? Mirror every change in `code.jsx` (same props,
   classes, behavior) and keep `preview.html` runnable standalone.
2. Adding a Section? Follow the four-direction architecture and the metadata
   key set above; read `library/React/Sections/DESIGN_TOKENS.md` first.
3. Adding a Component? Five files, TSX-first, compound families export
   multiple named primitives (see `library/React/Components/Tabs/tabs/code.tsx`).
4. Re-run `scripts/tooling/validators/validate.py` and the relevant QA
   harness after any change (see `agents/resources/qa.md`).
