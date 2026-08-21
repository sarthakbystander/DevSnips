"""Registry for the DevSnips React Tooltips generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference ``tooltip/code.tsx``). The
generator (``_gen_react_tooltips.py``) combines these with the reference
``code.tsx`` on disk to write ``code.tsx`` (derived), ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Direction is a PROP (`side` × `align`), not a variant — the placement variant
demonstrates the full matrix through props. Realistic, product-oriented demo
content only (projects, exports, reports, workspace settings). No lorem
ipsum, no marketing buzzwords.
"""
from _gen_react_tooltips import (
    register,
    LOGIC_BASE,
    POSITIONING_BASE,
    KEYBOARD_BASE,
    STATES_BASE,
    RESPONSIVE_BASE,
)

TAGS_BASE = ["tooltip", "react", "tailwind", "accessible", "keyboard", "hover", "focus", "responsive", "interactive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "role=tooltip semantics", "hover + focus open", "Escape to dismiss", "viewport flip", "controlled/uncontrolled"]
A11Y_BASE = ['role="tooltip" content', "aria-describedby wiring", "keyboard focus opens (no hover-only)", "Escape dismisses", "pointer-events-none content", "supplementary information only"]

# Shared props tables. The three primitives carry the same API family-wide.
TOOLTIP_PROPS = r"""### `<Tooltip>`

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
| `children` | `ReactNode` | — | A single `TooltipTrigger` + a single `TooltipContent`. |"""

TRIGGER_PROPS = r"""### `<TooltipTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `children` | `ReactElement` | — | Exactly one element: a native focusable element (`<button>`, `<a>`, `<input>`, …) or a component that forwards its ref and the pointer/focus handlers. |

`TooltipTrigger` clones the child to attach the trigger ref, the hover/focus handlers, and `aria-describedby` pointing at the tooltip. The child's own handlers run first and can cancel the tooltip behavior with `event.preventDefault()`. The trigger must be focusable — a tooltip must never depend on hover alone. For a natively `disabled` control (which cannot receive hover or focus), wrap it in a `<span tabIndex={0}>` so the explanation stays reachable — see `tooltip-disabled-trigger`."""

CONTENT_PROPS = r"""### `<TooltipContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="tooltip"` bubble (e.g. a larger `max-w-*`). |
| `children` | `ReactNode` | — | Text or structured, **non-interactive** content. |

`role="tooltip"` is fixed; every native `div` attribute (`aria-*`, `data-*`, …) is forwarded via `...rest`. Rendered only while open, `pointer-events-none`, capped at `min(16rem, 100vw - 2rem)` wide. Content that must be clicked or focused does not belong in a tooltip — use a popover or a dialog instead."""


def props_table():
    return "\n\n".join([TOOLTIP_PROPS, TRIGGER_PROPS, CONTENT_PROPS])


# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = """const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const CARD = "rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4";
const ROW = "flex items-center justify-between gap-4";
const ROW_NAME = "m-0 text-sm font-medium text-[var(--ds-color-foreground)]";
const ROW_META = "m-0 text-xs text-[var(--ds-color-muted-foreground)]";
const BTN_PRIMARY = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_OUTLINE = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const ICON_BUTTON = "inline-flex size-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-muted-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const INFO_BUTTON = "inline-flex size-[18px] shrink-0 items-center justify-center rounded-[var(--ds-radius-full)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const SELECT = "h-9 w-full rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const KBD = "rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-1 py-px font-mono text-[11px] leading-4 text-[var(--ds-color-foreground)]";
const DISABLED_WRAP = "inline-flex cursor-not-allowed rounded-[var(--ds-radius-sm)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";
"""

# 1. tooltip (reference)
register(
    "tooltip",
    title="Tooltip",
    subcategory="Core",
    description="The canonical compound tooltip: a real focusable trigger (aria-describedby), a role=tooltip bubble with a pointing arrow, hover-open after a short delay, immediate keyboard-focus open, and Escape/blur/pointer-leave dismissal.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["tooltip-placement", "tooltip-with-icon", "tooltip-controlled", "tooltip-disabled-trigger"],
    usage='''import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip";

<Tooltip>
  <TooltipTrigger>
    <button type="button" aria-label="About the retention period">
      <InfoIcon />
    </button>
  </TooltipTrigger>
  <TooltipContent>
    How long deleted projects stay recoverable.
  </TooltipContent>
</Tooltip>

// Placement is a prop, not a variant:
<Tooltip side="right" align="start" sideOffset={8}>…</Tooltip>

// Uncontrolled (default) or controlled:
const [open, setOpen] = useState(false);
<Tooltip open={open} onOpenChange={setOpen}>…</Tooltip>''',
    props_doc=props_table(),
    composition_note="This is the reference composition — every other variant in the family uses the same three primitives and extends the same class constants, placement model, and accessibility model. Direction is never a separate component: `side` and `align` are props on the root.",
    logic_doc=LOGIC_BASE,
    positioning_doc=POSITIONING_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="The info trigger is a real `<button type=\"button\">` with its own `aria-label`, so it is reachable by keyboard and announced correctly even before the tooltip opens; the tooltip then supplies the longer description through `aria-describedby`. Mounting several `<Tooltip>` roots on one page is safe: each root scopes its own id, timer, and listeners — hover or focus on one trigger dismisses the others naturally (through pointer leave / blur), and Escape dismisses whichever is open.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Reference implementation for the Tooltips family. It establishes the shared tooltip geometry (radius-md bubble, 10px/6px padding rhythm, 16rem measure, 6px default offset), the arrow treatment, the hover-delay vs immediate-focus-open model, the pointer/focus ownership handoff, and the measure-then-flip placement that every other variant reuses.",
    tsx_header="",
    showcase=DEMO_HELPERS + '''
function RetentionField() {
  return (
    <div className={CARD + " w-full max-w-xl space-y-4"}>
      <div>
        <div className="flex items-center gap-1.5">
          <label htmlFor="retention" className="text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">Retention period</label>
          <Tooltip>
            <TooltipTrigger>
              <button type="button" aria-label="About the retention period" className={INFO_BUTTON}>
                <Icon name="info" className="size-3.5" />
              </button>
            </TooltipTrigger>
            <TooltipContent>
              How long deleted projects stay recoverable. When the period ends, they are removed permanently.
            </TooltipContent>
          </Tooltip>
        </div>
        <select id="retention" className={SELECT + " mt-1.5"}>
          <option>7 days</option>
          <option>30 days</option>
          <option>90 days</option>
        </select>
      </div>
      <div className="flex items-center justify-end gap-2 border-t border-[var(--ds-color-border-subtle)] pt-3">
        <Tooltip>
          <TooltipTrigger>
            <button type="button" className={BTN_PRIMARY}>Save changes</button>
          </TooltipTrigger>
          <TooltipContent>Applies to every project in this workspace.</TooltipContent>
        </Tooltip>
      </div>
    </div>
  );
}

function ReportToolbar() {
  return (
    <div className={CARD + " flex items-center justify-between gap-4"}>
      <div className="min-w-0">
        <p className={ROW_NAME}>Quarterly report</p>
        <p className={ROW_META}>Generated 12 minutes ago</p>
      </div>
      <div className="flex items-center gap-2">
        <Tooltip>
          <TooltipTrigger>
            <button type="button" aria-label="Refresh report" className={ICON_BUTTON}>
              <Icon name="refresh" className="size-4" />
            </button>
          </TooltipTrigger>
          <TooltipContent>Refresh report</TooltipContent>
        </Tooltip>
        <Tooltip>
          <TooltipTrigger>
            <button type="button" aria-label="Download report" className={ICON_BUTTON}>
              <Icon name="download" className="size-4" />
            </button>
          </TooltipTrigger>
          <TooltipContent>Download as CSV</TooltipContent>
        </Tooltip>
      </div>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Field help — uncontrolled</p>
        <RetentionField />
        <p className={NOTE}>Hover the info trigger, or Tab to it: focus opens the tooltip without the hover delay. Escape or moving away dismisses it.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Adjacent tooltips — one at a time</p>
        <ReportToolbar />
        <p className={NOTE}>Moving between triggers closes the first tooltip before the second opens; only one is ever visible.</p>
      </div>
    </div>
  );
}''',
)

# 2. tooltip-placement
register(
    "tooltip-placement",
    title="Tooltip Placement",
    subcategory="Positioning",
    description="The full placement matrix through props — side × align on one shared core — plus the viewport correction: a trigger at the page edge flips its tooltip instead of overflowing.",
    tags=TAGS_BASE + ["placement", "positioning"],
    features=FEAT_BASE + ["side × align matrix", "edge flip demo", "align shift demo"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["tooltip", "tooltip-with-long-content", "tooltip-controlled"],
    usage='''import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-placement";

<Tooltip side="top" align="center">…</Tooltip>
<Tooltip side="right" align="start">…</Tooltip>
<Tooltip side="bottom" align="end" sideOffset={8}>…</Tooltip>
<Tooltip side="left">…</Tooltip>

// The preferred placement is a hint: when it would overflow the
// viewport, the tooltip flips (top ↔ bottom, left ↔ right) or shifts
// its alignment before paint — no flip is ever visible.''',
    props_doc=props_table(),
    composition_note="All twelve combinations below are the same three primitives; only the `side` / `align` props change. The arrow follows the resolved placement — including after a flip.",
    logic_doc=LOGIC_BASE,
    positioning_doc=POSITIONING_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Placement is purely visual: the accessibility tree only ever sees the trigger and its `aria-describedby` description, regardless of side, alignment, or a flip.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The 12-button matrix proves the placement model on one shared core (direction is a prop, not a component). The edge demo pins a trigger to the trailing edge of the page: at 375px its `side=\"right\"` tooltip has no room and resolves to the left — shrink the viewport to watch the correction. The same measurement also degrades `align=\"center\"` to `start` / `end` when a wide bubble would overflow a narrow screen.",
    tsx_header="""/**
 * DevSnips React Tooltip — placement matrix variant.
 *
 * Identical core to the reference tooltip; this variant demonstrates the
 * prop-driven placement model: `side` (top/right/bottom/left) × `align`
 * (start/center/end) × `sideOffset`, with pre-paint viewport correction
 * (side flip + alignment shift) and an arrow that follows the resolved
 * placement. Direction is a prop, never a separate component.
 */""",
    showcase=DEMO_HELPERS + '''
const PLACEMENTS = [
  ["top", "start"], ["top", "center"], ["top", "end"],
  ["right", "start"], ["right", "center"], ["right", "end"],
  ["bottom", "start"], ["bottom", "center"], ["bottom", "end"],
  ["left", "start"], ["left", "center"], ["left", "end"],
];

const PLACEMENT_BUTTON = "inline-flex h-9 w-full items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-2 font-mono text-[11px] leading-4 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";

function PlacementMatrix() {
  return (
    <div className={CARD + " mx-auto w-full max-w-md"}>
      <div className="grid grid-cols-3 gap-2">
        {PLACEMENTS.map(([side, align]) => (
          <Tooltip key={side + "-" + align} side={side} align={align}>
            <TooltipTrigger>
              <button type="button" className={PLACEMENT_BUTTON}>{side} · {align}</button>
            </TooltipTrigger>
            <TooltipContent>side={side}, align={align}</TooltipContent>
          </Tooltip>
        ))}
      </div>
    </div>
  );
}

function EdgeFlip() {
  return (
    <div className={CARD + " flex items-center justify-between gap-4"}>
      <div className="min-w-0">
        <p className={ROW_NAME}>Edge trigger</p>
        <p className={ROW_META}>Prefers side=right — flips left when there is no room</p>
      </div>
      <Tooltip side="right">
        <TooltipTrigger>
          <button type="button" className={BTN_OUTLINE}>Publish site</button>
        </TooltipTrigger>
        <TooltipContent>Publish the draft.</TooltipContent>
      </Tooltip>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>side × align — the prop-driven matrix</p>
        <PlacementMatrix />
        <p className={NOTE}>Hover or Tab through the grid. Direction is a prop: every cell is the same component with a different side + align.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Viewport correction</p>
        <EdgeFlip />
        <p className={NOTE}>At narrow widths the preferred side=right overflows, so the tooltip resolves to the left before paint. Try it at 375px.</p>
      </div>
    </div>
  );
}''',
)

# 3. tooltip-with-icon
register(
    "tooltip-with-icon",
    title="Tooltip with Icon Trigger",
    subcategory="Content",
    description="Icon-only toolbar buttons: every trigger carries a real aria-label (the accessible name), and the tooltip makes that name visible on hover or focus — the standard pattern for toolbars and action rows.",
    tags=TAGS_BASE + ["icon", "toolbar"],
    features=FEAT_BASE + ["icon-only triggers", "aria-label naming", "toolbar composition"],
    accessibility=A11Y_BASE + ["aria-label on every icon-only trigger"],
    interactive=True,
    related=["tooltip", "tooltip-rich-content", "tooltip-disabled-trigger"],
    usage='''import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-with-icon";

<Tooltip>
  <TooltipTrigger>
    <button type="button" aria-label="Copy link">
      <CopyIcon />
    </button>
  </TooltipTrigger>
  <TooltipContent>Copy link</TooltipContent>
</Tooltip>''',
    props_doc=props_table(),
    composition_note="An icon-only trigger must name itself: the button carries the real `aria-label` (that is its accessible name — the SVG is `aria-hidden`), and the tooltip renders the same label visually. The tooltip complements the name; it never replaces it.",
    logic_doc=LOGIC_BASE,
    positioning_doc=POSITIONING_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Without visible text, an icon button's only accessible name is its `aria-label` — so the label exists even where tooltips never appear (screen readers before interaction, touch devices, voice control). The tooltip then exposes the identical label to sighted pointer and keyboard users. Icon glyphs are `aria-hidden`; meaning comes from the label, not the graphic.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The toolbar row is the everyday use of this variant: five icon-only actions, each a 36px control with `aria-label` + matching tooltip. Keyboard users Tab through the row and get the same names as pointer users, with no hover delay.",
    tsx_header="""/**
 * DevSnips React Tooltip — icon-trigger variant.
 *
 * Identical core to the reference tooltip; this variant demonstrates the
 * icon-only trigger pattern: a real button whose accessible name comes
 * from its own aria-label, with the tooltip rendering the same label on
 * hover and keyboard focus.
 */""",
    showcase=DEMO_HELPERS + '''
const ACTIONS = [
  { icon: "copy", label: "Copy link" },
  { icon: "download", label: "Download report" },
  { icon: "share", label: "Share dashboard" },
  { icon: "settings", label: "Report settings" },
  { icon: "trash", label: "Delete report" },
];

function IconToolbar() {
  return (
    <div className={CARD + " flex items-center justify-between gap-4"}>
      <div className="min-w-0">
        <p className={ROW_NAME}>Weekly analytics</p>
        <p className={ROW_META}>Aug 10 – Aug 16 · Shared with the workspace</p>
      </div>
      <div role="toolbar" aria-label="Report actions" className="flex items-center gap-1.5">
        {ACTIONS.map((action) => (
          <Tooltip key={action.icon}>
            <TooltipTrigger>
              <button type="button" aria-label={action.label} className={ICON_BUTTON}>
                <Icon name={action.icon} className="size-4" />
              </button>
            </TooltipTrigger>
            <TooltipContent>{action.label}</TooltipContent>
          </Tooltip>
        ))}
      </div>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Report actions — icon-only triggers</p>
        <IconToolbar />
        <p className={NOTE}>Each button names itself with aria-label; the tooltip shows the same name to sighted users. Tab through the row — focus opens each tooltip immediately.</p>
      </div>
    </div>
  );
}''',
)

# 4. tooltip-with-long-content
register(
    "tooltip-with-long-content",
    title="Tooltip with Long Content",
    subcategory="Content",
    description="Multi-sentence explanations that stay readable: the bubble wraps at a 16rem measure, caps itself to the viewport on small screens, and keeps the arrow aligned after any correction.",
    tags=TAGS_BASE + ["long content", "wrapping"],
    features=FEAT_BASE + ["16rem readable measure", "viewport-capped width", "multi-line wrapping"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["tooltip", "tooltip-rich-content", "tooltip-placement"],
    usage='''import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-with-long-content";

<Tooltip>
  <TooltipTrigger>
    <button type="button" aria-label="About data residency">
      <InfoIcon />
    </button>
  </TooltipTrigger>
  <TooltipContent>
    Two or three sentences are fine. The bubble wraps at 16rem and never
    exceeds the viewport width, so the explanation stays readable.
  </TooltipContent>
</Tooltip>''',
    props_doc=props_table(),
    composition_note="Long content needs no extra API: `TooltipContent` already caps the bubble at `min(16rem, 100vw - 2rem)` and wraps. A larger ceiling is a `className` away (`max-w-[20rem]`) — but if you regularly need more than two or three sentences, the content wants a popover or a dialog, not a bigger tooltip.",
    logic_doc=LOGIC_BASE,
    positioning_doc=POSITIONING_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Long explanations are announced as one description through `aria-describedby`. Keep them plain text: no links, no buttons, no lists that must be operated — a screen-reader user can re-read the description, but cannot interact with anything inside a tooltip.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Both demos carry genuine multi-sentence content (data residency, billing cycles). At 375px the bubble caps at the viewport width minus a 2rem margin and the placement correction keeps it on-screen — long content never scrolls the page.",
    tsx_header="""/**
 * DevSnips React Tooltip — long-content variant.
 *
 * Identical core to the reference tooltip; this variant demonstrates
 * multi-sentence content: the bubble wraps at a readable 16rem measure,
 * caps itself to the viewport on small screens, and keeps its placement
 * (and arrow) correct after the viewport correction.
 */""",
    showcase=DEMO_HELPERS + '''
function ResidencyHelp() {
  return (
    <div className={CARD + " w-full max-w-xl space-y-3"}>
      <div className="flex items-center gap-1.5">
        <span className="text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">Data residency</span>
        <Tooltip>
          <TooltipTrigger>
            <button type="button" aria-label="About data residency" className={INFO_BUTTON}>
              <Icon name="database" className="size-3.5" />
            </button>
          </TooltipTrigger>
          <TooltipContent>
            Your workspace data is stored and processed in the region you choose here. Moving regions starts a background migration — typically under an hour — and your data stays readable in the current region until it finishes.
          </TooltipContent>
        </Tooltip>
      </div>
      <p className={ROW_META}>Current region: eu-central (Frankfurt)</p>
    </div>
  );
}

function BillingHelp() {
  return (
    <div className={CARD + " flex items-center justify-between gap-4"}>
      <div className="min-w-0">
        <p className={ROW_NAME}>Next invoice</p>
        <p className={ROW_META}>$49.00 on Sep 1, 2026</p>
      </div>
      <Tooltip align="end">
        <TooltipTrigger>
          <button type="button" className={BTN_OUTLINE}>What is included?</button>
        </TooltipTrigger>
        <TooltipContent>
          Your invoice covers the Team plan for up to 10 seats, 100 GB of versioned storage, and priority support. Extra seats are prorated to the day they were added; you only ever pay for the time a seat was active.
        </TooltipContent>
      </Tooltip>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Field explanation — multi-sentence</p>
        <ResidencyHelp />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Inline help — wrapped at a readable measure</p>
        <BillingHelp />
        <p className={NOTE}>Both bubbles wrap at 16rem and stay inside the viewport at any width. Two or three sentences is the practical ceiling for a tooltip.</p>
      </div>
    </div>
  );
}''',
)

# 5. tooltip-rich-content
register(
    "tooltip-rich-content",
    title="Tooltip with Rich Content",
    subcategory="Content",
    description="Structured — still non-interactive — content: a title row, supporting metadata, a status dot, or a keyboard-shortcut chip, composed with plain markup inside TooltipContent.",
    tags=TAGS_BASE + ["rich content", "structured", "shortcut"],
    features=FEAT_BASE + ["title + metadata structure", "kbd chip", "status dot", "non-interactive content"],
    accessibility=A11Y_BASE + ["structured content, still announced as one description"],
    interactive=True,
    related=["tooltip", "tooltip-with-icon", "tooltip-with-long-content"],
    usage='''import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-rich-content";

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
</Tooltip>''',
    props_doc=props_table(),
    composition_note="`TooltipContent` accepts any ReactNode, so structure (a title row, muted metadata, a `<kbd>` chip, a status dot) is plain markup — no extra primitives. The constraint is behavioral, not visual: rich content stays **non-interactive**. The moment content needs a link, a button, or focus, it has outgrown the tooltip — use a popover or dialog.",
    logic_doc=LOGIC_BASE,
    positioning_doc=POSITIONING_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Structured content is still announced as one flat description through `aria-describedby` — screen readers read the title and metadata in order. Visual structure (weight, muted color, chips) is a sighted-user enhancement; never rely on it to carry meaning the words do not. Decorative glyphs inside the tooltip (the status dot) are `aria-hidden`.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Two compositions: a status pill whose tooltip adds a title plus freshness metadata (with an aria-hidden status dot), and a command button whose tooltip pairs the action name with a `<kbd>` shortcut chip and a usage hint. Both are text — nothing inside either bubble can or needs to be clicked.",
    tsx_header="""/**
 * DevSnips React Tooltip — rich-content variant.
 *
 * Identical core to the reference tooltip; this variant demonstrates
 * structured, non-interactive content inside TooltipContent: a title row,
 * muted metadata, a status dot, and a keyboard-shortcut chip. Rich is a
 * visual property only — interactive content belongs in a popover or
 * dialog, never in a tooltip.
 */""",
    showcase=DEMO_HELPERS + '''
const STATUS_PILL = "inline-flex h-8 items-center gap-2 rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";

function StatusPill() {
  return (
    <div className={CARD + " flex items-center justify-between gap-4"}>
      <div className="min-w-0">
        <p className={ROW_NAME}>Production</p>
        <p className={ROW_META}>6 services monitored</p>
      </div>
      <Tooltip side="bottom" align="end">
        <TooltipTrigger>
          <button type="button" className={STATUS_PILL}>
            <span aria-hidden="true" className="size-1.5 rounded-[var(--ds-radius-full)] bg-[var(--ds-color-success)]"></span>
            Operational
          </button>
        </TooltipTrigger>
        <TooltipContent className="space-y-1">
          <span className="block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">All systems operational</span>
          <span className="block text-xs leading-4 text-[var(--ds-color-muted-foreground)]">6 services · No open incidents · Checked 2 minutes ago</span>
        </TooltipContent>
      </Tooltip>
    </div>
  );
}

function CommandHint() {
  return (
    <div className={CARD + " flex items-center justify-between gap-4"}>
      <div className="min-w-0">
        <p className={ROW_NAME}>Navigation</p>
        <p className={ROW_META}>Jump to any page without leaving the keyboard</p>
      </div>
      <Tooltip>
        <TooltipTrigger>
          <button type="button" className={BTN_OUTLINE}>
            <Icon name="command" className="size-4" />
            Command palette
          </button>
        </TooltipTrigger>
        <TooltipContent className="space-y-1">
          <span className="block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">Open the command palette</span>
          <span className="block text-xs leading-4 text-[var(--ds-color-muted-foreground)]">Then type to search every page. <kbd className={KBD}>⌘K</kbd></span>
        </TooltipContent>
      </Tooltip>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Status pill — title + metadata</p>
        <StatusPill />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Command hint — title + shortcut chip</p>
        <CommandHint />
        <p className={NOTE}>Structure is plain markup inside TooltipContent. Everything stays non-interactive: the shortcut chip is a kbd element, not a button.</p>
      </div>
    </div>
  );
}''',
)

# 6. tooltip-disabled-trigger
register(
    "tooltip-disabled-trigger",
    title="Tooltip on a Disabled Trigger",
    subcategory="States",
    description="Two disabled patterns done correctly: explaining a natively disabled control via a focusable wrapper (hover AND keyboard reachable), and suppressing a tooltip entirely with the disabled prop.",
    tags=TAGS_BASE + ["disabled", "states"],
    features=FEAT_BASE + ["focusable wrapper pattern", "disabled prop suppression", "explanation on disabled control"],
    accessibility=A11Y_BASE + ["disabled control explanation stays keyboard-reachable"],
    interactive=True,
    related=["tooltip", "tooltip-with-icon", "tooltip-controlled"],
    usage='''import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-disabled-trigger";

// A disabled control cannot receive hover or focus — wrap it in a
// focusable span so the explanation stays reachable:
<Tooltip>
  <TooltipTrigger>
    <span tabIndex={0} className="inline-flex cursor-not-allowed">
      <button type="button" disabled className="pointer-events-none">
        Export CSV
      </button>
    </span>
  </TooltipTrigger>
  <TooltipContent>
    Export is available on the Team plan. Ask a workspace admin to upgrade.
  </TooltipContent>
</Tooltip>

// Suppress a tooltip entirely (hover and focus do nothing):
<Tooltip disabled>…</Tooltip>''',
    props_doc=props_table(),
    composition_note="The wrapper pattern needs no component support: the `<span tabIndex={0}>` is simply the trigger's child element, and the inner disabled control is made `pointer-events-none` so pointer events land on the wrapper. `TooltipTrigger` attaches everything to the wrapper. The `disabled` prop on the root is the other direction — it turns a tooltip off while leaving the control itself enabled.",
    logic_doc=LOGIC_BASE,
    positioning_doc=POSITIONING_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="A natively `disabled` control is skipped by the tab order and swallows pointer events — a tooltip attached to it directly would be invisible to exactly the users who need the explanation most. The `<span tabIndex={0}>` wrapper puts a focusable, hoverable target back in the page (with its own `:focus-visible` ring), and `aria-describedby` on the wrapper announces the reason. The inner control keeps its native `disabled`, so assistive technology still reports the action as unavailable. The wrapper pattern is for *explaining* disabled controls — it must not make the action itself operable.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="First demo: an Export action gated behind the Team plan — the tooltip explains why it is disabled and how to resolve it, reachable by pointer and keyboard. Second demo: a hints checkbox toggling the `disabled` prop — while off, hover and focus do nothing and an open tooltip closes. Both patterns are reachable without ever faking a disabled control with `aria-disabled` alone.",
    tsx_header="""/**
 * DevSnips React Tooltip — disabled-trigger variant.
 *
 * Identical core to the reference tooltip; this variant demonstrates the
 * two disabled patterns: (1) explaining a natively disabled control by
 * wrapping it in a focusable <span tabIndex={0}> (the inner control is
 * pointer-events-none), and (2) suppressing a tooltip entirely with the
 * root's `disabled` prop.
 */""",
    showcase=DEMO_HELPERS + '''
function GatedExport() {
  return (
    <div className={CARD + " flex items-center justify-between gap-4"}>
      <div className="min-w-0">
        <p className={ROW_NAME}>Usage report</p>
        <p className={ROW_META}>Aug 2026 · 1,284 events</p>
      </div>
      <Tooltip>
        <TooltipTrigger>
          <span tabIndex={0} className={DISABLED_WRAP}>
            <button type="button" disabled className={BTN_OUTLINE + " pointer-events-none"}>
              <Icon name="lock" className="size-4" />
              Export CSV
            </button>
          </span>
        </TooltipTrigger>
        <TooltipContent>Export is available on the Team plan. Ask a workspace admin to upgrade.</TooltipContent>
      </Tooltip>
    </div>
  );
}

function HintsToggle() {
  const [hints, setHints] = React.useState(true);
  return (
    <div className={CARD + " space-y-3"}>
      <label className="flex items-center gap-2 text-[13px] leading-5 text-[var(--ds-color-foreground)]">
        <input
          type="checkbox"
          checked={hints}
          onChange={(event) => setHints(event.target.checked)}
          className="size-4 accent-[var(--ds-color-accent)]"
        />
        Enable action hints
      </label>
      <div className="flex items-center justify-between gap-4 border-t border-[var(--ds-color-border-subtle)] pt-3">
        <div className="min-w-0">
          <p className={ROW_NAME}>Delete project</p>
          <p className={ROW_META}>Hint is suppressed while hints are off</p>
        </div>
        <Tooltip disabled={!hints}>
          <TooltipTrigger>
            <button type="button" className={BTN_OUTLINE}>Delete project</button>
          </TooltipTrigger>
          <TooltipContent>This cannot be undone. The project is archived for 30 days first.</TooltipContent>
        </Tooltip>
      </div>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Gated action — focusable wrapper</p>
        <GatedExport />
        <p className={NOTE}>The disabled button is wrapped in a span with tabIndex=0: hover OR Tab to it to learn why export is unavailable.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Suppressed hint — the disabled prop</p>
        <HintsToggle />
      </div>
    </div>
  );
}''',
)

# 7. tooltip-controlled
register(
    "tooltip-controlled",
    title="Tooltip with Controlled State",
    subcategory="State",
    description="Open state lifted to the parent: a copy action forces its confirmation tooltip open for a moment, an external toggle pins a hint open, and every request flows through onOpenChange.",
    tags=TAGS_BASE + ["controlled", "state"],
    features=FEAT_BASE + ["controlled open state", "onOpenChange sync", "programmatic open/close"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["tooltip", "tooltip-disabled-trigger", "tooltip-with-icon"],
    usage='''import Tooltip, { TooltipTrigger, TooltipContent } from "./tooltip-controlled";

const [open, setOpen] = useState(false);

<Tooltip open={open} onOpenChange={setOpen}>
  <TooltipTrigger>
    <button type="button" onClick={copyLink}>Copy link</button>
  </TooltipTrigger>
  <TooltipContent>Copied to clipboard</TooltipContent>
</Tooltip>

// The parent has the final say: open/hover requests arrive through
// onOpenChange, but the parent can force the tooltip open (confirmation
// feedback) or keep it closed regardless of hover.''',
    props_doc=props_table(),
    composition_note="Controlled mode changes who owns the state, not the composition: the same three primitives, but `<Tooltip>` never mutates `open` itself — it reports every request through `onOpenChange` and the parent decides. Parent-initiated changes (forcing the tooltip open after a copy) do not echo back through `onOpenChange`, exactly like a controlled `<input>`.",
    logic_doc=LOGIC_BASE,
    positioning_doc=POSITIONING_BASE,
    keyboard_doc=None,
    behavior_doc=STATES_BASE,
    a11y_doc="Controlled state does not change the announcement model: the trigger still carries `aria-describedby`, and the tooltip still appears on focus without a delay whenever the parent honors the request. A parent that overrides hover/focus requests (like the copy demo, which reserves the tooltip for confirmation) must keep the tooltip genuinely supplementary — the copy action here is already confirmed by the clipboard itself, so suppressing hover hints loses nothing essential.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="First demo: the copy tooltip is fully parent-owned — hover/focus requests are logged through `onOpenChange` but ignored, and clicking Copy forces the tooltip open for 1.6 seconds as confirmation feedback. Second demo: an external Show/Hide toggle pins a hint open without touching the trigger. The log line proves every state change flows through one callback.",
    tsx_header="""/**
 * DevSnips React Tooltip — controlled-state variant.
 *
 * Identical core to the reference tooltip; this variant demonstrates
 * controlled mode: the parent owns `open` + `onOpenChange`, forces the
 * tooltip open as confirmation feedback after a copy action, pins a hint
 * open from an external toggle, and observes every hover/focus/blur
 * request through the single callback.
 */""",
    showcase=DEMO_HELPERS + '''
function CopyConfirmation() {
  const LINK = "https://app.devsnips.dev/projects/atlas";
  const [, copy] = useCopy(1600);
  const [open, setOpen] = React.useState(false);
  const [log, setLog] = React.useState([]);
  const timer = React.useRef(null);
  React.useEffect(() => () => window.clearTimeout(timer.current), []);
  function handleOpenChange(next) {
    // Fully parent-owned: hover/focus requests are observed, not honored.
    setLog((l) => [...l.slice(-2), next ? "open requested" : "close requested"]);
  }
  function handleCopy() {
    copy(LINK);
    // Optimistic confirmation — the parent forces the tooltip open for a moment.
    window.clearTimeout(timer.current);
    setOpen(true);
    timer.current = window.setTimeout(() => setOpen(false), 1600);
  }
  return (
    <div className="space-y-3">
      <div className={CARD + " flex items-center justify-between gap-4"}>
        <div className="min-w-0">
          <p className={ROW_NAME}>Share link</p>
          <p className={ROW_META + " truncate font-mono"}>{LINK}</p>
        </div>
        <Tooltip open={open} onOpenChange={handleOpenChange}>
          <TooltipTrigger>
            <button type="button" className={BTN_OUTLINE} onClick={handleCopy}>
              <Icon name="copy" className="size-4" />
              Copy link
            </button>
          </TooltipTrigger>
          <TooltipContent>Copied to clipboard</TooltipContent>
        </Tooltip>
      </div>
      <p className={NOTE} aria-live="polite">onOpenChange log: {log.length ? log.join(" → ") : "—"}</p>
    </div>
  );
}

function PinnedHint() {
  const [open, setOpen] = React.useState(false);
  return (
    <div className="space-y-3">
      <div className={CARD + " flex items-center justify-between gap-4"}>
        <div className="min-w-0">
          <p className={ROW_NAME}>Review requested</p>
          <p className={ROW_META}>atlas-web · opened 3 days ago</p>
        </div>
        <div className="flex items-center gap-2">
          <Tooltip open={open} onOpenChange={setOpen}>
            <TooltipTrigger>
              <button type="button" aria-label="About the reviewers" className={ICON_BUTTON}>
                <Icon name="users" className="size-4" />
              </button>
            </TooltipTrigger>
            <TooltipContent>2 reviewers assigned · 1 approval still needed.</TooltipContent>
          </Tooltip>
          <button type="button" className={BTN_OUTLINE} onClick={() => setOpen((o) => !o)}>
            {open ? "Hide hint" : "Show hint"}
          </button>
        </div>
      </div>
      <p className={NOTE}>The toggle drives the same controlled state — the tooltip opens without the trigger being hovered or focused.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Copy confirmation — fully parent-owned</p>
        <CopyConfirmation />
        <p className={NOTE}>Hover requests are logged but ignored: the parent reserves the tooltip for the Copied confirmation, shown for 1.6s after a click.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Pinned hint — external toggle</p>
        <PinnedHint />
      </div>
    </div>
  );
}''',
)
