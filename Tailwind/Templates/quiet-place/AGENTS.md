# AGENTS.md — Quiet Place

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium single-page landing page built with Tailwind CSS around a calm lakeside illustration. The design closely follows a supplied visual reference: a pale mint canvas, compact monospace navigation, condensed two-line headline, three centered feature blocks, coral primary actions,and a large illustrated forest-and-lake scene anchoring the lower half of the hero..



## Design system

Pale mint hero canvas with a soft off-white page surround, deep blue-green editorial type, condensed display headline paired with a compact monospace interface voice, coral pill CTA with a quiet secondary action, pixel-art-inspired illustration using layered SVG shapes, stepped edges, stippled texture,and limited muted colors, large lower illustration rather than generic stock imagery, rounded outer canvas and restrained borders;no glassmorphism or heavy shadows.



## File layout

```
quiet-place/
├── pages/
│   └── index.html
├── preview.html          # Template gallery shell
├── metadata.json
└── README.md
```

No external image assets — the landscape is a handcrafted inline SVG(forest, lake, fisherman, clouds, flowers, reeds, water reflections that stay crisp at every viewport size and can be edited directly in the HTML.



## How to adapt it

1. **Swap the sanctuary**: replace the Quiet Place brand, headline, feature copy,and CTA content in `pages/index.html`.
2. **Re-theme**: edit the color values in the page's inline `tailwind.config` (mint/coral/deep-blue-green ramp).
3. **Edit the illustration**: the SVG landscape in the hero is hand-built—adjust trees, water, fisherman or details directly in the markup.



## Do not

- Do not introduce external image assets or a framework;the inline SVG landscape is deliberate..
- Do not switch the calm mint/coral language to neon or glassmorphism.



## Quality bar

Semantic landmarks, labelled navigation, visible focus states, descriptive SVG title/description, keyboard-friendly buttons/links, touch-friendly controls, `prefers-reduced-motion` handling, mobile-first from 320px through 1920px+. Validate with `python3 scripts/validate.py` after changes.

