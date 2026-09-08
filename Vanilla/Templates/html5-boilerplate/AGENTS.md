# AGENTS.md — HTML5 Boilerplate

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A minimal, clean HTML5 starter template aligned with the DevSnips design system. A single self-contained `pages/index.html` with the bare document skeleton (doctype, head, body) plus the core `--ds-*` design-token foundation, so a new page starts on the shared visual base from the first line. No framework, no build step, no external dependencies.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system. **Light-default** with calm opt-in dark mode via `[data-theme="dark"]` (no-flash pre-paint script, saved or system preference). System font stack (Inter + JetBrains Mono with fallbacks) — no external download required to function.

## File layout

```
html5-boilerplate/
├── pages/
│   └── index.html   # the starter document
├── preview.html     # iframe wrapper so the preview opens directly
├── metadata.json
└── README.md
```

## How to adapt it

1. **Start a page**: copy `pages/index.html` and write content where the `<!-- Your content starts here. -->` marker sits.
2. **Rebrand**: edit the `--ds-*` tokens in the `:root` block of `<style>` — keep one controlled accent (`--ds-accent`).
3. **Extend tokens**: append family- or section-specific tokens per the full specification in [`design-tokens.md`](../design-tokens.md).
4. **Regenerate the preview**: `preview.html` is a thin `<iframe src="pages/index.html">` wrapper — no regeneration needed unless the wrapper itself changes.

## Do not

- Do not introduce a framework or a build step. Vanilla HTML + CSS + JS only.
- Do not remove the `--ds-*` token layer or hardcode visual values.
.
- Do not add heavy decoration; the starter is intentionally bare.

## Quality bar

Semantic HTML, `lang` attribute, viewport meta, `:focus-visible` ring, reduced-motion guard. Run `python3 scripts/qa_vanilla.py` after changes. Validate with `python3 scripts/_qa_template.py Vanilla/Templates/html5-boilerplate/preview.html`.