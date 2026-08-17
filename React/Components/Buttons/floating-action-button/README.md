# Floating Action Button

Elevated circular control for the screen's primary compose action.

## Usage

```jsx
<FloatingActionButton icon="plus" label="New project" onClick={create} />
```

## Props

`icon` (default plus) · `label` (aria-label; visible when `extended`) · `position` (bottom-right|bottom-left|top-right) · `extended` (icon + label) · `disabled` · `onClick`

## Variants

Single elevated circular variant (`color.primary`, `shadow-md`).

## Sizes

56px (standard) · 48px height when `extended`. Icon 20px.

## States

default · hover (subtle lift) · focus-visible (ring) · disabled.

## Accessibility

`aria-label` required (defaults to icon name if `label` omitted). Fixed positioning keeps it reachable. Focus ring visible despite the circular shape.

## Behavior

Primary compose action hovering over content. One per screen, fixed to a corner. Extended variant shows the label for discoverability.

## Design Tokens

Elevation (`shadow-md`), Radius (`radius-full`), Sizing (56px), Color (`color.primary`), Motion (hover lift).

## Notes

Reserve for the single most important compose action on a screen. Avoid on screens that already have a persistent primary CTA.
