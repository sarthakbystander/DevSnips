# Radio Card

Single selectable card wrapping a native radio; the whole card is a click target.

## Usage

```tsx
<RadioCard label="Team workspace" description="Shared with your organization." name="workspace" value="team" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioCard label="Team workspace" description="Shared with your organization." name="workspace" value="team" defaultChecked />
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
| `description` | `ReactNode` | — | Supporting description linked with `aria-describedby`. |

## States

A single selectable card wrapping a native radio. The entire card is a `<label htmlFor>` (clickable) while the real `<input type="radio">` carries the semantics and value. The selected state is shown with an accent border, not color alone.

## Accessibility

`<label htmlFor>` card + native `<input type="radio">`. `aria-invalid` when `invalid`, description linked with `aria-describedby`, visible `focus-visible` ring on the input (the card shows `focus-within` border emphasis).

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when an option needs more visual weight than a plain row — e.g. a plan or workspace choice. For a group of these use `radio-card-group`.
