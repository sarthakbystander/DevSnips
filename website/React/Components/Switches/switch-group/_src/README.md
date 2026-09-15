# Switch Group

Group of related independent on/off settings in a fieldset/legend with a shared value array.

## Usage

```tsx
<SwitchGroup legend="Notification preferences" options={[{value:"email",label:"Email notifications"},{value:"desktop",label:"Desktop notifications"},{value:"security",label:"Security alerts"}]} defaultValue={["email","security"]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchGroup legend="Notification preferences" options={[{value:"email",label:"Email notifications"},{value:"desktop",label:"Desktop notifications"},{value:"security",label:"Security alerts"}]} defaultValue={["email","security"]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |
| `options` | `{value,label,disabled?,description?}[]` (required) | — | Option list. |
| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled set of options that are on. |
| `onChange` | `(value[], event) => void` | — | Change callback. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | Layout. |
| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |

## States

A group of related, independent on/off settings inside a `<fieldset>`/`<legend>`. Maintains a value array of the options that are on; each switch stays independently controllable (this is not a radio group). Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes are both supported.

## Accessibility

`<fieldset>` + `<legend>` group labeling. Each native `<input type="checkbox" role="switch">` is wrapped in a `<label htmlFor>`; per-option descriptions are linked with `aria-describedby`. `aria-invalid` + `role="alert"` error message. Visible `focus-visible` ring on each control.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this for a set of independent binary settings (Email / Desktop / Security alerts). For an exclusive single choice use a radio group; for one card per setting use `switch-card-group`.
