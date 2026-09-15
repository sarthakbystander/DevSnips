# Textarea

Native multi-line textarea styled to the DevSnips input visual language — the reference for the whole family.

## Usage

```tsx
<Textarea label="Project description" placeholder="What does this project do?" rows={4} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<Textarea label="Project description" placeholder="What does this project do?" rows={4} />
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
| `readOnly` | `boolean` | — | Native read-only — focusable, selectable, submitted. |
| `required` / `name` / `id` | `boolean` / `string` | — | Native form semantics (`id` also the label `htmlFor`). |
| `minLength` / `maxLength` | `number` | — | Native length constraints. |
| `className` | `string` | — | Extra Tailwind classes merged onto the control. |
| other native props / `aria-*` | — | — | Passed through to the `<textarea>`. |

## States

A real native `<textarea>` styled with Tailwind + the `--ds-*` semantic tokens. Default / hover / focus / focus-visible / filled / disabled / read-only states all come from native pseudo-classes; dark mode follows the token theme. Vertical resize stays enabled (the intentional DevSnips resize behavior — horizontal resize is off so layouts never break). Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) usage work natively with no duplicated state.

## Accessibility

Real `<textarea>` element — full native keyboard interaction, selection, copy/paste, and form semantics are preserved. Pass `label` for a visible `<label htmlFor>` or `aria-label`/`aria-labelledby` for a bare control. Supporting text uses `aria-describedby`. Visible `focus-visible` ring from `--ds-color-focus-ring`. Disabled uses the real `disabled` attribute; read-only uses real `readOnly`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

This is the reference implementation for the Textareas family — it establishes the shared full-width layout, `min-h-[80px]` floor, `px-3 py-2` padding, `text-sm` typography, `radius-sm`, 1px `color.border`, `color.input` background, muted placeholder, focus ring, `resize-y` behavior, disabled/read-only treatments, and dark-mode behavior that every other textarea extends.
