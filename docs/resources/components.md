# Components

A **component** is one focused, reusable UI pattern: a button, an accordion, a dialog, a table, a tooltip. Components are the smallest resource type. They are self-describing, independently installed, and individually addressable.

## Component families per technology

Component families are the Capitalized folders directly under `library/<Tech>/Components/` (e.g. `Buttons`, `Accordions`, `Cards`, `Dialogs`, `Tables`, `Navigation`). Family names differ across technologies because each technology's collection evolved independently; the registry is the inventory of record.

Some technologies use grouping levels:

- **Tailwind Buttons** uses 3-level layout: `Components/Buttons/<group>/<sub-variant>/`, e.g. `Tailwind/Components/Buttons/basic-button/primary/`. The group folder carries `metadata.json` + `README.md` but is not itself a resource (it has leaf children).
- **Vanilla Components/Navigation** retains legacy sub-families (e.g. breadcrumb variants under `Navigation/Breadcrumb/`).

## File contract by technology

| Technology | Required files | Notes |
|---|---|---|
| React | `code.tsx`, `code.jsx`, `preview.html`, `metadata.json`, `README.md` | TSX-first; `code.jsx` is the JavaScript parity build (missing one is a **warning** in `deep_check.py`, not an error). |
| Tailwind | `code.html`, `preview.html`, `metadata.json`, `README.md` | `code.html` is a snippet (no DOCTYPE/CDN); `preview.html` is a full page. |
| Vanilla | `metadata.json` (only machine-enforced requirement) | Universal convention: `code.html` (self-contained) + `README.md`. No `preview.html` at component level. |

Details and examples: [Resource structure](resource-structure.md).

## Component conventions

- **Self-containment.** A component must render correctly when copied into a suitable page:
  - Vanilla: inline `<style>` + inline `<script>` inside the snippet; `--ds-*` tokens used with fallbacks.
  - Tailwind: markup + scoped vanilla JS only; any interactivity works standalone.
  - React: one primary export (compound families export multiple named primitives); all state internal or prop-driven.
- **Accessibility** is part of the quality bar: native semantics first, keyboard operability, visible focus, ARIA only where native HTML is insufficient, reduced-motion guards.
- **No preview-only code in production files.** `preview.html` exists to be opened in a browser; its framing (page shell, demo data, CDN setup) stays out of the implementation file.
- **Tokens.** Vanilla components embed a Swiss `:root{--ds-*}` block with dark-mode override so they work standalone *and* re-theme when `library/Vanilla/Components/tokens.css` is included. React components consume the React token spec via Tailwind arbitrary values.

## How components are indexed

Each component variant is a variant record inside its family in `snippets-index.json`:

- family: `tech` (`React` / `Tailwind CSS` / `Vanilla HTML/CSS/JS`), `category: "Components"`, `type: "component"`, `path` (e.g. `React/Components/Buttons/`), `variantsCount`, family-level `description` and `tags`.
- variant: `name`, `path` (e.g. `React/Components/Buttons/solid-button/`), `type: "component"`, `description`, `tags[]`, `features[]`, `styles[]` (optional), `files[]` manifest.

The specialized component index (`agents/resources/indexes/components-index.json`) additionally carries `id` (the CLI-resolvable path) and `install` (the exact `npx devsnips add <id>` command) per variant.

## Installing

```bash
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Vanilla/Components/Buttons/split-button
```

Installed under `./devsnips/<tech>/components/<family>/<variant>/` in the user's project. See [Installation](../agents/installation.md).
