# Button Group

Joined row of related buttons sharing a single border and rounded ends.

## Usage

```jsx
<ButtonGroup label="Alignment" variant="outline" size="sm" items={[{id:"left",label:"Left",active:true,onClick:…},…]} />
// or children:
<ButtonGroup><button/>…</ButtonGroup>
```

## Props

`items` ({id,label,icon,active,onClick}) or `children` (buttons) · `variant` · `size` · `label` (group aria-label)

## Variants

solid · outline · secondary · ghost via `variant`.

## Sizes

sm · **md (default)**.

## States

Per-button: default · hover · active (`aria-pressed`) · focus-visible · disabled.

## Accessibility

Container has `role="group"` + `aria-label`. Inner buttons share borders (overlapping 1px, squared radii) to read as one control.

## Behavior

Joined row of related buttons. Use for small choice sets and toolbars; for enforced single-choice prefer SegmentedButton.

## Design Tokens

Borders (shared 1px), Radius (squared inner), Sizing, Color.

## Notes

Active state uses `aria-pressed` + surface-active. For mutually-exclusive single choice, SegmentedButton is the better semantic.
