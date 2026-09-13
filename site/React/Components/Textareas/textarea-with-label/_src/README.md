# Textarea With Label

Textarea with a properly associated visible label — clicking the label focuses the field.

## Usage

```tsx
<TextareaWithLabel label="Support message" required rows={4} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaWithLabel label="Support message" required rows={4} />
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

## States

Same native textarea as the reference, but `label` is required and always rendered as `<label htmlFor>` above the control, so clicking the label text activates the field. Renders a `*` when `required` (the native `required` attribute carries the semantics; the asterisk is `aria-hidden`).

## Accessibility

`<label htmlFor>` association gives the control an accessible name and a larger click target. `required` is the native attribute (form validation + SR announcement); the visible asterisk is decorative and hidden from assistive tech. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when the field needs only a label. Reach for `textarea-with-description` when the user needs context before typing, or `textarea-with-helper` when guidance belongs below the field.
