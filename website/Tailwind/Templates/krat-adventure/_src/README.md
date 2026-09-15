# Krat — Adventure Wilderness Template

A premium cinematic wilderness landing page built with Tailwind CSS. The visual direction follows the supplied reference: deep navy canvas, saturated blue surfaces, warm orange/yellow imagery, oversized display type, small technical labels, generous negative space, and an intentionally asymmetric editorial grid.

## Structure

```text
krat-adventure/
├── pages/
│   └── index.html
├── preview.html
├── metadata.json
└── README.md
```

There are no local asset, CSS, or JavaScript directories. Tailwind is loaded through the CDN; photography is referenced from fixed Unsplash image URLs and interaction code is scoped to the page. `preview.html` is the template gallery shell (overview + sections index + design-system summary); `pages/index.html` is the live single-page site.

## Design language

- Deep navy `#070A38` foundation
- Electric royal-blue surfaces
- Warm sun-yellow and ember-orange accents
- Space Grotesk display typography with Inter body copy
- JetBrains Mono for technical labels and metadata
- Oversized editorial headings and strong vertical rhythm
- Asymmetrical adventure cards with staggered positioning
- Cinematic image overlays rather than conventional cards
- Full-screen navigation overlay
- Fine rules, coordinates, route numbers, and field-note metadata

## Sections

| Section | Purpose |
| --- | --- |
| Hero | Full-screen campaign introduction with oversized KRAT wordmark |
| Adventures | Three staggered route cards |
| The Wild | Editorial image/text feature section |
| Expedition | Featured expedition with statistics |
| Journal | Three staggered field-note articles |
| CTA | Large conversion section |
| Footer | Minimal navigation and location metadata |

## Responsive & accessibility

The page is mobile-first and designed from 320px through 1920px+. Desktop compositions use asymmetric grids and staggered cards; mobile switches to a deliberate vertical editorial flow. It includes semantic landmarks, a skip link, labelled navigation controls, visible keyboard focus, descriptive image alt text, an accessible menu button, Escape-to-close behavior, and reduced-motion support.

## Usage

Open `index.html` directly or serve the directory with a static server. No build step is required.
