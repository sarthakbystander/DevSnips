# Refresh Button

Re-fetch with in-flight feedback. `onRefresh` may return a Promise; while pending, the refresh icon spins (respecting reduced motion), the button is disabled, and `aria-busy` is set. Icon-only mode for compact toolbars.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<RefreshButton onRefresh={refetch} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `onRefresh` | `() => void \| Promise<void>` | — |
| `label` | `string` | `"Refresh"` |
| `showLabel` | `boolean` | `false` (icon-only when false; `label` becomes `aria-label`) |
| `variant` | `ghost \| outline \| secondary` | `ghost` |
| `size` | `ButtonSize` | `sm` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

ghost (default) · outline · secondary.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm`; icon-only by default for compact toolbars.

## States

default · hover · focus-visible · refreshing (spinner-spin icon + `aria-busy`, disabled) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. `aria-busy` reflects the refreshing state; `aria-label` is `label`. Reduced motion disables the spin animation.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Icon-only by default — place in a toolbar next to a data region. Pass `showLabel` for a labeled refresh action.
