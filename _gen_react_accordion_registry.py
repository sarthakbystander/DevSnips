"""Registry for the DevSnips React Accordion generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference ``accordion/code.tsx``).
The generator (``_gen_react_accordion.py``) combines these with the reference
``code.tsx`` on disk to write ``code.tsx`` (derived), ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented demo content only (deploys, environments, API
keys, webhooks, databases, billing). No lorem ipsum, no marketing buzzwords,
no emoji.
"""
from _gen_react_accordion import (
    register,
    ACCORDION_PROPS, ITEM_PROPS, TRIGGER_PROPS, CONTENT_PROPS, props_table,
)

TAGS_BASE = ["accordion", "disclosure", "react", "tailwind", "accessible", "responsive", "tokens"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "WAI-ARIA disclosure", "token-driven surface"]

# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = r"""const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const BTN_PRIMARY_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_OUTLINE_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_GHOST_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-transparent px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,currentColor_8%,transparent)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_DESTRUCTIVE_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-destructive)] px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-destructive-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-destructive)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const LINK = "font-medium text-[var(--ds-color-link)] underline underline-offset-2 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
"""

KEYBOARD_BASE = """Accordion triggers are real `<button type="button">` elements, so the keyboard model is the native button model: Tab moves focus through the triggers and through any interactive elements inside open regions, and Enter or Space toggles the focused item. Disabled triggers are natively `disabled`, so Tab skips them entirely and they cannot be activated by pointer or keyboard.

Arrow-key navigation and roving tabindex are deliberately NOT implemented: the WAI-ARIA accordion pattern marks them as optional, and triggers that behave like ordinary buttons keep Tab order predictable — every focusable element stays exactly one Tab stop."""

A11Y_BASE = """- Every trigger is a real `<button type="button">` with `aria-expanded` and `aria-controls` referencing its region's stable id; the region is `role="region"` with `aria-labelledby` pointing back at the trigger. Both ids derive from the accordion instance's `useId` base plus the item's `value`, so multiple accordions (including nested ones) never collide.
- The trigger sits inside an `<h3>` heading, so the accordion participates in the page outline.
- The leading `icon` and the trailing chevron are `aria-hidden="true"` — state is exposed by `aria-expanded`, never by the glyph. The `badge` pill is plain text inside the button and joins the accessible name; keep it short and meaningful (for example `"3 errors"`, not a bare `"!"`).
- The closed region uses the CSS `visibility` transition: while closed it is `visibility: hidden`, which removes it from the accessibility tree AND the tab order — collapsed content can never be announced or focused.
- Disabled items use the native `disabled` attribute: the state is exposed to assistive technology and the trigger leaves the tab order. No redundant `aria-disabled`."""

RESPONSIVE_BASE = """The accordion is fluid-width (`w-full min-w-0`) and fills its container at every viewport. Trigger titles and descriptions wrap (`break-words`), the text column is `flex-1 min-w-0`, and the icon, badge, and chevron are `shrink-0` so they never push text off-screen. Region content wraps and long words break. No horizontal overflow at 375 / 768 / 1280px."""

STATES_BASE = """- **Trigger (idle)** — `color.foreground` title, `color.muted-foreground` icon/chevron; hover applies a `color.surface-hover` wash; keyboard focus shows a 2px `color.focus-ring` outline drawn inset (`-outline-offset-2`) so it is never clipped by bordered containers.
- **Trigger (open)** — the chevron rotates 180° over 200ms (`motion-reduce` makes the flip instant); `aria-expanded` flips with it. The state is also visible in the open region below, never carried by color alone.
- **Trigger (disabled)** — native `disabled`: 50% opacity, no pointer events, removed from the tab order.
- **Region** — height animates with the CSS grid-rows trick (`0fr` ↔ `1fr`, 200ms, `ease-out`), and a discrete `visibility` transition hides closed content from the accessibility tree and tab order once the collapse completes. Under `prefers-reduced-motion` every transition is removed and state changes are instant.
- **Region content** — body-sm on `color.muted-foreground`; mounted in both states so component state inside a region survives a close/reopen cycle."""

NOTES_TOKENS = "Every visual value comes from the `--ds-*` semantic tokens; light and dark themes flip through the same token block. No component-specific CSS file, no inline styles, no hardcoded hex."


# 1. accordion
register(
    "accordion",
    title="Accordion",
    subcategory="Core",
    description="The reference accordion: single-expansion disclosure built from the shared compound primitives — real button triggers in headings, `aria-expanded`/`aria-controls` wiring, grid-rows height animation, and a clean border-divided list treatment. Every other variant in the family is built from these same primitives.",
    tags=TAGS_BASE + ["reference", "single", "compound", "disclosure"],
    features=FEAT_BASE + ["single expansion", "controlled + uncontrolled", "compound regions", "grid-rows animation"],
    accessibility=["button triggers with aria-expanded/aria-controls", "role=region labelled by trigger", "h3 heading wrapper", "closed region hidden from AT"],
    interactive=True,
    related=["accordion-collapsible", "accordion-multiple", "accordion-disabled", "accordion-bordered"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" defaultValue="environments">
  <AccordionItem value="environments">
    <AccordionTrigger>Environments</AccordionTrigger>
    <AccordionContent>
      Production deploys from the main branch.
    </AccordionContent>
  </AccordionItem>
  <AccordionItem value="api-keys">
    <AccordionTrigger>API keys</AccordionTrigger>
    <AccordionContent>
      Keys are shown once at creation time.
    </AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc=props_table(),
    composition_note="The root needs no props at all — `<Accordion>` alone gives an uncontrolled, non-collapsible single accordion. The demos below frame the divided list with a top border via the root's `className`.",
    logic_doc="""**Single mode (default)** keeps at most one item open: opening an item closes the previously open one. With the default `collapsible={false}`, activating the already-open trigger is a no-op — once an item has been opened, exactly one stays open. Pass `collapsible` to let the open item close again.

**Uncontrolled** usage passes `defaultValue` (the initially open value, or nothing to start fully collapsed); the accordion owns the state. **Controlled** usage passes `value` + `onValueChange` (`string | null` in single mode) and the parent owns the state.

