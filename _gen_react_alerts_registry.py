"""Registry for the DevSnips React Alerts generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference ``alert/code.tsx``). The
generator (``_gen_react_alerts.py``) combines these with the reference
``code.tsx`` on disk to write ``code.tsx`` (derived), ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented demo content only (deploys, billing, quotas,
backups, API versions). No lorem ipsum, no marketing buzzwords, no emoji.
"""
from _gen_react_alerts import (
    register,
    ALERT_PROPS, ICON_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, ACTION_PROPS,
    CLOSE_PROPS, props_table,
)

TAGS_BASE = ["alert", "feedback", "react", "tailwind", "accessible", "responsive", "tokens"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "live-region roles", "token-driven surface"]

# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = r"""const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const BTN_PRIMARY_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_OUTLINE_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_GHOST_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-transparent px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,currentColor_8%,transparent)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const LINK = "font-medium text-[var(--ds-color-link)] underline underline-offset-2 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
"""

KEYBOARD_STATIC = """The alert surface itself is not focusable and carries no keyboard behavior — it is feedback, not a control. Any interactive element composed inside it (an action button, a link) is a real native control: Tab reaches it, Enter/Space activates it, and a `focus-visible` ring (2px, `color.focus-ring` token) marks keyboard focus."""

KEYBOARD_DISMISS = KEYBOARD_STATIC + """

The close button is a real `<button type="button">`: Tab reaches it and Enter/Space activates it. When dismissal removes the focused button from the DOM, focus moves to the next operable element in document order (or the previous one at the end of the page) — it never drops to `<body>`."""

A11Y_BASE = """- The root carries a live-region role matched to urgency: `role="status"` (polite) for default/info/success, `role="alert"` (assertive) for warning/destructive — informational messages are never blanket-promoted to `role="alert"`.
- `AlertTitle` / `AlertDescription` register themselves with the root, so `aria-labelledby` / `aria-describedby` always reference real rendered content and are omitted entirely when the region is absent.
- The semantic icon is `aria-hidden="true"`: meaning is carried by the role and text, so state is never communicated by color alone.
- Pass `role={null}` for static page content that should not announce itself (for example an always-visible note rendered at page load)."""

RESPONSIVE_BASE = """The alert is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px the title and description wrap (long words break), while the icon and close button shrink-wrap instead of pushing text out — the text column is `flex-1` with `min-w-0`. `AlertAction` is `flex-wrap`, so multiple actions wrap to another row instead of overflowing, and the close button stays reachable. No horizontal overflow at 375 / 768 / 1280px."""

STATES_BASE = """- **Surface** — `color.surface` for `default`, or a semantic tint derived via `color-mix` from `color.info` / `color.success` / `color.warning` / `color.destructive`; 1px border (part token, part tint), `radius-md`, no elevation — inline alerts are not floating.
- **Title / description** — body-sm: a medium title on `color.foreground`, muted body on `color.muted-foreground`.
- **Icon** — 16px, colored by the variant's semantic token, decorative to assistive technology.
- **Close button** — muted glyph with a translucent `currentColor` hover wash, a `focus-visible` ring, and native `disabled` styling (50% opacity, no pointer events).
- **Dismissed** — unmounts from the DOM (uncontrolled) or when the parent sets `open={false}` (controlled); `onDismiss` fires in both modes."""


# 1. alert
register(
    "alert",
    title="Alert",
    subcategory="Core",
    description="The reference alert: a restrained inline feedback surface (radius-md, 1px border) with the title / description / icon / action / close primitives and role-matched live-region behavior. Every other variant in the family is built from these same primitives.",
    tags=TAGS_BASE + ["reference", "compound", "composition", "status"],
    features=FEAT_BASE + ["compound regions", "registered title/description association", "role override"],
    accessibility=["role=status by default (polite)", "aria-labelledby/describedby wired by registration", "role={null} for static content"],
    interactive=False,
    related=["alert-info", "alert-with-icon", "alert-dismissible", "alert-rich"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert";

<Alert>
  <AlertTitle>Usage resets on the 1st</AlertTitle>
  <AlertDescription>
    Your plan's request quota renews at the start of each billing cycle.
  </AlertDescription>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="Only compose the regions an alert needs — the second demo below is a bare `AlertDescription` with `role={null}`, which is the right shape for static page content that must not announce itself as a live region.",
    logic_doc="""`Alert` is a structural surface with a variant-driven role and tint. The default variant is neutral: no automatic icon, the `color.surface` background, and a polite `role="status"`.

The first demo composes `AlertTitle` + `AlertDescription` — the primitives register themselves, so the root's `aria-labelledby` / `aria-describedby` point at real content. The second demo renders static informational content with `role={null}`: it stays out of the live region because it is part of the page, not an event.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The `Alert` root forwards every attribute of a plain `<div>` (`id`, `aria-*`, `data-*`). If the message is a transient event (saved, failed, quota reached), keep the derived role; if it is static content, pass `role={null}`.",
    tsx_header='''/**
 * DevSnips React Alert — reference implementation.
 *
 * Inline feedback as a compound component: `<Alert>` is the bordered surface
 * (radius-md, 1px border, token-tinted per variant) and the region primitives
 * compose inside it — `<AlertIcon>` (semantic leading icon, decorative to AT
 * because the meaning is carried by the role + text), `<AlertTitle>`,
 * `<AlertDescription>`, `<AlertAction>` (a wrapping row of real buttons /
 * anchors), and `<AlertClose>` (a real dismiss button with an accessible
 * name).
 *
 * Urgency is expressed with ARIA roles, never color alone: informational
 * variants (`default`, `info`, `success`) default to `role="status"` (polite)
 * and attention-demanding variants (`warning`, `destructive`) default to
 * `role="alert"` (assertive). Pass `role` to override, or `role={null}` for
 * static page content that should not be a live region at all.
 *
 * Dismissal is controlled (`open` + `onDismiss`) or uncontrolled
 * (`defaultOpen`), and never strands keyboard focus: when the focused close
 * button disappears, focus moves to the next operable element in document
 * order before the alert unmounts.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Title + description</p>
        <Alert>
          <AlertTitle>Usage resets on the 1st</AlertTitle>
          <AlertDescription>
            Your plan&apos;s request quota renews at the start of each billing cycle.
            Current period usage is preserved in the usage export.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>The default variant is neutral: surface background, no automatic icon, polite role=&quot;status&quot;.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Description only, static content</p>
        <Alert role={null}>
          <AlertDescription>
            API version 2026-08 is the default for keys created after August 1.
            Existing keys keep their pinned version until rotated.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>role=&#123;null&#125; keeps static page content out of the live region — it is part of the page, not an event.</p>
      </div>
    </div>
  );
}''',
)

