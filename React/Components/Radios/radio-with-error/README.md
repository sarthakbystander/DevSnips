# Radio With Error

Radio with an associated validation message; sets aria-invalid and links the error via aria-describedby.

## Usage

```tsx
<RadioWithError label="Production" error="Production is currently unavailable." name="env" value="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioWithError label="Production" error="Production is currently unavailable." name="env" value="production" />
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
| `error` | `string` | — | Error message (sets `aria-invalid`, destructive styling, `role="alert"`). |
| `helperText` | `ReactNode` | — | Shown when no error is present. |

## States

Native radio with an optional error message. When `error` is set the input gets `aria-invalid="true"`, the border + dot take the destructive token, and the message is rendered with `role="alert"` and `aria-describedby`. The failure is communicated by border, dot, and text — not color alone.

## Accessibility

`aria-invalid="true"` + `aria-describedby={messageId}` on the native input; error paragraph carries `role="alert"`. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

The error state never relies on color alone — the border, the dot, and the message all change. Swap `error` for `helperText` to return to a neutral helper.
