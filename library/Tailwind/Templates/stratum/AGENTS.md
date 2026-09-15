# AGENTS.md — Stratum Fintech Ops Platform

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium single-page website template built with **Tailwind CSS only**(via CDN, vanilla HTML,and scoped vanilla JS. No frameworks, no build step. Brand: **Stratum** — a fictional vertical fintech operations platform unifying treasury, bill pay,and spend control for scale-stage finance teams.



## Design direction

**Neo-Brutalism + Editorial Modern** — a deliberate fusion: Neo-Brutalist geometry(2px solid black borders, square radii, hard offset shadows(4/8/12px), press-down hover/active interactions, flat bright accents) + Editorial Modern rhythm(Archivo display type, JetBrains Mono labels/metadata, numbered section eyebrows `/ 01 — …`, generous whitespace,and a confident reading hierarchy. Tokens: ink `#0A0A0A`, paper `#FBFAF7`, cream `#F4F1EA`, lime `#C6F24E`(primary accent), ember `#FF4FA3`, sky `#00C2FF`, forest `#00A86B`(success/live status.



## File layout

```
stratum/
├── pages/
│   └── index.html          # Full landing page (11 composed sections)
├── assets/
│   ├── icons/logo.svg
│   └── images/og-image.svg
├── preview.html            # Template gallery shell
├── metadata.json
└── README.md
```

No external image assets — the treasury panel, approval graph, sparkline, logo,and OG image are all hand-built inline SVG/HTML,and editable directly in the markup.



## Sections

Navbar + mobile menu, Hero(editorial split with treasury command-surface visualization + floating approval/FX mini-cards), Logos marquee, Three pillars(staggered offset cards: Treasury/Bill pay/Spend control, Bento capabilities(grid with policy-as-code approval-routing graph), Workflow(five-step capture→reconcile with timings), Metrics band(dark divided grid), Proof(testimonials, Pricing(three-tier cash-managed with featured Growth plan), FAQ(scoped single-open accordion,and CTA + Footer(dark conversion panel + five-column footer with live status.

## Interactivity (scoped vanilla JS)

Only two small scoped scripts — no libraries: (1) mobile menu toggle(aria-expanded, icon swap, auto-close on link click), (2) FAQ accordion(single-open, CSS-grid `0fr→1fr` animation, chevron rotation, ARIA state sync. CSS-only: `.press` hover, `.link-underline` grow, `.live-dot` pulse, marquee, sparkline draw.



## How to adapt it

1. **Rebrand**: swap the Stratum wordmark, the SVG logo (`assets/icons/logo.svg`),and the accent tokens in the `tailwind.config` `colors` block at the top of `pages/index.html`.


2. **Re-theme**: the entire palette is defined once in the Tailwind config + `:root`;changing `lime`/`ember`/`sky` re-colors every component consistently.



3. **Add a page**: duplicate `pages/index.html`, keep the shared `<head>` + navbar + footer,and swap the `<main>` content.



## Do not

- Do not introduce a framework, a build step, or photography dependencies—the visuals are inline SVG by design..
- Do not soften the Neo-Brutalist geometry(offset shadows, 2px borders, press interactions) — it is the design language..



## Quality bar

Semantic landmarks, skip link, single `h1`, descriptive `h2` hierarchy, accordion ARIA(`aria-expanded`/`aria-controls`/`role="region"`, keyboard-operable, single-open, mobile menu `aria-expanded`, visible focus states, SVG sparkline and OG image `role="img"` + `aria-label`, `prefers-reduced-motion` disables marquee/sparkline/transitions. Validate with `python3 scripts/validate.py` after changes.

