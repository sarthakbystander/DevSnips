# Textarea With Helper

Textarea with muted helper text below the field, wired via aria-describedby.

## Usage

```tsx
<TextareaWithHelper label="Feedback" helperText="Visible to the product team only." rows={4} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaWithHelper label="Feedback" helperText="Visible to the product team only." rows={4} />
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
| `helperText` | `ReactNode` (required) | — | Helper text below the control, linked with `aria-describedby`. |

## States

Native textarea with a label above and muted helper text below the control. Helper text answers questions that come up while filling the field — visibility, formatting rules, what happens on submit. It is linked with `aria-describedby`.

## Accessibility

`<label htmlFor>` + `aria-describedby={helperId}` on the native textarea. The helper is plain text (not color-coded), so it reads the same for everyone. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Description goes above the field (context before typing); helper goes below (guidance while typing). Do not stack both — pick the one that matches when the user needs the information.
