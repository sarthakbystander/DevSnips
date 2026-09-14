# Checkbox Card Group

Group of selectable card checkboxes in a fieldset/legend with a shared value array.

## Usage

```tsx
<CheckboxCardGroup legend="Workspace features" options={[{value:"sso",label:"SSO",description:"Single sign-on"},{value:"audit",label:"Audit log"}]} defaultValue={["sso"]} columns={2} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<CheckboxCardGroup legend="Workspace features" options={[{value:"sso",label:"SSO",description:"Single sign-on"},{value:"audit",label:"Audit log"}]} defaultValue={["sso"]} columns={2} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `legend` | `ReactNode` (required) | — | Group label in `<legend>`. |
| `options` | `{value,label,description?,disabled?}[]` (required) | — | Card options. |
| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled selected values. |
| `onChange` | `(value[], event) => void` | — | Change callback. |
| `columns` | `1 \| 2 \| 3` | `1` | Grid columns at the `sm` breakpoint and up. |
| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |

## States

A group of selectable card checkboxes inside a `<fieldset>`/`<legend>`. Maintains a value array of selected option values; controlled and uncontrolled modes both supported. Each card is a clickable `<label>` wrapping a real `<input type="checkbox">`. The grid collapses to a single column below the `sm` breakpoint.

## Accessibility

`<fieldset>` + `<legend>`. Each card is a `<label htmlFor>` wrapping a native input; descriptions linked with `aria-describedby`; `aria-invalid` + `role="alert"` error. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when each option needs the visual weight of a card and multiple selections are allowed. For an exclusive single choice use `radio-card-group`.
