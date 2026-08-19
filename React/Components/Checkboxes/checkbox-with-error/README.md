# Checkbox With Error

Checkbox with an associated validation message; sets aria-invalid and links the error via aria-describedby.

## Usage

```tsx
<CheckboxWithError label="I accept the terms" error="You must accept the terms to continue." />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<CheckboxWithError label="I accept the terms" error="You must accept the terms to continue." />
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
| `error` | `string` | — | Error message (sets `aria-invalid`, destructive styling, `role="alert"`). |
| `helperText` | `ReactNode` | — | Shown when no error is present. |

## States

Native checkbox with an optional error message. When `error` is set the input gets `aria-invalid="true"`, the border + check take the destructive token, and the message is rendered with `role="alert"` and `aria-describedby`. The failure is communicated by border, check color, and text — not color alone.

## Accessibility

`aria-invalid="true"` + `aria-describedby={messageId}` on the native input; error paragraph carries `role="alert"`. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

The error state never relies on color alone — the border, the check, and the message all change. Swap `error` for `helperText` to return to a neutral helper.
