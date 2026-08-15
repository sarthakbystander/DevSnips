# Event Conference

A dense, structured single-track conference website template. Part of the DevSnips Vanilla Templates collection and built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system.

## Design language

Minimal · light · editorial · neutral · typography-driven · restrained.

- Light-default, calm opt-in dark mode (no-flash, persisted).
- Hairline 1px borders over shadows; small controlled radii.
- Inter (text) + JetBrains Mono (labels / metadata), system fallbacks.
- Single controlled blue accent; neutral-first palette.
- Information-dense: schedule, stats, and details tables over decoration.

## Structure

```
event-conference/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # design system (--ds-* tokens)
│   └── script.js      # theme toggle, mobile nav, schedule tabs, countdown, reveal
├── preview.html       # self-contained single-file preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

`preview.html` opens directly with no backend. The modular files in `pages/` are for customization.

## Sections

1. **Header** — brand mark + date, anchor nav, theme toggle, mobile drawer.
2. **Hero + countdown** — editorial `clamp()` headline, facts grid, live countdown card.
3. **About** — narrative + highlights table + four-up stat row.
4. **Speakers** — grid of speakers (avatar initials, name, role, talk).
5. **Schedule** — two-day ARIA tablist + time-rail slot list.
6. **Venue** — narrative + details table.
7. **Sponsors** — capped Partner / Supporter tiers.
8. **Register** — three-tier ticket panel (early-bird / standard / workshop).
9. **Footer** — copyright + footer links.

## Interactions

Scoped, dependency-free vanilla JS:

- Theme toggle (light ↔ dark, persisted, no-flash pre-paint).
- Mobile nav drawer (`aria-expanded`, Esc closes, auto-close on link click).
- Schedule tablist (ARIA `role=tab`, roving tabindex, Arrow Left/Right/Home/End).
- Live countdown to event start (paused when tab hidden).
- Scroll-reveal (`.reveal` → `.is-visible`, reduced-motion safe).

## Accessibility

Skip link, semantic landmarks, single `h1`, ARIA tablist with full keyboard navigation, `role=timer` countdown, `:focus-visible` rings, native controls throughout, `prefers-reduced-motion` guards.

## Responsive

Three breakpoints (640 / 768 / 1024). Zero horizontal overflow at 320–1920px. Header CTA hides on very small screens (available in the drawer); countdown grid collapses to 2 columns at 320px; speakers/register grids reflow; hero splits to two columns on desktop.

## Dependencies

Google Fonts (Inter + JetBrains Mono). No framework, no build step.
