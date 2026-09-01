# Button With Chevron

A labeled button with a trailing chevron. `direction` controls orientation (down for menus/disclosure, right for advancing), and `open` rotates a down chevron to signal an expanded state.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<ButtonWithChevron open={open} onClick={toggle}>Sort by date</ButtonWithChevron>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | — |
| `direction` | `down \| right` | `down` |
| `open` | `boolean` | `false` (rotates a `down` chevron 180°) |
| `variant` | `solid \| outline \| secondary \| ghost` | `outline` |
| `size` | `ButtonSize` | `md` |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`. `aria-expanded` reflects `open` unless overridden by an `aria-expanded` prop.

## Variants

outline (default) · solid · secondary · ghost.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · active · focus-visible · open (chevron rotated, `aria-expanded`) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. When used as a disclosure/menu trigger, `aria-expanded` reflects `open` (pass it explicitly if you also control focus). The chevron rotation is a visual cue, not the only one — `aria-expanded` is the contract with assistive tech.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use `direction="down"` for menus and disclosure; `direction="right"` for advancing/next. The chevron rotates via a `transition-transform` that respects reduced motion.
