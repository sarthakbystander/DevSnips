# Radio Group

Radio group where only one option may be selected, in a fieldset/legend.

## Usage

```tsx
<RadioGroup legend="Deploy target" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="staging" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioGroup legend="Deploy target" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="staging" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |
| `options` | `{value,label,disabled?,description?}[]` (required) | — | Option list. |
| `value` / `defaultValue` | `string` | `""` | Controlled / uncontrolled selected value. |
| `onChange` | `(value, event) => void` | — | Selection callback. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | Layout. |
| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |

## States

A radio group: only one option may be selected. Wraps native `<input type="radio">` elements sharing a `name` inside a `<fieldset>`/`<legend>`. Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes are both supported. Native arrow-key navigation moves within the named group.

## Accessibility

`<fieldset>` + `<legend>` group labeling. Each native input is wrapped in a `<label htmlFor>`; per-option descriptions are linked with `aria-describedby`. `aria-invalid` + `role="alert"` error message. Visible `focus-visible` ring; arrow keys navigate natively.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this for an exclusive single choice. For multiple independent choices use `checkbox-group`. For card-style options use `radio-card-group`.
