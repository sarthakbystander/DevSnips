# Agent Instructions — Documentation Site

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A light-mode-first developer documentation template: 15 routed sections via hash routing, a nested sidebar, a scrollspy TOC, a Cmd+K search palette, tabbed code blocks with a lightweight syntax highlighter, and five callout variants. Modular files.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system (1062 references, 81 unique tokens&mdash;the most token-saturated template). **Light is the default**; dark mode is opt-in (persisted, no-flash pre-paint script). Blue-600 accent&mdash;never violet/neon.

## File layout

```
Documentation Site/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # the design system (--ds-* tokens)
│   └── script.js      # router + content + scrollspy + search + code tools + theme
├── assets/            # logo.svg, favicon.svg
├── preview.html       # self-contained preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

All content lives in `script.js` (`NAV` config + `PAGES.<id>` content builders)&mdash;there are no per-page files. `preview.html` is `code.html` with `style.css` + `script.js` inlined.

## How to adapt it

1. **Change the docs content**: edit the `PAGES` object in `pages/script.js` (each page id maps to a content-builder function). The router and sidebar regenerate from `NAV`.
2. **Restructure navigation**: edit the `NAV` config in `pages/script.js` (groups + nested entries).
3. **Rebrand**: edit the `--ds-*` tokens in `pages/style.css` `:root`&mdash;keep blue-600 as the accent.
4. **Rebuild the preview**: after editing the modular files, regenerate `preview.html` by inlining `style.css` and `script.js` into `code.html`.

## Do not

- Do not introduce a framework. The router, search, and highlighter are deliberately vanilla.
- Do not move content out of `script.js` into separate page files&mdash;the hash router expects in-memory content builders.
- Do not darken the default theme. Light is the canonical docs experience.

## Quality bar

Reduced-motion guards on all animations, ARIA on the search dialog / tablists / drawer / TOC, `:focus-visible` rings, keyboard-operable (Esc, Cmd/Ctrl+K, `/`, arrows, Enter). Run `python3 scripts/qa_vanilla.py` after changes.

## Gotcha

`script.js` and the inlined `preview.html` script block contain example code strings with literal `<script>` tags&mdash;the closing `</script>` must be escaped as `<\/script>` in JS source or the HTML parser closes the real script block prematurely.
