# Vesper — Attack-Surface Management Platform Template

A premium single-page website template built with **Tailwind CSS only** (via CDN), vanilla HTML, and scoped vanilla JS. No frameworks, no build step.

Brand used in the template: **Vesper** — a fictional external attack-surface management (EASM) platform for security teams. It continuously discovers exposed assets, prioritizes the exposures that actually matter, and verifies remediation before attackers find them.

## Design direction

**Glassmorphism + Cyber Minimal** — a deliberate fusion, not an effect mix.

- **Glassmorphism surfaces:** translucent frosted panels (`backdrop-blur` over low-opacity white) layered over an atmospheric backdrop, so depth reads through surface hierarchy rather than offset shadows.
- **Cyber Minimal discipline:** near-black space canvas, 1px white hairline rules, a single restrained cyan accent, technical monospace metadata, severity semantics (amber/red/ok used for status only), and engineering-grade content density.
- **Security voice:** realistic EASM content — asset inventory, severity (critical/high/medium/low), EPSS + KEV, reachability, MTTR, subdomain takeover, signed audit trail — instead of generic SaaS copy.

The combination stays coherent because both directions share the same restrained accent system, the same hairline geometry, and the same monospace metadata voice. The atmospheric mesh is low-opacity and slow — a backdrop, not the focal "gradient blob" anti-pattern.

This template deliberately differs from the repo's existing light templates: where `stratum` uses thick 2px borders + offset shadows and `meridian` uses 1px hairlines + tonal lift on a light canvas, Vesper uses translucent frosted glass over a dark atmospheric mesh with a single cyan glow.

## Design system

A single token set, applied consistently across every section.

| Token | Value | Use |
| --- | --- | --- |
| canvas | `#06070D` | page background (space black) |
| ink | `#E6E8EC` | foreground |
| surface | `#0C0E17` | panel/card base |
| muted | `#8A90A2` | secondary text |
| cyan | `#6EE7FF` | primary accent / signal highlight |
| amber | `#FBBF24` | high severity (status only) |
| red | `#F43F5E` | critical severity (status only) |
| ok | `#34D399` | resolved / healthy (status only) |

- **Type:** Sora (display, 400–800) · Inter (body, 400–700) · JetBrains Mono (labels/metadata, 400–700).
- **Geometry:** `rounded-2xl` glass surfaces, 1px white/10 hairlines, restrained glow (cyan drop-shadow on active states only), no offset hard shadows.
- **Spacing:** consistent 4px-based rhythm, max container `1240px`, mobile-first padding `px-5 sm:px-8`.

## Structure

