"""Registry for the DevSnips React Cards generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference ``card/code.tsx``). The
generator (``_gen_react_cards.py``) combines these with the reference
``code.tsx`` on disk to write ``code.tsx`` (derived), ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented demo content only (projects, deploys, usage,
reports, plans). No lorem ipsum, no marketing buzzwords, no emoji.
"""
from _gen_react_cards import (
    register,
    BASE_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, ACTION_PROPS,
    CONTENT_PROPS, FOOTER_PROPS, MEDIA_PROPS, SELECTABLE_PROPS, GROUP_PROPS,
    INTERACTIVE_PROPS, SKELETON_PROPS, props_table,
)

TAGS_BASE = ["card", "surface", "react", "tailwind", "accessible", "responsive", "tokens"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic regions", "token-driven surface"]

# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = r"""const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const BTN_PRIMARY = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_OUTLINE = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const ICON_BTN = "inline-flex size-8 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const CHIP = "inline-flex shrink-0 items-center gap-1 rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-2 py-0.5 text-[11px] font-medium text-[var(--ds-color-muted-foreground)]";
const META = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const STAT_LABEL = "m-0 text-xs font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const STAT_VALUE = "m-0 text-2xl font-semibold tracking-[-0.01em] tabular-nums text-[var(--ds-color-foreground)]";

// Stable, locally generated demo artwork (neutral grays — no external image
// dependencies, nothing that can disappear).
function demoImage(a, b) {
  var svg = "<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360' viewBox='0 0 640 360'>" +
    "<rect width='640' height='360' fill='" + a + "'/>" +
    "<rect x='24' y='24' width='592' height='312' rx='6' fill='none' stroke='" + b + "' stroke-width='2' opacity='0.5'/>" +
    "<circle cx='556' cy='76' r='28' fill='" + b + "' opacity='0.35'/>" +
    "<rect x='48' y='262' width='220' height='18' rx='4' fill='" + b + "' opacity='0.55'/>" +
    "<rect x='48' y='292' width='140' height='12' rx='4' fill='" + b + "' opacity='0.3'/>" +
    "</svg>";
  return "data:image/svg+xml," + encodeURIComponent(svg);
}
"""

KEYBOARD_STATIC = """The card surface itself is not focusable and carries no keyboard behavior — that is intentional, it is not a control. Every action rendered inside it (footer buttons, header icon buttons) is a native `<button>` or `<a>`, so Tab reaches it, Enter/Space activates it, and a `focus-visible` ring marks keyboard focus."""

A11Y_STATIC = """- The card is a plain structural `<div>` — no fake `role="button"`, no `tabIndex` on a container, no click handlers on `<div>` elements.
- `CardTitle` renders a real `<h3>` heading, so card titles participate in the page outline.
- Actions inside the card are real native controls with visible labels or explicit `aria-label`s and `focus-visible` rings.
- State and meaning are never carried by color alone."""

RESPONSIVE_BASE = """The card is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px titles and descriptions wrap, long words break, and the header action slot shrinks to its content instead of pushing text out (the header text column is `1fr` with a `min-w-0` grid track). Footer actions stack full-width below `sm` and lay out inline from `sm` up. No horizontal overflow at 375 / 768 / 1280px."""

STATES_BASE = """- **Surface** — `--ds-color-surface` with a 1px `--ds-color-border`, `radius-md`, and the restrained `shadow-xs` elevation (per the token rules: no floating-card aesthetics).
- **Title / description** — heading-md (18px, 600) on foreground; body-sm on `--ds-color-muted-foreground`.
- **Footer actions** — full-width stacked below `sm`, inline from `sm` up.
- **Disabled actions** — native `disabled`: 50% opacity, no pointer events, out of the tab order."""


# 1. card
register(
    "card",
    title="Card",
    subcategory="Core",
    description="The reference card: a restrained content surface (radius-md, 1px border, shadow-xs) with the header / content / footer region primitives. Every other variant in the family is built from these same primitives.",
    tags=TAGS_BASE + ["reference", "compound", "composition"],
    features=FEAT_BASE + ["compound regions", "real h3 title", "non-interactive surface"],
    accessibility=["real <h3> card title", "semantic header/content/footer regions", "no fake interactivity"],
    interactive=False,
    related=["card-with-header", "card-with-footer", "card-with-actions", "card-list"],
    usage='''import Card, {
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "./card";

<Card>
  <CardHeader>
    <CardTitle>Project overview</CardTitle>
    <CardDescription>Current project status and activity.</CardDescription>
  </CardHeader>
  <CardContent>…</CardContent>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, CONTENT_PROPS, FOOTER_PROPS]),
    composition_note="Only compose the regions a card needs — the base surface with a lone `CardContent` is a complete card, and the full header/content/footer composition adds structure only where it carries meaning.",
    logic_doc="""`Card` is a structural shell with no state and no behavior of its own. The regions stack in document order: `CardHeader` (title + description on the two-column grid), `CardContent` (the padded body), and `CardFooter` (pinned to the bottom of equal-height grid tracks via `mt-auto`).

The second demo below composes every region together — header, a definition-list body, and a footer with secondary + primary actions — to establish the shared visual language the rest of the family reuses.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The `Card` root forwards every attribute of a plain `<div>` (`id`, `aria-*`, `data-*`). If a whole card should be a click target, do not add a click handler here — use `InteractiveCard` or `SelectableCard` instead.",
    tsx_header='''/**
 * DevSnips React Card — reference implementation.
 *
 * A restrained content surface as a compound component: `<Card>` is the
 * structural shell (radius-md, 1px border, surface color, shadow-xs per the
 * token rules) and the region primitives compose inside it — `<CardHeader>`
 * (`<CardTitle>` + `<CardDescription>` + optional `<CardAction>` slot),
 * `<CardContent>`, `<CardFooter>`, and `<CardMedia>` for image-led cards.
 *
 * Three behavioral primitives cover the interactive patterns without ever
 * turning a plain `<div>` into a fake control:
 *
 * - `<SelectableCard>` — a native `<input type="radio">` / `type="checkbox"`
 *   whose entire card is its `<label>`; controlled and uncontrolled.
 * - `<SelectableCardGroup>` — a `<fieldset>`/`<legend>` radio group that owns
 *   the single selection so group state stays in sync in both modes.
 * - `<InteractiveCard>` — a whole-card navigation/action surface rendered as
 *   a REAL `<a href>` when `href` is set, otherwise a real `<button>`.
 *
 * `<CardSkeleton>` is the loading placeholder: predictable geometry, an
 * accessible busy state, and a reduced-motion-safe pulse.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Base surface — regions are optional</p>
        <Card className="max-w-sm">
          <CardContent>
            <p className="m-0 text-sm leading-5 text-[var(--ds-color-foreground)]">
              Webhooks are active for production deployments. Payloads are signed
              and retried for 24 hours.
            </p>
          </CardContent>
        </Card>
        <p className={NOTE}>The base Card is a non-interactive surface — structure only, no click target.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Full composition — header, content, footer</p>
        <Card className="max-w-sm">
          <CardHeader>
            <CardTitle>Project overview</CardTitle>
            <CardDescription>Current status and activity for the billing service.</CardDescription>
          </CardHeader>
          <CardContent>
            <dl className="m-0 grid grid-cols-2 gap-x-6 gap-y-3">
              <div>
                <dt className={META}>Status</dt>
                <dd className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">Healthy</dd>
              </div>
              <div>
                <dt className={META}>Region</dt>
                <dd className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">eu-central</dd>
              </div>
              <div>
                <dt className={META}>Deploys</dt>
                <dd className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">128 this month</dd>
              </div>
              <div>
                <dt className={META}>Uptime</dt>
                <dd className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">99.98%</dd>
              </div>
            </dl>
          </CardContent>
          <CardFooter className="sm:justify-end">
            <button type="button" className={BTN_OUTLINE}>Archive</button>
            <button type="button" className={BTN_PRIMARY}>Open project</button>
          </CardFooter>
        </Card>
        <p className={NOTE}>Footer actions stack full-width below 640px; resize to see the inline row.</p>
      </div>
    </div>
  );
}''',
)

