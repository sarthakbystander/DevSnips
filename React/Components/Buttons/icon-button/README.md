# Icon Button

Square icon-only control requiring an accessible name; matches control height.

## Usage

```jsx
<IconButton name="settings" label="Settings" size="sm" />
```

## Props

`name` (icon key) · `label` (required, becomes `aria-label`) · `size` · `variant` (ghost|outline|secondary|solid) · `active` · `disabled` · `onClick`

## Variants

ghost (default) · outline · secondary · solid. Square (`--icon` modifier: width == height).

## Sizes

sm · **md (default)** · lg.

## States

default · hover · active (`aria-pressed` + surface-active) · focus-visible · disabled.

## Accessibility

Icon-only, so `label` is mandatory for an accessible name. `active` exposes `aria-pressed`. Focus ring present. 36px (md) meets touch target; bump to lg on mobile.

## Behavior

Single iconographic action where a label would be redundant given surrounding context (card header, toolbar).

## Design Tokens

Iconography (16px default, 14/20 variants), Sizing (control height), Color (variant tokens), Radius.

## Notes

Never ship an IconButton without `label`. If the action is ambiguous in context, use a labeled button instead.
