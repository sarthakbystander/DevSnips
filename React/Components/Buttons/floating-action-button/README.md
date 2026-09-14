# Floating Action Button

A primary compose action hovering over content. Circular, elevated (shadow-md), fixed to a corner. Icon + optional label (extended FAB). `aria-label` is required. Reserve one per screen for the primary creation action.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<FloatingActionButton icon={<Plus />} label="New invoice" position="bottom-right" onClick={create} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `icon` | `ReactNode` | — (required; the action icon) |
| `label` | `string` | — (required: accessible name; visible when `extended`) |
| `position` | `bottom-right \| bottom-left \| top-right` | `bottom-right` |
| `extended` | `boolean` | `false` (icon+label pill when true) |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

Single solid circular FAB; extended mode renders an icon+label pill. Fixed to a viewport corner.

## Sizes

Default 56px (icon-only) / 48px tall extended. Meets 44px touch target.

## States

default · hover (subtle lift) · focus-visible · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. `label` is required and rendered as `aria-label`. Hover lift respects reduced motion. The FAB is `position: fixed` — keep exactly one per screen.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Reserve for the single primary creation action on a screen (compose, new invoice, new ticket). Don't use for navigation; that's a navbar/back-button's job.
