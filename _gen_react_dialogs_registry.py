"""Registry for the DevSnips React Dialogs generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference ``dialog/code.tsx``). The
generator (``_gen_react_dialogs.py``) combines these with the reference
``code.tsx`` on disk to write ``code.tsx`` (derived), ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented demo content only (projects, drafts, releases,
repositories, members, API tokens, keyboard shortcuts). No lorem ipsum, no
marketing buzzwords.
"""
from _gen_react_dialogs import (
    register,
    LOGIC_BASE,
    KEYBOARD_BASE,
    STATES_BASE,
    RESPONSIVE_BASE,
)

TAGS_BASE = ["dialog", "modal", "react", "tailwind", "accessible", "keyboard", "focus-trap", "responsive", "interactive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "role=dialog semantics", "focus trap", "focus restoration", "scroll lock", "Escape to close"]
A11Y_BASE = ['aria-haspopup="dialog" trigger', 'role="dialog" panel', "aria-modal when modal", "aria-labelledby + aria-describedby wiring", "focus trap while modal", "focus restoration on close", "Escape closes the top-most dialog"]

# Shared props tables. The eight primitives carry the same API family-wide.
DIALOG_PROPS = r"""### `<Dialog>`

| Name | Type | Default | Description |
|---|---|---|---|
| `open` | `boolean` | — | Open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial open state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the dialog requests to open or close. |
| `modal` | `boolean` | `true` | Modal behavior: overlay, scroll lock, focus trap, `aria-modal`. `false` renders a non-modal floating panel (no overlay; closes on Escape / outside pointer down). |
| `children` | `ReactNode` | — | `DialogTrigger` + `DialogContent`. |"""

TRIGGER_PROPS = r"""### `<DialogTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Visible trigger label. |

A real `<button type="button">` with `aria-haspopup="dialog"` + `aria-expanded`; every native button attribute (`disabled`, `aria-label`, …) is forwarded. Focus is restored here when the dialog closes."""

CONTENT_PROPS = r"""### `<DialogContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="dialog"` panel (e.g. a larger `max-w-*`). |
| `children` | `ReactNode` | — | Header, body content, footer, close button. |

Portaled to `document.body` and rendered only while open. Labelled by `DialogTitle` / described by `DialogDescription` automatically when they are rendered; pass `aria-label` when a dialog intentionally has no visible title, and `role="alertdialog"` for confirmation dialogs (forwarded via `...rest`)."""

HEADER_PROPS = r"""### `<DialogHeader>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the header. |
| `children` | `ReactNode` | — | `DialogTitle` + `DialogDescription`. |"""

TITLE_PROPS = r"""### `<DialogTitle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<h2>`. |
| `children` | `ReactNode` | — | Title text. |

Registers itself so `DialogContent` sets `aria-labelledby` only while a title exists."""

DESCRIPTION_PROPS = r"""### `<DialogDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Supporting description text. |

Registers itself so `DialogContent` sets `aria-describedby` only while a description exists."""

FOOTER_PROPS = r"""### `<DialogFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the action row. |
| `children` | `ReactNode` | — | Footer actions (`DialogClose`, plain buttons, links). |

Buttons stack full-width below `sm` and lay out right-aligned inline from `sm` up."""

CLOSE_PROPS = r"""### `<DialogClose>`

| Name | Type | Default | Description |
|---|---|---|---|
| `variant` | `"outline" \| "primary" \| "destructive" \| "ghost"` | `"outline"` | `outline` is the bordered footer cancel action; `primary` / `destructive` are confirming actions that also close; `ghost` is the icon-sized corner close button (positioned absolute top-right — give it an `aria-label` such as `"Close"`). |
| `onClick` | `(event) => void` | — | Called before the dialog closes; `event.preventDefault()` keeps the dialog open. |
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Visible label (or the close icon for `ghost`). |

A real `<button type="button">` that requests close; every native button attribute is forwarded."""


def props_table():
    return "\n\n".join([
        DIALOG_PROPS, TRIGGER_PROPS, CONTENT_PROPS, HEADER_PROPS,
        TITLE_PROPS, DESCRIPTION_PROPS, FOOTER_PROPS, CLOSE_PROPS,
    ])


# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = """const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const CARD = "rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4";
const ROW = "flex items-center justify-between gap-4";
const ROW_NAME = "m-0 text-sm font-medium text-[var(--ds-color-foreground)]";
const ROW_META = "m-0 text-xs text-[var(--ds-color-muted-foreground)]";
const BTN_PRIMARY = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_OUTLINE = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const FIELD_LABEL = "mb-1.5 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]";
const INPUT = "h-9 w-full rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-sm leading-5 text-[var(--ds-color-foreground)] placeholder:text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
"""


# 1. dialog (reference)
register(
    "dialog",
    title="Dialog",
    subcategory="Core",
    description="The canonical modal dialog: a real menu of compound parts — trigger, portaled role=dialog panel, header/title/description, footer actions, corner close — with focus trap, Escape, scroll lock, and focus restoration.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["dialog-controlled", "dialog-confirmation", "dialog-form", "dialog-scrollable"],
    usage='''import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog";

<Dialog>
  <DialogTrigger>Edit project</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Project settings</DialogTitle>
      <DialogDescription>Changes apply to everyone in the workspace.</DialogDescription>
    </DialogHeader>
    <div className="px-5 py-4">…</div>
    <DialogFooter>
      <DialogClose>Cancel</DialogClose>
      <DialogClose variant="primary" onClick={save}>Save changes</DialogClose>
    </DialogFooter>
    <DialogClose variant="ghost" aria-label="Close dialog"><XIcon /></DialogClose>
  </DialogContent>
</Dialog>

// Uncontrolled (default) or controlled:
const [open, setOpen] = useState(false);
<Dialog open={open} onOpenChange={setOpen}>…</Dialog>

// Non-modal floating panel (no overlay, no trap, no scroll lock):
<Dialog modal={false}>…</Dialog>''',
    props_doc=props_table(),
    composition_note="This is the reference composition — every other variant in the family uses the same primitives and extends the same class constants, states, and accessibility model. The `ghost` close is rendered last inside `DialogContent` so it stays last in the tab order (its position is visual, via `absolute`).",
    logic_doc=LOGIC_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Only one dialog is expected to be open per root; mounting several `<Dialog>` roots on the same page is safe because each root scopes its own ids, focus memory, and listeners — the module-level stack only coordinates Escape order and scroll locking between roots.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Reference implementation for the Dialogs family. It establishes the shared dialog geometry (radius-md panel, max-w-lg, 20px padding rhythm, 36px controls), the overlay/elevation model, the focus-ring treatment, the portal + focus-trap + focus-restore behavior, and the nesting-safe Escape stack that every other variant extends.",
    tsx_header="",
    showcase=DEMO_HELPERS + '''
function ProjectSettings() {
  const [saved, setSaved] = React.useState(false);
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>Design system migration</p>
            <p className={ROW_META}>Internal project · Updated 2 days ago</p>
          </div>
          <Dialog>
            <DialogTrigger>Edit project</DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Project settings</DialogTitle>
                <DialogDescription>Changes apply to everyone in the workspace.</DialogDescription>
              </DialogHeader>
              <div className="space-y-3 px-5 py-4">
                <div className="flex items-center justify-between gap-4 border-b border-[var(--ds-color-border-subtle)] pb-3">
                  <div>
                    <p className="m-0 text-sm font-medium text-[var(--ds-color-foreground)]">Visibility</p>
                    <p className="m-0 text-xs text-[var(--ds-color-muted-foreground)]">Who can see this project</p>
                  </div>
                  <span className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-2 py-0.5 text-[11px] font-medium text-[var(--ds-color-muted-foreground)]">Workspace</span>
                </div>
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="m-0 text-sm font-medium text-[var(--ds-color-foreground)]">Region</p>
                    <p className="m-0 text-xs text-[var(--ds-color-muted-foreground)]">Where project data is stored</p>
                  </div>
                  <span className="rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-2 py-0.5 text-[11px] font-medium text-[var(--ds-color-muted-foreground)]">eu-central</span>
                </div>
              </div>
              <DialogFooter>
                <DialogClose>Cancel</DialogClose>
                <DialogClose variant="primary" onClick={() => setSaved(true)}>Save changes</DialogClose>
              </DialogFooter>
              <DialogClose variant="ghost" aria-label="Close dialog"><Icon name="x" className="size-4" /></DialogClose>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <p className={NOTE}>{saved ? "Saved — reopen the dialog to keep editing." : "Open the dialog, then try Tab / Shift+Tab to cycle, Escape, the overlay, or the corner close."}</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Project settings — uncontrolled</p>
        <ProjectSettings />
      </div>
    </div>
  );
}''',
)

# 2. dialog-controlled
register(
    "dialog-controlled",
    title="Dialog with Controlled State",
    subcategory="State",
    description="Open state lifted to the parent: one controlled dialog serves a whole table of API tokens, `onOpenChange` keeps the parent in sync, and a second demo shows `aria-label` labelling when no visible title is rendered.",
    tags=TAGS_BASE + ["controlled", "state"],
    features=FEAT_BASE + ["controlled open state", "onOpenChange sync", "aria-label without visible title"],
    accessibility=A11Y_BASE + ["aria-label when no DialogTitle is rendered"],
    interactive=True,
    related=["dialog", "dialog-confirmation", "dialog-destructive", "dialog-non-modal"],
    usage='''import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog-controlled";

const [open, setOpen] = useState(false);

<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger>Revoke token</DialogTrigger>
  <DialogContent>…</DialogContent>
</Dialog>

// No visible title — label the panel explicitly instead:
<DialogContent aria-label="Session details">…</DialogContent>''',
    props_doc=props_table(),
    composition_note="Controlled mode uses the exact same primitives — only the state ownership changes. The parent passes `open` + `onOpenChange`; `DialogClose`, Escape, and the overlay all route through `onOpenChange(false)`.",
    logic_doc="""With `open` + `onOpenChange` the parent is the single source of truth: the dialog never mutates its own state, and every internal close request (Escape, overlay pointer down, `DialogClose`, trigger toggle) calls `onOpenChange(false)` instead. The parent decides whether to honor it — so closing can be gated behind dirty-form checks or async work.

Controlled mode is also how one dialog serves many targets: keep `open` plus the active record in state (here, the API token being revoked), render a single `<Dialog>`, and set both from each row action.

When a dialog intentionally renders no `DialogTitle`, the `aria-labelledby` attribute is omitted entirely — pass `aria-label` to `DialogContent` so the panel still has an accessible name (the "Session details" demo below).""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="The controlled demos show both labelling paths: the revoke dialog wires `aria-labelledby`/`aria-describedby` from its `DialogTitle`/`DialogDescription`; the session dialog omits them and supplies `aria-label=\"Session details\"` instead.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Everything behavioral (portal, trap, restore, scroll lock, Escape stack) is identical to the reference — controlled vs uncontrolled changes only who owns `open`.",
    tsx_header='''/**
 * DevSnips React Dialog — Controlled State.
 *
 * The shared dialog core with the open state lifted to the parent
 * (`open` + `onOpenChange`): one controlled dialog can serve many targets,
 * close requests (Escape, overlay, DialogClose) are routed through
 * `onOpenChange(false)` so the parent decides, and a dialog without a
 * visible title is labelled via `aria-label` on `DialogContent`.
 */''',
    showcase=DEMO_HELPERS + '''
const TOKENS = [
  { name: "ci-deploy-key", scope: "deploy:write", created: "Mar 2" },
  { name: "preview-uploads", scope: "uploads:write", created: "Apr 18" },
];

function RevokeTokens() {
  const [open, setOpen] = React.useState(false);
  const [target, setTarget] = React.useState(null);
  const [lastEvent, setLastEvent] = React.useState("none");
  const [revoked, setRevoked] = React.useState([]);
  function handleOpenChange(next) {
    setOpen(next);
    setLastEvent(next ? "open" : "closed");
  }
  return (
    <div className="space-y-3">
      <div className={CARD + " divide-y divide-[var(--ds-color-border-subtle)] p-0"}>
        {TOKENS.filter((t) => !revoked.includes(t.name)).map((t) => (
          <div key={t.name} className="flex items-center justify-between gap-4 p-4">
            <div className="min-w-0">
              <p className={ROW_NAME + " font-mono text-[13px]"}>{t.name}</p>
              <p className={ROW_META}>{t.scope} · Created {t.created}</p>
            </div>
            <button
              type="button"
              className={BTN_OUTLINE + " h-8 px-2.5 text-[13px]"}
              onClick={() => { setTarget(t); setOpen(true); setLastEvent("open"); }}
            >
              Revoke
            </button>
          </div>
        ))}
        {TOKENS.filter((t) => !revoked.includes(t.name)).length === 0 ? (
          <p className="m-0 p-4 text-sm text-[var(--ds-color-muted-foreground)]">All tokens revoked.</p>
        ) : null}
      </div>
      <Dialog open={open} onOpenChange={handleOpenChange}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Revoke {target ? target.name : "token"}?</DialogTitle>
            <DialogDescription>Any integration using this token stops working immediately. This cannot be undone.</DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose>Keep token</DialogClose>
            <DialogClose variant="destructive" onClick={() => target && setRevoked((r) => r.concat(target.name))}>Revoke token</DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <p className={NOTE}>Dialog state is owned by the parent — last onOpenChange event: {lastEvent}.</p>
    </div>
  );
}

function SessionDetails() {
  const [open, setOpen] = React.useState(false);
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>Current session</p>
            <p className={ROW_META}>Signed in from Berlin · Chrome</p>
          </div>
          <button type="button" className={BTN_OUTLINE} onClick={() => setOpen(true)}>Details</button>
        </div>
      </div>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent aria-label="Session details">
          <div className="space-y-2 px-5 py-5">
            <p className="m-0 text-sm font-medium text-[var(--ds-color-foreground)]">Berlin, Germany · Chrome 126</p>
            <p className="m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">Signed in 3 hours ago. This session can read and write workspace data. Sign out on shared devices.</p>
          </div>
          <DialogFooter>
            <DialogClose variant="primary">Got it</DialogClose>
          </DialogFooter>
          <DialogClose variant="ghost" aria-label="Close dialog"><Icon name="x" className="size-4" /></DialogClose>
        </DialogContent>
      </Dialog>
      <p className={NOTE}>This dialog renders no DialogTitle — the panel is labelled by aria-label instead.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Controlled — one dialog, many row targets</p>
        <RevokeTokens />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>No visible title — aria-label</p>
        <SessionDetails />
      </div>
    </div>
  );
}''',
)

