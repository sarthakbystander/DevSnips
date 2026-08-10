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
- **Single-page** (`type: "single-page"`): `quiet-place`, `krat-adventure` (root `index.html`), `stratum` (`pages/index.html` + `preview.html`), `meridian` (`pages/index.html` + `preview.html`).

### `stratum` — Neo-Brutalism + Editorial Modern fintech ops (single-page)
- Fictional brand: **Stratum** — vertical fintech ops platform (treasury / bill pay / spend control). Files: `pages/index.html` (full landing, 11 composed sections), `preview.html` (template gallery shell — overview + sections index + design-system summary), `assets/icons/logo.svg`, `assets/images/og-image.svg`, `metadata.json`, `README.md`.
- Design system tokens (defined in `tailwind.config` colors in the page head): ink `#0A0A0A`, paper `#FBFAF7`, cream `#F4F1EA`, lime `#C6F24E` (primary accent), ember `#FF4FA3`, sky `#00C2FF`, forest `#007A52` (success — darkened from `#00A86B` for WCAG AA on light bg). Fonts: Archivo (display 500-900), Inter (body), JetBrains Mono (labels/metadata). Geometry: 2px borders, square radii, offset shadows `shadow-brutal` 8px / `shadow-brutal-sm` 4px / `shadow-brutal-lg` 12px, `.press` translate-hover interaction.
- Hero = editorial split: copy left + hand-built "treasury command surface" product panel right (live status header, balance, animated SVG sparkline with stroke-dash draw, account ledger rows, sync footer) flanked by two floating mini-cards (approval needed / FX hedge, `sm:block` desktop-only). Bento capabilities section includes a policy-as-code approval-routing graph. Workflow = 5-step capture->reconcile with per-step timings. Pricing = cash-managed tiers (not per-seat). FAQ = scoped single-open accordion (CSS-grid `0fr->1fr`, `aria-expanded`/`aria-controls`/`role=region`, chevron rotate). CTA = dark panel with corner-tick framing.
- Scoped vanilla JS (inline `<script>` at body end): mobile menu toggle (aria-expanded + icon swap + auto-close on link click), FAQ accordion single-open. CSS-only: `.press` hover, `.link-underline` grow, `.live-dot` pulse, `.marquee-track` logos, `.spark-path` draw.
- **Accessibility**: skip link, semantic landmarks, single h1, AA-normal contrast on all text (opacity text uses `/60` minimum — `/40`/`/50` fail; forest token darkened to `#007A52`). `prefers-reduced-motion` disables marquee/sparkline/transitions.
- QA verified: 0 horizontal overflow at 320/375/390/430/768/1024/1280/1440/1920px, 0 console errors, accordion + mobile menu interactions pass, strict HTML5 valid (html5lib), metadata.json valid.
- Registered in `snippets-index.json` as family `Stratum Fintech Ops Platform (Template)` (`category: "Templates"`, `tech: "Tailwind CSS"`, `variantsCount: 1`); also under `technologies[Tailwind CSS].families`. Stats after: totalFamilies=88, totalVariants=733.

### `meridian` — Neo-Industrial + Swiss Minimal incident command (single-page)
- Fictional brand: **Meridian** — incident command platform for on-call engineering teams (alert routing / incident command / postmortems). Files: `pages/index.html` (full landing, 11 composed sections), `preview.html` (template gallery shell — overview + sections index + design-system summary), `assets/icons/logo.svg`, `assets/images/og-image.svg`, `metadata.json`, `README.md`.
- Design system tokens (defined in `tailwind.config` colors in the page head): canvas `#F5F6F8` (cool engineering paper), ink `#0B0D10`, surface `#FFFFFF`, panel `#EDEFF3`, muted `#5C6470`, amber `#E8A33C` (single primary accent), ok `#16A34A` + alert `#DC2626` (status dots/badges only). Fonts: Space Grotesk (display 400-700), Inter (body), JetBrains Mono (labels/metadata). Geometry: 1px hairline rules (`hl`/`hl-strong` utilities, `rgba(11,13,16,0.14)`), square radii, restrained tonal elevation (no offset shadows), graph-paper `.blueprint`/`.blueprint-fine` grid backgrounds. Deliberately differs from `stratum`: hairlines + tonal lift instead of 2px borders + offset shadows; Space Grotesk + amber on cool canvas instead of Archivo + lime on cream.
- Hero = editorial-technical split: copy left + hand-built "incident command surface" product panel right (dark title bar with live pulse dot, latency metric + animated SVG sparkline with stroke-dash draw + gradient fill, responders with avatar chips, timeline, runbook footer) flanked by two floating mini-cards (correlated signal / stepped escalation, `lg:block` desktop-only). Signature routing section = directed alert-routing graph (signal -> correlate node -> routing rule -> page owner, with dashed ack-fallback branch, animated `edge` flow). Workflow = 5-step incident lifecycle with per-step timings + signed-state rail. Pricing = per-on-call-team tiers (not per-seat). FAQ = scoped single-open accordion (CSS-grid `0fr->1fr`, `aria-expanded`/`aria-controls`/`role=region`/`aria-labelledby`, chevron rotate). CTA = dark panel with corner-tick framing + 3-step onboarding panel.
- Scoped vanilla JS (inline `<script>` at body end): mobile menu toggle (aria-expanded + icon swap + auto-close on link click), FAQ accordion single-open. CSS-only: hairline card hover (border-color + tonal lift), `.link-underline`/`.link-underline-amber` grow, `.live-dot`/`.live-dot-amber` pulse, `.marquee-track` logos, `.spark-path` draw, `.edge` routing flow.
- **Accessibility**: skip link, semantic landmarks, single h1, ARIA on accordion (labelledby + controls + region), mobile menu aria-expanded, SVG diagrams `role="img"` + `aria-label`, decorative SVGs `aria-hidden`. `prefers-reduced-motion` disables marquee/sparkline/edge-flow/transitions.
- QA verified: 0 horizontal overflow at 320/375/390/430/768/1024/1280/1440/1920px, 0 console errors (only Tailwind CDN production warning), accordion single-open + mobile menu interactions pass, strict HTML5 valid (html5lib), metadata.json valid.
- Registered in `snippets-index.json` as family `Meridian Incident Command Platform (Template)` (`category: "Templates"`, `tech: "Tailwind CSS"`, `variantsCount: 1`); also under `technologies[Tailwind CSS].families`. Stats after: totalFamilies=89, totalVariants=734.

