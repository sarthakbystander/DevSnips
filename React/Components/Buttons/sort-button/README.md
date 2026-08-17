# Sort Button

Control that sets sort field and direction with a directional indicator.

## Usage

```jsx
<SortButton field="Created" direction={dir} onToggle={cycle} />
```

## Props

`field` (active column label) · `direction` (asc|desc|null) · `onToggle` · `size` · `variant`

## Variants

outline (default) · secondary · ghost.

## Sizes

**sm (default)**.

## States

default · hover · active-sorted (surface-active + semibold + filled chevron) · focus-visible.

## Accessibility

`aria-label` includes the field and current direction ('Sort by Created, currently descending'). Direction shown by rotated chevron + label, not color alone.

## Behavior

Sets sort field and direction. Clicking toggles direction (desc↔asc). Active sort shown by the field label + directional chevron.

## Design Tokens

Iconography (sort, chevron), Motion (chevron rotation), Color (surface-active), Sizing.

## Notes

For multiple sortable columns, render one SortButton per column header, or use a menu trigger to pick the column.
