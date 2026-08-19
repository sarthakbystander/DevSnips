"""Registry for the DevSnips React Switches generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs.
The generator (``_gen_react_switches.py``) reads each component's ``code.tsx``
from disk and combines it with the spec here to write ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented content only (Email notifications, Security
alerts, Two-factor authentication, Cloud backup, Analytics, Developer mode).
No lorem ipsum, no marketing buzzwords.
"""
from _gen_react_switches import register

FEAT = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic HTML", "keyboard accessible", "native form control"]
A11Y = ["focus-visible", "keyboard accessible", "semantic HTML", "native input + role=switch", "associated labels", "ARIA"]

# Shared props table for the base switch control.
BASE_PROPS = """| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` / `value` | `string` | — | Native form name/value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |"""

# 1. switch (reference)
register(
    "switch",
    title="Switch",
    subcategory="Core",
    description="Native switch styled to the DevSnips select/input visual language with controlled and uncontrolled modes.",
    tags=["switch", "toggle", "form", "control", "settings", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch-with-label", "switch-group", "switch-card", "switch-disabled"],
    props_doc={
        "export_name": "Switch",
        "usage": '<Switch label="Email notifications" defaultChecked />',
        "table": BASE_PROPS,
    },
    behavior_doc="A native `<input type=\"checkbox\" role=\"switch\">` styled with Tailwind + the `--ds-*` semantic tokens. The thumb position tracks the tracked `isChecked` state; controlled (`checked`/`onChange`) and uncontrolled (`defaultChecked`) modes are both supported. A switch is an immediate binary setting — it takes effect the moment it toggles.",
    a11y_doc="Real `<input type=\"checkbox\" role=\"switch\">` element with an explicit `aria-checked` — full native keyboard (Space toggles), `aria-invalid` for errors, `aria-describedby` for associated text, visible `focus-visible` ring from `--ds-color-focus-ring`. When a label is provided it is wrapped in a `<label htmlFor>` so the text is a click target. When no label is rendered, pass `aria-label` or `aria-labelledby`.",
    notes_doc="This is the reference implementation for the Switches family — it establishes the shared 24×14px track, 10px thumb, full radius, border, focus ring, on/off/disabled/error states, and dark-mode behavior that every other switch extends.",
    showcase="""function Showcase() {
  const [a, setA] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <Switch label="Default off" />
      <Switch label="Default on" defaultChecked />
      <Switch label="Controlled" checked={a} onChange={(v)=>setA(v)} />
      <Switch label="Disabled (off)" disabled />
      <Switch label="Disabled (on)" disabled defaultChecked />
      <Switch aria-label="Developer mode (no visible label)" defaultChecked />
    </div>
  );
}""",
)

# 2. switch-with-label
register(
    "switch-with-label",
    title="Switch With Label",
    subcategory="Labeling",
    description="Switch with a visibly-associated label wrapped in a clickable label element.",
    tags=["switch", "toggle", "form", "control", "label", "settings", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch", "switch-with-helper", "switch-with-description"],
    props_doc={
        "export_name": "SwitchWithLabel",
        "usage": '<SwitchWithLabel label="Email notifications" defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)"),
    },
    behavior_doc="Same native switch as the reference, but `label` is required and always wrapped in a `<label htmlFor>`, so clicking anywhere on the text toggles the control. Renders a `*` when `required`.",
    a11y_doc="Native `<input type=\"checkbox\" role=\"switch\">` + `<label htmlFor>` association. `aria-invalid` for errors, `aria-describedby` for external helper/error text, visible `focus-visible` ring.",
    notes_doc="Use this when you only need a label and no helper or description. Reach for `switch-with-helper` or `switch-with-description` when extra context is needed.",
    showcase="""function Showcase() {
  const [a, setA] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SwitchWithLabel label="Email notifications" checked={a} onChange={(v)=>setA(v)} />
      <SwitchWithLabel label="Product updates" defaultChecked />
      <SwitchWithLabel label="Security alerts" required />
      <SwitchWithLabel label="Developer mode" disabled />
    </div>
  );
}""",
)

# 3. switch-with-description
register(
    "switch-with-description",
    title="Switch With Description",
    subcategory="Labeling",
    description="Switch with a strong label plus a supporting description wired via aria-describedby.",
    tags=["switch", "toggle", "form", "control", "description", "settings", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch", "switch-with-helper", "switch-card"],
    props_doc={
        "export_name": "SwitchWithDescription",
        "usage": '<SwitchWithDescription label="Two-factor authentication" description="Require a second factor at sign-in." defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `description` | `ReactNode` (required) | — | Supporting description linked with `aria-describedby`. |",
    },
    behavior_doc="Native switch with a bold label and a description block stacked beneath it. The description is linked with `aria-describedby`. The control is top-aligned so the track lines up with the label.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={descId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="Use this when the setting needs more than a one-line label to be understood — e.g. a security control whose effect needs a sentence of explanation.",
    showcase="""function Showcase() {
  const [tfa, setTfa] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:440}}>
      <SwitchWithDescription label="Two-factor authentication" description="Require a second factor at every sign-in." checked={tfa} onChange={(v)=>setTfa(v)} />
      <SwitchWithDescription label="Automatic updates" description="Install minor security updates as soon as they ship." defaultChecked />
      <SwitchWithDescription label="Public profile" description="Show your profile to anyone outside the workspace." />
    </div>
  );
}""",
)

# 4. switch-with-helper
register(
    "switch-with-helper",
    title="Switch With Helper",
    subcategory="Labeling",
    description="Switch with a visible label plus helper text wired via aria-describedby.",
    tags=["switch", "toggle", "form", "control", "helper", "settings", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch", "switch-with-label", "switch-with-error"],
    props_doc={
        "export_name": "SwitchWithHelper",
        "usage": '<SwitchWithHelper label="Product updates" helperText="Sent at most once a week." defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `helperText` | `ReactNode` (required) | — | Supporting text linked with `aria-describedby`. |",
    },
    behavior_doc="Native switch + a label and a helper paragraph. The helper is linked to the input with `aria-describedby` so assistive tech announces it after the label. The helper is indented to align with the label text.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={helperId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="Use this when a label alone is not enough and a short helper line gives useful context. For validation messaging use `switch-with-error`.",
    showcase="""function Showcase() {
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SwitchWithHelper label="Product updates" helperText="Sent at most once a week." defaultChecked />
      <SwitchWithHelper label="Auto-save drafts" helperText="Drafts are saved locally every 30 seconds." />
      <SwitchWithHelper label="Beta features" helperText="Early access to unfinished features. May change." />
    </div>
  );
}""",
)

# 5. switch-with-error
register(
    "switch-with-error",
    title="Switch With Error",
    subcategory="Validation",
    description="Switch with an associated validation message; sets aria-invalid and links the error via aria-describedby.",
    tags=["switch", "toggle", "form", "control", "error", "validation", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch", "switch-with-helper", "switch-group"],
    props_doc={
        "export_name": "SwitchWithError",
        "usage": '<SwitchWithError label="Two-factor authentication" error="Two-factor authentication is required for admin accounts." />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `error` | `string` | — | Error message (sets `aria-invalid`, destructive styling, `role=\"alert\"`). |\n| `helperText` | `ReactNode` | — | Shown when no error is present. |",
    },
    behavior_doc="Native switch with an optional error message. When `error` is set the input gets `aria-invalid=\"true\"`, the track border + checked fill take the destructive token, and the message is rendered with `role=\"alert\"` and `aria-describedby`. The failure is communicated by border, fill, and text — not color alone.",
    a11y_doc="`aria-invalid=\"true\"` + `aria-describedby={messageId}` on the native input; error paragraph carries `role=\"alert\"`. Visible `focus-visible` ring.",
    notes_doc="The error state never relies on color alone — the track, the fill, and the message all change. Swap `error` for `helperText` to return to a neutral helper.",
    showcase="""function Showcase() {
  const [on, setOn] = React.useState(false);
  const error = on ? undefined : "Two-factor authentication is required for admin accounts.";
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SwitchWithError label="Two-factor authentication" checked={on} onChange={(v)=>setOn(v)} error={error} />
      <SwitchWithError label="Weekly digest" error="Email delivery is paused until you verify your address." />
      <SwitchWithError label="Cloud backup" helperText="Runs every night at 02:00 UTC." defaultChecked />
    </div>
  );
}""",
)

# 6. switch-disabled
register(
    "switch-disabled",
    title="Switch Disabled",
    subcategory="States",
    description="Switch variant focused on the disabled non-interactive state.",
    tags=["switch", "toggle", "form", "control", "disabled", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch", "switch-group", "switch-card"],
    props_doc={
        "export_name": "SwitchDisabled",
        "usage": '<SwitchDisabled label="Inherited from team plan" defaultChecked />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `ReactNode` (required) | — | Visible label. |\n| `helperText` | `ReactNode` | — | Helper text (still readable when disabled). |\n| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |\n| `onChange` | `(checked, event) => void` | — | Change callback (won't fire while disabled). |\n| `disabled` | `boolean` | `true` | Defaults to disabled. |\n| `name` / `value` / `id` | `string` | — | Native form attrs. |",
    },
    behavior_doc="Native switch with `disabled` set (defaults to `true`). The visual treatment uses reduced opacity + muted foreground so the control stays perceivable without looking interactive. Native disabled semantics are preserved (excluded from form submission, not focusable, not clickable).",
    a11y_doc="Native `disabled` attribute carries the semantics. Helper text stays associated via `aria-describedby`. Reduced opacity + muted color keeps it perceivable without looking interactive.",
    notes_doc="Use `switch-disabled` for settings that exist but cannot be changed in this context (e.g. a permission inherited from a team plan, or an option gated behind verification).",
    showcase="""function Showcase() {
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SwitchDisabled label="Audit logging (on by team plan)" helperText="Managed by your workspace administrator." defaultChecked />
      <SwitchDisabled label="Public access" helperText="Available on the Pro plan and above." />
      <SwitchDisabled label="Requires domain verification first" />
    </div>
  );
}""",
)

# 7. switch-loading
register(
    "switch-loading",
    title="Switch Loading",
    subcategory="States",
    description="Switch with a real loading state that blocks interaction while the change is persisted.",
    tags=["switch", "toggle", "form", "control", "loading", "async", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y + ["aria-busy"],
    interactive=True,
    related=["switch", "switch-disabled", "switch-with-status"],
    props_doc={
        "export_name": "SwitchLoading",
        "usage": '<SwitchLoading label="Analytics" loading={saving} checked={on} onChange={handleSave} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `ReactNode` (required) | — | Visible label. |\n| `loading` | `boolean` | `false` | Pending update state — disables the input, sets `aria-busy`, swaps the thumb for a spinner of the same geometry (no layout shift). |\n| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |\n| `onChange` | `(checked, event) => void` | — | Change callback (won't fire while loading/disabled). |\n| `disabled` | `boolean` | — | Disables the control. |\n| `name` / `value` / `id` | `string` | — | Native form attrs. |",
    },
    behavior_doc="Native switch with a `loading` prop for async persistence. While `loading` is true the input is disabled (no conflicting interaction can occur), `aria-busy=\"true\"` is set, and the thumb is replaced by a spinner of exactly the same geometry — the control never moves or resizes. The spinner represents a real pending update, not decoration.",
    a11y_doc="`aria-busy=\"true\"` + native `disabled` while loading, so assistive tech reports the control as busy and it is removed from interaction. The thumb spinner is `aria-hidden`. Visible `focus-visible` ring.",
    notes_doc="Drive `loading` from your save flow: set it true when the toggle fires, resolve it when the request settles. Keep the checked value unchanged until the update succeeds, so the thumb never lies about persisted state.",
    showcase="""function Showcase() {
  const [on, setOn] = React.useState(true);
  const [saving, setSaving] = React.useState(false);
  const [backupOn, setBackupOn] = React.useState(false);
  const [backupSaving, setBackupSaving] = React.useState(false);
  function save(setVal, setBusy, val) {
    setBusy(true);
    setTimeout(() => { setVal(val); setBusy(false); }, 900);
  }
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SwitchLoading label="Analytics" checked={on} loading={saving} onChange={(v)=>save(setOn, setSaving, v)} />
      <SwitchLoading label="Cloud backup" checked={backupOn} loading={backupSaving} onChange={(v)=>save(setBackupOn, setBackupSaving, v)} />
      <SwitchLoading label="Saving…" loading defaultChecked />
      <SwitchLoading label="Cloud backup (unavailable)" disabled />
    </div>
  );
}""",
)

# 8. switch-group
register(
    "switch-group",
    title="Switch Group",
    subcategory="Group",
    description="Group of related independent on/off settings in a fieldset/legend with a shared value array.",
    tags=["switch", "toggle", "form", "control", "group", "fieldset", "settings", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch", "switch-card-group", "switch-with-description"],
    props_doc={
        "export_name": "SwitchGroup",
        "usage": '<SwitchGroup legend="Notification preferences" options={[{value:"email",label:"Email notifications"},{value:"desktop",label:"Desktop notifications"},{value:"security",label:"Security alerts"}]} defaultValue={["email","security"]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |\n| `options` | `{value,label,disabled?,description?}[]` (required) | — | Option list. |\n| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled set of options that are on. |\n| `onChange` | `(value[], event) => void` | — | Change callback. |\n| `orientation` | `\"vertical\" \\| \"horizontal\"` | `\"vertical\"` | Layout. |\n| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |",
    },
    behavior_doc="A group of related, independent on/off settings inside a `<fieldset>`/`<legend>`. Maintains a value array of the options that are on; each switch stays independently controllable (this is not a radio group). Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes are both supported.",
    a11y_doc="`<fieldset>` + `<legend>` group labeling. Each native `<input type=\"checkbox\" role=\"switch\">` is wrapped in a `<label htmlFor>`; per-option descriptions are linked with `aria-describedby`. `aria-invalid` + `role=\"alert\"` error message. Visible `focus-visible` ring on each control.",
    notes_doc="Use this for a set of independent binary settings (Email / Desktop / Security alerts). For an exclusive single choice use a radio group; for one card per setting use `switch-card-group`.",
    showcase="""function Showcase() {
  const [prefs, setPrefs] = React.useState(["email","security"]);
  const opts = [
    {value:"email",label:"Email notifications",description:"Daily summary in your inbox."},
    {value:"desktop",label:"Desktop notifications",description:"Real-time alerts on this device."},
    {value:"security",label:"Security alerts",description:"Critical account and access notices."},
    {value:"marketing",label:"Marketing emails",description:"Occasional offers and product news."}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:440}}>
      <SwitchGroup legend="Notification preferences" options={opts} value={prefs} onChange={(v)=>setPrefs(v)} />
    </div>
  );
}""",
)

# 9. switch-card
register(
    "switch-card",
    title="Switch Card",
    subcategory="Card",
    description="Settings card that pairs a label and supporting content with a switch in a deliberate, accessible row.",
    tags=["switch", "toggle", "form", "control", "card", "settings", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch-card-group", "switch-with-description", "switch"],
    props_doc={
        "export_name": "SwitchCard",
        "usage": '<SwitchCard label="Cloud backup" description="Every night at 02:00 UTC, retained for 30 days." defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `description` | `ReactNode` | — | Supporting content linked with `aria-describedby`. |",
    },
    behavior_doc="A single settings card. The whole row is a deliberate click target (a real `<label htmlFor>`) while the native switch input carries the semantics. The on state is shown with a primary border plus the moved thumb — not color alone. Hover, focus-within, and disabled states mirror the other switch variants.",
    a11y_doc="`<label htmlFor>` wraps label, description, and input. The description is linked with `aria-describedby`. Visible `focus-visible` ring on the input; the card border strengthens on focus-within. `aria-invalid` when `invalid`.",
    notes_doc="Use a switch card when a setting carries real weight — a sentence of context, a destructive consequence, or billing impact. Do not wrap every switch in a card; inline settings stay inline.",
    showcase="""function Showcase() {
  const [analytics, setAnalytics] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:440}}>
      <SwitchCard label="Cloud backup" description="Runs every night at 02:00 UTC. Backups are retained for 30 days." checked={analytics} onChange={(v)=>setAnalytics(v)} />
      <SwitchCard label="Public profile" description="Your profile is visible to anyone outside the workspace." />
      <SwitchCard label="Session timeout" description="Sign out inactive sessions after 30 minutes." defaultChecked />
      <SwitchCard label="Audit logging" description="Enabled by your team plan." disabled defaultChecked />
    </div>
  );
}""",
)

# 10. switch-card-group
register(
    "switch-card-group",
    title="Switch Card Group",
    subcategory="Group",
    description="Group of settings cards in a fieldset/legend, each with an independently-controlled switch.",
    tags=["switch", "toggle", "form", "control", "group", "card", "fieldset", "settings", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch-group", "switch-card", "switch-with-description"],
    props_doc={
        "export_name": "SwitchCardGroup",
        "usage": '<SwitchCardGroup legend="Privacy" columns={2} options={[{value:"analytics",label:"Analytics",description:"Share anonymous usage data."},{value:"public",label:"Public profile",description:"Visible outside the workspace."}]} defaultValue={["analytics"]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |\n| `options` | `{value,label,description?,disabled?}[]` (required) | — | Option list. |\n| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled set of options that are on. |\n| `onChange` | `(value[], event) => void` | — | Change callback. |\n| `columns` | `1 \\| 2` | `1` | Card columns at the `sm` breakpoint. |\n| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |",
    },
    behavior_doc="A group of settings cards inside a `<fieldset>`/`<legend>`. Maintains a value array of the options that are on; each card's switch stays independently controllable. Controlled and uncontrolled modes both supported. `columns={2}` collapses to a single column below the `sm` breakpoint.",
    a11y_doc="`<fieldset>` + `<legend>` group labeling; each card is a `<label htmlFor>` wrapping a real native input. Per-option descriptions linked with `aria-describedby`; `aria-invalid` + `role=\"alert\"` error message; visible `focus-visible` ring per control.",
    notes_doc="Use this for a small set of heavyweight settings that each need a sentence of context (privacy, backups, integrations). For lightweight inline settings use `switch-group`.",
    showcase="""function Showcase() {
  const [settings, setSettings] = React.useState(["analytics","auto-save"]);
  const opts = [
    {value:"analytics",label:"Analytics",description:"Share anonymous usage data to help improve the product."},
    {value:"public",label:"Public profile",description:"Your profile is visible to anyone outside the workspace."},
    {value:"auto-save",label:"Auto-save",description:"Drafts are saved locally every 30 seconds."},
    {value:"marketing",label:"Marketing emails",description:"Occasional offers and product news."}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:640}}>
      <SwitchCardGroup legend="Privacy" columns={2} options={opts} value={settings} onChange={(v)=>setSettings(v)} />
    </div>
  );
}""",
)

# 11. switch-with-icon
register(
    "switch-with-icon",
    title="Switch With Icon",
    subcategory="Icon",
    description="Switch with an optional icon that communicates the setting's meaning.",
    tags=["switch", "toggle", "form", "control", "icon", "settings", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch-with-label", "switch-with-status", "switch-card"],
    props_doc={
        "export_name": "SwitchWithIcon",
        "usage": '<SwitchWithIcon label="Email notifications" icon={<BellIcon />} defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `icon` | `ReactNode` | — | Optional leading icon that communicates the setting's meaning. Omit when none adds meaning. |",
    },
    behavior_doc="Same native switch as the reference, with an optional ReactNode `icon` rendered between the control and the label. The icon is state-aware (primary token when on, muted when off) but the state is never communicated by icon color alone — the thumb and track carry it.",
    a11y_doc="`<label htmlFor>` association; the icon is decorative-adjacent (the label still carries the accessible name). `aria-invalid` for errors, `aria-describedby` for external helper text, visible `focus-visible` ring.",
    notes_doc="Icons must communicate meaning (a bell for notifications, a shield for security) — they are not decoration. Do not add icons to every switch in a dense settings page; use them where the glyph disambiguates a short label.",
    showcase="""function Showcase() {
  const [notify, setNotify] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SwitchWithIcon label="Email notifications" icon={<Icon name="bell" className="size-4" />} checked={notify} onChange={(v)=>setNotify(v)} />
      <SwitchWithIcon label="Developer mode" icon={<Icon name="command" className="size-4" />} />
      <SwitchWithIcon label="Auto-save" icon={<Icon name="save" className="size-4" />} defaultChecked />
      <SwitchWithIcon label="Security alerts" disabled defaultChecked />
    </div>
  );
}""",
)

# 12. switch-with-status
register(
    "switch-with-status",
    title="Switch With Status",
    subcategory="Status",
    description="Switch paired with an explicit text status readout (Enabled / Disabled).",
    tags=["switch", "toggle", "form", "control", "status", "settings", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["switch-with-label", "switch-loading", "switch-card"],
    props_doc={
        "export_name": "SwitchWithStatus",
        "usage": '<SwitchWithStatus label="Analytics" defaultChecked />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `ReactNode` (required) | — | Visible label. |\n| `onText` / `offText` | `ReactNode` | `Enabled` / `Disabled` | Status readout for each state. |\n| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |\n| `onChange` | `(checked, event) => void` | — | Change callback. |\n| `disabled` | `boolean` | — | Disables the control. |\n| `name` / `value` / `id` | `string` | — | Native form attrs. |",
    },
    behavior_doc="Native switch with an explicit status readout beneath the label. The status text tracks the checked state (`Enabled` / `Disabled` by default, overridable with `onText` / `offText`), so the state is readable in words — never color alone. The readout is wired to the input with `aria-describedby`.",
    a11y_doc="`<label htmlFor>` association; the status line is linked with `aria-describedby` so assistive tech announces the current state as supporting text. Visible `focus-visible` ring.",
    notes_doc="Use this when the current state must be unambiguous at a glance — integrations, automation, sync. For a plain setting the thumb + track are enough; reach for `switch-with-status` when the words themselves matter.",
    showcase="""function Showcase() {
  const [analytics, setAnalytics] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SwitchWithStatus label="Analytics" checked={analytics} onChange={(v)=>setAnalytics(v)} />
      <SwitchWithStatus label="Auto backup" />
      <SwitchWithStatus label="Maintenance mode" onText="Active" offText="Inactive" />
      <SwitchWithStatus label="Two-factor authentication" disabled defaultChecked />
    </div>
  );
}""",
)
