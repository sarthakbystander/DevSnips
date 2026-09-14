# Searchable Select

Combobox select with a real search input that filters options.

## Usage

```tsx
import { SearchableSelect } from './code';

<SearchableSelect label="Environment" options={opts} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SearchableSelect } from './code';

<SearchableSelect label="Environment" options={opts} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,disabled?}[]` | — | Option list. |
| `value` / `defaultValue` / `onChange` | — | — | Controlled / uncontrolled. |
| `searchPlaceholder` | `string` | `"Search options"` | Input placeholder. |
| `placeholder` / `size` / `label` / `id` / `name` / `className` | — | — | Standard. |

## Behavior

Trigger opens a panel with a search input (autofocused) above a filtered listbox. Typing filters options by label (case-insensitive substring). ArrowDown/Up moves the active option among filtered results, Home/End jump, Enter selects, Escape closes and clears the search. An empty-results state shows "No matches".

## Accessibility

Search input is `role="combobox" aria-expanded aria-controls aria-activedescendant aria-autocomplete="list"`; listbox `role="listbox"`; options `role="option" aria-selected`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use when the option list is long enough that filtering helps. For free-text input see `combobox`; for multiple selection with search see `multi-select-with-search`.
