# Copy Button

Clipboard copy with transient feedback. Uses the async Clipboard API with an execCommand fallback. On success, swaps the icon to a check and the label to "Copied", then reverts. An `aria-live` region announces the copied state.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<CopyButton value={projectId} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `value` | `string` | — (text to copy) |
| `label` | `string` | `"Copy"` |
| `copiedLabel` | `string` | `"Copied"` |
| `resetMs` | `number` | `2000` |
| `onCopy` | `(value: string) => void` | — |
| `variant` | `outline \| secondary \| ghost \| solid` | `outline` |
| `size` | `ButtonSize` | `sm` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

outline (default) · secondary · ghost · solid.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm`.

## States

default · hover · focus-visible · **copied** (check icon + "Copied" label + `aria-live` announcement, reverts after `resetMs`).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. An `aria-live="polite"` region announces "Copied" so screen readers hear the result. `aria-label` includes the value being copied. Success is conveyed by icon + label change, not color alone.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Always pair with the value displayed nearby (a code/ID row) so the copy target is unambiguous. Gracefully degrades when the Clipboard API is unavailable.
