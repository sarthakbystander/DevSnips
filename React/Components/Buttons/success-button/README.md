# Success Button

Positive-emphasis action for confirm, publish, approve, and complete flows.

## Usage

```jsx
<SuccessButton loading={publishing} done={done} onClick={publish}>Publish changes</SuccessButton>
```

## Props

`children` · `size` · `block` · `iconLeft` · `iconRight` · `loading` · `done` (shows a check + suppresses trailing icon) · `disabled` · `onClick`

## Variants

Single filled variant on `color.success`. Contextual only.

## Sizes

sm · **md (default)** · lg.

## States

default · hover · active · focus-visible · loading · done (transient completion) · disabled.

## Accessibility

Native `<button>`, `aria-busy` while loading. The `done` state swaps the leading icon to a check and the label should change ('Published').

## Behavior

Positive confirmation — publish, approve, mark complete. Use a `done` state for transient success feedback, then revert.

## Design Tokens

Color (`color.success`, `color.success-foreground`), Radius, Sizing, Motion.

## Notes

Not a replacement for the primary action. Use when the action itself is explicitly affirmative.
