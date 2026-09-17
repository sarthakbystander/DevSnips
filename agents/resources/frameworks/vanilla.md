# Vanilla Framework

Deep reference for Vanilla resources in `library/Vanilla/`. For the shared
resource model start with `agents/resources/resources.md`; for QA see
`agents/resources/qa.md`.

## Where Vanilla resources live

`library/Vanilla/` holds the three content types:

- `library/Vanilla/Components/` — 17 families, 126 variants (Accordions,
  Buttons, Cards, Forms, Loaders, Modals, Navigation with legacy
  sub-families such as `Navigation/Breadcrumb/`, Toasts, Tooltips, …).
- `library/Vanilla/Sections/` — 16 families, 65 neo-brutalist website
  sections (Contact, Content, CTA, FAQ, Features, Footer, Gallery, Hero,
  Logos, Navigation, Pricing, Process, Products, Statistics, Team,
  Testimonials).
- `library/Vanilla/Templates/` — 8 templates (agency, developer-portfolio,
  documentation-site, event-conference, html5-boilerplate, job-board,
  product-launch, saas-dashboard).

Framework-level documents and galleries:

- `library/Vanilla/Components/tokens.css` +
  `library/Vanilla/Components/DESIGN_TOKENS.md` — the Swiss neo-minimal
  `--ds-*` token system (canonical token source).
- `library/Vanilla/Sections/sections-index.html`,
  `sections-showcase.html`, `sections-gallery.md` — section galleries (the
  showcase embeds each section in an isolated `srcdoc` iframe).

## Components

Each variant folder contains exactly three files: `code.html`,
`metadata.json`, `README.md`. Real examples:
`library/Vanilla/Components/Accordions/accordion-panel/`,
`library/Vanilla/Components/Buttons/split-button/`.

- `code.html` is SELF-CONTAINED: inline `<style>` + inline `<script>` inside
  the snippet. Legacy components ship as copy-paste-ready fragments WITHOUT a
  `<!DOCTYPE>` wrapper (the absence is an accepted convention, not a bug —
  `scripts/tooling/validators/validate.py` and
  `scripts/qa/resources/qa_vanilla.py` treat it as informational).
- Tokens: components reference `var(--ds-<token>, <original-fallback>)` so
  they render identically standalone AND re-theme together when
  `library/Vanilla/Components/tokens.css` is included once (shadcn-style CSS
  variables). A full Swiss `:root{--ds-*}` block + dark-mode override is
  embedded in each component's `<style>`.
- Quality bar (enforced): `prefers-reduced-motion` guards on all
  transitions/animations, `:focus-visible` rings, ARIA/roles on custom
  widgets, and `<button>`/`<a>`/native-input semantics (or
  `tabindex`+`role="button"`+Enter/Space handlers) for click-wired controls.
  Pure status displays (spinners, progress) need ARIA but not keyboard.
- Metadata follows the family/variant schema (`name`, `slug` = folder name,
  `component`, `family`, `variant`, `description`, `framework`, `language`,
  `tags`, `related`, `features`) — see the schema in
  `agents/resources/resources.md` and a real example in
  `library/Vanilla/Components/Buttons/split-button/metadata.json`.

## Sections

Neo-brutalist website sections. Each variant folder contains exactly three
files: `code.html`, `metadata.json`, `README.md`. Real example:
`library/Vanilla/Sections/Hero/hero-minimal/`.

- `code.html` is a FULL standalone page: `<!DOCTYPE html>` with inline
  `<style>` + `<script>` and `<body class="nb">`.
- These sections deliberately keep their own token system (`--bg`,
  `--surface`, `--foreground`, `--muted`, `--border`, `--primary`, `--accent`,
  `--pink`, `--lime`, `--cyan`, `--radius`, `--shadow`, …) with light + dark
  via `prefers-color-scheme` — they are NOT migrated to the `--ds-*` system.
- Metadata carries `category: "sections"`, `type: "section"`, `technology`,
  plus `responsive`, `darkMode`, `accessibility`, `browserSupport`,
  `dependencies`, `source`, `related` (observed in
  `library/Vanilla/Sections/Hero/hero-minimal/metadata.json`).
- `Navigation` in Sections contributes only section-level variants; the
  legacy navigation sub-families live under
  `library/Vanilla/Components/Navigation/`.

## Templates

All 8 templates share the canonical layout — the root holds `preview.html` +
`metadata.json` + `README.md` + `AGENTS.md` (required, enforced by
`scripts/tooling/validators/validate.py`); ALL code lives in `pages/`:

- Modular templates (agency, developer-portfolio, documentation-site,
  event-conference, job-board, product-launch): `pages/code.html` +
  `pages/style.css` (the `--ds-*` design system) + `pages/script.js`;
  `preview.html` is self-contained (inlines the CSS+JS). Example:
  `library/Vanilla/Templates/agency/` (root has exactly `AGENTS.md`,
  `metadata.json`, `preview.html`, `README.md`, `pages/`).
- Single-page starter (html5-boilerplate): `pages/index.html` only; root
  `preview.html` is a thin full-viewport iframe wrapper.
- SaaS Dashboard (multipage): page files in `pages/`, shared `css/`, `js/`,
  `assets/` at root referenced by the gallery shell.

Template conventions (lineage of the shared Vanilla template design-token
spec): light-default with calm opt-in dark mode (no-flash pre-paint +
persisted toggle), hairline 1px borders, small radii, one controlled blue
accent, Inter + JetBrains Mono, IntersectionObserver scroll-reveal
(reduced-motion safe), skip link, single `h1`, `:focus-visible`, native
controls. Off-brand styles (glassmorphism, neon, gradients, purple accents)
are banned by that spec.

## Validation and QA

- `scripts/qa/resources/qa_vanilla.py` scans Vanilla components against the
  quality bar and is wired into `scripts/tooling/validators/validate.py`
  (a required-check failure fails validation). Flags: `--only-failures`,
  `--json`, and advisory `--tokens` (reports `--ds-*` adoption vs raw hex,
  always exits 0). It scans the Components tree (observed run:
  "scanned: 191 components"); Sections/Templates are governed by their own
  specs.
- Structural validation: `scripts/tooling/validators/validate.py` +
  `scripts/tooling/validators/deep_check.py`.
- Template Playwright QA: `scripts/qa/resources/_qa_template.py`
  (overflow at 320–1920px, console errors, template interactions).

## CLI behavior

Vanilla resources are indexed under technology `Vanilla HTML/CSS/JS` and
install like any other resource (`cli/src/registry/resolver.js`,
`cli/src/install/writer.js`). Note the registry tech string is
`"Vanilla HTML/CSS/JS"` — use that exact value when filtering by technology.
CLI details: `agents/resources/cli.md`.

## Rules of thumb for agents

1. Components = fragments (no DOCTYPE, inline style+script, `--ds-*` with
   fallbacks); Sections = full pages (DOCTYPE, `nb` body, own tokens);
   Templates = root metadata + `pages/` code. Do not mix the shapes.
2. Every interactive control must be a native element or carry full
   role+keyboard handling; every animation needs a reduced-motion guard.
3. Keep `slug` equal to the folder name in component metadata.
4. After edits: `python scripts/tooling/validators/validate.py` and
   `python scripts/qa/resources/qa_vanilla.py --only-failures`.