The first demo starts with the environments section open. The second starts fully collapsed — opening any section closes the others.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- `type="single"` is the default; `type="multiple"` changes `value`/`onValueChange` to `string[]` (see the accordion-multiple variant).
- `collapsible` only applies to single mode.
- Item `value`s must be unique within the accordion and id-safe (they derive the DOM ids).
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — reference implementation.
 *
 * A WAI-ARIA disclosure accordion as a compound component: `<Accordion>`
 * owns the open-item state, `<AccordionItem>` scopes one entry,
 * `<AccordionTrigger>` is the disclosure control, and `<AccordionContent>`
 * is the collapsible region. Triggers are REAL `<button type="button">`
 * elements wrapped in an `<h3>` heading — never clickable divs — with
 * `aria-expanded` + `aria-controls` wired to stable, per-instance ids.
 *
 * Expansion mode is a discriminated union: `type="single"` (default) keeps
 * at most one item open and supports `collapsible`; `type="multiple"`
 * tracks an array of open values. Both modes are controlled
 * (`value` + `onValueChange`) or uncontrolled (`defaultValue`), with types
 * that match the mode (`string | null` for single, `string[]` for
 * multiple).
 *
 * Open/close animates with the CSS grid-rows trick (0fr <-> 1fr, no
 * JavaScript measurement) plus a discrete `visibility` transition: the
 * closed region is `visibility: hidden`, which removes it from the
 * accessibility tree AND the tab order while the height animates. Content
 * stays mounted in both states, so component state inside a region (form
 * values, scroll position) survives a close/reopen cycle. All transitions
 * are disabled under `prefers-reduced-motion`.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Single expansion · uncontrolled</p>
        <Accordion type="single" defaultValue="environments" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="environments">
            <AccordionTrigger>Environments</AccordionTrigger>
            <AccordionContent>
              Production deploys from the main branch. Every pull request gets an
              isolated preview environment with its own URL, torn down automatically
              when the pull request merges or closes.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="api-keys">
            <AccordionTrigger>API keys</AccordionTrigger>
            <AccordionContent>
              Keys are shown once at creation time. Store them in your secret manager;
              rotating a key invalidates the previous one immediately.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="webhooks">
            <AccordionTrigger>Webhooks</AccordionTrigger>
            <AccordionContent>
              Deliveries are retried with exponential backoff for 24 hours. A endpoint
              that fails for three consecutive days is paused and the team is notified.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>One item open at a time. Activating the open item&apos;s trigger is a no-op — pass collapsible to let it close.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Starts collapsed</p>
        <Accordion type="single" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="general">
            <AccordionTrigger>General</AccordionTrigger>
            <AccordionContent>
              The project name appears in the dashboard, in deployment URLs, and in
              invoice line items. Renaming a project does not change its slug.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="advanced">
            <AccordionTrigger>Advanced</AccordionTrigger>
            <AccordionContent>
              Transfer ownership, export configuration, or delete the project. These
              actions require an owner role and cannot be undone.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Without defaultValue, every item starts closed. Opening one still closes the others.</p>
      </div>
    </div>
  );
}''',
)

# 2. accordion-multiple
register(
    "accordion-multiple",
    title="Multiple Accordion",
    subcategory="Behavior",
    description="Multiple-expansion mode: any number of items can stay open at once. `value` and `onValueChange` become `string[]` — the TypeScript types are discriminated by `type=\"multiple\"`, so the compiler enforces the array shape. Includes a controlled demo with external Expand all / Collapse all actions.",
    tags=TAGS_BASE + ["multiple", "controlled", "uncontrolled", "state"],
    features=FEAT_BASE + ["multiple open items", "discriminated union types", "controlled with external actions", "open-count readout"],
    accessibility=["button triggers with aria-expanded/aria-controls", "role=region labelled by trigger", "closed region hidden from AT"],
    interactive=True,
    related=["accordion", "accordion-collapsible", "accordion-nested"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

const [open, setOpen] = useState<string[]>(["build"]);

<Accordion type="multiple" value={open} onValueChange={setOpen}>
  <AccordionItem value="build">
    <AccordionTrigger>Build settings</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>

// Uncontrolled:
<Accordion type="multiple" defaultValue={["build", "env"]}>…</Accordion>''',
    props_doc="\n\n".join([ACCORDION_PROPS, ITEM_PROPS]),
    composition_note="Nothing about the items changes in multiple mode — only the root's state shape. The controlled demo below shows the parent reading the open array to drive a live count and Expand all / Collapse all actions.",
    logic_doc="""`type="multiple"` lets any number of items stay open: toggling an item adds or removes its value from the open array without touching the others. There is no `collapsible` concept — items always toggle freely.

**Uncontrolled:** `defaultValue={["build", "env"]}` seeds the initially open items. **Controlled:** `value` + `onValueChange` hand the array to the parent, which can inspect it (the `2 of 3 open` readout) and set it directly (Expand all / Collapse all). The TypeScript props are a discriminated union on `type`, so a single-mode `string` value is a compile error in multiple mode and vice versa.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- The controlled `value` must be an array in multiple mode; the discriminated union enforces it at compile time.
- Expand all / Collapse all are ordinary parent-level buttons calling `onValueChange` — the accordion exposes no imperative API.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — multiple-expansion variant.
 *
 * `type="multiple"` lets any number of items stay open at once; `value`,
 * `defaultValue`, and `onValueChange` become `string[]`, enforced by the
 * discriminated-union props. Shares the entire reference core (compound
 * primitives, grid-rows animation, visibility-gated regions) — only the
 * registered demo content differs. Controlled and uncontrolled usage both
 * work; the demo includes parent-driven Expand all / Collapse all actions.
 */''',
    showcase=DEMO_HELPERS + '''
function ControlledDemo() {
  const [open, setOpen] = React.useState(["build"]);
  const VALUES = ["build", "env", "logs"];
  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center gap-2">
        <button type="button" className={BTN_OUTLINE_SM} onClick={() => setOpen(VALUES)}>Expand all</button>
        <button type="button" className={BTN_GHOST_SM} onClick={() => setOpen([])}>Collapse all</button>
        <span className={NOTE} aria-live="polite">{open.length} of {VALUES.length} open</span>
      </div>
      <Accordion type="multiple" value={open} onValueChange={setOpen} className="border-t border-[var(--ds-color-border)]">
        <AccordionItem value="build">
          <AccordionTrigger>Build settings</AccordionTrigger>
          <AccordionContent>
            Builds run in an isolated container with 4 vCPUs and 8 GB of memory.
            The install and build commands come from northline.json or the dashboard.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="env">
          <AccordionTrigger>Environment variables</AccordionTrigger>
          <AccordionContent>
            Variables are encrypted at rest and injected at build and run time.
            Scope a variable to production, preview, or development targets.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="logs">
          <AccordionTrigger>Build logs</AccordionTrigger>
          <AccordionContent>
            Logs stream in real time during a deploy and are retained for 30 days
            on the Pro plan, 90 days on Enterprise.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <p className={NOTE}>Controlled: the parent owns the open array, reads it for the count, and sets it from external buttons.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Multiple expansion · uncontrolled</p>
        <Accordion type="multiple" defaultValue={["regions", "scaling"]} className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="regions">
            <AccordionTrigger>Regions</AccordionTrigger>
            <AccordionContent>
              Functions run in iad1 by default. Add regions to serve traffic closer
              to your users; static assets always deploy to the full edge network.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="scaling">
            <AccordionTrigger>Scaling</AccordionTrigger>
            <AccordionContent>
              Concurrency scales automatically with traffic. Set a maximum to cap
              spend, or reserve baseline concurrency for latency-critical routes.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="failover">
            <AccordionTrigger>Failover</AccordionTrigger>
            <AccordionContent>
              When a region reports elevated errors, traffic shifts to the next
              healthiest region within one minute. No configuration is required.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>defaultValue seeds two open items; every item toggles independently.</p>
      </div>
      <ControlledDemo />
    </div>
  );
}''',
)

# 3. accordion-collapsible
register(
    "accordion-collapsible",
    title="Collapsible Accordion",
    subcategory="Behavior",
    description="Single-expansion mode with `collapsible`: the open item can be closed again by activating its trigger, so zero or one items are open. Shown side-by-side with the default mandatory behavior, where activating the open item's trigger is a no-op and exactly one item stays open.",
    tags=TAGS_BASE + ["collapsible", "single", "toggle", "behavior"],
    features=FEAT_BASE + ["collapsible single mode", "mandatory single-open contrast", "zero-open state"],
    accessibility=["button triggers with aria-expanded/aria-controls", "role=region labelled by trigger", "closed region hidden from AT"],
    interactive=True,
    related=["accordion", "accordion-multiple", "accordion-disabled"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

// The open item can be closed again:
<Accordion type="single" collapsible defaultValue="usage">
  <AccordionItem value="usage">
    <AccordionTrigger>Usage</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>

// Default (mandatory): the open item stays open.
<Accordion type="single" defaultValue="usage">…</Accordion>''',
    props_doc="\n\n".join([ACCORDION_PROPS, ITEM_PROPS]),
    composition_note="Same primitives, one boolean. The two demos below are deliberately identical except for `collapsible` so the behavioral difference is the only variable.",
    logic_doc="""In single mode the `collapsible` prop controls what happens when the user activates the already-open trigger:

