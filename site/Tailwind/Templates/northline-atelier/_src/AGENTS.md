# AGENTS.md — Northline Atelier Architecture Studio

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A premium four-page architecture studio website built with Tailwind CSS, semantic HTML, inline SVG,and small scoped vanilla JS where interaction is useful. The visual direction is **Soft Modern**: warm paper tones, quiet charcoal type, thin rules, editorial grids, restrained rounded corners,and generous whitespace.



## Design system

Soft warm background `#F5F2EC`, ink `#20201D`, muted text `#77746C`, fine borders instead of heavy cards, serif display headlines paired with a clean sans-serif body, large editorial whitespace and asymmetric grids, a restrained olive accent used for active states and small highlights, subtle image-like architectural drawings made with inline SVG.



## File layout

```
northline-atelier/
├── pages/
│   ├── index.html        # Home: studio introduction, featured project, selected work, approach, CTA
│   ├── projects.html     # Filterable project archive with categories
│   ├── studio.html       # Practice story, principles, capabilities, team
│   └── contact.html      # Enquiry form, process, contact details, studio hours
├── preview.html          # Template gallery shell
├── metadata.json
└── README.md
```

No `assets/`, `css/`, `js/`, or `images/` directories — visual details use Tailwind utilities, CSS shapes, gradients,and inline SVG.



## How to adapt it

1. **Swap the studio**: replace the Northline brand, projects, team profiles, principles and copy across the pages.
2. **Re-theme**: edit the color values in each page's inline `tailwind.config` (warm paper/ink/olive ramp), keeping one restrained accent.



3. **Add a page**: duplicate a `pages/*.html`, keep the shared navbar + footer,and swap the `<main>` content. Register it in `preview.html`'s page index.



## Do not

- Do not introduce a framework, a build step, or heavy card styling—the fine-border editorial grid is the design language..
- Do not replace the restrained olive accent with a saturated or neon color.



## Quality bar

Semantic landmarks, visible keyboard focus, labelled form controls, descriptive SVG titles, reduced-motion handling, mobile-first responsiveness from 320px through 1920px+. Validate with `python3 scripts/validate.py` after changes.


