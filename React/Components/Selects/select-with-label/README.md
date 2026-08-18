# Select With Label

Custom select with an always-rendered associated label.

## Usage

```tsx
import { SelectWithLabel } from './code';

<SelectWithLabel label="Project" options={[{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"}]} defaultValue="devsnips" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithLabel } from './code';

<SelectWithLabel label="Project" options={[{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"}]} defaultValue="devsnips" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | `"Field"` | Visible label (always rendered). |
| `options` | `{value,label,disabled?}[]` | — | Option list. |
| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled. |
| `onChange` | `(value, option) => void` | — | Selection callback. |
| `size` / `placeholder` / `id` / `name` / `className` | — | — | Standard. |

## Behavior

Same combobox/listbox behavior as the reference `Select`: click/ArrowDown opens, ArrowUp/Down/Home/End navigate, Enter/Space selects, Escape closes.

## Accessibility

`<label htmlFor>` pairs the visible label with the trigger. Full ARIA listbox pattern.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use when the label is the primary structural emphasis and must always be present.
