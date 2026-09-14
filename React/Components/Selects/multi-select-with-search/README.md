# Multi Select With Search

Multi-select combined with a search filter over the options.

## Usage

```tsx
import { MultiSelectWithSearch } from './code';

<MultiSelectWithSearch label="Members" options={opts} defaultValue={["sarthak"]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { MultiSelectWithSearch } from './code';

<MultiSelectWithSearch label="Members" options={opts} defaultValue={["sarthak"]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,disabled?}[]` | — | Option list. |
| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled. |
| `onChange` | `(values, options) => void` | — | Selection callback. |
| `searchPlaceholder` / `placeholder` / `size` / `label` | — | — | Standard. |

## Behavior

Trigger shows a count summary. Panel has a search input + filtered checkbox options. Typing filters; ArrowDown/Up moves active among filtered; Enter/Space toggles (panel stays open); Escape closes and clears the search. Empty-results state included.

## Accessibility

Combobox + listbox + `role="option" aria-selected` pattern. Focus remains predictable: the search input is the panel's primary focus.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use when selecting multiple items from a large list (e.g. assigning many team members).