- **`collapsible`** — the open item closes and the accordion reaches a zero-open state. This suits supplementary detail (filter panels, advanced settings) where nothing needs to be visible by default.
- **Default (mandatory)** — activating the open trigger is a no-op. Once one item has been opened, exactly one stays open. This suits primary navigation and settings where a section should always be visible.

Opening a different item closes the current one in both cases — `collapsible` only changes the self-toggle.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- `collapsible` is ignored in multiple mode (items always toggle freely).
- A mandatory single accordion can still start fully collapsed if no `defaultValue` is given — the guarantee applies after the first open.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — collapsible single-expansion variant.
 *
 * With `collapsible`, activating the already-open trigger closes it, so a
 * single accordion may have zero or one items open. Without it (the
 * default), the self-toggle is a no-op and exactly one item stays open.
 * Shares the entire reference core — only the registered demo content
 * differs.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Collapsible — the open item can close</p>
        <Accordion type="single" collapsible defaultValue="usage" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="usage">
            <AccordionTrigger>Usage details</AccordionTrigger>
            <AccordionContent>
              Bandwidth, function invocations, and build minutes for the current
              billing period, broken down per project and per day.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="limits">
            <AccordionTrigger>Plan limits</AccordionTrigger>
            <AccordionContent>
              The Pro plan includes 1 TB of bandwidth and 125 GB-hours of function
              memory per month. Overage is billed at the published metered rates.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Click the open trigger again — the section closes and nothing stays open.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Mandatory — one item always stays open</p>
        <Accordion type="single" defaultValue="profile" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="profile">
            <AccordionTrigger>Profile</AccordionTrigger>
            <AccordionContent>
              Your display name and avatar appear on preview deployment comments
              and in the team activity feed.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="security">
            <AccordionTrigger>Security</AccordionTrigger>
            <AccordionContent>
              Two-factor authentication is required for all members of teams with
              SAML single sign-on enabled.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Click the open trigger — nothing happens. One section is always expanded.</p>
      </div>
    </div>
  );
}''',
)

# 4. accordion-with-icons
register(
    "accordion-with-icons",
    title="Accordion with Icons",
    subcategory="Content",
    description="Triggers with a leading icon via the `icon` prop — a ReactNode rendered in a fixed 16px `aria-hidden` slot. Icons supplement the trigger text (settings sections with recognizable glyphs); they never replace it, so the accessible name always comes from real text.",
    tags=TAGS_BASE + ["icons", "leading-icon", "settings"],
    features=FEAT_BASE + ["leading icon slot", "aria-hidden icons", "16px icon sizing", "icon + text hierarchy"],
    accessibility=["icons aria-hidden (meaning from text)", "button triggers with aria-expanded/aria-controls", "role=region labelled by trigger"],
    interactive=True,
    related=["accordion-with-description", "accordion-with-badge", "accordion"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" defaultValue="profile">
  <AccordionItem value="profile">
    <AccordionTrigger icon={<UserIcon />}>Profile</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([TRIGGER_PROPS, ITEM_PROPS]),
    composition_note="Pass any ReactNode to `icon` — the component renders it in a fixed 16px, `aria-hidden`, `shrink-0` slot before the text column. Mixing items with and without icons in one accordion is valid but visually inconsistent; pick one treatment per accordion.",
    logic_doc="""The `icon` prop adds a leading visual affordance to the trigger. It is rendered in an `aria-hidden="true"` span: the glyph helps sighted users scan a list of sections, but the meaning always comes from the trigger text, so the icon carries no information that assistive technology needs.

The slot is 16px square with `shrink-0`, so the icon keeps its size while the title wraps on narrow viewports. Icon color follows `color.muted-foreground` in both themes via the token system.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- Icons must be inline SVG (or another inline node) — the slot sizes them with `[&_svg]:size-4` and inherits `currentColor`.
- Never put meaning only in the icon; the trigger text must stand alone.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — leading-icon variant.
 *
 * The `icon` prop on `<AccordionTrigger>` renders a ReactNode in a fixed
 * 16px `aria-hidden` slot before the title. Icons supplement the trigger
 * text for sighted scanning; the accessible name always comes from the
 * text. Shares the entire reference core — only the registered demo
 * content differs.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Settings sections with leading icons</p>
        <Accordion type="single" defaultValue="profile" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="profile">
            <AccordionTrigger icon={<Icon name="user" />}>Profile</AccordionTrigger>
            <AccordionContent>
              Your display name, avatar, and public profile URL. These appear on
              preview deployment comments and in the team activity feed.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="notifications">
            <AccordionTrigger icon={<Icon name="bell" />}>Notifications</AccordionTrigger>
            <AccordionContent>
              Choose which events send email: failed deploys, domain expirations,
              and usage alerts. Digest emails batch low-priority events once a day.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="security">
            <AccordionTrigger icon={<Icon name="settings" />}>Security</AccordionTrigger>
            <AccordionContent>
              Manage two-factor authentication, active sessions, and personal
              access tokens. Sessions older than 30 days expire automatically.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="archive">
            <AccordionTrigger icon={<Icon name="archive" />}>Archive</AccordionTrigger>
            <AccordionContent>
              Archived projects are read-only and keep their deployment history.
              Restore a project at any time; deletion is permanent after 30 days.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Icons are aria-hidden — the section name carries the meaning. SVGs size to 16px via the slot.</p>
      </div>
    </div>
  );
}''',
)

