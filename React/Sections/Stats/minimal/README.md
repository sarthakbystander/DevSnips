# Stats — Minimal

A production-ready DevSnips React Stats section in the **Minimal** direction.

## Usage

`code.tsx` is the authored implementation and `code.jsx` exposes the same public API. See `code.tsx` for the exact props and defaults.

```tsx
import { StatsSection } from "./code";

export default function Page() {
  return <StatsSection />;
}
```

## Customization

Use the props documented in `code.tsx` to replace metric values, labels, descriptions, and supporting content.

## Accessibility

Keep metric labels associated with values and preserve heading hierarchy and readable text.

## Files

- `code.tsx` — authored TypeScript implementation
- `code.jsx` — JavaScript API parity entrypoint
- `preview.html` — runnable preview
- `metadata.json` — registry metadata
