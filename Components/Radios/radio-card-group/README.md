# Radio Card Group

Group of selectable card radios in a fieldset/legend; only one may be selected.

## Usage

```tsx
<RadioCardGroup legend="Workspace plan" options={[{value:"personal",label:"Personal"},{value:"team",label:"Team"}]} defaultValue="team" columns={3} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioCardGroup legend="Workspace plan" options={[{value:"personal",label:"Personal"},{value:"team",label:"Team"}]} defaultValue="team" columns={3} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `legend` | `ReactNode` (required) | — | Group label in `<legend>`. |
| `options` | `{value,label,description?,disabled?}[]` (required) | — | Card options. |
| `value` / `defaultValue` | `string` | `""` | Controlled / uncontrolled selected value. |
| `onChange` | `(value, event) => void` | — | Selection callback. |
| `columns` | `1 \| 2 \| 3` | `1` | Grid columns at the `sm` breakpoint and up. |
| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |

## States

A group of selectable card radios inside a `<fieldset>`/`<legend>`. Only one card may be selected. Controlled and uncontrolled modes both supported. Each card is a clickable `<label>` wrapping a real `<input type="radio">`. The grid collapses to a single column below the `sm` breakpoint.

## Accessibility

`<fieldset>` + `<legend>`. Each card is a `<label htmlFor>` wrapping a native radio; descriptions linked with `aria-describedby`; `aria-invalid` + `role="alert"` error. Visible `focus-visible` ring; arrow keys navigate natively within the named group.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when each option needs the visual weight of a card and exactly one selection is allowed. For multiple selections use `checkbox-card-group`.