```text
vesper/
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

There are no external image assets. The attack-surface console, topology graph, radar, sparkline, logo, and OG image are all hand-built inline SVG / HTML so they stay crisp at every viewport and are editable directly in the markup. No photography dependencies.

## Sections

| # | Section | Purpose |
| --- | --- | --- |
| 01 | Navbar + mobile menu | Sticky glass nav, scoped JS menu, brand mark, mono utility labels |
| 02 | Hero | Editorial-cyber split: copy + attack-surface command-console visualization with live radar, sparkline, and floating critical-exposure/new-asset mini-cards |
| 03 | Logos strip | Trust marquee of fictional security-first customer brands |
| 04 | Three pillars | Frosted-glass panels: Discover / Prioritize / Remediate |
| 05 | Topology graph | Signature asset-reachability diagram (internet → edge → services → data) with exposed path in cyan |
| 06 | Lifecycle | Five-step EASM workflow with timings + signed-state rail |
| 07 | Outcomes band | Customer outcomes on a glass grid (MTTR / exposures / shadow assets / noise) |
| 08 | Proof | Featured pull-quote + secondary security-leader testimonials |
| 09 | Pricing | Three-tier, per-asset pricing with featured Team plan |
| 10 | FAQ | Scoped single-open accordion (ARIA + keyboard) |
| 11 | CTA + Footer | Glass conversion panel + 3-step onboarding + six-column footer with live status |

## Notable design decisions

- **Product visualization over decoration.** The hero's right column is a believable attack-surface console (status title bar, severity bar, exposure rows, surface radar, exposures-per-day sparkline) flanked by two floating contextual mini-cards (critical exposure + new asset discovered) — not a generic gradient blob.
- **Directed reachability graph.** The signature visual is an engineering diagram of the asset topology (internet → load balancer → API gateway → K8s API / Postgres / S3), with the exposed attacker path animated in cyan and the critical node ringed in red — reinforcing the "see the path an attacker would take" message.
- **Severity semantics.** Cyan is the single primary accent; amber, red, and green appear only as severity/status indicators — keeping the cyber-minimal restraint consistent while letting security signals read instantly.
- **Per-asset pricing.** Plans are priced by attack-surface size, not per seat — reinforcing the product positioning in the pricing architecture itself.
- **Section numbering.** Mono `/ 01 — …` eyebrows give editorial-cyber structure and aid scanning.
- **Atmospheric, not decorative.** The mesh backdrop is low-opacity and slow-drifting behind a vignette + cyber-grid, anchoring glass panels without becoming noise.

## Responsive behavior

Mobile-first, designed from **320px through 1920px+**:

- Below `lg`, the hero stacks vertically and the floating mini-cards hide (they're a desktop enhancement).
- The topology graph is a responsive inline SVG that scales to its container; the legend reflows on narrow widths.
- The lifecycle grid goes 5 → 2 → 1, keeping step order and timings legible.
- Outcomes metrics reflow from 4 → 2 with maintained dividers.
- Pricing reflows to 1-column; the featured plan keeps its "Most popular" tag and glow.
- The navbar collapses to a scoped mobile menu with safe open/close behavior.
- No accidental horizontal scrolling — `overflow-x-hidden` on the body and careful use of `max-w` containers.

## Accessibility

- Semantic landmarks (`header`, `main`, `section`, `footer`, `nav`, `figure`, `article`, `ol`).
- Skip-to-content link.
- Correct heading hierarchy (single `h1`, descriptive `h2` per section, `h3` for FAQ items).
- Accordion uses `aria-expanded`, `aria-controls`, `role="region"`, keyboard-operable buttons, single-open behavior.
- Mobile menu button toggles `aria-expanded` and swaps icons.
- Visible focus states via a cyan `:focus-visible` ring; interactive cards are links/buttons.
- SVG diagrams carry `role="img"` and descriptive `aria-label`s; decorative SVGs are `aria-hidden`.
- `prefers-reduced-motion` disables mesh drift, radar sweep, marquee, sparkline draw, edge flow, and all transitions.

## Interactions (scoped vanilla JS)

Only two small scoped scripts — no libraries:

1. **Mobile menu** — toggle open/close, swap icon, update `aria-expanded`, auto-close on link click.
2. **FAQ accordion** — single-open, CSS-grid `0fr → 1fr` panel animation, chevron rotation, ARIA state syncing.

CSS-only interactions: glass card hover (border + soft cyan glow + tonal lift), link-underline grow, live-status dot pulse, animated topology edges, radar sweep, sparkline draw, mesh drift, logos marquee.

## Usage

Open `pages/index.html` directly in a browser, or serve the directory with any static server:

```bash
cd Tailwind/Templates/vesper
python3 -m http.server 8080
# visit http://localhost:8080/pages/index.html
```

`preview.html` is the template gallery shell — open it for an overview and a clickable index of every section. Tailwind is loaded from the CDN, so there is no build step and no `node_modules`.

## Customization

- **Rebrand:** swap the `Vesper` wordmark, the SVG logo (`assets/icons/logo.svg`), and the accent tokens in the `tailwind.config` `colors` block at the top of `pages/index.html`.
- **Re-theme:** the entire palette is defined once in the Tailwind config + `<style>`; changing `cyan` re-colors every accent consistently, while `amber`/`red`/`ok` only touch severity indicators.
- **Add a page:** duplicate `pages/index.html`, keep the shared `<head>` + navbar + footer, and swap the `<main>` content.
