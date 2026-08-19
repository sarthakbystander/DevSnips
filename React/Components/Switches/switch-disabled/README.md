# Switch Disabled

Switch variant focused on the disabled non-interactive state.

## Usage

```tsx
<SwitchDisabled label="Inherited from team plan" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchDisabled label="Inherited from team plan" defaultChecked />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label. |
| `helperText` | `ReactNode` | — | Helper text (still readable when disabled). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback (won't fire while disabled). |
| `disabled` | `boolean` | `true` | Defaults to disabled. |
| `name` / `value` / `id` | `string` | — | Native form attrs. |

## States

Native switch with `disabled` set (defaults to `true`). The visual treatment uses reduced opacity + muted foreground so the control stays perceivable without looking interactive. Native disabled semantics are preserved (excluded from form submission, not focusable, not clickable).

## Accessibility

Native `disabled` attribute carries the semantics. Helper text stays associated via `aria-describedby`. Reduced opacity + muted color keeps it perceivable without looking interactive.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use `switch-disabled` for settings that exist but cannot be changed in this context (e.g. a permission inherited from a team plan, or an option gated behind verification).
