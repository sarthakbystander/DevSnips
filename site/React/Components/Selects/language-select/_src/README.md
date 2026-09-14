# Language Select

Single-select listbox for languages with an optional native name.

## Usage

```tsx
import { LanguageSelect } from './code';

<LanguageSelect label="Language" options={[{value:"en",label:"English",nativeName:"English"}]} defaultValue="en" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { LanguageSelect } from './code';

<LanguageSelect label="Language" options={[{value:"en",label:"English",nativeName:"English"}]} defaultValue="en" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,nativeName?,disabled?}[]` | — | Languages. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

Option rows + trigger show the label with the optional native name in muted text beside it. Full keyboard nav + ARIA listbox + outside-click + selected check.

## Accessibility

Native name is decorative; the label carries the accessible name.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Works for both programming languages (TypeScript/Python) and human languages (English, Chinese).
