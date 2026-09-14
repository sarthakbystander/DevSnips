# Sticky Action Button

A persistent primary CTA that sticks to the bottom of the viewport with a hairline top border and a translucent surface so content scrolls beneath. Use for the single primary action on long forms or review screens.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<StickyActionButton onClick={submit} loading={saving}>Submit order</StickyActionButton>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | — |
| `variant` | `solid \| destructive \| success` | `solid` |
| `loading` | `boolean` | `false` |
| `disabled` | `boolean` | `false` |
| `iconLeft` / `iconRight` | `ReactNode` | — |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`. The component renders a sticky bar wrapping the action.

## Variants

solid (default) · destructive · success. The bar is sticky with a hairline top border and a translucent backdrop-blurred surface.

## Sizes

Always `lg` block (full-width) inside the bar — it's the single primary action on a long surface.

## States

default · hover · active · focus-visible · loading (spinner + `aria-busy`, disabled) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. The bar is a landmark-free wrapper; the action is a full-width block button so it's an unambiguous primary target. Reduced motion disables the bar's backdrop transition.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use for the single primary action on long forms or review screens (Submit order, Confirm and pay). Pair with a non-destructive escape above if needed.
