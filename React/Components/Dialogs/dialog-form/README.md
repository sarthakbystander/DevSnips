# Dialog with Form

A real `<form>` inside the dialog: labelled native inputs, native constraint validation (submit is blocked while invalid), and the dialog closes only after a successful submit.

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
} from "./dialog-form";

const [open, setOpen] = useState(false);

<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger>Invite member</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Invite a member</DialogTitle>
      <DialogDescription>They will receive an email invitation.</DialogDescription>
    </DialogHeader>
    <form
      className="contents"
      onSubmit={(event) => {
        event.preventDefault();
        invite(new FormData(event.currentTarget));
        setOpen(false);
      }}
    >
      <div className="space-y-4 px-5 py-4">
        <label htmlFor="email">Work email</label>
        <input id="email" name="email" type="email" required />
      </div>
      <DialogFooter>
        <DialogClose>Cancel</DialogClose>
        <button type="submit">Send invite</button>
      </DialogFooter>
    </form>
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
} from "./dialog-form";

const [open, setOpen] = useState(false);

<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger>Invite member</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Invite a member</DialogTitle>
      <DialogDescription>They will receive an email invitation.</DialogDescription>
    </DialogHeader>
    <form
      className="contents"
      onSubmit={(event) => {
        event.preventDefault();
        invite(new FormData(event.currentTarget));
        setOpen(false);
      }}
    >
      <div className="space-y-4 px-5 py-4">
        <label htmlFor="email">Work email</label>
        <input id="email" name="email" type="email" required />
      </div>
      <DialogFooter>
        <DialogClose>Cancel</DialogClose>
        <button type="submit">Send invite</button>
      </DialogFooter>
    </form>
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

The form is a plain `<form className="contents">` wrapping the body and footer, so the submit button participates in native form semantics while the dialog layout is unchanged. Pair it with controlled state: the submit handler decides when to close, after native validation has passed.

## Dialog Behavior

Native constraint validation does the work: with `type="email"` + `required`, the browser blocks the submit (and shows its validation message) while the value is invalid — the dialog stays open. `onSubmit` only fires once the form is valid, where the showcase reads `FormData` and closes the dialog via controlled state.

Do not make the submit button a `DialogClose`: a close action fires on click, before validation. The submit button is a plain `<button type="submit">`; only Cancel is a `DialogClose`.

Opening focuses the first field (the first focusable element), so keyboard and screen-reader users land directly in the form. Escape and the corner close discard the draft input and close.

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

Every field has a visible `<label htmlFor>`; validation feedback comes from the native constraint-validation UI, which assistive technology announces. The invite submit is a real submit button — Enter in a field submits the form.

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

The demo uses controlled state for the submit-closes flow; the fields themselves are uncontrolled native inputs read through `FormData` on submit.
