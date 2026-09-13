# AGENTS.md — AI SaaS Platform

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium, production-ready multi-page website template for an AI SaaS startup (brand: **Nexus AI**, a fictional unified AI inference platform). Built with **Tailwind CSS only** (via CDN), vanilla HTML, and scoped vanilla JS. No frameworks, no build step.

## Design system

A quiet, editorial, light-mode-first design: warm paper background (`#F9F7F4`), refined neutral ink ramp, a single terracotta accent (`#E07A5F` / `#C85D42`) for CTAs, active states and emphasis; Fraunces (display serif) + Inter (body) typography; white cards, 1px hairline borders and restrained soft shadows — no gradients as a primary visual language. The palette lives inline in the per-page `tailwind.config` (`paper` / `ink` / `terracotta` ramp) — adjust those values to re-theme every page at once.



## File layout

```
ai-saas-platform/
├── pages/            # 11 self-contained static HTML pages (index, features, integrations, pricing,
│                        customers, blog, blog-post, docs, login, signup, dashboard)
├── components/      # Reference snippets (NOT server-included): navbar, footer, buttons, reusable-ui)
├── assets/          # icons/, images/, illustrations/, placeholders/ (SVG only)
├── preview.html     # Template gallery / index of all 11 pages
├── metadata.json
└── README.md
```

Each page is self-contained static HTML — `components/` files are copy-paste reference blocks, not includes. Internal links are relativeand work when served from the folder.



## Interactivity (vanilla JS, scoped)

- **Navbar mobile menu** — `data-navbar` / `data-nav-toggle` / `data-mobile-menu`, toggles `aria-expanded`.
- **Accordion** — `data-accordion` + `data-accordion-item`, CSS-grid `grid-rows-[0fr]↔[1fr]` animation, single-open via `data-single-open`, chevron rotation.

- **Pricing billing toggle** — `data-billing` switches monthly/yearly price + period text.


- **Scroll reveal** — `[data-reveal]` elements fade-up via `IntersectionObserver` (graceful fallback if unsupported.



## How to adapt it

1. **Swap the brand**: replace the Nexus AI name/mark, copy, and SVG placeholdersin `assets/` with real product content.
2. **Re-theme**: edit the color values in each page's inline `tailwind.config` — every page updates consistently.

3. **Add a page**: duplicate a `pages/*.html`, keep the shared `<head>` + navbar + footer, and swap the `<main>` content. Register it in `preview.html`'s page index when applicable.



## Do not

- Do not introduce a framework, backend, or server-includes. Each page is staticand self-contained.
- Do not add gradients as a primary visual language; the editorial warm-paper + hairline rule system is deliberate.
- Do not break the scoped `data-*` JS contracts or remove ARIA from toggles.



## Quality bar

Semantic HTML (`header`, `nav`, `main`, `section`, `article`, `footer`), ARIA labels, `aria-expanded` on toggles, focus-visible rings, `prefers-reduced-motion` respected for dashboard chart animations. Validate with `python3 scripts/validate.py` after changes; run any related `scripts/_qa_*.py` template harness when present.