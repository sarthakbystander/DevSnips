# Select Disabled

Custom select demonstrating the disabled, non-interactive state.

## Usage

```tsx
import { SelectDisabled } from './code';

<SelectDisabled label="Environment" options={opts} disabled defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectDisabled } from './code';

<SelectDisabled label="Environment" options={opts} disabled defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `disabled` | `boolean` | `true` | Disables the trigger. |
| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |

## Behavior

When `disabled`, the trigger is non-interactive (`pointer-events-none`, muted surface, reduced opacity). ARIA is preserved so the control remains perceivable.

## Accessibility

`disabled` on the trigger; `aria-disabled` reflected. Disabled state uses opacity + muted surface, not just color.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Defaults to `disabled` to showcase the state; pass `disabled={false}` to make it interactive.
