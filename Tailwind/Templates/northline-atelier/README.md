# Northline Atelier — Architecture Studio Template

A premium four-page architecture studio website built with Tailwind CSS, semantic HTML, inline SVG, and small scoped vanilla JS where interaction is useful. The visual direction is **Soft Modern**: warm paper tones, quiet charcoal type, thin rules, editorial grids, restrained rounded corners, and generous whitespace.

## Structure

```text
northline-atelier/
├── pages/
│   ├── index.html       # Home, featured project, practice overview, selected work
│   ├── projects.html    # Project archive with category filters
│   ├── studio.html      # Studio profile, principles, team, capabilities
│   └── contact.html     # Enquiry form, studio details, process
├── metadata.json
└── README.md
```

There are no `assets/`, `css/`, `js/`, or `images/` directories. Visual details use Tailwind utilities, CSS shapes, gradients, and inline SVG.

## Design language

- Soft warm background: `#F5F2EC`
- Ink: `#20201D`; muted text: `#77746C`
- Fine borders instead of heavy cards
- Serif display headlines paired with a clean sans-serif body
- Large editorial whitespace and asymmetric grids
- Restrained olive accent used for active states and small highlights
- Subtle image-like architectural drawings made with inline SVG

## Pages

| Page | Purpose |
| --- | --- |
| Home | Studio introduction, featured project, selected work, approach and CTA |
| Projects | Filterable project archive with categories and project metadata |
| Studio | Practice story, principles, capabilities and team |
| Contact | Project enquiry form, process, contact details and studio hours |

## Responsive & accessibility

The layout is mobile-first and designed for 320px through 1920px+. Grids intentionally change composition at breakpoints rather than simply stacking. Navigation becomes a compact menu on smaller screens, forms remain touch-friendly, and long project titles wrap without overflow. Pages use semantic landmarks, visible keyboard focus, labelled form controls, descriptive SVG titles, and reduced-motion handling.

## Usage

Open any file in `pages/` directly or serve the template with a static server. Tailwind is loaded through the CDN, so no build step is required.
