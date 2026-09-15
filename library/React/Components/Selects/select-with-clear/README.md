# Select With Clear

Custom single-select with a clear control that resets the selection.

## Usage

```tsx
import { SelectWithClear } from './code';

<SelectWithClear label="Environment" options={opts} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithClear } from './code';

<SelectWithClear label="Environment" options={opts} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `clearLabel` | `string` | `"Clear selection"` | Accessible label for the clear button. |
| `onChange` | `(value, option \| null) => void` | — | Called with `null` on clear. |
| `options` / `value` / `defaultValue` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

When a value is selected, an `x` clear button appears in the trigger. Clicking it resets the selection to empty and calls `onChange(null, null)`. The clear button stops propagation so it does not open the listbox.

## Accessibility

The clear button is a real `<button type="button">` with an `aria-label` (default "Clear selection").

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Clearing is a distinct action from selecting a different option.
