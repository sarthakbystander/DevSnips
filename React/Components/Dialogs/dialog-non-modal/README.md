# Non-Modal Dialog

`modal={false}`: a floating keyboard-shortcuts reference panel — no overlay, no scroll lock, no focus trap; the page behind stays interactive and the panel closes on Escape, outside pointer down, or its close actions.

## Usage

```tsx
import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogClose,
} from "./dialog-non-modal";

<Dialog modal={false}>
  <DialogTrigger>Keyboard shortcuts</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Keyboard shortcuts</DialogTitle>
    </DialogHeader>
    <div className="px-5 py-4">…shortcut table…</div>
    <DialogFooter>
      <DialogClose>Close</DialogClose>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogClose,
} from "./dialog-non-modal";

<Dialog modal={false}>
  <DialogTrigger>Keyboard shortcuts</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Keyboard shortcuts</DialogTitle>
    </DialogHeader>
    <div className="px-5 py-4">…shortcut table…</div>
    <DialogFooter>
      <DialogClose>Close</DialogClose>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

## Props

### `<Dialog>`

| Name | Type | Default | Description |
|---|---|---|---|
| `open` | `boolean` | — | Open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial open state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the dialog requests to open or close. |
| `modal` | `boolean` | `true` | Modal behavior: overlay, scroll lock, focus trap, `aria-modal`. `false` renders a non-modal floating panel (no overlay; closes on Escape / outside pointer down). |
| `children` | `ReactNode` | — | `DialogTrigger` + `DialogContent`. |

### `<DialogTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Visible trigger label. |

A real `<button type="button">` with `aria-haspopup="dialog"` + `aria-expanded`; every native button attribute (`disabled`, `aria-label`, …) is forwarded. Focus is restored here when the dialog closes.

### `<DialogContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="dialog"` panel (e.g. a larger `max-w-*`). |
| `children` | `ReactNode` | — | Header, body content, footer, close button. |

Portaled to `document.body` and rendered only while open. Labelled by `DialogTitle` / described by `DialogDescription` automatically when they are rendered; pass `aria-label` when a dialog intentionally has no visible title, and `role="alertdialog"` for confirmation dialogs (forwarded via `...rest`).

### `<DialogHeader>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the header. |
| `children` | `ReactNode` | — | `DialogTitle` + `DialogDescription`. |

### `<DialogTitle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<h2>`. |
| `children` | `ReactNode` | — | Title text. |

Registers itself so `DialogContent` sets `aria-labelledby` only while a title exists.

### `<DialogDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Supporting description text. |

Registers itself so `DialogContent` sets `aria-describedby` only while a description exists.

### `<DialogFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the action row. |
| `children` | `ReactNode` | — | Footer actions (`DialogClose`, plain buttons, links). |

Buttons stack full-width below `sm` and lay out right-aligned inline from `sm` up.

### `<DialogClose>`

| Name | Type | Default | Description |
|---|---|---|---|
| `variant` | `"outline" \| "primary" \| "destructive" \| "ghost"` | `"outline"` | `outline` is the bordered footer cancel action; `primary` / `destructive` are confirming actions that also close; `ghost` is the icon-sized corner close button (positioned absolute top-right — give it an `aria-label` such as `"Close"`). |
| `onClick` | `(event) => void` | — | Called before the dialog closes; `event.preventDefault()` keeps the dialog open. |
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Visible label (or the close icon for `ghost`). |

A real `<button type="button">` that requests close; every native button attribute is forwarded.

## Composition

- `Dialog` — the root provider. Owns the open state (controlled `open` + `onOpenChange`, or uncontrolled `defaultOpen`), the `modal` behavior switch, the generated ids, and the focus-restore memory.
- `DialogTrigger` — a real `<button type="button">` with `aria-haspopup="dialog"` + `aria-expanded`. Click toggles the dialog.
- `DialogContent` — the portaled `role="dialog"` panel (`aria-modal` when modal) plus, in modal mode, the overlay that blocks the background. Rendered only while open; moves focus inside on open and traps Tab while modal.
- `DialogHeader` — the header layout slot (`DialogTitle` + `DialogDescription`).
- `DialogTitle` — an `<h2>` that registers itself so the panel is labelled by it.
- `DialogDescription` — a `<p>` that registers itself so the panel is described by it.
- `DialogFooter` — the action row; buttons go full-width stacked on small screens, right-aligned inline from `sm` up.
- `DialogClose` — a real `<button>` that closes the dialog (footer cancel actions, or the header close with `variant="ghost"`).

