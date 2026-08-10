# Neo-Brutalist Sections

65 production-ready, framework-free website sections built with vanilla HTML, CSS, and JavaScript.

## What's here

16 section families, 65 variants total:

| Family | Variants | Examples |
|--------|----------|----------|
| Hero | 10 | minimal, startup, saas, product, gradient, image, split, bento, center, animated |
| Navigation | 4 | simple navbar, sticky navbar, mega menu, sidebar |
| Features | 5 | grid, icons, bento, timeline, comparison |
| Logos | 3 | logo cloud, trusted-by marquee, client cards |
| Statistics | 3 | animated counters, achievement band, KPI cards |
| Products | 6 | showcase, dashboard preview, mobile app, integrations, roadmap, changelog |
| Pricing | 4 | simple, saas (toggle), comparison, enterprise |
| Testimonials | 4 | cards, carousel, masonry, video |
| Team | 3 | grid, leadership, advisors |
| Process | 4 | timeline, workflow, steps, how-it-works |
| Content | 4 | blog grid, featured articles, docs preview, resources |
| Gallery | 3 | masonry, portfolio, projects |
| FAQ | 2 | accordion, searchable |
| CTA | 4 | banner, split, download, newsletter |
| Contact | 3 | form, cards, office locations |
| Footer | 3 | minimal, multi-column, large |

## Design language

Neo-Brutalism: bold typography, 2–3px borders, hard offset shadows, flat colors, high contrast. A shared token system (CSS variables) keeps every section on-brand:

```css
--bg --surface --foreground --muted --border --primary --accent --pink --lime --cyan
--radius --shadow --shadow-lg --ring --container --gutter
```

- Light + dark via `prefers-color-scheme`
- Mobile-first responsive (320px → 1920px), no horizontal scroll
- Reduced-motion safe (`prefers-reduced-motion`)
- Semantic HTML, ARIA, keyboard nav, visible focus rings

## Folder convention (follows existing Vanilla components)

```
Vanilla/Components/<Family>/<variant-slug>/
├── <variant-slug>.html   # self-contained: inline <style> + <script>, copy-paste ready
├── metadata.json         # DevSnips metadata schema
└── README.md             # usage notes
```

Each `.html` is fully standalone — no build step, no external CSS/JS, no frameworks. Just copy it into your page.

## Browse

- `index.html` — filterable gallery of all 65 sections
- `showcase.html` — every section rendered live on one page (each in an isolated iframe)
- Or open any `<variant>.html` directly for a single-section preview

## Customize

Edit the `:root` CSS variables at the top of any section's `<style>` to rebrand colors, radius, and shadows. Swap placeholder text/images for your content.
