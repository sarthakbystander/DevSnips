# Link Button

A button rendered as an inline link for terse secondary actions inside forms and rows. Reads as a link but still triggers onClick; for true navigation, pass an href.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<LinkButton onClick={forgot}>Forgot password?</LinkButton>
<LinkButton href="/help">View all</LinkButton>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | — |
| `href` | `string` | — (renders `<a>` when set) |
| `disabled` | `boolean` | `false` |
| `iconLeft` / `iconRight` | `ReactNode` | — |
| `type` | `button \| submit \| reset` | `button` (button mode) |

When `href` is set the component renders an `<a>` (with `aria-disabled` when disabled); otherwise a `<button>`.

## Variants

Single link variant: `color.link` text, underline on hover, no border or fill. When `href` is provided, renders a real anchor.

## Sizes

Height is auto (inline). Font inherits the surrounding text size; use it inline with body copy.

## States

default · hover (underline + `link-hover`) · focus-visible · disabled (reduced opacity + `aria-disabled`).

## Accessibility

Button mode renders a native `<button>`; link mode renders a native `<a href>`. Focus-visible ring uses `color.focus-ring`. Disabled links use `aria-disabled` (not `tabindex=-1`) so the affordance stays perceivable; pair with JS that ignores activation when disabled.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use for terse inline actions ("View all", "Forgot password?", "Add label"). For primary navigation, prefer a real anchor or a SolidButton.
