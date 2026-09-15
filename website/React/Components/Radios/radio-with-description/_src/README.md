# Radio With Description

Radio with a strong label plus a supporting description wired via aria-describedby.

## Usage

```tsx
<RadioWithDescription label="Team workspace" description="Shared with your organization." name="workspace" value="team" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioWithDescription label="Team workspace" description="Shared with your organization." name="workspace" value="team" defaultChecked />
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
| `description` | `ReactNode` (required) | — | Supporting description linked with `aria-describedby`. |

## States

Native radio with a bold label and a description block stacked beneath it. The description is linked with `aria-describedby`. The control is top-aligned so the circle lines up with the label.

## Accessibility

`<label htmlFor>` + `aria-describedby={descId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when the option needs more than a one-line label to be understood — e.g. a plan or workspace choice where the effect needs a sentence of explanation.
