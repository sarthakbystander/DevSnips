# Product Launch (Ledger)

Clean multi-page product launch and waitlist template built on the DevSnips design-token system.

**Technology:** Vanilla HTML / CSS / JS  
**Category:** templates  
**Subcategory:** product-launch

## Pages

| Page | Path | Purpose |
|------|------|--------|
| Home | `pages/index.html` | Hero, value props, waitlist form |
| Features | `pages/features.html` | Capability overview |
| Pricing | `pages/pricing.html` | Three-tier pricing |
| FAQ | `pages/faq.html` | Accordion Q&A |

## Structure

```
ai-tool-launch/
├── pages/
│   ├── index.html
│   ├── features.html
│   ├── pricing.html
│   ├── faq.html
│   ├── style.css      # Shared design tokens + components
│   └── script.js      # Theme, mobile nav, waitlist demo
├── preview.html       # Canonical preview (loads index)
├── metadata.json
└── README.md
```

## Design system

Uses shared `--ds-*` tokens from `Vanilla/Templates/design-tokens.md`:

- Neutral-first, light mode default
- Black primary actions, hairline borders
- Dark mode via `data-theme="dark"`
- Focus-visible and `prefers-reduced-motion` support

## Usage

1. Open `preview.html` or any file under `pages/` in a browser.
2. No build step. Paths are relative.
3. Waitlist form is front-end only (demo success state).

## Features

- Multi-page navigation with `aria-current`
- Sticky header + mobile menu
- Theme toggle (persisted in localStorage)
- Waitlist email form with success message
- Pricing cards (Starter / Team / Business)
- FAQ details/summary accordion
- Zero dependencies
