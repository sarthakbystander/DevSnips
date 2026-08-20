"""Registry for the DevSnips React Tabs generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs.
The generator (``_gen_react_tabs.py``) reads each component's ``code.tsx``
from disk and combines it with the spec here to write ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented content only (Overview, Activity, Files,
Settings, Comments, Deployments, Members, Security). No lorem ipsum, no
marketing buzzwords.
"""
from _gen_react_tabs import register

FEAT = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic tab roles", "roving tabIndex", "keyboard navigation"]
A11Y = ["tablist / tab / tabpanel roles", "aria-selected", "aria-controls", "aria-labelledby", "roving tabIndex", "Home / End support", "focus-visible"]

TAGS_BASE = ["tabs", "navigation", "tablist", "tabpanel", "react", "tailwind", "accessible", "interactive", "keyboard", "responsive"]

# Shared props tables. TabsTrigger/Content carry the same API family-wide.
TABS_PROPS = r"""### `<Tabs>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` | — | Selected tab value (controlled). |
| `defaultValue` | `string` | — | Initial selected value (uncontrolled). |
| `onValueChange` | `(value: string) => void` | — | Selection callback. |
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Arrow-key navigation axis + layout. |
| `className` | `string` | — | Extra classes on the root. |
| `children` | `ReactNode` | — | `TabsList` + `TabsContent` composition. |"""

LIST_PROPS = """### `<TabsList>`

| Name | Type | Default | Description |
|---|---|---|---|
| `aria-label` | `string` | — | Group label for the tablist (recommended). |
| `className` | `string` | — | Extra classes on the tablist. |
| `children` | `ReactNode` | — | `TabsTrigger` elements. |"""

TRIGGER_PROPS = """### `<TabsTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` (required) | — | Value this trigger selects; associates it with its panel. |
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered `aria-hidden`). |
| `badge` | `ReactNode` | — | Small contextual chip after the label. |
| `count` | `number` | — | Numeric chip after the label. |
| `disabled` | `boolean` | `false` | Prevents activation; skipped by key navigation. |
| `className` | `string` | — | Extra classes on the trigger. |
| `children` | `ReactNode` | — | Visible label. |"""

CONTENT_PROPS = """### `<TabsContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` (required) | — | Matches the owning `TabsTrigger`. |
| `className` | `string` | — | Extra classes on the panel. |
| `children` | `ReactNode` | — | Panel content. |"""

ADD_ACTION_PROPS = """### `<TabsAddAction>`

| Name | Type | Default | Description |
|---|---|---|---|
| `aria-label` | `string` (required) | — | Accessible name for the action. |
| `onClick` | `(event) => void` | — | Click callback. |
| `disabled` | `boolean` | `false` | Disables the action. |
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Custom icon/content (defaults to the built-in plus icon). |"""


def props_table(extra=None):
    parts = [TABS_PROPS, LIST_PROPS, TRIGGER_PROPS, CONTENT_PROPS]
    if extra:
        parts.append(extra)
    return "\n\n".join(parts)


# Panel-text and note classes used inside the previews (Tailwind arbitrary
# values, no extra CSS).
P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]"
NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]"

