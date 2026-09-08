# Agent Instructions — Atlas Analytics

Guidance for an AI coding agent working with this template. Read this before modifying.

## What this template is

A flagship **11-page** Tailwind CSS product-analytics application template for **Atlas Analytics**, a fictional enterprise analytics platform. Built in a Minimal Editorial Analytics design language — the opposite of a glassy, neon dashboard.

Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step.

## Design language

Minimal, light, editorial, data-dense analytics product interface:
- Neutral-first palette: canvas `#ffffff`, near-black text `#111111`, soft gray secondary `#6b7280`
- Single controlled accent: **blue `#2563eb`** (used only for interactive emphasis, links, primary actions, chart data)
- Semantic status colors used sparingly: success `#16a34a`, warning `#d97706`, danger `#dc2626`, info `#0ea5e9`
- Inter for display + body; JetBrains Mono for metrics, labels, metadata
- 1px hairline borders (`#e5e7eb`), small radii (4–6px), restrained shadows
- Typography-driven hierarchy, controlled content density
- NO neon, purple-on-black, glassmorphism, gradient text, decorative blobs

## Design tokens

Four-layer token model (primitive → semantic → template → component):

```css
:root {
  --ds-gray-0: #ffffff;
  --ds-blue-600: #2563eb;
  --ds-bg-canvas: #ffffff;
  --ds-text-primary: #111111;
  --ds-border-default: #e5e7eb;
  --template-sidebar-width: 248px;
}
[data-theme="dark"] {
  --ds-bg-canvas: #0a0a0a;
  --ds-text-primary: #f5f5f5;
  --ds-border-default: #262626;
}
```

Components consume semantic tokens so dark mode inverts cleanly without touching markup.

## File layout

```
atlas-analytics/
├── preview.html                # Template showcase
├── metadata.json
├── README.md
├── assets/
│   ├── icons/logo.svg          # [A] mark
│   └── images/og-image.svg     # OG card
└── pages/
    ├── index.html              # Overview — KPIs, WAU chart, top sources, activity feed
    ├── analytics.html          # Analytics explorer — metric trend, events table
    ├── funnels.html            # Funnel analysis — 4-stage funnel SVG
    ├── cohorts.html            # Cohort analysis — triangular retention heatmap
    ├── retention.html          # Retention curves — overlapping curves by cohort
    ├── revenue.html            # Revenue analytics — MRR/ARR, plan breakdown
    ├── reports.html            # Saved report cards + builder prompt
    ├── segments.html           # User segment definitions and filters
    ├── dashboards.html         # Custom dashboard builder
    ├── events.html             # Event explorer with filtering
    └── settings.html           # Platform settings
```

## How to adapt it

1. **Swap branding**: Update "Atlas Analytics" brand name throughout; replace logo in `assets/icons/logo.svg`
2. **Rebrand colors**: Modify the blue accent value in CSS custom properties
3. **Edit data**: Replace placeholder metrics, charts, and tables with actual data
4. **Add/remove pages**: Add new HTML files to `pages/`; update navigation accordingly
5. **Customize charts**: SVG charts are inline — modify data points and scales as needed

## Key patterns

- **Sidebar navigation**: Fixed 248px sidebar with active state highlighting
- **Metric cards**: Reusable KPI card pattern with trend indicators
- **SVG charts**: Inline SVG charts with CSS-styled elements
- **Data tables**: Sortable, filterable table patterns
- **Dark mode**: Calm opt-in dark mode via `[data-theme="dark"]` token swap

## Do not

- Do not introduce gradients, glassmorphism, or neon aesthetics
- Do not add external chart libraries — charts are inline SVG
- Do not remove the `prefers-reduced-motion` guards
- Do not change from the minimal editorial analytics aesthetic

## Quality bar

- Semantic HTML with proper landmarks
- ARIA attributes on interactive elements
- Visible focus states on all controls
- `prefers-reduced-motion` support
- Responsive design with collapsible sidebar on mobile

## Gotchas

- Charts are static SVG mockups, not live data visualizations
- Sidebar width is controlled by `--template-sidebar-width` token
- Dark mode requires adding `data-theme="dark"` to `<html>` element
