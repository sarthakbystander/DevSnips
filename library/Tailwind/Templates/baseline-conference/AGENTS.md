# AGENTS.md — Baseline Conference

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium multi-page website template for a fictional two-day design & engineering conference (**Baseline**, Lisbon, May  ́14–15, 2026), built in a bold **Neo-Brutalist** design system. Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step, no local asset directories.



## Design system

Neo-Brutalism — the polar opposite of a soft-glass SaaS template: cream paper background (`#FFFDF5`), near-black ink (`#111111`), hard `border-2 border-black` hairlines, offset drop shadows `shadow-[8px_8px_0_0_#000]` that "press down" on hover, flat bright accents(yellow `#FFE600`, pink `#FF4FA3`, lime `#00E676`, cyan `#00C2FF`), Archivo display type + JetBrains Mono for labels/numbers, sharp corners, oversized headlines, press-down hover on buttons/cards (translate + shadow shrink).



## File layout

```
baseline-conference/
├── pages/
│   ├── index.html        # Home: hero, stats, tracks, speakers preview, schedule teaser, sponsors, CTA
│   ├── speakers.html     # Track filter chips + speaker grid (scoped JS filter)
│   ├── schedule.html     # Two-day schedule with day tabs + session cards (scoped JS tabs)
│   ├── venue.html        # CSS map illustration, venue info, travel & accessibility
│   ├── register.html     # Ticket tiers, order summary, validated registration form
│   └── conduct.html      # Code of conduct: long-form article
├── preview.html          # Template gallery shell
├── metadata.json
└── README.md
```

No `assets/`, `css/`, `js/`, or `images/` directories — all visuals are Tailwind, inline SVG, and CSS shapes. Avatars are initials in colored blocks.



## How to adapt it

1. **Swap the event**: replace the Baseline branding, dates, speakers, schedule slots, sponsors,and copy across the pages.
2. **Re-theme**: edit the color values in each page's inline `tailwind.config` (cream, ink, accent ramp), keeping the hard border + offset shadow geometry.
3. **Add a page**: duplicate a `pages/*.html`, keep the shared navbar + footer,and swap the `<main>` content. Register it in `preview.html`'s page index.



## Do not

- Do not introduce a framework or a build step. Tailwind CDN + vanilla JS only.
- Do not soften the Neo-Brutalist geometry (hard 2px borders, offset shadows, press-down hover) — it is the design language.
.


## Quality bar

Semantic landmarks (`header`, `nav`, `main`, `footer`), ARIA on the mobile menu and schedule tabs (`aria-expanded`, `role="tablist"`, `role="tab"`, `role="tabpanel"`), visible focus rings, `sr-only` labels on icon-only controls, `prefers-reduced-motion` guard that disables hover press animation. Validate with `python3 scripts/validate.py` after changes.

