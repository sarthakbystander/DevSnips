# Combobox

True WAI-ARIA combobox: a text input that filters and selects from a listbox.

## Usage

```tsx
import { Combobox } from './code';

<Combobox label="Environment" options={opts} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { Combobox } from './code';

<Combobox label="Environment" options={opts} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label}[]` | — | Option list. |
| `value` / `defaultValue` / `onChange` | — | — | Controlled / uncontrolled (value = selected value). |
| `onInputChange` | `(query: string) => void` | — | Input change callback. |
| `size` / `placeholder` / `label` / `id` / `name` / `className` | — | — | Standard. |

## Behavior

The text INPUT is the trigger (`role="combobox" aria-autocomplete="list"`). Typing filters the listbox below. ArrowDown opens + moves the active option, Enter selects (sets the input to the option label), Escape closes. Distinct from `searchable-select`: here the input itself is the trigger, not a button that opens a panel with a search box.

## Accessibility

Input `role="combobox" aria-expanded aria-controls aria-activedescendant aria-autocomplete="list"`; listbox `role="listbox"`; options `role="option" aria-selected`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use when the user may type a free value OR pick from the list. For pick-only with search, see `searchable-select`.
