# Switch Loading

Switch with a real loading state that blocks interaction while the change is persisted.

## Usage

```tsx
<SwitchLoading label="Analytics" loading={saving} checked={on} onChange={handleSave} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<SwitchLoading label="Analytics" loading={saving} checked={on} onChange={handleSave} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label. |
| `loading` | `boolean` | `false` | Pending update state — disables the input, sets `aria-busy`, swaps the thumb for a spinner of the same geometry (no layout shift). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback (won't fire while loading/disabled). |
| `disabled` | `boolean` | — | Disables the control. |
| `name` / `value` / `id` | `string` | — | Native form attrs. |

## States

Native switch with a `loading` prop for async persistence. While `loading` is true the input is disabled (no conflicting interaction can occur), `aria-busy="true"` is set, and the thumb is replaced by a spinner of exactly the same geometry — the control never moves or resizes. The spinner represents a real pending update, not decoration.

## Accessibility

`aria-busy="true"` + native `disabled` while loading, so assistive tech reports the control as busy and it is removed from interaction. The thumb spinner is `aria-hidden`. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This switch uses the semantic color, radius, spacing, and motion tokens.

## Notes

Drive `loading` from your save flow: set it true when the toggle fires, resolve it when the request settles. Keep the checked value unchanged until the update succeeds, so the thumb never lies about persisted state.
