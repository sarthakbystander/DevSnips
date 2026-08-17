# More Actions Button

Overflow menu trigger for contextual row or card actions.

## Usage

```jsx
<MoreActionsButton actions={[{id:"edit",label:"Edit details",icon:"edit"},…]} onAction={handle} />
```

## Props

`actions` ({id,label,icon,destructive}) · `onAction(id, action)` · `size` · `variant` · `label` (default 'More actions') · `align` (left|right)

## Variants

ghost (default) · outline · secondary.

## Sizes

**sm (default)**.

## States

default · hover · open (menu) · focus-visible.

## Accessibility

Trigger `aria-haspopup="menu"` + `aria-expanded` + `aria-label`. Menu `role="menu"`, items `role="menuitem"`. Destructive items use `data-variant="destructive"` (destructive color + explicit verb). Keyboard: Arrow keys move, Enter activates, Escape closes + returns focus. Outside click closes.

## Behavior

Overflow menu for contextual row/card actions. Keeps primary actions visible and tucks the rest behind a predictable 'more' affordance.

## Design Tokens

Elevation (`shadow-md` menu), Radius (`radius-md` menu), Iconography (more), Sizing, Color (destructive).

## Notes

Order actions by frequency. Put destructive actions last and mark them destructive. Keep the list under ~8 items; if longer, reconsider the IA.
