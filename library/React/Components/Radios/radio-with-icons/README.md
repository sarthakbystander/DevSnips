# Radio With Icons

Radio with an optional leading icon and selected indicator icon that communicate meaning.

## Usage

```tsx
<RadioWithIcons label="Team workspace" icon={<Icon name="user" />} name="workspace" value="team" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<RadioWithIcons label="Team workspace" icon={<Icon name="user" />} name="workspace" value="team" defaultChecked />
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
| `icon` | `ReactNode` | — | Leading icon that communicates meaning (color shifts on select). |
| `selectedIcon` | `ReactNode` | — | Trailing indicator shown when selected. |

## States

A radio with an optional leading icon that communicates meaning (e.g. a workspace-type glyph). Icons are ReactNode and must not be purely decorative — omit `icon` when none adds meaning. A trailing `selectedIcon` may be shown when the option is selected. Built on the native `<input type="radio">`; the icon sits in the clickable label.

## Accessibility

`<label htmlFor>` + native `<input type="radio">`. Icons are `aria-hidden` decoration — the label carries the accessible name. `aria-invalid` when `invalid`, visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

Only use icons that add meaning (e.g. distinguishing workspace types). Do not add a decorative icon to every basic radio. The leading icon is optional precisely so a plain labeled radio stays the default.
