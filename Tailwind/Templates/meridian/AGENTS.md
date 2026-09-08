# AGENTS.md — Meridian Incident Command Platform

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium single-page website template built with **Tailwind CSS only**(via CDN, vanilla HTML,and scoped vanilla JS. No frameworks, no build step. Brand: **Meridian** — a fictional incident command platform for on-call engineering teams(it correlates alerts, routes them to the right owner, coordinates response,and turns every incident into a structured postmortem.

.



## Design direction

**Neo-Industrial + Swiss Minimal** — a deliberate fusion: Neo-Industrial utility labels and metadata in monospace, structured grids, dense information panels, directed routing diagrams, status indicators,and a restrained blueprint graph-paper surface; Swiss Minimal discipline of 1px hairline rules, square corners, a single restrained amber accent `#E8A33C`, strict alignment, and typography-driven hierarchy with generous whitespace. Type: Space Grotesk(display) · Inter(body) · JetBrains Mono(labels/metadata). canvas `#F5F6F8`, ink `#0B0D10`, surface `#FFFFFF`, panel `#EDEFF3`, muted `#5C6470`; ok `#16A34A` / alert `#DC2626` are status-only.



## File layout

```
meridian/
├── pages/
│   └── index.html          # Full landing page (11 composed sections)
├── assets/
│   ├── icons/logo.svg
│   └── images/og-image.svg
├── preview.html            # Template gallery shell
├── metadata.json
└── README.md
```

No external image assets — the incident console, routing graph, sparkline, logo,and OG image are all hand-built inline SVG/HTML,and editable directly in the markup.



## Sections

Navbar + mobile menu, Hero(editorial-technical split with command-surface visualization + floating signal/escalation cards), Logos strip, Three pillars(Route/Respond/Learn), Routing graph(directed alert-routing diagram with ack-fallback), Lifecycle(five-step incident workflow with timings+ signed-state rail), Outcomes band(dark divided grid), Proof(testimonials), Pricing(three-tier per-on-call-team), FAQ(scoped single-open accordion,and CTA + Footer(dark corner-tick panel + five-column footer with live status.



## Interactivity (scoped vanilla JS)

Only two small scoped scripts — no libraries: (1) mobile menu toggle(aria-expanded, icon swap, auto-close on link click), (2) FAQ accordion(single-open, CSS-grid `0fr→1fr` animation, chevron rotation, ARIA state sync. CSS-only: hairline card hover, link-underline grow, live-status dot pulse, animated routing edges, sparkline draw, logos marquee.



## How to adapt it

1. **Rebrand**: swap the Meridian wordmark, the SVG logo (`assets/icons/logo.svg`),and the accent tokens in the `tailwind.config` `colors` block at the top of `pages/index.html`.
2. **Re-theme**: the entire palette is defined once in the Tailwind config + `<style>`;changing `amber` re-colors every accent consistently,while `ok`/`alert` only touch status indicators.

3. **Add a page**: duplicate `pages/index.html`, keep the shared `<head>` + navbar + footer,and swap the `<main>` content.



## Do not

- Do not introduce a framework, a build step, or photography dependencies—the visuals are inline SVG by design..
- Do not replace the hairline + tonal-elevation system with offset shadows or thick borders(that is the `stratum` language).
- Do not break the ARIA contract on the FAQ accordion or mobile menu.



## Quality bar

Semantic landmarks, skip link, single `h1`, descriptive `h2`/`h3` hierarchy, accordion ARIA(`aria-expanded`/`aria-controls`/`role="region"`/`aria-labelledby`, keyboard-operable, single-open, mobile menu `aria-expanded`, visible focus states, SVG diagrams `role="img"` + `aria-label`, decorative SVGs `aria-hidden`, `prefers-reduced-motion` disables marquee/sparkline/edge flow/transitions. Validate with `python3 scripts/validate.py` after changes.


