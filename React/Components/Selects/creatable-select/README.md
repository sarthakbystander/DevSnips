# Creatable Select

Combobox that lets users create a new option when no match exists.

## Usage

```tsx
import { CreatableSelect } from './code';

<CreatableSelect label="Label" options={opts} onCreateOption={(v)=>{}} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { CreatableSelect } from './code';

<CreatableSelect label="Label" options={opts} onCreateOption={(v)=>{}} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,disabled?}[]` | — | Existing options. |
| `onCreateOption` | `(value: string) => void` | — | Called when a new option is created. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `searchPlaceholder` / `createLabel` | — | — | Standard. |

## Behavior

Type to filter. When the query is non-empty and no exact-match option exists, a `Create "<query>"` row appears at the top. Selecting it calls `onCreateOption(query)`, appends the new option to the list, and selects it. ArrowDown/Up navigates, Enter creates/selects, Escape closes+clears.

## Accessibility

Combobox + listbox pattern; the create row is `role="option"` with a descriptive label.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Implement real persistence in `onCreateOption` (e.g. POST to your API). The preview appends to local state for demonstration.
