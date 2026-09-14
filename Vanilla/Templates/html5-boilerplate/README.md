# HTML5 Boilerplate

A minimal, clean HTML5 starter template aligned with the DevSnips design system. Part of the DevSnips Vanilla Templates collection and built on the shared [`design-tokens.md`](../design-tokens.md) `--ds-*` token system.

## What it is

A single self-contained `index.html` with the bare HTML5 document skeleton&mdash;doctype, `<head>`, `<body>`&mdash;plus the core design-token foundation so a new page starts on the shared visual base from the first line.

## What&rsquo;s included

- HTML5 doctype, `<html lang="en">`, viewport + description meta.
- Core `--ds-*` design tokens (semantic background/text/border/action/accent, fonts, radii, spacing, motion).
- Light-default theme with calm opt-in dark mode via `[data-theme="dark"]`.
- No-flash pre-paint theme script (saved preference or system preference).
- System-font stack: Inter + JetBrains Mono, with fallbacks (no external download required to function).
- Box-sizing reset and base body styles on tokens.
- `:focus-visible` ring for keyboard users.
- `prefers-reduced-motion` guard.

## Structure

```
html5-boilerplate/
├── pages/
│   └── index.html   # the starter document
├── preview.html     # iframe wrapper so the preview opens directly
├── metadata.json
└── README.md
```

## Usage

Copy `pages/index.html` and start writing your content where the `<!-- Your content starts here. -->` marker sits. To extend the token set, refer to the full specification in [`design-tokens.md`](../design-tokens.md).

## Dependencies

None. System fonts with fallbacks&mdash;the page is fully functional with no network.