# 2. card-with-header
register(
    "card-with-header",
    title="Card with Header",
    subcategory="Core",
    description="The header region in detail: a real `<h3>` title, a muted description, and the optional `CardAction` slot — laid out on a two-column grid so long titles wrap while the action stays pinned top-right.",
    tags=TAGS_BASE + ["header", "title", "description"],
    features=FEAT_BASE + ["two-column header grid", "long-title wrapping", "optional action slot"],
    accessibility=["real <h3> card title", "muted description paragraph", "action slot separate from title text"],
    interactive=False,
    related=["card", "card-with-actions", "card-with-footer"],
    usage='''import Card, {
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
} from "./card-with-header";

<Card>
  <CardHeader>
    <CardTitle>API usage</CardTitle>
    <CardDescription>Requests in the current billing period.</CardDescription>
    <CardAction>
      <button aria-label="More actions">…</button>
    </CardAction>
  </CardHeader>
  <CardContent>…</CardContent>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, ACTION_PROPS, CONTENT_PROPS]),
    composition_note="`CardHeader` is a `grid-cols-[1fr_auto]`: `CardTitle` and `CardDescription` stack in the text column, and `CardAction` occupies the auto-sized second column at the top. Omit `CardAction` and the second column collapses to zero width — no spacer markup needed.",
    logic_doc="""The header grid keeps the action slot aligned even when the title wraps to several lines: the text column is `1fr` with a zero minimum so long titles wrap, while the action column is `auto` and never shrinks.

The second demo renders an intentionally long title to show the wrap behavior — the description starts on its own row and the icon button stays at the top right instead of being pushed down or clipped.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC + """
- The title is a heading and the description is a plain paragraph — the action slot is not part of the heading text, so screen readers announce the title cleanly.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The `CardAction` slot composes real controls from the Buttons/Dropdowns families — see `card-with-actions` for a worked example.",
    tsx_header='''/**
 * DevSnips React Card — Header composition.
 *
 * The shared card core; this variant demonstrates the header region:
 * `CardTitle` (a real `<h3>`) + `CardDescription` + the optional
 * `CardAction` slot, laid out on the two-column header grid so long
 * titles wrap while the action stays pinned top-right.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Title + description</p>
        <Card className="max-w-sm">
          <CardHeader>
            <CardTitle>API usage</CardTitle>
            <CardDescription>Requests counted in the current billing period.</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="m-0 text-sm leading-5 text-[var(--ds-color-foreground)]">
              1.24M of 2M requests used. The period resets on the first of next month.
            </p>
          </CardContent>
        </Card>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Long title + header action</p>
        <Card className="max-w-sm">
          <CardHeader>
            <CardTitle>Design tokens migration for the white-label partner theme</CardTitle>
            <CardDescription>Tracks the move from hardcoded hex values to semantic tokens.</CardDescription>
            <CardAction>
              <button type="button" className={ICON_BTN} aria-label="More actions for tokens migration">
                <Icon name="more" className="size-4" />
              </button>
            </CardAction>
          </CardHeader>
          <CardContent>
            <p className="m-0 text-sm leading-5 text-[var(--ds-color-foreground)]">
              18 of 24 components migrated. Inputs and selects remain.
            </p>
          </CardContent>
        </Card>
        <p className={NOTE}>The title wraps while the action stays pinned top-right — no overlap, no clipping.</p>
      </div>
    </div>
  );
}''',
)

# 3. card-with-footer
register(
    "card-with-footer",
    title="Card with Footer",
    subcategory="Core",
    description="The footer region: a primary + secondary action row that stacks full-width on small screens, plus a split footer (metadata left, action right) via a `sm:justify-between` className override.",
    tags=TAGS_BASE + ["footer", "actions", "buttons"],
    features=FEAT_BASE + ["stack-to-inline action row", "split footer via className", "equal-height grid tracks"],
    accessibility=["footer actions are real buttons", "focus-visible rings", "primary last in DOM order"],
    interactive=True,
    related=["card", "card-with-header", "card-with-actions"],
    usage='''import Card, {
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "./card-with-footer";

<Card>
  <CardHeader>
    <CardTitle>Team plan</CardTitle>
  </CardHeader>
  <CardContent>…</CardContent>
  <CardFooter className="sm:justify-end">
    <button>Compare plans</button>
    <button>Upgrade</button>
  </CardFooter>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, HEADER_PROPS, TITLE_PROPS, CONTENT_PROPS, FOOTER_PROPS]),
    composition_note="`CardFooter` reuses the dialog-footer recipe: `flex-col-reverse` below `sm` (the primary action, last in DOM, lands on top of the stack) and an inline row from `sm` up. No justify utility is baked in — pass `sm:justify-end` for right-aligned actions or `sm:justify-between` for a split footer, and the override never conflicts.",
    logic_doc="""Footers pin to the bottom of the card (`mt-auto`), so cards in an equal-height grid keep their action rows aligned.

The first demo is the standard secondary + primary pair. The second is the split pattern: muted metadata on the left, a single action on the right, composed with `sm:justify-between` and a plain `<p>` — no special primitive needed. Both sets of actions are real `<button>` elements and stay reachable when they stack at 375px.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC + """
- The primary action is last in DOM order, so keyboard users reach the safe secondary action first when tabbing, and the destructive-or-committing action is never the first stop.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Footer content is not limited to buttons — links, metadata, and status chips all work. Keep interactive elements real (`<button>` / `<a>`).",
    tsx_header='''/**
 * DevSnips React Card — Footer composition.
 *
 * The shared card core; this variant demonstrates the footer region: a
 * primary + secondary action row that stacks full-width below `sm` (same
 * recipe as the dialog footer) and a split footer (metadata left, action
 * right) via `sm:justify-between`. `mt-auto` pins the footer to the bottom
 * of equal-height grid tracks.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Secondary + primary</p>
        <Card className="max-w-sm">
          <CardHeader>
            <CardTitle>Team plan</CardTitle>
            <CardDescription>For growing teams shipping every day.</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="m-0 text-sm leading-5 text-[var(--ds-color-foreground)]">
              $20 per member per month. Unlimited projects, preview deployments,
              and 1 TB of bandwidth included.
            </p>
          </CardContent>
          <CardFooter className="sm:justify-end">
            <button type="button" className={BTN_OUTLINE}>Compare plans</button>
            <button type="button" className={BTN_PRIMARY}>Upgrade to Team</button>
          </CardFooter>
        </Card>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Split footer — metadata + action</p>
        <Card className="max-w-sm">
          <CardHeader>
            <CardTitle>Usage report</CardTitle>
            <CardDescription>Bandwidth, builds, and function invocations for March.</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="m-0 text-sm leading-5 text-[var(--ds-color-foreground)]">
              Generated from metering data collected across all production projects.
            </p>
          </CardContent>
          <CardFooter className="sm:justify-between">
            <p className={META}>Generated Apr 1 · 4 pages</p>
            <button type="button" className={BTN_OUTLINE}>Download PDF</button>
          </CardFooter>
        </Card>
        <p className={NOTE}>Below 640px the metadata sits under the full-width button.</p>
      </div>
    </div>
  );
}''',
)

# 4. card-with-actions
register(
    "card-with-actions",
    title="Card with Actions",
    subcategory="Composite",
    description="Contextual actions in the `CardAction` header slot: real icon buttons (pin, settings, more) with accessible names and live feedback — composed from the same button recipe as the rest of the library, not re-implemented inside Cards.",
    tags=TAGS_BASE + ["actions", "icon-button", "contextual", "menu"],
    features=FEAT_BASE + ["header action slot", "icon buttons with aria-label", "live action feedback"],
    accessibility=["icon buttons carry aria-label", "focus-visible rings", "actions stay outside the heading text"],
    interactive=True,
    related=["card-with-header", "card", "card-interactive"],
    usage='''import Card, {
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
} from "./card-with-actions";

<Card>
  <CardHeader>
    <CardTitle>Weekly digest</CardTitle>
    <CardDescription>Every Monday at 9:00.</CardDescription>
    <CardAction>
      <button aria-label="Pin digest">…</button>
      <button aria-label="Digest settings">…</button>
    </CardAction>
  </CardHeader>
  <CardContent>…</CardContent>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, ACTION_PROPS, CONTENT_PROPS]),
    composition_note="`CardAction` is a plain flex slot at the top right of the header grid. The buttons inside it are ordinary DevSnips-style buttons — the Cards family deliberately does not ship its own button or menu implementation; compose the Buttons and Dropdowns families here.",
    logic_doc="""Header actions operate on the card's subject (pin this digest, configure these alerts), which is why they live in the header next to the title rather than in the footer with the primary flow.

Each demo button is a real `<button type="button">` with an `aria-label` (icon-only buttons have no visible text). The note under the card reports the last activated action, proving the controls are wired — nothing here is decorative.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC + """
- Icon-only buttons announce through their `aria-label` (`"Pin digest"`, `"Digest settings"`, …), never through the icon itself — icons are `aria-hidden`.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Keep header actions to one or two compact controls; a full menu belongs in a DropdownMenu trigger placed in the same slot, and the primary flow belongs in `CardFooter`.",
    tsx_header='''/**
 * DevSnips React Card — Contextual actions.
 *
 * The shared card core; this variant demonstrates the `CardAction` header
 * slot: real icon buttons (pin / settings / more) with accessible names,
 * composed from the shared button recipe — Cards deliberately does not
 * re-implement the Buttons or Dropdowns families.
 */''',
    showcase=DEMO_HELPERS + '''
function DigestCard() {
  const [pinned, setPinned] = React.useState(false);
  const [last, setLast] = React.useState("No actions yet.");
  return (
    <div className="space-y-2">
      <Card className="max-w-sm">
        <CardHeader>
          <CardTitle>Weekly digest</CardTitle>
          <CardDescription>Deploy and usage summary, every Monday at 9:00.</CardDescription>
          <CardAction>
            <button
              type="button"
              className={ICON_BTN}
              aria-label={pinned ? "Unpin digest" : "Pin digest"}
              aria-pressed={pinned}
              onClick={() => { setPinned(!pinned); setLast(pinned ? "Digest unpinned." : "Digest pinned."); }}
            >
              <Icon name="pin" className="size-4" />
            </button>
            <button
              type="button"
              className={ICON_BTN}
              aria-label="Digest settings"
              onClick={() => setLast("Digest settings opened.")}
            >
              <Icon name="settings" className="size-4" />
            </button>
            <button
              type="button"
              className={ICON_BTN}
              aria-label="More digest actions"
              onClick={() => setLast("More-actions menu would open here (compose DropdownMenu).")}
            >
              <Icon name="more" className="size-4" />
            </button>
          </CardAction>
        </CardHeader>
        <CardContent>
          <p className="m-0 text-sm leading-5 text-[var(--ds-color-foreground)]">
            Sent to 6 members of the platform team. Includes failed deploys and
            bandwidth anomalies.
          </p>
        </CardContent>
      </Card>
      <p className={NOTE} aria-live="polite">{last}{pinned ? " Pin is toggled on." : ""}</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Header action slot — pin is a real toggle</p>
        <DigestCard />
      </div>
    </div>
  );
}''',
)

# 5. card-with-icon
register(
    "card-with-icon",
    title="Card with Icon",
    subcategory="Content",
    description="Icon-led content cards: a restrained icon chip establishes hierarchy without dominating the card. Icons are inline SVG, `aria-hidden`, and carry meaning — the title still does the talking.",
    tags=TAGS_BASE + ["icon", "hierarchy", "content"],
    features=FEAT_BASE + ["icon chip", "aria-hidden icons", "three-up responsive grid"],
    accessibility=["icons are aria-hidden decoration beside real headings", "meaning carried by text, not color or icon alone"],
    interactive=False,
    related=["card", "card-stat", "card-list"],
    usage='''import Card, {
  CardContent,
  CardTitle,
  CardDescription,
} from "./card-with-icon";

<Card>
  <CardContent className="flex flex-col gap-3">
    <span aria-hidden="true" className="icon-chip">{/* svg */}</span>
    <CardTitle>API reference</CardTitle>
    <CardDescription>Endpoints, scopes, and error codes.</CardDescription>
  </CardContent>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, CONTENT_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="The icon chip is plain composition, not a new primitive: a 40px rounded `surface-subtle` square holding an inline SVG, stacked above `CardTitle` + `CardDescription` inside `CardContent`.",
    logic_doc="""The icon establishes the category (docs, storage, integrations) so a grid of cards scans quickly — but hierarchy still comes from the heading, and the icon never replaces a label.

Icons come from the shared inline-SVG set used across the React library (stroke-based, `currentColor`, `aria-hidden`). No emoji, no icon fonts, no decorative overload: one icon per card.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC + """
- Every icon is wrapped `aria-hidden="true"`; the adjacent `CardTitle` heading carries the accessible name of the card's subject.""",
    responsive_doc="The three-up grid collapses to one column below `sm` and the icon chip keeps its fixed 40px size at every width. " + RESPONSIVE_BASE,
    notes_doc="If the icon is the only thing distinguishing otherwise identical cards, prefer clearer titles instead of more icons.",
    tsx_header='''/**
 * DevSnips React Card — Icon-led content.
 *
 * The shared card core; this variant demonstrates the icon-chip pattern: a
 * restrained 40px `surface-subtle` square with an inline `aria-hidden` SVG
 * stacked above `CardTitle` + `CardDescription`. The icon establishes
 * category hierarchy without dominating the card.
 */''',
    showcase=DEMO_HELPERS + '''
const ICON_CHIP = "flex size-10 items-center justify-center rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] text-[var(--ds-color-foreground)]";

function IconCard({ icon, title, children }) {
  return (
    <Card>
      <CardContent className="flex flex-col gap-3 py-5">
        <span aria-hidden="true" className={ICON_CHIP}>
          <Icon name={icon} className="size-5" />
        </span>
        <div className="space-y-1">
          <CardTitle>{title}</CardTitle>
          <CardDescription>{children}</CardDescription>
        </div>
      </CardContent>
    </Card>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Icon-led cards in a responsive grid</p>
        <div className="grid gap-4 sm:grid-cols-3">
          <IconCard icon="book" title="API reference">
            Endpoints, scopes, rate limits, and error codes for the REST API.
          </IconCard>
          <IconCard icon="layers" title="Storage">
            Object storage with versioned buckets and lifecycle rules.
          </IconCard>
          <IconCard icon="grid" title="Integrations">
            Connect issue trackers, chat, and CI providers to the workspace.
          </IconCard>
        </div>
        <p className={NOTE}>One meaningful icon per card; the heading still carries the name.</p>
      </div>
    </div>
  );
}''',
)

