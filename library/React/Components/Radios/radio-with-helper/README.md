# Radio With Helper

Radio with a visible label plus helper text wired via aria-describedby.

## Usage

```tsx
<RadioWithHelper label="Production" helperText="Live traffic, real customers." name="env" value="production" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioWithHelper label="Production" helperText="Live traffic, real customers." name="env" value="production" defaultChecked />
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
| `helperText` | `ReactNode` (required) | — | Supporting text linked with `aria-describedby`. |

## States

Native radio + a label and a helper paragraph. The helper is linked to the input with `aria-describedby` so assistive tech announces it after the label. The helper is indented to align with the label text.

## Accessibility

`<label htmlFor>` + `aria-describedby={helperId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when a label alone is not enough and a short helper line gives useful context. For validation messaging use `radio-with-error`.
