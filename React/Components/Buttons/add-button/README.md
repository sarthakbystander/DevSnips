# Add Button

Creation affordance with a leading plus icon for adding items to a list.

## Usage

```jsx
<AddButton size="sm" onClick={add}>Add team</AddButton>
// icon-only:
<AddButton showLabel={false} label="Add member" />
```

## Props

`children` (default 'Add') · `variant` (solid|outline|secondary|ghost, default solid) · `size` · `showLabel` · `disabled` · `onClick` · `label` (aria-label when icon-only)

## Variants

solid (default) · outline · secondary · ghost.

## Sizes

sm · **md (default)**.

## States

default · hover · active · focus-visible · disabled.

## Accessibility

Leading plus icon is `aria-hidden`; the label is the accessible name. Icon-only mode uses `label` as `aria-label`.

## Behavior

Creation affordance — adding an item to a list, table, or form section. Defaults to solid because adding is often the primary creation action on a surface.

## Design Tokens

Iconography (plus), Sizing, Color, Radius.

## Notes

Use a specific verb ('Add team', 'Add field') rather than the generic 'Add' where possible.
