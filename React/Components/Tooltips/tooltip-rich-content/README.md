# Tooltip with Rich Content

Structured — still non-interactive — content: a title row, supporting metadata, a status dot, or a keyboard-shortcut chip, composed with plain markup inside TooltipContent.

## Usage

```tsx
import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-rich-content";

<Tooltip>
  <TooltipTrigger>
    <button type="button">Open command palette</button>
  </TooltipTrigger>
  <TooltipContent className="space-y-1">
    <span className="block font-medium">Open command palette</span>
    <span className="block text-xs text-[var(--ds-color-muted-foreground)]">
      Then type to search every page. <kbd>⌘K</kbd>
    </span>
  </TooltipContent>
</Tooltip>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-rich-content";

<Tooltip>
  <TooltipTrigger>
    <button type="button">Open command palette</button>
  </TooltipTrigger>
  <TooltipContent className="space-y-1">
    <span className="block font-medium">Open command palette</span>
    <span className="block text-xs text-[var(--ds-color-muted-foreground)]">
      Then type to search every page. <kbd>⌘K</kbd>
    </span>
  </TooltipContent>
</Tooltip>
```

## Props

### `<Tooltip>`

| Name | Type | Default | Description |
|---|---|---|---|
| `open` | `boolean` | — | Open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial open state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the tooltip requests to open or close (hover, focus, blur, Escape). |
| `side` | `"top" \| "right" \| "bottom" \| "left"` | `"top"` | Preferred side of the trigger; flips to the opposite side when it would overflow the viewport. |
| `align` | `"start" \| "center" \| "end"` | `"center"` | Alignment along the trigger; shifts toward the edge with room when it would overflow. |
| `sideOffset` | `number` | `6` | Gap between the trigger and the tooltip, in pixels. Applied after any flip. |
| `delayDuration` | `number` | `300` | Hover delay before opening, in milliseconds. Keyboard focus always opens immediately. |
| `disabled` | `boolean` | `false` | Suppress the tooltip entirely: hover and focus do nothing, and a tooltip that becomes disabled while open closes. |
| `className` | `string` | — | Extra classes on the positioning wrapper (a `relative inline-flex` span). |
| `children` | `ReactNode` | — | A single `TooltipTrigger` + a single `TooltipContent`. |

### `<TooltipTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `children` | `ReactElement` | — | Exactly one element: a native focusable element (`<button>`, `<a>`, `<input>`, …) or a component that forwards its ref and the pointer/focus handlers. |

`TooltipTrigger` clones the child to attach the trigger ref, the hover/focus handlers, and `aria-describedby` pointing at the tooltip. The child's own handlers run first and can cancel the tooltip behavior with `event.preventDefault()`. The trigger must be focusable — a tooltip must never depend on hover alone. For a natively `disabled` control (which cannot receive hover or focus), wrap it in a `<span tabIndex={0}>` so the explanation stays reachable — see `tooltip-disabled-trigger`.

### `<TooltipContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="tooltip"` bubble (e.g. a larger `max-w-*`). |
| `children` | `ReactNode` | — | Text or structured, **non-interactive** content. |

`role="tooltip"` is fixed; every native `div` attribute (`aria-*`, `data-*`, …) is forwarded via `...rest`. Rendered only while open, `pointer-events-none`, capped at `min(16rem, 100vw - 2rem)` wide. Content that must be clicked or focused does not belong in a tooltip — use a popover or a dialog instead.

## Composition

- `Tooltip` — the root provider. Owns the open state (controlled `open` + `onOpenChange`, or uncontrolled `defaultOpen`), the placement config (`side`, `align`, `sideOffset`), the hover `delayDuration`, the `disabled` switch, and the generated tooltip id. Renders a `relative inline-flex` wrapper the content is positioned against.
- `TooltipTrigger` — clones its single child element (a real focusable element, or a `<span tabIndex={0}>` around a disabled control) to attach the trigger ref, the pointer/focus handlers, and `aria-describedby` pointing at the tooltip.
- `TooltipContent` — the `role="tooltip"` bubble plus its pointing arrow. Rendered only while open, `pointer-events-none` (a tooltip never carries interactive content), measured against the viewport before paint and flipped/shifted when the preferred placement would overflow.

`TooltipContent` accepts any ReactNode, so structure (a title row, muted metadata, a `<kbd>` chip, a status dot) is plain markup — no extra primitives. The constraint is behavioral, not visual: rich content stays **non-interactive**. The moment content needs a link, a button, or focus, it has outgrown the tooltip — use a popover or dialog.

## Tooltip Behavior

The root `<Tooltip>` owns the open state. Both modes are supported:

- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultOpen`; the component owns the state.

Hover opens the tooltip after `delayDuration` (default 300 ms, so passing cursors do not flash it); keyboard focus opens it **immediately** — keyboard users never wait for a hover delay. The component tracks *what* opened it: a pointer-opened tooltip closes on pointer leave, a focus-opened tooltip closes on blur. If focus leaves while the pointer still hovers, ownership hands over to the pointer so the tooltip closes on pointer leave instead — the two gestures never fight.

Escape dismisses the open tooltip (focus stays on the trigger). The `disabled` prop suppresses opening entirely — and a tooltip that becomes disabled while open closes. A pending hover-open timer is cancelled on pointer leave and on unmount, so a tooltip never opens after its trigger is gone.

On touch devices there is no hover: tapping the trigger fires the same pointer path, so the tooltip appears on tap and dismisses on the next outside interaction. Touch users get the same content as pointer users.

## Positioning

Placement is prop-driven — `side` (`top` / `right` / `bottom` / `left`) × `align` (`start` / `center` / `end`), with `sideOffset` (pixels, default 6) for the trigger gap. `center` aligns the tooltip's center with the trigger's center; `start` / `end` align the leading / trailing edges.

Before paint, `TooltipContent` measures itself and the trigger against the viewport (an 8px margin) and corrects the placement when it would overflow: `top` ↔ `bottom` and `left` ↔ `right` flip when the preferred side lacks room and the opposite side has more, and an `align` that would overflow an edge shifts toward the side with room (`center` degrades to `start` / `end` first). The correction runs in a layout effect while the content is still transparent, so the flip never flashes. `sideOffset` is applied after the flip, so the gap always points the right way.

The content is absolutely positioned inside the root's `relative inline-flex` wrapper — there is no portal and no positioning library. The bubble is capped at `min(16rem, 100vw - 2rem)` wide, so even long content stays inside a 375px viewport. One honest constraint of the no-portal approach: an ancestor with `overflow: hidden` (and a stacking trap) can clip the bubble — place the `<Tooltip>` outside clipping containers.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Tab` | Moves focus to the trigger; a focused trigger opens its tooltip immediately (no hover delay) |
| `Shift+Tab` / `Tab` away | Blur dismisses the tooltip |
| `Escape` | Dismiss the open tooltip; focus stays on the trigger |

The trigger is a real focusable element (a `<button>`, `<a>`, or — for a disabled control — a `<span tabIndex={0}>`), so Enter/Space activation and tab order follow normal browser behavior. The tooltip itself is not focusable and contains no interactive elements — it is announced through the trigger's `aria-describedby`.

## Accessibility

The structure follows the WAI-ARIA tooltip pattern.

- The trigger is a real focusable element — a tooltip must never depend on hover alone. Keyboard focus opens the tooltip exactly like pointer hover.
- The tooltip is `role="tooltip"`, and the trigger carries `aria-describedby` pointing at the tooltip's id, so assistive technology announces the tooltip text as the trigger's description when it appears.
- The tooltip is `pointer-events-none` and never contains interactive content (links, buttons, inputs). Content that must be interacted with belongs in a popover or dialog, not a tooltip.
- A tooltip is **supplementary**: it must never be the only way to reach essential information. Everything it says is either repeated in the visible UI or genuinely optional detail.
- A natively `disabled` control does not receive hover or focus events, so a tooltip explaining *why* it is disabled must wrap it in a focusable `<span tabIndex={0}>` (the inner control gets `pointer-events-none`) — see `tooltip-disabled-trigger`.

Structured content is still announced as one flat description through `aria-describedby` — screen readers read the title and metadata in order. Visual structure (weight, muted color, chips) is a sighted-user enhancement; never rely on it to carry meaning the words do not. Decorative glyphs inside the tooltip (the status dot) are `aria-hidden`.

## States

- **Trigger** — the wrapped element keeps its own styling and its visible `:focus-visible` ring (`--ds-color-focus-ring`); the tooltip adds no visual state to the trigger.
- **Content** — `surface-elevated` with a 1px `--ds-color-border` and a restrained `--ds-shadow-sm`, radius-md, 13px/20px text, per the Dropdown / Popover / Tooltip token rules.
- **Arrow** — a rotated square sharing the content's surface and border, notched toward the trigger; follows the resolved placement (including after a flip).
- **Open transition** — a subtle 150ms opacity fade-in that doubles as the pre-measurement guard; `motion-reduce:transition-none` disables it.
- **Disabled** — the `disabled` prop suppresses opening; a natively `disabled` trigger cannot receive hover/focus, so the tooltip pattern for disabled controls is the focusable `<span tabIndex={0}>` wrapper (see `tooltip-disabled-trigger`).

## Responsive Behavior

The bubble is capped at `min(16rem, 100vw - 2rem)` wide, wraps its text, and is measured against the viewport before paint — flipping sides or shifting alignment when it would overflow. The trigger keeps its own size (36px controls in the demos — a comfortable touch target). On touch devices the tooltip appears on tap, since there is no hover. Every demo is verified overflow-free at 375 / 768 / 1280px with the tooltip open and closed.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This tooltip variant uses the semantic color, radius, shadow, typography, and motion tokens — per the Dropdown / Popover / Tooltip row of the component token rules (radius-md, shadow-sm–md, 1px subtle border, body-sm text).

## Notes

Two compositions: a status pill whose tooltip adds a title plus freshness metadata (with an aria-hidden status dot), and a command button whose tooltip pairs the action name with a `<kbd>` shortcut chip and a usage hint. Both are text — nothing inside either bubble can or needs to be clicked.
