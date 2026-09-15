# Radio

Native radio styled to the DevSnips select/input visual language with controlled and uncontrolled modes.

## Usage

```tsx
<Radio label="Production" name="env" value="production" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<Radio label="Production" name="env" value="production" defaultChecked />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` | `string` | — | Shared group name (groups radios). |
| `value` | `string \| number \| readonly string[]` (required) | — | Native form value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |

## States

A native `<input type="radio">` styled with Tailwind + the `--ds-*` semantic tokens. The selected dot is a sibling element whose opacity tracks the tracked `isChecked` state. Controlled (`checked`/`onChange`) and uncontrolled (`defaultChecked`) modes are both supported.

## Accessibility

Real `<input type="radio">` element — full native keyboard (Arrow keys move within a named group, Space + select), `aria-invalid` for errors, `aria-describedby` for associated text, visible `focus-visible` ring from `--ds-color-focus-ring`. When a label is provided it is wrapped in a `<label htmlFor>`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

This is the reference implementation for the Radios family — it establishes the shared 18px control size, full-round radius, border, focus ring, selected/disabled/error states, and dark-mode behavior that every other radio extends.
