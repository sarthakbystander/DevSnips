# Install & customize a resource

This tutorial covers installing a resource and adapting it to your project's design system without breaking its self-containment or accessibility guarantees.

## 1. Install

Pick a resource with the shape you want, then install it (example: a Vanilla split button):

```bash
npx devsnips add Vanilla/Components/Buttons/split-button
```

Output goes to `./devsnips/vanilla/components/buttons/split-button/`.

## 2. Understand what you got

A Vanilla component ships `code.html` — a **self-contained** snippet with its `<style>` and `<script>` inline. It references design tokens as `var(--ds-*, <original>)` so it renders correctly **with or without** the shared token file:

- **Standalone** (no `tokens.css`): the fallback value applies; the component looks as authored.
- **Themed** (include `library/Vanilla/Components/tokens.css`): every component speaks the same language and re-themes together.

See [Theming](../theming.md) for the token contract.

A Tailwind component ships `code.html` (snippet only — no DOCTYPE/CDN) + a full `preview.html`. A React component ships `code.tsx` (and a `code.jsx` parity build for Components). See [Resource structure](../resources/resource-structure.md).

## 3. Adapt without breaking guarantees

### Colors and spacing

Change token **values**, not the token wiring. For Vanilla, edit the fallback or include `tokens.css` and edit the `:root` block — never delete the `var(--ds-…)` reference, or the component stops re-theming.

```css
/* standalone tweak — keep the token reference */
border-radius: var(--ds-radius-md, 12px);   /* was 8px */
```

For Tailwind, adjust the utility classes directly in `code.html`. For React, the component reads the React token spec via Tailwind arbitrary values — see `library/React/DESIGN_TOKENS.md`.

### Dark mode

Vanilla components that support dark mode read `prefers-color-scheme` (and/or the `tokens.css` dark override). Keep that media query intact when you adapt; stripping it silently drops dark mode. The quality bar checks for this — see [QA](../qa/overview.md).

### Accessibility (do not regress)

- Keep native semantics first (`<button>`, `<nav>`, `<label>`); add ARIA only where native HTML is insufficient.
- Keep `focus-visible` styling so keyboard focus is visible.
- Keep any `prefers-reduced-motion` guard on animations.

These are enforced by `qa_vanilla.py` for Vanilla components; keep them intact when you adapt.

## 4. Update the project context

The CLI records the install in `devsnips/config.json` automatically. If you adapt the resource, keep `devsnips/AGENTS.md` notes for any project-specific conventions you apply — that file is user-owned and never overwritten by the CLI.

## Go deeper

- [Theming](../theming.md) — the `--ds-*` contract and per-tech token consumption.
- [Components](../resources/components.md) — the component type per technology.
- [CLI troubleshooting](../cli/troubleshooting.md) — if an install failed.