# 6. card-with-image
register(
    "card-with-image",
    title="Card with Image",
    subcategory="Content",
    description="Image-led cards with `CardMedia`: a real `<img>` cropped into a 16:9 (or square) frame with `object-cover`, meaningful `alt` text, lazy loading, and a graceful decorative placeholder when no image is available.",
    tags=TAGS_BASE + ["image", "media", "object-cover", "alt-text"],
    features=FEAT_BASE + ["16:9 and square crop boxes", "object-cover cropping", "missing-image placeholder", "lazy loading"],
    accessibility=["meaningful alt text on content images", "decorative placeholder is aria-hidden", "no layout collapse without an image"],
    interactive=False,
    related=["card", "card-horizontal", "card-list"],
    usage='''import Card, {
  CardMedia,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "./card-with-image";

<Card>
  <CardMedia src="/covers/guide.svg" alt="Cover art for the observability guide" />
  <CardHeader>
    <CardTitle>Observability field guide</CardTitle>
    <CardDescription>Dashboards, alerts, and SLOs.</CardDescription>
  </CardHeader>
  <CardFooter className="sm:justify-between">
    <p>24 min read</p>
    <button>Save</button>
  </CardFooter>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, MEDIA_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, FOOTER_PROPS]),
    composition_note="`CardMedia` renders first inside the card and draws its own crop box: `aspect-video` (default) or `aspect-square`, with the image filling the frame via `object-cover`. Rounded top corners match the card radius.",
    logic_doc="""The media frame owns the aspect ratio, so images of any natural size crop predictably without stretching or breaking the layout. `loading="lazy"` is on by default.

When `src` is omitted the frame keeps its geometry and renders a decorative, `aria-hidden` placeholder (second demo) — the card never collapses and assistive technology is not bothered with a broken image. Alt text defaults to `""` (decorative); pass real alt text whenever the image carries meaning, as the first demo does. The preview artwork is generated inline as a data URI — no external image that could disappear.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC + """
- Content images carry meaningful `alt` text; the missing-image placeholder and purely decorative artwork use `alt=""` / `aria-hidden`.""",
    responsive_doc="The media frame is full-width with a fixed aspect ratio, so the image scales with the card at every viewport and `object-cover` crops instead of distorting. " + RESPONSIVE_BASE,
    notes_doc="For side-by-side media (left column on desktop, top banner on mobile) see `card-horizontal`, which uses `aspect=\"none\"` plus a fixed column width.",
    tsx_header='''/**
 * DevSnips React Card — Image-led composition.
 *
 * The shared card core; this variant demonstrates `CardMedia`: a real
 * `<img>` cropped into an aspect-ratio frame with `object-cover`, semantic
 * `alt` handling (`""` decorative by default), `loading="lazy"`, and a
 * graceful `aria-hidden` placeholder when no image is available.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Image + header + footer</p>
        <Card className="max-w-sm">
          <CardMedia
            src={demoImage("#E5E5E5", "#737373")}
            alt="Abstract gray placeholder artwork for the observability guide cover"
          />
          <CardHeader>
            <CardTitle>Observability field guide</CardTitle>
            <CardDescription>Dashboards, alerts, and SLOs for on-call teams.</CardDescription>
          </CardHeader>
          <CardFooter className="sm:justify-between">
            <p className={META}>24 min read · Engineering</p>
            <button type="button" className={BTN_OUTLINE}>Save for later</button>
          </CardFooter>
        </Card>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Missing image — geometry holds</p>
        <Card className="max-w-sm">
          <CardMedia />
          <CardHeader>
            <CardTitle>Untitled draft</CardTitle>
            <CardDescription>No cover image uploaded yet — the layout does not collapse.</CardDescription>
          </CardHeader>
          <CardFooter className="sm:justify-between">
            <p className={META}>Edited 3 days ago</p>
            <button type="button" className={BTN_OUTLINE}>Add cover</button>
          </CardFooter>
        </Card>
        <p className={NOTE}>The placeholder is decorative (aria-hidden); real images carry real alt text.</p>
      </div>
    </div>
  );
}''',
)
# 7. card-horizontal
register(
    "card-horizontal",
    title="Horizontal Card",
    subcategory="Layout",
    description="A responsive horizontal card: media in a fixed left column with content beside it from `sm` up, collapsing to a top banner + stacked content below `sm`. Uses `CardMedia aspect=\"none\"` with showcase-level layout classes.",
    tags=TAGS_BASE + ["horizontal", "media", "layout"],
    features=FEAT_BASE + ["fixed-width media column", "vertical collapse below sm", "no overflow at 375/768/1280"],
    accessibility=["image alt text as with CardMedia", "reading order preserved when stacked"],
    interactive=False,
    related=["card-with-image", "card", "card-list"],
    usage='''import Card, {
  CardMedia,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "./card-horizontal";

<Card className="overflow-hidden sm:flex-row">
  <CardMedia aspect="none" className="h-40 sm:h-auto sm:w-48" src="/cover.svg" alt="Report cover" />
  <div className="flex min-w-0 flex-1 flex-col">
    <CardHeader>
      <CardTitle>Q2 market insights</CardTitle>
      <CardDescription>Quarterly analysis for the pricing team.</CardDescription>
    </CardHeader>
    <CardFooter className="sm:justify-between">
      <p>Report · 14 pages</p>
      <button>Open report</button>
    </CardFooter>
  </div>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, MEDIA_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, FOOTER_PROPS]),
    composition_note="Horizontal arrangement is layout, not a new primitive: the card root gets `className=\"overflow-hidden sm:flex-row\"`, the media frame gets `aspect=\"none\"` plus a fixed column width (`h-40 sm:h-auto sm:w-48`), and a flex-column wrapper holds the header/footer regions.",
    logic_doc="""The card is `flex-col` by default; adding `sm:flex-row` places the media frame and the text wrapper side by side from the `sm` breakpoint up. `aspect="none"` removes the ratio box so the frame can be a full-height column (`sm:h-auto sm:w-48`).

Below `sm` the media renders as a fixed-height banner (`h-40`) across the top and the regions stack — content is never clipped or hidden to make space. The card's `overflow-hidden` clips the media corners to the card radius in both arrangements.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC + """
- Document order is media, then header/footer regions; when the layout collapses at 375px the image still precedes the text, so reading order stays intact.""",
    responsive_doc="Below `sm` (640px) the media is a `h-40` banner and the regions stack full-width; from `sm` up it becomes a 192px column and the text column flexes. Verified against overflow at 375 / 768 / 1280px.",
    notes_doc="The `overflow-hidden` on the card root clips the media flush to the card border, so the frame needs no per-placement corner overrides.",
    tsx_header='''/**
 * DevSnips React Card — Horizontal media layout.
 *
 * The shared card core; this variant demonstrates the horizontal pattern:
 * the root gets `overflow-hidden sm:flex-row`, the media frame gets
 * `aspect="none"` + `h-40 sm:h-auto sm:w-48`, and the header/footer
 * regions stack in a flex column beside it — collapsing to a top banner
 * below `sm` without clipping content.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Media column + stacked regions</p>
        <Card className="overflow-hidden sm:flex-row">
          <CardMedia
            aspect="none"
            className="h-40 sm:h-auto sm:w-48"
            src={demoImage("#FAFAFA", "#A3A3A3")}
            alt="Cover art for the Q2 market insights report"
          />
          <div className="flex min-w-0 flex-1 flex-col">
            <CardHeader>
              <CardTitle>Q2 market insights</CardTitle>
              <CardDescription>Quarterly analysis for the pricing team.</CardDescription>
            </CardHeader>
            <CardFooter className="sm:justify-between">
              <p className={META}>Report · 14 pages</p>
              <button type="button" className={BTN_OUTLINE}>Open report</button>
            </CardFooter>
          </div>
        </Card>
        <p className={NOTE}>Resize: the media column collapses to a top banner below 640px; content never clips.</p>
      </div>
    </div>
  );
}''',
)

# 8. card-selectable
register(
    "card-selectable",
    title="Selectable Card",
    subcategory="Selection",
    description="Real selection semantics, not a clickable `<div>`: `SelectableCard` wraps a native radio or checkbox input whose whole card is the `<label>`, and `SelectableCardGroup` manages the single choice inside a `<fieldset>`/`legend`. Controlled and uncontrolled modes both supported.",
    tags=TAGS_BASE + ["selectable", "radio", "checkbox", "fieldset", "keyboard"],
    features=FEAT_BASE + ["native input semantics", "label-as-card", "single + multi select", "group tracking", "arrow-key radio nav"],
    accessibility=["native <input type=radio/checkbox>", "visible label is the accessible name", "selected border + control, not color alone", "aria-describedby description", "native disabled"],
    interactive=True,
    related=["card", "card-interactive", "card-list"],
    usage='''import Card, { SelectableCard, SelectableCardGroup } from "./card-selectable";

// Single choice (recommended — the group keeps state in sync):
<SelectableCardGroup
  legend="Choose a plan"
  columns={3}
  options={[
    { value: "starter", label: "Starter" },
    { value: "team", label: "Team" },
    { value: "enterprise", label: "Enterprise" },
  ]}
/>

// Independent multi-select:
<SelectableCard label="Usage alerts" description="Notify at 80% of limits." />''',
    props_doc="\n\n".join([SELECTABLE_PROPS, GROUP_PROPS]),
    composition_note="`SelectableCard` is self-contained: its `<label htmlFor>` wraps the input, the visible label, the description, and the tracked indicator. For single choice prefer `SelectableCardGroup`, which renders one `SelectableCard` per option inside a `<fieldset>` and owns the value.",
    logic_doc="""Each selectable card's entire surface is the `<label htmlFor>` of its input, so clicking anywhere toggles the control — and the input's own change handler keeps the tracked React state (border + indicator) in sync in both controlled (`checked` + `onChange`) and uncontrolled (`defaultChecked`) modes.

`SelectableCardGroup` is a `<fieldset>` of `type="radio"` cards. It owns the selected value and passes `checked` down to each option — the same recipe the Radio family uses — because a deselected radio receives no change event of its own; the group re-derives every option's state. `defaultValue` keeps uncontrolled mode working while `onChange` reports every new selection (shown in the live note). Checkbox semantics (`type="checkbox"`) are for independent multi-select; radio semantics (`type="radio"`) are for single choice within the same `name`.""",
    keyboard_doc="""| Key | Behavior |
|---|---|
| `Tab` | Move into / between selectable cards (native input focus order) |
| `Space` | Toggle the focused radio / checkbox card |
| `Arrow keys` (radio group) | Move selection within the group (native browser behavior) |
| Click on the card | Toggles — the whole card is the `<label htmlFor>` |

Each input exposes a real `focus-visible` outline via the `color.focus-ring` token; disabled options are skipped by Tab and cannot be activated.""",
    behavior_doc="""- **Idle** — bordered surface with the card shadow-xs; hover shifts to `surface-hover`.
- **Selected** — `--ds-color-primary` border plus the checked indicator (check glyph / radio dot) — border + control, never color alone.
- **Focus** — `focus-visible` 2px outline on the real input; `focus-within` strengthens the card border.
- **Disabled** — native `disabled` on the input: 60% opacity on the label, `cursor-not-allowed`, out of the tab order.""",
    a11y_doc="""- Selection semantics come from native `<input type="radio">` / `<input type="checkbox">` elements — no fake `role="button"`, no click-handlers on `<div>`s.
- The visible label text is the input's accessible name via `<label htmlFor>`; the description is wired with `aria-describedby` on the input.
- `SelectableCardGroup` is a real `<fieldset>` + `<legend>`, so screen readers announce the group context for each option.
- The selected state is border + visible control glyph; the tracked indicator div is `aria-hidden`.""",
    responsive_doc="The group's grid is single-column below `sm` and uses the `columns` count from `sm` up; labels and descriptions wrap instead of overflowing. " + RESPONSIVE_BASE,
    notes_doc="For multi-select checkboxes use ≤ a few cards or consider the Checkboxes family; `SelectableCard` reuses that control recipe at card scale.",
    tsx_header='''/**
 * DevSnips React Card — Selectable surfaces.
 *
 * The shared card core with its two selection primitives: `SelectableCard`
 * wraps a native `<input type="radio">` / `type="checkbox">` (the whole card
 * is its `<label htmlFor>`), and `SelectableCardGroup` manages single choice
 * inside a `<fieldset>`/`legend`. Selected state is tracked from controlled
 * or uncontrolled state and shown as border + control — never color alone.
 */''',
    showcase=DEMO_HELPERS + '''
function PlanPicker() {
  const [plan, setPlan] = React.useState("team");
  return (
    <div className="space-y-3">
      <SelectableCardGroup
        legend="Choose a plan"
        columns={3}
        defaultValue="team"
        onChange={(value) => setPlan(value)}
        options={[
          { value: "starter", label: "Starter", description: "1 member, 3 projects. Free." },
          { value: "team", label: "Team", description: "Unlimited projects. $20 per member." },
          { value: "enterprise", label: "Enterprise", description: "SSO, audit logs, SLA." },
        ]}
      />
      <p className={NOTE} aria-live="polite">Selected plan: {plan}</p>
    </div>
  );
}

function TargetEnv() {
  const [env, setEnv] = React.useState("production");
  const select = (next) => () => setEnv(next);
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <SelectableCard type="radio" name="target-env" label="Production" description="Live traffic on this deploy." checked={env === "production"} onChange={select("production")} />
      <SelectableCard type="radio" name="target-env" label="Preview" description="Share a staging URL first." checked={env === "preview"} onChange={select("preview")} />
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Single choice — SelectableCardGroup (radio semantics)</p>
        <PlanPicker />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Independent choices — checkbox semantics</p>
        <div className="grid gap-3 sm:grid-cols-3">
          <SelectableCard label="Email digests" description="Weekly summary of deploys." defaultChecked />
          <SelectableCard label="Usage alerts" description="Notify at 80% of limits." />
          <SelectableCard label="Audit log exports" description="Requires the enterprise plan." disabled />
        </div>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Controlled pair — parent owns the value</p>
        <TargetEnv />
      </div>
    </div>
  );
}''',
)

# 9. card-interactive
register(
    "card-interactive",
    title="Interactive Card",
    subcategory="Interaction",
    description="A card that is itself the interactive element — without the fake-`<div>` anti-pattern. With `href` it renders a real anchor (navigation); without `href` it renders a real `<button type=\"button\">` (actions). Discriminated-union typing keeps the two modes apart.",
    tags=TAGS_BASE + ["interactive", "anchor", "button", "navigation", "keyboard"],
    features=FEAT_BASE + ["real <a> navigation mode", "real <button> action mode", "hover/active surface feedback", "disabled button mode"],
    accessibility=["real anchor for navigation", "real button for actions", "no nested interactive elements", "focus-visible ring"],
    interactive=True,
    related=["card-selectable", "card-with-actions", "card"],
    usage='''import Card, {
  InteractiveCard,
  CardContent,
} from "./card-interactive";

