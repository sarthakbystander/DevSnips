# Nested Dialogs

A dialog opening another dialog: a member-removal confirmation stacked over the share dialog, with Escape closing only the top-most and focus restoring down the chain.

## Usage

```tsx
import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog-nested";

// The nested dialog is composed inside the parent's content:
<Dialog>
  <DialogTrigger>Share project</DialogTrigger>
  <DialogContent>
    <DialogHeader><DialogTitle>Share “Design system”</DialogTitle></DialogHeader>

    <Dialog> {/* nested root, one DialogTrigger per row */}
      {members.map((m) => (
        <DialogTrigger key={m.id} onClick={() => setTarget(m)}>Remove</DialogTrigger>
      ))}
      <DialogContent role="alertdialog" className="max-w-md">
        <DialogHeader>
          <DialogTitle>Remove {target?.name}?</DialogTitle>
          <DialogDescription>They will lose access immediately.</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <DialogClose>Keep member</DialogClose>
          <DialogClose variant="destructive" onClick={removeTarget}>Remove member</DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
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
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog-nested";

// The nested dialog is composed inside the parent's content:
<Dialog>
  <DialogTrigger>Share project</DialogTrigger>
  <DialogContent>
    <DialogHeader><DialogTitle>Share “Design system”</DialogTitle></DialogHeader>

    <Dialog> {/* nested root, one DialogTrigger per row */}
      {members.map((m) => (
        <DialogTrigger key={m.id} onClick={() => setTarget(m)}>Remove</DialogTrigger>
      ))}
      <DialogContent role="alertdialog" className="max-w-md">
        <DialogHeader>
          <DialogTitle>Remove {target?.name}?</DialogTitle>
          <DialogDescription>They will lose access immediately.</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <DialogClose>Keep member</DialogClose>
          <DialogClose variant="destructive" onClick={removeTarget}>Remove member</DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
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

The nested dialog is an ordinary `<Dialog>` root composed inside the parent's `DialogContent` — no special API. Because each root has its own context, the nested trigger/content wire to the nested root, and both panels portal to `document.body` in open order, so the nested layer always paints above the parent. The nested confirmation is narrowed with `className="max-w-md"` so the stacked layers read clearly.

## Dialog Behavior

Three pieces of the core cooperate to make nesting safe:

- **The module-level open stack** — every open dialog registers itself; Escape closes only the last (top-most) entry, so Escape in a nested confirmation never closes the parent behind it.
- **The shared scroll-lock counter** — body scroll stays locked until every open dialog has closed; closing the nested dialog never unlocks the page early.
- **Per-root focus memory** — each dialog remembers the element focused when it opened. Closing the nested dialog restores focus to the Remove button inside the parent; closing the parent later restores focus to the page trigger. If the remembered element was unmounted in the meantime (a removed member row), the restore is skipped instead of throwing.

The parent's focus trap is scoped to its own DOM subtree, so while focus lives in the nested panel the parent trap stays out of the way.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the dialog, focus the first focusable element inside |
| `Tab` (modal dialog) | Move to the next focusable element; wraps from the last element back to the first |
| `Shift+Tab` (modal dialog) | Move to the previous focusable element; wraps from the first element to the last |
| `Escape` | Close the top-most open dialog and restore focus to its trigger |
| `Tab` (non-modal dialog) | Moves forward naturally — the page stays reachable |

The trigger and every action are native `<button>` elements, so Enter/Space activation follows normal browser behavior. Disabled actions use the native `disabled` attribute: they are skipped by Tab and cannot be activated.

## Accessibility

The structure follows the WAI-ARIA dialog (modal) pattern.

- The trigger is a native `<button>` with `aria-haspopup="dialog"`, `aria-expanded`, and `aria-controls` pointing at the panel.
- The panel is `role="dialog"` with `aria-modal="true"` in modal mode. `DialogTitle` / `DialogDescription` register themselves, and the panel wires `aria-labelledby` / `aria-describedby` only when they are present — a dialog without a visible title must pass `aria-label` to `DialogContent` (the attributes are omitted, never left pointing at nothing). Confirmation-style dialogs can pass `role="alertdialog"` through `DialogContent`.
- Focus is real DOM focus: opening moves focus into the dialog, Tab is trapped while modal, and closing restores focus to the trigger — focus is never left on an unmounted element (the restore target is checked against `isConnected`).
- The background is unreachable while modal: the overlay blocks pointer interaction, the focus trap blocks keyboard access, and `aria-modal` tells assistive technology the rest of the page is inert.
- Disabled actions carry the native `disabled` attribute, which assistive technology announces as unavailable.

Each layer is a complete `role="dialog"` (the nested one `role="alertdialog"`) with its own label; the nested overlay blocks interaction with the parent behind it, and focus never lands on an unmounted element — the restore target is checked with `isConnected`.

## States

- **Trigger (idle)** — bordered surface button per the shared control system (36px, radius-sm, `shadow-xs`).
- **Trigger (open)** — `aria-expanded="true"`; keeps the hover surface.
- **Overlay (modal)** — `var(--ds-color-overlay)` backdrop covering the viewport; pointer down on it closes the dialog.
- **Panel** — `--ds-color-surface-elevated` with a 1px `--ds-color-border` and the `--ds-shadow-lg` elevation, radius-md, centered, capped at `100dvh - 2rem` with internal column layout, per the Dialog token rules.
- **Title / description** — heading-md (18px, 600) on foreground; body-sm on `--ds-color-muted-foreground`.
- **Footer actions** — full-width stacked below `sm`, right-aligned inline from `sm` up.
- **Disabled actions** — native `disabled`: 50% opacity, no pointer events, out of the tab order.

## Responsive Behavior

The panel is `width: calc(100vw - 2rem)` up to `max-w-lg` (512px, inside the 400–640px dialog token range) and capped at `max-height: calc(100dvh - 2rem)`, so it stays inside the viewport at every width from 375px up — including small landscape screens — without page overflow. Long content scrolls inside a `min-h-0 flex-1 overflow-y-auto` body region while the header and footer stay pinned (see `dialog-scrollable`). Footer actions stack full-width below `sm` and lay out inline from `sm` up. The trigger keeps the shared 36px control height — a comfortable touch target — at every breakpoint.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This dialog variant uses the semantic color, radius, shadow, typography, and motion tokens — including `color.overlay` for the backdrop and the Dialog row of the component token rules (radius-md, shadow-lg).

## Notes

Removing a member deletes its row (including the button that opened the nested dialog); the focus-restore guard detects the disconnected node and leaves focus placement to the browser rather than focusing a dead element.
