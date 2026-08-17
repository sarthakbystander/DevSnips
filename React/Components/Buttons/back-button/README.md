# Back Button

Navigation control that returns to the previous view with a leading arrow.

## Usage

```jsx
<BackButton href="/projects">All projects</BackButton>
// icon-only:
<BackButton showLabel={false} label="Back to results" />
```

## Props

`children` (default 'Back') · `href` (renders `<a>`) · `size` · `variant` (ghost|outline) · `showLabel` · `onClick` · `label` (aria-label when icon-only)

## Variants

ghost (default) · outline.

## Sizes

sm · **md (default)**.

## States

default · hover · focus-visible · disabled.

## Accessibility

Renders `<button>` or `<a>`. Icon-only mode exposes `label` as `aria-label`. Leading arrow-left conveys direction.

## Behavior

Returns to the previous view. Use above page content or as a wizard footer action. For real navigation use `href`.

## Design Tokens

Iconography (arrow-left), Sizing, Color, Motion.

## Notes

Prefer browser/SPA back for app navigation; use this for explicit 'Back to list' affordances where the destination isn't obvious.
