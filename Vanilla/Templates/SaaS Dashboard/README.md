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

- **Dense metric hierarchy** — a primary MRR card with a prominent display value
  plus three secondary KPIs (active customers, conversion rate, ARPU). Each card
  carries a delta vs. the previous period and a mini sparkline.
- **Interactive SVG revenue chart** — period toggle (7d / 30d / 12m) with a
  two-series comparison (this period vs. last), proper axes + gridlines, and a
  hover/touch tooltip with a crosshair. Pure SVG generated in JS — no chart library.
- **Plan-breakdown panel** — a stacked bar with per-plan customers and MRR, a legend,
  and a total-MRR footer.
- **Activity timeline** — recent workspace events with avatars, event + target,
  status dots, and timestamps.
- **Transactions list** — invoice IDs, customer + company, amounts, and status pills.
- **Customers table** — sortable columns (click headers), paginated, and filterable
  by name/email/plan. It transforms into stacked cards below the tablet breakpoint.
  Per-row view/delete actions surface a toast and remove the row.
- **Workspace-usage panel** — quota bars (seats, API calls, storage) with an upgrade
  prompt.
- **Dark mode** — follows the system `prefers-color-scheme` on first paint (no flash),
  with a header toggle that persists the choice in `localStorage`.
- **Responsive sidebar** — fixed sidebar on desktop; converts to an off-canvas drawer
  with a backdrop below 1024px. `Esc` and the backdrop close it.
- **Refined neutral design system** — all colors, radii, shadows, spacing, and fonts
  are `--ds-*` CSS variables in `:root` (cool-stone surfaces, hairline borders,
  restrained shadows, one indigo accent, semantic status colors), with a dark-mode
  override under `[data-theme="dark"]`.
- **Data abstraction** — all content lives in a single `DASHBOARD` object in
  `js/dashboard.js`, so you can swap in a real API without touching any render code.

## Accessibility

- Skip-to-content link.
- Semantic landmarks (`aside`, `header`, `main`, `nav`, `footer`).
- `aria-pressed` on the period segmented control and theme toggle; `aria-current` on
  the active nav item; `aria-sort` on the table headers; `aria-label` on icon-only
  buttons; the chart has a descriptive `role="img"` + `aria-label`.
- Visible `:focus-visible` ring on every interactive control.
- `prefers-reduced-motion` disables animations, sparklines, and count-up easing.
- All controls are real `<button>`/`<a>`/`<input>` elements; row actions are buttons
  with descriptive labels; the sidebar drawer is keyboard-closable via `Esc`.

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
