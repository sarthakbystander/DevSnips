# Pagination Button

Page navigation with prev/next, windowed numbers, and clear active/disabled states.

## Usage

```jsx
<PaginationButton page={page} totalPages={20} onPageChange={setPage} />
```

## Props

`page` (current, 1-based) · `totalPages` · `onPageChange(page)` · `size` · `siblingCount` (default 1)

## Variants

Single navigation variant (ghost buttons + active page).

## Sizes

**sm (default)**.

## States

Per-button: default · hover · **active** (`aria-current="page"` + surface-active + border-strong + semibold) · focus-visible. Prev/Next **disabled** at bounds (`aria-disabled`, kept perceivable).

## Accessibility

`nav` with `aria-label="Pagination"`. Active page uses `aria-current="page"`. Prev/Next have descriptive `aria-label` and `aria-disabled` at bounds (not removed, so the affordance remains). Ellipses are `aria-hidden`.

## Behavior

Windowed page list with ellipses for large ranges. Prev/Next move by one. Active page is keyboard-focusable and clearly distinct via background + border + weight.

## Design Tokens

Iconography (chevron-left/right), Color (surface-active, border-strong), Typography (weight), Sizing, Motion.

## Notes

For very large ranges, add a 'rows per page' control and a jump-to-page field. Keep the active page's focus restored after navigation.
