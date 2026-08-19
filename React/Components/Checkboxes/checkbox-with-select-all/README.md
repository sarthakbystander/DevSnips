# Checkbox With Select All

Checkbox group with a real select-all control that reflects checked/indeterminate/unchecked child state.

## Usage

```tsx
<CheckboxWithSelectAll legend="Permissions" options={[{value:"read",label:"Read"},{value:"write",label:"Write"}]} defaultValue={["read"]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<CheckboxWithSelectAll legend="Permissions" options={[{value:"read",label:"Read"},{value:"write",label:"Write"}]} defaultValue={["read"]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `legend` | `ReactNode` (required) | — | Group label in `<legend>`. |
| `options` | `{value,label,disabled?,description?}[]` (required) | — | Child options. |
| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled selected values. |
| `onChange` | `(value[], event) => void` | — | Change callback. |
| `selectAllLabel` | `ReactNode` | `"Select all"` | Master control label. |
| `disabled` / `required` / `name` / `id` | — | — | Standard field props. |

## States

A checkbox group with a REAL select-all control. The master checkbox reflects the children's state: checked when all (enabled) children are selected, indeterminate when some are selected, unchecked when none. Toggling it selects/deselects every enabled child. The master's `.indeterminate` IDL property is set imperatively on the DOM node.

## Accessibility

`<fieldset>` + `<legend>`. Master + children are all native `<input type="checkbox">` sharing a `name`; per-option descriptions linked with `aria-describedby`. Visible `focus-visible` ring. The indeterminate state is set on the DOM node (no HTML attribute exists).

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

This composes the `checkbox-indeterminate` primitive into a real select-all pattern. Disabled children are excluded from the all/none calculation but keep their existing selection state.
