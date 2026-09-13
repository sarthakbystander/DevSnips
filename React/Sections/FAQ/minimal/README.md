# FAQ — Minimal

A production-ready DevSnips React FAQ section in the **Minimal** direction.

## Usage

The authored implementation is in `code.tsx`; `code.jsx` exposes the same public API for JavaScript consumers. See `code.tsx` for the exact props and defaults.

```tsx
import { FAQSection } from "./code";

export default function Page() {
  return <FAQSection />;
}
```

## Customization

Pass the component props documented in `code.tsx` to replace copy, items, and actions. The section uses DevSnips semantic tokens and Tailwind utility classes.

## Accessibility

Keep the supplied semantic heading structure, labels, keyboard interactions, and visible focus states when customizing the section.

## Files

- `code.tsx` — authored TypeScript implementation
- `code.jsx` — JavaScript API parity entrypoint
- `preview.html` — runnable preview
- `metadata.json` — registry metadata
