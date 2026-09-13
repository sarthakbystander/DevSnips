# Newsletter — Neo Brutalist

A production-ready DevSnips React Newsletter section in the **Neo Brutalist** direction.

## Usage

`code.tsx` is the authored implementation and `code.jsx` exposes the same public API. See `code.tsx` for the exact props and defaults.

```tsx
import { NewsletterSection } from "./code";

export default function Page() {
  return <NewsletterSection />;
}
```

## Customization

Use the props documented in `code.tsx` to replace copy, labels, and submission actions.

## Accessibility

Keep the form labels, error messaging, and focus states accessible when integrating it with a real endpoint.

## Files

- `code.tsx` — authored TypeScript implementation
- `code.jsx` — JavaScript API parity entrypoint
- `preview.html` — runnable preview
- `metadata.json` — registry metadata