# 1. tabs (reference)
register(
    "tabs",
    title="Tabs",
    subcategory="Core",
    description="Accessible navigation tabs implemented as a compound component with controlled and uncontrolled selection.",
    tags=TAGS_BASE,
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["tabs-underline", "tabs-contained", "tabs-with-panel", "tabs-vertical"],
    props_doc={
        "usage": '''import Tabs, { TabsList, TabsTrigger, TabsContent } from "./tabs";

const [value, setValue] = useState("activity");

<Tabs value={value} onValueChange={setValue}>
  <TabsList aria-label="Project navigation">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">…</TabsContent>
  <TabsContent value="activity">…</TabsContent>
  <TabsContent value="settings">…</TabsContent>
</Tabs>

// Uncontrolled:
<Tabs defaultValue="overview">…</Tabs>''',
        "table": props_table(),
    },
    composition_note="This is the reference composition — every other variant in the family uses the same four primitives and only changes the treatment constants or layout.",
    behavior_doc="""- **Selected** — subtle `--ds-color-surface-active` background with foreground text.
- **Idle** — muted foreground; hover shifts onto `--ds-color-surface-hover`.
- **Focus-visible** — `--ds-color-focus-ring` outline in both themes.
- **Disabled** — native `disabled`; reduced opacity and removed from the tab order.""",
    a11y_doc="Give the tablist an `aria-label` when more than one tablist lives on a page. The active state is never color alone — background and font change together.",
    notes_doc="Reference implementation for the Tabs family. It establishes the shared tab height (36px), radius, typography, spacing, focus ring, panel spacing, and the controlled/uncontrolled selection model that every other variant extends.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("activity");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Project navigation">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
          <TabsTrigger value="files">Files</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>
        <TabsContent value="overview"><p className={P}>Project health is nominal — the last two milestones reached the main branch on schedule.</p></TabsContent>
        <TabsContent value="activity"><p className={P}>14 events in the last 24 hours: two deployments, nine comments, and one member invite.</p></TabsContent>
        <TabsContent value="files"><p className={P}>8 tracked files. index.html changed most recently.</p></TabsContent>
        <TabsContent value="settings"><p className={P}>Notification, access, and billing preferences for this project.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>Controlled via <code>value</code> + <code>onValueChange</code> — current value: <code>{value}</code>. Click a tab or use Arrow keys, Home, and End.</p>
      <Tabs defaultValue="comments">
        <TabsList aria-label="Document navigation">
          <TabsTrigger value="comments">Comments</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
        </TabsList>
        <TabsContent value="comments"><p className={P}>Three open threads to review before Friday's review.</p></TabsContent>
        <TabsContent value="history"><p className={P}>Last published on June 12. Two earlier drafts are archived.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>Uncontrolled via <code>defaultValue</code>.</p>
    </div>
  );
}""",
)

# 2. tabs-with-icons
register(
    "tabs-with-icons",
    title="Tabs With Icons",
    subcategory="Content",
    description="Tabs with optional meaningful leading icons rendered aria-hidden.",
    tags=TAGS_BASE + ["icon"],
    features=FEAT,
    accessibility=A11Y + ["icon aria-hidden"],
    interactive=True,
    related=["tabs", "tabs-with-badge", "tabs-with-count"],
    props_doc={
        "usage": '''<Tabs defaultValue="downloads">
  <TabsList aria-label="Account sections">
    <TabsTrigger value="downloads" icon={<DownloadIcon />}>Downloads</TabsTrigger>
    <TabsTrigger value="members" icon={<UserIcon />}>Members</TabsTrigger>
    <TabsTrigger value="settings" icon={<SettingsIcon />}>Settings</TabsTrigger>
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="Icons are optional ReactNode content passed through `icon` — nothing requires an icon library; pass any element, for example an inline svg.",
    behavior_doc="""Same selected / idle / focus / disabled states as the reference tabs. The icon inherits the trigger's text color, so it follows selected and idle states automatically.""",
    a11y_doc="Icons are wrapped in an `aria-hidden` span — they carry meaning only as a visual aid; the text label remains the accessible name. Never add decorative icons that duplicate the label.",
    notes_doc="Use icons when each section has a clear glyph (Downloads, Members, Settings). Skip the icon otherwise — optical consistency matters more than filling every tab.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("downloads");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Account sections">
          <TabsTrigger value="downloads" icon={<Icon name="download" />}>Downloads</TabsTrigger>
          <TabsTrigger value="notifications" icon={<Icon name="bell" />}>Notifications</TabsTrigger>
          <TabsTrigger value="members" icon={<Icon name="user" />}>Members</TabsTrigger>
          <TabsTrigger value="settings" icon={<Icon name="settings" />}>Settings</TabsTrigger>
        </TabsList>
        <TabsContent value="downloads"><p className={P}>Two export jobs finished overnight. The largest report is 48 MB.</p></TabsContent>
        <TabsContent value="notifications"><p className={P}>Email digests are on. Push alerts are muted while you are out of office.</p></TabsContent>
        <TabsContent value="members"><p className={P}>9 members have workspace access. Two invitations are pending.</p></TabsContent>
        <TabsContent value="settings"><p className={P}>Profile, security, and integration preferences for this account.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>Icons are optional ReactNode content — each communicates the section's meaning and is rendered <code>aria-hidden</code>.</p>
    </div>
  );
}""",
)

# 3. tabs-with-badge
register(
    "tabs-with-badge",
    title="Tabs With Badge",
    subcategory="Content",
    description="Tabs with a small contextual badge (New, Beta) that stays secondary to the label.",
    tags=TAGS_BASE + ["badge"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["tabs", "tabs-with-count", "tabs-with-icons"],
    props_doc={
        "usage": '''<Tabs defaultValue="activity">
  <TabsList aria-label="Product sections">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity" badge="New">Activity</TabsTrigger>
    <TabsTrigger value="reports" badge="Beta">Reports</TabsTrigger>
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="The badge is a text chip passed through `badge` — useful for rollout flags like New or Beta, not for decoration.",
    behavior_doc="""Same selected / idle / focus / disabled states as the reference tabs. The badge chip uses the accent tokens at a small size so it never overrides the label.""",
    a11y_doc="Badge text is part of the trigger's accessible name, so keep it short and meaningful. It is not color alone — the text communicates the state.",
    notes_doc="Use for temporal rollout hints (New, Beta). For numeric information prefer tabs-with-count.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("activity");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Product sections">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="activity" badge="New">Activity</TabsTrigger>
          <TabsTrigger value="reports" badge="Beta">Reports</TabsTrigger>
        </TabsList>
        <TabsContent value="overview"><p className={P}>Campaign reach is up 12% week over week.</p></TabsContent>
        <TabsContent value="activity"><p className={P}>The real-time event stream shipped this week — every member can join it from this screen.</p></TabsContent>
        <TabsContent value="reports"><p className={P}>Beta reports add cohort retention and funnel drop-off to the standard rollup.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>Badges stay secondary to the label — text, not color alone, communicates the flag.</p>
    </div>
  );
}""",
)

