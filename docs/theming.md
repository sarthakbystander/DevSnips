# Theming & design tokens

DevSnips resources are **token-driven**: they read their visual values from CSS custom properties (`--ds-*`) so a whole project re-themes by editing one file. This page is the end-user contract. The canonical per-tech token references live inside `library/` (listed below); this page explains the model.

## The opt-in model

Every migrated Vanilla component references tokens **with the original value as a fallback**:

```css
border-radius: var(--ds-radius-md, 8px);
```

That single pattern gives you three guarantees:

- **Standalone** — a component is copy-paste ready and renders correctly even without `tokens.css` loaded (the fallback applies).
- **Cohesive** — include `tokens.css` once and every component speaks the same visual language and upgrades together. Re-theme by editing one file.
- **Safe migration** — the fallback preserves the original look, so migrating hundreds of components cannot visually break them.

`tokens.css` lives at `library/Vanilla/Components/tokens.css` — a single `:root` block plus a `prefers-color-scheme: dark` override.

## How to theme a project

```css
/* your app, after tokens.css */
:root {
  --ds-bg: #0b0f14;            /* page background */
  --ds-surface: #0f1620;       /* card / panel */
  --ds-foreground: #e6edf3;    /* primary text */
  --ds-border: #1f2a37;        /* hairline rule */
}
```

Every component that uses `--ds-bg`, `--ds-surface`, `--ds-foreground`, `--ds-border`, etc. picks the new values up immediately — with no per-component edits.

## The token contract

The `library/Vanilla/Components/DESIGN_TOKENS.md` reference documents the full token set (the "Swiss" neo-minimal system: neutral surfaces, hairline borders, restrained elevation, a single accent, system typography, WCAG AA contrast, aligned to Tailwind's scale). Key surface/text tokens:

| Token | Light | Dark | Use |
|---|---|---|---|
| `--ds-bg` | `#ffffff` | `#0a0a0a` | page background |
| `--ds-surface` | `#ffffff` | `#111111` | card / panel |
| `--ds-surface-2` | `#f7f7f7` | `#171717` | raised panel |
| `--ds-surface-3` | `#ededed` | `#1f1f1f` | inset / muted panel |
| `--ds-foreground` | `#0a0a0a` | `#fafafa` | primary text |
| `--ds-muted` | `#525252` | `#a3a3a3` | secondary text |
| `--ds-subtle` | `#a3a3a3` | `#737373` | tertiary / placeholder |
| `--ds-border` | `#e5e5e5` | `#262626` | hairline 1px rule |

Read the authoritative list from `library/Vanilla/Components/DESIGN_TOKENS.md`; do not quote token values from this page.

## Per-technology token surfaces

| Tech | Token reference | Consumption |
|---|---|---|
| Vanilla | `library/Vanilla/Components/DESIGN_TOKENS.md` (+ `tokens.css`) | `var(--ds-*, <fallback>)` inline in each `code.html`; `tokens.css` is the `:root` + dark override |
| Tailwind | `library/Tailwind/Components/STYLE_TOKENS.md` | the 15 style systems' shared conventions (fonts, surfaces, helpers) used by every section variant |
| React | `library/React/DESIGN_TOKENS.md` (+ `library/React/Sections/DESIGN_TOKENS.md`) | components consume the React token spec via Tailwind arbitrary values |
| Templates | `library/Vanilla/Templates/design-tokens.md` | template-level token notes |

## Dark mode

Token-driven components get dark mode from the `prefers-color-scheme: dark` override in `tokens.css`. When you adapt a resource, keep that media query (and the token references) intact — stripping it silently drops dark mode. The Vanilla quality bar checks for this; see [QA](qa/overview.md).

## Go deeper

- [Install & customize](tutorials/install-and-customize.md) — adapting tokens in a project.
- [Resource structure](resources/resource-structure.md) — where the token references live in each tech's files.
- [Technologies](resources/technologies.md) — per-tech conventions.
