# Stratum — Fintech Ops Platform Template

A premium single-page website template built with **Tailwind CSS only** (via CDN), vanilla HTML, and scoped vanilla JS. No frameworks, no build step.

Brand used in the template: **Stratum** — a fictional vertical fintech operations platform unifying treasury, bill pay, and spend control for scale-stage finance teams.

## Design direction

**Neo-Brutalism + Editorial Modern** — a deliberate fusion, not a decoration mix.

- **Neo-Brutalist geometry:** 2px solid black borders, square radii, hard offset shadows (4 / 8 / 12px), press-down hover/active interactions, flat bright accents.
- **Editorial Modern rhythm:** Archivo display type (oversized, tight-tracked), JetBrains Mono for technical labels and metadata, numbered section eyebrows (`/ 01 — …`), generous whitespace, and a confident reading hierarchy.
- **Vertical fintech voice:** realistic money-motion content — cash position, approval routing, FX hedges, reconciliation rates, close-time reduction — instead of generic SaaS copy.

The combination stays coherent because both directions share the same disciplined grid, the same restrained accent palette, and the same monospace metadata voice.

## Design system

A single token set, applied consistently across every section.

| Token | Value | Use |
| --- | --- | --- |
| ink | `#0A0A0A` | foreground, borders, primary surfaces |
| paper | `#FBFAF7` | page background |
| cream | `#F4F1EA` | secondary surfaces / panels |
| lime | `#C6F24E` | primary accent / CTA highlight |
| ember | `#FF4FA3` | attention / approval emphasis |
| sky | `#00C2FF` | informational accent |
| forest | `#00A86B` | success / live status |

- **Type:** Archivo (display, 500–900) · Inter (body, 400–700) · JetBrains Mono (labels/metadata, 400–700).
- **Geometry:** 2px borders, square corners, offset shadows `4px`/`8px`/`12px`, `.press` translate interaction.
- **Spacing:** 4px-based rhythm, max container `1320px`, mobile-first padding `px-5 sm:px-8`.

## Structure

```text
stratum/
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

There are no external image assets. The treasury panel, approval graph, sparkline, logo, and OG image are all hand-built inline SVG / HTML so they stay crisp at every viewport and are editable directly in the markup. No photography dependencies.

## Sections

| # | Section | Purpose |
| --- | --- | --- |
| 01 | Navbar + mobile menu | Sticky nav, scoped JS menu, brand mark |
| 02 | Hero | Editorial split: copy + treasury command-surface visualization with live sparkline and floating approval/FX cards |
| 03 | Logos marquee | Trust strip of fictional customer brands |
| 04 | Three pillars | Staggered offset cards: Treasury / Bill pay / Spend control |
| 05 | Bento capabilities | Policy-as-code approval-routing graph + capability tiles |
| 06 | Workflow | Five-step capture → reconcile sequence with timings |
| 07 | Metrics band | Customer outcomes on a dark divided grid |
| 08 | Proof | Featured pull-quote + secondary testimonial cards |
| 09 | Pricing | Three-tier, cash-managed pricing with featured Growth plan |
| 10 | FAQ | Scoped single-open accordion (ARIA + keyboard) |
| 11 | CTA + Footer | Dark conversion panel + five-column footer with live status |

## Notable design decisions

- **Product visualization over decoration.** The hero's right column is a believable treasury panel (status header, balance, animated sparkline, account ledger, sync footer) flanked by two floating contextual mini-cards (approval needed / FX hedge) — not a generic gradient blob.
- **Policy-as-code graph.** The bento feature card visualizes an approval routing graph (trigger → policy → route → pass) with an evaluation-time label, reinforcing the "infrastructure, not a spreadsheet" message.
- **Staggered offsets.** Pillar and workflow cards use progressive `mt` offsets to break the predictable equal-grid rhythm without breaking alignment.
- **Cash-managed pricing.** Plans are priced by managed cash, not per seat — reinforcing the product positioning in the pricing architecture itself.
- **Section numbering.** Mono `/ 01 — …` eyebrows give editorial structure and aid scanning.

## Responsive behavior

Mobile-first, designed from **320px through 1920px+**:

- Below `lg`, the hero stacks vertically and the floating mini-cards hide (they're a desktop enhancement).
- The bento grid collapses from 4 columns → 2 → 1 with the large feature spanning full width.
- The workflow grid goes 5 → 2 → 1, keeping step order and timings legible.
- Metrics and pricing reflow to 2-column then 1-column with maintained dividers.
- The navbar collapses to a scoped mobile menu with safe open/close behavior.
- No accidental horizontal scrolling — `overflow-x-hidden` on the body and careful use of `max-w` containers.

## Accessibility

- Semantic landmarks (`header`, `main`, `section`, `footer`, `nav`, `article`, `figure`).
- Skip-to-content link.
- Correct heading hierarchy (single `h1`, descriptive `h2` per section).
- Accordion uses `aria-expanded`, `aria-controls`, `role="region"`, keyboard-operable buttons, single-open behavior.
- Mobile menu button toggles `aria-expanded` and swaps icons.
- Visible focus states via Tailwind defaults; interactive cards are focusable links.
- SVG sparkline and OG image carry `role="img"` and `aria-label`.
- `prefers-reduced-motion` disables marquee, sparkline draw, and all transitions.

## Interactions (scoped vanilla JS)

Only two small scoped scripts — no libraries:

1. **Mobile menu** — toggle open/close, swap icon, update `aria-expanded`, auto-close on link click.
2. **FAQ accordion** — single-open, CSS-grid `0fr → 1fr` panel animation, chevron rotation, ARIA state syncing.

CSS-only interactions: `.press` hover/active translate + shadow swell, `.link-underline` grow, `.live-dot` pulse, marquee, sparkline draw.

## Usage

Open `pages/index.html` directly in a browser, or serve the directory with any static server:

```bash
cd Tailwind/Templates/stratum
python3 -m http.server 8080
# visit http://localhost:8080/pages/index.html
```

`preview.html` is the template gallery shell — open it for an overview and a clickable index of every section. Tailwind is loaded from the CDN, so there is no build step and no `node_modules`.

## Customization

- **Rebrand:** swap the `Stratum` wordmark, the SVG logo (`assets/icons/logo.svg`), and the accent tokens in the `tailwind.config` `colors` block at the top of `pages/index.html`.
- **Re-theme:** the entire palette is defined once in the Tailwind config + `:root`; changing `lime`/`ember`/`sky` re-colors every component consistently.
- **Add a page:** duplicate `pages/index.html`, keep the shared `<head>` + navbar + footer, and swap the `<main>` content.
