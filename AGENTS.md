# DevSnips — Repository Knowledge

## What this repo is
DevSnips is an open-source, framework-free frontend component library organized as design-system "families". Each Tailwind family lives under `Tailwind/Components/` (e.g. `Tailwind/Components/Accordions/`, `Tailwind/Components/Tables/`) and contains variant sub-folders.

## Folder + file convention (per variant)
Every variant folder (kebab-case) must contain exactly three files:
- `code.html` — component ONLY. No `<html>`/`<head>`/`<body>`/`<!doctype>`/Tailwind CDN. Copy-paste ready.
- `preview.html` — full `<!DOCTYPE html>` page with Tailwind CDN (`https://cdn.tailwindcss.com`), Inter font, responsive layout, and realistic application context around the component.
- `metadata.json` — see schema below.

The `code.html` snippet comment header is optional but follows CONTRIBUTING.md:
`<!-- Snippet Name / Description / Author: DevSnips Contributors / Usage Example -->`

## metadata.json schema (used across Tables, Cards, Accordions)
```json
{
  "name": "Display Name",
  "slug": "kebab-folder-name",
  "component": "accordion",        // singular family noun
  "family": "accordions",          // plural
  "variant": "basic",              // short variant key
  "description": "...",
  "framework": "Tailwind CSS",
  "language": "HTML",
  "tags": ["..."],
  "related": ["other-variant-slug"],
  "features": ["..."]
}
```
Required keys: name, slug, component, family, variant, description, framework, language, tags, related, features. `slug` must equal the folder name.

## snippets-index.json registration
- Top-level `families[]` array; each family has `name`, `path`, `tech`, `category`, `description`, `variantsCount`, `variants[]` (each with name/path/description/features/tags/files), `tags`, `searchTerms`.
- Update `stats.totalFamilies` and `stats.totalVariants` (sum of variantsCount) after adding a family.
- Also add the family name to `technologies[].families` for the matching tech (`Tailwind CSS`).

## Accordion JS pattern (verified working)
Use a `<div data-accordion="name">` wrapper containing `<div data-accordion-item>` blocks and an inline `<script>` at the end. The script scopes itself with:
```js
const root = document.currentScript.closest('[data-accordion]');
```
This works because the `<script>` parses inside the root. Panel animation uses the CSS-grid trick:
`grid grid-rows-[0fr]` ↔ toggle `grid-rows-[1fr]` with `transition-[grid-template-rows] duration-300 ease-out`, wrapped in `overflow-hidden`. Chevron rotates via `style.transform = 'rotate(180deg)'`. Single-open mode: add `data-single-open` attr and close siblings on open. Always set `aria-expanded` + `aria-controls` + `role="region"` + `aria-labelledby` + `focus-visible:ring`.

## Code standards
- HTML + Tailwind CSS only. Vanilla JS only where interaction is required.
- NO React/Vue/Alpine/Bootstrap/jQuery.
- 2-space indentation. Semantic HTML. Accessibility required (ARIA, keyboard, focus rings).

## Tailwind SaaS Sections — `Tailwind/Sections/saas/`
Premium SaaS website sections (one variant/style per section, mixed across the three design styles). Same 3-file convention as other Sections families (`code.html` / `preview.html` / `metadata.json`).
15 sections shipped: product-hero (vercel), launch-hero (neo-brutalism), dashboard-hero (sharp-glassmorphism), feature-grid (neo-brutalism), bento-showcase (sharp-glassmorphism), product-workflow (vercel), three-tier-pricing (sharp-glassmorphism), usage-pricing (neo-brutalism), pricing-comparison (vercel), logo-cloud (vercel), testimonials (sharp-glassmorphism), metrics (neo-brutalism), screenshot-showcase (sharp-glassmorphism), trial-cta (neo-brutalism), enterprise-footer (vercel). Several include scoped vanilla-JS interactivity (countdown, billing toggle, usage calculator, workflow step switcher, screenshot tabs, count-up, newsletter) using the `document.currentScript.closest('[data-<scope>="<style>"]')` pattern. Registered in `snippets-index.json` under `tech: "Tailwind CSS"`, `category: "Sections"`.

## Tailwind Sections — `Tailwind/Sections/`
Multi-style website sections organized as `category/section/style/` (three levels, all kebab-case). Each style folder contains exactly: `preview.html` (full `<!DOCTYPE html>` page with Tailwind CDN + app-context shell), `code.html` (snippet only — no DOCTYPE/CDN), `metadata.json` (keys: name, slug, category, subcategory, section, style, description, framework, language, tags, features, responsive, dependencies). `slug` = `<section>-<style>`.

