# Agent Instructions — Product Launch

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A clean, restrained product launch / waitlist landing page for a dev-focused product. Single page: header, hero + waitlist, social proof, features, how it works, pricing, FAQ, final CTA, footer.

## Design system

Built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system. **Light-default**; calm opt-in dark mode (no-flash, persisted). Inter + JetBrains Mono. Hairline borders, small radii, single controlled blue accent, one primary action per section.

## File layout

```
product-launch/
├── pages/
│   ├── code.html      # HTML structure (links style.css + script.js)
│   ├── style.css      # design system (--ds-* tokens)
│   └── script.js      # theme toggle, mobile nav, FAQ accordion, waitlist form, reveal
├── preview.html       # self-contained preview (inlines CSS+JS)
├── metadata.json
└── README.md
```

## How to adapt it

1. **Swap the product**: edit `pages/code.html`&mdash;brand mark, name, version badge, hero headline/lede, status meta, feature copy, how-it-works steps, pricing tiers, FAQ items.
2. **Wire the waitlist to a backend**: the form in `script.js` currently simulates submission. Replace the success path with a real `fetch` to your endpoint; keep the inline validation and `aria-live` error messages.
3. **Rebrand**: edit the `--ds-*` tokens in `pages/style.css` `:root`&mdash;keep one controlled accent.
4. **Rebuild the preview**: run `python3 ../_build_preview.py .` from the template folder.

## Do not

- Do not add glassmorphism, neon, gradients, gradient text, or oversized hero/decoration.
- Do not introduce a framework. Vanilla HTML + CSS + JS only.
- Do not remove form validation or ARIA on the accordion/form.

## Quality bar

Skip link, semantic landmarks, single `h1`, ARIA on the FAQ accordion (`aria-expanded`/`aria-controls`/`role=region`), form `aria-invalid` + `aria-live` errors, `role=img` progress bar, `:focus-visible` rings, reduced-motion guard. Run `python3 scripts/qa_vanilla.py` after changes. Validate with `python3 scripts/_qa_template.py Vanilla/Templates/product-launch/preview.html`.
