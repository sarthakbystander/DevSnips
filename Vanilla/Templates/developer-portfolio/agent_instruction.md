# Agent Instructions — Developer Portfolio

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A personal, technical, editorial-minimal portfolio for a software / design engineer. Single page: header, intro, selected work, about/capabilities, notes, contact, footer.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system. **Light-default**; calm opt-in dark mode (no-flash, persisted). Inter + JetBrains Mono. Hairline 1px borders, small radii, single controlled blue accent.

## File layout

```
developer-portfolio/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # design system (--ds-* tokens)
│   └── script.js      # theme toggle, mobile nav, scrollspy, reveal
├── preview.html       # self-contained preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

## How to adapt it

1. **Swap the persona**: edit `pages/code.html`&mdash;name, brand mark, role, intro lead, status badge, metadata grid.
2. **Swap projects**: edit the `.work-card` blocks in the selected-work section (index, title, role, year, description, stack tags, link).
3. **Swap notes**: edit the `.note-row` blocks (date, category, title, excerpt).
4. **Rebrand**: edit the `--ds-*` tokens in `pages/style.css` `:root`&mdash;keep one controlled accent.
5. **Rebuild the preview**: run `python3 ../_build_preview.py .` from the template folder (inlines `style.css` + `script.js` into `code.html`).

## Do not

- Do not add glassmorphism, neon, gradients, blobs, or oversized decoration.
- Do not introduce a framework. Vanilla HTML + CSS + JS only.
- Do not remove the `--ds-*` token layer or hardcode visual values.

## Quality bar

Skip link, semantic landmarks, single `h1`, `aria-expanded`/`aria-controls` mobile toggle, `aria-current` scrollspy, `:focus-visible` rings, reduced-motion guard. Run `python3 scripts/qa_vanilla.py` after changes. Validate with `python3 scripts/_qa_template.py Vanilla/Templates/developer-portfolio/preview.html` (overflow + console + interactions).
