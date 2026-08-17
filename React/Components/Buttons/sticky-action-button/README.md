# Sticky Action Button

Primary action pinned to the viewport base so it stays reachable while scrolling.

## Usage

```jsx
<StickyActionButton onClick={submit} loading={submitting}>Confirm & subscribe</StickyActionButton>
```

## Props

`children` · `iconLeft` · `iconRight` · `loading` · `disabled` · `variant` (solid|destructive|success) · `type` · `onClick`

## Variants

solid (default) · destructive · success.

## Sizes

lg (block, full-width).

## States

default · hover · active · focus-visible · loading (spinner + `aria-busy`) · disabled.

## Accessibility

Native `<button>`, `aria-busy` while loading. Sticky bar has a hairline top border + translucent surface so the boundary is clear. The action stays in the tab order while scrolling.

## Behavior

Persistent primary CTA pinned to the viewport (or panel) base. Full-width so it stays reachable on mobile; the translucent surface lets content scroll beneath.

## Design Tokens

Elevation (translucent surface + border, not heavy shadow), Sizing (lg block), Color (variant tokens), Motion.

## Notes

Use one sticky CTA per long form/review screen. Don't stack multiple — pick the single primary action.
