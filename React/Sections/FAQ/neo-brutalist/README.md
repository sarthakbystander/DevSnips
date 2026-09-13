# FAQ — Neo Brutalist

A production-ready DevSnips React FAQ section in the **Neo Brutalist** direction.

## Usage

`code.tsx` is the authored implementation and `code.jsx` exposes the same public API. See `code.tsx` for the exact props and defaults.

```tsx
import { FAQSection } from "./code";

export default function Page() {
  return <FAQSection />;
}
```

## Customization

Pass the props documented in `code.tsx` to replace content and behavior while keeping the section's responsive layout and design tokens.

## Accessibility

Preserve the semantic headings, labels, keyboard interactions, and visible focus states when customizing the section.

## Files

- `code.tsx` — authored TypeScript implementation
- `code.jsx` — JavaScript API parity entrypoint
- `preview.html` — runnable preview
- `metadata.json` — registry metadata
