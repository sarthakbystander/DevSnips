# Switch With Description

Switch with a strong label plus a supporting description wired via aria-describedby.

## Usage

```tsx
<SwitchWithDescription label="Two-factor authentication" description="Require a second factor at sign-in." defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchWithDescription label="Two-factor authentication" description="Require a second factor at sign-in." defaultChecked />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` / `value` | `string` | — | Native form name/value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |
| `description` | `ReactNode` (required) | — | Supporting description linked with `aria-describedby`. |

## States

Native switch with a bold label and a description block stacked beneath it. The description is linked with `aria-describedby`. The control is top-aligned so the track lines up with the label.

## Accessibility

`<label htmlFor>` + `aria-describedby={descId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when the setting needs more than a one-line label to be understood — e.g. a security control whose effect needs a sentence of explanation.
