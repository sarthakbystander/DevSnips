# Templates

A **template** is a complete page or multi-page site — an application starting point, not a snippet collection. Templates may contain multiple pages, shared assets, and their own project tooling.

## Common requirements (all technologies)

Every template **must** have a resource-level `AGENTS.md` at its root — enforced by `scripts/tooling/validators/validate.py` (existence + non-empty) and mirrored by the index generator. Templates also require `metadata.json` (`type: "template"`), and `preview.html` for Tailwind and React; Vanilla templates require `preview.html` **or** a non-empty `pages/`, plus `README.md`.

A template folder is a valid leaf whether it carries its own root `metadata.json` (single template) or contains sub-template leaf folders.

## Per-technology structure

### React templates

A complete Vite + TypeScript + Tailwind application. `library/React/Templates/spray-art-school/` is the reference:

- Build setup at root: `package.json` (react, react-router-dom, framer-motion, vite, tailwindcss, typescript; `dev`/`build`/`preview` scripts), `tsconfig.json`, `tailwind.config.ts`, `postcss.config.js`, `.gitignore`.
- App code under `src/`: `main.tsx`, `App.tsx`, `pages/`, `sections/`, `components/`, `data/`, `styles/globals.css`.
- Root `index.html` (Vite entry) + `preview.html` + `README.md` + `metadata.json` (`type: "template"`, `pages`, `style`) + `AGENTS.md`.

### Tailwind templates

Multi-page static sites. Two scopes:

- **Multi-page**: page code in `pages/` (e.g. `Tailwind/Templates/atlas-analytics/pages/`); shared navbar/footer either in `components/` (ai-saas-platform) or inlined per page.
- **Single-page**: a root `index.html` landing, or `pages/index.html` + root `preview.html` (e.g. `meridian`, which keeps a root `index.html` alongside `pages/`, `assets/`, `preview.html`, `metadata.json`, `README.md`, `AGENTS.md`).

`metadata.json` carries `pages` (count) and `style`. The registry `files` manifest lists root files plus one level of `pages/*`.

### Vanilla templates

All share one canonical layout — root holds `preview.html`, `metadata.json`, `README.md`, `AGENTS.md`; **all code lives in `pages/`**:

- **Modular** (agency, developer-portfolio, documentation-site, event-conference, job-board, product-launch): `pages/code.html` + `pages/style.css` (the `--ds-*` design system) + `pages/script.js`; `preview.html` is self-contained.
- **Single-page starter** (html5-boilerplate): `pages/index.html` only; root `preview.html` is a thin iframe wrapper.
- **Multipage with shared assets** (saas-dashboard): page files in `pages/`, shared `css/`, `js/`, `assets/` at root.

Vanilla template design conventions (the shared token spec, `library/Vanilla/Templates/design-tokens.md`): light-default with calm opt-in dark mode (no-flash pre-paint + persisted toggle), hairline 1px borders, small radii, one controlled blue accent, Inter + JetBrains Mono, IntersectionObserver scroll-reveal (reduced-motion safe), skip link, single `h1`, `:focus-visible`, native controls.

## What the CLI installs from a template

The registry `files` manifest for a template lists root files plus one level inside `pages/` (Tailwind, Vanilla) or `src/`, `components/`, `data/`, `sections/`, `styles/` (React). The CLI installs the source files from that manifest (`*.html`, `*.css`, `*.js`, `*.ts`, `*.tsx`, `*.jsx`), plus `README.md` and `AGENTS.md`, excluding `metadata.json` and `preview.html`. Files nested deeper than one level under those directories are not listed and not installed.

```bash
npx devsnips add Tailwind/Templates/meridian
```

Installed under `./devsnips/tailwind/templates/meridian/`.

## Using templates

- **As a starting point** — the template becomes the project base. Follow its resource-level `AGENTS.md`.
- **As a donor** — extract specific pages/sections/components into an existing project. Extract precisely (page + its direct dependencies), drop template-only routing/assets, re-verify each extracted piece.

Do not copy a full template for a one-section request — see [Resource selection](../agents/resource-selection.md).

## Conventional template dependencies

Tailwind CSS (via CDN), Google Fonts, Pico CSS (CDN — e.g. the Vanilla agency template), and for the React template: React, React Router, Framer Motion. Anything beyond these is out of convention.
