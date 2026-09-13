# Timezone Select

Single-select listbox for timezones with a mono offset display.

## Usage

```tsx
import { TimezoneSelect } from './code';

<TimezoneSelect label="Timezone" options={[{value:"America/New_York",label:"New York",offset:"GMT-5"}]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { TimezoneSelect } from './code';

<TimezoneSelect label="Timezone" options={[{value:"America/New_York",label:"New York",offset:"GMT-5"}]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,offset?,disabled?}[]` | — | Timezones with optional offset. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

Option rows + trigger show the offset in `font-mono` muted foreground. Full keyboard nav + ARIA listbox + outside-click + selected check.

## Accessibility

Offset is decorative; the label carries the accessible name.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Pass IANA timezone identifiers as `value` for integrations with date libraries.
