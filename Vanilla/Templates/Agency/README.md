# Agency Template (Vanilla)

A premium, **dark-first** editorial agency website template built for DevSnips
with semantic HTML, CSS (Pico CSS foundation), and vanilla JavaScript. The
template is split into modular files — `code.html` (HTML structure) +
`style.css` (the design system) + `script.js` (navigation, scroll reveal, and
scrollspy interactions) — with `preview.html` as a self-contained single-file
preview of the UI so you can open it directly and see exactly how the template
looks.

**Technology:** vanilla
**Category:** templates
**Subcategory:** agency
**Type:** single-page (one-page agency marketing site)

## Files

```
Agency/
├── code.html               # HTML structure (links style.css + script.js) — the modular source
├── style.css               # the design system (Pico CSS foundation + DevSnips --ds-* tokens)
├── script.js               # mobile nav + scroll reveal + scrollspy (vanilla JS, no deps)
├── preview.html            # single-file preview of the UI (inlines style.css + script.js) — open this to see it
├── metadata.json           # DevSnips registration metadata
└── README.md               # This file
```

No `assets/` directory is required. The template uses no local images, icons,
fonts, or other binary assets. All imagery is loaded from Unsplash URLs and all
fonts and the Pico CSS base are loaded from CDNs (see **Dependencies**).

## Preview

Open `preview.html` directly in a browser to see the template — it is a
self-contained single-file preview that inlines the CSS and JS:

```bash
cd "Vanilla/Templates/Agency"
python3 -m http.server 8080
# visit http://localhost:8080/preview.html
```

For development and customization, work with the split files — open `code.html`
(which references `style.css` and `script.js` relatively) in the same served
folder. The whole template runs without a build step. The only external requests
are Google Fonts (Inter), Pico CSS, and the Unsplash images, all from CDNs.

Per the shared `design-tokens.md` convention, the template folder contains
exactly **one** `preview.html`. It is the canonical preview shown by the DevSnips
website. It is fully responsive, uses the template's real CSS/JS, uses relative
paths, and loads correctly when opened directly.

### Architecture

The template is split into three modular files plus a single-file preview:

- **`code.html`** — the HTML shell (header, hero, about, services, work, case
  study, process, capabilities, team, testimonials, insights, CTA, footer) that
  links `style.css` and `script.js`. This is the modular source you customize.
- **`style.css`** — the entire design system: Pico CSS overrides, the `--ds-*`
  token block, base/typography/button styles, every section style, the
  responsive breakpoints, and the reduced-motion guard.
- **`script.js`** — the runtime: mobile navigation toggle, IntersectionObserver
  scroll-reveal animations, and scrollspy active-nav state. No dependencies.
- **`preview.html`** — a self-contained single-file preview that inlines
  `style.css` and `script.js` into the `code.html` structure, so it can be opened
  directly with no build step and renders identically to the modular version.

## Sections

The page is composed of these sections, in order:

1. **Header** — sticky nav bar with logo, anchor links, a primary CTA, and a
   mobile menu toggle (below 768px).
2. **Hero** — large-typography headline with an asymmetric two-column text +
   image grid and a meta row (projects, contributors, client rating).
3. **About** — split heading + paragraph with a two-up statistics grid
   (projects delivered, core contributors).
4. **Services** — editorial numbered list of six service offerings.
5. **Selected Work** — alternating image/content project layouts (two projects).
6. **Case Study** — featured case study with Challenge / Approach / Solution /
   Results and a 16:9 image.
7. **Process** — five-step horizontal grid (Discover, Define, Design, Build,
   Refine).
8. **Capabilities** — four-up grid (Visual Identity, Interaction Design,
   Accessibility, Performance).
9. **Team** — four-up team grid with square portraits.
10. **Testimonials** — three-up testimonial cards with blockquotes and citations.
11. **Insights** — three-up blog/insights cards with category, date, and read
    time meta.
12. **CTA** — centered contact call-to-action.
13. **Footer** — four-column footer (brand, navigation, resources, community)
    with a bottom bar.

## Design system

The template extends the shared DevSnips `--ds-*` token system (defined in
[`design-tokens.md`](../design-tokens.md)) and overlays Pico CSS defaults.

