# Switch Card

Settings card that pairs a label and supporting content with a switch in a deliberate, accessible row.

## Usage

```tsx
<SwitchCard label="Cloud backup" description="Every night at 02:00 UTC, retained for 30 days." defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchCard label="Cloud backup" description="Every night at 02:00 UTC, retained for 30 days." defaultChecked />
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
| `description` | `ReactNode` | — | Supporting content linked with `aria-describedby`. |

## States

A single settings card. The whole row is a deliberate click target (a real `<label htmlFor>`) while the native switch input carries the semantics. The on state is shown with a primary border plus the moved thumb — not color alone. Hover, focus-within, and disabled states mirror the other switch variants.

## Accessibility

`<label htmlFor>` wraps label, description, and input. The description is linked with `aria-describedby`. Visible `focus-visible` ring on the input; the card border strengthens on focus-within. `aria-invalid` when `invalid`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use a switch card when a setting carries real weight — a sentence of context, a destructive consequence, or billing impact. Do not wrap every switch in a card; inline settings stay inline.
