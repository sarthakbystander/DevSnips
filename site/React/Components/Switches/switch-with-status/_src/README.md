# Switch With Status

Switch paired with an explicit text status readout (Enabled / Disabled).

## Usage

```tsx
<SwitchWithStatus label="Analytics" defaultChecked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchWithStatus label="Analytics" defaultChecked />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label. |
| `onText` / `offText` | `ReactNode` | `Enabled` / `Disabled` | Status readout for each state. |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `name` / `value` / `id` | `string` | — | Native form attrs. |

## States

Native switch with an explicit status readout beneath the label. The status text tracks the checked state (`Enabled` / `Disabled` by default, overridable with `onText` / `offText`), so the state is readable in words — never color alone. The readout is wired to the input with `aria-describedby`.

## Accessibility

`<label htmlFor>` association; the status line is linked with `aria-describedby` so assistive tech announces the current state as supporting text. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when the current state must be unambiguous at a glance — integrations, automation, sync. For a plain setting the thumb + track are enough; reach for `switch-with-status` when the words themselves matter.
