# Native Select

Genuine native select element styled to match the DevSnips select language.

## Usage

```tsx
import { NativeSelect } from './code';

<NativeSelect label="Environment" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { NativeSelect } from './code';

<NativeSelect label="Environment" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | `"Select"` | Visible label. |
| `options` | `{value,label,disabled?}[]` | — | Option list. |
| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled value. |
| `onChange` | `(value, option) => void` | — | Selection callback. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Control height. |
| `placeholder` | `string` | `"Select an option"` | First disabled option. |
| `disabled` | `boolean` | — | Disables the select. |
| native `<select>` attrs | — | — | `name`, `id`, `aria-*`. |

## Behavior

Uses the browser's native `<select>` for full native behavior (form submission, mobile picker, platform conventions). A chevron overlay is positioned over the native control to match the custom select visual language.

## Accessibility

Native `<select>` + `<option>` elements are accessible by default. A visible `<label htmlFor>` associates the field; `aria-invalid` and `aria-describedby` wire error/helper text.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use native-select when you need native form semantics and platform pickers (especially mobile). Use the custom `select` when you need custom interaction or styling the native control cannot provide.