# 3. dialog-confirmation
register(
    "dialog-confirmation",
    title="Confirmation Dialog",
    subcategory="Confirmation",
    description="The proceed-or-cancel pattern as `role=\"alertdialog\"`: a focused question, the safe action focused first, and the confirming action on the trailing edge.",
    tags=TAGS_BASE + ["confirmation", "alertdialog"],
    features=FEAT_BASE + ["role=alertdialog", "safe action focused first"],
    accessibility=A11Y_BASE + ['role="alertdialog"', "initial focus on the safe action"],
    interactive=True,
    related=["dialog", "dialog-destructive", "dialog-nested", "dialog-controlled"],
    usage='''import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog-confirmation";

<Dialog>
  <DialogTrigger>Discard draft</DialogTrigger>
  <DialogContent role="alertdialog">
    <DialogHeader>
      <DialogTitle>Discard this draft?</DialogTitle>
      <DialogDescription>This will permanently delete the draft.</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <DialogClose>Keep editing</DialogClose>
      <DialogClose variant="primary" onClick={discard}>Discard draft</DialogClose>
    </DialogFooter>
  </DialogContent>
</Dialog>''',
    props_doc=props_table(),
    composition_note="A confirmation is the reference composition minus the corner close: a focused question, a short description, and two footer actions. The safe action (`Keep editing`) is first in the DOM, so it is what focus lands on when the dialog opens — the destructive path always requires a deliberate move.",
    logic_doc="""`role="alertdialog"` (forwarded through `DialogContent`'s props) tells assistive technology this is an alert requiring an immediate response; everything else — focus trap, Escape, overlay close, scroll lock, focus restoration — behaves exactly like the reference dialog.

Focus order is the safety mechanism: the cancel action is first in the DOM so opening the dialog focuses it, and the confirming action is last. On small screens the footer flips visual order (`flex-col-reverse`) so the confirming action stays visually primary while the DOM order — and therefore the focus order — is unchanged.""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Escape and the overlay both cancel the confirmation (the safe default); only activating the confirming action proceeds.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="For destructive confirmations (delete, revoke) use `dialog-destructive`, which pairs this pattern with the destructive action styling and a stronger warning presentation.",
    tsx_header='''/**
 * DevSnips React Dialog — Confirmation.
 *
 * The shared dialog core composed as a confirmation: `role="alertdialog"`,
 * a focused question with a short description, the safe action first in the
 * DOM (it receives the initial focus), and the confirming action last.
 */''',
    showcase=DEMO_HELPERS + '''
function DiscardDraft() {
  const [discarded, setDiscarded] = React.useState(false);
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>Draft: Quarterly platform report</p>
            <p className={ROW_META}>{discarded ? "Discarded just now" : "Autosaved 12 minutes ago · 1,240 words"}</p>
          </div>
          <Dialog>
            <DialogTrigger>Discard draft</DialogTrigger>
            <DialogContent role="alertdialog">
              <DialogHeader>
                <DialogTitle>Discard this draft?</DialogTitle>
                <DialogDescription>This will permanently delete the draft of “Quarterly platform report”. Published versions are not affected.</DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <DialogClose>Keep editing</DialogClose>
                <DialogClose variant="primary" onClick={() => setDiscarded(true)}>Discard draft</DialogClose>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <p className={NOTE}>Focus starts on “Keep editing” — the safe action. Escape and the overlay cancel; only “Discard draft” proceeds.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Discard confirmation — alertdialog</p>
        <DiscardDraft />
      </div>
    </div>
  );
}''',
)

# 4. dialog-destructive
register(
    "dialog-destructive",
    title="Destructive Dialog",
    subcategory="Confirmation",
    description="The destructive confirmation pattern: `role=\"alertdialog\"`, a warning presentation in the semantic destructive tokens, Cancel focused first, and the destructive action styled with the destructive button treatment.",
    tags=TAGS_BASE + ["destructive", "alertdialog", "delete"],
    features=FEAT_BASE + ["role=alertdialog", "destructive action styling", "warning presentation"],
    accessibility=A11Y_BASE + ['role="alertdialog"', "initial focus on Cancel", "destructive state not conveyed by color alone"],
    interactive=True,
    related=["dialog", "dialog-confirmation", "dialog-nested", "dialog-form"],
    usage='''import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog-destructive";

<Dialog>
  <DialogTrigger>Delete repository</DialogTrigger>
  <DialogContent role="alertdialog">
    <DialogHeader>
      <DialogTitle>Delete this repository?</DialogTitle>
      <DialogDescription>All branches, releases, and settings will be permanently removed.</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <DialogClose>Cancel</DialogClose>
      <DialogClose variant="destructive" onClick={deleteRepo}>Delete repository</DialogClose>
    </DialogFooter>
  </DialogContent>
</Dialog>''',
    props_doc=props_table(),
    composition_note="The destructive confirmation adds a warning row ahead of the title — an icon in a `--ds-color-destructive-soft` chip plus consequence copy — and uses `variant=\"destructive\"` on the confirming `DialogClose`. The icon chip is `aria-hidden`; the destructive nature is carried by the words, never by color alone.",
    logic_doc="""Like the plain confirmation, `role="alertdialog"` is forwarded through `DialogContent` and the safe action (`Cancel`) is first in the DOM so it receives the initial focus. The destructive action is a `DialogClose variant="destructive"`: it runs its `onClick` (the deletion) and then closes the dialog through the same close path as every other action.

Escape and the overlay cancel — a destructive action can never be triggered by accident while moving through the interface.""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="The destructive action is exposed in words (“Delete repository”), not color alone; the warning icon is aria-hidden decoration in a destructive-soft chip.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="For non-destructive proceed/cancel flows use `dialog-confirmation`; for nested destructive confirms inside another dialog see `dialog-nested`.",
    tsx_header='''/**
 * DevSnips React Dialog — Destructive.
 *
 * The shared dialog core composed as a destructive confirmation:
 * `role="alertdialog"`, a warning presentation in the semantic destructive
 * tokens, Cancel first in the DOM (initial focus), and the confirming
 * action styled with `DialogClose variant="destructive"`.
 */''',
    showcase=DEMO_HELPERS + '''
function DeleteRepository() {
  const [deleted, setDeleted] = React.useState(false);
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME + " font-mono text-[13px]"}>devsnips/design-system</p>
            <p className={ROW_META}>{deleted ? "Scheduled for deletion" : "Private repository · 214 MB · 38 branches"}</p>
          </div>
          <Dialog>
            <DialogTrigger>Delete</DialogTrigger>
            <DialogContent role="alertdialog">
              <div className="flex items-start gap-3 px-5 pt-5">
                <span aria-hidden="true" className="inline-flex size-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-md)] bg-[var(--ds-color-destructive-soft)] text-[var(--ds-color-destructive)]">
                  <Icon name="alert-triangle" className="size-4" />
                </span>
                <DialogHeader className="px-0 pt-0.5">
                  <DialogTitle>Delete this repository?</DialogTitle>
                  <DialogDescription>All branches, releases, and settings of devsnips/design-system will be permanently removed. This cannot be undone.</DialogDescription>
                </DialogHeader>
              </div>
              <DialogFooter>
                <DialogClose>Cancel</DialogClose>
                <DialogClose variant="destructive" onClick={() => setDeleted(true)}>Delete repository</DialogClose>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <p className={NOTE}>Focus starts on Cancel. The warning icon is decorative — the words carry the meaning.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Delete confirmation — alertdialog + destructive action</p>
        <DeleteRepository />
      </div>
    </div>
  );
}''',
)

