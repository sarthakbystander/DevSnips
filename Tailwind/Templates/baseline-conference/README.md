# Baseline — Design & Engineering Conference Template

A premium multi-page website template for a fictional two-day design & engineering conference, built in a bold **Neo-Brutalist** design system. Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step, no local asset directories.

Brand used in the template: **Baseline** — a fictional conference in Lisbon, May 14–15, 2026.

## Design language

Neo-Brutalism — the polar opposite of a soft-glass SaaS template:

- Cream paper background (`#FFFDF5`) with near-black ink (`#111111`)
- Hard `border-2 border-black` hairlines everywhere
- Offset drop shadows `shadow-[8px_8px_0_0_#000]` that "press down" on hover
- Flat bright accents: yellow `#FFE600`, pink `#FF4FA3`, lime `#00E676`, cyan `#00C2FF`
- Archivo display type + JetBrains Mono for labels and numbers
- Generous spacing, sharp corners, oversized headlines
- Press-down hover on buttons/cards (translate + shadow shrink)

## Structure

```
baseline-conference/
├── pages/
│   ├── index.html          # Home: hero, stats, tracks, speakers preview, schedule teaser, sponsors, register CTA
│   ├── speakers.html       # Speakers hero, track filter chips, speaker grid (scoped JS filter)
│   ├── schedule.html       # Two-day schedule with day tabs + session cards (scoped JS tabs)
│   ├── venue.html          # Venue hero, CSS map illustration, venue info, travel & accessibility
│   ├── register.html       # Ticket tiers, order summary, registration form with validation
│   └── conduct.html        # Code of conduct: long-form article with quick-nav
├── preview.html            # Template gallery shell: overview + pages index + design-system summary
├── metadata.json
└── README.md
```

No `assets/`, `css/`, `js/`, or `images/` directories — all visuals are Tailwind, inline SVG, and CSS shapes. Avatars are initials in colored blocks.

## Pages

| # | Page | Purpose |
|---|------|---------|
| 01 | Home | Full landing: hero, stats, tracks, speakers preview, schedule teaser, sponsors, CTA |
| 02 | Speakers | Track filter chips + responsive speaker grid |
| 03 | Schedule | Day 1 / Day 2 tabs + session timetable |
| 04 | Venue | CSS map illustration, venue details, travel & accessibility |
| 05 | Register | Ticket tiers, order summary, validated registration form |
| 06 | Code of Conduct | Long-form policy article with quick-nav |

## Responsiveness

Mobile-first, tested from 320px through 1920px+. Fluid type via Tailwind responsive prefixes, responsive nav (hamburger → mobile menu below `lg`), grids that reflow (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3/4`), schedule that stacks on mobile, forms that stay usable on small screens. No horizontal overflow.

## Accessibility

Semantic landmarks (`header`, `nav`, `main`, `footer`), ARIA on the mobile menu and schedule tabs (`aria-expanded`, `role="tablist"`, `role="tab"`, `role="tabpanel"`), visible focus rings, `sr-only` labels on icon-only controls, and a `prefers-reduced-motion` guard that disables hover press animation.

## Usage

Open any page in `pages/` directly in a browser. All links use relative paths so the template works from the file system. Tailwind is loaded via CDN — no install required.
