# Textarea With Error

Textarea with a destructive error state and an associated inline message (aria-invalid + role=alert).

## Usage

```tsx
<TextareaWithError label="Bug report" error={message} rows={5} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaWithError label="Bug report" error={message} rows={5} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` (required) | — | Visible label above the control. |
| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled value. |
| `onChange` | `(event) => void` | — | Native change callback. |
| `rows` | `number` | `3` | Visible rows — the natural height floor (with `min-h-[80px]`). |
| `placeholder` | `string` | — | Muted placeholder (never critical information). |
| `disabled` | `boolean` | — | Native disabled — not focusable, not submitted. |
| `readOnly` | `boolean` | — | Native read-only — focusable, selectable, submitted. |
| `required` / `name` / `id` | `boolean` / `string` | — | Native form semantics (`id` also the label `htmlFor`). |
| `minLength` / `maxLength` | `number` | — | Native length constraints. |
| `className` | `string` | — | Extra Tailwind classes merged onto the control. |
| other native props / `aria-*` | — | — | Passed through to the `<textarea>`. |
| `error` | `string` | — | Error message. When set: destructive border + `aria-invalid` + `role="alert"` message. |

## States

Native textarea with an inline error state driven by the `error` prop. While `error` is set the border switches to `color.destructive`, `aria-invalid="true"` is applied, and the message renders below the field in a `role="alert"` region linked with `aria-describedby`. Clearing `error` returns the field to the default state. The state is never color alone — the message text carries it.

## Accessibility

`aria-invalid="true"` on the textarea while invalid; the message is a `role="alert"` region associated with `aria-describedby`, so screen readers announce it when it appears. The visible message (`Error: …`) plus border means the state does not rely on red color alone. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Keep the message specific and actionable (what is wrong + how to fix it). Validate on submit or blur — showing an error while the user is still typing their first characters is noise.
