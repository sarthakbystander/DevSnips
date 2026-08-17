# Toggle Button

Single on/off control exposing aria-pressed and a distinct selected surface.

## Usage

```jsx
<ToggleButton label="Pin" iconOff="pin" pressed={pinned} onToggle={setPinned} />
```

## Props

`label` (visible text and, when icon-only, `aria-label`) · `pressed` (controlled) · `defaultPressed` · `onToggle(pressed)` · `iconOff` · `iconOn` · `showLabel` · `size` · `variant`

## Variants

ghost (default) · outline · secondary.

## Sizes

sm · **md (default)**.

## States

default · hover · **pressed** (`aria-pressed="true"` + surface-active + semibold) · focus-visible · disabled.

## Accessibility

Exposes `aria-pressed`. Pressed state shown by background + weight, not color alone. Icon-only mode uses `label` as the accessible name.

## Behavior

Single binary switch. Controlled (`pressed`) or uncontrolled (`defaultPressed`). `iconOn`/`iconOff` can reflect state in the icon.

## Design Tokens

Color (surface-active), Typography (weight), Iconography, Sizing, Motion.

## Notes

For multi-option or grouped toggles, use ToggleGroup. Avoid using toggle for navigation — use it for state.
