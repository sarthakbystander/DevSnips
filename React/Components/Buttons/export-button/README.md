# Export Button

Menu trigger for export destinations with a keyboard-navigable list.

## Usage

```jsx
<ExportButton formats={[{id:"csv",label:"Export as CSV"},…]} onExport={handle} />
```

## Props

`formats` ({id,label,icon}) · `onExport(id, format)` · `size` · `variant` · `disabled` · `label`

## Variants

outline (default) · secondary.

## Sizes

**sm (default)** · md.

## States

default · hover · open (menu) · focus-visible · disabled.

## Accessibility

Trigger has `aria-haspopup="menu"` + `aria-expanded`. Menu `role="menu"`, items `role="menuitem"`. Keyboard: Arrow keys move, Enter exports, Escape closes and returns focus. Outside click closes.

## Behavior

Menu trigger for export destinations. Use where multiple export targets exist; for a single format use DownloadButton.

## Design Tokens

Elevation (`shadow-md` menu), Radius, Iconography (download, chevron), Sizing, Motion.

## Notes

Don't use for a single format — DownloadButton is simpler. Keep format labels specific ('Export as CSV', not just 'CSV').