# 5. accordion-with-description
register(
    "accordion-with-description",
    title="Accordion with Description",
    subcategory="Content",
    description="Triggers with a title plus a short supporting line via the `description` prop — a muted 13px second row under the title that keeps a clean two-level hierarchy. Useful for documentation and settings sections where the title alone is ambiguous.",
    tags=TAGS_BASE + ["description", "two-line trigger", "docs", "hierarchy"],
    features=FEAT_BASE + ["title + description trigger", "muted supporting line", "wrapping two-line layout"],
    accessibility=["description joins the accessible name", "button triggers with aria-expanded/aria-controls", "role=region labelled by trigger"],
    interactive=True,
    related=["accordion-with-icons", "accordion-faq", "accordion"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" defaultValue="install">
  <AccordionItem value="install">
    <AccordionTrigger description="Install the CLI and deploy your first service">
      Getting started
    </AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([TRIGGER_PROPS, ITEM_PROPS]),
    composition_note="The `description` prop renders in the same text column as the title, so the two lines align and wrap together. Keep descriptions to one short sentence — the trigger is a label, not a summary.",
    logic_doc="""The `description` prop adds a muted 13px supporting line under the title inside the trigger button. Because it is part of the button, it joins the accessible name — screen reader users hear the title and the description together, which is exactly the context a two-line trigger is meant to give.

The title keeps its medium weight and foreground color; the description drops to `color.muted-foreground`, so the hierarchy is typographic (weight + color + size), not structural. Both lines wrap with `break-words` on narrow viewports.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- Keep the description to a short clause; long supporting copy belongs in the region content.
- The description is plain text — do not pass interactive elements (a control inside a button is invalid and breaks the trigger).
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — description-trigger variant.
 *
 * The `description` prop on `<AccordionTrigger>` adds a muted 13px
 * supporting line under the title, inside the button — so it wraps with
 * the title and joins the accessible name. Hierarchy is typographic:
 * medium foreground title, muted second line. Shares the entire reference
 * core — only the registered demo content differs.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Documentation sections with supporting lines</p>
        <Accordion type="single" defaultValue="install" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="install">
            <AccordionTrigger description="Install the CLI and deploy your first service">
              Getting started
            </AccordionTrigger>
            <AccordionContent>
              Install the CLI with npm i -g northline, run northline login, then
              northline deploy from your project root. The first deploy provisions
              a preview URL in under a minute.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="config">
            <AccordionTrigger description="Route traffic with northline.json">
              Configuration
            </AccordionTrigger>
            <AccordionContent>
              northline.json declares routes, redirects, and headers. Changes apply
              on the next deploy; the file is validated before the build starts.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="domains">
            <AccordionTrigger description="Point a custom domain at your project">
              Custom domains
            </AccordionTrigger>
            <AccordionContent>
              Add the domain in project settings, create the displayed DNS records,
              and wait for verification. Certificates are issued and renewed
              automatically.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>The description is muted, wraps with the title, and is part of the trigger&apos;s accessible name.</p>
      </div>
    </div>
  );
}''',
)

# 6. accordion-disabled
register(
    "accordion-disabled",
    title="Disabled Accordion Items",
    subcategory="States",
    description="Items disabled at the `<AccordionItem>` level: the trigger renders as a natively disabled button — unfocusable, not activatable by pointer or keyboard, exposed as disabled to assistive technology, and skipped by Tab. Disabled items can never open.",
    tags=TAGS_BASE + ["disabled", "states", "permissions"],
    features=FEAT_BASE + ["item-level disabled", "native disabled semantics", "skipped in tab order", "state not color alone"],
    accessibility=["native disabled attribute", "unfocusable + unactivatable", "skipped by Tab", "no redundant aria-disabled"],
    interactive=True,
    related=["accordion", "accordion-with-badge", "accordion-with-actions"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" defaultValue="staging">
  <AccordionItem value="staging">
    <AccordionTrigger>Staging</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
  <AccordionItem value="production" disabled>
    <AccordionTrigger>Production</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([ITEM_PROPS, TRIGGER_PROPS]),
    composition_note="`disabled` lives on `AccordionItem`, not the trigger — disabling is a property of the whole entry. Pair a disabled item with a visible reason (in the trigger text or adjacent copy) so the state is never a mystery.",
    logic_doc="""Passing `disabled` to an `AccordionItem` disables the whole entry. The trigger renders with the native `disabled` attribute, which gives the correct behavior for free: the button cannot be clicked, cannot be activated with Enter/Space, is removed from the Tab order, and is announced as disabled (dimmed/unavailable) by screen readers.

The toggle handler also guards against disabled items, so even a programmatic toggle request is refused — a disabled item cannot open through any path. Native `disabled` is used instead of `aria-disabled` because the item must be inert, not merely announced as disabled.""",
    keyboard_doc=KEYBOARD_BASE + """

A disabled trigger is removed from the Tab order entirely (native `disabled`), so keyboard users skip over it rather than landing on a control that does nothing.""",
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """

- The demo pairs each disabled item with a visible reason (`requires approval` / `Enterprise plan`), because a control that is merely grey invites confusion. The 50% opacity is a supplement, never the only signal.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- Prefer `disabled` over hiding the item when the user should know the section exists but cannot use it yet.
- `disabled` is per-item; disabling every item of an accordion is valid but usually means the whole section should be hidden instead.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — disabled-items variant.
 *
 * `disabled` on `<AccordionItem>` disables the whole entry: the trigger is
 * a natively disabled button (unfocusable, unactivatable, announced as
 * disabled, skipped by Tab), and the toggle path guards against it too, so
 * a disabled item cannot open through any interaction. Shares the entire
 * reference core — only the registered demo content differs.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Environment targets with gated access</p>
        <Accordion type="single" defaultValue="staging" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="staging">
            <AccordionTrigger>Staging</AccordionTrigger>
            <AccordionContent>
              Every push to the staging branch deploys here. The staging database
              is seeded nightly from an anonymized production snapshot.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="production" disabled>
            <AccordionTrigger badge="requires approval">Production</AccordionTrigger>
            <AccordionContent>
              Production deploys require a second approver from the release team.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="edge" disabled>
            <AccordionTrigger badge="Enterprise">Edge network</AccordionTrigger>
            <AccordionContent>
              Multi-region edge replication is available on the Enterprise plan.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Two items are natively disabled: unclickable, skipped by Tab, announced as disabled. The badge states the reason.</p>
      </div>
    </div>
  );
}''',
)

# 7. accordion-with-badge
register(
    "accordion-with-badge",
    title="Accordion with Badge",
    subcategory="Content",
    description="Triggers with a status or count badge via the `badge` prop — a neutral token-styled pill pinned before the chevron. The badge is plain, non-interactive text inside the button: it never intercepts clicks and never creates a confusing accessible name.",
    tags=TAGS_BASE + ["badge", "status", "count", "pill"],
    features=FEAT_BASE + ["trailing badge pill", "non-interactive badge", "accessible-name safe", "token-styled pill"],
    accessibility=["badge text joins the trigger name", "non-interactive pill (no nested controls)", "button triggers with aria-expanded/aria-controls"],
    interactive=True,
    related=["accordion-with-icons", "accordion-disabled", "accordion-faq"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" defaultValue="checks">
  <AccordionItem value="checks">
    <AccordionTrigger badge="3 errors">Failed checks</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([TRIGGER_PROPS, ITEM_PROPS]),
    composition_note="The badge slot takes a ReactNode but is designed for short text (`\"3 errors\"`, `\"Beta\"`, `\"New\"`). It renders as a span — never a button or link — so the trigger remains the only control in the heading.",
    logic_doc="""The `badge` prop renders a neutral pill (1px `color.border`, `color.surface-subtle` fill, 11px muted text) between the title column and the chevron. It is `shrink-0`, so long titles wrap instead of squeezing the badge.

Because the pill is plain text inside the trigger button, its text joins the accessible name — `Failed checks, 3 errors, expanded, button` — which is meaningful as long as the badge text is meaningful. Prefer words-plus-count (`3 errors`) over bare symbols. The badge never intercepts pointer events: the whole trigger row remains one button.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- Keep badge text short and meaningful — it is announced as part of the trigger name.
- Do not pass interactive content; a control inside the trigger button is invalid HTML and breaks the disclosure.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — badge variant.
 *
 * The `badge` prop on `<AccordionTrigger>` renders a short status/count
 * pill before the chevron: neutral token styling, `shrink-0`, plain text
 * inside the button (so it joins the accessible name and never intercepts
 * clicks). Shares the entire reference core — only the registered demo
 * content differs.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Status and count badges</p>
        <Accordion type="single" defaultValue="checks" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="checks">
            <AccordionTrigger badge="3 errors">Failed checks</AccordionTrigger>
            <AccordionContent>
              The type check, the integration test suite, and the preview smoke
              test failed on the last deploy. Re-run checks after fixing the
              failing commit.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="integrations">
            <AccordionTrigger badge="Beta">Integrations</AccordionTrigger>
            <AccordionContent>
              Connect issue tracking and error monitoring from the integrations
              directory. The directory API is in beta and may change.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="changelog">
            <AccordionTrigger badge="New">Changelog digest</AccordionTrigger>
            <AccordionContent>
              A weekly digest of shipped changes across the projects you own,
              delivered every Monday morning.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Badges are non-interactive pills; their text joins the trigger&apos;s accessible name.</p>
      </div>
    </div>
  );
}''',
)

