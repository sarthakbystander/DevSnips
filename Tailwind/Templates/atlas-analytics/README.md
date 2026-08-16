# Atlas Analytics Platform — Template

A flagship **11-page** Tailwind CSS product-analytics application template for **Atlas Analytics**, a fictional enterprise analytics platform. Built in a **Minimal Editorial Analytics** design language — the opposite of a glassy, neon, AI-aesthetic dashboard. Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step.

The product brand is **Atlas Analytics**, and the logo mark is a hairline **[A]** (`assets/icons/logo.svg`).

> Atlas is a reference implementation for **composition** — eleven independently-usable application pages sharing one shell, demonstrating how dozens of small, reusable pieces combine into a coherent product UI without a framework, build system, backend, or JavaScript application.

## Design language

Minimal, light, editorial, data-dense — closer to a refined analytics product interface than a decorative marketing template:

- Neutral-first palette: canvas `#ffffff`, near-black text `#111111`, soft gray secondary `#6b7280`, muted `#9ca3af`, and a 16-step gray ramp
- A single controlled accent: **blue `#2563eb`** (used only for interactive emphasis, links, primary actions and chart data — never as decoration)
- Semantic status colors used sparingly: success `#16a34a`, warning `#d97706`, danger `#dc2626`, info `#0ea5e9`
- **Inter** for display + body; **JetBrains Mono** for metrics, labels and metadata
- 1px hairline borders (`#e5e7eb`), small radii (4–6px), restrained shadows (`0 1px 2px rgb(0 0 0 / 0.04)`)
- Typography-driven hierarchy, generous-but-intentional whitespace, controlled content density
- **No** neon, purple-on-black, glassmorphism, frosted cards, gradient text, glowing borders, decorative blobs or animated backgrounds

## Design tokens

The system is expressed through CSS custom properties so the entire UI — including a calm dark mode — is a variable swap. The four-layer token model (primitive → semantic → template → component) follows the DevSnips shared design-token philosophy:

```css
:root {
  --ds-gray-0: #ffffff;        /* primitive neutrals */
  --ds-blue-600: #2563eb;      /* controlled accent */
  --ds-bg-canvas: #ffffff;     /* semantic background */
  --ds-text-primary: #111111;  /* semantic text */
  --ds-border-default: #e5e7eb;
  --template-sidebar-width: 248px;
}
[data-theme="dark"] {
  --ds-bg-canvas: #0a0a0a;
  --ds-text-primary: #f5f5f5;
  --ds-border-default: #262626;
}
```

Components consume semantic tokens (`.bg-canvas`, `.bg-surface`, `.text-primary`, `.text-secondary`, `.text-muted`, `.bd`, `.bd-subtle`, `.bd-strong`, `.accent`) so dark mode inverts cleanly without touching markup.

## Structure

```
atlas-analytics/
├── preview.html                # Template showcase — overview, page index, design-system summary
├── metadata.json
├── README.md
├── assets/
│   ├── icons/logo.svg          # [A] mark (hairline frame, geometric peak, blue apex dot)
│   └── images/og-image.svg     # Editorial OG card with headline + mini dashboard
└── pages/
    ├── index.html              # Overview — KPIs, WAU chart, top sources, activity feed
    ├── analytics.html          # Analytics explorer — metric trend, events table, distribution
    ├── funnels.html            # Funnel analysis — 4-stage funnel SVG, drop-off, comparison
    ├── cohorts.html            # Cohort analysis — triangular retention heatmap
    ├── retention.html          # Retention curves — overlapping curves by cohort
    ├── revenue.html            # Revenue analytics — MRR/ARR, trend, plan breakdown, transactions
    ├── reports.html            # Reports — saved report cards + builder prompt
    ├── dashboards.html         # Dashboards — custom widget grid + empty state
    ├── segments.html           # Segments — audience segment table with trends
    ├── events.html             # Events — event frequency table + naming guidance
    └── settings.html           # Settings — tabbed workspace/general/billing
```

No `css/`, `js/` or `images/` directories beyond `assets/` — all visuals are inline SVG and Tailwind. Charts are hand-built SVG (sparklines, area, bar, funnel, heatmap, retention curves) with a consistent restrained stroke language.

## The shared Atlas shell

Every page renders the same application chrome, inlined per page (copy-paste — no server includes, no framework):

