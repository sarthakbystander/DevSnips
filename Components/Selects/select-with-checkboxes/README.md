# Select With Checkboxes

Custom single-select where each option row shows a checkbox reflecting selection.

## Usage

```tsx
import { SelectWithCheckboxes } from './code';

<SelectWithCheckboxes label="Environment" options={opts} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithCheckboxes } from './code';

<SelectWithCheckboxes label="Environment" options={opts} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,disabled?}[]` | — | Option list. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

Each option row has a checkbox indicator that reflects the selected state. Click/Enter/Space selects (single-select: selecting one checks it, the previous selection unchecks) and closes. Keyboard ArrowUp/Down/Home/End navigates.

## Accessibility

Options are `role="option" aria-selected`; the checkbox glyph reflects `aria-selected` so state is communicated by shape + background, not color alone.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

The checkbox is a visual affordance for the single-select state — it is not a multi-select. For multiple selection see `multi-select`.
