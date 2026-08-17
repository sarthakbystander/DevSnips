# Refresh Button

Re-fetch control that spins the refresh icon while the request is in flight.

## Usage

```jsx
<RefreshButton onRefresh={refetch} />  // icon-only
<RefreshButton showLabel onRefresh={refetch} />
```

## Props

`onRefresh` (may return a Promise) · `label` (default 'Refresh') · `showLabel` (default false) · `size` · `variant`

## Variants

ghost (default) · outline · secondary.

## Sizes

**sm (default)** · md.

## States

default · hover · **loading** (spinning icon + `aria-busy` + disabled) · focus-visible.

## Accessibility

`aria-busy` while in flight. Icon-only by default — `label` is the accessible name. Spinner respects `prefers-reduced-motion` (slower, not removed, so the state is still perceivable).

## Behavior

Re-fetches data. Disables re-trigger until the request settles to prevent duplicate fetches. `onRefresh` may return a Promise; the spinner runs until it resolves.

## Design Tokens

Motion (spin, respects reduced-motion), Iconography (refresh), Sizing, Color, States (§15).

## Notes

Update a 'last refreshed' timestamp alongside so users see the result of the refresh, not just the spin.
