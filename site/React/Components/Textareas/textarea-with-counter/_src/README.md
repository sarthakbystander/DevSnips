# Textarea With Counter

Textarea with a live character counter (current / maximum) derived from the real value.

## Usage

```tsx
<TextareaWithCounter label="Release notes" maxLength={280} helperText="Shown on the changelog page." rows={4} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaWithCounter label="Release notes" maxLength={280} helperText="Shown on the changelog page." rows={4} />
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
| `helperText` | `ReactNode` | — | Optional text beside the counter. |

## States

Native textarea with a live character counter under the field. The count is computed from the actual value (controlled `value` or tracked uncontrolled text) — it updates on every keystroke and is never faked. When `maxLength` is supplied the counter reads `current / maximum` and the native attribute enforces the limit; at the limit the count gains weight + foreground color as a quiet, non-color-only cue. Without `maxLength` the counter is a plain character count.

## Accessibility

The counter region is linked with `aria-describedby` and marked `aria-live="polite"`, so screen readers can read the count on demand and hear polite updates without focus theft. The at-limit cue is text weight + color together — not color alone. Native `maxLength` behavior (typing stops at the cap) is preserved.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use for bounded content: changelog entries, status updates, short bios. For long-form content where a limit would be hostile, drop `maxLength` and keep the plain count, or use the plain `textarea`.
