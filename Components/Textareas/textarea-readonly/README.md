# Textarea Readonly

Read-only textarea using the real native readOnly attribute — focusable, selectable, submitted.

## Usage

```tsx
<TextareaReadonly label="Generated summary" value={summary} rows={4} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaReadonly label="Generated summary" value={summary} rows={4} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |
| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled value. |
| `onChange` | `(event) => void` | — | Native change callback. |
| `rows` | `number` | `3` | Visible rows — the natural height floor (with `min-h-[80px]`). |
| `placeholder` | `string` | — | Muted placeholder (never critical information). |
| `disabled` | `boolean` | — | Native disabled — not focusable, not submitted. |
| `readOnly` | `boolean` | `true` | Native read-only — focusable, selectable, submitted. |
| `required` / `name` / `id` | `boolean` / `string` | — | Native form semantics (`id` also the label `htmlFor`). |
| `minLength` / `maxLength` | `number` | — | Native length constraints. |
| `className` | `string` | — | Extra Tailwind classes merged onto the control. |
| other native props / `aria-*` | — | — | Passed through to the `<textarea>`. |

## States

Native textarea with `readOnly` defaulted to `true`. The value cannot be edited, but the control stays in the tab order, its text stays selectable and copyable, and its value IS submitted with the form. The subtle surface + muted text come from the `:read-only` pseudo-class — visually distinct from the muted `disabled` treatment. Pass `readOnly={false}` to flip it back.

## Accessibility

Real `readOnly` attribute — screen readers announce the field as read-only while it remains focusable, so the content is reachable and reviewable by keyboard users (unlike `disabled`, which is skipped). Visible `focus-visible` ring still applies.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use read-only for values the user may inspect or copy but not change: a generated summary, an audit-trail entry, the rendered version of a template. Disabled and read-only are different states — this variant exists to keep that distinction honest.
