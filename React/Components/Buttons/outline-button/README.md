# Outline Button

Bordered, transparent-fill medium-emphasis action that pairs with a primary button.

## Usage

```jsx
<OutlineButton size="md" onClick={cancel}>Cancel</OutlineButton>
```

## Props

`children` · `size` · `block` · `iconLeft` · `iconRight` · `loading` · `disabled` · `type` · `onClick`

## Variants

Single outline variant — transparent fill, `color.border-strong` border, `color.surface-hover` on hover.

## Sizes

sm · **md (default)** · lg. xs/xl omitted; outline is a secondary emphasis and rarely needs extreme sizes.

## States

default · hover (surface lift) · active · focus-visible · loading · disabled.

## Accessibility

Native `<button>`, visible focus ring, `aria-busy` while loading, perceivable disabled state.

## Behavior

Medium emphasis — the standard Cancel / secondary action in a primary/secondary pair. Hover lifts the fill without changing the border weight.

## Design Tokens

Color (`color.border-strong`, `color.surface-hover`, `color.foreground`), Radius (`radius-sm`), Borders (1px), Sizing, Motion.

## Notes

Use alongside a SolidButton to establish primary/secondary hierarchy. Avoid stacking several outline buttons of equal weight.