# 5. dialog-form
register(
    "dialog-form",
    title="Dialog with Form",
    subcategory="Composite",
    description="A real `<form>` inside the dialog: labelled native inputs, native constraint validation (submit is blocked while invalid), and the dialog closes only after a successful submit.",
    tags=TAGS_BASE + ["form", "inputs", "validation"],
    features=FEAT_BASE + ["real form element", "native constraint validation", "submit closes after validation"],
    accessibility=A11Y_BASE + ["labelled native inputs", "native validation messages", "initial focus on the first field"],
    interactive=True,
    related=["dialog", "dialog-controlled", "dialog-destructive", "dialog-scrollable"],
    usage='''import Dialog, {
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
</Dialog>''',
    props_doc=props_table(),
    composition_note="The form is a plain `<form className=\"contents\">` wrapping the body and footer, so the submit button participates in native form semantics while the dialog layout is unchanged. Pair it with controlled state: the submit handler decides when to close, after native validation has passed.",
    logic_doc="""Native constraint validation does the work: with `type="email"` + `required`, the browser blocks the submit (and shows its validation message) while the value is invalid — the dialog stays open. `onSubmit` only fires once the form is valid, where the showcase reads `FormData` and closes the dialog via controlled state.

Do not make the submit button a `DialogClose`: a close action fires on click, before validation. The submit button is a plain `<button type="submit">`; only Cancel is a `DialogClose`.

Opening focuses the first field (the first focusable element), so keyboard and screen-reader users land directly in the form. Escape and the corner close discard the draft input and close.""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Every field has a visible `<label htmlFor>`; validation feedback comes from the native constraint-validation UI, which assistive technology announces. The invite submit is a real submit button — Enter in a field submits the form.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo uses controlled state for the submit-closes flow; the fields themselves are uncontrolled native inputs read through `FormData` on submit.",
    tsx_header='''/**
 * DevSnips React Dialog — Form.
 *
 * The shared dialog core composed with a real `<form>`: labelled native
 * inputs, native constraint validation (submit is blocked while invalid),
 * and controlled open state so the dialog closes only after a successful
 * submit. Focus lands on the first field when the dialog opens.
 */''',
    showcase=DEMO_HELPERS + '''
function InviteMember() {
  const [open, setOpen] = React.useState(false);
  const [sent, setSent] = React.useState("");
  function handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setSent(String(data.get("email") || ""));
    setOpen(false);
  }
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>Workspace members</p>
            <p className={ROW_META}>{sent ? ("Invite sent to " + sent) : "14 members · 2 pending invites"}</p>
          </div>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger>Invite member</DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Invite a member</DialogTitle>
                <DialogDescription>They will receive an email with a link to join this workspace.</DialogDescription>
              </DialogHeader>
              <form className="contents" onSubmit={handleSubmit}>
                <div className="space-y-4 px-5 py-4">
                  <div>
                    <label className={FIELD_LABEL} htmlFor="dsf-email">Work email</label>
                    <input className={INPUT} id="dsf-email" name="email" type="email" required placeholder="name@company.com" autoComplete="off" />
                  </div>
                  <div>
                    <label className={FIELD_LABEL} htmlFor="dsf-role">Role</label>
                    <select className={INPUT} id="dsf-role" name="role" defaultValue="member">
                      <option value="member">Member — can create and edit projects</option>
                      <option value="admin">Admin — can also manage members and billing</option>
                      <option value="viewer">Viewer — read-only access</option>
                    </select>
                  </div>
                </div>
                <DialogFooter>
                  <DialogClose>Cancel</DialogClose>
                  <button type="submit" className={BTN_PRIMARY}>Send invite</button>
                </DialogFooter>
              </form>
              <DialogClose variant="ghost" aria-label="Close dialog"><Icon name="x" className="size-4" /></DialogClose>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <p className={NOTE}>Native validation: submit with an empty or invalid email and the dialog stays open. Focus lands on the email field.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Invite member — real form + validation</p>
        <InviteMember />
      </div>
    </div>
  );
}''',
)

# 6. dialog-scrollable
register(
    "dialog-scrollable",
    title="Scrollable Dialog",
    subcategory="Layout",
    description="Long content in a pinned-header/pinned-footer layout: the body region scrolls internally while the panel stays capped inside the viewport.",
    tags=TAGS_BASE + ["scrollable", "long-content", "layout"],
    features=FEAT_BASE + ["internal body scrolling", "pinned header + footer", "viewport-capped panel"],
    accessibility=A11Y_BASE + ["scrollable region reachable by keyboard"],
    interactive=True,
    related=["dialog", "dialog-form", "dialog-with-custom-footer", "dialog-non-modal"],
    usage='''import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog-scrollable";

<Dialog>
  <DialogTrigger>View changelog</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Changelog</DialogTitle>
      <DialogDescription>Every release of the design system package.</DialogDescription>
    </DialogHeader>
    <div className="min-h-0 flex-1 overflow-y-auto border-y border-[var(--ds-color-border-subtle)] px-5 py-4">
      …long content…
    </div>
    <DialogFooter>
      <DialogClose>Close</DialogClose>
    </DialogFooter>
  </DialogContent>
</Dialog>''',
    props_doc=props_table(),
    composition_note="`DialogContent` is already a capped-height flex column (`max-h-[calc(100dvh-2rem)]` + `overflow-hidden`). The scrollable pattern is one composition class on the body region: `min-h-0 flex-1 overflow-y-auto`, plus hairline `border-y` separators so the pinned header and footer read as fixed regions.",
    logic_doc="""The panel never grows past the viewport: `max-height: calc(100dvh - 2rem)` caps it and the flex column keeps the header and footer at their natural height while the body region takes the remaining space (`flex-1`) and scrolls (`overflow-y-auto`). `min-h-0` is required — without it a flex child refuses to shrink below its content size and the panel would overflow instead of scrolling.

The body scroll region is an ordinary overflow container: mouse, touch, and keyboard (focus a control inside, or arrow keys once it has focus) all scroll natively. Body scroll remains locked behind the dialog — only the dialog body scrolls.""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="The header (with the title that labels the dialog) and the footer actions remain visible and reachable at all times while the body scrolls; Tab order follows the DOM — header, body content, footer, corner close.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Content is a generated release log; the point of the demo is the scroll mechanics, so the list is deliberately long enough to overflow at every QA viewport height (900px and below).",
    tsx_header='''/**
 * DevSnips React Dialog — Scrollable.
 *
 * The shared dialog core composed for long content: the panel is a
 * viewport-capped flex column, the body region is a
 * `min-h-0 flex-1 overflow-y-auto` container, and the header + footer stay
 * pinned while the body scrolls internally.
 */''',
    showcase=DEMO_HELPERS + '''
const RELEASES = [
  { v: "2.4.0", d: "Aug 12", items: ["Dialog, Toast, and Tooltip promoted to stable", "Focus ring token unified across overlay components", "Fixed table header offset in sticky mode"] },
  { v: "2.3.1", d: "Jul 28", items: ["Patch: pagination windowing at page boundaries", "Patch: select typeahead with diacritics"] },
  { v: "2.3.0", d: "Jul 15", items: ["Segmented button radiogroup semantics", "Reduced-motion guards on every transition", "Dark surface-elevated token adjusted"] },
  { v: "2.2.0", d: "Jun 30", items: ["Tabs vertical orientation + scrollable lists", "Breadcrumb collapse and max-width patterns"] },
  { v: "2.1.2", d: "Jun 16", items: ["Patch: checkbox indeterminate in Firefox", "Patch: radio arrow-key wrapping"] },
  { v: "2.1.0", d: "Jun 2", items: ["Switch loading state without layout shift", "Textarea auto-resize with font-load re-measure"] },
  { v: "2.0.0", d: "May 19", items: ["TypeScript-first rewrite of every component", "Tailwind token consumption via arbitrary values", "JSX parity build for every component"] },
  { v: "1.9.0", d: "May 5", items: ["Command button global shortcut", "Pagination page-size selector"] },
  { v: "1.8.1", d: "Apr 21", items: ["Patch: dropdown submenu edge flip"] },
  { v: "1.8.0", d: "Apr 7", items: ["Dropdown checkboxes + radio groups", "Destructive menu item tone split"] },
];

function Changelog() {
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME + " font-mono text-[13px]"}>@devsnips/react</p>
            <p className={ROW_META}>Current version 2.4.0 · 42 releases total</p>
          </div>
          <Dialog>
            <DialogTrigger>View changelog</DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Changelog</DialogTitle>
                <DialogDescription>Recent releases of @devsnips/react.</DialogDescription>
              </DialogHeader>
              <div className="min-h-0 flex-1 overflow-y-auto border-y border-[var(--ds-color-border-subtle)] px-5 py-4">
                <ol className="m-0 list-none space-y-5 p-0">
                  {RELEASES.map((r) => (
                    <li key={r.v}>
                      <div className="flex items-baseline justify-between gap-4">
                        <p className="m-0 font-mono text-[13px] font-medium text-[var(--ds-color-foreground)]">{r.v}</p>
                        <p className="m-0 text-xs text-[var(--ds-color-muted-foreground)]">{r.d}</p>
                      </div>
                      <ul className="m-0 mt-1.5 list-disc space-y-0.5 pl-4 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
                        {r.items.map((item) => <li key={item}>{item}</li>)}
                      </ul>
                    </li>
                  ))}
                </ol>
              </div>
              <DialogFooter className="sm:items-center sm:justify-between">
                <span className="inline-flex items-center gap-1.5 text-xs text-[var(--ds-color-muted-foreground)]"><Icon name="clock" className="size-3.5" aria-hidden="true" />Release notes emailed monthly</span>
                <DialogClose>Close</DialogClose>
              </DialogFooter>
              <DialogClose variant="ghost" aria-label="Close dialog"><Icon name="x" className="size-4" /></DialogClose>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <p className={NOTE}>The body scrolls internally; the header and footer stay pinned, and the page behind stays locked.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Changelog — pinned header/footer, scrolling body</p>
        <Changelog />
      </div>
    </div>
  );
}''',
)

