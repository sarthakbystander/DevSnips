# Checkbox Readonly

Read-only checkbox that stays focusable but cannot be toggled by the user.

## Usage

```tsx
<CheckboxReadonly label="System-managed permission" checked />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<CheckboxReadonly label="System-managed permission" checked />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label. |
| `checked` | `boolean` (required) | — | Fixed checked state. |
| `onChange` | `(checked, event) => void` | — | Fires with the blocked attempt. |
| `helperText` | `ReactNode` | — | Helper text. |
| `name` / `value` / `id` | `string` | — | Native form attrs. |

## States

Read-only checkbox. The native input uses `readOnly` plus a `preventDefault` on change (browsers do not natively honor `readOnly` on checkboxes), so clicks and Space do not toggle the value. Unlike `disabled`, it remains focusable and is still part of the document flow.

## Accessibility

Native `readOnly` + `aria-readonly="true"`. The control is focusable so users can read its state; `preventDefault` keeps the value fixed. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This checkbox uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this for a value that is fixed in this context but should still be focusable and perceivable (e.g. a system-managed permission). Use `checkbox-disabled` when the option is genuinely non-interactive.