// Navigation — renders a real <a>:
<InteractiveCard href="/docs">
  <CardContent>Browse the documentation</CardContent>
</InteractiveCard>

// Action — renders a real <button type="button">:
<InteractiveCard onClick={startExport} disabled={busy}>
  <CardContent>Export usage report</CardContent>
</InteractiveCard>''',
    props_doc=INTERACTIVE_PROPS,
    composition_note="`InteractiveCard` replaces the `Card` root for one-of-one-control cards: its children are still the normal region primitives (`CardHeader`, `CardContent`), but the surface is a single anchor/button instead of a `<div>`.",
    logic_doc="""The anchor branch is the navigation pattern: middle-click, open-in-new-tab, copy-link, and screen-reader link semantics all work, and the demo below tracks the live hash — the same hash-navigation trick the Breadcrumbs/Pagination previews use.

The button branch is the action pattern: it activates on Enter and Space, carries the only meaningful `disabled` state (anchors cannot be disabled natively — the prop simply does not exist on the anchor branch, enforced by the typed union).

Because the whole card is one control, other interactive elements must not be nested inside it — that produces invalid, confusing activation. Secondary actions belong on a sibling `Card` (e.g. in a `CardAction` slot), never inside an `InteractiveCard`.""",
    keyboard_doc="""| Key | Behavior |
|---|---|
| `Tab` | Reach the card control (one tab stop per card) |
| `Enter` | Follow the link (anchor mode) or activate the button (button mode) |
| `Space` | Activate the button (button mode) |

Anchor-mode cards are followed with Enter like any link; button-mode cards use the native button activation set. Disabled button cards are skipped by Tab.""",
    behavior_doc="""- **Idle** — bordered surface (shadow-xs) exactly like a plain card.
- **Hover** — border strengthens and the surface shifts (`surface-hover`); the whole card signals it is one target.
- **Active** — `surface-active` press feedback (colors only, no transform).
- **Focus-visible** — 2px `color.focus-ring` outline, offset 2px, around the whole card.
- **Disabled (button mode)** — native `disabled`: 50% opacity, `pointer-events-none`, out of the tab order.""",
    a11y_doc="""- The card is one real control — `<a href>` for navigation, `<button type="button">` for actions — never a `<div>` with a click handler.
- Screen readers announce a link or a button with its text content as the accessible name; icons inside are `aria-hidden`.
- No nested interactive elements inside the card; only such a structure produces one clean activation.
- `disabled` exists only on the button branch (anchors have no native disabled state) and is exposed by the native attribute.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="If you need more than one action per card, use a plain `Card` with `CardAction`/`CardFooter` instead of stretching `InteractiveCard` into a multi-control container.",
    tsx_header='''/**
 * DevSnips React Card — Whole-card interaction.
 *
 * The shared card core with its `InteractiveCard` primitive: the surface is
 * a real `<a href>` (navigation) or a real `<button type="button">`
 * (actions) — never a `<div>` with a click handler. A typed discriminated
 * union keeps the two branches honest; `disabled` exists only on the button
 * branch, and nested interactive elements are explicitly avoided.
 */''',
    showcase=DEMO_HELPERS + '''
