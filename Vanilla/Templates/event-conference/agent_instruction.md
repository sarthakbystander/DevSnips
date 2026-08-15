# Agent Instructions — Event Conference

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A dense, structured single-track conference website. Single page: header, hero + countdown, about, speakers, schedule (two-day tablist), venue, sponsors, register, footer.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system. **Light-default**; calm opt-in dark mode (no-flash, persisted). Inter + JetBrains Mono. Hairline borders, small radii, single controlled blue accent, information-dense tables over decoration.

## File layout

```
event-conference/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # design system (--ds-* tokens)
│   └── script.js      # theme toggle, mobile nav, schedule tabs, countdown, reveal
├── preview.html       # self-contained preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

## How to adapt it

1. **Swap the event**: edit `pages/code.html`&mdash;brand, dates, location, facts grid, about copy, speakers, schedule slots, venue details, sponsor tiers, register tiers.
2. **Set the countdown target**: edit the `target` Date in `pages/script.js` (`new Date('YYYY-MM-DDT09:00:00Z')`). The countdown auto-pauses when the tab is hidden.
3. **Add a schedule day**: add a new `.tab-link` (with `role=tab`, `aria-controls`, `data-tab`) and a matching `.tab-panel` (with `role=tabpanel`); the tablist keyboard logic in `script.js` handles any number of tabs.
4. **Rebrand**: edit the `--ds-*` tokens in `pages/style.css` `:root`&mdash;keep one controlled accent.
5. **Rebuild the preview**: run `python3 ../_build_preview.py .` from the template folder.

## Do not

- Do not add glassmorphism, neon, gradients, or animated decorative backgrounds.
- Do not introduce a framework. Vanilla HTML + CSS + JS only.
- Do not break the ARIA tablist contract (`role=tab`/`tabpanel`, `aria-selected`, roving tabindex, arrow-key nav).

## Quality bar

Skip link, semantic landmarks, single `h1`, ARIA tablist with full keyboard nav (Arrow Left/Right/Home/End), `role=timer` countdown, `:focus-visible` rings, reduced-motion guard. Run `python3 scripts/qa_vanilla.py` after changes. Validate with `python3 scripts/_qa_template.py Vanilla/Templates/event-conference/preview.html`.
