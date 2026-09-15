# Select With Loading

Custom select that shows a loading state with aria-busy while options load.

## Usage

```tsx
import { SelectWithLoading } from './code';

<SelectWithLoading label="Environment" options={opts} loading />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithLoading } from './code';

<SelectWithLoading label="Environment" options={opts} loading />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `loading` | `boolean` | — | Shows a spinner + disables interaction (`aria-busy`). |
| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

While `loading` is true, the trigger is non-interactive (`pointer-events-none`), shows `aria-busy="true"`, and a Spinner replaces the chevron. When loading completes, full listbox behavior resumes.

## Accessibility

`aria-busy="true"` announces the loading state to assistive technology.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

For asynchronous option fetching, see `async-select` which wraps this loading state around a `loadOptions` callback.