# 4. tabs-with-count
register(
    "tabs-with-count",
    title="Tabs With Count",
    subcategory="Content",
    description="Tabs with meaningful numeric counts rendered as bordered chips with tabular figures.",
    tags=TAGS_BASE + ["count"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["tabs", "tabs-with-badge", "tabs-with-icons"],
    props_doc={
        "usage": '''<Tabs defaultValue="comments">
  <TabsList aria-label="Discussion sections">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="comments" count={12}>Comments</TabsTrigger>
    <TabsTrigger value="files" count={8}>Files</TabsTrigger>
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="Pass a real number through `count` — the chip stays readable at row level with tabular figures and never shifts layout as digits change.",
    behavior_doc="""Same selected / idle / focus / disabled states as the reference tabs. The count chip is a bordered pill with `tabular-nums` figures, so it stays visible on the selected background.""",
    a11y_doc="The count sits inside the trigger, so it joins the accessible name (e.g. \"Comments 12\"). Keep counts honest — no padded statistics.",
    notes_doc="Use only when the number answers a real question (open comments, tracked files). Non-numeric markers belong in tabs-with-badge.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("comments");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Discussion sections">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="comments" count={12}>Comments</TabsTrigger>
          <TabsTrigger value="files" count={8}>Files</TabsTrigger>
        </TabsList>
        <TabsContent value="overview"><p className={P}>Q3 revenue is tracking 8% above plan with no open blockers.</p></TabsContent>
        <TabsContent value="comments"><p className={P}>12 open comments. Three threads are awaiting a reply from the design group.</p></TabsContent>
        <TabsContent value="files"><p className={P}>8 tracked files taking 86 MB. The archive exports nightly.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>Counts are real numbers rendered with tabular figures — they stay readable when selected and never cause layout shift.</p>
    </div>
  );
}""",
)

# 5. tabs-underline
register(
    "tabs-underline",
    title="Tabs (Underline)",
    subcategory="Core",
    description="Tabs with a restrained 2px underline active indicator over the shared border.",
    tags=TAGS_BASE + ["underline"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["tabs", "tabs-contained", "tabs-vertical"],
    props_doc={
        "usage": '''<Tabs defaultValue="overview">
  <TabsList aria-label="Workspace navigation">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
    <TabsTrigger value="comments">Comments</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="The underline treatment differs only in its class constants — the list carries the shared bottom border and the selected trigger overlays it with a 2px primary rule (`-mb-px` alignment).",
    behavior_doc="""- **Selected** — 2px `--ds-color-primary` underline + foreground text (weight and border, not color alone).
- **Idle** — transparent underline; hover reveals `--ds-color-border-strong`.
- **Focus-visible** — `--ds-color-focus-ring` outline.
- **Disabled** — native `disabled`; reduced opacity and removed from the tab order.""",
    a11y_doc="The underline is a border indicator — supported by text weight change on select, so state never depends on color alone.",
    notes_doc="The wrap-tolerant underline variant. Because the list border is shared, wrapped rows keep a consistent baseline.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("overview");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Workspace navigation">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
          <TabsTrigger value="comments">Comments</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>
        <TabsContent value="overview"><p className={P}>Sprint 18 closes Friday with 42 points delivered and two cards in review.</p></TabsContent>
        <TabsContent value="activity"><p className={P}>9 events today — three deployments from the api workspace.</p></TabsContent>
        <TabsContent value="comments"><p className={P}>5 open comment threads across two documents.</p></TabsContent>
        <TabsContent value="settings"><p className={P}>Workspace preferences: region, locale, and notification defaults.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>Selected tab = 2px primary underline over the shared list border. Tolerates wrapping on narrow screens.</p>
    </div>
  );
}""",
)

# 6. tabs-contained
register(
    "tabs-contained",
    title="Tabs (Contained)",
    subcategory="Core",
    description="Tabs whose tablist sits in a restrained bordered container; the selected tab lifts onto the surface token.",
    tags=TAGS_BASE + ["contained"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["tabs", "tabs-underline", "tabs-vertical"],
    props_doc={
        "usage": '''<Tabs defaultValue="preview">
  <TabsList aria-label="Deployment views">
    <TabsTrigger value="preview">Preview</TabsTrigger>
    <TabsTrigger value="commits">Commits</TabsTrigger>
    <TabsTrigger value="checks">Checks</TabsTrigger>
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="The list is wrapped in a bordered, padded surface; the selected tab sits on `--ds-color-surface` with a hairline shadow. Only the treatment constants change.",
    behavior_doc="""- **Selected** — `--ds-color-surface` background + `--ds-shadow-xs` hairline shadow.
- **Idle** — muted foreground; hover shifts text only.
- **Focus-visible** — `--ds-color-focus-ring` outline.
- **Disabled** — native `disabled`; reduced opacity and removed from the tab order.""",
    a11y_doc="Same structural semantics as the reference tabs — the visual container changes nothing for assistive technology.",
    notes_doc="Pick contained when the tablist should read as one grouped control — for dense toolbars. The container is deliberately quiet; avoid pill-styled segmented treatments elsewhere.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("preview");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Deployment views">
          <TabsTrigger value="preview">Preview</TabsTrigger>
          <TabsTrigger value="commits">Commits</TabsTrigger>
          <TabsTrigger value="checks">Checks</TabsTrigger>
        </TabsList>
        <TabsContent value="preview"><p className={P}>The branch preview is live — last published 12 minutes ago by the deploy queue.</p></TabsContent>
        <TabsContent value="commits"><p className={P}>3 commits ahead of main. The oldest one updates the pricing page copy.</p></TabsContent>
        <TabsContent value="checks"><p className={P}>14 checks passing, 1 skipped (visual review is manual on this branch).</p></TabsContent>
      </Tabs>
      <p className={NOTE}>The tablist reads as one grouped control; the selected tab lifts onto the surface token.</p>
    </div>
  );
}""",
)

