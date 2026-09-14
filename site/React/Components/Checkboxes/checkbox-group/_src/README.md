# Checkbox Group

Group of related checkboxes in a fieldset/legend with a shared value array.

## Usage

```tsx
<CheckboxGroup legend="Notification preferences" options={[{value:"email",label:"Email"},{value:"push",label:"Push"},{value:"sms",label:"SMS",disabled:true}]} defaultValue={["email"]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<CheckboxGroup legend="Notification preferences" options={[{value:"email",label:"Email"},{value:"push",label:"Push"},{value:"sms",label:"SMS",disabled:true}]} defaultValue={["email"]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |
| `options` | `{value,label,disabled?,description?}[]` (required) | — | Option list. |
| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled selected values. |
| `onChange` | `(value[], event) => void` | — | Change callback. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | Layout. |
| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |

## States

A group of related checkboxes inside a `<fieldset>`/`<legend>`. Maintains a value array of selected option values. Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes are both supported. Each option is a native `<input type="checkbox">` sharing a `name`.

## Accessibility

`<fieldset>` + `<legend>` group labeling. Each native input is wrapped in a `<label htmlFor>`; per-option descriptions are linked with `aria-describedby`. `aria-invalid` + `role="alert"` error message. Visible `focus-visible` ring on each control.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this for a set of independent on/off choices. For an exclusive single choice use `radio-group`. For a master toggle with select-all use `checkbox-with-select-all`.
