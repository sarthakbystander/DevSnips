# Segmented Button

Joined single-choice control — the compact alternative to radios or tabs.

## Usage

```jsx
<SegmentedButton value={range} onChange={setRange} options={[{value:"7d",label:"7d"},…]} label="Date range" />
```

## Props

`options` ({value,label,icon}) · `value` (controlled) · `onChange(value)` · `size` · `label` (radiogroup aria-label)

## Variants

Single joined segmented variant.

## Sizes

**sm (default)** · md.

## States

Per-segment: default · hover · selected (`aria-checked="true"` + surface-active + semibold) · focus-visible.

## Accessibility

Container `role="radiogroup"`, segments `role="radio"` + `aria-checked`. Selected state conveyed by background + weight, not color alone.

## Behavior

Single-choice control for 2–5 mutually exclusive options. Compact alternative to radio groups or tabs.

## Design Tokens

Borders (shared 1px), Radius (squared inner), Color (surface-active), Typography (weight change), Sizing.

## Notes

For more than ~5 options, use a Select. For multi-select, use ToggleGroup.
