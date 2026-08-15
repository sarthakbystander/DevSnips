# Agent Instructions — Job Board

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A dense, structured developer job board: single-page view switching (jobs, job detail, companies, company detail, saved, candidate) with keyword search, location/type filters, category chips, paginated lists, a scoped apply modal, toasts, and a mobile filter drawer. All data lives in `script.js`.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system. The template's original `--color-*` vocabulary is mapped onto `--ds-*` tokens so the light-mode visual output is preserved while the shared system is the foundation. **Light is the default**; opt-in calm dark mode via `prefers-color-scheme` (accent + status colors preserved).

## File layout

```
Job Board/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # the design system (--ds-* tokens + --color-* mapping)
│   └── script.js      # all views, rendering, filtering, pagination, save/apply, drawer
├── preview.html       # self-contained preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

All data (10 companies, 24 jobs, applications) lives in `script.js`.

## How to adapt it

1. **Swap the dataset**: replace the company/job/application arrays in `pages/script.js` with realistic content per `design-tokens.md` §48.
2. **Rebrand**: edit the `--ds-*` tokens in `pages/style.css` `:root`&mdash;the `--color-*` mapping resolves them automatically.
3. **Add a filter**: add a category chip + a filter predicate in the jobs view rendering in `script.js`.
4. **Rebuild the preview**: regenerate `preview.html` by inlining `style.css` and `script.js` into `code.html`.

## Do not

- Do not introduce a framework or a backend. Views are rendered client-side from in-memory data.
- Do not break the `--color-*` → `--ds-*` mapping unless you also rewrite the stylesheet's value references.
- Do not use color alone for job status&mdash;badges convey state via text labels too.

## Quality bar

ARIA on the search input, filter selects, apply modal (`role=dialog`/`aria-modal`, Esc + overlay close), `aria-expanded` on the mobile toggle, `:focus-visible` rings, reduced-motion guard, status badges convey state beyond color. Run `python3 scripts/qa_vanilla.py` after changes.
