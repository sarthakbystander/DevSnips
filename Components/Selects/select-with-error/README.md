# Select With Error

Custom select with an error message and aria-invalid state.

## Usage

```tsx
import { SelectWithError } from './code';

<SelectWithError label="Environment" error="Select a deploy target." options={opts} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithError } from './code';

<SelectWithError label="Environment" error="Select a deploy target." options={opts} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | `"Select"` | Visible label. |
| `error` | `string` | — | Error message; sets `aria-invalid`. |
| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |

## Behavior

Reference combobox/listbox behavior with a destructive border + error message when `error` is set.

## Accessibility

`aria-invalid="true"` on the trigger; error message linked via `aria-describedby`. State is communicated by border + text, not color alone.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Clear the `error` prop once the user makes a valid selection.
