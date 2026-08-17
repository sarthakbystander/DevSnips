# Destructive Button

Filled destructive action for irreversible operations, with an outline variant.

## Usage

```jsx
<DestructiveButton variant="solid" onClick={del}>Delete project</DestructiveButton>
```

## Props

`children` · `variant` (solid|outline, default solid) · `size` · `block` · `iconLeft` · `loading` · `disabled` · `onClick`

## Variants

`solid` (filled `color.destructive`) and `outline` (destructive text + soft fill on hover) for lower-emphasis destructive controls.

## Sizes

sm · **md (default)** · lg.

## States

default · hover · active · focus-visible · loading · disabled.

## Accessibility

Native `<button>`, focus ring, `aria-busy`. Destructive intent is conveyed by the label and color together — never color alone, so always pair with an explicit verb ('Delete', 'Remove').

## Behavior

Irreversible actions only. Always provide a confirming context and a non-destructive Cancel. The outline variant suits dense rows where a filled button is too loud.

## Design Tokens

Color (`color.destructive`, `color.destructive-foreground`, `color.destructive-soft`), Radius, Sizing, Motion.

## Notes

Reserve for delete/remove/discard. One destructive action per confirmation surface.
