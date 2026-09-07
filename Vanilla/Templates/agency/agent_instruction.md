# Agent Instructions — Agency

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A dark-first editorial creative-agency marketing template: 13 sections (header, hero, about, services, selected work, case study, process, capabilities, team, testimonials, insights, CTA, footer) with mobile nav, scroll-reveal, and scrollspy.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system (Pico CSS + `--ds-*` tokens, Pico's `--pico-*` vars re-pointed at `--ds-*`). **Dark-first, fixed** theme (no light toggle): black bg, white text, single lime accent. Inter type. Square radii, 1px hairline borders, no drop shadows.

## File layout

```
Agency/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # the design system (--ds-* tokens, dark-first)
│   └── script.js      # mobile nav + scroll reveal + scrollspy
├── preview.html       # self-contained preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

No `assets/`&mdash;all imagery is Unsplash CDN URLs; fonts + Pico CSS are CDN.

## How to adapt it

1. **Swap content / imagery**: edit `pages/code.html`; replace Unsplash URLs with the client's imagery.
2. **Rebrand**: edit the `--ds-*` tokens in `pages/style.css` `:root` (the accent is `--ds-color-accent`).
3. **Add a section**: add a `<section>` to `code.html` with a `.ds-reveal` child and an `id` (scrollspy + reveal pick it up automatically).
4. **Rebuild the preview**: regenerate `preview.html` by inlining `style.css` and `script.js` into `code.html`.

## Do not

- Do not add a light-mode toggle&mdash;the dark-first theme is deliberate and fixed.
- Do not replace the lime accent with violet/neon. Keep one controlled accent.
- Do not introduce rounded surfaces or drop shadows; the flat editorial grid is the design language.

## Quality bar

`aria-expanded` + `aria-controls` mobile menu, `aria-current` scrollspy, `:focus-visible` accent ring, descriptive alt text, reduced-motion guard. The head inline `<script>document.documentElement.classList.add('js')</script>` gates reveal (no-JS falls back to visible). Run `python3 scripts/qa_vanilla.py` after changes.

## Gotcha

`script.js` and the inlined `preview.html` script block contain example code strings with literal `<script>` tags&mdash;escape the closing tag as `<\/script>` in JS source inside `preview.html`.
