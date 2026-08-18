# Select With Groups

Custom single-select with grouped options and accessible group dividers.

## Usage

```tsx
import { SelectWithGroups } from './code';

<SelectWithGroups label="Resource" groups={[{label:"Fruits",options:[...]},{label:"Vegetables",options:[...]}]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithGroups } from './code';

<SelectWithGroups label="Resource" groups={[{label:"Fruits",options:[...]},{label:"Vegetables",options:[...]}]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `groups` | `{label:string; options:{value,label,disabled?}[]}[]` | — | Grouped options. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

Group labels render as non-interactive dividers. Keyboard navigation skips group labels — only options are navigable for `activeIndex`. Selected option shows a check.

## Accessibility

Group labels are `role="presentation"` dividers (muted uppercase). Options are `role="option" aria-selected`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Groups are visually distinguished by the muted divider, not excessive decoration.