```
┌─────────────────────────────────────────────────────┐
│ [A] Atlas    Prod ▾   ⌘K Search          ☾  JD      │  ← sticky topbar
├──────────────┬──────────────────────────────────────┤
│ ANALYZE      │  Overview / Home                     │
│  Overview    │  ───────────────────────────────     │
│  Analytics   │                                      │
│  Funnels     │          PAGE CONTENT                │
│  Cohorts     │                                      │
│  Retention   │                                      │
│  Revenue     │                                      │
│ BUILD        │                                      │
│  Reports     │                                      │
│  Dashboards  │                                      │
│  Segments    │                                      │
│  Events      │                                      │
│ CONFIGURE    │                                      │
│  Settings    │                                      │
└──────────────┴──────────────────────────────────────┘
```

Navigation uses plain relative links (`<a href="analytics.html">`), so the entire product is navigable by opening any single `pages/*.html` file directly in a browser.

### Responsive behavior

- **Desktop (`lg+`)**: full 248px sidebar + 64px topbar + wide content
- **Tablet / mobile (`<lg`)**: sidebar collapses into a slide-in drawer (hamburger toggle, `aria-expanded`/`aria-controls`, Esc + backdrop close); content reflows to a single column; KPI grids reduce; charts scale to width; tables become horizontally scrollable inside `overflow-x-auto`

## Pages

| # | Page | Purpose |
|---|------|---------|
| 01 | Overview | KPI grid with sparklines, weekly active-users area chart, top traffic sources table, recent activity feed |
| 02 | Analytics | Metric trend chart with range + metric switching (scoped JS), events table, event distribution bars |
| 03 | Funnels | 4-stage conversion funnel SVG with per-stage drop-off, step table and compare-period toggle |
| 04 | Cohorts | Triangular weekly retention heatmap with percentage cells and cohort size column |
| 05 | Retention | Overlapping retention curves by cohort with legend and N-week retention table |
| 06 | Revenue | MRR/ARR KPIs, revenue trend area chart, plan breakdown bars, recent transactions table |
| 07 | Reports | Saved report cards with schedule badges, last-run metadata and a report-builder prompt |
| 08 | Dashboards | Custom dashboard grid with widget cards and an empty-state prompt |
| 09 | Segments | Audience segment table with size, composition, status and trend sparkline |
| 10 | Events | Event frequency table, naming-convention guidance and sample event payloads |
| 11 | Settings | Tabbed (Workspace / General / Billing) form with toggles, selects, a danger zone |

## Notable design decisions

- **Light, not dark.** Atlas is deliberately the one light, minimal, data-dense product UI in the Tailwind templates — a deliberate contrast to stratum (neo-brutalist dark), meridian (hairline amber) and vesper (glassmorphism cyber). Dark mode is a calm inversion of the same system.
- **Charts are hand-built SVG**, not a charting library — sparklines, area charts, bar charts, a funnel, a triangular cohort heatmap and overlapping retention curves. The palette stays neutral with the blue accent reserved for the primary series.
- **Density over decoration.** Hierarchy comes from typography, spacing, alignment and 1px borders — not from cards, shadows or color blocks. Tables use light row dividers; KPIs are unboxed where a clean grid suffices.
- **One controlled accent.** Blue `#2563eb` appears only on interactive emphasis, links, primary buttons and chart data. Status colors (green/amber/red) appear only on status — never as decoration.
- **Scoped vanilla JS** — each interaction (drawer, command palette, tabs, metric/range switching, theme toggle) is a small IIFE, reduced-motion safe.

## Accessibility

Semantic landmarks (`header`, `nav`, `main`, `footer`), skip link, a single `h1` per page, ARIA on the drawer (`aria-expanded`/`aria-controls`), command palette (`role="dialog"`/`aria-modal`), settings tabs (`role="tablist"`/`tab`/`tabpanel`) and the theme toggle; visible focus rings in the accent color; `prefers-reduced-motion` disables transitions and the command-palette fade.

## Technology & dependencies

- Tailwind CSS via CDN (`https://cdn.tailwindcss.com`) with a small inline `tailwind.config` theme extension (semantic colors + font families)
- Google Fonts: Inter, JetBrains Mono
- Vanilla JavaScript (scoped IIFEs; `IntersectionObserver` not required)
- No build step, no npm, no frameworks

## Usage

Open `preview.html` for the template showcase, or open any page in `pages/` directly in a browser. All links use relative paths so the template works from the file system — download it, open `pages/index.html`, and navigate the entire product without a server.

> Atlas Analytics is a fictional brand created for this DevSnips template. All metrics, accounts, events and copy are invented.
