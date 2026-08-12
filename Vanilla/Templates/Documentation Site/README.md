# Documentation Site Template (Vanilla)

A premium, editorial **developer documentation** template built for DevSnips with
plain HTML, CSS, Pico CSS, and vanilla JavaScript. A single self-contained SPA
with a header, nested left sidebar, main content, and a sticky *On this page*
table of contents. No React, no Tailwind, no bundler, no build step, no backend.

**Technology:** vanilla
**Category:** templates
**Subcategory:** documentation-site
**Type:** single-page (15 documentation sections, hash-routed)

## Preview

Open `preview.html` directly in a browser, or serve the folder for local
development:

```bash
cd "Vanilla/Templates/Documentation Site"
python3 -m http.server 8080
# visit http://localhost:8080/preview.html
```

The whole template runs without a build step. The only external requests are
Google Fonts (Inter + JetBrains Mono) and Pico CSS, both from CDNs.

## What's inside

```
Documentation Site/
├── preview.html            # The single canonical DevSnips preview (this SPA)
├── metadata.json            # DevSnips registration metadata
├── README.md                # This file
└── assets/
    ├── logo.svg             # DevSnips [DS] mark
    └── favicon.svg          # DevSnips favicon
```

Per the shared `design-tokens.md` convention, the template folder contains
exactly **one** `preview.html`. It is the canonical preview shown by the DevSnips
website. It is fully responsive, uses the template's real CSS/JS, uses relative
paths, and loads correctly when opened directly.

### Architecture

`preview.html` is a single hash-routed SPA. A `NAV` config drives the nested
sidebar, a `PAGES` object maps each section ID to a content-builder function,
and a small runtime handles routing, scrollspy, search, code tools, theming,
and the mobile drawer. All content for all 15 sections lives in the one file —
there are no separate `pages/`.

### Sections (15)

| Group | Sections |
|---|---|
| **Start** | Documentation Home, Introduction, Getting Started, Installation, Quick Start |
| **Library** | Vanilla, Components, Templates, Design Tokens |
| **Reference** | Guides, API Reference, Examples, FAQ |
| **Project** | Changelog, Roadmap, Contributing |

### Design system

The template extends the shared DevSnips `--ds-*` token system (defined in
`Vanilla/Templates/design-tokens.md`) with a handful of `--template-*` variables
that adapt — never override — the global language. It is **neutral-first** with
one controlled **blue-600** accent (never violet/neon), hairline 1px borders,
restrained shadows, an Inter + JetBrains Mono type scale, a base-4 spacing
scale, and small radii by default. Light and dark mode are supported via a
`data-theme` attribute on `<html>` with a no-flash system-preference fallback.

## Features

- **Single SPA** covering all 15 documentation sections via hash routing
- **Nested sidebar navigation** with four groups, expandable parents, active
  page state (`aria-current`), and a live filter input
- **Breadcrumbs**, **last-updated metadata**, **reading-time estimate**, and an
  **edit-on-GitHub** action on every content page
- **Sticky scrollspy table of contents** generated per page from `h2`/`h3`
  headings via `IntersectionObserver`; collapses to a tappable panel below 1180px
- **Previous/next navigation** at the foot of every content page
- **Cmd+K (and `/`) search command palette** — arrow-key navigation, Enter to
  open, Esc to close, grouped results with matched-term highlighting
- **Code blocks** with a lightweight vanilla-JS syntax highlighter
  (HTML, CSS, JS, JSON, Bash), a language label, and a **clipboard copy button**
- **Tabbed code blocks** (e.g. npm/pnpm/yarn) with ARIA tablist semantics
- **Five callout variants** — info, note, tip, warning, danger
- **Responsive tables** in `overflow-x:auto` wrappers (never cause page overflow)
- **Status/category badges** — stable, beta, deprecated, accent, neutral, solid
- **API reference blocks** with signature, return type, parameter table, example
- **Light/dark mode** — no-flash system preference + persisted header toggle
- **Responsive by composition** — sidebar → off-canvas drawer below 1024px,
  TOC → collapsible panel below 1180px, header compacts below 640px

## Accessibility

Skip link, semantic landmarks (`header`/`main`/`nav`/`aside`/`article`), ARIA
on the search dialog, tablists, drawer, breadcrumbs, and TOC, `:focus-visible`
rings throughout, keyboard-operable controls (Escape closes overlays, Cmd/Ctrl+K
and `/` open search, arrow keys navigate results), and `prefers-reduced-motion`
guards on every animation.

## QA

Verified with Playwright across six viewport widths (320–1920px):

- **0 console errors** on every page and breakpoint
- **0 horizontal overflow** — `scrollWidth == clientWidth` at 320, 375, 768,
  1024, 1280, and 1920px
- Strict HTML5 valid (html5lib), valid `metadata.json`
- Interactions pass: hash routing + active nav, scrollspy TOC, search open/close,
  theme toggle, code copy buttons, code tabs, mobile drawer open/close

Zero runtime dependencies beyond Pico CSS and Google Fonts (both from CDN).

## Customizing

The whole template is data-driven from the top of the `<script>` block in
`preview.html`:

- `NAV` — sidebar structure (groups, items, nested children, badges)
- `META` — per-page eyebrow, title, last-updated date, edit-on-GitHub path
- `PAGES` — per-section content-builder functions

To add a section: add an entry to `NAV`, a row to `META`, and a `PAGES.<id>`
function. The router, TOC, search index, and prev/next pick it up automatically.
