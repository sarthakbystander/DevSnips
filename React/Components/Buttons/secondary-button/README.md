# Secondary Button

Tonal secondary surface button for frequent, lower-stakes toolbar actions.

## Usage

```jsx
<SecondaryButton iconLeft={<Icon name="duplicate" />}>Duplicate</SecondaryButton>
```

## Props

`children` · `size` · `block` · `iconLeft` · `iconRight` · `loading` · `disabled` · `onClick`

## Variants

Single tonal variant — `color.secondary` background with `color.border`.

## Sizes

sm · **md (default)** · lg.

## States

default · hover (surface-active) · active · focus-visible · loading · disabled.

## Accessibility

Native `<button>`, focus ring, `aria-busy` on loading.

## Behavior

Lower emphasis than solid, higher than outline/ghost. Best for repeated toolbar actions (Rename, Duplicate, Archive) where a solid button would over-emphasise.

## Design Tokens

Color (`color.secondary`, `color.secondary-foreground`, `color.border`), Radius, Sizing, Motion.

## Notes

Sits between solid and outline in the emphasis ladder: solid → secondary → outline → ghost.
