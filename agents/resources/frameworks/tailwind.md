# Tailwind Framework

Deep reference for Tailwind resources in `library/Tailwind/`. For the shared
resource model start with `agents/resources/resources.md`; for QA see
`agents/resources/qa.md`.

## Where Tailwind resources live

`library/Tailwind/` holds the three content types plus one gallery page:

- `library/Tailwind/Components/` — 13 families, 259 variants: Accordions,
  Buttons, Cards, Dropdowns, Input, Modals, Navbar, Navigation, Progress,
  Tables, Tabs, Toasts, Tooltips.
- `library/Tailwind/Sections/` — 16 categories, 200 variants: the
  single-concept categories (404, Blog, Contact, FAQ, Footer, Logos,
  Newsletter, Stats, Team, Testimonials) and the multi-concept categories
  (AI-Product, App-UI, Developer, Marketing, Premium-Visual, SaaS).
- `library/Tailwind/Templates/` — 10 templates (ai-saas-platform,
  atlas-analytics, baseline-conference, devsnips-store, krat-adventure,
  meridian, northline-atelier, quiet-place, stratum, vesper).
- `library/Tailwind/index.html` — category-index gallery fetching
  `snippets-index.json`.

On-disk casing is Mixed-Case for multi-word categories (`AI-Product`,
`App-UI`, `Premium-Visual`, `SaaS`); `snippets-index.json` stores the same
casing (verified: family path `Tailwind/Sections/AI-Product/`).

## Components

Two shapes exist:

1. Flat variants: `Components/<Family>/<variant>/` with exactly four files —
   `code.html`, `preview.html`, `metadata.json`, `README.md`. Example:
   `library/Tailwind/Components/Accordions/basic-accordion/`.
2. Grouped variants (3 levels): `Components/Buttons/<group>/<sub-variant>/`,
   e.g. `library/Tailwind/Components/Buttons/basic-button/primary/`. The group
   folder carries its own `metadata.json` + `README.md` (see
   `library/Tailwind/Components/Buttons/basic-button/`); each sub-variant has
   its own `metadata.json`. The sub-variant schema (observed in
   `.../basic-button/primary/metadata.json`) differs from the section schema:
   keys are `name`, `component`, `variant`, `description`,
   `category: "Components"`, `subcategory: "Buttons"`,
   `tech: ["Tailwind CSS","HTML"]`, `tags`, `searchTerms`, `related`, …

## Sections

Two shapes exist:

1. Single-concept categories are 2 levels: `Sections/<Category>/<style>/`,
   e.g. `library/Tailwind/Sections/Blog/minimal/`. Every category uses each
   of the 15 styles exactly once (1:1 permutation).
2. Multi-concept categories are 3 levels:
   `Sections/<Category>/<section>/<style>/`, e.g.
   `library/Tailwind/Sections/AI-Product/ai-chat-interface/neo-brutalism/`.

Every section variant folder contains exactly four files:
`code.html` (snippet only), `preview.html`, `metadata.json`, `README.md`.

Section metadata (observed in `library/Tailwind/Sections/Blog/minimal/metadata.json`):
`id`, `slug` (= `<section>-<style>`), `name`, `description`, `framework`,
`language`, `technology`, `type: "section"`, `category`, `subcategory`,
`section`, `style`, `tags`, `features`, `responsive`, `darkMode`,
`accessibility`, `browserSupport`, `dependencies`.

## Code and preview requirements

- `code.html` is COPY-PASTE READY: component markup only — no `<html>`,
  `<head>`, `<body>`, `<!DOCTYPE>`, or Tailwind CDN script.
- `preview.html` is a full `<!DOCTYPE html>` page loading
  `https://cdn.tailwindcss.com` and the Inter font, with a realistic
  application shell around the component.
- 2-space indentation, semantic HTML, accessibility required (ARIA,
  keyboard, focus rings). See `docs/CONTRIBUTING.md`.
- Interactivity uses scoped vanilla JS with the
  `document.currentScript.closest('[data-<thing>="<style>"]')` pattern so
  snippets work standalone (many SaaS/Navbar/Footer sections).
- Any pure-CSS animations (marquees, blinking cursors) must be
  reduced-motion safe.

## The three shared section design styles

Used by the multi-concept categories (and documented with token palettes in
`library/Tailwind/Components/STYLE_TOKENS.md`):

- `neo-brutalism` — Archivo + JetBrains Mono, `border-2 border-black`, offset
  shadows, flat accents, scope attribute `="nb"`.
- `vercel` — Geist, dark `#050505`, hairlines, teal accent, scope `="vc"`.
- `sharp-glassmorphism` — Sora, glass over animated mesh, scope `="sg"`.

## Generators (Tailwind sections)

The 10 single-concept categories are generated:

- `scripts/tooling/generators/styles.py` — the 15 style token sets.
- `scripts/tooling/generators/builders_<category>.py` — 15 concepts per
  category (builders_404.py, builders_blog.py, builders_contact.py,
  builders_faq.py, builders_footer.py, builders_logos.py, builders_navbar.py,
  builders_newsletter.py, builders_stats.py, builders_team.py,
  builders_testimonials.py).
- `scripts/tooling/generators/generate.py` — writes `code.html` +
  `preview.html` into `library/Tailwind/Sections/` (with `helpers.py`,
  `layout.py`).

Caution: running the full generator regenerates ALL section folders and can
overwrite hand-patched variants. Prefer editing committed `code.html`
directly unless you specifically intend a regeneration sweep.

## Templates

`library/Tailwind/Templates/` has two scopes:

- Multi-page: shared navbar/footer may live in `components/`
  (ai-saas-platform) or be inlined per page; page code in `pages/` (e.g.
  `library/Tailwind/Templates/atlas-analytics/pages/` — 11 pages).
- Single-page: a root `index.html` landing (quiet-place, krat-adventure) or
  `pages/index.html` + root `preview.html` (meridian — which also keeps a
  root `index.html` alongside `pages/`, `assets/`, `preview.html`,
  `metadata.json`, `README.md`, `AGENTS.md`).

Every template must ship `AGENTS.md` at its root (enforced by
`scripts/tooling/validators/validate.py`). `metadata.json` carries
`type: "template"` and `pages`.

## Validation and QA

- `scripts/tooling/validators/validate.py` +
  `scripts/tooling/validators/deep_check.py` cover structure, metadata, and
  index consistency.
- `scripts/qa/resources/test_tailwind_nav.py` validates the Tailwind gallery
  pages (`library/Tailwind/index.html` and category indexes).
- `scripts/qa/resources/_qa_template.py` is a generic Playwright harness that
  also works on Tailwind template previews (e.g.
  `python3 scripts/qa/resources/_qa_template.py library/Tailwind/Templates/meridian/preview.html`).

## Rules of thumb for agents

1. Never add a Tailwind CDN script or `<!DOCTYPE>` to `code.html`.
2. Section `slug` = `<section>-<style>`; the variant folder is named after
   the style slug (single-concept) or the section slug (multi-concept).
3. Keep `preview.html` self-sufficient — it is what browsers and QA
   harnesses open.
4. After edits: `python scripts/tooling/validators/validate.py`, then
   regenerate or hand-check the index (see `agents/resources/indexing.md`).
