# AGENTS.md — Vesper Attack-Surface Management Platform

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium single-page website template built with **Tailwind CSS only**(via CDN, vanilla HTML,and scoped vanilla JS. No frameworks, no build step. Brand: **Vesper** — a fictional external attack-surface management(EASM) platform for security teams(it continuously discovers exposed assets, prioritizes the exposures that matter,and verifies remediation before attackers find them.



## Design direction

**Glassmorphism + Cyber Minimal** — a deliberate fusion: translucent frosted panels(`backdrop-blur` over low-opacity white) layered over an atmospheric backdrop(fuchsia/indigo/cyan mesh with slow drift + fine cyber-grid + vignette), plus Cyber Minimal discipline(near-black space canvas `#06070D`, 1px white hairline rules, a single restrained cyan accent `#6EE7FF`, technical monospace metadata, severity semantics(amber `#FBBF24` high / red `#F43F5E` critical / ok `#34D399` resolved — status only, and engineering-grade content density. Type: Sora(display) · Inter(body) · JetBrains Mono(labels/metadata. Geometry: `rounded-2xl` glass, 1px white/10 hairlines, restrained cyan glow(active states only, no offset hard shadows.



## File layout

```
vesper/
├── pages/
│   └── index.html          # Full landing page (11 composed sections)
├── assets/
│   ├── icons/logo.svg
│   └── images/og-image.svg
├── preview.html            # Template gallery shell
├── metadata.json
└── README.md
```

No external image assets — the attack-surface console, topology graph, radar, sparkline, logo,and OG image are all hand-built inline SVG/HTML,and editable directly in the markup.



## Sections

Navbar + mobile menu, Hero(editorial-cyber split with attack-surface command-console visualization + floating critical-exposure/new-asset mini-cards, Logos strip, Three pillars(frosted-glass: Discover/Prioritize/Remediate, Topology graph(signature asset-reachability diagram with exposed path in cyan,and critical node in red, Lifecycle(five-step EASM workflow with timings+ signed-state rail, Outcomes band(glass grid, Proof(security-leader testimonials, Pricing(three-tier per-asset with featured Team plan, FAQ(scoped single-open accordion,and CTA + Footer(glass conversion panel + 3-step onboarding + six-column footer with live status.



## Interactivity (scoped vanilla JS)

Only two small scoped scripts — no libraries: mobile menu toggle(aria-expanded, icon swap, auto-close on link click, and FAQ accordion(single-open, CSS-grid `0fr→1fr` animation, chevron rotation, ARIA state sync. CSS-only: glass card hover(border + soft cyan glow + tonal lift, link-underline grow, live-status dot pulse, animated topology edges, radar sweep, sparkline draw, mesh drift, logos marquee.



## How to adapt it

1. **Rebrand**: swap the Vesper wordmark, the SVG logo (`assets/icons/logo.svg`),and the accent tokens in the `tailwind.config` `colors` block at the top of `pages/index.html`.


2. **Re-theme**: changing `cyan` re-colors every accent consistently,while `amber`/`red`/`ok` only touch severity indicators.

3. **Add a page**: duplicate `pages/index.html`, keep the shared `<head>` + navbar + footer,and swap the `<main>` content.



## Do not

- Do not introduce a framework, a build step, or photography dependencies—the visuals are inline SVG by design..
- Do not replace the glassmorphism + hairline system with offset hard shadows or thick borders(that is a different template language)ể


- Do not use amber/red/green except as severity/status indicators;cyan is the single primary accent.



## Quality bar

Semantic landmarks, skip link, single `h1`, descriptive `h2`/`h3` hierarchy, accordion ARIA(`aria-expanded`/`aria-controls`/`role="region"`, keyboard-operable, single-open, mobile menu `aria-expanded`, visible cyan `:focus-visible` ring, SVG diagrams `role="img"` + `aria-label`, decorative SVGs `aria-hidden`, `prefers-reduced-motion` disables mesh drift/radar sweep/marquee/sparkline/edge flow/transitions. Validate with `python3 scripts/validate.py` after changes.

