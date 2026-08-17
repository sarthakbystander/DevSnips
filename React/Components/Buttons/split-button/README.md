# Split Button

Primary action paired with an attached, keyboard-navigable action menu.

## Usage

```jsx
<SplitButton label="Create project" actions={[{id:"blank",label:"Blank project"},…]} onAction={handle} />
```

## Props

`label` · `actions` ({id,label,icon,destructive}) · `onAction(id, action)` · `variant` (solid|outline) · `size` · `disabled`

## Variants

solid (default) · outline.

## Sizes

sm · **md (default)** · lg.

## States

default · hover · active · focus-visible · open (menu) · disabled.

## Accessibility

Trigger has `aria-haspopup="menu"` + `aria-expanded`. Menu uses `role="menu"`, items `role="menuitem"`. Keyboard: trigger ArrowDown/Enter opens; Arrow keys move; Enter activates; Escape closes and returns focus to the trigger. Outside click closes.

## Behavior

The leading button fires the default (last-chosen) action; the chevron opens a menu of alternatives. Selecting an item sets it as the new default and fires `onAction`.

## Design Tokens

Elevation (`shadow-md` menu), Radius (`radius-md` menu, `radius-sm` button), Color, Sizing, Motion.

## Notes

Shared 1px border with negative margin keeps it one composite control. Don't use for navigation — use it for action variants.
