# Select With Success

Custom select with a success message and confirmation state.

## Usage

```tsx
import { SelectWithSuccess } from './code';

<SelectWithSuccess label="Environment" success="Deploy target verified." options={opts} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithSuccess } from './code';

<SelectWithSuccess label="Environment" success="Deploy target verified." options={opts} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | `"Select"` | Visible label. |
| `success` | `string` | — | Success message; sets success border. |
| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |

## Behavior

Reference combobox/listbox behavior with a success border + confirmation message.

## Accessibility

Success message linked via `aria-describedby`. State uses border + text + check indicator, not color alone.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use to confirm a valid selection (e.g. a verified deploy target).
