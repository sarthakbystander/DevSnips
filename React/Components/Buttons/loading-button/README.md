# Loading Button

Action button with a first-class loading state that preserves layout.

## Usage

```jsx
<LoadingButton variant="solid" loading={saving} loadingLabel="Saving…" onClick={save}>Save changes</LoadingButton>
```

## Props

`children` · `loadingLabel` (label shown while loading) · `variant` (solid|outline|secondary|destructive|success) · `size` · `block` · `iconLeft` · `loading` · `disabled` · `onClick`

## Variants

All base variants via `variant`. Loading is a state, not a separate visual style.

## Sizes

sm · **md (default)** · lg.

## States

default · hover · active · focus-visible · **loading** (spinner + `aria-busy`, disabled) · disabled.

## Accessibility

`aria-busy` set while loading; button disabled to prevent double-fire. Spinner is `aria-hidden` (state is conveyed by `aria-busy` + label change).

## Behavior

Async submit. The spinner occupies the leading icon slot so layout is preserved. Use `loadingLabel` to reflect the in-progress action ('Saving…', 'Exporting…').

## Design Tokens

Motion (spinner), Sizing, Color (variant tokens), States (§15 loading).

## Notes

Always change the label during loading so screen-reader users perceive the transition, not just `aria-busy`.
