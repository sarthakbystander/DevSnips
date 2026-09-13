# Textarea Auto Resize

Textarea that grows and shrinks with its content, capped at a configurable maximum height.

## Usage

```tsx
<TextareaAutoResize label="Commit message" maxHeight={240} rows={2} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<TextareaAutoResize label="Commit message" maxHeight={240} rows={2} />
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
| `maxHeight` | `number` | `320` | Height cap in px — the field scrolls past it instead of growing. |

## States

Native textarea whose height tracks its content: it grows as lines are added, shrinks when they are removed, and stops at `maxHeight` (default 320px) where it scrolls. Measurement runs from the real value — initial content, uncontrolled typing, and controlled `value` updates all trigger it — plus once on viewport resize (wrapped lines reflow). Manual resize is disabled (`resize-none`) because the component owns the height; height changes are instant, so nothing animates and reduced-motion users see identical behavior. Without effects running it still renders as a normal `rows`-sized textarea.

## Accessibility

Same native semantics as the reference textarea — real focus, keyboard, selection, and form behavior. No live regions are needed because the resize is a visual nicety, not a state change. Visible `focus-visible` ring; `resize-none` is safe here because the field grows on its own.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This textarea uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use for inputs where the content length varies wildly and scrolling a fixed box hides context: commit messages, review comments, support replies. Keep `maxHeight` sane so a paste of 500 lines cannot push the rest of the form off-screen.