- **Palette** — black `#000000` background, white text, one lime accent
  `#ccff00`, gray-100 `#f4f4f4`, gray-600 `#666666`, gray-900 `#121212`. The theme
  is **dark-first and fixed** — there is no light-mode toggle.
- **Typography** — Inter (400 / 600 / 800 / 900) from Google Fonts; oversized
  `clamp()`-based hero and CTA headlines, an uppercase eyebrow label, and a
  tight `letter-spacing` on headings.
- **Geometry** — `0px` radius (square corners), `1px solid #222` hairline
  borders, no rounded surfaces and no drop shadows — a flat, editorial grid.
- **Spacing** — a base-4 `--ds-space-*` ramp (0.25rem → 4rem).
- **Motion** — a single `0.3s cubic-bezier(0.4, 0, 0.2, 1)` transition token;
  IntersectionObserver scroll-reveal fades sections in. All motion is gated by
  `@media (prefers-reduced-motion: reduce)`.

To re-theme the template, edit the `--ds-*` custom properties at the top of
`style.css` (`:root`). Pico CSS variables (`--pico-*`) are re-pointed at the
`--ds-*` tokens so Pico inherits the theme automatically.

## Usage

Copy the `Agency/` folder into your project and open `code.html` (serving the
folder over HTTP so the relative `style.css` and `script.js` load), or copy the
HTML, CSS, and JavaScript into an existing project. No build step or backend is
required. To swap images, replace the Unsplash `src` URLs in `code.html` (and in
`preview.html` if you keep it in sync) with your own.

## Responsive behavior

The layout is responsive by composition with three breakpoints:

- **≤ 768px** — the nav links collapse into a dropdown menu toggled by the menu
  button (`aria-expanded`), the primary CTA hides, the hero and project grids
  stack to one column, the about/case-study grids stack, and the process /
  capabilities / team / testimonials / insights / footer grids reflow to 1–2
  columns. Headline `clamp()` ranges shrink for narrow screens.
- **769–1024px** — the hero and about grids collapse to single columns, the
  process grid becomes 3-up, capabilities 2-up, team 2-up, testimonials 2-up,
  insights 2-up, and the footer 2-up.
- **> 1024px** — the full multi-column editorial layout is restored.

`overflow-x: hidden` on `body` plus fluid `clamp()` typography and
`max-width: 1400px` containers keep the page free of horizontal overflow from
320px to 1920px.

## Accessibility

- Semantic HTML landmarks (`header`, `nav`, `main`, `section`, `article`,
  `footer`) and a single `h1`.
- Skip-to-content link revealed on focus.
- Mobile navigation uses `aria-expanded` and `aria-controls`; the menu button
  label/icon swaps between `☰` and `✕`.
- `aria-current="location"` is set on the active scrollspy navigation link.
- `:focus-visible` outline (2px accent) on all interactive controls.
- `prefers-reduced-motion: reduce` disables smooth scroll, scroll-reveal
  transforms, and all CSS transitions/animations.
- Descriptive `alt` text on all images; decorative ordering uses CSS `order`
  rather than DOM reordering.

## Dependencies

- **Pico CSS** (`@picocss/pico@2`) — loaded from `cdn.jsdelivr.net` (CDN).
- **Google Fonts** — Inter (400 / 600 / 800 / 900), loaded from
  `fonts.googleapis.com`.
- **Unsplash** — imagery loaded from `images.unsplash.com` URLs (CDN).

No npm packages, build tools, bundlers, or JavaScript frameworks are required.
The vanilla JavaScript in `script.js` has no runtime dependencies.

## Browser support

Chrome, Firefox, Safari, and Edge (modern evergreen browsers). Uses standard
CSS Grid, custom properties, `clamp()`, `backdrop-filter`, and
`IntersectionObserver` — all supported in current evergreen browsers.

## Customization

- **Colors / typography / spacing** — edit the `--ds-*` tokens in the `:root`
  block of `style.css`.
- **Content** — edit the HTML in `code.html` (and mirror to `preview.html` to
  keep the preview in sync, or regenerate it by inlining `style.css` +
  `script.js` into `code.html`).
- **Sections** — add or remove `<section class="ds-…">` blocks in `code.html`;
  add `ds-reveal` to opt a section into scroll reveal, and ensure any
  `section[id]` you want in the scrollspy nav has a matching `#id` link in the
  header nav list.
- **Images** — replace the Unsplash `src` URLs with your own assets.
