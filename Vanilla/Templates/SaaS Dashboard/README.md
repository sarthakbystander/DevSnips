# SaaS Dashboard (Vanilla)

A self-contained, framework-free **SaaS admin dashboard** template built with plain
HTML, CSS, and vanilla JavaScript. Drop the folder into any project — no React, no
Tailwind, no bundler, no build step.

**Technology:** vanilla
**Category:** templates
**Subcategory:** saas-dashboard

## Preview

Open `preview.html` directly in a browser (no server needed — it's self-contained):

```bash
# Option A: just open the file
open "Vanilla/Templates/SaaS Dashboard/preview.html"

# Option B: serve the folder (handy for hot-reloading during edits)
cd Vanilla/Templates/SaaS\ Dashboard
python3 -m http.server 8080
# visit http://localhost:8080/preview.html
```

## What's inside

```
SaaS Dashboard/
├── preview.html        # Self-contained live demo — all CSS/JS/SVG inlined, open directly in a browser
├── code.html          # Same dashboard with the snippet comment header, ready to copy-paste
├── metadata.json      # DevSnips registration metadata
├── README.md           # This file
├── css/dashboard.css  # Optional: the dashboard stylesheet split out for modular projects
├── js/dashboard.js    # Optional: the dashboard script split out for modular projects
└── assets/{logo,favicon}.svg
```

`preview.html` and `code.html` are fully self-contained single files (inline `<style>` +
`<script>`, logo as a data URI) — matching the DevSnips Vanilla/Templates convention
(e.g. `micro-saas-product/preview.html`). Open either in a browser with no server
required. The `css/`, `js/`, and `assets/` folders are provided for developers who
prefer a split, modular setup — move the inlined `<style>`/`<script>` into those files
and link them with `<link rel="stylesheet" href="css/dashboard.css">` and
`<script src="js/dashboard.js" defer></script>`.

## Features

- **Interactive SVG line chart** — period toggle (7d / 30d / 12m) with a hover/touch
  tooltip and crosshair. No charting library; pure SVG generated in JS.
- **Animated count-up KPI cards** — revenue, active customers, conversion rate, and
  average session animate on load (reduced-motion aware).
- **Activity feed** — recent workspace events rendered from a small JS data array.
- **Customer table** — plan, status pills, MRR, last-active; per-row view/delete
  actions surface a toast and remove the row.
- **Dark mode** — follows the system `prefers-color-scheme` on first load, with a
  header toggle that persists the choice in `localStorage`.
- **Responsive sidebar** — fixed sidebar on desktop; converts to an off-canvas drawer
  with a backdrop below 860px. `Esc` closes it.
- **Design-token system** — all colors, radii, shadows, spacing, and fonts are
  `--ds-*` CSS variables in `:root`, with a dark-mode override under
  `@media (prefers-color-scheme: dark)` and `[data-theme="dark"]`.

## Accessibility

- Skip-to-content link.
- Semantic landmarks (`aside`, `header`, `main`, `nav`, `footer`).
- `aria-pressed` on the segmented control and theme toggle; `aria-current` on the
  active nav item; `aria-label` on icon-only buttons.
- Visible `:focus-visible` ring on every interactive control.
- `prefers-reduced-motion` disables animations and count-up easing.
- Customer table row actions are real `<button>`s with descriptive labels.

## Usage

### Option A — use the folder (recommended)

Copy `SaaS Dashboard/` into your project and link the assets:

```html
<link rel="stylesheet" href="css/dashboard.css">
<!-- ... markup from preview.html ... -->
<script src="js/dashboard.js" defer></script>
```

### Option B — single-file copy-paste

`code.html` is a single self-contained file with all CSS and JS inlined and the SVG
logo embedded as a data URI. Copy its contents into any `.html` file and open it —
no external requests except the Google Fonts.

## Theming

Override the design tokens to re-skin the whole dashboard:

```css
:root {
  --ds-accent: #0ea5e9;        /* primary accent */
  --ds-accent-strong: #0284c7;
  --ds-radius: 10px;           /* global corner radius */
  --ds-sidebar-w: 240px;       /* sidebar width */
}
```

For a fixed light or dark palette regardless of system preference, set
`data-theme="dark"` (or `"light"`) on the `<html>` element and remove the
`prefers-color-scheme` media query — or just let the toggle drive it.

## Data

All data is illustrative and lives in `js/dashboard.js` (`series`, `ACTIVITY`).
Replace those arrays with real API responses to wire the template to your backend.
The chart redraws via `drawChart(key)`; call it after swapping `series`.

## Browser support

Latest Chrome, Firefox, Safari, and Edge. Uses CSS custom properties, CSS Grid,
and `localStorage` — all baseline in modern browsers.

## Dependencies

Google Fonts: **Inter** (UI) and **JetBrains Mono** (figures/labels). Both are
optional — the stack falls back to system fonts if the network is unavailable.

## License

Part of the DevSnips project. See the repository `LICENSE`.
