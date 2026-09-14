# AGENTS.md — DevSnips Curated Design Store

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium **seven-page** Tailwind CSS ecommerce template for **DevSnips**, a fictional curated store of considered design objects(vessels, lighting, textiles, furniture). Built in an **Editorial Modern + Monochrome Luxury** design language. Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step.



## Design system

Editorial Modern fused with Monochrome Luxury — a magazine-influenced system, not a soft-glass SaaS store: warm neutral palette(ink `#14110D`, paper `#F5F1EA`, bone `#ECE6DB`, cream `#FBF8F1`, stone `#8A8275`), a single warm clay accent `#B5552D` (used sparingly for emphasis and the logo dot), **Fraunces** high-contrast serif for display + **Inter** body + **JetBrains Mono** labels/prices/metadata, hairline rules (`rgba(20,17,13,0.16)`), square-ish geometry, no drop shadows or gradients, oversized editorial headlines, numbered sections, magazine masthead rhythm.



## File layout

```
devsnips-store/
├── pages/
│   ├── index.html        # Home: editorial hero, new arrivals, material spectrum, featured collection, journal, newsletter
│   ├── shop.html         # Filter chips, sort, live count (scoped JS)
│   ├── product.html      # Gallery, finish swatches, quantity stepper, care-guide accordion, related
│   ├── cart.html         # Working quantity steppers + remove, receipt-style summary, shipping estimate
│   ├── checkout.html     # Stepper-led contact/shipping/payment + fixed order summary
│   ├── journal.html      # Featured article + tag filters + magazine cards
│   └── about.html        # Atelier: principles, process timeline, maker studios
├── assets/
│   ├── icons/logo.svg    # [D] mark
│   └── images/og-image.svg
├── preview.html          # Template gallery shell
├── metadata.json
└── README.md
```

All visuals are inline SVG and Tailwind — product illustrations are hand-built SVG silhouettes with a consistent stroke language.



## How to adapt it

1. **Swap the store**: replace the DevSnips brand, products, studios and copy across the pages. All products are invented placeholders.
2. **Re-theme**: edit the color values in each page's inline `tailwind.config` (ink/paper/bone/cream/clay ramp) — keep one warm clay accent.


3. **Add a page**: duplicate a `pages/*.html`, keep the shared navbar (centered [D] logo + cart badge) and footer, and swap the `<main>` content. Register it in `preview.html`'s page index.



## Interactivity (scoped vanilla JS, IIFEs)

Mobile menu, product filter chips + sort + live count, thumbnail gallery, finish swatches, quantity steppers, single-open care-guide accordion (CSS-grid `0fr→1fr`, ARIA, keyboard), cart math (line totals, shipping estimate, empty state) and newsletter. `prefers-reduced-motion` disables scroll reveal and transitions.



## Do not

- Do not introduce a framework, backend, or build step. Tailwind CDN + vanilla JS only.
- Do not add drop shadows or gradients; the hairline rule + square geometry system is deliberate.


- Do not break the scoped `data-*` JS contracts or remove ARIA from the accordion/mobile menu.



## Quality bar

Semantic landmarks (`header`, `nav`, `main`, `footer`), skip link, a single `h1` per page, ARIA on the mobile menu (`aria-expanded`/`aria-controls`), accordion and stepper, visible focus rings, `prefers-reduced-motion` support. Validate with `python3 scripts/validate.py` after changes.

