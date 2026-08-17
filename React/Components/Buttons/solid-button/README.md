# Solid Button

Filled primary action button — the canonical high-emphasis confirmation control.

## Usage

```jsx
<SolidButton size="md" onClick={save}>Save changes</SolidButton>
```

## Props

`children` · `size` (xs|sm|md|lg|xl, default md) · `block` · `iconLeft` · `iconRight` · `loading` · `disabled` · `type` · `onClick` · native button props

## Variants

Single filled variant built on `color.primary` / `color.primary-foreground`. See OutlineButton / SecondaryButton / GhostButton for other emphasis levels.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8→20px; icon 14→20px.

## States

default · hover · active · focus-visible · loading (spinner + `aria-busy`, layout preserved) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance. Meets 44px touch target at lg/xl.

## Behavior

One high-emphasis primary action per surface. Loading swaps the leading slot for a spinner and disables interaction; the label may change while loading.

## Design Tokens

Color (`color.primary`, `color.primary-foreground`), Sizing (control heights), Radius (`radius-sm`), Typography (`label-md`/`label-sm`), Motion (default duration), States (§15).

## Notes

Keep exactly one solid button per prominent surface to preserve hierarchy. Pair with an OutlineButton for the cancel/secondary action.
