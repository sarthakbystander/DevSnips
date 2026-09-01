# Switch Card Group

Group of settings cards in a fieldset/legend, each with an independently-controlled switch.

## Usage

```tsx
<SwitchCardGroup legend="Privacy" columns={2} options={[{value:"analytics",label:"Analytics",description:"Share anonymous usage data."},{value:"public",label:"Public profile",description:"Visible outside the workspace."}]} defaultValue={["analytics"]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchCardGroup legend="Privacy" columns={2} options={[{value:"analytics",label:"Analytics",description:"Share anonymous usage data."},{value:"public",label:"Public profile",description:"Visible outside the workspace."}]} defaultValue={["analytics"]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |
| `options` | `{value,label,description?,disabled?}[]` (required) | — | Option list. |
| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled set of options that are on. |
| `onChange` | `(value[], event) => void` | — | Change callback. |
| `columns` | `1 \| 2` | `1` | Card columns at the `sm` breakpoint. |
| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |

## States

A group of settings cards inside a `<fieldset>`/`<legend>`. Maintains a value array of the options that are on; each card's switch stays independently controllable. Controlled and uncontrolled modes both supported. `columns={2}` collapses to a single column below the `sm` breakpoint.

## Accessibility

`<fieldset>` + `<legend>` group labeling; each card is a `<label htmlFor>` wrapping a real native input. Per-option descriptions linked with `aria-describedby`; `aria-invalid` + `role="alert"` error message; visible `focus-visible` ring per control.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this for a small set of heavyweight settings that each need a sentence of context (privacy, backups, integrations). For lightweight inline settings use `switch-group`.
