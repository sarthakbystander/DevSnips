# AGENTS.md — Krat Adventure Wilderness

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium cinematic wilderness landing page built with Tailwind CSS. The visual direction follows a supplied reference: deep navy canvas, saturated blue surfaces, warm orange/yellow imagery, oversized display type, small technical labels, generous negative space, and an intentionally asymmetric editorial grid.



## Design system

Deep navy `#070A38` foundation, electric royal-blue surfaces, warm sun-yellow and ember-orange accents, Space Grotesk display type + Inter body copy, JetBrains Mono technical labels/metadata, oversized editorial headings, asymmetrical adventure cards with staggered positioning, cinematic image overlays, a full-screen navigation overlay, fine rules, coordinates, route numbers and field-note metadata.



## File layout

```
krat-adventure/
├── pages/
│   └── index.html        # Live single-page site
├── preview.html          # Template gallery shell (overview + sections index)
├── metadata.json
└── README.md
```

No local asset, CSS, or JavaScript directories. Tailwind is loaded through the CDN; photography is referenced from fixed Unsplash image URLsand interaction code is scoped to the page..



## Sections

Hero (full-screen campaign introduction with oversized KRAT wordmark), Adventures (three staggered route cards), The Wild(editorial image/text feature), Expedition(featured expedition with statistics), Journal(three staggered field-note articles), CTA(large conversion section), Footer(minimal navigation and location metadata).



## How to adapt it

1. **Swap the destination**: replace the KRAT product copy, Unsplash photography URLs, routes, journal entries and statistics.
2. **Re-theme**: edit the color values in the page's inline `tailwind.config` (navy/blue/warm accent ramp).
3. **Add a section**: add a `<section>` to `pages/index.html` with matching editorial rhythm; keep the full-screen navigation overlay pattern.



## Do not

- Do not introduce a framework or local asset directories;the template is CDN + Unsplash by design.



## Quality bar

Semantic landmarks, a skip link, labelled navigation controls, visible keyboard focus, descriptive image alt text, an accessible menu button, Escape-to-close behavior, reduced-motion support. Validate with `python3 scripts/validate.py` after changes.

