# Filter Button

Opens filters and shows the active count. `activeCount` renders a count chip and switches the button to `surface-active` so the filtered state is obvious. `open` rotates the leading icon and exposes `aria-expanded`.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<FilterButton activeCount={3} open={open} onToggle={toggle} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `activeCount` | `number` | `0` |
| `open` | `boolean` | `false` (sets `aria-expanded`) |
| `label` | `string` | `"Filter"` |
| `variant` | `outline \| secondary \| ghost` | `outline` |
| `size` | `ButtonSize` | `sm` |
| `onToggle` | `() => void` | — |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

outline (default) · secondary · ghost. When `activeCount > 0` the button uses `surface-active` and shows a count chip.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm` for toolbars.

## States

default · hover · focus-visible · open (`aria-expanded`, icon rotates) · active-filters (`surface-active` + count chip) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. `aria-expanded` reflects `open`; `aria-label` includes the active count (e.g. "Filter, 3 active"). The count chip is decorative (`aria-hidden`) because the count is already in the label.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Wire to a popover/panel of filter controls. Keep the count accurate so the state is trustworthy.
