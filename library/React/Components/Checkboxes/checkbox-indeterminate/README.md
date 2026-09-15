# Checkbox Indeterminate

Real indeterminate checkbox that sets the HTMLInputElement.indeterminate property imperatively.

## Usage

```tsx
<CheckboxIndeterminate label="Notifications" indeterminate />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<CheckboxIndeterminate label="Notifications" indeterminate />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `readOnly` | `boolean` | — | Read-only (blocks toggling). |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` / `value` | `string` | — | Native form name/value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |
| `indeterminate` | `boolean` | `false` | Sets the native `.indeterminate` IDL property (imperative). Renders a dash indicator. |

## States

A REAL indeterminate checkbox. The underlying `HTMLInputElement.indeterminate` property is set imperatively on the DOM node (there is no HTML attribute for it) via an effect that runs whenever `indeterminate` changes. The indeterminate indicator is a horizontal dash, distinct from the checked check mark. `checked` and `indeterminate` are independent.

## Accessibility

Native `<input type="checkbox">` with the `.indeterminate` IDL property set on the DOM node. Keyboard behavior is native. `aria-invalid` when `invalid`, visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

This is the primitive behind `checkbox-with-select-all`. Browsers have no HTML attribute for indeterminate — it must be set in JS on the DOM node, which is why an effect + ref is used rather than a prop-to-attribute mapping.