# 8. accordion-faq
register(
    "accordion-faq",
    title="FAQ Accordion",
    subcategory="Content",
    description="A realistic frequently-asked-questions accordion: question/answer pairs with roomier region padding, body-sm answer copy, and semantic question text in the trigger (the question IS the button label — no redundant ARIA question roles).",
    tags=TAGS_BASE + ["faq", "questions", "support", "content"],
    features=FEAT_BASE + ["question/answer semantics", "roomier region padding", "multiple mode", "realistic support copy"],
    accessibility=["question text = accessible name", "role=region labelled by trigger", "closed region hidden from AT"],
    interactive=True,
    related=["accordion-with-description", "accordion", "accordion-multiple"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="multiple">
  <AccordionItem value="billing">
    <AccordionTrigger>How is metered usage billed?</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([ACCORDION_PROPS, ITEM_PROPS, TRIGGER_PROPS, CONTENT_PROPS]),
    composition_note="FAQ content uses `type=\"multiple\"` so readers can keep several answers open while comparing them, and a slightly roomier region (`pb-5`) since answers are read, not scanned. The question stays in the trigger — no heading levels are skipped because each trigger already sits in an `h3`.",
    logic_doc="""An FAQ is the canonical accordion use case: the question is the trigger label, the answer is the region. This variant keeps the default treatment and adds only realistic support copy and roomier region padding — no special "FAQ styling" is invented, because the pattern is content, not chrome.

Multiple mode is used so a reader can open two answers side by side. Each trigger's `h3` wrapper keeps the questions in the page outline, which is exactly how users scan a FAQ with assistive technology: jump between headings, then activate the button for the full answer.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """

- There are no ARIA roles for "question" and "answer" — the disclosure pattern (button + `aria-expanded` + `role="region"`) is the correct semantics. Adding more ARIA would only add noise.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- Long answers belong in the region; if an answer needs structure, compose lists and links inside `AccordionContent` — it accepts any ReactNode.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — FAQ variant.
 *
 * Question/answer disclosure: the question is the trigger label (sitting in
 * its `h3` wrapper, so questions stay in the page outline), the answer is
 * the region. Multiple mode lets readers keep answers open side by side;
 * region padding is roomier for reading. No special "FAQ" chrome — the
 * pattern is content, not styling. Shares the entire reference core.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Billing and usage questions</p>
        <Accordion type="multiple" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="metered">
            <AccordionTrigger>How is metered usage billed?</AccordionTrigger>
            <AccordionContent className="pb-5">
              Bandwidth, function invocations, and build minutes are metered
              hourly and billed at the end of each monthly cycle. The usage
              dashboard shows the same numbers the invoice is computed from, so
              there are no surprises at renewal.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="quota">
            <AccordionTrigger>What happens when I exceed my plan quota?</AccordionTrigger>
            <AccordionContent className="pb-5">
              Nothing breaks. Overage is billed at the published metered rates,
              and a usage alert fires at 80% and 100% of the included quota. Set
              a hard spend cap in billing settings to stop metered usage instead.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="proration">
            <AccordionTrigger>Are plan changes prorated?</AccordionTrigger>
            <AccordionContent className="pb-5">
              Upgrades apply immediately and the invoice is prorated to the day.
              Downgrades take effect at the end of the current cycle so you keep
              what you have already paid for.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="export">
            <AccordionTrigger>Can I export my data if I cancel?</AccordionTrigger>
            <AccordionContent className="pb-5">
              Yes. Deployment artifacts, environment variables, and analytics
              exports remain available for 90 days after cancellation. After
              that, all project data is permanently deleted.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Multiple mode: readers can compare answers without losing their place. Questions are h3 headings in the page outline.</p>
      </div>
    </div>
  );
}''',
)


# 9. accordion-nested
register(
    "accordion-nested",
    title="Nested Accordion",
    subcategory="Composite",
    description="An accordion inside an accordion's region: each `<Accordion>` instance owns an independent state and id base (via `useId`), so nested items toggle without touching the parent, ids never collide, and keyboard behavior stays the predictable native-button model at every depth.",
    tags=TAGS_BASE + ["nested", "independent state", "hierarchy", "composite"],
    features=FEAT_BASE + ["independent nested state", "no id collisions", "parent stays open", "predictable tab order"],
    accessibility=["per-instance id base (no collisions)", "parent/child states fully independent", "role=region at every level"],
    interactive=True,
    related=["accordion-multiple", "accordion", "accordion-with-description"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" defaultValue="databases">
  <AccordionItem value="databases">
    <AccordionTrigger>Databases</AccordionTrigger>
    <AccordionContent>
      <Accordion type="multiple">
        <AccordionItem value="postgres">
          <AccordionTrigger>Postgres</AccordionTrigger>
          <AccordionContent>…</AccordionContent>
        </AccordionItem>
      </Accordion>
    </AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([ACCORDION_PROPS, ITEM_PROPS, CONTENT_PROPS]),
    composition_note="Nesting is plain composition — `AccordionContent` accepts any ReactNode, including another `<Accordion>`. Give nested items their own `value`s (they only need to be unique within their own accordion) and indent the nested list with the content's `className`.",
    logic_doc="""Each `<Accordion>` creates its own context and its own `useId` base, so nesting requires zero special handling:

- **Independent state** — the nested accordion tracks its own open values; toggling a nested item never bubbles to the parent, and the parent region stays open while you work inside it.
- **No id collisions** — the parent's and child's trigger/region ids derive from different instance ids, so `aria-controls` relationships stay correct at every depth.
- **Predictable keyboard** — nested triggers are ordinary buttons in the same Tab order: Tab walks into the open region and reaches the nested triggers in document order. No arrow-key tricks to learn.

Keep nesting to one level deep in real interfaces; deeper trees are usually better served by navigation.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- The nested list is indented with the region's own padding — the parent and child use the same trigger geometry, so the hierarchy reads through indentation, not different styling.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — nested variant.
 *
 * An `<Accordion>` composed inside an `<AccordionContent>`: each instance
 * owns its state and its `useId` base, so nested items toggle without
 * touching the parent, trigger/region ids never collide, and keyboard
 * behavior stays the native-button model at every depth. Shares the entire
 * reference core — only the registered demo content differs.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Infrastructure settings with nested services</p>
        <Accordion type="single" defaultValue="databases" className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="databases">
            <AccordionTrigger>Databases</AccordionTrigger>
            <AccordionContent>
              <p className="m-0 pb-3">
                Managed databases run in the same region as your functions and are
                backed up every 24 hours.
              </p>
              <Accordion type="multiple" className="border-t border-[var(--ds-color-border)]">
                <AccordionItem value="postgres">
                  <AccordionTrigger>Postgres</AccordionTrigger>
                  <AccordionContent>
                    Point-in-time recovery covers the last 7 days. Connection
                    pooling is enabled by default on all plans.
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="redis">
                  <AccordionTrigger>Redis</AccordionTrigger>
                  <AccordionContent>
                    An in-memory store for sessions and rate limiting, with
                    optional persistence. Eviction policy defaults to allkeys-lru.
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="kv">
                  <AccordionTrigger>Key-value store</AccordionTrigger>
                  <AccordionContent>
                    An eventually consistent edge store for configuration and
                    feature flags, replicated to every region within 60 seconds.
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="compute">
            <AccordionTrigger>Compute</AccordionTrigger>
            <AccordionContent>
              Functions scale to zero by default. Reserved concurrency keeps a
              baseline warm for latency-sensitive routes.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="storage">
            <AccordionTrigger>Object storage</AccordionTrigger>
            <AccordionContent>
              S3-compatible object storage with signed upload URLs and lifecycle
              rules for automatic archival.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>The nested accordion keeps its own state: open Postgres and Redis while the parent stays open. Parent and child ids never collide.</p>
      </div>
    </div>
  );
}''',
)