# 7. dialog-nested
register(
    "dialog-nested",
    title="Nested Dialogs",
    subcategory="Composite",
    description="A dialog opening another dialog: a member-removal confirmation stacked over the share dialog, with Escape closing only the top-most and focus restoring down the chain.",
    tags=TAGS_BASE + ["nested", "stacked", "confirmation"],
    features=FEAT_BASE + ["nested dialogs", "top-most Escape handling", "focus restore chain"],
    accessibility=A11Y_BASE + ["Escape closes only the top-most dialog", "focus restores into the parent dialog"],
    interactive=True,
    related=["dialog", "dialog-destructive", "dialog-confirmation", "dialog-controlled"],
    usage='''import Dialog, {
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
</Dialog>''',
    props_doc=props_table(),
    composition_note="The nested dialog is an ordinary `<Dialog>` root composed inside the parent's `DialogContent` — no special API. Because each root has its own context, the nested trigger/content wire to the nested root, and both panels portal to `document.body` in open order, so the nested layer always paints above the parent. The nested confirmation is narrowed with `className=\"max-w-md\"` so the stacked layers read clearly.",
    logic_doc="""Three pieces of the core cooperate to make nesting safe:

- **The module-level open stack** — every open dialog registers itself; Escape closes only the last (top-most) entry, so Escape in a nested confirmation never closes the parent behind it.
- **The shared scroll-lock counter** — body scroll stays locked until every open dialog has closed; closing the nested dialog never unlocks the page early.
- **Per-root focus memory** — each dialog remembers the element focused when it opened. Closing the nested dialog restores focus to the Remove button inside the parent; closing the parent later restores focus to the page trigger. If the remembered element was unmounted in the meantime (a removed member row), the restore is skipped instead of throwing.

The parent's focus trap is scoped to its own DOM subtree, so while focus lives in the nested panel the parent trap stays out of the way.""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Each layer is a complete `role=\"dialog\"` (the nested one `role=\"alertdialog\"`) with its own label; the nested overlay blocks interaction with the parent behind it, and focus never lands on an unmounted element — the restore target is checked with `isConnected`.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Removing a member deletes its row (including the button that opened the nested dialog); the focus-restore guard detects the disconnected node and leaves focus placement to the browser rather than focusing a dead element.",
    tsx_header='''/**
 * DevSnips React Dialog — Nested.
 *
 * The shared dialog core composed two layers deep: a confirmation dialog
 * stacked over its parent. The module-level open stack makes Escape close
 * only the top-most dialog, the shared scroll-lock counter keeps the page
 * locked until every dialog closes, and each root restores focus to the
 * element that opened it.
 */''',
    showcase=DEMO_HELPERS + '''
const INITIAL_MEMBERS = [
  { id: "m1", name: "Ada Lindqvist", email: "ada@devsnips.io", role: "Owner" },
  { id: "m2", name: "Marcus Chen", email: "marcus@devsnips.io", role: "Editor" },
  { id: "m3", name: "Priya Nair", email: "priya@devsnips.io", role: "Viewer" },
];

function ShareProject() {
  const [members, setMembers] = React.useState(INITIAL_MEMBERS);
  const [target, setTarget] = React.useState(null);
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>Design system migration</p>
            <p className={ROW_META}>{members.length} members with access</p>
          </div>
          <Dialog>
            <DialogTrigger>Share project</DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Share “Design system migration”</DialogTitle>
                <DialogDescription>Everyone listed here can open the project. Removing a member revokes their access immediately.</DialogDescription>
              </DialogHeader>
              <Dialog>
                <div className="px-5 py-4">
                  <ul className="m-0 list-none space-y-2 p-0">
                    {members.map((m) => (
                      <li key={m.id} className="flex items-center gap-3 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-subtle)] px-3 py-2">
                        <span aria-hidden="true" className="inline-flex size-8 shrink-0 items-center justify-center rounded-full bg-[var(--ds-color-surface-active)] text-[11px] font-semibold text-[var(--ds-color-foreground)]">{m.name.split(" ").map((p) => p[0]).join("")}</span>
                        <span className="min-w-0 flex-1">
                          <span className="block truncate text-sm font-medium text-[var(--ds-color-foreground)]">{m.name}</span>
                          <span className="block truncate text-xs text-[var(--ds-color-muted-foreground)]">{m.email} · {m.role}</span>
                        </span>
                        {m.role !== "Owner" ? (
                          <DialogTrigger className="h-8 px-2.5 text-[13px]" onClick={() => setTarget(m)}>Remove</DialogTrigger>
                        ) : (
                          <span className="px-2.5 text-xs text-[var(--ds-color-muted-foreground)]">Owner</span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
                <DialogContent role="alertdialog" className="max-w-md">
                  <DialogHeader>
                    <DialogTitle>Remove {target ? target.name : "member"}?</DialogTitle>
                    <DialogDescription>{target ? target.email : "They"} will lose access to “Design system migration” immediately. You can invite them again later.</DialogDescription>
                  </DialogHeader>
                  <DialogFooter>
                    <DialogClose>Keep member</DialogClose>
                    <DialogClose variant="destructive" onClick={() => target && setMembers((list) => list.filter((m) => m.id !== target.id))}>Remove member</DialogClose>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
              <DialogFooter>
                <DialogClose variant="primary">Done</DialogClose>
              </DialogFooter>
              <DialogClose variant="ghost" aria-label="Close dialog"><Icon name="x" className="size-4" /></DialogClose>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <p className={NOTE}>Open a member’s Remove confirmation, then press Escape: only the confirmation closes. Escape again closes the share dialog.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Share dialog with nested remove confirmation</p>
        <ShareProject />
      </div>
    </div>
  );
}''',
)

# 8. dialog-with-custom-footer
register(
    "dialog-with-custom-footer",
    title="Dialog with Custom Footer",
    subcategory="Layout",
    description="The footer as a free composition area: a real checklist link and draft metadata on the leading edge, cancel/publish actions on the trailing edge.",
    tags=TAGS_BASE + ["footer", "layout", "composition"],
    features=FEAT_BASE + ["split footer layout", "footer link + metadata", "stacked on small screens"],
    accessibility=A11Y_BASE + ["footer link is a real anchor", "focus order follows the DOM"],
    interactive=True,
    related=["dialog", "dialog-scrollable", "dialog-form", "dialog-confirmation"],
    usage='''import Dialog, {
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "./dialog-with-custom-footer";

<DialogFooter className="sm:items-center sm:justify-between">
  <div className="flex items-center gap-3">
    <a href="#checklist">View release checklist</a>
    <span>Draft saved 2 min ago</span>
  </div>
  <div className="flex gap-2">
    <DialogClose>Cancel</DialogClose>
    <DialogClose variant="primary" onClick={publish}>Publish release</DialogClose>
  </div>
</DialogFooter>''',
    props_doc=props_table(),
    composition_note="`DialogFooter` is a plain flex container — the default right-aligned action row is just its base classes. This variant overrides the `sm` justification (`sm:justify-between`) and composes two groups inside: a leading link/metadata cluster and the trailing action pair. Below `sm` the column layout stacks both groups naturally.",
    logic_doc="""Everything behavioral is the reference dialog; only the footer composition differs. The checklist link is a real `<a href>` — it participates in the focus trap like any other focusable element and activates with normal browser navigation.

When overriding the footer, keep the action pair in a trailing `<div className=\"flex gap-2\">` rather than restyling the buttons — the `DialogClose` variants already carry the correct action styling.""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="The checklist link is a real anchor with an href (keyboard-focusable, announced as a link); the draft timestamp is supplementary text, not required to understand the actions.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Footer composition is deliberately un-opinionated: any content can live there. This variant documents the one pattern every product eventually needs — navigation/metadata on the left, actions on the right.",
    tsx_header='''/**
 * DevSnips React Dialog — Custom Footer.
 *
 * The shared dialog core with the footer used as a free composition area:
 * a real link and draft metadata on the leading edge, cancel/publish
 * actions on the trailing edge, stacked on small screens.
 */''',
    showcase=DEMO_HELPERS + '''
function PublishRelease() {
  const [published, setPublished] = React.useState(false);
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME + " font-mono text-[13px]"}>@devsnips/react v2.4.0</p>
            <p className={ROW_META}>{published ? "Publishing to the registry…" : "Draft release · 14 commits since v2.3.1"}</p>
          </div>
          <Dialog>
            <DialogTrigger>Publish release</DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Publish v2.4.0</DialogTitle>
                <DialogDescription>This publishes the current draft to the package registry and creates the v2.4.0 tag.</DialogDescription>
              </DialogHeader>
              <div className="space-y-2 px-5 py-4 text-sm leading-5">
                <div className="flex items-center justify-between gap-4 border-b border-[var(--ds-color-border-subtle)] pb-2">
                  <span className="text-[var(--ds-color-muted-foreground)]">Target registry</span>
                  <span className="font-mono text-[13px] text-[var(--ds-color-foreground)]">npmjs.com</span>
                </div>
                <div className="flex items-center justify-between gap-4 border-b border-[var(--ds-color-border-subtle)] pb-2">
                  <span className="text-[var(--ds-color-muted-foreground)]">Commits</span>
                  <span className="font-mono text-[13px] text-[var(--ds-color-foreground)]">14 since v2.3.1</span>
                </div>
                <div className="flex items-center justify-between gap-4">
                  <span className="text-[var(--ds-color-muted-foreground)]">Checks</span>
                  <span className="inline-flex items-center gap-1.5 text-[13px] text-[var(--ds-color-success)]"><Icon name="check" className="size-3.5" aria-hidden="true" />All 42 passing</span>
                </div>
              </div>
              <DialogFooter className="sm:items-center sm:justify-between">
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                  <a
                    href="#release-checklist"
                    className="rounded-[var(--ds-radius-xs)] text-sm font-medium text-[var(--ds-color-link)] underline-offset-2 hover:text-[var(--ds-color-link-hover)] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]"
                  >
                    View release checklist
                  </a>
                  <span className="inline-flex items-center gap-1.5 text-xs text-[var(--ds-color-muted-foreground)]"><Icon name="clock" className="size-3.5" aria-hidden="true" />Draft saved 2 min ago</span>
                </div>
                <div className="flex gap-2">
                  <DialogClose>Cancel</DialogClose>
                  <DialogClose variant="primary" onClick={() => setPublished(true)}>Publish release</DialogClose>
                </div>
              </DialogFooter>
              <DialogClose variant="ghost" aria-label="Close dialog"><Icon name="x" className="size-4" /></DialogClose>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <p className={NOTE}>The checklist link is a real anchor — Tab reaches it before the footer actions, and Enter navigates.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Publish release — split footer with link + metadata</p>
        <PublishRelease />
      </div>
    </div>
  );
}''',
)

