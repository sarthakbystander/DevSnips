# Integrations — Neo Brutalist

A production-ready DevSnips React Integrations section in the **Neo Brutalist** direction.

## Usage

`code.tsx` is the authored implementation and `code.jsx` exposes the same public API. See `code.tsx` for the exact props and defaults.

```tsx
import { IntegrationsSection } from "./code";

export default function Page() {
  return <IntegrationsSection />;
}
```

## Customization

Use the props documented in `code.tsx` to replace integration names, icons, descriptions, and links.

## Accessibility

Provide accessible names for integration icons and preserve heading hierarchy and focus states.

## Files

- `code.tsx` — authored TypeScript implementation
- `code.jsx` — JavaScript API parity entrypoint
- `preview.html` — runnable preview
- `metadata.json` — registry metadata
