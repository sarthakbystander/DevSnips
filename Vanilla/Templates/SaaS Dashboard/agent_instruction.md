# Agent Instructions — SaaS Dashboard

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A multi-page SaaS operator dashboard (31 page files under `pages/`) with a shared mock data layer (`js/`), shared styles (`css/`), and a gallery preview shell (`preview.html`). The realistic product feel comes from the interconnected pages and the shared mock DB&mdash;the highest-value template in the Vanilla set.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system (971 token references, 35 unique tokens). **Light-default.** When adapting:

- Keep the `--ds-*` token layer as the source of truth; do not hardcode hex values.
- Prefer 1px borders over shadows; small controlled radii; restrained surfaces.
- Single controlled accent. No glassmorphism, neon, gradients, or oversized decoration (see `design-tokens.md` §6).
- Dark mode is the same system inverted (calm)&mdash;never black + neon.

## File layout

```
SaaS Dashboard/
├── pages/        # 31 interconnected HTML pages (each links ../css + ../js)
├── css/          # shared dashboard styles (--ds-* tokens)
├── js/           # shared mock DB + interactions
├── assets/       # icons / images
├── preview.html  # gallery shell (overview + page index)
├── metadata.json
└── README.md
```

Pages reference shared `../css` and `../js` via relative paths. The mock data lives in `js/` so every page renders consistently.

## How to adapt it

1. **Rebrand**: edit the `--ds-*` token values (accent, neutrals) in `css/`&mdash;every page updates together.
2. **Add a page**: copy an existing `pages/*.html`, keep the `<link>`/`<script>` relative refs, add a sidebar entry, and register it in `preview.html`'s page index.
3. **Swap the mock data**: replace the dataset in `js/` (keys + realistic content per `design-tokens.md` §48).
4. **Add a chart/table**: use the existing token-driven table styles; prefer light row dividers over boxed cells (`design-tokens.md` §34).

## Do not

- Do not split pages into separate CSS/JS per page&mdash;the shared `css/` + `js/` are what keep the 31 pages coherent.
- Do not introduce a framework (React/Vue/Tailwind/Bootstrap). Vanilla HTML + CSS + JS only.
- Do not remove the `--ds-*` token layer or hardcode visual values.

## Quality bar (enforced by `scripts/qa_vanilla.py`)

Every page must pass: reduced-motion guard on animations, `:focus-visible` ring, ARIA on interactive widgets, keyboard-operable controls. Run `python3 scripts/qa_vanilla.py` after changes.
