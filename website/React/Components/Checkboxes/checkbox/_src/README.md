# Checkbox

Native checkbox styled to the DevSnips select/input visual language with controlled and uncontrolled modes.

## Usage

```tsx
<Checkbox label="Email notifications" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<Checkbox label="Email notifications" defaultChecked />
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

## States

A native `<input type="checkbox">` styled with Tailwind + the `--ds-*` semantic tokens. The check glyph is a sibling element whose opacity tracks the tracked `isChecked` state. Controlled (`checked`/`onChange`) and uncontrolled (`defaultChecked`) modes are both supported; `readOnly` blocks toggling via `preventDefault`.

## Accessibility

Real `<input type="checkbox">` element — full native keyboard (Space toggles), `aria-invalid` for errors, `aria-describedby` for associated text, visible `focus-visible` ring from `--ds-color-focus-ring`. When a label is provided it is wrapped in a `<label htmlFor>` so the text is a click target.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

This is the reference implementation for the Checkboxes family — it establishes the shared 18px control size, `radius-xs`, border, focus ring, checked/disabled/error states, and dark-mode behavior that every other checkbox extends.
