# Textarea Disabled

Disabled textarea using the real native disabled attribute — not focusable, not submitted.

## Usage

```tsx
<TextareaDisabled label="Closure reason" defaultValue="Closed after the v2 migration completed." rows={3} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaDisabled label="Closure reason" defaultValue="Closed after the v2 migration completed." rows={3} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |
| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled value. |
| `onChange` | `(event) => void` | — | Native change callback. |
| `rows` | `number` | `3` | Visible rows — the natural height floor (with `min-h-[80px]`). |
| `placeholder` | `string` | — | Muted placeholder (never critical information). |
| `disabled` | `boolean` | `true` | Native disabled — not focusable, not submitted. |
| `readOnly` | `boolean` | — | Native read-only — focusable, selectable, submitted. |
| `required` / `name` / `id` | `boolean` / `string` | — | Native form semantics (`id` also the label `htmlFor`). |
| `minLength` / `maxLength` | `number` | — | Native length constraints. |
| `className` | `string` | — | Extra Tailwind classes merged onto the control. |
| other native props / `aria-*` | — | — | Passed through to the `<textarea>`. |

## States

Native textarea with `disabled` defaulted to `true`. The native attribute does the work: the control leaves the tab order, cannot be focused or edited, and its value is NOT submitted with the form. The muted surface + reduced opacity come from the `:disabled` pseudo-class; the label gets a not-allowed cursor. Pass `disabled={false}` to flip it back to the normal reference textarea.

## Accessibility

Real `disabled` attribute — assistive tech announces the control as unavailable and skips it in the tab order. The value stays perceivable (readable muted text) rather than removed. Compare with `textarea-readonly`, which stays focusable and is submitted.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use disabled for fields that are temporarily unavailable because of state (a closed ticket, a locked workspace). If the user should still be able to select and copy the text, use `textarea-readonly` instead.
