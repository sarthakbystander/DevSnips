# Toggle Group

Joined toggles supporting single- or multi-select with roving focus.

## Usage

```jsx
<ToggleGroup type="single" value={view} onValueChange={setView} options={[{value:"list",label:"List"},…]} label="View mode" />
```

## Props

`options` ({value,label,icon}) · `type` (single|multiple) · `value` (string for single, array for multiple) · `defaultValue` · `onValueChange` · `size` · `label`

## Variants

Single joined variant; type controls selection semantics.

## Sizes

**sm (default)** · md.

## States

Per-toggle: default · hover · **pressed** (`aria-pressed="true"` + surface-active) · focus-visible. Roving focus via Arrow keys.

## Accessibility

Container `role="group"`. Each toggle exposes `aria-pressed`. Arrow keys move focus between toggles; Space/Enter toggles.

## Behavior

`type="single"` = one on (radiogroup-like). `type="multiple"` = any number on (checkbox-like). Controlled or uncontrolled.

## Design Tokens

Borders (shared 1px), Radius (squared inner), Color (surface-active), Typography (weight), Sizing.

## Notes

Selected state uses surface-active + weight, not color alone. For strictly single-choice with a strong radiogroup semantic, SegmentedButton is equivalent.
