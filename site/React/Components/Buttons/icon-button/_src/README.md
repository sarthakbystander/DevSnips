# Icon Button

A square icon-only control. No visible label, so an accessible name is required. Matches control height; the icon slot is square (width equals height).

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<IconButton icon={<Trash className="shrink-0" />} label="Delete row" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `icon` | `ReactNode` | — (required) |
| `label` | `string` | — (required: accessible name) |
| `variant` | `ghost \| outline \| secondary \| solid` | `ghost` |
| `size` | `ButtonSize` | `md` |
| `active` | `boolean` | `false` |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`. `label` is always rendered as `aria-label`.

## Variants

ghost (default) · outline · secondary · solid. Same emphasis semantics as the labeled variants.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Icon-only: the button is square (`w` == `h`); padding is removed.

## States

default · hover · active · focus-visible · selected (`active` → `aria-pressed` + `surface-active`) · disabled (reduced opacity).

## Accessibility

**Icon-only buttons must have an accessible name.** `label` is required and renders as `aria-label`. Renders a native `<button>`; focus-visible ring uses `color.focus-ring`. Meets 44px touch target at lg/xl. Never omit `label` — a button with no text and no aria-label is unnamed to screen readers.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use where a label would be redundant given surrounding context (toolbar, card header, table row). When space allows, prefer a labeled button — it's more discoverable.