Non-modal is a prop, not a different component: the same primitives with `modal={false}` on the root. The panel keeps the shared dialog geometry but renders without the overlay and without `aria-modal`.

## Dialog Behavior

`modal={false}` switches three behaviors off: no overlay is rendered (the page stays clickable), body scroll is not locked, and Tab is not trapped — focus can leave the panel and reach the page behind it. `aria-modal` is omitted, since assistive technology must not be told the background is inert when it is not.

Closing still works from every direction: Escape (the panel registers on the same top-most stack), a pointer down outside the panel, the trigger toggle, and `DialogClose`. Focus is still moved into the panel on open and restored to the trigger on close.

Use non-modal for reference material the user consults while working elsewhere on the page — shortcuts, inspectors, help panels. Use the default modal dialog whenever the surrounding page must wait for a decision.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the panel, focus the first focusable element inside |
| `Tab` / `Shift+Tab` | Move naturally — no trap; the page behind stays reachable |
| `Escape` | Close the panel and restore focus to the trigger |

The trigger and close actions are native `<button>` elements, so Enter/Space activation follows normal browser behavior.

## Accessibility

The structure follows the WAI-ARIA dialog (modal) pattern.

- The trigger is a native `<button>` with `aria-haspopup="dialog"`, `aria-expanded`, and `aria-controls` pointing at the panel.
- The panel is `role="dialog"` with `aria-modal="true"` in modal mode. `DialogTitle` / `DialogDescription` register themselves, and the panel wires `aria-labelledby` / `aria-describedby` only when they are present — a dialog without a visible title must pass `aria-label` to `DialogContent` (the attributes are omitted, never left pointing at nothing). Confirmation-style dialogs can pass `role="alertdialog"` through `DialogContent`.
- Focus is real DOM focus: opening moves focus into the dialog, Tab is trapped while modal, and closing restores focus to the trigger — focus is never left on an unmounted element (the restore target is checked against `isConnected`).
- The background is unreachable while modal: the overlay blocks pointer interaction, the focus trap blocks keyboard access, and `aria-modal` tells assistive technology the rest of the page is inert.
- Disabled actions carry the native `disabled` attribute, which assistive technology announces as unavailable.

Without `aria-modal`, screen-reader users can still reach the page behind the panel — matching the actual, non-blocking behavior. Because there is no focus trap, keyboard users can Tab out of the panel at any time.

## States

- **Trigger (idle / open)** — per the shared control system; `aria-expanded` reflects the panel.
- **Panel** — same surface/border/elevation geometry as the modal dialog, centered; no overlay behind it, so the page remains visible and interactive.
- **Page** — never scroll-locked; clicking outside the panel dismisses it.

## Responsive Behavior

The panel is `width: calc(100vw - 2rem)` up to `max-w-lg` (512px, inside the 400–640px dialog token range) and capped at `max-height: calc(100dvh - 2rem)`, so it stays inside the viewport at every width from 375px up — including small landscape screens — without page overflow. Long content scrolls inside a `min-h-0 flex-1 overflow-y-auto` body region while the header and footer stay pinned (see `dialog-scrollable`). Footer actions stack full-width below `sm` and lay out inline from `sm` up. The trigger keeps the shared 36px control height — a comfortable touch target — at every breakpoint.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This dialog variant uses the semantic color, radius, shadow, typography, and motion tokens — including `color.overlay` for the backdrop and the Dialog row of the component token rules (radius-md, shadow-lg).

## Notes

The demo page is intentionally tall: while the non-modal panel is open the page keeps scrolling, and clicking the background dismisses the panel.
