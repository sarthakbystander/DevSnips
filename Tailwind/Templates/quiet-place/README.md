# Quiet Place — Mindfulness & Creative Sanctuary

A premium single-page landing page built with Tailwind CSS around a calm lakeside illustration. The design closely follows the supplied visual reference: a pale mint canvas, compact monospace navigation, condensed two-line headline, three centered feature blocks, coral primary actions, and a large illustrated forest-and-lake scene anchoring the lower half of the hero.

## Structure

```text
quiet-place/
├── pages/
│   └── index.html
├── preview.html
├── metadata.json
└── README.md
```

There are no external image assets. The landscape is a handcrafted inline SVG so the trees, clouds, fisherman, shoreline, plants, flowers, water, and reflections remain crisp at every viewport size and can be edited directly in the HTML. `preview.html` is the template gallery shell (overview + sections index + design-system summary); `pages/index.html` is the live single-page site.

## Design language

- Pale mint hero canvas with a soft off-white page surround
- Deep blue-green editorial type
- Condensed display headline paired with a compact monospace interface voice
- Coral pill CTA with a quiet secondary action
- Pixel-art-inspired illustration using layered SVG shapes, stepped edges, stippled texture, and limited muted colors
- Large lower illustration rather than generic stock imagery
- Rounded outer canvas and restrained borders; no glassmorphism or heavy shadows

## Illustration

The hero artwork is intentionally detailed rather than decorative placeholder art. It contains:

- layered pine forests on both sides of the lake
- foreground grass, reeds, shrubs, flowers, stones, and shoreline texture
- a seated fisherman with a rod and line reaching into the water
- distant atmospheric clouds
- multiple water bands and horizontal reflection marks
- small pixel-like highlights and texture clusters
- responsive scaling without losing the composition

## Responsive behavior

The page is mobile-first and designed from 320px through 1920px+. Desktop preserves the wide reference composition. Tablet spacing and artwork scale down progressively. On small screens the navigation collapses, the feature blocks stack, the headline scales down, and the landscape remains visible instead of being removed.

## Accessibility

Semantic landmarks, labelled navigation, visible focus states, descriptive SVG title/description, keyboard-friendly buttons/links, touch-friendly controls, and `prefers-reduced-motion` handling are included.

## Usage

Open `pages/index.html` directly or serve the directory with any static server. Tailwind is loaded from the CDN, so there is no build step.
