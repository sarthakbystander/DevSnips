# Country Select

Single-select listbox for countries with a 2-letter ISO code badge (no emoji flags).

## Usage

```tsx
import { CountrySelect } from './code';

<CountrySelect label="Country" options={[{value:"US",label:"United States",code:"US"}]} defaultValue="US" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { CountrySelect } from './code';

<CountrySelect label="Country" options={[{value:"US",label:"United States",code:"US"}]} defaultValue="US" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,code:string,disabled?}[]` | — | Countries with 2-letter ISO code. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

Each option shows a small square 2-letter code badge (`font-mono text-[10px]`) + label. The trigger shows the selected country's badge + label. Full keyboard nav + ARIA listbox + outside-click.

## Accessibility

Code badge is `aria-hidden`; the option label carries the accessible name.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Uses a code-badge instead of emoji flags for a restrained, consistent look across platforms.
