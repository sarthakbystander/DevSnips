# Switch With Icon

Switch with an optional icon that communicates the setting's meaning.

## Usage

```tsx
<SwitchWithIcon label="Email notifications" icon={<BellIcon />} defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchWithIcon label="Email notifications" icon={<BellIcon />} defaultChecked />
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
| `icon` | `ReactNode` | — | Optional leading icon that communicates the setting's meaning. Omit when none adds meaning. |

## States

Same native switch as the reference, with an optional ReactNode `icon` rendered between the control and the label. The icon is state-aware (primary token when on, muted when off) but the state is never communicated by icon color alone — the thumb and track carry it.

## Accessibility

`<label htmlFor>` association; the icon is decorative-adjacent (the label still carries the accessible name). `aria-invalid` for errors, `aria-describedby` for external helper text, visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Icons must communicate meaning (a bell for notifications, a shield for security) — they are not decoration. Do not add icons to every switch in a dense settings page; use them where the glyph disambiguates a short label.