# 7. tabs-vertical
register(
    "tabs-vertical",
    title="Tabs (Vertical)",
    subcategory="Layout",
    description="Vertical tablist for settings and multi-pane navigation; arrow keys follow the vertical axis.",
    tags=TAGS_BASE + ["vertical", "layout"],
    features=FEAT,
    accessibility=A11Y + ["aria-orientation"],
    interactive=True,
    related=["tabs", "tabs-underline", "tabs-scrollable"],
    props_doc={
        "usage": '''<Tabs orientation="vertical" defaultValue="general">
  <TabsList aria-label="Settings sections">
    <TabsTrigger value="general">General</TabsTrigger>
    <TabsTrigger value="security">Security</TabsTrigger>
    <TabsTrigger value="notifications">Notifications</TabsTrigger>
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="Set `orientation=\"vertical\"` on `Tabs` — the list switches to a column and the panel takes the remaining width. Below `sm` the list stacks above the panel at full width.",
    behavior_doc="""Same selected / idle / focus / disabled states as the reference tabs, rotated to a column. `aria-orientation=\"vertical\"` is rendered on the tablist automatically.""",
    a11y_doc="Vertical tabs use ArrowUp / ArrowDown; Home and End still work. `aria-orientation=\"vertical\"` is announced on the tablist so screen readers present the pattern correctly.",
    notes_doc="Use for settings and multi-pane preferences. Fixed width (224px at sm+) keeps the panel from being squeezed.",
    showcase="""function Showcase() {
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 720}}>
      <Tabs orientation="vertical" defaultValue="general">
        <TabsList aria-label="Settings sections">
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>
        <TabsContent value="general"><p className={P}>Workspace name, region, and default locale. These apply to every member.</p></TabsContent>
        <TabsContent value="security"><p className={P}>Two-factor enforcement is on for all 9 members. Sessions expire after 30 days.</p></TabsContent>
        <TabsContent value="notifications"><p className={P}>Digest emails ship every weekday at 09:00 UTC. Mentions always come through.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>ArrowUp / ArrowDown move between tabs; the layout stacks the list above the panel below <code>sm</code>.</p>
    </div>
  );
}""",
)

# 8. tabs-scrollable
register(
    "tabs-scrollable",
    title="Tabs (Scrollable)",
    subcategory="Layout",
    description="Horizontal tabs that scroll when the tablist exceeds the available width, without losing keyboard access.",
    tags=TAGS_BASE + ["scrollable", "overflow"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["tabs", "tabs-vertical", "tabs-with-add-action"],
    props_doc={
        "usage": '''<Tabs defaultValue="overview">
  <TabsList aria-label="Project sections">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
    …
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="The tablist carries `overflow-x-auto` with the scrollbar suppressed (`scrollbar-width:none` + webkit pseudo-element). No scroll buttons are needed — Arrow keys bring the focused tab into view.",
    behavior_doc="""Same selected / idle / focus / disabled states as the reference tabs. The list scrolls horizontally instead of wrapping; labels are never truncated. Focusing a tab (mouse or keyboard) scrolls it into view natively.""",
    a11y_doc="Keyboard navigation is unaffected by the scroll — focus happens first and the browser brings the focused tab into view. The suppressed scrollbar only affects the visual chrome.",
    notes_doc="Use when the section list legitimately outgrows the viewport (many categories). Prefer fewer tabs or the vertical treatment when you can restructure.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("overview");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  const items = [
    ["overview", "Overview", "Sprint summary for the current iteration."],
    ["activity", "Activity", "9 events today across two workspaces."],
    ["files", "Files", "8 tracked files. index.html changed most recently."],
    ["comments", "Comments", "3 open comment threads to review."],
    ["deployments", "Deployments", "Last deploy shipped 22 minutes ago."],
    ["members", "Members", "9 active members, two pending invites."],
    ["security", "Security", "Two-factor is on; sessions expire in 30 days."],
    ["integrations", "Integrations", "CI webhook and the issue tracker are connected."],
    ["billing", "Billing", "Invoices settle on the first of each month."],
    ["settings", "Settings", "Workspace preferences and defaults."],
  ];
  return (
    <div className="w-full space-y-6" style={{maxWidth: 520}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Project sections">
          {items.map(([v, label]) => <TabsTrigger key={v} value={v}>{label}</TabsTrigger>)}
        </TabsList>
        {items.map(([v, label, body]) => (
          <TabsContent key={v} value={v}><p className={P}>{body}</p></TabsContent>
        ))}
      </Tabs>
      <p className={NOTE}>The list scrolls horizontally with a suppressed scrollbar — Arrow keys still bring the focused tab into view.</p>
    </div>
  );
}""",
)

# 9. tabs-disabled
register(
    "tabs-disabled",
    title="Tabs (Disabled)",
    subcategory="States",
    description="Tabs with disabled entries that cannot activate, stay out of the tab order, and are skipped by arrow keys.",
    tags=TAGS_BASE + ["disabled", "states"],
    features=FEAT,
    accessibility=A11Y + ["disabled semantics"],
    interactive=True,
    related=["tabs", "tabs-contained", "tabs-scrollable"],
    props_doc={
        "usage": '''<Tabs defaultValue="activity">
  <TabsList aria-label="Workspace navigation">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
    <TabsTrigger value="settings" disabled>Settings</TabsTrigger>
    <TabsTrigger value="billing" disabled>Billing</TabsTrigger>
  </TabsList>
  …
</Tabs>''',
        "table": props_table(),
    },
    composition_note="Mark entries with `disabled` — the trigger renders a native disabled `<button>` and the arrow-key handler filters it out of the navigation set.",
    behavior_doc="""- **Disabled** — `disabled:opacity-50` + `pointer-events-none`; cannot be activated.
- Keyboard navigation skips disabled entries entirely.
- Native `disabled` also removes the tab from the tab order (it never receives focus).""",
    a11y_doc="Native `disabled` <button> semantics — screen readers announce the tab as unavailable. Arrow keys filter it out, so there is no dead stop while navigating.",
    notes_doc="Pair disabled with a real reason (e.g. an admin-only section). If every sibling is disabled, provide context elsewhere on the page.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("activity");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Workspace navigation">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
          <TabsTrigger value="settings" disabled>Settings</TabsTrigger>
          <TabsTrigger value="billing" disabled>Billing</TabsTrigger>
        </TabsList>
        <TabsContent value="overview"><p className={P}>Workspace rollup: revenue, reach, and retention by week.</p></TabsContent>
        <TabsContent value="activity"><p className={P}>14 events in the last 24 hours.</p></TabsContent>
        <TabsContent value="settings"><p className={P}>Settings are admin-only on this workspace.</p></TabsContent>
        <TabsContent value="billing"><p className={P}>Billing is handled by the org owner.</p></TabsContent>
      </Tabs>
      <p className={NOTE}>Two entries are disabled — native <code>disabled</code> blocks activation, arrow keys skip them, and they never land in the tab order.</p>
    </div>
  );
}""",
)

