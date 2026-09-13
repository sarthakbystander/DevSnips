# Comparison — Minimal

A production-ready DevSnips React Comparison section in the **Minimal** direction.

## Usage

`code.tsx` is the authored implementation and `code.jsx` exposes the same public API. See `code.tsx` for the exact props and defaults.

```tsx
import { ComparisonSection } from "./code";

export default function Page() {
  return <ComparisonSection />;
}
```

## Customization

Use the props documented in `code.tsx` to replace comparison labels, rows, values, and actions.

## Accessibility

Preserve table or list semantics, row/column relationships, labels, and visible focus states.

## Files

- `code.tsx` — authored TypeScript implementation
- `code.jsx` — JavaScript API parity entrypoint
- `preview.html` — runnable preview
- `metadata.json` — registry metadata
