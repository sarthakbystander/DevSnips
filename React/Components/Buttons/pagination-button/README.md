# Pagination Button

Page navigation for paginated lists and tables. Renders Prev, a windowed number set with ellipses, and Next. The active page uses `surface-active` + `aria-current="page"`. Prev/Next disable at the bounds (kept perceivable, not removed).

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<PaginationButton page={page} totalPages={12} onPageChange={setPage} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `page` | `number` | `1` (current) |
| `totalPages` | `number` | `1` |
| `onPageChange` | `(page: number) => void` | — |
| `size` | `ButtonSize` | `sm` |
| `siblingCount` | `number` | `1` (pages shown either side of current) |

Plus all native `HTMLAttributes<HTMLElement>`.

## Variants

Single ghost style. Prev/Next are icon-only; numbered pages are square-ish buttons. Active page: `surface-active` + `aria-current="page"` + border-strong.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm`.

## States

default · hover · focus-visible · current (`aria-current="page"`, surface-active + border-strong) · disabled Prev/Next at bounds (`aria-disabled`, reduced opacity).

## Accessibility

Renders a `<nav aria-label="Pagination">`. Each page button has `aria-label="Page N"`; the current page has `aria-current="page"`. Prev/Next have `aria-label` and `aria-disabled` at the bounds (kept visible so the affordance stays perceivable). Focus-visible ring on every control.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Keep `siblingCount` modest (1–2) so the control stays compact. For very large counts, consider a jump-to-page input alongside.
