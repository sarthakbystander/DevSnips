# Meridian — Incident Command Platform Template

A premium single-page website template built with **Tailwind CSS only** (via CDN), vanilla HTML, and scoped vanilla JS. No frameworks, no build step.

Brand used in the template: **Meridian** — a fictional incident command platform for on-call engineering teams. It correlates alerts, routes them to the right owner, coordinates response, and turns every incident into a structured postmortem.

## Design direction

**Neo-Industrial + Swiss Minimal** — a deliberate fusion, not a decoration mix.

- **Neo-Industrial language:** utility labels and metadata set in monospace, structured grids, dense information panels, engineering vocabulary, directed routing diagrams, status indicators, and a restrained blueprint graph-paper surface.
- **Swiss Minimal discipline:** 1px hairline rules, square corners, a single restrained accent, strict alignment, precise spacing rhythm, and typography-driven hierarchy with generous, intentional whitespace.
- **On-call voice:** realistic incident-ops content — MTTA, MTTR, noise suppression, severity, escalation, runbooks, correlation, signed audit trail — instead of generic SaaS copy.

The combination stays coherent because both directions share the same hairline geometry, the same single-accent restraint, and the same monospace metadata voice.

This template deliberately differs from the repo's existing `stratum` template: where Stratum uses thick 2px borders and offset hard shadows (Neo-Brutalism), Meridian uses 1px hairlines and tonal elevation; where Stratum uses Archivo + lime, Meridian uses Space Grotesk + amber on a cool canvas.

## Design system

A single token set, applied consistently across every section.

| Token | Value | Use |
| --- | --- | --- |
| canvas | `#F5F6F8` | page background (cool engineering paper) |
| ink | `#0B0D10` | foreground, borders, dark surfaces |
| surface | `#FFFFFF` | panels / cards |
| panel | `#EDEFF3` | secondary surface |
| muted | `#5C6470` | secondary text |
| amber | `#E8A33C` | primary accent / signal highlight |
| ok | `#16A34A` | healthy status (dots/badges only) |
| alert | `#DC2626` | incident / degraded status (dots/badges only) |

- **Type:** Space Grotesk (display, 400–700) · Inter (body, 400–700) · JetBrains Mono (labels/metadata, 400–700).
- **Geometry:** 1px hairline borders, square corners, restrained tonal elevation (no offset shadows), a single amber accent used sparingly.
- **Spacing:** consistent 4px-based rhythm, max container `1280px`, mobile-first padding `px-5 sm:px-8`.

## Structure

```text
meridian/
├── pages/
│   └── index.html          # Full landing page (11 composed sections)
├── assets/
│   ├── icons/
│   │   └── logo.svg        # Logo mark (favicon)
│   └── images/
│       └── og-image.svg    # Open Graph / preview graphic
├── preview.html            # Template gallery shell (overview + sections index)
├── metadata.json
└── README.md
```

There are no external image assets. The incident console, routing graph, sparkline, logo, and OG image are all hand-built inline SVG / HTML so they stay crisp at every viewport and are editable directly in the markup. No photography dependencies.

## Sections

| # | Section | Purpose |
| --- | --- | --- |
| 01 | Navbar + mobile menu | Sticky nav, scoped JS menu, brand mark, mono utility labels |
| 02 | Hero | Editorial-technical split: copy + incident command-surface visualization with live sparkline and floating signal/escalation cards |
| 03 | Logos strip | Trust marquee of fictional engineering customer brands |
| 04 | Three pillars | Hairline-divided panels: Route / Respond / Learn |
| 05 | Routing graph | Signature directed alert-routing diagram (signal → correlate → rule → page) with ack-fallback |
| 06 | Lifecycle | Five-step incident workflow with timings + signed-state rail |
| 07 | Outcomes band | Customer outcomes on a dark divided grid |
| 08 | Proof | Featured pull-quote + secondary engineer testimonials |
| 09 | Pricing | Three-tier, per-on-call-team pricing with featured Squad plan |
| 10 | FAQ | Scoped single-open accordion (ARIA + keyboard) |
| 11 | CTA + Footer | Dark corner-tick conversion panel + five-column footer with live status |

