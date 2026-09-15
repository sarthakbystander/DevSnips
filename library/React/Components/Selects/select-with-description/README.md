# Select With Description

Custom single-select where options carry a label and a description.

## Usage

```tsx
import { SelectWithDescription } from './code';

<SelectWithDescription label="Environment" options={[{value:"production",label:"Production",description:"Live production environment"}]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithDescription } from './code';

<SelectWithDescription label="Environment" options={[{value:"production",label:"Production",description:"Live production environment"}]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,description?,disabled?}[]` | — | Options with descriptions. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

Option rows show a label (medium) + description (muted `text-xs`). Rows stay compact. Selected option shows a check on the right. Full keyboard nav.

## Accessibility

Options are `role="option" aria-selected`; description text is readable by screen readers.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Keep option rows compact — do not make them unnecessarily tall.
