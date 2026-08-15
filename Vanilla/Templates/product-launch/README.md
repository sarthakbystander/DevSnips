# Product Launch

A clean, restrained product launch / waitlist landing page for a dev-focused product. Part of the DevSnips Vanilla Templates collection and built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system.

## Design language

Minimal · light · editorial · neutral · typography-driven · restrained.

- Light-default, calm opt-in dark mode (no-flash, persisted).
- Hairline 1px borders over shadows; small controlled radii.
- Inter (text) + JetBrains Mono (labels / metadata), system fallbacks.
- Single controlled blue accent; neutral-first palette.
- One primary action per section; hierarchy from type and spacing.

## Structure

```
product-launch/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # design system (--ds-* tokens)
│   └── script.js      # theme toggle, mobile nav, accordion, waitlist form, reveal
├── preview.html       # self-contained single-file preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

`preview.html` opens directly with no backend. The modular files in `pages/` are for customization.

## Sections

1. **Header** — brand mark + version badge, anchor nav, theme toggle, mobile drawer.
2. **Hero + waitlist** — editorial `clamp()` headline, status meta, working waitlist card (validation + success + progress bar).
3. **Social proof** — company logo row.
4. **Features** — three-column grid (six features).
5. **How it works** — four-step numbered list.
6. **Pricing** — two-plan teaser (Free / Team), per-team pricing.
7. **FAQ** — single-open accordion (CSS-grid, ARIA).
8. **Final CTA** — primary + secondary actions.
9. **Footer** — copyright + footer links.

## Interactions

Scoped, dependency-free vanilla JS:

- Theme toggle (light ↔ dark, persisted, no-flash pre-paint).
- Mobile nav drawer (`aria-expanded`, Esc closes, auto-close on link click).
- FAQ accordion (single-open, `aria-expanded`/`aria-controls`/`role=region`).
- Waitlist form (name + email inline validation, `aria-invalid` + `aria-live` errors, simulated submission, success state, count bump).
- Scroll-reveal (`.reveal` → `.is-visible`, reduced-motion safe).

## Accessibility

Skip link, semantic landmarks, single `h1`, ARIA on the accordion and form, `role=img` progress bar, `:focus-visible` rings, native controls throughout, `prefers-reduced-motion` guards.

## Responsive

Three breakpoints (640 / 768 / 1024). Zero horizontal overflow at 320–1920px. Header CTA hides on very small screens (available in the drawer); feature/pricing grids reflow; hero splits to two columns on desktop.

## Dependencies

Google Fonts (Inter + JetBrains Mono). No framework, no build step.
