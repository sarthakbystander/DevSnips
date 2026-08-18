# Segmented Select

Horizontal segmented selector with radiogroup semantics.

## Usage

```tsx
import { SegmentedSelect } from './code';

<SegmentedSelect label="View" options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}]} defaultValue="list" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SegmentedSelect } from './code';

<SegmentedSelect label="View" options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}]} defaultValue="list" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,disabled?}[]` | — | Segments. |
| `value` / `defaultValue` / `onChange` / `size` / `label` | — | — | Standard. |

## Behavior

A row of segments where exactly one is active. NOT a dropdown — a horizontal segmented control. Keyboard: ArrowLeft/Right/Up/Down moves between segments (roving tabindex), Home/End jump, Tab enters/exits the group. Active segment = `surface-active` + `font-medium` + border emphasis.

## Accessibility

`role="radiogroup"` wrapper; each segment `role="radio" aria-checked` with roving tabindex.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use for a small, mutually-exclusive option set where all choices should be visible at once.