# 9. dialog-non-modal
register(
    "dialog-non-modal",
    title="Non-Modal Dialog",
    subcategory="Behavior",
    description="`modal={false}`: a floating keyboard-shortcuts reference panel — no overlay, no scroll lock, no focus trap; the page behind stays interactive and the panel closes on Escape, outside pointer down, or its close actions.",
    tags=TAGS_BASE + ["non-modal", "floating", "panel"],
    features=FEAT_BASE + ["modal={false}", "no overlay or scroll lock", "page stays interactive"],
    accessibility=A11Y_BASE + ["no aria-modal in non-modal mode", "Tab leaves the panel naturally"],
    interactive=True,
    related=["dialog", "dialog-scrollable", "dialog-controlled", "dialog-with-custom-footer"],
    usage='''import Dialog, {
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
</Dialog>''',
    props_doc=props_table(),
    composition_note="Non-modal is a prop, not a different component: the same primitives with `modal={false}` on the root. The panel keeps the shared dialog geometry but renders without the overlay and without `aria-modal`.",
    logic_doc="""`modal={false}` switches three behaviors off: no overlay is rendered (the page stays clickable), body scroll is not locked, and Tab is not trapped — focus can leave the panel and reach the page behind it. `aria-modal` is omitted, since assistive technology must not be told the background is inert when it is not.

Closing still works from every direction: Escape (the panel registers on the same top-most stack), a pointer down outside the panel, the trigger toggle, and `DialogClose`. Focus is still moved into the panel on open and restored to the trigger on close.

Use non-modal for reference material the user consults while working elsewhere on the page — shortcuts, inspectors, help panels. Use the default modal dialog whenever the surrounding page must wait for a decision.""",
    keyboard_doc="""| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the panel, focus the first focusable element inside |
| `Tab` / `Shift+Tab` | Move naturally — no trap; the page behind stays reachable |
| `Escape` | Close the panel and restore focus to the trigger |

The trigger and close actions are native `<button>` elements, so Enter/Space activation follows normal browser behavior.""",
    behavior_doc="""- **Trigger (idle / open)** — per the shared control system; `aria-expanded` reflects the panel.
- **Panel** — same surface/border/elevation geometry as the modal dialog, centered; no overlay behind it, so the page remains visible and interactive.
- **Page** — never scroll-locked; clicking outside the panel dismisses it.""",
    a11y_doc="Without `aria-modal`, screen-reader users can still reach the page behind the panel — matching the actual, non-blocking behavior. Because there is no focus trap, keyboard users can Tab out of the panel at any time.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo page is intentionally tall: while the non-modal panel is open the page keeps scrolling, and clicking the background dismisses the panel.",
    tsx_header='''/**
 * DevSnips React Dialog — Non-Modal.
 *
 * The shared dialog core with `modal={false}`: a floating panel without an
 * overlay, scroll lock, or focus trap. The page behind stays interactive;
 * the panel closes on Escape, an outside pointer down, the trigger toggle,
 * or DialogClose — and focus still restores to the trigger.
 */''',
    showcase=DEMO_HELPERS + '''
const SHORTCUTS = [
  ["⌘ K", "Open command palette"],
  ["⌘ ⇧ P", "Open the actions menu"],
  ["G then D", "Go to dashboard"],
  ["G then S", "Go to settings"],
  ["⌘ /", "Toggle the sidebar"],
  ["?", "Open this shortcuts panel"],
];

const KBD = "rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-1.5 py-0.5 font-mono text-[11px] leading-4 text-[var(--ds-color-foreground)]";

function ShortcutsPanel() {
  const [count, setCount] = React.useState(0);
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>Editor canvas</p>
            <p className={ROW_META}>The page stays interactive while the panel floats above it</p>
          </div>
          <div className="flex items-center gap-2">
            <button type="button" className={BTN_OUTLINE} onClick={() => setCount((c) => c + 1)}>
              Background action{count > 0 ? " ×" + count : ""}
            </button>
            <Dialog modal={false}>
              <DialogTrigger>Keyboard shortcuts</DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Keyboard shortcuts</DialogTitle>
                </DialogHeader>
                <div className="px-5 py-4">
                  <table className="w-full border-collapse text-sm leading-5">
                    <tbody>
                      {SHORTCUTS.map((row) => (
                        <tr key={row[1]} className="border-b border-[var(--ds-color-border-subtle)] last:border-0">
                          <td className="py-2 pr-4"><kbd className={KBD}>{row[0]}</kbd></td>
                          <td className="py-2 text-[var(--ds-color-muted-foreground)]">{row[1]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <DialogFooter>
                  <DialogClose>Close</DialogClose>
                </DialogFooter>
                <DialogClose variant="ghost" aria-label="Close dialog"><Icon name="x" className="size-4" /></DialogClose>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </div>
      <p className={NOTE}>With the panel open: the background button still works (clicking outside dismisses the panel), the page still scrolls, and Tab is not trapped.</p>
      <div className="space-y-2" aria-hidden="true">
        {Array.from({ length: 12 }).map((_, i) => (
          <div key={i} className="rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-subtle)] bg-[var(--ds-color-surface-subtle)] px-4 py-3 text-xs text-[var(--ds-color-muted-foreground)]">
            Canvas row {i + 1} — scrolls normally while the non-modal panel is open.
          </div>
        ))}
      </div>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Keyboard shortcuts — modal=false floating panel</p>
        <ShortcutsPanel />
      </div>
    </div>
  );
}''',
)
