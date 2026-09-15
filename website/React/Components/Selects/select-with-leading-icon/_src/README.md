# Select With Leading Icon

Custom select with a meaningful leading icon inside the trigger.

## Usage

```tsx
import { SelectWithLeadingIcon } from './code';

<SelectWithLeadingIcon label="Repository" leadingIcon={<SearchIcon/>} options={opts} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithLeadingIcon } from './code';

<SelectWithLeadingIcon label="Repository" leadingIcon={<SearchIcon/>} options={opts} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `leadingIcon` | `ReactNode` | — | Icon rendered at the trigger left. |
| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |

## Behavior

Reference combobox/listbox behavior. The leading icon is decorative (`aria-hidden`) and shifts the trigger content with `pl-9`.

## Accessibility

Leading icon is `aria-hidden`; the trigger remains fully labeled and keyboard-operable.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use a leading icon only when it adds meaning (e.g. a search icon for a filterable context). Avoid decorative icons.