### `vesper` — Glassmorphism + Cyber Minimal attack-surface management (single-page)
- Fictional brand: **Vesper** — external attack-surface management (EASM) platform for security teams (discover exposed assets / prioritize real exposures / verify remediation). Files: `pages/index.html` (full landing, 11 composed sections), `preview.html` (template gallery shell — overview + sections index + design-system summary), `assets/icons/logo.svg`, `assets/images/og-image.svg`, `metadata.json`, `README.md`.
- Design system tokens (defined in `tailwind.config` colors in the page head): canvas `#06070D` (space black), ink `#E6E8EC`, surface `#0C0E17`, panel `#11131F`, muted `#8A90A2`, cyan `#6EE7FF` (primary accent / signal), amber `#FBBF24` (high severity only), red `#F43F5E` (critical only), ok `#34D399` (resolved only). Fonts: Sora (display 400-800), Inter (body), JetBrains Mono (labels/metadata). Geometry: `rounded-2xl` frosted-glass surfaces (`backdrop-blur(20px)`), 1px white/10 hairlines, restrained cyan glow (drop-shadow on active states only), no offset hard shadows. Atmospheric backdrop: low-opacity fuchsia `#D946EF`/indigo `#6366F1`/cyan `#6EE7FF` mesh (slow-drift) + fine `cyber-grid` + radial vignette — a backdrop, not the gradient-blob anti-pattern. Deliberately differs from `stratum` (light, 2px borders + offset shadows) and `meridian` (light, 1px hairlines + tonal lift).
- Hero = editorial-cyber split: copy left + hand-built "attack-surface command console" product panel right (title bar with severity dots + SCANNING live status, tracked-assets/open-exposures summary with severity bar + legend, exposure rows with CRIT/HIGH/MED pills, live surface radar SVG with rotating sweep + plotted severity assets, exposures-per-day sparkline with draw animation, verified footer rail) flanked by two floating mini-cards (critical exposure + new asset discovered, `lg:block` desktop-only). Signature topology section = directed asset-reachability graph (internet → load balancer → API gateway → K8s API / Postgres / S3) with exposed attacker path animated in cyan and critical node ringed in red, + side exposure-detail card. Lifecycle = 5-step EASM workflow (Discover → Classify → Prioritize → Remediate → Verify) with per-step timings + signed-state rail (SHA-256 tamper-evident). Pricing = per-asset tiers (not per-seat). FAQ = scoped single-open accordion (CSS-grid `0fr->1fr`, `aria-expanded`/`aria-controls`/`role=region`/`aria-labelledby`, chevron rotate). CTA = glass conversion panel with corner-tick framing + 3-step onboarding panel.
- Scoped vanilla JS (inline `<script>` at body end): mobile menu toggle (aria-expanded + icon swap + auto-close on link click), FAQ accordion single-open. CSS-only: `.card` glass hover (border + soft cyan glow + tonal lift), `.link-underline` grow, `.live-dot`/`.live-dot-red` pulse, animated `.edge`/`.edge-hot` topology flow, `.radar-sweep` rotation, `.spark-path` draw, `.mesh-drift`, `.marquee-track` logos.
- **Accessibility**: skip link, semantic landmarks, single h1, ARIA on accordion (labelledby + controls + region), mobile menu aria-expanded, SVG diagrams `role="img"` + `aria-label`, decorative SVGs `aria-hidden`, cyan `:focus-visible` ring. `prefers-reduced-motion` disables mesh drift/radar sweep/marquee/sparkline/edge flow/transitions.
- QA verified: 0 horizontal overflow at 320/375/390/430/768/1024/1280/1440/1920px (index + preview), 0 console errors, accordion single-open + mobile menu interactions pass (aria-expanded sync verified), strict HTML5 valid (html5lib), metadata.json + snippets-index.json valid JSON.
- Registered in `snippets-index.json` as family `Vesper Attack-Surface Management Platform (Template)` (`category: "Templates"`, `tech: "Tailwind CSS"`, `variantsCount: 1`); also under `technologies[Tailwind CSS].families`. Stats after: totalFamilies=90, totalVariants=735.
