# Inline Edit Select

A displayed value that switches into an editable select on demand.

## Usage

```tsx
import { InlineEditSelect } from './code';

<InlineEditSelect label="Environment" options={opts} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { InlineEditSelect } from './code';

<InlineEditSelect label="Environment" options={opts} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` | — | — | As reference. |
| `editLabel` | `string` | `"Edit"` | `aria-label` for the edit trigger. |

## Behavior

Displays the selected value as static text with a hover affordance + edit pencil. Click/Enter starts editing (reveals a combobox). Selecting an option saves + returns to display. Escape reverts (cancels) + returns to display. Outside-click while editing closes and keeps the current selection.

## Accessibility

The edit trigger is a labeled button (`aria-label` default "Edit"); the editing combobox uses the full ARIA listbox pattern.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use for values that are usually read but occasionally edited (e.g. a setting in a table row).
