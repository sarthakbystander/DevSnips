# Checkbox Disabled

Checkbox variant focused on the disabled non-interactive state.

## Usage

```tsx
<CheckboxDisabled label="Inherited from team" checked defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<CheckboxDisabled label="Inherited from team" checked defaultChecked />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `readOnly` | `boolean` | — | Read-only (blocks toggling). |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` / `value` | `string` | — | Native form name/value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |
| `helperText` | `ReactNode` | — | Helper text (still readable when disabled). |
| `disabled` | `boolean` | `true` | Defaults to disabled. |

## States

Native checkbox with `disabled` set (defaults to `true`). The visual treatment uses reduced opacity + muted foreground so the control stays perceivable without looking interactive. Native disabled semantics are preserved (excluded from form submission, not focusable).

## Accessibility

Native `disabled` attribute carries the semantics. Helper text stays associated via `aria-describedby`. Reduced opacity + muted color keeps it perceivable.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use `checkbox-disabled` for options that exist but cannot be changed in this context (e.g. a permission inherited from a team plan). For a value that is fixed but should still be focusable, use `checkbox-readonly`.
