# 🚀 DevSnips – Component Library

Reusable frontend components organized as design system families.

## Structure

DevSnips is organized around two content types — **Components** (reusable UI building blocks and sections) and **Templates** (complete website/page templates) — under each supported technology.

```
├── Tailwind/
│   ├── Components/            # 50 families, 526 variants
│   └── Templates/             # 9 full-site templates
├── Vanilla/
│   ├── Components/            # 34 families, 297 variants
│   └── Templates/             # 14 templates
├── React/
│   ├── Components/            # (reserved for future React components)
│   └── Templates/             # (reserved for future React templates)
├── _gen/                      # Section-style component generator
├── scripts/                   # Validation + indexing tooling
├── snippets-index.json        # Content index (106 families, 846 variants)
└── README.md
```

> The former `Sections/`, `Utilities/`, and `Resources/` collections have been
> consolidated. All former Sections are now Components; the standalone
> Utilities and Resources product categories have been removed.

## Quick Start

1. Browse `Tailwind/Components/` for ready-to-use Tailwind components
2. Check `Vanilla/Components/` for HTML/CSS/JS patterns
3. Copy, customize, and ship

## Component Families

### Tailwind

**Components (50 families, 526 variants):**

| Family | Variants |
|--------|----------|
| **Accordions** | 15 |
| **Buttons** | 58 (3-level: 15 style groups × sub-variants) |
| **Cards** | 40 |
| **Dropdowns** | 30 |
| **Input** | 49 |
| **Modals** | 30 |
| **Navigation** | 35 |
| **Progress** | 6 |
| **Tables** | 20 |
| **Tabs** | 15 |
| **Toasts** | 6 |
| **Tooltips** | 6 |
| **404 / Blog / Contact / FAQ / Footer / Logos / Navbar / Newsletter / Stats / Team / Testimonials** | 15 each (11 categories × 15 design styles) |
| **ai-product** | Agent Workflow, AI Chat Interface, Model Comparison, Prompt Library (3 styles each) |
| **app-ui** | Dashboard Overview, Kanban Board (3 styles each) |
| **developer** | Code Playground, Command Palette (3 styles each) |
| **marketing** | Feature Grid, Hero Landing (3 styles each) |
| **premium-visual** | Aurora Hero (3 styles) |
| **saas** | 15 SaaS sections — product-hero, launch-hero, dashboard-hero, feature-grid, bento-showcase, product-workflow, three-tier-pricing, usage-pricing, pricing-comparison, logo-cloud, testimonials, metrics, screenshot-showcase, trial-cta, enterprise-footer |

Design-style reference: `Tailwind/Components/STYLE_TOKENS.md` (neo-brutalism, vercel, sharp-glassmorphism, + the 15 generated styles).

**Templates (9):** ai-saas-platform (multipage), baseline-conference (multipage), devsnips-store (multipage), northline-atelier (multipage), krat-adventure (single-page), meridian (single-page), stratum (single-page), vesper (single-page), quiet-place (single-page).

### Vanilla

**Components (34 families, 293 variants):** Accordions (5), Alerts (2), Avatars (1), Badges (2), Buttons (14), Cards (15), CTA (4), Contact (3), Content (4), Display (6), Dropdowns (1), FAQ (2), Features (5), Footer (3), Forms (36), Gallery (3), Hero (10), Loaders (8), Logos (3), Marketing (6 — FAQ, Hero, Pricing, Testimonials), Media (17), Modals (11), Navigation (28), Other (65), Pricing (4), Process (4), Products (6), Ratings (3), Statistics (3), Tables (4), Tabs (5), Team (3), Testimonials (4), Tooltips (3).

The 15 former Neo-Brutalist Vanilla Sections families (Hero, Navigation, Features, Logos, Statistics, Products, Pricing, Testimonials, Team, Process, Content, Gallery, FAQ, CTA, Contact, Footer) are now merged into `Vanilla/Components/`. Browse them via `Vanilla/Components/sections-index.html` and `Vanilla/Components/sections-showcase.html`.

**Templates (14):** Landing-Pages (one-page-scrolling), Standalone (404-not-found-page, Coming-Soon), ai-tool-launch, blog-landing-pages, event-conference, freelancer-portfolio, html5-boilerplate, micro-saas-product, nft-web3-project, portfolio-site, product-launch, startup-template, template-element.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
