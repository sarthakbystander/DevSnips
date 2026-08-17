# Filter Button

Toolbar control that opens filters and signals an active-filtered state with a count badge.

## Usage

```jsx
<FilterButton activeCount={count} open={open} onToggle={toggle} />
```

## Props

`activeCount` (renders a count chip + surface-active when >0) · `open` (aria-expanded + icon rotation) · `size` · `variant` · `onToggle` · `label`

## Variants

outline (default) · secondary · ghost.

## Sizes

**sm (default)** · md.

## States

default · hover · active-filters (badge + surface-active + semibold) · open · focus-visible.

## Accessibility

`aria-expanded` when open. When filters are active, `aria-label` includes the count ('Filter, 3 active'). Active state conveyed by badge + weight, not color alone.

## Behavior

Opens filter criteria and signals an active-filtered state. Wire `onToggle` to a popover/panel of filter controls.

## Design Tokens

Color (surface-active, accent for the count chip), Iconography (filter), Sizing, Motion.

## Notes

The count badge is the clearest signal of an active filter. Clear-all should reset `activeCount` to 0.
