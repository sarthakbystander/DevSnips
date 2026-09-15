# AGENTS.md — Atlas Analytics Platform

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A flagship **11-page** Tailwind CSS product-analytics application template for **Atlas Analytics**, a fictional enterprise analytics platform. Built in a **Minimal Editorial Analytics** design language — the opposite of a glassy, neon, AI-aesthetic dashboard. Tailwind CSS (via CDN) + vanilla HTML + scoped vanilla JS. No frameworks, no build step.

The template is a reference implementation for **composition**: eleven independently-usable application pages sharing one shell, demonstrating how dozens of small pieces combine into a coherent product UI without a framework, build system, backend, or JavaScript application.

## Design system

Minimal, light, editorial, data-dense: neutral-first palette (canvas `#ffffff`, near-black text `#111111`, soft gray secondary `#6b7280`), a single controlled accent **blue `#2563eb`** (used only for interactive emphasis, links, primary actions and chart data), semantic status colors used sparingly, **Inter** display/body + **JetBrains Mono** metrics/labels, 1px hairline borders, small radii (4-6px), restrained shadows. The system is expressed through CSS custom properties (primitive → semantic → template → component token model), so the entire UI — including a calm dark mode — is a variable swap. Components consume semantic helper classes (`.bg-canvas`, `.bg-surface`, `.text-primary`, `.text-secondary`, `.text-muted`, `.bd`, `.bd-subtle`, `.bd-strong`, `.accent`) so dark mode inverts cleanly without touching markup.



## File layout

```
atlas-analytics/
├── pages/            # 11 independently-usable application pages
├── assets/
│   ├── icons/logo.svg      # [A] mark
│   └── images/og-image.svg
├── preview.html            # Template showcase (overview + page index)
├── metadata.json
└── README.md
```

No `css/`, `js/` or `images/` directories beyond `assets/` — all visuals are inline SVG and Tailwind. Charts are hand-built SVG (sparklines, area, bar, funnel, heatmap, retention curves). Every page renders the same application chrome, inlined per page (copy-paste — no server includes. Navigation uses plain relative links (`<a href="analytics.html">`), so any single `pages/*.html` opens and navigates the whole product directly from the filesystem.

## Interactivity (vanilla JS, scoped IIFEs)

- **Theme toggle** — no-flash pre-paint detection + persisted toggle.
- **Sidebar drawer** (`<lg`) — hamburger toggle, `aria-expanded`/`aria-controls`, Esc + backdrop close.

- **Command palette** — `role="dialog"`/`aria-modal`, filter, Esc close, ⌘K open.


- **Settings tabs** — `role="tablist"`/`tab`/`tabpanel`; metric/range switching on the analytics page.



## How to adapt it

1. **Change the data**: replace the invented metrics, accounts, events and copy in the page markup. All data is fictional placeholders.
2. **Re-theme**: edit the custom property values in the `:root` (and `[data-theme="dark"]`) block that each page inlines — the blue accent and semantic tokens drive the whole UI.
3. **Add a page**: duplicate a `pages/*.html`, apply the shared Atlas shell (sticky topbar + sidebar), add a sidebar entry in that markup, and register it in `preview.html`'s page index.



## Do not

- Do not introduce a framework, a charting library, or a backend. All visuals are inline SVG and interactions are small IIFEs.
- Do not add neon, purple-on-black, glassmorphism, frosted cards, gradient text, glowing borders, decorative blobs or animated backgrounds — the restrained editorial data-dense language is deliberate.

- Do not break the `--ds-*` semantic token layer or hardcode hex values in components insteadof tokens.



## Quality bar

Semantic landmarks (`header`, `nav`, `main`, `footer`), skip link, a single `h1` per page, ARIA on the drawer, command palette and settings tabs, visible focus rings in the accent color, `prefers-reduced-motion` disables transitions. Validate with `python3 scripts/validate.py` after changes.

