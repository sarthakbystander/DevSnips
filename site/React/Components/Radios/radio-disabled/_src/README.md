# Radio Disabled

Radio variant focused on the disabled non-interactive state.

## Usage

```tsx
<RadioDisabled label="Enterprise (requires upgrade)" name="plan" value="enterprise" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioDisabled label="Enterprise (requires upgrade)" name="plan" value="enterprise" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` | `string` | — | Shared group name (groups radios). |
| `value` | `string \| number \| readonly string[]` (required) | — | Native form value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |
| `helperText` | `ReactNode` | — | Helper text (still readable when disabled). |
| `disabled` | `boolean` | `true` | Defaults to disabled. |

## States

Native radio with `disabled` set (defaults to `true`). The visual treatment uses reduced opacity + muted foreground so the control stays perceivable without looking interactive. Native disabled semantics are preserved (excluded from form submission, not focusable).

## Accessibility

Native `disabled` attribute carries the semantics. Helper text stays associated via `aria-describedby`. Reduced opacity + muted color keeps it perceivable.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use `radio-disabled` for options that exist but cannot be chosen in this context (e.g. a plan that requires an upgrade).