# 10. accordion-with-actions
register(
    "accordion-with-actions",
    title="Accordion with Actions",
    subcategory="Composite",
    description="Accordion regions that contain real actions — buttons and links inside the expanded content. The trigger itself stays a single clean button (no nested controls); actions live in the region, where they are fully keyboard reachable and operable while the item is open.",
    tags=TAGS_BASE + ["actions", "buttons", "links", "composite"],
    features=FEAT_BASE + ["real buttons in content", "real links in content", "keyboard reachable actions", "no nested trigger controls"],
    accessibility=["actions inside role=region", "no nested controls in trigger", "focus-visible rings on actions"],
    interactive=True,
    related=["accordion", "accordion-disabled", "accordion-faq"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" collapsible>
  <AccordionItem value="api-keys">
    <AccordionTrigger>API keys</AccordionTrigger>
    <AccordionContent>
      <p>Rotate keys without downtime.</p>
      <button type="button">Rotate key</button>
      <a href="/docs/keys">Key rotation docs</a>
    </AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([CONTENT_PROPS, ITEM_PROPS, TRIGGER_PROPS]),
    composition_note="Compose actions from the DevSnips button treatments (the demo uses the family's small primary/outline/ghost/destructive classes) and real anchors. Never put a button inside `AccordionTrigger` — a control inside a control is invalid HTML and breaks both.",
    logic_doc="""Regions are ordinary content containers, so real controls compose naturally: buttons trigger actions, anchors navigate. Because the closed region is removed from the tab order (`visibility: hidden`), keyboard users only ever reach the actions of open items — there are no ghost tab stops.

Actions stay reachable at every viewport: the demo wraps them in a `flex flex-wrap` row so they reflow onto multiple lines at 375px instead of overflowing. Focus rings on actions use the standard `color.focus-ring` token.""",
    keyboard_doc=KEYBOARD_BASE + """

Actions inside an open region are part of the normal Tab order: Tab from a trigger moves into its open region's first control, and Enter/Space activates it. When the item closes, its actions leave the tab order with it.""",
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- Destructive actions (like Delete project below) should still confirm elsewhere — the accordion region is an entry point, not a confirmation pattern.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — region-actions variant.
 *
 * Regions compose real controls: buttons and anchors inside the expanded
 * content, fully keyboard reachable while the item is open and removed
 * from the tab order when it closes. The trigger stays a single clean
 * button — controls never nest inside it. Shares the entire reference
 * core — only the registered demo content differs.
 */''',
    showcase=DEMO_HELPERS + '''
function ActionDemo() {
  const [log, setLog] = React.useState("No actions yet");
  return (
    <div className="space-y-2">
      <Accordion type="single" collapsible className="border-t border-[var(--ds-color-border)]">
        <AccordionItem value="api-keys">
          <AccordionTrigger>API keys</AccordionTrigger>
          <AccordionContent>
            <p className="m-0">
              The production key was created 42 days ago. Rotating issues a new
              key and invalidates the old one after a 1-hour grace period.
            </p>
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <button type="button" className={BTN_PRIMARY_SM} onClick={() => setLog("Rotated the production key")}>Rotate key</button>
              <a className={LINK} href="#/docs/keys" onClick={(e) => e.preventDefault()}>Key rotation docs</a>
            </div>
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="deploy-hooks">
          <AccordionTrigger>Deploy hooks</AccordionTrigger>
          <AccordionContent>
            <p className="m-0">
              Deploy hooks trigger a production deploy from an external system —
              a CMS publish, a scheduled job, or a chat command.
            </p>
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <button type="button" className={BTN_OUTLINE_SM} onClick={() => setLog("Created a deploy hook")}>Add hook</button>
              <button type="button" className={BTN_GHOST_SM} onClick={() => setLog("Copied the hook URL")}>Copy URL</button>
            </div>
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="danger">
          <AccordionTrigger>Danger zone</AccordionTrigger>
          <AccordionContent>
            <p className="m-0">
              Deleting a project removes every deployment, environment variable,
              and log. The action cannot be undone.
            </p>
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <button type="button" className={BTN_DESTRUCTIVE_SM} onClick={() => setLog("Delete requested — a confirmation dialog would open here")}>Delete project</button>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <p className={NOTE} role="status">{log}</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <ActionDemo />
    </div>
  );
}''',
)

# 11. accordion-loading
register(
    "accordion-loading",
    title="Loading Accordion",
    subcategory="States",
    description="A region that loads asynchronously: while data is pending the content area renders geometry-preserving skeleton bars (aria-hidden) with an sr-only announcement and `aria-busy` on the region — then swaps to the real data without a layout jump. The pulse is disabled under reduced motion.",
    tags=TAGS_BASE + ["loading", "skeleton", "aria-busy", "async"],
    features=FEAT_BASE + ["skeleton bars", "aria-busy region", "sr-only announcement", "geometry preserved", "reduced-motion pulse off"],
    accessibility=["aria-busy on the region", "sr-only loading text", "skeleton aria-hidden", "reduced-motion disables pulse"],
    interactive=True,
    related=["accordion", "accordion-with-actions", "accordion-disabled"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion type="single" defaultValue="usage">
  <AccordionItem value="usage">
    <AccordionTrigger>Usage this period</AccordionTrigger>
    <AccordionContent aria-busy={loading}>
      {loading ? <SkeletonRows /> : <UsageRows data={data} />}
    </AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([CONTENT_PROPS, ITEM_PROPS]),
    composition_note="`aria-busy` is forwarded to the region's content div (like every other attribute). The skeleton is plain divs with `animate-pulse motion-reduce:animate-none` — no measurement, no library.",
    logic_doc="""Async regions need three things: a busy signal for assistive technology, a placeholder that keeps the layout stable, and a motion fallback.

- **`aria-busy`** marks the region as being updated; the demo also renders an sr-only `Loading usage data` so the state is announced even where `aria-busy` is ignored.
- **Geometry** — the skeleton rows use fixed heights matched to the loaded rows, so the swap does not jump the page. The skeleton itself is `aria-hidden` (it is a placeholder, not content).
- **Reduced motion** — `motion-reduce:animate-none` kills the pulse; the bars stay as static placeholders, and the state change remains instant.

The demo loads on mount and re-loads on Reload, so both transitions (skeleton → data and data → skeleton → data) are exercised.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- Keep skeleton row heights close to the real content; a skeleton that is twice the final height is its own layout shift.
- The trigger stays fully operable while a region loads — loading never disables disclosure.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — async-loading region variant.
 *
 * While region data is pending, the content area renders geometry-
 * preserving skeleton bars (`aria-hidden`) with an sr-only announcement
 * and `aria-busy` on the region; the pulse is disabled under
 * `prefers-reduced-motion`. Shares the entire reference core — only the
 * registered demo content differs.
 */''',
    showcase=DEMO_HELPERS + '''
const SKELETON_BAR = "h-3 rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-surface-active)] animate-pulse motion-reduce:animate-none";
const SR_ONLY = "absolute h-px w-px overflow-hidden whitespace-nowrap [clip:rect(0_0_0_0)]";
const DATA_ROW = "flex items-baseline justify-between gap-3 py-1 text-sm leading-6";
const DATA_KEY = "text-[var(--ds-color-muted-foreground)]";
const DATA_VAL = "font-medium tabular-nums text-[var(--ds-color-foreground)]";

function UsagePanel() {
  const [run, setRun] = React.useState(0);
  const [loading, setLoading] = React.useState(true);
  React.useEffect(() => {
    setLoading(true);
    const t = setTimeout(() => setLoading(false), 1400);
    return () => clearTimeout(t);
  }, [run]);
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <button type="button" className={BTN_OUTLINE_SM} onClick={() => setRun((r) => r + 1)} disabled={loading}>
          {loading ? "Loading…" : "Reload usage"}
        </button>
      </div>
      <Accordion type="single" defaultValue="usage" className="border-t border-[var(--ds-color-border)]">
        <AccordionItem value="usage">
          <AccordionTrigger>Usage this period</AccordionTrigger>
          <AccordionContent aria-busy={loading}>
            {loading ? (
              <div className="space-y-2 py-1" aria-hidden="true">
                <div className={SKELETON_BAR + " w-11/12"} />
                <div className={SKELETON_BAR + " w-3/4"} />
                <div className={SKELETON_BAR + " w-2/3"} />
              </div>
            ) : (
              <div>
                <div className={DATA_ROW}><span className={DATA_KEY}>Bandwidth</span><span className={DATA_VAL}>812 GB / 1 TB</span></div>
                <div className={DATA_ROW}><span className={DATA_KEY}>Function invocations</span><span className={DATA_VAL}>1.9M / 2M</span></div>
                <div className={DATA_ROW}><span className={DATA_KEY}>Build minutes</span><span className={DATA_VAL}>412 / 500</span></div>
              </div>
            )}
            {loading ? <span className={SR_ONLY}>Loading usage data</span> : null}
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="history">
          <AccordionTrigger>Previous periods</AccordionTrigger>
          <AccordionContent>
            Usage history for the last 12 billing periods is available as a CSV
            export from the billing settings page.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <p className={NOTE}>aria-busy + sr-only announcement while pending; skeleton heights match the loaded rows so nothing jumps.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <UsagePanel />
    </div>
  );
}''',
)

# 12. accordion-bordered
register(
    "accordion-bordered",
    title="Bordered Accordion",
    subcategory="Layout",
    description="The contained treatment: the same accordion framed in a `radius-md` bordered surface — an alternate structure for settings panels and cards, driven entirely by the root's `className`. The trigger's inset focus ring is what makes this work: it is never clipped by the container's `overflow-hidden`.",
    tags=TAGS_BASE + ["bordered", "contained", "layout", "surface"],
    features=FEAT_BASE + ["contained bordered treatment", "radius-md surface", "inset focus ring", "className-driven"],
    accessibility=["inset focus ring never clipped", "button triggers with aria-expanded/aria-controls", "role=region labelled by trigger"],
    interactive=True,
    related=["accordion", "accordion-faq", "accordion-with-description"],
    usage='''import Accordion, {
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "./accordion";

<Accordion
  type="single"
  collapsible
  className="overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]"
>
  <AccordionItem value="general">
    <AccordionTrigger>General</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>''',
    props_doc="\n\n".join([ACCORDION_PROPS, ITEM_PROPS]),
    composition_note="The bordered treatment is a container concern, not a component prop: apply `overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]` to the root. The last item's divider is already suppressed (`last:border-b-0`), so the container border closes the list cleanly.",
    logic_doc="""Two structural treatments from the same primitives:

- **Flush (default)** — a border-divided list that sits directly on the page; the reference and most variants use this.
- **Contained** — the root carries a `radius-md` border and surface background; `overflow-hidden` clips the first and last trigger's hover wash to the container's corners.

The contained treatment works because the trigger's focus ring is drawn inset (`-outline-offset-2`): the container's `overflow-hidden` never clips the keyboard focus indicator. This is the deliberate reason for the inset ring — it is an architectural decision, not a style preference.""",
    keyboard_doc=KEYBOARD_BASE,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="""- The container gets the surface, the items keep their dividers — do not add borders to both the root and the items.
- """ + NOTES_TOKENS,
    tsx_header='''/**
 * DevSnips React Accordion — bordered-container variant.
 *
 * The contained structural treatment: the root carries a `radius-md`
 * border, a surface background, and `overflow-hidden`, driven entirely by
 * `className`. It works because the trigger's focus ring is drawn inset
 * (`-outline-offset-2`), so the container never clips the keyboard focus
 * indicator. Shares the entire reference core — only the registered demo
 * content differs.
 */''',
    showcase=DEMO_HELPERS + '''
const BORDERED = "overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]";

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Contained — bordered surface</p>
        <Accordion type="single" collapsible className={BORDERED}>
          <AccordionItem value="general">
            <AccordionTrigger>General</AccordionTrigger>
            <AccordionContent>
              The workspace name appears in the dashboard sidebar and in email
              notifications. Members see the same name on their invites.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="members">
            <AccordionTrigger>Members</AccordionTrigger>
            <AccordionContent>
              Invite teammates by email. Invites expire after 7 days; pending
              invites can be re-sent or revoked from this panel.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="billing">
            <AccordionTrigger>Billing</AccordionTrigger>
            <AccordionContent>
              One subscription per workspace. Invoices are emailed to every
              billing contact and archived in the billing settings page.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>radius-md border + surface, className-driven. Hover the first item — the wash clips to the rounded corners; focus a trigger — the inset ring stays visible.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Flush — divided list (default)</p>
        <Accordion type="single" collapsible className="border-t border-[var(--ds-color-border)]">
          <AccordionItem value="a">
            <AccordionTrigger>General</AccordionTrigger>
            <AccordionContent>
              The same primitives without the container: dividers only, sitting
              directly on the page background.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="b">
            <AccordionTrigger>Members</AccordionTrigger>
            <AccordionContent>
              Both treatments share the identical trigger geometry, focus ring,
              and animation — the structure is a container decision.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
        <p className={NOTE}>Same component, no container chrome — the treatment lives on the root&apos;s className.</p>
      </div>
    </div>
  );
}''',
)

