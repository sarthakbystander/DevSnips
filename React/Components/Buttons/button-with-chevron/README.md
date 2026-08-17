# Button With Chevron

Button with a directional chevron that rotates to reflect open state.

## Usage

```jsx
<ButtonWithChevron open={open} onClick={toggle} aria-controls="panel">Advanced filters</ButtonWithChevron>
```

## Props

`children` · `direction` (down|right, default down) · `open` (rotates a down chevron 180°) · `variant` · `size` · `disabled` · `onClick` · `aria-controls`/`aria-expanded` passthrough

## Variants

solid · outline (default) · secondary · ghost.

## Sizes

sm · **md (default)** · lg.

## States

default · hover · active · focus-visible · open (chevron rotated) · disabled.

## Accessibility

Exposes `aria-expanded` when `open` (or an explicit `aria-expanded`). Pair with `aria-controls` to associate the toggled panel. Focus ring present.

## Behavior

Disclosure/menu affordance. `direction="right"` is for advancing; `direction="down"` (default) rotates on open to signal expansion.

## Design Tokens

Motion (chevron rotation, default duration), Iconography, Sizing, Color.

## Notes

For true menus, also wire keyboard (ArrowDown to open). See SplitButton / MoreActionsButton for full menu implementations.
