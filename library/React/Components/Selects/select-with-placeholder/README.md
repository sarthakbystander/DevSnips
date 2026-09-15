# Select With Placeholder

Custom select emphasizing a prominent placeholder when nothing is selected.

## Usage

```tsx
import { SelectWithPlaceholder } from './code';

<SelectWithPlaceholder label="Project" placeholder="Choose a project" options={opts} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithPlaceholder } from './code';

<SelectWithPlaceholder label="Project" placeholder="Choose a project" options={opts} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `placeholder` | `string` | `"Choose\u2026"` | Placeholder when no value. |
| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` | — | — | As reference. |

## Behavior

Reference combobox/listbox behavior. Placeholder shows in muted foreground until a selection is made.

## Accessibility

Placeholder is presentational; the field is labeled and keyboard-accessible.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Placeholders are never critical information — use them for guidance, not as a substitute for a label.
