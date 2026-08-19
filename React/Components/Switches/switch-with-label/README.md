# Switch With Label

Switch with a visibly-associated label wrapped in a clickable label element.

## Usage

```tsx
<SwitchWithLabel label="Email notifications" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchWithLabel label="Email notifications" defaultChecked />
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

## States

Same native switch as the reference, but `label` is required and always wrapped in a `<label htmlFor>`, so clicking anywhere on the text toggles the control. Renders a `*` when `required`.

## Accessibility

Native `<input type="checkbox" role="switch">` + `<label htmlFor>` association. `aria-invalid` for errors, `aria-describedby` for external helper/error text, visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when you only need a label and no helper or description. Reach for `switch-with-helper` or `switch-with-description` when extra context is needed.
