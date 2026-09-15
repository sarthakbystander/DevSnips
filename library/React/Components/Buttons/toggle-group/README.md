# Toggle Group

A joined set of toggles. `type="single"` behaves like a radiogroup (one on); `type="multiple"` like a group of checkboxes. Selected segments use `surface-active` + `aria-pressed`, with arrow-key roving.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<ToggleGroup type="single" value={view} onValueChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}}] />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `options` | `Array<{ value: string; label: ReactNode; icon?: string; disabled?: boolean }>` | — |
| `type` | `single \| multiple` | `single` |
| `value` | `string` (single) \| `string[]` (multiple) | — (controlled) |
| `defaultValue` | same shape as `value` | — (uncontrolled initial) |
| `onValueChange` | `(value: string \| null) \| (string[]) => void` | — |
| `size` | `ButtonSize` | `sm` |
| `label` | `string` | — (group `aria-label`) |

Plus all native `HTMLAttributes<HTMLDivElement>`.

## Variants

Single bordered container. Selected segments use `surface-active` + `aria-pressed="true"`. Unselected are transparent; hover lifts to `surface-hover`.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm` for compact toolbars.

## States

default · hover · focus-visible · pressed (`aria-pressed`, surface-active + font-weight) · disabled (per option).

## Accessibility

Renders `role="group"` with `aria-label`. Each segment is a native `<button>` with `aria-pressed`. **Keyboard**: ArrowLeft/Right move focus (roving); Space/Enter toggles. Single-select toggles behave like a radiogroup but expose `aria-pressed` (one true at a time).

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

For strictly single-choice radiogroup semantics, prefer SegmentedButton. ToggleGroup is for flexible single- or multi-select toggle sets.
