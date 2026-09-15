# AI SaaS Platform — Multi-Page Tailwind Template

A premium, production-ready multi-page website template for an AI SaaS startup. Built with **Tailwind CSS only** (via CDN), vanilla HTML, and scoped vanilla JS. No frameworks, no build step.

Brand used in the template: **Nexus AI** — a fictional unified AI inference platform.

## Design language

A quiet, editorial, light-mode-first design:

- Warm paper background (`#F9F7F4`) with a refined neutral ink ramp (`#1C1917` → `#78716C`)
- A single terracotta accent (`#E07A5F` / `#C85D42`) — used sparingly for CTAs, active states, and emphasis
- Fraunces (display serif) + Inter (body) typography; oversized, tight-tracked, balanced headlines
- White cards, 1px hairline borders (`rgba(28,25,23,0.08)`), restrained soft shadows — no gradients as a primary visual language
- Subtle scroll-reveal, marquee, and float animations (all `prefers-reduced-motion` safe)
- Consistent spacing system and visual hierarchy across every page

## Structure

```
ai-saas-platform/
├── pages/
│   ├── index.html          # Landing: hero, logos, features, workflow, bento, integrations, testimonials, metrics, pricing, FAQ, CTA
│   ├── features.html       # Feature hero, capability grid, detailed sections, comparison table, CTA
│   ├── integrations.html   # Integration hero, ecosystem grid, API + SDK section, CTA
│   ├── pricing.html        # Pricing hero, plans (billing toggle JS), comparison table, enterprise, FAQ
│   ├── customers.html      # Customer hero, metrics, featured case study, testimonials, brand showcase, CTA
│   ├── blog.html           # Blog hero, featured article, categories, article cards, newsletter
│   ├── blog-post.html      # Article header, author, reading area, tags, related articles
│   ├── docs.html           # Docs layout: sidebar nav, search bar, code blocks, on-this-page TOC
│   ├── login.html          # Split-screen auth: branding panel + email/password + social login
│   ├── signup.html         # Split-screen: benefits panel + registration form + social signup
│   └── dashboard.html      # App UI: sidebar, top nav, analytics cards, charts, model mix, activity, cost
├── components/
│   ├── navbar.html         # Sticky paper navbar + mobile menu (scoped JS)
│   ├── footer.html         # Brand, link columns, newsletter, social, legal bar
│   ├── buttons.html        # Button system: terracotta primary, dark-ink solid, outline, ghost, pill badge, link-with-arrow
│   └── reusable-ui.html    # Eyebrow, accent headline, paper card, stat, avatars, marquee, accordion
├── assets/
│   ├── icons/              # logo.svg + feature icons (ai, chart, shield, grid, integrations, bolt, users, clock, check)
│   ├── images/             # dashboard-mockup.svg, workflow-mockup.svg, og-image.svg
│   ├── illustrations/      # orb.svg (gradient orb illustration)
│   └── placeholders/       # avatar.svg
├── preview.html            # Template gallery / index of all 11 pages
├── metadata.json
└── README.md
```

## Pages

| # | Page | Purpose |
|---|------|---------|
| 01 | Home | Complete SaaS landing experience |
| 02 | Features | AI capabilities, comparison, CTA |
| 03 | Integrations | App ecosystem + developer API |
| 04 | Pricing | Plans, billing toggle, comparison, FAQ |
| 05 | Customers | Stories, case study, metrics |
| 06 | Blog | Featured article + cards + newsletter |
| 07 | Blog post | Article layout + author + related |
| 08 | Docs | Sidebar nav + search + code blocks |
| 09 | Login | Split-screen authentication |
| 10 | Signup | Registration with benefits |
| 11 | Dashboard | Matching application UI |

## Usage

1. Open `preview.html` to browse the whole template.
2. Open `pages/index.html` for the marketing home page. All internal links are relative and work when served from the folder.
3. The `components/` files are reference snippets — copy individual blocks into your own pages. They are not server-included; each page is self-contained static HTML.

Serve the folder with any static server, e.g.:

```bash
python3 -m http.server
# then visit http://localhost:8000/Tailwind/Templates/ai-saas-platform/preview.html
```

## Interactivity (vanilla JS, scoped)

- **Navbar mobile menu** — `data-navbar` / `data-nav-toggle` / `data-mobile-menu`, toggles `aria-expanded`.
- **Accordion** — `data-accordion` + `data-accordion-item`, CSS-grid `grid-rows-[0fr]↔[1fr]` animation, single-open via `data-single-open`, chevron rotation.
- **Pricing billing toggle** — `data-billing` switches monthly/yearly price + period text.
- **Scroll reveal** — `[data-reveal]` elements fade-up via `IntersectionObserver` (graceful fallback if unsupported).

## Responsive & accessibility

- Mobile / tablet / desktop layouts throughout.
- Semantic HTML (`header`, `nav`, `main`, `section`, `article`, `aside`, `figure`, `footer`).
- ARIA labels, `aria-expanded` on toggles, `role="tablist"` on filter groups, focus-visible rings on interactive elements.
- `prefers-reduced-motion` respected for dashboard chart animations.

## Tech

- Tailwind CSS via CDN (`https://cdn.tailwindcss.com`)
- Google Fonts: Fraunces (display) + Inter (body)
- Pure HTML + scoped vanilla JS. No React/Vue/Bootstrap/DaisyUI/Flowbite.

## Customization

- Swap the brand name/mark, copy, and colors to fit your product.
- The palette lives inline in the per-page `tailwind.config` (`paper` / `ink` / `terracotta` ramp). Adjust those values to retheme every page at once.
- Replace SVG placeholders in `assets/` with real product screenshots when ready.
