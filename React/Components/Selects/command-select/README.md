# Command Select

Command-palette-style select with search over grouped options.

## Usage

```tsx
import { CommandSelect } from './code';

<CommandSelect label="Command" groups={[{label:"Environments",options:[...]}]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { CommandSelect } from './code';

<CommandSelect label="Command" groups={[{label:"Environments",options:[...]}]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `groups` | `{label:string; options:{value,label,disabled?}[]}[]` | — | Grouped options. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `searchPlaceholder` / `label` | — | — | Standard. |

## Behavior

Search input + grouped options. Typing filters across all groups (empty groups hidden). ArrowDown/Up moves active among flattened filtered options (skipping group labels); Enter selects; Escape closes. Restrained elevation — no giant glow.

## Accessibility

Combobox + listbox; group labels are `role="presentation"` dividers.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Keep the visual treatment consistent with DevSnips — elevated panel + border, no command-palette glow effects.
