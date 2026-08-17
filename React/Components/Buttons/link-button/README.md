# Link Button

Button styled as an inline link for terse secondary actions inside forms and rows.

## Usage

```jsx
<LinkButton onClick={forgot}>Forgot password?</LinkButton>
// or true navigation:
<LinkButton href="/docs">Read the docs</LinkButton>
```

## Props

`children` · `iconLeft` · `iconRight` · `href` (renders an `<a>`) · `disabled` · `onClick`

## Variants

Single link variant — `color.link` text, underline on hover, no border or fill.

## Sizes

Inherits surrounding text size; height is auto (no fixed control height).

## States

default · hover (underline + `color.link-hover`) · focus-visible · disabled.

## Accessibility

Renders `<button>` for actions or `<a>` for navigation. Focus ring visible. `aria-disabled` when disabled link.

## Behavior

Terse inline actions that should read as links but still trigger `onClick`. For real navigation use `href`.

## Design Tokens

Color (`color.link`, `color.link-hover`), Typography (inherits), Motion.

## Notes

Don't use for primary actions — link styling signals low emphasis. Reserve for 'View all', 'Forgot password?', row-level 'Open'.
