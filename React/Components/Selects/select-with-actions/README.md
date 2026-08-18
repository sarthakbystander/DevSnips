# Select With Actions

Custom select whose dropdown panel has action rows (e.g. Add new, Manage).

## Usage

```tsx
import { SelectWithActions } from './code';

<SelectWithActions label="Project" options={opts} actions={[{label:"Add new\u2026",onSelect:()=>{}}]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithActions } from './code';

<SelectWithActions label="Project" options={opts} actions={[{label:"Add new\u2026",onSelect:()=>{}}]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `actions` | `{label:string; onSelect:()=>void}[]` | — | Footer action rows. |
| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

The dropdown panel renders options above a divider (`border-t`) and action buttons below. Selecting an action calls `onSelect` and closes the panel. Options use full listbox keyboard nav; actions are separate focusable buttons.

## Accessibility

Actions are real `<button>` elements with descriptive labels, reachable by keyboard.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use for selects that need quick inline actions (create a new option, manage the list).
