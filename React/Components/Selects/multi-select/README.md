# Multi Select

Custom listbox supporting multiple selections with restrained count summary.

## Usage

```tsx
import { MultiSelect } from './code';

<MultiSelect label="Tags" options={opts} defaultValue={["backend"]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { MultiSelect } from './code';

<MultiSelect label="Tags" options={opts} defaultValue={["backend"]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,disabled?}[]` | — | Option list. |
| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled values. |
| `onChange` | `(values: string[], options) => void` | — | Selection callback. |
| `placeholder` / `size` / `label` / `id` / `name` / `className` | — | — | Standard. |

## Behavior

Trigger shows a restrained summary (0 → placeholder, 1-2 → labels joined by ", ", 3+ → "N selected"). Clicking/Enter/Space toggles an option's selection WITHOUT closing the panel (multi stays open). ArrowUp/Down/Home/End navigate; Escape closes.

## Accessibility

Options are `role="option" aria-selected`; selected options use a checked indicator + `surface-selected` background + `font-medium`, not color alone.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Avoid turning selected values into a pile of pill badges — the count summary keeps the trigger restrained.
