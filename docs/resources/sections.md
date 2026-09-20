# Sections

A **section** is a complete page-level composition — a hero, a pricing area, a testimonial block, a footer — intended to be composed into pages. Sections are larger than components and carry real content structure, not just interactive behavior.

## Section families per technology

| Technology | Layout |
|---|---|
| React | `Sections/<Family>/<direction>/` — most families ship exactly four direction-named variants (Minimal, Dark Premium, Bento, Neo-Brutalist); `Features` has additional variants. Families: CTA, Comparison, Contact, FAQ, Features, Hero, Integrations, Logo-Cloud, Newsletter, Pricing, Stats, Team, Testimonials. |
| Tailwind | Two shapes: single-concept categories at `Sections/<Category>/<style>/` (e.g. `Blog/minimal/`), and multi-concept categories at `Sections/<Category>/<section>/<style>/` (e.g. `AI-Product/model-comparison/vercel/`). Categories include 404, Blog, Contact, FAQ, Footer, Logos, Newsletter, Stats, Team, Testimonials (single-concept) and AI-Product, App-UI, Developer, Marketing, Premium-Visual, SaaS (multi-concept). |
| Vanilla | `Sections/<Family>/<variant>/` — a neo-brutalist collection (Contact, Content, CTA, FAQ, Features, Footer, Gallery, Hero, Logos, Navigation, Pricing, Process, Products, Statistics, Team, Testimonials). |

## File contract by technology

| Technology | Required files | Notes |
|---|---|---|
| React | `code.tsx`, `preview.html`, `metadata.json` | **No `README.md`, no `code.jsx`.** One exported component (`HeroSection`, `FeaturesSection`, …) with all content as overridable props. |
| Tailwind | `code.html`, `preview.html`, `metadata.json` | `README.md` optional but must be non-empty when present. |
| Vanilla | `metadata.json` (machine-enforced minimum) | Convention: `code.html` + `README.md`. Vanilla section `code.html` is a **full standalone page** (`<!DOCTYPE html>`, `<body class="nb">`), unlike Vanilla component fragments. |

## Technology-specific section conventions

### React — four design directions

React sections follow four directions governed by `library/React/Sections/DESIGN_TOKENS.md`: **Minimal**, **Dark Premium**, **Bento**, **Neo-Brutalist**. Metadata records the `direction` field. Most families have exactly one variant per direction.

### Tailwind — shared style system

Single-concept categories permute a fixed set of styles (one style per category, 1:1). Multi-concept categories use three shared design styles documented with token palettes in `library/Tailwind/Components/STYLE_TOKENS.md`:

| Style | Fonts | Visual signature | Scope attribute |
|---|---|---|---|
| `neo-brutalism` | Archivo + JetBrains Mono | `border-2 border-black`, offset shadows, flat accents | `="nb"` |
| `vercel` | Geist | dark `#050505`, hairlines, teal accent | `="vc"` |
| `sharp-glassmorphism` | Sora | glass over animated mesh | `="sg"` |

Variant folder naming: single-concept folders are named after the style slug (`Sections/Blog/minimal/`); multi-concept folders are named after the `<section>-<style>` slug (`Sections/AI-Product/ai-chat-interface/neo-brutalism/`). Metadata `slug` = `<section>-<style>`.

### Vanilla — self-owned token system

Vanilla sections deliberately keep their own token vocabulary (`--bg`, `--surface`, `--foreground`, `--primary`, `--accent`, `--radius`, `--shadow`, …) with light + dark via `prefers-color-scheme`. They are **not** migrated to the `--ds-*` component token system; do not mix the shapes.

## Sections vs components

Use a section when the artifact occupies a page region and carries content structure (headings, media, lists, CTAs). Use a component when the artifact is one interaction pattern. If a request says "a pricing *page*", that is closer to a template; "a pricing *block*" is a section.

## Installing

```bash
npx devsnips add Tailwind/Sections/Blog/minimal
npx devsnips add React/Sections/Hero/minimal
npx devsnips add Vanilla/Sections/Hero/hero-minimal
```

Installed under `./devsnips/<tech>/sections/<...>/`. Integration guidance for agents: [Adaptation](../agents/adaptation.md).
