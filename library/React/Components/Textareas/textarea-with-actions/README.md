# Textarea With Actions

Textarea with a contextual action bar — live character count plus real Clear and Copy buttons.

## Usage

```tsx
<TextareaWithActions label="Support reply" maxLength={500} onCopy={(v) => console.log(v)} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaWithActions label="Support reply" maxLength={500} onCopy={(v) => console.log(v)} />
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
| `clearLabel` / `copyLabel` / `copiedLabel` | `string` | `Clear` / `Copy` / `Copied` | Action labels. |
| `resetMs` | `number` | `2000` | Delay before the copy label resets. |
| `onClear` / `onCopy` | `() => void` / `(value) => void` | — | Action callbacks. |

## States

Native textarea with an action bar below the field: a live character count on the left, and real Clear and Copy buttons on the right. Clear empties the value and returns focus to the field; Copy writes the current value to the clipboard (with a fallback for non-secure contexts) and confirms via a label swap + an `aria-live` status message. Both buttons disable while the field is empty, and both act on the real value in controlled and uncontrolled modes. The bar wraps on narrow screens.

## Accessibility

Both actions are real `<button type="button">` elements with visible text labels, keyboard-operable, with visible `focus-visible` rings. Copy feedback is announced through a `role="status"` / `aria-live="polite"` region; the count is `aria-describedby` + polite live. Clear returns focus to the textarea so keyboard users are not stranded.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Every action here has a real job — clearing drafts and copying composed text. Do not add icon buttons for decoration; extend the bar only with actions that operate on the value (e.g. a template insert or a formatting command).