const NAV_CARDS = [
  { title: "Documentation", desc: "Guides, API reference, and examples.", href: "#/docs", icon: "book" },
  { title: "API tokens", desc: "Create and revoke access tokens.", href: "#/settings/tokens", icon: "settings" },
];

function NavigationDemo() {
  const [hash, setHash] = React.useState(window.location.hash || "(no hash yet)");
  React.useEffect(() => {
    const on = () => setHash(window.location.hash || "(no hash yet)");
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return (
    <div className="space-y-2">
      <div className="grid gap-4 sm:grid-cols-2">
        {NAV_CARDS.map((item) => (
          <InteractiveCard key={item.href} href={item.href}>
            <CardContent className="flex items-center justify-between gap-4 py-5">
              <div className="min-w-0">
                <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">{item.title}</p>
                <p className="m-0 mt-1 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">{item.desc}</p>
              </div>
              <Icon name="arrow-right" className="size-4 shrink-0 text-[var(--ds-color-muted-foreground)]" />
            </CardContent>
          </InteractiveCard>
        ))}
      </div>
      <p className={NOTE}>Anchor mode — current hash: {hash}</p>
    </div>
  );
}

function ActionDemo() {
  const [last, setLast] = React.useState("Nothing exported yet.");
  return (
    <div className="space-y-2">
      <div className="grid gap-4 sm:grid-cols-2">
        <InteractiveCard onClick={() => setLast("Exported usage-report.csv.")}>
          <CardContent className="flex items-center gap-3 py-5">
            <Icon name="download" className="size-5 shrink-0 text-[var(--ds-color-foreground)]" />
            <div className="min-w-0">
              <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">Export usage report</p>
              <p className="m-0 mt-1 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">CSV for the current billing period.</p>
            </div>
          </CardContent>
        </InteractiveCard>
        <InteractiveCard disabled>
          <CardContent className="flex items-center gap-3 py-5">
            <Icon name="download" className="size-5 shrink-0 text-[var(--ds-color-foreground)]" />
            <div className="min-w-0">
              <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">Export audit log</p>
              <p className="m-0 mt-1 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">Requires the enterprise plan.</p>
            </div>
          </CardContent>
        </InteractiveCard>
      </div>
      <p className={NOTE} aria-live="polite">Button mode — {last}</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Navigation — anchor mode</p>
        <NavigationDemo />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Action — button mode</p>
        <ActionDemo />
      </div>
    </div>
  );
}''',
)

# 10. card-stat
register(
    "card-stat",
    title="Stat Card",
    subcategory="Content",
    description="Compact metric presentation: an uppercase muted label, a large tabular-numeral value, and a semantic trend (icon + text, success/quiet tokens — never color alone). Plain composition of the card primitives — no fake chart components.",
    tags=TAGS_BASE + ["stat", "metric", "kpi", "trend"],
    features=FEAT_BASE + ["tabular numerals", "semantic trend colors", "muted label", "icon + text trend"],
    accessibility=["label/value trend readable as text", "icon and color supplementary, text carries the delta"],
    interactive=False,
    related=["card-with-icon", "card", "card-list"],
    usage='''import Card, { CardContent } from "./card-stat";

<Card>
  <CardContent className="flex flex-col gap-1.5 py-5">
    <p className="label">Monthly recurring revenue</p>
    <p className="value">$48,290</p>
    <p className="trend">+12.4% vs last month</p>
  </CardContent>
</Card>''',
    props_doc="\n\n".join([BASE_PROPS, CONTENT_PROPS]),
    composition_note="A stat card is composition, not a new export: `Card` + `CardContent` with a muted label, a large `tabular-nums` value, and a trend line. The pattern is small enough to keep out of the component API.",
    logic_doc="""The label is uppercase muted text, the value is 24px semibold with `tabular-nums` so figures align in dashboards, and the trend line pairs a 14px direction icon with a text delta plus a baseline ("vs last month").

The demos show the three common cases — up (revenue, users), down-as-good (fewer tickets), and the neutral reading — using the `success` token for positive movement and muted text for the neutral frame. A real product can map movement direction to its own semantics the same way. No decorative sparklines or fake charts: the point of the variant is the reusable metric structure.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc="""- **Label** — uppercase, muted, 12px: category of the metric.
- **Value** — 24px semibold with `tabular-nums` on the foreground color.
- **Trend** — direction icon + delta text in the `success` token for favorable movement; muted text for the baseline. Color is always paired with text.""",
    a11y_doc=A11Y_STATIC + """
- The trend line is text ('+12.4% vs last month') — the arrow icon is decorative and `aria-hidden`; movement is never conveyed by color or icon alone.""",
    responsive_doc="The three-up grid collapses to one column below `sm`; values keep `tabular-nums` alignment; long labels wrap. " + RESPONSIVE_BASE,
    notes_doc="Keep stat cards to four-or-fewer per row so each metric stays readable — a row of equal-width metric cards is the intended composition.",
    tsx_header='''/**
 * DevSnips React Card — Stat (metric) composition.
 *
 * The shared card core; this variant demonstrates the metric pattern:
 * uppercase muted label, large `tabular-nums` value, and a semantic trend
 * (icon + text in the `success` token — movement is never color alone).
 */''',
    showcase=DEMO_HELPERS + '''
function StatCard({ label, value, delta, down }) {
  return (
    <Card>
      <CardContent className="flex flex-col gap-1.5 py-5">
        <p className={STAT_LABEL}>{label}</p>
        <p className={STAT_VALUE}>{value}</p>
        <p className="m-0 flex flex-wrap items-center gap-1.5 text-xs leading-4">
          <Icon
            name={down ? "trending-down" : "trending-up"}
            className="size-3.5 text-[var(--ds-color-success)]"
          />
          <span className="font-medium text-[var(--ds-color-success)]">{delta}</span>
          <span className="text-[var(--ds-color-muted-foreground)]">vs last month</span>
        </p>
      </CardContent>
    </Card>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Metrics row — three-up grid</p>
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard label="Monthly recurring revenue" value="$48,290" delta="+12.4%" />
          <StatCard label="Active users" value="8,431" delta="+3.1%" />
          <StatCard label="Support tickets" value="96" delta="-18.2%" down />
        </div>
        <p className={NOTE}>Fewer open tickets is a favorable down trend — the delta is text, not color alone.</p>
      </div>
    </div>
  );
}''',
)

# 11. card-loading
register(
    "card-loading",
    title="Loading Card",
    subcategory="Feedback",
    description="`CardSkeleton` placeholders that match the real card's geometry so content swaps in without layout shift: an accessible busy surface (`aria-busy` + visually hidden label) with a restrained, reduced-motion-safe pulse.",
    tags=TAGS_BASE + ["loading", "skeleton", "busy", "aria-busy"],
    features=FEAT_BASE + ["geometry-matched placeholder", "aria-busy surface", "reduced-motion pulse off", "media/lines/footer options"],
    accessibility=["aria-busy=true", "visually hidden live label", "placeholder blocks aria-hidden", "reduced-motion: no pulse"],
    interactive=True,
    related=["card", "card-list", "card-with-image"],
    usage='''import Card, { CardSkeleton } from "./card-loading";

{loading ? (
  <CardSkeleton lines={2} footer label="Loading report…" />
) : (
  <Card>…real content…</Card>
)}''',
    props_doc=SKELETON_PROPS,
    composition_note="`CardSkeleton` renders a `Card` root with `aria-busy=\"true\"` — options (`media`, `lines`, `footer`) shape the placeholder to the card it stands in for, so swapping is a clean geometry match.",
    logic_doc="""Each placeholder block is a restrained gray shape on an `animate-pulse` opacity loop, matched to the real region sizes (title-ish bar, text lines, 36px button slots, 16:9 media frame). Toggle the demo's Reload button: the skeleton holds the layout while the (simulated) fetch runs, then the real card swaps in with no shift.

Under `prefers-reduced-motion` the pulse is disabled (`motion-reduce:animate-none`) — the static shapes still communicate loading. The label is visually hidden so the busy state announces without a visible banner, and the blocks are `aria-hidden` like any decorative progress.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc="""- **Busy surface** — normal card styling + `aria-busy="true"`; quiet, static gray placeholder blocks.
- **Pulse** — opacity loop only; layout never shifts; disabled under `prefers-reduced-motion`.
- **Options** — `media` adds a 16:9 frame, `lines` sets body line count (min 1), `footer` adds an action row, `label` customizes the hidden announcement.""",
    a11y_doc="""- `aria-busy="true"` marks the surface during loading; a visually hidden `span` (e.g. "Loading report…") announces the state when visible text would be noise.
- Placeholder blocks are wrapped `aria-hidden="true"` so they read as nothing, not garbage.
- The toggle demo announces through an `aria-live` note next to the Reload button.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Match the skeleton to the destination card's shape (`media` for image cards, `footer` for action cards) — the swap-in reads as instant and stable.",
    tsx_header='''/**
 * DevSnips React Card — Skeleton loading.
 *
 * The shared card core with its `CardSkeleton` primitive: placeholder blocks
 * matched to the real regions (media / lines / footer), `aria-busy="true"`
 * with a visually hidden label, and an opacity pulse disabled under
 * `prefers-reduced-motion` — loading without layout shift.
 */''',
    showcase=DEMO_HELPERS + '''
function ReportLoader() {
  const [loading, setLoading] = React.useState(true);
  React.useEffect(() => {
    const t = setTimeout(() => setLoading(false), 1600);
    return () => clearTimeout(t);
  }, []);
  function reload() {
    setLoading(true);
    setTimeout(() => setLoading(false), 1600);
  }
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <div className="max-w-sm space-y-3">
        {loading ? (
          <CardSkeleton lines={2} footer label="Loading report…" />
        ) : (
          <Card>
            <CardHeader>
              <CardTitle>March usage report</CardTitle>
              <CardDescription>Bandwidth and builds across 4 projects.</CardDescription>
            </CardHeader>
            <CardFooter className="sm:justify-between">
              <p className={META}>Generated Apr 1</p>
              <button type="button" className={BTN_OUTLINE}>Open report</button>
            </CardFooter>
          </Card>
        )}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <p className={NOTE} aria-live="polite">
            {loading ? "Loading report…" : "Loaded — the swap has no layout shift."}
          </p>
          <button type="button" className={BTN_OUTLINE} onClick={reload}>Reload</button>
        </div>
      </div>
      <div className="max-w-sm">
        <Card>
          <CardHeader>
            <CardTitle>February usage report</CardTitle>
            <CardDescription>Bandwidth and builds across 4 projects.</CardDescription>
          </CardHeader>
          <CardFooter className="sm:justify-between">
            <p className={META}>Generated Mar 1</p>
            <button type="button" className={BTN_OUTLINE}>Open report</button>
          </CardFooter>
        </Card>
        <p className={NOTE}>The stable reference card next to it keeps its footprint.</p>
      </div>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Loading → loaded (toggle with Reload)</p>
        <ReportLoader />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Media + plain skeleton shapes</p>
        <div className="grid gap-4 sm:grid-cols-2">
          <CardSkeleton media lines={2} />
          <CardSkeleton lines={3} />
        </div>
        <p className={NOTE}>Pulse is opacity-only; prefers-reduced-motion renders static shapes.</p>
      </div>
    </div>
  );
}''',
)

# 12. card-list
register(
    "card-list",
    title="Card List",
    subcategory="Layout",
    description="Repeated cards in a semantic list: a `<ul>`/`<li>` grid with consistent spacing that collapses responsively, one composed `Card` per item — the reusable component does the work, no new grid framework.",
    tags=TAGS_BASE + ["list", "grid", "collection", "ul/li semantics"],
    features=FEAT_BASE + ["ul/li semantics", "responsive columns", "consistent gaps", "per-item composed cards"],
    accessibility=["real list structure (ul/li)", "per-item real buttons with unique names", "section labelled by real h2"],
    interactive=True,
    related=["card", "card-with-icon", "card-selectable"],
    usage='''import Card, {
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "./card-list";

<ul className="grid gap-4 sm:grid-cols-2">
  {projects.map((p) => (
    <li key={p.id}>
      <Card>
        <CardHeader>
          <CardTitle>{p.name}</CardTitle>
          <CardDescription>{p.desc}</CardDescription>
        </CardHeader>
        <CardContent>{p.meta}</CardContent>
        <CardFooter className="sm:justify-between">
          <p>No incidents</p>
          <button aria-label={"Open " + p.name}>Open</button>
        </CardFooter>
      </Card>
    </li>
  ))}
</ul>''',
    props_doc="\n\n".join([BASE_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, CONTENT_PROPS, FOOTER_PROPS]),
    composition_note="Structure the collection yourself (a `section` with a heading, and a `<ul>` of `<li>` items), and let each item compose the shared card primitives. Grid classes (`grid sm:grid-cols-2 gap-4`) live in your layout, keeping Cards free of a grid framework.",
    logic_doc="""The demo renders four project cards from data — each a plain `Card` with header (+ a badge in the action slot when set), meta content, and a split footer. Everything repeats consistently because it maps a single composed card.

List semantics matter here: the `<ul>`/`<li>` wrapper tells assistive technology this is a collection and how many items it holds, and each item keeps its own footer action (with a unique accessible name per project).""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_STATIC + """
- The collection is a real `<ul>` of `<li>` items inside a `section` labelled by a real `<h2>` — screen readers announce list size and position.
- Footer actions have per-item accessible names (`aria-label="Open api-gateway"`), never four buttons all named "Open".""",
    responsive_doc="The grid is one column below `sm`, two columns from `sm` up, with footers aligned across equal-height tracks (`mt-auto`). " + RESPONSIVE_BASE,
    notes_doc="For dense text-only lists use the Table or list composition; this variant is for card content in a collection.",
    tsx_header='''/**
 * DevSnips React Card — List collection.
 *
 * The shared card core; this variant demonstrates the list pattern: a real
 * `<ul>`/`<li>` grid of composed cards (header + meta + footer) with
 * consistent gaps and per-item accessible actions — the reusable component,
 * not a new grid framework.
 */''',
    showcase=DEMO_HELPERS + '''
const PROJECTS = [
  { name: "api-gateway", desc: "Edge routing for production traffic.", meta: "TypeScript · Updated 2h ago", badge: "Production" },
  { name: "design-tokens", desc: "Semantic tokens and theming guides.", meta: "CSS · Updated 1 day ago", badge: null },
  { name: "billing-service", desc: "Usage metering and invoicing.", meta: "TypeScript · Updated 3 days ago", badge: null },
  { name: "docs-site", desc: "Public documentation and changelog.", meta: "Markdown · Updated 4h ago", badge: "Public" },
];

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-3">
        <p className={LABEL}>Projects collection — ul/li grid</p>
        <section aria-labelledby="projects-heading">
          <h2 id="projects-heading" className="m-0 text-base font-semibold leading-6 text-[var(--ds-color-foreground)]">
            Recent projects
          </h2>
          <ul className="m-0 mt-3 grid list-none gap-4 p-0 sm:grid-cols-2">
            {PROJECTS.map((p) => (
              <li key={p.name}>
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle>{p.name}</CardTitle>
                    <CardDescription>{p.desc}</CardDescription>
                    {p.badge ? (
                      <CardAction>
                        <span className={CHIP}>{p.badge}</span>
                      </CardAction>
                    ) : null}
                  </CardHeader>
                  <CardContent>
                    <p className={META}>{p.meta}</p>
                  </CardContent>
                  <CardFooter className="sm:justify-between">
                    <p className={META}>No incidents</p>
                    <button type="button" className={BTN_OUTLINE} aria-label={"Open " + p.name}>
                      Open
                    </button>
                  </CardFooter>
                </Card>
              </li>
            ))}
          </ul>
        </section>
        <p className={NOTE}>Real list semantics: screen readers announce 4 items.</p>
      </div>
    </div>
  );
}''',
)
