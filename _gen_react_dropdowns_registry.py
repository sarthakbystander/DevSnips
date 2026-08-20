"""Registry for the DevSnips React Dropdowns generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs.
The generator (``_gen_react_dropdowns.py``) reads each component's
``code.tsx`` from disk and combines it with the spec here to write
``code.jsx``, ``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented demo content only (projects, documents, releases,
repositories, workspace settings, editor commands). No lorem ipsum, no
marketing buzzwords.
"""
from _gen_react_dropdowns import (
    register,
    LOGIC_BASE,
    KEYBOARD_BASE,
    STATES_BASE,
    RESPONSIVE_BASE,
)

TAGS_BASE = ["dropdown", "menu", "actions", "react", "tailwind", "accessible", "keyboard", "responsive", "interactive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "role=menu semantics", "keyboard navigation", "focus management", "outside-pointer close", "viewport-aware placement"]
A11Y_BASE = ['aria-haspopup="menu" trigger', 'role="menu" panel', 'role="menuitem" items', "aria-expanded state", "focus restoration on close", "native disabled items", "focus-visible ring"]

# Shared props tables. The seven core primitives carry the same API family-wide.
MENU_PROPS = r"""### `<DropdownMenu>`

| Name | Type | Default | Description |
|---|---|---|---|
| `open` | `boolean` | — | Open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial open state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the menu requests to open or close. |
| `placement` | `"bottom-start" \| "bottom-end" \| "top-start" \| "top-end"` | `"bottom-start"` | Preferred placement; flips to stay in the viewport. |
| `className` | `string` | — | Extra classes on the relative wrapper. |
| `children` | `ReactNode` | — | `DropdownMenuTrigger` + `DropdownMenuContent`. |"""

TRIGGER_PROPS = r"""### `<DropdownMenuTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Visible trigger label (a chevron is rendered after it). |

A real `<button type="button">` with `aria-haspopup="menu"` + `aria-expanded`; every native button attribute (`disabled`, `aria-label`, …) is forwarded."""

CONTENT_PROPS = r"""### `<DropdownMenuContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="menu"` panel. |
| `children` | `ReactNode` | — | Items, labels, groups, and separators. |

Rendered only while open. Labelled by the trigger via `aria-labelledby`; pass `aria-label` to override."""

ITEM_PROPS = r"""### `<DropdownMenuItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered aria-hidden). |
| `shortcut` | `string` | — | Informational shortcut at the trailing edge (aria-hidden; exposed via `aria-keyshortcuts`). |
| `destructive` | `boolean` | `false` | Destructive styling via the semantic destructive token. |
| `disabled` | `boolean` | `false` | Native disabled: skipped by arrow keys, out of the tab order, not activatable. |
| `closeOnSelect` | `boolean` | `true` | Whether activating the item closes the menu. |
| `onSelect` | `(event) => void` | — | Called on activation before the menu closes; `event.preventDefault()` keeps the menu open. |
| `children` | `ReactNode` | — | Visible item label. |"""

LABEL_PROPS = r"""### `<DropdownMenuLabel>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the label. |
| `children` | `ReactNode` | — | Section heading text. |

Non-interactive. Give it an `id` and point the group's `aria-labelledby` at it when labelling a `DropdownMenuGroup`."""

GROUP_PROPS = r"""### `<DropdownMenuGroup>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the group. |
| `children` | `ReactNode` | — | Grouped items. |

Renders `role="group"`; forward `aria-labelledby` to associate it with its `DropdownMenuLabel`."""

SEPARATOR_PROPS = r"""### `<DropdownMenuSeparator>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the separator. |

A `role="separator"` horizontal rule. Not focusable, not announced as an item."""

CHECKBOX_ITEM_PROPS = r"""### `<DropdownMenuCheckboxItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `checked` | `boolean` | — | Checked state (controlled). |
| `defaultChecked` | `boolean` | `false` | Initial checked state (uncontrolled). |
| `onCheckedChange` | `(checked: boolean) => void` | — | Called with the next checked state on activation. |
| `closeOnSelect` | `boolean` | `false` | Whether activating the item closes the menu. |
| `onSelect` | `(event) => void` | — | Called on activation after the state toggles. |
| `shortcut` | `string` | — | Informational shortcut at the trailing edge. |
| `disabled` | `boolean` | `false` | Native disabled: skipped by keys, not activatable. |
| `children` | `ReactNode` | — | Visible item label. |

Renders `role="menuitemcheckbox"` with `aria-checked`; the check indicator is aria-hidden decoration."""

RADIO_GROUP_PROPS = r"""### `<DropdownMenuRadioGroup>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` | — | Selected value (controlled). |
| `defaultValue` | `string` | `""` | Initial selected value (uncontrolled). |
| `onValueChange` | `(value: string) => void` | — | Called with the newly selected value. |
| `children` | `ReactNode` | — | `DropdownMenuRadioItem` options. |

Renders `role="group"`; exactly one item in the group is checked at a time."""

RADIO_ITEM_PROPS = r"""### `<DropdownMenuRadioItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` (required) | — | The value this option represents. |
| `closeOnSelect` | `boolean` | `false` | Whether activating the item closes the menu. |
| `onSelect` | `(event) => void` | — | Called on activation after the group value updates. |
| `disabled` | `boolean` | `false` | Native disabled: skipped by keys, not activatable. |
| `children` | `ReactNode` | — | Visible option label. |

Renders `role="menuitemradio"` with `aria-checked`; the dot indicator is aria-hidden decoration."""

SUB_PROPS = r"""### `<DropdownMenuSub>`

| Name | Type | Default | Description |
|---|---|---|---|
| `children` | `ReactNode` | — | `DropdownMenuSubTrigger` + `DropdownMenuSubContent`. |

Owns the nested level's open state and registers with the parent menu level so sibling pointer interaction closes it."""

SUB_TRIGGER_PROPS = r"""### `<DropdownMenuSubTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered aria-hidden). |
| `className` | `string` | — | Extra classes on the item. |
| `children` | `ReactNode` | — | Visible item label (a chevron-right is rendered after it). |

A `role="menuitem"` button with `aria-haspopup="menu"` + `aria-expanded`; ArrowRight / Enter / Space open the submenu, hovering opens it without moving focus."""

SUB_CONTENT_PROPS = r"""### `<DropdownMenuSubContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="menu"` panel. |
| `children` | `ReactNode` | — | Submenu items. |

Opens to the right of its trigger and flips left when the right side would leave the viewport. ArrowLeft / Escape close only this level."""


def props_table(*extra):
    parts = [MENU_PROPS, TRIGGER_PROPS, CONTENT_PROPS, ITEM_PROPS, LABEL_PROPS, GROUP_PROPS, SEPARATOR_PROPS]
    parts.extend(extra)
    return "\n\n".join(parts)


# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = """const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const CARD = "rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4";
const ROW = "flex items-center justify-between gap-4";
const ROW_NAME = "m-0 text-sm font-medium text-[var(--ds-color-foreground)]";
const ROW_META = "m-0 text-xs text-[var(--ds-color-muted-foreground)]";
"""

# 1. dropdown-menu (reference)
register(
    "dropdown-menu",
    title="Dropdown Menu",
    subcategory="Core",
    description="The canonical action menu: a real menu-button trigger, a role=menu panel of menuitem actions, roving keyboard focus, separators, disabled items, and viewport-aware placement.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["dropdown-menu-with-icons", "dropdown-menu-with-sections", "dropdown-menu-destructive", "dropdown-menu-submenu"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "./dropdown-menu";

<DropdownMenu>
  <DropdownMenuTrigger>Actions</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem onSelect={() => renameProject()}>Rename project</DropdownMenuItem>
    <DropdownMenuItem onSelect={() => duplicateProject()}>Duplicate project</DropdownMenuItem>
    <DropdownMenuItem disabled>Transfer ownership</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem onSelect={() => archiveProject()}>Archive project</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>

// Uncontrolled (default) or controlled:
const [open, setOpen] = useState(false);
<DropdownMenu open={open} onOpenChange={setOpen}>…</DropdownMenu>

// Placement (flips to stay in the viewport):
<DropdownMenu placement="bottom-end">…</DropdownMenu>''',
    props_doc=props_table(),
    composition_note="This is the reference composition — every other variant in the family uses the same primitives and extends the same class constants, states, and accessibility model.",
    logic_doc=LOGIC_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Only one menu is open at a time per root; mounting a second `<DropdownMenu>` on the same page is safe because each root scopes its own trigger, panel, and listeners.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Reference implementation for the Dropdowns family. It establishes the shared menu geometry (radius-md panel, 13px items, 36px trigger), the surface/border/shadow model, the focus-ring treatment, the open/close + focus-restore behavior, and the viewport flip logic that every other variant extends.",
    showcase=DEMO_HELPERS + '''
function ProjectActions() {
  const [lastAction, setLastAction] = React.useState("None yet");
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>Design system migration</p>
            <p className={ROW_META}>Project · Updated 2 days ago</p>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger>Actions</DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onSelect={() => setLastAction("Rename project")}>Rename project</DropdownMenuItem>
              <DropdownMenuItem onSelect={() => setLastAction("Duplicate project")}>Duplicate project</DropdownMenuItem>
              <DropdownMenuItem disabled>Transfer ownership</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onSelect={() => setLastAction("Archive project")}>Archive project</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      <p className={NOTE}>Last action: {lastAction}. Try opening with the mouse, ArrowDown, and closing with Escape or by clicking outside.</p>
    </div>
  );
}
function ControlledMenu() {
  const [open, setOpen] = React.useState(false);
  return (
    <div className="flex flex-wrap items-center gap-3">
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger>Release actions</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Publish release</DropdownMenuItem>
          <DropdownMenuItem>Edit release notes</DropdownMenuItem>
          <DropdownMenuItem>Roll back release</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Menu is {open ? "open" : "closed"} — the parent owns the state.</p>
    </div>
  );
}
function PlacementDemo() {
  return (
    <div className="flex flex-wrap items-start justify-between gap-3">
      <DropdownMenu placement="top-start">
        <DropdownMenuTrigger>Top start</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Draft release</DropdownMenuItem>
          <DropdownMenuItem>Schedule release</DropdownMenuItem>
          <DropdownMenuItem>Copy changelog</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <DropdownMenu placement="bottom-end">
        <DropdownMenuTrigger>Bottom end</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>View deployment</DropdownMenuItem>
          <DropdownMenuItem>Redeploy</DropdownMenuItem>
          <DropdownMenuItem>Inspect build log</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Project actions — uncontrolled</p>
        <ProjectActions />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Controlled open state</p>
        <ControlledMenu />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Placement variants</p>
        <PlacementDemo />
      </div>
    </div>
  );
}''',
)

# 2. dropdown-menu-with-icons
register(
    "dropdown-menu-with-icons",
    title="Dropdown Menu with Icons",
    subcategory="Content",
    description="Menu items with meaningful leading icons in a consistent 16px aria-hidden slot — the text label still carries the accessible name, so meaning never depends on the icon alone.",
    tags=TAGS_BASE + ["icons", "icon"],
    features=FEAT_BASE + ["leading icon slot", "currentColor icons"],
    accessibility=A11Y_BASE + ["aria-hidden icons", "text label carries the name"],
    interactive=True,
    related=["dropdown-menu", "dropdown-menu-with-shortcuts", "dropdown-menu-destructive", "dropdown-menu-with-sections"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "./dropdown-menu-with-icons";
import { PencilIcon, CopyIcon, ArchiveIcon } from "./icons";

<DropdownMenu>
  <DropdownMenuTrigger>Document</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem icon={<PencilIcon />}>Rename document</DropdownMenuItem>
    <DropdownMenuItem icon={<CopyIcon />}>Make a copy</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem icon={<ArchiveIcon />}>Archive document</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>''',
    props_doc=props_table(),
    composition_note="Icons are the `icon` prop on `<DropdownMenuItem>` — a `ReactNode` rendered in a fixed 16px, aria-hidden, `currentColor` slot ahead of the label. Regular items tint the icon `--ds-color-muted-foreground`; destructive items inherit the destructive text color.",
    logic_doc=LOGIC_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Icons are decorative by construction: they render inside an `aria-hidden` span and the visible text remains the accessible name. Never ship an icon-only menu item — if an item's meaning is not obvious from words, improve the words.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The icon slot is a fixed 16px (`[&_svg]:size-4`) with `shrink-0`, so labels stay aligned down the column even when some items have no icon. Pass any SVG that sizes itself to `currentColor`; no icon library is required.",
    showcase=DEMO_HELPERS + '''
function DocumentActions() {
  const [lastAction, setLastAction] = React.useState("None yet");
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="flex min-w-0 items-center gap-3">
            <span className="inline-flex size-8 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] text-[var(--ds-color-muted-foreground)] [&_svg]:size-4"><Icon name="file" /></span>
            <div className="min-w-0">
              <p className={ROW_NAME}>Q3 roadmap.docx</p>
              <p className={ROW_META}>Document · 84 KB</p>
            </div>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger>Document</DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem icon={<Icon name="external" />} onSelect={() => setLastAction("Open in new tab")}>Open in new tab</DropdownMenuItem>
              <DropdownMenuItem icon={<Icon name="edit" />} onSelect={() => setLastAction("Rename document")}>Rename document</DropdownMenuItem>
              <DropdownMenuItem icon={<Icon name="duplicate" />} onSelect={() => setLastAction("Make a copy")}>Make a copy</DropdownMenuItem>
              <DropdownMenuItem icon={<Icon name="folder" />} onSelect={() => setLastAction("Move to folder")}>Move to folder</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem icon={<Icon name="archive" />} onSelect={() => setLastAction("Archive document")}>Archive document</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      <p className={NOTE}>Last action: {lastAction}</p>
    </div>
  );
}
function AccountMenu() {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <DropdownMenu>
        <DropdownMenuTrigger>mina@devsnips.io</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem icon={<Icon name="user" />}>Profile</DropdownMenuItem>
          <DropdownMenuItem icon={<Icon name="settings" />}>Settings</DropdownMenuItem>
          <DropdownMenuItem icon={<Icon name="bell" />}>Notifications</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem icon={<Icon name="logout" />}>Sign out</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Icons are muted decoration; the words carry the meaning.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Document actions</p>
        <DocumentActions />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Account menu</p>
        <AccountMenu />
      </div>
    </div>
  );
}''',
)

# 3. dropdown-menu-with-sections
register(
    "dropdown-menu-with-sections",
    title="Dropdown Menu with Sections",
    subcategory="Content",
    description="Related actions grouped under readable section labels with role=group semantics and hairline separators — an account/workspace switcher pattern, not a card stack.",
    tags=TAGS_BASE + ["sections", "grouped", "labels"],
    features=FEAT_BASE + ["section labels", "role=group", "separators"],
    accessibility=A11Y_BASE + ["role=group with aria-labelledby", "non-interactive labels"],
    interactive=True,
    related=["dropdown-menu", "dropdown-menu-with-icons", "dropdown-menu-submenu"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuGroup,
  DropdownMenuSeparator,
} from "./dropdown-menu-with-sections";

<DropdownMenu>
  <DropdownMenuTrigger>mina@devsnips.io</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel id="account-label">Account</DropdownMenuLabel>
    <DropdownMenuGroup aria-labelledby="account-label">
      <DropdownMenuItem>Profile</DropdownMenuItem>
      <DropdownMenuItem>Settings</DropdownMenuItem>
    </DropdownMenuGroup>
    <DropdownMenuSeparator />
    <DropdownMenuLabel id="workspace-label">Workspace</DropdownMenuLabel>
    <DropdownMenuGroup aria-labelledby="workspace-label">
      <DropdownMenuItem>Projects</DropdownMenuItem>
      <DropdownMenuItem>Members</DropdownMenuItem>
      <DropdownMenuItem disabled>Billing (owner only)</DropdownMenuItem>
    </DropdownMenuGroup>
  </DropdownMenuContent>
</DropdownMenu>''',
    props_doc=props_table(),
    composition_note="Sections are composition, not new primitives: `<DropdownMenuLabel>` renders the heading (uppercase, tracked, smaller — distinguishable without color) and `<DropdownMenuGroup>` wraps the items in `role=\"group\"`. Wire them together with an `id` on the label and `aria-labelledby` on the group, and separate sections with `<DropdownMenuSeparator>`.",
    logic_doc=LOGIC_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE + """
- **Label** — non-interactive heading row; skipped by pointer and keyboard.
- **Separator** — hairline `--ds-color-border` rule with vertical breathing room; not an item.""",
    a11y_doc="Groups announce their label through the `aria-labelledby` association, so screen-reader users hear the section context when moving between groups. Labels and separators are skipped by arrow-key navigation automatically because only menu items are focus stops.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Keep sections short (2–5 items) and few (2–3 per menu). If a menu grows past three labelled sections, the information architecture wants a settings page, not a bigger menu.",
    showcase=DEMO_HELPERS + '''
function WorkspaceMenu() {
  const [lastAction, setLastAction] = React.useState("None yet");
  return (
    <div className="space-y-3">
      <DropdownMenu>
        <DropdownMenuTrigger>mina@devsnips.io</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel id="account-label">Account</DropdownMenuLabel>
          <DropdownMenuGroup aria-labelledby="account-label">
            <DropdownMenuItem onSelect={() => setLastAction("Profile")}>Profile</DropdownMenuItem>
            <DropdownMenuItem onSelect={() => setLastAction("Settings")}>Settings</DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuLabel id="workspace-label">Workspace</DropdownMenuLabel>
          <DropdownMenuGroup aria-labelledby="workspace-label">
            <DropdownMenuItem onSelect={() => setLastAction("Projects")}>Projects</DropdownMenuItem>
            <DropdownMenuItem onSelect={() => setLastAction("Members")}>Members</DropdownMenuItem>
            <DropdownMenuItem disabled>Billing (owner only)</DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem onSelect={() => setLastAction("Sign out")}>Sign out</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Last action: {lastAction}</p>
    </div>
  );
}
function BoardMenu() {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <DropdownMenu>
        <DropdownMenuTrigger>Board</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel id="arrange-label">Arrange</DropdownMenuLabel>
          <DropdownMenuGroup aria-labelledby="arrange-label">
            <DropdownMenuItem>Group by status</DropdownMenuItem>
            <DropdownMenuItem>Group by assignee</DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuLabel id="board-actions-label">Board</DropdownMenuLabel>
          <DropdownMenuGroup aria-labelledby="board-actions-label">
            <DropdownMenuItem>Rename board</DropdownMenuItem>
            <DropdownMenuItem>Duplicate board</DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Labels are headings — uppercase, tracked, smaller — never item-styled.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Account / workspace sections</p>
        <WorkspaceMenu />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Board arrangement</p>
        <BoardMenu />
      </div>
    </div>
  );
}''',
)

# 4. dropdown-menu-with-shortcuts
register(
    "dropdown-menu-with-shortcuts",
    title="Dropdown Menu with Shortcuts",
    subcategory="Content",
    description="Informational keyboard shortcuts aligned to the trailing edge of menu items — exposed via aria-keyshortcuts, never part of the accessible name, with stable right alignment.",
    tags=TAGS_BASE + ["shortcuts", "hotkeys", "keyboard"],
    features=FEAT_BASE + ["aria-keyshortcuts", "trailing shortcut column", "truncation-safe"],
    accessibility=A11Y_BASE + ["aria-keyshortcuts", "aria-hidden shortcut glyphs"],
    interactive=True,
    related=["dropdown-menu", "dropdown-menu-with-icons", "dropdown-menu-checkboxes"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "./dropdown-menu-with-shortcuts";

<DropdownMenu>
  <DropdownMenuTrigger>File</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem shortcut="Ctrl+S">Save</DropdownMenuItem>
    <DropdownMenuItem shortcut="Ctrl+Shift+S">Save a copy</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem shortcut="Ctrl+E">Export</DropdownMenuItem>
    <DropdownMenuItem shortcut="Ctrl+P" disabled>Print</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>''',
    props_doc=props_table(),
    composition_note="Shortcuts are the `shortcut` prop on `<DropdownMenuItem>` — a string rendered in a trailing, `ml-auto`, `pl-6` column. The label keeps `min-w-0 flex-1 truncate`, so a long label truncates before it can push the shortcut column out of alignment.",
    logic_doc=LOGIC_BASE + """

The `shortcut` prop is informational only — it documents the accelerator; it does not register a global key handler. Wire real global shortcuts separately (the Buttons family's command-button shows the pattern).""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE + """
- **Shortcut text** — `text-xs` muted, right-aligned in a stable column; hidden on items without a shortcut so the column never shifts.""",
    a11y_doc="The shortcut glyph is `aria-hidden` and mirrored on the item as `aria-keyshortcuts`, so assistive technology can announce the accelerator without it becoming part of the accessible name (activating the item still announces just the label).",
    responsive_doc=RESPONSIVE_BASE + """ On narrow screens the label truncates first (`min-w-0 flex-1 truncate`); the shortcut column keeps `shrink-0` so it never wraps or overflows the panel.""",
    notes_doc="Shortcuts use the platform's modifier notation in the demo (Ctrl+…); a real app would swap ⌘/Ctrl by platform. The same string is passed to `aria-keyshortcuts`.",
    showcase=DEMO_HELPERS + '''
function FileMenu() {
  const [lastAction, setLastAction] = React.useState("None yet");
  return (
    <div className="space-y-3">
      <DropdownMenu>
        <DropdownMenuTrigger>File</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem shortcut="Ctrl+S" onSelect={() => setLastAction("Save")}>Save</DropdownMenuItem>
          <DropdownMenuItem shortcut="Ctrl+Shift+S" onSelect={() => setLastAction("Save a copy")}>Save a copy</DropdownMenuItem>
          <DropdownMenuItem shortcut="F2" onSelect={() => setLastAction("Rename")}>Rename</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem shortcut="Ctrl+E" onSelect={() => setLastAction("Export")}>Export</DropdownMenuItem>
          <DropdownMenuItem shortcut="Ctrl+P" disabled>Print</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem shortcut="Ctrl+Shift+Alt+P" onSelect={() => setLastAction("Publish to staging")}>Publish to the staging environment</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Last action: {lastAction}. Shortcuts are informational — activating the item works with or without them.</p>
    </div>
  );
}
function EditMenu() {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <DropdownMenu placement="bottom-end">
        <DropdownMenuTrigger>Edit</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem shortcut="Ctrl+Z">Undo</DropdownMenuItem>
          <DropdownMenuItem shortcut="Ctrl+Shift+Z">Redo</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem shortcut="Ctrl+X">Cut</DropdownMenuItem>
          <DropdownMenuItem shortcut="Ctrl+C">Copy</DropdownMenuItem>
          <DropdownMenuItem shortcut="Ctrl+V">Paste</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>The shortcut column stays put even when labels are long.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Editor file menu</p>
        <FileMenu />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Edit menu — bottom-end placement</p>
        <EditMenu />
      </div>
    </div>
  );
}''',
)

# 5. dropdown-menu-destructive
register(
    "dropdown-menu-destructive",
    title="Dropdown Menu Destructive",
    subcategory="States",
    description="A menu containing destructive actions, styled with the restrained semantic destructive token and quarantined below a separator — clearly dangerous, never neon.",
    tags=TAGS_BASE + ["destructive", "danger", "delete"],
    features=FEAT_BASE + ["destructive token styling", "separator quarantine", "confirmable via onSelect"],
    accessibility=A11Y_BASE + ["destructive distinguished by token + wording"],
    interactive=True,
    related=["dropdown-menu", "dropdown-menu-with-icons", "dropdown-menu-with-sections"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "./dropdown-menu-destructive";

<DropdownMenu>
  <DropdownMenuTrigger>Repository</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Edit repository</DropdownMenuItem>
    <DropdownMenuItem>Archive repository</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem destructive onSelect={(e) => confirmDelete(e)}>
      Delete repository
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>''',
    props_doc=props_table(),
    composition_note="Destructive is the `destructive` prop on `<DropdownMenuItem>` — it swaps the item to `--ds-color-destructive` text on a `--ds-color-destructive-soft` hover/focus surface. Quarantine destructive actions below a `<DropdownMenuSeparator>` so they are visually and spatially separated from ordinary actions.",
    logic_doc=LOGIC_BASE + """

For irreversible actions, keep the menu open and confirm first: call `event.preventDefault()` in `onSelect` (or set `closeOnSelect={false}`) and open a confirmation dialog instead of acting immediately.""",
    keyboard_doc=None,
    behavior_doc=STATES_BASE + """
- **Destructive item** — `--ds-color-destructive` text (a softened red that meets contrast in both themes, not neon), `--ds-color-destructive-soft` hover/focus surface; the wording ("Delete…", "Remove…") carries the meaning, color supports it.""",
    a11y_doc="Destructive state is communicated by the action's wording and position (below a separator, last in the menu) in addition to color — never by color alone. A disabled destructive item (`disabled` + `destructive`) keeps both cues: muted opacity and the destructive tint.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Use at most one destructive cluster per menu, always at the bottom. If everything in the menu is destructive, the destructive styling loses its signal — prefer a dedicated confirmation flow.",
    showcase=DEMO_HELPERS + '''
function RepositoryMenu() {
  const [status, setStatus] = React.useState("No destructive action taken.");
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="min-w-0">
            <p className={ROW_NAME}>api-gateway</p>
            <p className={ROW_META}>Repository · 214 commits · 3 collaborators</p>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger>Repository</DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onSelect={() => setStatus("Editing repository settings.")}>Edit repository</DropdownMenuItem>
              <DropdownMenuItem onSelect={() => setStatus("Repository archived.")}>Archive repository</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem destructive onSelect={() => setStatus("Repository scheduled for deletion.")}>Delete repository</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      <p className={NOTE}>{status}</p>
    </div>
  );
}
function MemberMenu() {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <DropdownMenu>
        <DropdownMenuTrigger>Member</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Change role</DropdownMenuItem>
          <DropdownMenuItem>View activity</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem destructive>Remove from workspace</DropdownMenuItem>
          <DropdownMenuItem destructive disabled>Delete workspace (owner only)</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Destructive actions sit below the separator; a disabled destructive action keeps both cues.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Repository danger zone</p>
        <RepositoryMenu />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Member management</p>
        <MemberMenu />
      </div>
    </div>
  );
}''',
)

# 6. dropdown-menu-checkboxes
CHECKBOX_LOGIC = LOGIC_BASE + """

`<DropdownMenuCheckboxItem>` is the exception to close-on-select: toggling an option keeps the menu open by default (`closeOnSelect` defaults to `false`), so several view options can be flipped in one visit. Both state modes are supported — controlled (`checked` + `onCheckedChange`) and uncontrolled (`defaultChecked`)."""

register(
    "dropdown-menu-checkboxes",
    title="Dropdown Menu Checkboxes",
    subcategory="Selection",
    description="Checkable menu items (role=menuitemcheckbox + aria-checked) for toggling view options — controlled and uncontrolled, with the menu staying open while options are flipped.",
    tags=TAGS_BASE + ["checkbox", "selection", "toggle", "view-options"],
    features=FEAT_BASE + ["role=menuitemcheckbox", "aria-checked state", "stays open on toggle", "controlled + uncontrolled"],
    accessibility=A11Y_BASE + ["role=menuitemcheckbox", "aria-checked announced", "aria-hidden check indicator"],
    interactive=True,
    related=["dropdown-menu", "dropdown-menu-radio", "dropdown-menu-with-shortcuts"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuSeparator,
} from "./dropdown-menu-checkboxes";

// Uncontrolled:
<DropdownMenu>
  <DropdownMenuTrigger>View options</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuCheckboxItem defaultChecked>Show sidebar</DropdownMenuCheckboxItem>
    <DropdownMenuCheckboxItem>Show toolbar</DropdownMenuCheckboxItem>
    <DropdownMenuCheckboxItem defaultChecked>Show status bar</DropdownMenuCheckboxItem>
  </DropdownMenuContent>
</DropdownMenu>

// Controlled:
const [rulers, setRulers] = useState(false);
<DropdownMenuCheckboxItem checked={rulers} onCheckedChange={setRulers}>
  Show rulers
</DropdownMenuCheckboxItem>''',
    props_doc=props_table(CHECKBOX_ITEM_PROPS),
    composition_note="`<DropdownMenuCheckboxItem>` joins the core primitives: a real button with `role=\"menuitemcheckbox\"` and `aria-checked`, a fixed 16px indicator slot whose check glyph tracks the checked state, and the same keyboard/pointer behavior as a plain item. Mix checkbox items with plain items, labels, and separators freely.",
    logic_doc=CHECKBOX_LOGIC,
    keyboard_doc=KEYBOARD_BASE.replace(
        "| `Enter` / `Space` (menu) | Activate the focused item (native button behavior) |",
        "| `Enter` / `Space` (menu) | Activate the focused item; on a checkbox item, toggles its checked state |"),
    behavior_doc=STATES_BASE + """
- **Checkbox item (checked)** — the leading check glyph fades in (`--ds-color-primary`), `aria-checked="true"` carries the state to assistive technology.
- **Checkbox item (unchecked)** — the indicator slot stays empty, reserving alignment.
- **Checkbox item (disabled)** — native `disabled` with the current state frozen and visible.""",
    a11y_doc="State is communicated by `aria-checked` on the item itself, not by the glyph — the check mark is `aria-hidden` decoration. Because the items are real buttons, Space/Enter toggle them natively.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The check column is reserved on every checkbox item so checked and unchecked rows keep identical label alignment. Use checkboxes for independent options; for mutually exclusive options use dropdown-menu-radio.",
    showcase=DEMO_HELPERS + '''
const PANELS = [
  ["sidebar", "Show sidebar", true],
  ["toolbar", "Show toolbar", false],
  ["statusbar", "Show status bar", true],
  ["wrap", "Word wrap", false],
];
function ViewOptions() {
  const [visible, setVisible] = React.useState(() => Object.fromEntries(PANELS.map(([k, , on]) => [k, on])));
  const names = PANELS.filter(([k]) => visible[k]).map(([, label]) => label.replace("Show ", ""));
  return (
    <div className="space-y-3">
      <DropdownMenu>
        <DropdownMenuTrigger>View options</DropdownMenuTrigger>
        <DropdownMenuContent>
          {PANELS.map(([key, label, on]) => (
            <DropdownMenuCheckboxItem key={key} defaultChecked={on} onCheckedChange={(next) => setVisible((v) => ({ ...v, [key]: next }))}>{label}</DropdownMenuCheckboxItem>
          ))}
          <DropdownMenuSeparator />
          <DropdownMenuCheckboxItem disabled>Minimap (Pro plan)</DropdownMenuCheckboxItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Visible: {names.length ? names.join(", ") : "nothing"} — the menu stays open while you toggle.</p>
    </div>
  );
}
function ControlledRulers() {
  const [rulers, setRulers] = React.useState(true);
  const [grid, setGrid] = React.useState(false);
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-3">
        <DropdownMenu>
          <DropdownMenuTrigger>Canvas</DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuCheckboxItem checked={rulers} onCheckedChange={setRulers}>Show rulers</DropdownMenuCheckboxItem>
            <DropdownMenuCheckboxItem checked={grid} onCheckedChange={setGrid}>Show grid</DropdownMenuCheckboxItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <label className="flex items-center gap-2 text-sm text-[var(--ds-color-foreground)]">
          <input type="checkbox" checked={grid} onChange={(e) => setGrid(e.target.checked)} className="size-4 accent-[var(--ds-color-accent)]" />
          Grid (external control)
        </label>
      </div>
      <p className={NOTE}>Controlled items mirror external state both ways: rulers {rulers ? "on" : "off"}, grid {grid ? "on" : "off"}.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>View options — uncontrolled</p>
        <ViewOptions />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Canvas options — controlled</p>
        <ControlledRulers />
      </div>
    </div>
  );
}''',
)

# 7. dropdown-menu-radio
RADIO_LOGIC = LOGIC_BASE + """

`<DropdownMenuRadioGroup>` owns the selected value. Both modes are supported — controlled (`value` + `onValueChange`) and uncontrolled (`defaultValue`). Selecting an option keeps the menu open by default (`closeOnSelect` defaults to `false`) so the selection can be reviewed in place."""

register(
    "dropdown-menu-radio",
    title="Dropdown Menu Radio Group",
    subcategory="Selection",
    description="Mutually exclusive menu options (role=menuitemradio + aria-checked) for settings like theme or sort order — exactly one checked, controlled or uncontrolled.",
    tags=TAGS_BASE + ["radio", "selection", "single-select", "theme", "sort"],
    features=FEAT_BASE + ["role=menuitemradio", "aria-checked exclusivity", "controlled + uncontrolled"],
    accessibility=A11Y_BASE + ["role=menuitemradio in role=group", "aria-checked announced", "aria-hidden dot indicator"],
    interactive=True,
    related=["dropdown-menu", "dropdown-menu-checkboxes", "dropdown-menu-with-sections"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
} from "./dropdown-menu-radio";

const [theme, setTheme] = useState("system");

<DropdownMenu>
  <DropdownMenuTrigger>Theme</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel>Appearance</DropdownMenuLabel>
    <DropdownMenuRadioGroup value={theme} onValueChange={setTheme}>
      <DropdownMenuRadioItem value="system">System</DropdownMenuRadioItem>
      <DropdownMenuRadioItem value="light">Light</DropdownMenuRadioItem>
      <DropdownMenuRadioItem value="dark">Dark</DropdownMenuRadioItem>
    </DropdownMenuRadioGroup>
  </DropdownMenuContent>
</DropdownMenu>

// Uncontrolled: <DropdownMenuRadioGroup defaultValue="system">…''',
    props_doc=props_table(RADIO_GROUP_PROPS, RADIO_ITEM_PROPS),
    composition_note="`<DropdownMenuRadioGroup>` wraps a set of `<DropdownMenuRadioItem>` options in `role=\"group\"` and owns the single selected value through context. Pair it with a `<DropdownMenuLabel>` for context, and use plain items or separators above and below as needed.",
    logic_doc=RADIO_LOGIC,
    keyboard_doc=KEYBOARD_BASE.replace(
        "| `Enter` / `Space` (menu) | Activate the focused item (native button behavior) |",
        "| `Enter` / `Space` (menu) | Activate the focused item; on a radio item, selects it (only one option is checked) |"),
    behavior_doc=STATES_BASE + """
- **Radio item (checked)** — the leading dot glyph fades in (`--ds-color-primary`), `aria-checked="true"`; exactly one option in the group is checked at a time.
- **Radio item (unchecked)** — the indicator slot stays empty, reserving alignment.
- **Radio item (disabled)** — native `disabled`; a disabled selected option keeps its dot visible but cannot be changed by pointer or keys.""",
    a11y_doc="Exclusivity is communicated by `role=\"menuitemradio\"` + `aria-checked` inside a `role=\"group\"` — assistive technology announces both the state and the grouping. These are real buttons with native Space/Enter activation, not divs styled to look like radios.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Use radio groups for mutually exclusive choices (theme, sort order, density). For independent toggles use dropdown-menu-checkboxes. The group value is a plain string — map it to your app's setting in `onValueChange`.",
    showcase=DEMO_HELPERS + '''
const THEMES = [["system", "System"], ["light", "Light"], ["dark", "Dark"]];
function ThemeMenu() {
  const [theme, setTheme] = React.useState("system");
  return (
    <div className="space-y-3">
      <DropdownMenu>
        <DropdownMenuTrigger>Theme: {THEMES.find(([v]) => v === theme)[1]}</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel>Appearance</DropdownMenuLabel>
          <DropdownMenuRadioGroup value={theme} onValueChange={setTheme} aria-label="Theme">
            {THEMES.map(([value, label]) => (
              <DropdownMenuRadioItem key={value} value={value}>{label}</DropdownMenuRadioItem>
            ))}
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Controlled — the trigger label mirrors the selected theme.</p>
    </div>
  );
}
function SortMenu() {
  const [sort, setSort] = React.useState("modified");
  return (
    <div className="space-y-3">
      <DropdownMenu>
        <DropdownMenuTrigger>Sort files</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuLabel id="sort-label">Sort by</DropdownMenuLabel>
          <DropdownMenuRadioGroup defaultValue="modified" onValueChange={setSort} aria-labelledby="sort-label">
            <DropdownMenuRadioItem value="name">Name</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="modified">Date modified</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="size">Size</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="kind" disabled>Kind (Pro plan)</DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
      <p className={NOTE}>Uncontrolled with a defaultValue; current sort: {{name: "Name", modified: "Date modified", size: "Size"}[sort] || sort}.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Theme — controlled</p>
        <ThemeMenu />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Sort order — uncontrolled</p>
        <SortMenu />
      </div>
    </div>
  );
}''',
)

# 8. dropdown-menu-submenu
SUBMENU_KEYBOARD = """| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the menu, focus the first item |
| `ArrowDown` / `ArrowUp` | Move focus between enabled items at the current level, wrapping |
| `ArrowRight` (sub trigger) | Open the submenu, focus its first item |
| `ArrowLeft` (submenu) | Close the submenu, focus its sub trigger |
| `Enter` / `Space` (sub trigger) | Open the submenu, focus its first item |
| `Home` / `End` | Focus the first / last enabled item at the current level |
| `Escape` (submenu) | Close only the submenu, focus its sub trigger |
| `Escape` (top-level menu) | Close the whole menu, focus the root trigger |
| `Tab` | Close the whole menu and move focus forward naturally |

Pointer: hovering a sub trigger opens its submenu without moving focus; hovering a sibling item closes the open submenu at that level; clicking a sub trigger opens it and focuses the first item."""

SUBMENU_LOGIC = """Submenus add one nested level through three primitives:

- `DropdownMenuSub` — owns the nested open state and registers a close callback with the parent menu level, so pointer interaction with a sibling item closes the open submenu.
- `DropdownMenuSubTrigger` — a `role="menuitem"` with `aria-haspopup="menu"` + `aria-expanded` and a trailing chevron-right. ArrowRight / Enter / Space open the submenu and focus its first item; hover opens it without moving focus.
- `DropdownMenuSubContent` — the nested `role="menu"` panel, labelled by its sub trigger. It opens to the right of the trigger and flips to the left when the right side would leave the viewport.

Focus moves predictably: into the submenu on open, back to the sub trigger on ArrowLeft / Escape / sibling-close, and back to the root trigger when the whole menu closes. Closing a submenu never strands focus inside a removed panel — it falls back to the sub trigger. Activating a leaf item still closes the whole tree and returns focus to the root trigger.""" + "\n\n" + LOGIC_BASE.split("The panel opens relative")[0].rstrip()

register(
    "dropdown-menu-submenu",
    title="Dropdown Menu Submenu",
    subcategory="Composite",
    description="One nested menu level with correct menu semantics: ArrowRight opens, ArrowLeft closes, Escape collapses only the submenu, and the panel flips sides at the viewport edge.",
    tags=TAGS_BASE + ["submenu", "nested", "flyout"],
    features=FEAT_BASE + ["nested submenu", "ArrowRight/ArrowLeft level navigation", "side flip at viewport edge", "hover open without focus theft"],
    accessibility=A11Y_BASE + ["nested role=menu panels", "aria-haspopup sub trigger", "level-scoped Escape", "focus never stranded"],
    interactive=True,
    related=["dropdown-menu", "dropdown-menu-with-sections", "dropdown-menu-with-icons"],
    usage='''import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
} from "./dropdown-menu-submenu";

<DropdownMenu>
  <DropdownMenuTrigger>File</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Open</DropdownMenuItem>
    <DropdownMenuSub>
      <DropdownMenuSubTrigger>Share</DropdownMenuSubTrigger>
      <DropdownMenuSubContent>
        <DropdownMenuItem>Copy link</DropdownMenuItem>
        <DropdownMenuItem>Email</DropdownMenuItem>
        <DropdownMenuItem>Export as PDF</DropdownMenuItem>
      </DropdownMenuSubContent>
    </DropdownMenuSub>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Archive</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>''',
    props_doc=props_table(SUB_PROPS, SUB_TRIGGER_PROPS, SUB_CONTENT_PROPS),
    composition_note="A submenu is a `<DropdownMenuSub>` wrapping exactly one `<DropdownMenuSubTrigger>` and one `<DropdownMenuSubContent>`, placed inline among the parent menu's items. The primitives nest recursively, but one level covers almost every real use case — deeper nesting is an information-architecture smell.",
    logic_doc=SUBMENU_LOGIC,
    keyboard_doc=SUBMENU_KEYBOARD,
    behavior_doc=STATES_BASE + """
- **Sub trigger** — a menu item with a trailing chevron-right affordance; while its submenu is open it keeps `aria-expanded=\"true\"`.
- **Submenu panel** — same surface/border/shadow model as the root panel, anchored to the sub trigger's side instead of below the root trigger.""",
    a11y_doc="Each level is its own `role=\"menu\"` labelled by its own trigger, and key handling is level-scoped: Escape and ArrowLeft collapse only the innermost open level. The root trigger's `aria-controls` chain stays intact because submenus live inside the root panel's DOM subtree.",
    responsive_doc=RESPONSIVE_BASE + """ Submenus open to the side rather than below, so the level flip (right ↔ left) is what keeps them on screen on narrow viewports; combined with the panel width cap, a submenu stays fully usable at 375px.""",
    notes_doc="Hover opens a submenu without moving focus (pointer users keep pointing); keyboard opens move focus to the first sub item. The two entry modes are deliberate — focus follows the modality that opened the level.",
    showcase=DEMO_HELPERS + '''
function FileActions() {
  const [lastAction, setLastAction] = React.useState("None yet");
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <div className={ROW}>
          <div className="flex min-w-0 items-center gap-3">
            <span className="inline-flex size-8 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] text-[var(--ds-color-muted-foreground)] [&_svg]:size-4"><Icon name="file" /></span>
            <div className="min-w-0">
              <p className={ROW_NAME}>Launch checklist.md</p>
              <p className={ROW_META}>Document · Shared with 6 people</p>
            </div>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger>File</DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onSelect={() => setLastAction("Open")}>Open</DropdownMenuItem>
              <DropdownMenuSub>
                <DropdownMenuSubTrigger icon={<Icon name="share" />}>Share</DropdownMenuSubTrigger>
                <DropdownMenuSubContent>
                  <DropdownMenuItem icon={<Icon name="link" />} onSelect={() => setLastAction("Share → Copy link")}>Copy link</DropdownMenuItem>
                  <DropdownMenuItem icon={<Icon name="mail" />} onSelect={() => setLastAction("Share → Email")}>Email</DropdownMenuItem>
                  <DropdownMenuItem icon={<Icon name="download" />} onSelect={() => setLastAction("Share → Export as PDF")}>Export as PDF</DropdownMenuItem>
                </DropdownMenuSubContent>
              </DropdownMenuSub>
              <DropdownMenuSub>
                <DropdownMenuSubTrigger icon={<Icon name="folder" />}>Move to</DropdownMenuSubTrigger>
                <DropdownMenuSubContent>
                  <DropdownMenuItem onSelect={() => setLastAction("Move to → Projects")}>Projects</DropdownMenuItem>
                  <DropdownMenuItem onSelect={() => setLastAction("Move to → Personal")}>Personal</DropdownMenuItem>
                  <DropdownMenuItem onSelect={() => setLastAction("Move to → Archive")}>Archive</DropdownMenuItem>
                </DropdownMenuSubContent>
              </DropdownMenuSub>
              <DropdownMenuSeparator />
              <DropdownMenuItem onSelect={() => setLastAction("Rename")}>Rename</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      <p className={NOTE}>Last action: {lastAction}. Try ArrowRight on Share, then ArrowLeft or Escape to come back.</p>
    </div>
  );
}
function EdgeMenu() {
  return (
    <div className="space-y-3">
      <div className="flex justify-end">
        <DropdownMenu placement="bottom-end">
          <DropdownMenuTrigger>Row actions</DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem>View order</DropdownMenuItem>
            <DropdownMenuSub>
              <DropdownMenuSubTrigger>Assign to</DropdownMenuSubTrigger>
              <DropdownMenuSubContent>
                <DropdownMenuItem>Mina Chen</DropdownMenuItem>
                <DropdownMenuItem>Jonas Weber</DropdownMenuItem>
                <DropdownMenuItem>Aisha Bello</DropdownMenuItem>
              </DropdownMenuSubContent>
            </DropdownMenuSub>
            <DropdownMenuItem>Refund order</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <p className={NOTE}>Against the right edge, the submenu flips and opens to the left.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>File actions — share and move submenus</p>
        <FileActions />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Viewport-edge flip</p>
        <EdgeMenu />
      </div>
    </div>
  );
}''',
)
