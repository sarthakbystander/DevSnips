# SaaS Dashboard Template (Vanilla)

A complete, commercial-grade **SaaS admin dashboard** template built with plain
HTML, CSS, and vanilla JavaScript. 30 interconnected pages share one coherent
mock dataset, a JS-injected app shell, and a single Northstar design system.
No React, no Tailwind, no bundler, no build step, no backend.

**Technology:** vanilla
**Category:** templates
**Subcategory:** saas-dashboard
**Type:** multipage (30 pages)

## Preview

Open `preview.html` in a browser (a template gallery linking to every page), or
serve the folder for local development:

```bash
cd "Vanilla/Templates/SaaS Dashboard"
python3 -m http.server 8080
# visit http://localhost:8080/preview.html  (gallery)
# or      http://localhost:8080/pages/dashboard.html  (start page)
```

## What's inside

```
SaaS Dashboard/
├── preview.html            # Template gallery — links to every page + design-system summary
├── pages/                  # 30 interconnected pages (see below)
├── css/app.css             # Shared Northstar design system (tokens, shell, components, responsive)
├── js/app.js               # Shared dataset (DB) + app-shell renderer + components + chart utils
├── metadata.json          # DevSnips registration metadata
├── README.md              # This file
└── assets/{logo,favicon}.svg
```

### Architecture

A single `DB` object in `js/app.js` holds all mock data — customers, team,
invoices, transactions, activity, conversations, notifications, API keys,
webhooks, integrations, segments, invitations, sessions, status components,
and incidents. Every page reads from it, so a customer on the Customers page
is the same customer in transactions, activity, and the inbox. **Swap `DB` for
a real API and the render code works unchanged.**

`app.js` also injects the app shell (sidebar + topbar) around each page's
`<main data-page="…">` from a single `NAV` config, so navigation is always
consistent and there are no dead links. Shared components (modal, drawer,
confirm, toast, tabs, breadcrumbs, pagination, pills, avatars, skeleton/empty/
error states) and chart utilities (line, bar, donut, sparkline) are exposed on
`window.NS` / `window.NSCharts`.

### Pages (30)

| Section | Pages |
|---|---|
| **Overview** | dashboard, analytics, reports, activity |
| **Customers** | customers, customer-details, customer-activity, customer-segments, invitations |
| **Revenue** | billing, plans, payment-methods, invoices, transactions |
| **Communication** | inbox, notifications, preferences |
| **Workspace** | team, roles, integrations, workspace-settings |
| **Settings** | settings, profile, security, sessions, api-keys, webhooks |
| **Support** | help-center, support, system-status |

### Design system

One indigo accent (`#4f46e5`) on a cool-stone neutral ramp, semantic status
colors (success/warning/danger/info), hairline borders, restrained shadows, and
tight rhythm — via `--ds-*` CSS variables with light + dark + system-preference
variants. Reused identically across every page so the product feels cohesive.

### Features

- **Coherent mock data** shared across all pages
- **Interactive SVG charts**: line (with comparison + tooltip), bar, donut, sparklines
- **Sortable, paginated, filterable tables** with bulk selection + bulk actions
- **3-panel support inbox** (conversation list / thread / customer sidebar)
- **Modals, drawers, confirmation dialogs, toasts**
- **Permissions matrix, API keys, webhooks, integrations marketplace**
- **System status** with uptime bars + incident history
- **Loading/empty/error** application states
- **Light/dark mode** with no-flash system preference detection
- **Responsive**: sidebar → off-canvas drawer, tables → cards, multi-panel → stacked
- **Accessible**: skip link, ARIA, focus-visible rings, keyboard-operable, reduced-motion safe

### QA

Verified with Playwright across all 30 pages at 9 viewport widths
(320–1920px): **0 console errors, 0 horizontal overflow**. 11 interaction
tests pass (chart toggle, table sort/pagination, bulk selection, tab switching,
inbox reply, modal opening, mobile drawer, notifications dropdown, theme toggle).

Zero dependencies — the only external request is Google Fonts.
