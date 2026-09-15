# Command Button

Opens a command palette. A wide trigger with a search icon, placeholder text, and a kbd hint showing the platform shortcut. Wire `onOpen` to mount the palette; when `bindShortcut` is true, listens for the global shortcut (Cmd/Ctrl+K).

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<CommandButton onOpen={openPalette} placeholder="Search or run a command…" shortcut="⌘K" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `placeholder` | `string` | `"Search or run a command…"` |
| `shortcut` | `string` | `"⌘K"` |
| `onOpen` | `() => void` | — |
| `variant` | `outline \| secondary` | `outline` |
| `size` | `ButtonSize` | `md` |
| `bindShortcut` | `boolean` | `true` (listen for Cmd/Ctrl+K globally) |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

outline (default) · secondary. A wide trigger that reads as a search field; muted text + a kbd hint on the trailing edge.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · focus-visible · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. The kbd hint is decorative (`aria-hidden`); the button's accessible name is the placeholder. When `bindShortcut` is on, Cmd/Ctrl+K calls `onOpen` so the palette is reachable without a visible click.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use once per app for a global command palette. The trigger is a button (not an input) — it opens the palette, which holds the real search input.
