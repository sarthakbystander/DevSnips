# Select Readonly

Custom select in a read-only state: value locked but readable, not greyed-out.

## Usage

```tsx
import { SelectReadonly } from './code';

<SelectReadonly label="Environment" options={opts} readOnly defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectReadonly } from './code';

<SelectReadonly label="Environment" options={opts} readOnly defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `readOnly` | `boolean` | `true` | Renders a static, non-editable display. |
| `label` / `options` / `value` / `defaultValue` / `size` | — | — | As reference. |

## Behavior

When `readOnly`, the value renders as a static, non-interactive display (not a button) — readable but not changeable. Distinct from `disabled`: not greyed-out, just locked. Falls back to the interactive trigger when `readOnly={false}`.

## Accessibility

Static display uses `role="textbox" aria-readonly="true"` so screen readers announce a read-only value. A lock affordance signals the state non-color-wise.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use for values a user can see but not edit (e.g. an inherited environment). For editable-but-currently-locked, see `inline-edit-select`.
