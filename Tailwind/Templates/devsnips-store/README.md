# DevSnips Curated Design Store — Template

A premium **six-page** Tailwind CSS ecommerce template for **DevSnips**, a fictional curated store of considered design objects (vessels, lighting, textiles, furniture). Built in an **Editorial Modern + Monochrome Luxury** design language. Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step.

The store brand is **DevSnips**, and the logo mark is a hairline **[D]** representing DevSnips (`assets/icons/logo.svg`).

## Design language

Editorial Modern fused with Monochrome Luxury — a magazine-influenced system, not a soft-glass SaaS store:

- Warm neutral palette: ink `#14110D`, paper `#F5F1EA`, bone `#ECE6DB`, cream `#FBF8F1`, stone `#8A8275`
- A single warm accent: clay `#B5552D` (used sparingly for emphasis and the logo dot)
- **Fraunces** (high-contrast serif, optical sizing) for display + headings; **Inter** for body; **JetBrains Mono** for labels, prices and metadata
- Hairline rules (`rgba(20,17,13,0.16)`), square-ish geometry, no drop shadows or gradients
- Oversized editorial headlines, numbered sections, magazine masthead rhythm
- Generous whitespace, restrained interactions (hover reveals, hover lifts, focus rings)

## Structure

```
devsnips-store/
├── preview.html                # Template gallery shell — overview, pages index, design-system summary
├── metadata.json
├── README.md
├── assets/
│   ├── icons/logo.svg          # [D] mark representing DevSnips (hairline frame, bracket serif, clay dot)
│   └── images/og-image.svg     # Editorial OG card with headline + vessel motif
└── pages/
    ├── index.html              # Home: editorial hero, new arrivals, material spectrum, featured collection, journal, newsletter
    ├── shop.html               # Collection listing: filter chips, sort, responsive product grid
    ├── product.html            # PDP: gallery, finish swatches, quantity stepper, care-guide accordion, related
    ├── cart.html               # Line items, receipt-style order summary, shipping estimate, empty state
    ├── checkout.html           # Stepper-led contact/shipping/payment + fixed order summary
    ├── journal.html            # Editorial article index: featured entry, tag filters, magazine cards
    └── about.html              # Atelier: principles, process timeline, maker studios, CTA
```

No `css/`, `js/` or `images/` directories beyond `assets/` — all visuals are inline SVG and Tailwind. Product illustrations are hand-built SVG silhouettes with a consistent stroke language.

## Pages

| # | Page | Purpose |
|---|------|---------|
| 01 | Home | Editorial issue-cover hero, new arrivals grid, material spectrum, featured collection, journal preview, newsletter |
| 02 | Shop | Collection listing with category filter chips, sort dropdown, live count (scoped JS) |
| 03 | Product | PDP with thumbnail gallery, finish swatches, quantity stepper, single-open accordion, related objects |
| 04 | Cart | Line items with working quantity steppers + remove, receipt-style summary, shipping estimate (scoped JS) |
| 05 | Checkout | Three-step stepper, contact/shipping/payment form, fixed order summary |
| 06 | Journal | Featured article + filterable magazine-style article index |
| 07 | Atelier | Brand story, three principles, four-step process timeline, maker studio cards |

## Notable design decisions

- **Editorial hero as an "issue cover"** — a masthead bar (Vol. 04 / The Vessel Collection / Spring–Summer 2026), oversized serif headline with an italic line and clay full stop, and a numbered collection index beside a featured object panel.
- **Product cards reveal on hover** — a thin ink bar slides up showing the material/origin metadata, in place of a second image.
- **Material spectrum** — a five-swatch row (stoneware, oak, linen, brass, wool) with firing/source metadata, paired with a quiet metrics band.
- **Receipt-style order summary** — mono type, hairline rules and a `repeating-linear-gradient` ruled background give the cart summary a deliberate, paper-receipt quality.
- **Scoped vanilla JS** — each interaction (mobile menu, filters, gallery, swatches, quantity, accordion, cart math, newsletter) is wrapped in an IIFE and reduced-motion-safe.

## Responsiveness

Mobile-first, tested from 320px through 1920px+. Fluid type via `clamp()` on hero headings, responsive nav (hamburger → mobile menu below `lg`), grids that reflow (`grid-cols-1 → sm:2 → lg:3/4`), checkout that stacks the order summary below the form on mobile, and product/cart rows that recompose. No horizontal overflow.

## Accessibility

Semantic landmarks (`header`, `nav`, `main`, `footer`), skip link, a single `h1` per page, ARIA on the mobile menu (`aria-expanded`/`aria-controls`), accordion (`aria-expanded`/`aria-controls`/`role="region"`), and stepper; visible focus rings in clay; `prefers-reduced-motion` disables scroll reveal and transitions.

## Technology & dependencies

- Tailwind CSS via CDN (`https://cdn.tailwindcss.com`) with a small inline `tailwind.config` theme extension (custom colors + font families)
- Google Fonts: Fraunces, Inter, JetBrains Mono
- Vanilla JavaScript (scoped IIFEs, IntersectionObserver for scroll reveal)
- No build step, no npm, no frameworks

## Usage

Open `preview.html` for the template overview, or open any page in `pages/` directly in a browser. All links use relative paths so the template works from the file system.

> DevSnips is a fictional brand created for this DevSnips template. All products, studios and copy are invented.
