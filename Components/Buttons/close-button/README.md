# Close Button

A dismiss control for overlays. Icon-only (X), requires an accessible name (defaults to "Close"). Use inside dialogs, drawers, toasts, and banners; pair with Escape handling on the owning surface.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<CloseButton onClick={closeDialog} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `label` | `string` | `"Close"` (rendered as `aria-label`) |
| `variant` | `ghost \| outline` | `ghost` |
| `size` | `ButtonSize` | `md` |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

ghost (default) · outline.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Icon-only: square (`w` == `h`).

## States

default · hover · focus-visible · disabled (reduced opacity).

## Accessibility

Icon-only, so an accessible name is **required** — `label` (default "Close") is rendered as `aria-label`. Focus-visible ring uses `color.focus-ring`. Pair with Escape handling on the owning dialog/drawer/banner.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use inside dialogs, drawers, toasts, banners. The owning surface should close on Escape and move focus appropriately.