## Notable design decisions

- **Product visualization over decoration.** The hero's right column is a believable incident console (status title bar, latency metric, animated sparkline, responders, timeline, runbook footer) flanked by two floating contextual mini-cards (correlated signal + stepped escalation) — not a generic gradient blob.
- **Directed routing graph.** The signature visual is an engineering diagram of the alert-routing pipeline (three signals → correlate node → routing rule → page owner, with a dashed ack-fallback branch) — reinforcing the "signal to the right page" message with animated flow edges.
- **Hairline discipline.** Cards live inside 1px-rule containers and use tonal/background shifts on hover rather than offset shadows — keeping the Swiss Minimal restraint consistent across every surface.
- **Per-on-call-team pricing.** Plans are priced by rotation, not per seat — reinforcing the product positioning ("on-call is a team sport") in the pricing architecture itself.
- **Section numbering.** Mono `/ 01 — …` eyebrows give editorial-industrial structure and aid scanning.
- **Blueprint surfaces.** Subtle graph-paper grid backgrounds anchor the engineering aesthetic without becoming noise.

## Responsive behavior

Mobile-first, designed from **320px through 1920px+**:

- Below `lg`, the hero stacks vertically and the floating mini-cards hide (they're a desktop enhancement).
- The routing graph is a responsive inline SVG that scales to its container; the surrounding metric dl and the legend reflow on narrow widths.
- The lifecycle grid goes 5 → 2 → 1, keeping step order and timings legible.
- Outcomes metrics reflow from 2×2 to a stacked single column with maintained dividers.
- Pricing reflows to 1-column with maintained hairline dividers; the featured plan keeps its "Most popular" tag.
- The navbar collapses to a scoped mobile menu with safe open/close behavior.
- No accidental horizontal scrolling — `overflow-x-hidden` on the body and careful use of `max-w` containers.

## Accessibility

- Semantic landmarks (`header`, `main`, `section`, `footer`, `nav`, `figure`, `article`, `ol`).
- Skip-to-content link.
- Correct heading hierarchy (single `h1`, descriptive `h2` per section, `h3` for FAQ items).
- Accordion uses `aria-expanded`, `aria-controls`, `role="region"`, `aria-labelledby`, keyboard-operable buttons, single-open behavior.
- Mobile menu button toggles `aria-expanded` and swaps icons.
- Visible focus states via Tailwind defaults; interactive cards are links/buttons.
- SVG diagrams carry `role="img"` and descriptive `aria-label`s; decorative SVGs are `aria-hidden`.
- `prefers-reduced-motion` disables marquee, sparkline draw, edge flow, and all transitions.

## Interactions (scoped vanilla JS)

Only two small scoped scripts — no libraries:

1. **Mobile menu** — toggle open/close, swap icon, update `aria-expanded`, auto-close on link click.
2. **FAQ accordion** — single-open, CSS-grid `0fr → 1fr` panel animation, chevron rotation, ARIA state syncing.

CSS-only interactions: hairline card hover (border + tonal lift), link-underline grow, live-status dot pulse, animated routing edges, sparkline draw, logos marquee.

## Usage

Open `pages/index.html` directly in a browser, or serve the directory with any static server:

```bash
cd Tailwind/Templates/meridian
python3 -m http.server 8080
# visit http://localhost:8080/pages/index.html
```

`preview.html` is the template gallery shell — open it for an overview and a clickable index of every section. Tailwind is loaded from the CDN, so there is no build step and no `node_modules`.

## Customization

- **Rebrand:** swap the `Meridian` wordmark, the SVG logo (`assets/icons/logo.svg`), and the accent tokens in the `tailwind.config` `colors` block at the top of `pages/index.html`.
- **Re-theme:** the entire palette is defined once in the Tailwind config + `<style>`; changing `amber` re-colors every accent consistently, while `ok`/`alert` only touch status indicators.
- **Add a page:** duplicate `pages/index.html`, keep the shared `<head>` + navbar + footer, and swap the `<main>` content.
