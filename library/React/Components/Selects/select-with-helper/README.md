# Select With Helper

Custom select with helper text linked through aria-describedby.

## Usage

```tsx
import { SelectWithHelper } from './code';

<SelectWithHelper label="Team member" helperText="Owner receives deploy notifications." options={opts} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithHelper } from './code';

<SelectWithHelper label="Team member" helperText="Owner receives deploy notifications." options={opts} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | `"Select"` | Visible label. |
| `helperText` | `string` | — | Supporting text (`aria-describedby`). |
| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |

## Behavior

Reference combobox/listbox behavior plus a helper message below the field.

## Accessibility

Helper text is linked to the trigger via `aria-describedby` and announced by screen readers.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Pair with `select-with-error` / `select-with-success` when validation feedback is needed.
