# Add Button

A creation affordance with a leading plus. `label` is both the visible text and (when icon-only) the accessible name. Defaults to solid since adding is often the primary creation action on a surface.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<AddButton onClick={create}>Add member</AddButton>
<AddButton showLabel={false} label="Add row" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | `"Add"` |
| `variant` | `solid \| outline \| secondary \| ghost` | `solid` |
| `size` | `ButtonSize` | `md` |
| `showLabel` | `boolean` | `true` (icon-only when false; `children` becomes `aria-label`) |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

solid (default) · outline · secondary · ghost.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · active · focus-visible · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. Icon-only mode uses `children` (or "Add") as `aria-label`.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Reserve for creation actions. For a floating primary compose action, use FloatingActionButton instead.
