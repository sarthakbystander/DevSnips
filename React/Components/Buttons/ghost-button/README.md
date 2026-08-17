# Ghost Button

Borderless, transparent low-emphasis button that reveals a surface only on hover.

## Usage

```jsx
<GhostButton size="sm" active={tab==="overview"}>Overview</GhostButton>
```

## Props

`children` · `size` · `iconLeft` · `iconRight` · `active` (sets `aria-pressed` + surface-active) · `disabled` · `onClick`

## Variants

Single ghost variant — transparent, borderless; hover lifts to `color.surface-hover`.

## Sizes

sm · **md (default)** · lg.

## States

default · hover · active (pressed) · focus-visible · disabled. `active` adds `aria-pressed` and `color.surface-active`.

## Accessibility

Native `<button>`. `active` exposes `aria-pressed`. Focus ring required and present.

## Behavior

Lowest emphasis — tertiary or incidental actions so the primary action keeps emphasis. Common in tab bars and inline toolbars.

## Design Tokens

Color (`color.surface-hover`, `color.surface-active`, `color.foreground`), Radius, Sizing, Motion.

## Notes

Because ghost buttons have no resting chrome, give them context (a label or adjacent control) so they remain discoverable.