# 2. alert-info
register(
    "alert-info",
    title="Info Alert",
    subcategory="Severity",
    description="Informational feedback: a neutral-blue tint derived from the `color.info` token, the info glyph, and a polite `role=\"status\"` — for neutral, non-urgent messages the user should know about but does not have to act on.",
    tags=TAGS_BASE + ["info", "informational", "status", "polite"],
    features=FEAT_BASE + ["info tint + glyph", "polite role=status", "long-content wrapping"],
    accessibility=["role=status (polite, non-interrupting)", "icon aria-hidden, meaning in text", "not color alone: glyph + wording"],
    interactive=False,
    related=["alert", "alert-success", "alert-warning", "alert-with-link"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-info";

<Alert variant="info">
  <AlertTitle>Scheduled maintenance</AlertTitle>
  <AlertDescription>
    The EU region will be read-only on Sunday from 02:00 to 02:30 UTC.
  </AlertDescription>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, ICON_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="`variant=\"info\"` supplies the tint, the leading info glyph, and the polite role automatically — compose only the content regions.",
    logic_doc="""The info variant announces politely (`role="status"`), so it never interrupts what a screen-reader user is currently doing — the right urgency for neutral, informational messages.

The second demo renders intentionally long content: the description wraps at any width, long unbroken strings break, and the icon stays pinned to the first line instead of stretching.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- `role="status"` maps to `aria-live="polite"` implicitly — the message is queued, not shouted. Do not add `aria-live` yourself; the role already carries it, and nesting live regions causes duplicate announcements.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Reserve `info` for neutral messages. If the user must act promptly (quota exhausted, payment failing), use `warning` or `destructive` instead.",
    tsx_header='''/**
 * DevSnips React Alert — Info.
 *
 * The shared alert core; this variant demonstrates `variant="info"`: a
 * neutral-blue tint derived from the `color.info` token, the info glyph,
 * and a polite `role="status"` for non-urgent informational messages.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Scheduled maintenance</p>
        <Alert variant="info">
          <AlertTitle>Scheduled maintenance</AlertTitle>
          <AlertDescription>
            The EU region will be read-only on Sunday from 02:00 to 02:30 UTC.
            Writes resume automatically; no action is required.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>Polite announcement: role=&quot;status&quot; queues the message instead of interrupting.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Long content wraps</p>
        <Alert variant="info">
          <AlertTitle>New region available: eu-central-2 (Zurich)</AlertTitle>
          <AlertDescription>
            Projects pinned to the eu-central region group can now replicate read
            workloads to eu-central-2. Replication keys use the format
            ds_eu_central_2_9f8b7a6c5d4e3f2a1b0c9d8e7f6a5b4c and inherit the
            project&apos;s existing retention policy.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>Long titles wrap, unbroken strings break, and the icon stays pinned to the first line.</p>
      </div>
    </div>
  );
}''',
)

# 3. alert-success
register(
    "alert-success",
    title="Success Alert",
    subcategory="Severity",
    description="Confirmation of a completed operation: a green tint derived from the `color.success` token, the check glyph, and a polite `role=\"status\"` — for \"it worked\" feedback after saves, payments, backups, and syncs.",
    tags=TAGS_BASE + ["success", "confirmation", "status", "polite"],
    features=FEAT_BASE + ["success tint + check glyph", "polite role=status"],
    accessibility=["role=status (polite)", "icon aria-hidden, outcome in text", "not color alone: glyph + wording"],
    interactive=False,
    related=["alert-info", "alert-destructive", "alert-dismissible", "alert-live"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-success";

<Alert variant="success">
  <AlertTitle>Payment method updated</AlertTitle>
  <AlertDescription>
    Invoices will now be charged to the Visa ending in 4242.
  </AlertDescription>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, ICON_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="`variant=\"success\"` supplies the tint, the check glyph, and the polite role — confirm the outcome in the title, state the consequence in the description.",
    logic_doc="""The success variant confirms that an operation finished. It announces politely (`role="status"`) — a confirmation should never interrupt the user's next task.

Write the title as the outcome ("Payment method updated") and the description as the consequence ("Invoices will now be charged to …"), so the message is meaningful even without the color and glyph.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="For transient success feedback after an async action (save, export), mount the alert when the operation resolves — see `alert-live` for the dynamic pattern.",
    tsx_header='''/**
 * DevSnips React Alert — Success.
 *
 * The shared alert core; this variant demonstrates `variant="success"`: a
 * green tint derived from the `color.success` token, the check glyph, and a
 * polite `role="status"` for confirmations of completed operations.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Billing change confirmed</p>
        <Alert variant="success">
          <AlertTitle>Payment method updated</AlertTitle>
          <AlertDescription>
            Invoices will now be charged to the Visa ending in 4242. The previous
            card was removed from the workspace.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>Title = outcome, description = consequence — meaningful without the color.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Background job finished</p>
        <Alert variant="success">
          <AlertTitle>Nightly backup completed</AlertTitle>
          <AlertDescription>
            14.2 GB archived to cold storage at 03:00 UTC. The next backup runs
            in 21 hours.
          </AlertDescription>
        </Alert>
      </div>
    </div>
  );
}''',
)

# 4. alert-warning
register(
    "alert-warning",
    title="Warning Alert",
    subcategory="Severity",
    description="Caution that needs attention before it becomes a failure: an amber tint derived from the `color.warning` token, the triangle glyph, and an assertive `role=\"alert\"` — for quota, deprecation, and expiring-access messages.",
    tags=TAGS_BASE + ["warning", "caution", "alert-role", "assertive"],
    features=FEAT_BASE + ["warning tint + triangle glyph", "assertive role=alert", "deprecation pattern"],
    accessibility=["role=alert (assertive)", "icon aria-hidden, risk in text", "not color alone: glyph + wording"],
    interactive=False,
    related=["alert-destructive", "alert-with-action", "alert-dismissible"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-warning";

<Alert variant="warning">
  <AlertTitle>Approaching request limit</AlertTitle>
  <AlertDescription>
    91% of this month's quota is used. Upgrade or throttle to avoid 429 responses.
  </AlertDescription>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, ICON_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="`variant=\"warning\"` supplies the tint, the triangle glyph, and the assertive role — state the risk in the title and the consequence (plus how to avoid it) in the description.",
    logic_doc="""The warning variant is assertive (`role="alert"`): a warning exists to be noticed, so it may interrupt. Use it for conditions that will become failures if ignored — quota exhaustion, retiring endpoints, expiring credentials.

The second demo is the deprecation pattern: name the retiring surface, give the date, and point at the replacement. Every warning should answer "what happens if I do nothing?".""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- `role="alert"` maps to `aria-live="assertive"` implicitly — reserved for messages that genuinely need prompt attention. If everything is assertive, nothing is.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Warnings pair naturally with an action (upgrade, migrate, renew) — see `alert-with-action` for the composition.",
    tsx_header='''/**
 * DevSnips React Alert — Warning.
 *
 * The shared alert core; this variant demonstrates `variant="warning"`: an
 * amber tint derived from the `color.warning` token, the triangle glyph, and
 * an assertive `role="alert"` for cautions that need attention before they
 * become failures.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Quota caution</p>
        <Alert variant="warning">
          <AlertTitle>Approaching request limit</AlertTitle>
          <AlertDescription>
            91% of this month&apos;s quota is used. Requests above the limit
            return 429 responses until the cycle resets on the 1st.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>Assertive announcement: role=&quot;alert&quot; is reserved for messages that need prompt attention.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Deprecation</p>
        <Alert variant="warning">
          <AlertTitle>Deprecated endpoint</AlertTitle>
          <AlertDescription>
            GET /v1/users retires on 2026-12-01. Migrate to /v2/users before the
            cutoff; the old route then returns 410 Gone.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>Every warning answers &quot;what happens if I do nothing?&quot;.</p>
      </div>
    </div>
  );
}''',
)

# 5. alert-destructive
register(
    "alert-destructive",
    title="Destructive Alert",
    subcategory="Severity",
    description="Failures and blocking errors: a red tint derived from the `color.destructive` token, the error glyph, and an assertive `role=\"alert\"` — for failed operations and validation summaries the user must resolve.",
    tags=TAGS_BASE + ["destructive", "error", "alert-role", "assertive", "validation"],
    features=FEAT_BASE + ["destructive tint + error glyph", "assertive role=alert", "error-summary pattern"],
    accessibility=["role=alert (assertive)", "icon aria-hidden, failure in text", "not color alone: glyph + wording"],
    interactive=False,
    related=["alert-warning", "alert-with-action", "alert-rich", "alert-live"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-destructive";

<Alert variant="destructive">
  <AlertTitle>Deployment failed</AlertTitle>
  <AlertDescription>
    Build #482 exited with code 1 during the test step.
  </AlertDescription>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, ICON_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="`variant=\"destructive\"` supplies the tint, the error glyph, and the assertive role. `AlertDescription` is a `<div>`, so an error summary can contain a real list — see the second demo.",
    logic_doc="""The destructive variant is assertive (`role="alert"`): the operation failed and the user must do something before they can continue.

The first demo reports a failed deployment. The second is the form error-summary pattern: the description contains a real `<ul>` of field errors, so keyboard and screen-reader users can enumerate what must be fixed — the summary says what is wrong, the fields say where.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- Error summaries list every problem in text; the red tint and glyph are supplements, never the only error indication.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="When the user can fix the failure inline (retry, update billing), add an action — see `alert-with-action`. When the message arrives asynchronously, mount it on the event — see `alert-live`.",
    tsx_header='''/**
 * DevSnips React Alert — Destructive.
 *
 * The shared alert core; this variant demonstrates
 * `variant="destructive"`: a red tint derived from the `color.destructive`
 * token, the error glyph, and an assertive `role="alert"` for failures and
 * blocking errors — including the form error-summary pattern.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Failed operation</p>
        <Alert variant="destructive">
          <AlertTitle>Deployment failed</AlertTitle>
          <AlertDescription>
            Build #482 exited with code 1 during the test step. The previous
            release is still live; no traffic was affected.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>Assertive announcement: the failure must be resolved before work continues.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Form error summary</p>
        <Alert variant="destructive">
          <AlertTitle>Could not save the environment</AlertTitle>
          <AlertDescription>
            <p className="m-0">Fix the following fields, then save again:</p>
            <ul className="m-0 mt-1.5 list-disc space-y-1 pl-5">
              <li>Variable name must start with a letter (row 3: 2ND_KEY).</li>
              <li>Value is required for DATABASE_URL.</li>
              <li>Region must be one of eu-central, us-east, ap-south.</li>
            </ul>
          </AlertDescription>
        </Alert>
        <p className={NOTE}>A real list inside the description — enumerable by keyboard and screen reader.</p>
      </div>
    </div>
  );
}''',
)

# 6. alert-with-icon
register(
    "alert-with-icon",
    title="Alert with Icon",
    subcategory="Content",
    description="The leading icon slot in detail: semantic variants render their status glyph automatically, the `icon` prop replaces it with any `ReactNode`, and `icon={null}` suppresses it — the icon is always decorative to assistive technology.",
    tags=TAGS_BASE + ["icon", "glyph", "semantic icon", "composition"],
    features=FEAT_BASE + ["automatic variant glyphs", "custom icon prop", "icon suppression"],
    accessibility=["icon slot always aria-hidden", "meaning carried by role + text", "custom icons stay decorative"],
    interactive=False,
    related=["alert", "alert-info", "alert-success", "alert-rich"],
    usage='''import Alert, {
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from "./alert-with-icon";

// Custom glyph on a neutral alert
<Alert icon={<MyBellIcon />}>
  <AlertTitle>Notifications paused</AlertTitle>
  <AlertDescription>Digest emails resume on Monday.</AlertDescription>
</Alert>

// Icon suppressed
<Alert variant="success" icon={null}>
  <AlertTitle>Saved</AlertTitle>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, ICON_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="The icon is the leading grid column of the root flex row; the text column keeps `min-w-0` so content wraps beside it. `AlertIcon` renders the variant glyph by default and wraps any custom glyph you pass as children (16px, currentColor, `aria-hidden`).",
    logic_doc="""Three icon treatments, all through one prop:

1. **Automatic** — semantic variants (`info`, `success`, `warning`, `destructive`) render their status glyph when `icon` is undefined.
2. **Replaced** — pass any `ReactNode` as `icon` to render a custom glyph in the same slot (demo 1: a bell on a neutral alert; demo 3: a download glyph replacing the success check).
3. **Suppressed** — pass `icon={null}` to remove the slot entirely (demo 2).""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- Custom glyphs rendered through `icon` or `AlertIcon` inherit the same `aria-hidden` slot — an icon never becomes the sole carrier of meaning, so write the message text to stand alone.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The icon slot is 16px and colored by the variant's semantic token (muted for `default`). Pass your own SVG as `icon` — the slot sizes it with `[&_svg]`-free, currentColor-friendly geometry.",
    tsx_header='''/**
 * DevSnips React Alert — Icon composition.
 *
 * The shared alert core; this variant demonstrates the leading icon slot:
 * semantic variants render their status glyph automatically, the `icon`
 * prop replaces it with any ReactNode, and `icon={null}` suppresses it.
 * The slot is always `aria-hidden` — meaning comes from the role + text.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Custom glyph on a neutral alert</p>
        <Alert icon={<Icon name="bell" className="size-4" />}>
          <AlertTitle>Notifications paused</AlertTitle>
          <AlertDescription>
            Digest emails are paused until Monday 09:00. Critical alerts still
            reach the on-call channel.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>Pass any ReactNode as icon — the slot sizes and aligns it.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Icon suppressed</p>
        <Alert variant="success" icon={null}>
          <AlertTitle>Environment variables saved</AlertTitle>
          <AlertDescription>
            4 variables updated. Running services pick them up on the next deploy.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>icon=&#123;null&#125; removes the slot — the text column takes the full width.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Variant glyph replaced</p>
        <Alert variant="success" icon={<Icon name="download" className="size-4" />}>
          <AlertTitle>Usage report ready</AlertTitle>
          <AlertDescription>
            The September export (2.1 MB, CSV) is ready to download from the
            reports page.
          </AlertDescription>
        </Alert>
        <p className={NOTE}>The success tint stays; only the glyph changes.</p>
      </div>
    </div>
  );
}''',
)

# 7. alert-with-action
register(
    "alert-with-action",
    title="Alert with Action",
    subcategory="Composite",
    description="An alert with real action buttons in the `AlertAction` row — for messages that ask the user to do something: upgrade, retry, update billing. Actions are native `<button>` elements and wrap below the text at narrow widths.",
    tags=TAGS_BASE + ["action", "button", "cta", "composite"],
    features=FEAT_BASE + ["wrapping action row", "real buttons", "primary + secondary pairing"],
    accessibility=["real <button> actions", "focus-visible rings", "no nested interactive elements"],
    interactive=True,
    related=["alert-warning", "alert-destructive", "alert-with-link", "alert-rich"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
  AlertAction,
} from "./alert-with-action";

<Alert variant="warning">
  <AlertTitle>Trial ends in 5 days</AlertTitle>
  <AlertDescription>
    Upgrade to keep private projects and audit logs.
  </AlertDescription>
  <AlertAction>
    <button type="button" onClick={upgrade}>Upgrade plan</button>
    <button type="button" onClick={compare}>Compare plans</button>
  </AlertAction>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, ACTION_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="`AlertAction` renders inside the text column below the description (`mt-1.5 flex flex-wrap gap-2`): actions belong to the message's reading flow and wrap instead of overflowing. Pair at most one primary action with one secondary/ghost action — an alert is not a toolbar.",
    logic_doc="""Actions in an alert are real native `<button>` elements — compose them from the DevSnips Buttons family (the demos inline the same classes).

Both demos log their clicks to a live note below the alert, so the behavior is observable: "Upgrade plan" / "Compare plans" on the trial warning, and "Update billing" / "Retry" on the payment failure. Retry is the recoverable path, so it is the outlined secondary action, not the primary.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- Actions are real `<button>` elements with visible labels — no `div` click targets, no icon-only actions without an accessible name.
- Interactive children are siblings inside `AlertAction`, never nested inside the title, description, or each other.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="If the action navigates somewhere, use a real `<a>` instead — see `alert-with-link`. If the action resolves the message, consider making the alert dismissible too — see `alert-dismissible` and `alert-rich`.",
    tsx_header='''/**
 * DevSnips React Alert — Action composition.
 *
 * The shared alert core; this variant demonstrates `AlertAction`: a wrapping
 * row of real `<button>` / `<a>` controls rendered inside the text column
 * below the description. Actions are native controls — never clickable
 * divs — and they wrap instead of overflowing at narrow widths.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const [log, setLog] = React.useState("No actions yet.");
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Trial warning with actions</p>
        <Alert variant="warning">
          <AlertTitle>Trial ends in 5 days</AlertTitle>
          <AlertDescription>
            Upgrade to keep private projects, audit logs, and the 100k request
            quota after the trial ends.
          </AlertDescription>
          <AlertAction>
            <button type="button" className={BTN_PRIMARY_SM} onClick={() => setLog("Clicked: Upgrade plan")}>Upgrade plan</button>
            <button type="button" className={BTN_GHOST_SM} onClick={() => setLog("Clicked: Compare plans")}>Compare plans</button>
          </AlertAction>
        </Alert>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Payment failure with recovery actions</p>
        <Alert variant="destructive">
          <AlertTitle>Payment failed</AlertTitle>
          <AlertDescription>
            The card ending in 4242 was declined. Update the billing details or
            retry the charge before Friday to keep the workspace active.
          </AlertDescription>
          <AlertAction>
            <button type="button" className={BTN_PRIMARY_SM} onClick={() => setLog("Clicked: Update billing")}>Update billing</button>
            <button type="button" className={BTN_OUTLINE_SM} onClick={() => setLog("Clicked: Retry charge")}>Retry charge</button>
          </AlertAction>
        </Alert>
      </div>
      <p className={NOTE} aria-live="polite">{log}</p>
    </div>
  );
}''',
)

# 8. alert-with-link
register(
    "alert-with-link",
    title="Alert with Link",
    subcategory="Composite",
    description="An alert containing real anchors — an inline link inside the description, or a link in the action row. Links navigate, so they are `<a href>` elements with normal browser behavior, never click handlers on text.",
    tags=TAGS_BASE + ["link", "anchor", "navigation", "composite"],
    features=FEAT_BASE + ["real <a href> links", "inline + action-row placement", "hash navigation demo"],
    accessibility=["real anchors (keyboard + screen-reader link semantics)", "focus-visible rings", "underlined, not color alone"],
    interactive=True,
    related=["alert-with-action", "alert-info", "alert-warning"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-with-link";

<Alert variant="info">
  <AlertTitle>API version 2026-08 is now the default</AlertTitle>
  <AlertDescription>
    New keys use the latest version. Read the{" "}
    <a href="/changelog">migration notes</a> before rotating existing keys.
  </AlertDescription>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, DESCRIPTION_PROPS, ACTION_PROPS, TITLE_PROPS]),
    composition_note="Inline links live inside `AlertDescription` text; destination-styled links (view, verify, open) sit in `AlertAction` next to buttons. Both are plain `<a href>` anchors — middle-click, open-in-new-tab, and screen-reader link semantics all work.",
    logic_doc="""Links navigate; buttons act. When the message points at more information (changelog, migration guide, status page), use a real anchor — the first demo links inline from the description, the second places a link in the action row beside a button.

The preview uses `#/...` hash links so navigation is observable without a page reload — the live note below reports the current hash.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- Links use `color.link` plus an underline — destination is never communicated by color alone.
- Anchors keep their native keyboard behavior: Tab to reach, Enter to follow.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Do not style a `<button>` to look like a link for navigation, and do not attach `onClick` navigation to a `<span>` — both break link semantics. If it navigates, it is an `<a>`.",
    tsx_header='''/**
 * DevSnips React Alert — Link composition.
 *
 * The shared alert core; this variant demonstrates real anchors inside an
 * alert: an inline link in the description and a destination link in the
 * action row. Links are `<a href>` elements with normal browser behavior —
 * never click handlers on text.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const [hash, setHash] = React.useState(window.location.hash || "(no hash yet)");
  React.useEffect(() => {
    const on = () => setHash(window.location.hash || "(no hash yet)");
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Inline link in the description</p>
        <Alert variant="info">
          <AlertTitle>API version 2026-08 is now the default</AlertTitle>
          <AlertDescription>
            Keys created after August 1 use the latest version. Read the{" "}
            <a className={LINK} href="#/changelog">migration notes</a> before
            rotating existing keys, or pin a version in{" "}
            <a className={LINK} href="#/settings/api">API settings</a>.
          </AlertDescription>
        </Alert>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Link in the action row</p>
        <Alert variant="warning">
          <AlertTitle>Domain not verified</AlertTitle>
          <AlertDescription>
            docs.example.com is not serving traffic yet. Add the TXT record and
            verify ownership to finish the setup.
          </AlertDescription>
          <AlertAction>
            <a className={LINK} href="#/settings/domains">Open domain settings</a>
            <a className={LINK} href="#/docs/custom-domains">Setup guide</a>
          </AlertAction>
        </Alert>
      </div>
      <p className={NOTE}>Real anchors — current hash: {hash}</p>
    </div>
  );
}''',
)

# 9. alert-dismissible
register(
    "alert-dismissible",
    title="Dismissible Alert",
    subcategory="Behavior",
    description="An alert the user can dismiss: a real close button with an accessible name, controlled (`open` + `onDismiss`) or uncontrolled (`defaultOpen`) state, and focus management that never strands keyboard users when the alert unmounts.",
    tags=TAGS_BASE + ["dismissible", "close", "controlled", "uncontrolled", "focus management"],
    features=FEAT_BASE + ["real close button", "controlled + uncontrolled", "focus relocation on dismiss", "custom close label"],
    accessibility=["close button aria-label", "keyboard-operable dismissal", "focus moves to next operable element", "onDismiss callback"],
    interactive=True,
    related=["alert", "alert-compact", "alert-rich", "alert-live"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-dismissible";

// Uncontrolled
<Alert variant="info" dismissible onDismiss={() => persistDismissal()}>
  <AlertTitle>Usage resets on the 1st</AlertTitle>
  <AlertDescription>Your quota renews each billing cycle.</AlertDescription>
</Alert>

// Controlled
const [open, setOpen] = useState(true);
<Alert
  variant="info"
  dismissible
  open={open}
  onDismiss={() => setOpen(false)}
>
  …
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, CLOSE_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="Set `dismissible` and the root appends a trailing `AlertClose` wired to the alert's dismissal state — no manual wiring. For custom placement, compose `<AlertClose />` yourself (it reads the nearest `Alert` context) and leave `dismissible` off.",
    logic_doc="""Dismissal works in both state modes:

- **Uncontrolled** (demo 1): the alert owns its visibility. Clicking the close button unmounts it and `onDismiss` still fires (persist the dismissal there). The "Reset demo" button remounts it.
- **Controlled** (demo 2): the parent owns `open`. Clicking close fires `onDismiss` and the alert hides only when the parent sets `open={false}` — the event log shows the callback firing.

In both modes the close button is a real `<button type="button">` with an accessible name (`closeLabel` on the root, or `label` on `AlertClose`). Because the focused button unmounts on dismissal, focus first moves to the next operable element in document order — try it: Tab to the close button, press Enter, and focus lands on the control after the alert instead of dropping to `<body>`.""",
    keyboard_doc=KEYBOARD_DISMISS,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- The icon-only close button always carries an accessible name (`"Dismiss alert"` by default; customize with `closeLabel` per message).
- Dismissal moves focus to the next operable element before unmounting — keyboard users never lose their place.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="`AlertClose` supports a veto: call `event.preventDefault()` in a custom `onClick` to stop the dismissal (for example while a save is in flight).",
    tsx_header='''/**
 * DevSnips React Alert — Dismissible.
 *
 * The shared alert core; this variant demonstrates dismissal: the
 * `dismissible` prop appends a real `<AlertClose>` button (accessible name,
 * keyboard-operable), visibility is controlled (`open` + `onDismiss`) or
 * uncontrolled (`defaultOpen`), and focus moves to the next operable
 * element before the alert unmounts.
 */''',
    showcase=DEMO_HELPERS + '''
function UncontrolledDemo() {
  const [instance, setInstance] = React.useState(0);
  const [log, setLog] = React.useState("onDismiss: not called yet.");
  return (
    <div className="space-y-2">
      <p className={LABEL}>Uncontrolled — the alert owns its visibility</p>
      <Alert key={instance} variant="info" dismissible onDismiss={() => setLog("onDismiss fired: alert dismissed (uncontrolled).")}>
        <AlertTitle>Usage resets on the 1st</AlertTitle>
        <AlertDescription>
          Your plan&apos;s request quota renews at the start of each billing
          cycle. This notice dismisses itself — no parent state required.
        </AlertDescription>
      </Alert>
      <div className="flex flex-wrap items-center gap-3">
        <button type="button" className={BTN_OUTLINE_SM} onClick={() => setInstance((n) => n + 1)}>Reset demo</button>
        <p className={NOTE}>{log}</p>
      </div>
      <p className={NOTE}>Tab to the close button and press Enter — focus moves to Reset demo, not to the page body.</p>
    </div>
  );
}

function ControlledDemo() {
  const [open, setOpen] = React.useState(true);
  const [events, setEvents] = React.useState(["(event log empty)"]);
  const record = (msg) => setEvents((prev) => [msg].concat(prev).slice(0, 3));
  return (
    <div className="space-y-2">
      <p className={LABEL}>Controlled — the parent owns open</p>
      <Alert
        variant="info"
        dismissible
        open={open}
        onDismiss={() => { setOpen(false); record("onDismiss → parent set open=false"); }}
        closeLabel="Dismiss deployment message"
      >
        <AlertTitle>Deployment window moved</AlertTitle>
        <AlertDescription>
          The weekly deploy window is now Tuesdays 10:00 UTC. The parent owns
          this alert&apos;s visibility and logs every dismissal.
        </AlertDescription>
      </Alert>
      {!open ? (
        <button type="button" className={BTN_OUTLINE_SM} onClick={() => { setOpen(true); record("show again → open=true"); }}>Show again</button>
      ) : null}
      <p className={NOTE} aria-live="polite">{events[0]}</p>
      <p className={NOTE}>Custom closeLabel: screen readers announce &quot;Dismiss deployment message&quot;.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <UncontrolledDemo />
      <ControlledDemo />
    </div>
  );
}''',
)

# 10. alert-compact
register(
    "alert-compact",
    title="Compact Alert",
    subcategory="Density",
    description="The `size=\"sm\"` density: reduced padding and gaps for dense interfaces — settings panels, inspector sidebars, data-dense admin screens — while keeping the full compound API, roles, and wrapping behavior.",
    tags=TAGS_BASE + ["compact", "dense", "size", "density"],
    features=FEAT_BASE + ["size=sm density", "same compound API", "stacked dense layout"],
    accessibility=["same live-region roles at both densities", "28px close target in compact", "text stays 14px (readable)"],
    interactive=True,
    related=["alert", "alert-dismissible", "alert-info"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-compact";

<Alert variant="info" size="sm">
  <AlertTitle>Autosave is on</AlertTitle>
  <AlertDescription>Changes save every 30 seconds.</AlertDescription>
</Alert>''',
    props_doc="\n\n".join([ALERT_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, CLOSE_PROPS]),
    composition_note="Density is a prop, not a className override: `size=\"sm\"` reduces the root padding/gap and shrinks the close button from 32px to 28px in one consistent step — no utility-class conflicts with the base padding.",
    logic_doc="""`size="sm"` is for dense contexts: settings panels, inspectors, and admin screens where alerts stack. The demos render three compact alerts in a narrow panel — info, success, and warning — plus a compact dismissible alert.

Text stays at body-sm (14px) at both densities: compactness comes from spacing, not from shrinking type below a readable size.""",
    keyboard_doc=KEYBOARD_DISMISS,
    behavior_doc=STATES_BASE + """
- **Compact (`size=\"sm\"`)** — padding 12px/8px and gap 10px (from 16px/12px and 12px); close button 28px (from 32px). Type and roles are unchanged.""",
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Choose the density per surface, not per message urgency — a compact destructive alert is still `role=\"alert\"`.",
    tsx_header='''/**
 * DevSnips React Alert — Compact density.
 *
 * The shared alert core; this variant demonstrates `size="sm"`: reduced
 * padding and gaps for dense interfaces (settings panels, inspectors), with
 * the same compound API, live-region roles, and wrapping behavior. Density
 * is a prop — not a className override — so it never conflicts with the
 * base spacing utilities.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Dense status stack (size=&quot;sm&quot;)</p>
        <div className="max-w-md space-y-2">
          <Alert variant="info" size="sm">
            <AlertTitle>Autosave is on</AlertTitle>
            <AlertDescription>Changes save every 30 seconds.</AlertDescription>
          </Alert>
          <Alert variant="success" size="sm">
            <AlertTitle>Schema validated</AlertTitle>
            <AlertDescription>42 collections checked, no issues found.</AlertDescription>
          </Alert>
          <Alert variant="warning" size="sm">
            <AlertTitle>Cache near capacity</AlertTitle>
            <AlertDescription>Evictions begin at 95% — currently 88%.</AlertDescription>
          </Alert>
        </div>
        <p className={NOTE}>Same API and roles — only the spacing changes.</p>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Compact + dismissible</p>
        <div className="max-w-md">
          <Alert variant="info" size="sm" dismissible>
            <AlertTitle>Keyboard shortcuts updated</AlertTitle>
            <AlertDescription>
              Press ? anywhere to see the new shortcut map.
            </AlertDescription>
          </Alert>
        </div>
        <p className={NOTE}>The compact close button keeps a 28px target and its accessible name.</p>
      </div>
    </div>
  );
}''',
)

# 11. alert-rich
register(
    "alert-rich",
    title="Rich Alert",
    subcategory="Composite",
    description="The full composition: semantic icon, title, description, action row, and a dismiss button working together — the shape for product updates and operational incidents that carry both context and next steps.",
    tags=TAGS_BASE + ["rich", "composite", "actions", "dismissible", "full composition"],
    features=FEAT_BASE + ["icon + title + description + actions + close", "mixed buttons and anchors", "graceful mobile collapse"],
    accessibility=["all primitives in one composition", "registered labelledby/describedby", "close + actions all real controls"],
    interactive=True,
    related=["alert-with-action", "alert-with-link", "alert-dismissible", "alert"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
  AlertAction,
} from "./alert-rich";

<Alert variant="info" dismissible>
  <AlertTitle>New version available</AlertTitle>
  <AlertDescription>
    CLI 2.4.0 adds streaming deploy logs and config validation.
  </AlertDescription>
  <AlertAction>
    <button type="button" onClick={update}>Update now</button>
    <a href="/changelog">Release notes</a>
  </AlertAction>
</Alert>''',
    props_doc=props_table(),
    composition_note="Every primitive in one composition: the variant supplies the icon and role, `AlertTitle` / `AlertDescription` carry the message, `AlertAction` pairs a primary button with a real anchor, and `dismissible` appends the close button. The root flex row keeps the icon and close shrink-wrapped while the text column wraps.",
    logic_doc="""Two complete compositions:

1. **Product update** (info): icon + title + description + Update now (real button) + Release notes (real anchor) + dismiss.
2. **Operational incident** (destructive): icon + title + description with the failing step in mono + Retry deployment (real button) + View build log (real anchor) + dismiss.

At 375px the action row wraps and the close button keeps its place at the top right — the composition degrades gracefully instead of overflowing.""",
    keyboard_doc=KEYBOARD_DISMISS,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- Tab order follows the reading order: actions first (they live in the text column), then the close button — which is also where focus returns from if the alert is not dismissed.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Rich does not mean crowded: one message, at most two actions. If you need more, the content probably wants a card or a dialog instead of an alert.",
    tsx_header='''/**
 * DevSnips React Alert — Rich composition.
 *
 * The shared alert core; this variant demonstrates the full composition:
 * semantic icon + title + description + action row (real buttons and
 * anchors) + a dismiss button. The root flex row keeps the icon and close
 * shrink-wrapped while the text column wraps, so the composition degrades
 * gracefully at narrow widths.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const [log, setLog] = React.useState("No actions yet.");
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Product update</p>
        <Alert variant="info" dismissible onDismiss={() => setLog("Dismissed: version notice")}>
          <AlertTitle>CLI 2.4.0 is available</AlertTitle>
          <AlertDescription>
            Streaming deploy logs, config validation before push, and a faster
            project switcher. Installs alongside your current version.
          </AlertDescription>
          <AlertAction>
            <button type="button" className={BTN_PRIMARY_SM} onClick={() => setLog("Clicked: Update now")}>Update now</button>
            <a className={LINK} href="#/changelog">Release notes</a>
          </AlertAction>
        </Alert>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Operational incident</p>
        <Alert variant="destructive" dismissible onDismiss={() => setLog("Dismissed: incident alert")}>
          <AlertTitle>Deployment to production failed</AlertTitle>
          <AlertDescription>
            Build #482 exited with code 1 in step{" "}
            <code className="rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-surface-active)] px-1 py-0.5 font-mono text-[12px] text-[var(--ds-color-foreground)]">test:integration</code>.
            The previous release is still serving traffic.
          </AlertDescription>
          <AlertAction>
            <button type="button" className={BTN_PRIMARY_SM} onClick={() => setLog("Clicked: Retry deployment")}>Retry deployment</button>
            <a className={LINK} href="#/builds/482">View build log</a>
          </AlertAction>
        </Alert>
      </div>
      <p className={NOTE} aria-live="polite">{log}</p>
    </div>
  );
}''',
)

# 12. alert-live
register(
    "alert-live",
    title="Live-Region Alert",
    subcategory="Behavior",
    description="Dynamic application feedback done right: alerts mounted on the event announce through their role — `role=\"status\"` politely for outcomes, `role=\"alert\"` assertively for failures — with one live region per message so nothing is announced twice.",
    tags=TAGS_BASE + ["live region", "aria-live", "async", "status", "dynamic"],
    features=FEAT_BASE + ["mount-on-event announcements", "polite vs assertive roles", "no duplicate announcements"],
    accessibility=["role-driven live regions", "single region per message", "static contrast with role={null}"],
    interactive=True,
    related=["alert-success", "alert-destructive", "alert-dismissible", "alert"],
    usage='''import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-live";

const [result, setResult] = useState(null);

async function save() {
  await api.save(settings);
  // Mount the alert when the event happens — the role announces it.
  setResult({ variant: "success", title: "Settings saved" });
}

{result ? (
  <Alert variant={result.variant}>
    <AlertTitle>{result.title}</AlertTitle>
  </Alert>
) : null}''',
    props_doc="\n\n".join([ALERT_PROPS, TITLE_PROPS, DESCRIPTION_PROPS]),
    composition_note="No extra primitives: live-region behavior comes from the role the variant already carries. The pattern is *where* the alert mounts — conditionally, on the event — not a new component.",
    logic_doc="""A live region announces when **content changes inside it**. The reliable pattern is to mount the alert when the event happens: the role (`status` or `alert`) makes the insertion an announcement. Do not pre-render a hidden alert and toggle visibility — a region that exists but is hidden behaves inconsistently across screen readers.

Demo 1 runs a fake async save: "Save settings" resolves into a `role="status"` success alert (polite), "Simulate failure" resolves into a `role="alert"` destructive alert (assertive). One alert node exists at a time, so each event produces exactly one announcement — nesting `aria-live` wrappers around an alert would announce it twice.

Demo 2 is the contrast case: an always-visible project note with `role={null}`. It is static content, so it announces nothing — which is correct.""",
    keyboard_doc=KEYBOARD_STATIC,
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE + """
- Mount-on-event gives one announcement per event; a new event replaces the alert node, which re-announces with the new content.
- Never wrap an `Alert` in another `aria-live` container — nested live regions cause duplicate announcements.""",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="If the alert appears near the control that triggered it, sighted users get the spatial connection for free; screen-reader users get the announcement — you do not need to move focus to the alert (and should not, unless it contains required actions).",
    tsx_header='''/**
 * DevSnips React Alert — Live-region pattern.
 *
 * The shared alert core; this variant demonstrates dynamic feedback: alerts
 * mounted on the event announce through their role — `role="status"`
 * (polite) for outcomes, `role="alert"` (assertive) for failures. Mount
 * conditionally instead of toggling a pre-rendered node, keep one live
 * region per message, and never nest `aria-live` wrappers — that is what
 * causes duplicate announcements.
 */''',
    showcase=DEMO_HELPERS + '''
function LiveSaveDemo() {
  const [state, setState] = React.useState({ status: "idle", variant: null, title: "" });
  const timer = React.useRef(null);
  React.useEffect(() => () => clearTimeout(timer.current), []);
  function run(kind) {
    clearTimeout(timer.current);
    setState({ status: "saving", variant: null, title: "" });
    timer.current = setTimeout(() => {
      if (kind === "fail") {
        setState({ status: "done", variant: "destructive", title: "Settings could not be saved" });
      } else {
        setState({ status: "done", variant: "success", title: "Settings saved" });
      }
    }, 600);
  }
  return (
    <div className="space-y-2">
      <p className={LABEL}>Async save feedback — mounted on the event</p>
      <div className="flex flex-wrap gap-2">
        <button type="button" className={BTN_OUTLINE_SM} disabled={state.status === "saving"} onClick={() => run("ok")}>Save settings</button>
        <button type="button" className={BTN_GHOST_SM} disabled={state.status === "saving"} onClick={() => run("fail")}>Simulate failure</button>
      </div>
      <div className="min-h-[52px]">
        {state.status === "saving" ? (
          <p className={NOTE}>Saving…</p>
        ) : null}
        {state.variant ? (
          <Alert variant={state.variant}>
            <AlertTitle>{state.title}</AlertTitle>
            <AlertDescription>
              {state.variant === "success"
                ? "Notification rules and the weekly digest preference were updated."
                : "The server rejected the change (409 Conflict). Your previous settings are still active."}
            </AlertDescription>
          </Alert>
        ) : null}
      </div>
      <p className={NOTE}>Success mounts with role=&quot;status&quot; (polite); failure mounts with role=&quot;alert&quot; (assertive). One node per event — announced exactly once.</p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <LiveSaveDemo />
      <div className="space-y-2">
        <p className={LABEL}>Contrast: static content announces nothing</p>
        <Alert role={null}>
          <AlertTitle>Project created on March 3</AlertTitle>
          <AlertDescription>
            This note is part of the page, not an event — role=&#123;null&#125;
            keeps it out of the live region.
          </AlertDescription>
        </Alert>
      </div>
    </div>
  );
}''',
)
