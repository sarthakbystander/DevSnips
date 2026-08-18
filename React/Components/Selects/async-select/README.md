# Async Select

Custom select that loads options asynchronously via a loadOptions callback.

## Usage

```tsx
import { AsyncSelect } from './code';

<AsyncSelect label="Repository" loadOptions={(q)=>Promise.resolve(opts)} defaultOptions />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { AsyncSelect } from './code';

<AsyncSelect label="Repository" loadOptions={(q)=>Promise.resolve(opts)} defaultOptions />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `loadOptions` | `(query: string) => Promise<{value,label,disabled?}[]>` | — | Async loader. |
| `defaultOptions` | `{value,label}[] \| boolean` | — | Initial options or `true` to load on mount. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |
| `loadingPlaceholder` / `emptyMessage` | `string` | — | Loading + empty copy. |

## Behavior

On open (or mount when `defaultOptions === true`), calls `loadOptions(query)`. Shows a loading spinner (`aria-busy`) while pending, then results. If the promise rejects, shows an error state inside the panel. Empty state when no results. The component performs NO real network requests — it calls the consumer's `loadOptions`.

## Accessibility

`aria-busy="true"` during load; loading/empty/error states are text-announced.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

The preview simulates async loading with a `setTimeout`-wrapped promise. Wire `loadOptions` to your real data source in production.