# 10. tabs-with-panel
register(
    "tabs-with-panel",
    title="Tabs With Panel",
    subcategory="Composite",
    description="Complete tabs + panel composition with realistic content; panels stay mounted and toggle via hidden.",
    tags=TAGS_BASE + ["panel", "content"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["tabs", "tabs-underline", "tabs-with-add-action"],
    props_doc={
        "usage": '''<Tabs defaultValue="overview">
  <TabsList aria-label="Sprint views">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
    <TabsTrigger value="files">Files</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">…</TabsContent>
  <TabsContent value="activity">…</TabsContent>
  <TabsContent value="files">…</TabsContent>
</Tabs>''',
        "table": props_table(),
    },
    composition_note="Panels are the quiet half of the pattern: association is automatic (`value` on trigger and content must match) and every panel stays mounted. Inactive panels carry `hidden`, so interface state inside a panel is preserved.",
    behavior_doc="""Every `TabsContent` renders immediately; the inactive ones are hidden with the `hidden` attribute. There is no mount/unmount lifecycle — form inputs and scroll positions inside a panel survive switching tabs.""",
    a11y_doc="Each panel is labeled by its trigger via `aria-labelledby` and stays focusable (`tabIndex={0}`) so scrollable panel content remains reachable from the keyboard.",
    notes_doc="Use this as the full composition example. The variant's README documents the mounted-with-hidden panel behavior in detail.",
    showcase="""function Showcase() {
  const [value, setValue] = React.useState("overview");
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  const H = "m-0 text-sm leading-5 font-medium text-[var(--ds-color-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <TabsList aria-label="Sprint views">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
          <TabsTrigger value="files">Files</TabsTrigger>
        </TabsList>
        <TabsContent value="overview">
          <div className="space-y-2">
            <p className={H}>Sprint 18</p>
            <p className={P}>38 of 42 points delivered. Two cards moved to review; one is blocked on API approval.</p>
          </div>
        </TabsContent>
        <TabsContent value="activity">
          <ul className="m-0 space-y-1 pl-5 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
            <li>Deploy job #112 finished in 41s.</li>
            <li>Aria opened 2 comment threads on the pricing page.</li>
            <li>Bill joined the workspace as an editor.</li>
          </ul>
        </TabsContent>
        <TabsContent value="files">
          <div className="space-y-1 font-mono text-xs leading-5 text-[var(--ds-color-muted-foreground)]">
            <div>index.html — 12 KB</div>
            <div>assets/style.css — 48 KB</div>
            <div>assets/app.js — 96 KB</div>
          </div>
        </TabsContent>
      </Tabs>
      <p className={NOTE}>All three panels stay mounted — inactive ones carry the <code>hidden</code> attribute, so panel state is preserved.</p>
    </div>
  );
}""",
)

# 11. tabs-with-add-action
register(
    "tabs-with-add-action",
    title="Tabs With Add Action",
    subcategory="Composite",
    description="Tabs plus a separate add action rendered outside the tablist with a required accessible label.",
    tags=TAGS_BASE + ["add", "action"],
    features=FEAT,
    accessibility=A11Y + ["separate action button"],
    interactive=True,
    related=["tabs", "tabs-with-panel", "tabs-scrollable"],
    props_doc={
        "usage": '''<Tabs defaultValue="projects">
  <div className="flex items-start gap-2">
    <TabsList aria-label="Workspace views">
      <TabsTrigger value="projects">Projects</TabsTrigger>
      <TabsTrigger value="archived">Archived</TabsTrigger>
    </TabsList>
    <TabsAddAction aria-label="Add a project" onClick={addProject} />
  </div>
  <TabsContent value="projects">…</TabsContent>
  <TabsContent value="archived">…</TabsContent>
</Tabs>''',
        "table": props_table(ADD_ACTION_PROPS),
    },
    composition_note="`TabsAddAction` is a plain button rendered next to the tablist inside a flex row — it is not part of the tablist, so Arrow keys never land on it and its `aria-label` is required by the type.",
    behavior_doc="""- The add action is a real `<button>` outside `role="tablist"` — tab semantics are untouched.
- It shares the trigger's 36px height, radius, border, and focus ring, so the row reads as one system.
- In the demo, clicking it appends a new tab and selects it.""",
    a11y_doc="The button requires an `aria-label` (enforced by the prop type) because it is icon-only. It is reachable by normal Tab focus without entering the tablist's arrow-key interaction.",
    notes_doc="Compose the row with flexbox so the add action sits beside the list, as in the usage example. Disable it with `disabled` like any other control.",
    showcase="""function Showcase() {
  const initial = [
    { value: "projects", label: "Projects", body: "12 active projects, 3 with a pending review." },
    { value: "archived", label: "Archived", body: "Two projects archived this quarter. Restore them from Workspace settings." },
  ];
  const [tabs, setTabs] = React.useState(initial);
  const [value, setValue] = React.useState("projects");
  const n = React.useRef(initial.length);
  function addProject() {
    n.current += 1;
    const id = "project-" + n.current;
    const entry = { value: id, label: "Project " + n.current, body: "Created from the add action. Rename it from Workspace settings when ready." };
    setTabs((t) => t.concat(entry));
    setValue(id);
  }
  const P = "m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
  const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
  return (
    <div className="w-full space-y-6" style={{maxWidth: 560}}>
      <Tabs value={value} onValueChange={setValue}>
        <div className="flex items-start gap-2">
          <TabsList aria-label="Workspace views">
            {tabs.map((t) => <TabsTrigger key={t.value} value={t.value}>{t.label}</TabsTrigger>)}
          </TabsList>
          <TabsAddAction aria-label="Add a project" onClick={addProject} />
        </div>
        {tabs.map((t) => (
          <TabsContent key={t.value} value={t.value}><p className={P}>{t.body}</p></TabsContent>
        ))}
      </Tabs>
      <p className={NOTE}>The + button is a real button rendered outside the tablist — Arrow keys never land on it and its accessible label is required.</p>
    </div>
  );
}""",
)
