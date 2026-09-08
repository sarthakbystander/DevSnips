# Agent Instructions — Baseline Conference

Guidance for an AI coding agent working with this template. Read this before modifying.

## What this template is

A premium multi-page website template for **Baseline** — a fictional two-day design & engineering conference in Lisbon, May 14–15, 2026. Built in a bold **Neo-Brutalist** design system.

Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step.

## Design language

Neo-Brutalism — sharp, bold, press-down interactions:
- Cream paper background (`#FFFDF5`) with near-black ink (`#111111`)
- Hard `border-2 border-black` hairlines everywhere
- Offset drop shadows `shadow-[8px_8px_0_0_#000]` that "press down" on hover
- Flat bright accents: yellow `#FFE600`, pink `#FF4FA3`, lime `#00E676`, cyan `#00C2FF`
- Archivo display type + JetBrains Mono for labels and numbers
- Generous spacing, sharp corners, oversized headlines
- Press-down hover on buttons/cards (translate + shadow shrink)

## File layout

```
baseline-conference/
├── pages/
│   ├── index.html          # Home: hero, stats, tracks, speakers, schedule, sponsors, register CTA
│   ├── speakers.html       # Speakers with track filter chips (scoped JS filter)
│   ├── schedule.html       # Two-day schedule with day tabs (scoped JS tabs)
│   ├── venue.html          # Venue info, CSS map illustration, travel & accessibility
│   ├── register.html       # Ticket tiers, order summary, registration form with validation
│   └── conduct.html        # Code of conduct: long-form article with quick-nav
├── preview.html            # Template gallery shell
├── metadata.json
└── README.md
```

No `assets/`, `css/`, `js/`, or `images/` directories — all visuals are Tailwind, inline SVG, and CSS shapes. Avatars are initials in colored blocks.

## How to adapt it

1. **Swap event details**: Update conference name, dates, location throughout
2. **Edit speakers/schedule**: Modify speaker cards and session data in respective pages
3. **Rebrand colors**: Adjust the four accent colors while maintaining neo-brutalist aesthetic
4. **Update registration**: Modify ticket tiers and form fields as needed
5. **Customize venue**: Replace venue information and update CSS map illustration

## Key patterns

- **Track filter chips**: JavaScript-powered filtering of speakers by track
- **Day tabs**: Tab switching for two-day schedule view
- **Press-down interaction**: Translate + shadow shrink on hover/active states
- **Code of conduct nav**: Quick navigation within long-form content

## Do not

- Do not soften the brutalist aesthetic with rounded corners or soft shadows
- Do not add gradients or glassmorphism effects
- Do not remove the hard black borders that define the style
- Do not change the offset shadow direction

## Quality bar

- Semantic HTML with proper heading hierarchy
- ARIA attributes on interactive elements (tabs, filters)
- Visible focus states matching the brutalist aesthetic
- Keyboard navigation for tabs and filters
- Responsive design from mobile to desktop

## Gotchas

- Speaker filtering uses scoped vanilla JS — ensure filter logic matches updated speaker data
- Schedule tabs require matching data-day attributes
- All imagery is CSS/SVG-based — no external image dependencies
