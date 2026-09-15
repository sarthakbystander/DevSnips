# Developer Portfolio

A personal, technical, editorial-minimal portfolio template for a software / design engineer. Part of the DevSnips Vanilla Templates collection and built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system.

## Design language

Minimal · light · editorial · neutral · typography-driven · restrained.

- Light-default, calm opt-in dark mode (no-flash, persisted).
- Hairline 1px borders over shadows; small controlled radii.
- Inter (text) + JetBrains Mono (labels / metadata), system fallbacks.
- Single controlled blue accent; neutral-first palette.
- High information density with intentional whitespace.

## Structure

```
developer-portfolio/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # design system (--ds-* tokens)
│   └── script.js      # theme toggle, mobile nav, scrollspy, reveal
├── preview.html       # self-contained single-file preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

`preview.html` opens directly with no backend. The modular files in `pages/` are for customization.

## Sections

1. **Header** — brand mark, anchor nav, theme toggle, mobile drawer.
2. **Intro** — editorial `clamp()` lead, availability status badge, metadata grid.
3. **Selected work** — project cards (index, title, role, year, description, stack tags, case-study link).
4. **About** — narrative + capabilities table + four-up stat row.
5. **Notes** — writing list with date + category meta.
6. **Contact** — lead, channels list (email / GitHub / calendar).
7. **Footer** — copyright + footer links.

## Interactions

Scoped, dependency-free vanilla JS:

- Theme toggle (light ↔ dark, persisted, no-flash pre-paint).
- Mobile nav drawer (`aria-expanded`, Esc closes, auto-close on link click).
- Scrollspy active nav (`aria-current="location"` via `IntersectionObserver`).
- Scroll-reveal (`.reveal` → `.is-visible`, reduced-motion safe).

## Accessibility

Skip link, semantic landmarks, single `h1`, `aria-expanded`/`aria-controls` on the mobile toggle, `aria-current` on active nav, `:focus-visible` rings, native controls throughout, `prefers-reduced-motion` guards.

## Responsive

Three breakpoints (640 / 768 / 1024). Zero horizontal overflow at 320–1920px. Nav collapses to a drawer below 768px; grids reflow; intro splits to two columns on desktop.

## Dependencies

Google Fonts (Inter + JetBrains Mono). No framework, no build step.
