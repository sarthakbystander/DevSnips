# Textarea With Description

Textarea with a strong label plus a supporting description above the field, wired via aria-describedby.

## Usage

```tsx
<TextareaWithDescription label="Bug report" description="Include steps to reproduce and what you expected to happen." rows={5} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaWithDescription label="Bug report" description="Include steps to reproduce and what you expected to happen." rows={5} />
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
| `description` | `ReactNode` (required) | — | Supporting description linked with `aria-describedby`. |

## States

Native textarea with a label and a muted description block stacked between the label and the control. The description frames the field before typing — what to include, the expected format, who will read it. It is linked to the control with `aria-describedby`.

## Accessibility

`<label htmlFor>` + `aria-describedby={descriptionId}` on the native textarea, so screen readers announce both the name and the description. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use this when the field needs a sentence of explanation before the user starts typing — e.g. a bug report that needs repro steps, or a documentation summary with an expected scope. For shorter after-the-fact guidance, use `textarea-with-helper`.
