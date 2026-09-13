# CTA — Neo Brutalist

A production-ready DevSnips React CTA section in the **Neo Brutalist** direction.

## Usage

`code.tsx` is the authored implementation and `code.jsx` exposes the same public API. See `code.tsx` for the exact props and defaults.

```tsx
import { CTASection } from "./code";

export default function Page() {
  return <CTASection />;
}
```

## Customization

Use the props documented in `code.tsx` to replace the eyebrow, title, description, actions, and footnote.

## Accessibility

Preserve the heading hierarchy, link labels, and visible focus states.

## Files

- `code.tsx` — authored TypeScript implementation
- `code.jsx` — JavaScript API parity entrypoint
- `preview.html` — runnable preview
- `metadata.json` — registry metadata