Three shared design styles with distinct token palettes (canonical reference in `Tailwind/Sections/STYLE_TOKENS.md`):
- `neo-brutalism` — Archivo + JetBrains Mono; hard `border-2 border-black`, offset `shadow-[8px_8px_0_0_#000]`, flat bright accents (#FFE600/#FF4FA3/#00E676/#00C2FF), press-down hover, cream `#FFFDF5` bg. Scope attrs use `="nb"`.
- `vercel` — Geist + Geist Mono; dark `#050505`/`#0a0a0a`, `border-white/10` hairlines, single teal `#50e3c2` accent, white primary buttons. Scope attrs use `="vc"`.
- `sharp-glassmorphism` — Sora + JetBrains Mono; `bg-white/10 backdrop-blur-2xl` glass over animated `.sg-mesh` gradient (fuchsia/indigo/cyan), gradient CTAs, cyan `#6ee7ff` glow. Scope attrs use `="sg"`. Glass needs a colored backdrop to read.

JS scoped via `document.currentScript.closest('[data-<thing>="<style>"]')` so snippets work standalone. Categories: ai-product (ai-chat-interface, model-comparison, prompt-library, agent-workflow), saas, developer, app-ui, marketing, premium-visual. Registered in `snippets-index.json` `families[]` with `tech: "Tailwind CSS"`, `category: "Sections"`, path = `Tailwind/Sections/<category>/<section>/`; variants are the style folders. Also listed under `technologies[].families` for Tailwind CSS.

## Vanilla Sections (Neo-Brutalist) — `Vanilla/Sections/`
- 65 self-contained website sections across 16 families (Hero, Navigation, Features, Logos, Statistics, Products, Pricing, Testimonials, Team, Process, Content, Gallery, FAQ, CTA, Contact, Footer).
- Folder = `Vanilla/Sections/<Family>/<kebab-slug>/` containing exactly: `<slug>.html` (self-contained: inline `<style>` + `<script>`, full `<!DOCTYPE html>`, body class `nb`), `metadata.json`, `README.md`. This matches the existing Vanilla component convention (one `.html` per variant), NOT the Tailwind code.html/preview.html split.
- Shared design tokens embedded in each `.html` `<style>` `:root`: `--bg --surface --foreground --muted --border --primary --accent --pink --lime --cyan --radius --shadow --shadow-lg --ring --container --gutter`. Light + dark via `prefers-color-scheme`. Reduced-motion safe.
- `metadata.json` keys: id, name, slug, component, family, variant, description, framework, language, technology, category, subcategory, tags, features, responsive, darkMode, accessibility, browserSupport, dependencies, source, related.
- Browse via `Vanilla/Sections/index.html` (filterable gallery) and `Vanilla/Sections/showcase.html` (all sections live, each in an isolated iframe).
- Registered in `snippets-index.json` `families[]` with `tech: "Vanilla HTML/CSS/JS"`, `category: "Sections"`; also listed under `technologies[].families` for the Vanilla tech.

## Tailwind Sections (15-Style Multi-Concept) — `Tailwind/Sections/<Category>/<style-slug>/`
- 11 section categories (Testimonials, FAQ, Contact, Footer, Navbar, Stats, Team, Blog, Logos, Newsletter, 404), each with 15 variant folders = 165 sections, 660 files total.
- Folder = `Tailwind/Sections/<Category>/<style-slug>/` — the folder is named after its **design style** (not `Section-NN`), matching the repo's existing multi-style convention (`developer/code-playground/neo-brutalism/`, etc.). Each category uses each of the 15 styles exactly once (1:1 permutation), so the folder name is the style slug. Each folder contains exactly 4 files: `preview.html` (full `<!DOCTYPE>` + Tailwind CDN + Google Fonts + style head_css + body decor), `code.html` (snippet only — snippet comment header + `<section>`, NO DOCTYPE/CDN), `metadata.json` (keys: id=`<category>-<style-slug>`, slug=id, name, technology=tailwind, category=sections, subcategory, section, style, description, framework, language, tags, features, responsive, darkMode, accessibility, browserSupport, dependencies), `README.md` (features + responsive + browser support + usage + design language).
- 15 design styles defined in `_gen/styles.py` TOKENS dict: neo-brutalism, edge-glassmorphism, vercel, minimal, apple-inspired, bento-grid, editorial, dark-premium, startup-landing, futuristic, gradient-mesh, soft-ui, cyber, monochrome, elegant-luxury. Each has: title, fonts, font_url, font_display, font_mono, head_css (CSS vars + .f-disp/.f-mono/.nb-shadow/.sg-mesh helpers + prefers-color-scheme), body_class, decor (fixed animated background), surface/surface_soft/badge/btn_primary/btn_secondary/input/chip/hover_card/text_muted/accent/accent2/text tokens.
- Style rotation per category is offset (`offset = (cat_index*4) % 15`) so each category spans all 15 styles with even distribution (11 sections per style across the library).
- Generator lives in `_gen/`: `styles.py` (tokens), `helpers.py` (esc/fill/avatar/ic/star_row/logo_svg/ICONS), `layout.py` (head/section wrappers), `builders_<category>.py` (15 concepts each), `generate.py` (writes files), `update_index.py` (updates snippets-index.json). Run `python3 -m _gen.generate` then `python3 -m _gen.update_index`.
- Registered in `snippets-index.json` as 11 new families named `<Category> (Tailwind)` with `tech: "Tailwind CSS"`, `category: "Sections"`, path `Tailwind/Sections/<Category>/`, variantsCount=15. Also listed under `technologies[].families` for Tailwind CSS. Stats: totalFamilies=85, totalVariants=730.
- Pure HTML + Tailwind CSS only (vanilla JS only for navbar/footer interactivity via scoped inline scripts). No React/Vue/Alpine/Bootstrap/DaisyUI/Flowbite. Inline `<style>` only for pure-CSS animations (logos marquee, 404 blinking cursor).


## Tailwind Templates — `Tailwind/Templates/<slug>/`
Full website templates (not single components). Two scopes exist:
- **Multi-page** (`type: "multipage"`): `ai-saas-platform` (11 pages incl. components/ + assets/), `baseline-conference` (6 pages), `northline-atelier` (4 pages). Pages live in `pages/`, shared navbar/footer in `components/` (ai-saas only).
- **Single-page** (`type: "single-page"`): `quiet-place`, `krat-adventure` (root `index.html`), `stratum` (`pages/index.html` + `preview.html`).

### `stratum` — Neo-Brutalism + Editorial Modern fintech ops (single-page)
- Fictional brand: **Stratum** — vertical fintech ops platform (treasury / bill pay / spend control). Files: `pages/index.html` (full landing, 11 composed sections), `preview.html` (template gallery shell — overview + sections index + design-system summary), `assets/icons/logo.svg`, `assets/images/og-image.svg`, `metadata.json`, `README.md`.
- Design system tokens (defined in `tailwind.config` colors in the page head): ink `#0A0A0A`, paper `#FBFAF7`, cream `#F4F1EA`, lime `#C6F24E` (primary accent), ember `#FF4FA3`, sky `#00C2FF`, forest `#007A52` (success — darkened from `#00A86B` for WCAG AA on light bg). Fonts: Archivo (display 500-900), Inter (body), JetBrains Mono (labels/metadata). Geometry: 2px borders, square radii, offset shadows `shadow-brutal` 8px / `shadow-brutal-sm` 4px / `shadow-brutal-lg` 12px, `.press` translate-hover interaction.
- Hero = editorial split: copy left + hand-built "treasury command surface" product panel right (live status header, balance, animated SVG sparkline with stroke-dash draw, account ledger rows, sync footer) flanked by two floating mini-cards (approval needed / FX hedge, `sm:block` desktop-only). Bento capabilities section includes a policy-as-code approval-routing graph. Workflow = 5-step capture->reconcile with per-step timings. Pricing = cash-managed tiers (not per-seat). FAQ = scoped single-open accordion (CSS-grid `0fr->1fr`, `aria-expanded`/`aria-controls`/`role=region`, chevron rotate). CTA = dark panel with corner-tick framing.
- Scoped vanilla JS (inline `<script>` at body end): mobile menu toggle (aria-expanded + icon swap + auto-close on link click), FAQ accordion single-open. CSS-only: `.press` hover, `.link-underline` grow, `.live-dot` pulse, `.marquee-track` logos, `.spark-path` draw.
- **Accessibility**: skip link, semantic landmarks, single h1, AA-normal contrast on all text (opacity text uses `/60` minimum — `/40`/`/50` fail; forest token darkened to `#007A52`). `prefers-reduced-motion` disables marquee/sparkline/transitions.
- QA verified: 0 horizontal overflow at 320/375/390/430/768/1024/1280/1440/1920px, 0 console errors, accordion + mobile menu interactions pass, strict HTML5 valid (html5lib), metadata.json valid.
- Registered in `snippets-index.json` as family `Stratum Fintech Ops Platform (Template)` (`category: "Templates"`, `tech: "Tailwind CSS"`, `variantsCount: 1`); also under `technologies[Tailwind CSS].families`. Stats after: totalFamilies=88, totalVariants=733.
