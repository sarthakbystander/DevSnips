"""Registry for the DevSnips React Checkboxes + Radios generators.

Each ``register()`` call adds one variant's metadata + showcase + README docs.
The generators (``_gen_react_checkboxes.py`` and ``_gen_react_radios.py``)
read each component's ``code.tsx`` from disk and combine it with the spec
here to write ``code.jsx``, ``preview.html``, ``metadata.json``, and
``README.md``.

Realistic, product-oriented content only (Email notifications, Product
updates, Security alerts, Production/Staging/Development, Personal/Team
workspace). No lorem ipsum, no marketing buzzwords.
"""
from _gen_react_checkboxes import register as register_checkbox
from _gen_react_radios import register as register_radio

FEAT = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic HTML", "keyboard accessible", "native form control"]
A11Y = ["focus-visible", "keyboard accessible", "semantic HTML", "native checkbox", "associated labels", "ARIA"]

# Shared props table for the base checkbox/radio control.
BASE_PROPS = """| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(checked, event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `readOnly` | `boolean` | — | Read-only (blocks toggling). |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` / `value` | `string` | — | Native form name/value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |"""

# ===========================================================================
# CHECKBOXES
# ===========================================================================

# 1. checkbox (reference)
register_checkbox(
    "checkbox",
    title="Checkbox",
    subcategory="Core",
    description="Native checkbox styled to the DevSnips select/input visual language with controlled and uncontrolled modes.",
    tags=["checkbox", "form", "selection", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox-with-label", "checkbox-indeterminate", "checkbox-group", "checkbox-card"],
    props_doc={
        "export_name": "Checkbox",
        "usage": '<Checkbox label="Email notifications" defaultChecked />',
        "table": BASE_PROPS,
    },
    behavior_doc="A native `<input type=\"checkbox\">` styled with Tailwind + the `--ds-*` semantic tokens. The check glyph is a sibling element whose opacity tracks the tracked `isChecked` state. Controlled (`checked`/`onChange`) and uncontrolled (`defaultChecked`) modes are both supported; `readOnly` blocks toggling via `preventDefault`.",
    a11y_doc="Real `<input type=\"checkbox\">` element — full native keyboard (Space toggles), `aria-invalid` for errors, `aria-describedby` for associated text, visible `focus-visible` ring from `--ds-color-focus-ring`. When a label is provided it is wrapped in a `<label htmlFor>` so the text is a click target.",
    notes_doc="This is the reference implementation for the Checkboxes family — it establishes the shared 18px control size, `radius-xs`, border, focus ring, checked/disabled/error states, and dark-mode behavior that every other checkbox extends.",
    showcase="""function Showcase() {
  const [a, setA] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <Checkbox label="Default unchecked" />
      <Checkbox label="Checked" defaultChecked />
      <Checkbox label="Controlled" checked={a} onChange={(v)=>setA(v)} />
      <Checkbox label="Disabled" disabled defaultChecked />
      <Checkbox label="Indeterminate" indeterminate />
    </div>
  );
}""",
)

# 2. checkbox-with-label
register_checkbox(
    "checkbox-with-label",
    title="Checkbox With Label",
    subcategory="Labeling",
    description="Checkbox with a visibly-associated label wrapped in a clickable label element.",
    tags=["checkbox", "form", "selection", "label", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-with-helper", "checkbox-with-description"],
    props_doc={
        "export_name": "CheckboxWithLabel",
        "usage": '<CheckboxWithLabel label="Email notifications" defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)"),
    },
    behavior_doc="Same native checkbox as the reference, but `label` is required and always wrapped in a `<label htmlFor>`, so clicking anywhere on the text toggles the control. Renders a `*` when `required`.",
    a11y_doc="Native `<input type=\"checkbox\">` + `<label htmlFor>` association. `aria-invalid` for errors, `aria-describedby` for external helper/error text, visible `focus-visible` ring.",
    notes_doc="Use this when you only need a label and no helper or description. Reach for `checkbox-with-helper` or `checkbox-with-description` when extra context is needed.",
    showcase="""function Showcase() {
  const [a, setA] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CheckboxWithLabel label="Email notifications" checked={a} onChange={(v)=>setA(v)} />
      <CheckboxWithLabel label="Product updates" defaultChecked />
      <CheckboxWithLabel label="Security alerts" required />
      <CheckboxWithLabel label="Disabled option" disabled defaultChecked />
    </div>
  );
}""",
)

# 3. checkbox-with-helper
register_checkbox(
    "checkbox-with-helper",
    title="Checkbox With Helper",
    subcategory="Labeling",
    description="Checkbox with a visible label plus helper text wired via aria-describedby.",
    tags=["checkbox", "form", "selection", "helper", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-with-label", "checkbox-with-error"],
    props_doc={
        "export_name": "CheckboxWithHelper",
        "usage": '<CheckboxWithHelper label="Product updates" helperText="Sent at most once a week." defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `helperText` | `ReactNode` (required) | — | Supporting text linked with `aria-describedby`. |",
    },
    behavior_doc="Native checkbox + a label and a helper paragraph. The helper is linked to the input with `aria-describedby` so assistive tech announces it after the label. The helper is indented to align with the label text.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={helperId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="Use this when a label alone is not enough and a short helper line gives useful context. For validation messaging use `checkbox-with-error`.",
    showcase="""function Showcase() {
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CheckboxWithHelper label="Email notifications" helperText="Receive a summary of activity in your inbox." defaultChecked />
      <CheckboxWithHelper label="Product updates" helperText="Sent at most once a week." />
      <CheckboxWithHelper label="Security alerts" helperText="Critical security notices only." defaultChecked />
    </div>
  );
}""",
)

# 4. checkbox-with-error
register_checkbox(
    "checkbox-with-error",
    title="Checkbox With Error",
    subcategory="Validation",
    description="Checkbox with an associated validation message; sets aria-invalid and links the error via aria-describedby.",
    tags=["checkbox", "form", "selection", "error", "validation", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-with-helper", "checkbox-group"],
    props_doc={
        "export_name": "CheckboxWithError",
        "usage": '<CheckboxWithError label="I accept the terms" error="You must accept the terms to continue." />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `error` | `string` | — | Error message (sets `aria-invalid`, destructive styling, `role=\"alert\"`). |\n| `helperText` | `ReactNode` | — | Shown when no error is present. |",
    },
    behavior_doc="Native checkbox with an optional error message. When `error` is set the input gets `aria-invalid=\"true\"`, the border + check take the destructive token, and the message is rendered with `role=\"alert\"` and `aria-describedby`. The failure is communicated by border, check color, and text — not color alone.",
    a11y_doc="`aria-invalid=\"true\"` + `aria-describedby={messageId}` on the native input; error paragraph carries `role=\"alert\"`. Visible `focus-visible` ring.",
    notes_doc="The error state never relies on color alone — the border, the check, and the message all change. Swap `error` for `helperText` to return to a neutral helper.",
    showcase="""function Showcase() {
  const [checked, setChecked] = React.useState(false);
  const error = checked ? undefined : "You must accept the terms to continue.";
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CheckboxWithError label="I accept the terms of service" checked={checked} onChange={(v)=>setChecked(v)} error={error} />
      <CheckboxWithError label="Subscribe to marketing email" error="Marketing email is currently unavailable." defaultChecked />
    </div>
  );
}""",
)

# 5. checkbox-with-description
register_checkbox(
    "checkbox-with-description",
    title="Checkbox With Description",
    subcategory="Labeling",
    description="Checkbox with a strong label plus a supporting description wired via aria-describedby.",
    tags=["checkbox", "form", "selection", "description", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-with-helper", "checkbox-card"],
    props_doc={
        "export_name": "CheckboxWithDescription",
        "usage": '<CheckboxWithDescription label="Two-factor authentication" description="Require a second factor at sign-in." defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `description` | `ReactNode` (required) | — | Supporting description linked with `aria-describedby`. |",
    },
    behavior_doc="Native checkbox with a bold label and a description block stacked beneath it. The description is linked with `aria-describedby`. The control is top-aligned so the box lines up with the label.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={descId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="Use this when the option needs more than a one-line label to be understood — e.g. a setting whose effect needs a sentence of explanation.",
    showcase="""function Showcase() {
  const [tfa, setTfa] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:440}}>
      <CheckboxWithDescription label="Two-factor authentication" description="Require a second factor at every sign-in." checked={tfa} onChange={(v)=>setTfa(v)} />
      <CheckboxWithDescription label="Session timeout" description="Sign out inactive sessions after 30 minutes." />
      <CheckboxWithDescription label="Backup codes" description="Generate single-use backup codes for account recovery." defaultChecked />
    </div>
  );
}""",
)

# 6. checkbox-disabled
register_checkbox(
    "checkbox-disabled",
    title="Checkbox Disabled",
    subcategory="States",
    description="Checkbox variant focused on the disabled non-interactive state.",
    tags=["checkbox", "form", "selection", "disabled", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-readonly", "checkbox-group"],
    props_doc={
        "export_name": "CheckboxDisabled",
        "usage": '<CheckboxDisabled label="Inherited from team" checked defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `helperText` | `ReactNode` | — | Helper text (still readable when disabled). |\n| `disabled` | `boolean` | `true` | Defaults to disabled. |",
    },
    behavior_doc="Native checkbox with `disabled` set (defaults to `true`). The visual treatment uses reduced opacity + muted foreground so the control stays perceivable without looking interactive. Native disabled semantics are preserved (excluded from form submission, not focusable).",
    a11y_doc="Native `disabled` attribute carries the semantics. Helper text stays associated via `aria-describedby`. Reduced opacity + muted color keeps it perceivable.",
    notes_doc="Use `checkbox-disabled` for options that exist but cannot be changed in this context (e.g. a permission inherited from a team plan). For a value that is fixed but should still be focusable, use `checkbox-readonly`.",
    showcase="""function Showcase() {
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CheckboxDisabled label="Inherited from team plan" helperText="Managed by your workspace administrator." defaultChecked />
      <CheckboxDisabled label="Unavailable on current plan" />
      <CheckboxDisabled label="Requires verification first" helperText="Verify your domain to enable this option." />
    </div>
  );
}""",
)

# 7. checkbox-readonly
register_checkbox(
    "checkbox-readonly",
    title="Checkbox Readonly",
    subcategory="States",
    description="Read-only checkbox that stays focusable but cannot be toggled by the user.",
    tags=["checkbox", "form", "selection", "readonly", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-disabled", "checkbox-group"],
    props_doc={
        "export_name": "CheckboxReadonly",
        "usage": '<CheckboxReadonly label="System-managed permission" checked />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `ReactNode` (required) | — | Visible label. |\n| `checked` | `boolean` (required) | — | Fixed checked state. |\n| `onChange` | `(checked, event) => void` | — | Fires with the blocked attempt. |\n| `helperText` | `ReactNode` | — | Helper text. |\n| `name` / `value` / `id` | `string` | — | Native form attrs. |",
    },
    behavior_doc="Read-only checkbox. The native input uses `readOnly` plus a `preventDefault` on change (browsers do not natively honor `readOnly` on checkboxes), so clicks and Space do not toggle the value. Unlike `disabled`, it remains focusable and is still part of the document flow.",
    a11y_doc="Native `readOnly` + `aria-readonly=\"true\"`. The control is focusable so users can read its state; `preventDefault` keeps the value fixed. Visible `focus-visible` ring.",
    notes_doc="Use this for a value that is fixed in this context but should still be focusable and perceivable (e.g. a system-managed permission). Use `checkbox-disabled` when the option is genuinely non-interactive.",
    showcase="""function Showcase() {
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CheckboxReadonly label="Read access (system-managed)" checked helperText="Granted to all workspace members." />
      <CheckboxReadonly label="Write access (system-managed)" helperText="Not granted by default." />
    </div>
  );
}""",
)

# 8. checkbox-indeterminate
register_checkbox(
    "checkbox-indeterminate",
    title="Checkbox Indeterminate",
    subcategory="Indeterminate",
    description="Real indeterminate checkbox that sets the HTMLInputElement.indeterminate property imperatively.",
    tags=["checkbox", "form", "selection", "indeterminate", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-with-select-all", "checkbox-group"],
    props_doc={
        "export_name": "CheckboxIndeterminate",
        "usage": '<CheckboxIndeterminate label="Notifications" indeterminate />',
        "table": BASE_PROPS + "\n| `indeterminate` | `boolean` | `false` | Sets the native `.indeterminate` IDL property (imperative). Renders a dash indicator. |",
    },
    behavior_doc="A REAL indeterminate checkbox. The underlying `HTMLInputElement.indeterminate` property is set imperatively on the DOM node (there is no HTML attribute for it) via an effect that runs whenever `indeterminate` changes. The indeterminate indicator is a horizontal dash, distinct from the checked check mark. `checked` and `indeterminate` are independent.",
    a11y_doc="Native `<input type=\"checkbox\">` with the `.indeterminate` IDL property set on the DOM node. Keyboard behavior is native. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="This is the primitive behind `checkbox-with-select-all`. Browsers have no HTML attribute for indeterminate — it must be set in JS on the DOM node, which is why an effect + ref is used rather than a prop-to-attribute mapping.",
    showcase="""function Showcase() {
  const [state, setState] = React.useState("indeterminate");
  const checked = state === "checked";
  const indeterminate = state === "indeterminate";
  function cycle() {
    setState(state === "unchecked" ? "checked" : state === "checked" ? "indeterminate" : "unchecked");
  }
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CheckboxIndeterminate label="Unchecked" />
      <CheckboxIndeterminate label="Checked" checked defaultChecked />
      <CheckboxIndeterminate label="Indeterminate" indeterminate />
      <div className="ds-card" style={{width:"100%"}}>
        <button className="ds-theme-toggle" onClick={cycle} type="button">Cycle state</button>
        <p className="ds-note" style={{marginTop:8}}>Current: {state}</p>
      </div>
    </div>
  );
}""",
)

# 9. checkbox-group
register_checkbox(
    "checkbox-group",
    title="Checkbox Group",
    subcategory="Group",
    description="Group of related checkboxes in a fieldset/legend with a shared value array.",
    tags=["checkbox", "form", "selection", "group", "fieldset", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-with-select-all", "checkbox-card-group"],
    props_doc={
        "export_name": "CheckboxGroup",
        "usage": '<CheckboxGroup legend="Notification preferences" options={[{value:"email",label:"Email"},{value:"push",label:"Push"},{value:"sms",label:"SMS",disabled:true}]} defaultValue={["email"]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |\n| `options` | `{value,label,disabled?,description?}[]` (required) | — | Option list. |\n| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled selected values. |\n| `onChange` | `(value[], event) => void` | — | Change callback. |\n| `orientation` | `\"vertical\" \\| \"horizontal\"` | `\"vertical\"` | Layout. |\n| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |",
    },
    behavior_doc="A group of related checkboxes inside a `<fieldset>`/`<legend>`. Maintains a value array of selected option values. Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes are both supported. Each option is a native `<input type=\"checkbox\">` sharing a `name`.",
    a11y_doc="`<fieldset>` + `<legend>` group labeling. Each native input is wrapped in a `<label htmlFor>`; per-option descriptions are linked with `aria-describedby`. `aria-invalid` + `role=\"alert\"` error message. Visible `focus-visible` ring on each control.",
    notes_doc="Use this for a set of independent on/off choices. For an exclusive single choice use `radio-group`. For a master toggle with select-all use `checkbox-with-select-all`.",
    showcase="""function Showcase() {
  const [prefs, setPrefs] = React.useState(["email","security"]);
  const opts = [
    {value:"email",label:"Email notifications",description:"Daily summary in your inbox."},
    {value:"push",label:"Push notifications",description:"Real-time alerts on your devices."},
    {value:"security",label:"Security alerts",description:"Critical account and access notices."},
    {value:"marketing",label:"Product updates",description:"New features and changelog."}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:480}}>
      <CheckboxGroup legend="Notification preferences" options={opts} value={prefs} onChange={(v)=>setPrefs(v)} helperText="Choose how you want to be notified." />
      <CheckboxGroup legend="With error" options={opts} defaultValue={[]} error="Select at least one notification channel." />
    </div>
  );
}""",
)

# 10. checkbox-card
register_checkbox(
    "checkbox-card",
    title="Checkbox Card",
    subcategory="Card",
    description="Single selectable card wrapping a native checkbox; the whole card is a click target.",
    tags=["checkbox", "form", "selection", "card", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox", "checkbox-card-group", "checkbox-with-description"],
    props_doc={
        "export_name": "CheckboxCard",
        "usage": '<CheckboxCard label="Team workspace" description="Shared with your organization." defaultChecked />',
        "table": BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `description` | `ReactNode` | — | Supporting description linked with `aria-describedby`. |",
    },
    behavior_doc="A single selectable card wrapping a native checkbox. The entire card is a `<label htmlFor>` (clickable) while the real `<input type=\"checkbox\">` carries the semantics and value. The selected state is shown with an accent border, not color alone.",
    a11y_doc="`<label htmlFor>` card + native `<input type=\"checkbox\">`. `aria-invalid` when `invalid`, description linked with `aria-describedby`, visible `focus-visible` ring on the input (the card shows `focus-within` border emphasis).",
    notes_doc="Use this when an option needs more visual weight than a plain row — e.g. a plan or workspace choice. For a group of these use `checkbox-card-group`.",
    showcase="""function Showcase() {
  const [a, setA] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CheckboxCard label="Team workspace" description="Shared with everyone in your organization." checked={a} onChange={(v)=>setA(v)} />
      <CheckboxCard label="Personal workspace" description="Private to your account." />
      <CheckboxCard label="Archived workspace" description="Read-only, excluded from search." disabled />
    </div>
  );
}""",
)

# 11. checkbox-card-group
register_checkbox(
    "checkbox-card-group",
    title="Checkbox Card Group",
    subcategory="Group",
    description="Group of selectable card checkboxes in a fieldset/legend with a shared value array.",
    tags=["checkbox", "form", "selection", "card", "group", "fieldset", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox-card", "checkbox-group", "radio-card-group"],
    props_doc={
        "export_name": "CheckboxCardGroup",
        "usage": '<CheckboxCardGroup legend="Workspace features" options={[{value:"sso",label:"SSO",description:"Single sign-on"},{value:"audit",label:"Audit log"}]} defaultValue={["sso"]} columns={2} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `legend` | `ReactNode` (required) | — | Group label in `<legend>`. |\n| `options` | `{value,label,description?,disabled?}[]` (required) | — | Card options. |\n| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled selected values. |\n| `onChange` | `(value[], event) => void` | — | Change callback. |\n| `columns` | `1 \\| 2 \\| 3` | `1` | Grid columns at the `sm` breakpoint and up. |\n| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |",
    },
    behavior_doc="A group of selectable card checkboxes inside a `<fieldset>`/`<legend>`. Maintains a value array of selected option values; controlled and uncontrolled modes both supported. Each card is a clickable `<label>` wrapping a real `<input type=\"checkbox\">`. The grid collapses to a single column below the `sm` breakpoint.",
    a11y_doc="`<fieldset>` + `<legend>`. Each card is a `<label htmlFor>` wrapping a native input; descriptions linked with `aria-describedby`; `aria-invalid` + `role=\"alert\"` error. Visible `focus-visible` ring.",
    notes_doc="Use this when each option needs the visual weight of a card and multiple selections are allowed. For an exclusive single choice use `radio-card-group`.",
    showcase="""function Showcase() {
  const [sel, setSel] = React.useState(["sso","audit"]);
  const opts = [
    {value:"sso",label:"Single sign-on",description:"Authenticate via your IdP."},
    {value:"audit",label:"Audit log",description:"90-day searchable history."},
    {value:"rbac",label:"Role-based access",description:"Custom roles and scopes."},
    {value:"backup",label:"Daily backup",description:"Encrypted off-site backup."},
    {value:"sla",label:"99.9% SLA",description:"Uptime guarantee and credits."},
    {value:"support",label:"Priority support",description:"1-hour response time."}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:640}}>
      <CheckboxCardGroup legend="Workspace features" options={opts} value={sel} onChange={(v)=>setSel(v)} columns={3} helperText="Select the features to enable for this workspace." />
    </div>
  );
}""",
)

# 12. checkbox-with-select-all
register_checkbox(
    "checkbox-with-select-all",
    title="Checkbox With Select All",
    subcategory="Indeterminate",
    description="Checkbox group with a real select-all control that reflects checked/indeterminate/unchecked child state.",
    tags=["checkbox", "form", "selection", "select-all", "indeterminate", "group", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["checkbox-indeterminate", "checkbox-group", "checkbox"],
    props_doc={
        "export_name": "CheckboxWithSelectAll",
        "usage": '<CheckboxWithSelectAll legend="Permissions" options={[{value:"read",label:"Read"},{value:"write",label:"Write"}]} defaultValue={["read"]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `legend` | `ReactNode` (required) | — | Group label in `<legend>`. |\n| `options` | `{value,label,disabled?,description?}[]` (required) | — | Child options. |\n| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled selected values. |\n| `onChange` | `(value[], event) => void` | — | Change callback. |\n| `selectAllLabel` | `ReactNode` | `\"Select all\"` | Master control label. |\n| `disabled` / `required` / `name` / `id` | — | — | Standard field props. |",
    },
    behavior_doc="A checkbox group with a REAL select-all control. The master checkbox reflects the children's state: checked when all (enabled) children are selected, indeterminate when some are selected, unchecked when none. Toggling it selects/deselects every enabled child. The master's `.indeterminate` IDL property is set imperatively on the DOM node.",
    a11y_doc="`<fieldset>` + `<legend>`. Master + children are all native `<input type=\"checkbox\">` sharing a `name`; per-option descriptions linked with `aria-describedby`. Visible `focus-visible` ring. The indeterminate state is set on the DOM node (no HTML attribute exists).",
    notes_doc="This composes the `checkbox-indeterminate` primitive into a real select-all pattern. Disabled children are excluded from the all/none calculation but keep their existing selection state.",
    showcase="""function Showcase() {
  const [sel, setSel] = React.useState(["read","comment"]);
  const opts = [
    {value:"read",label:"Read access",description:"View all resources in the workspace."},
    {value:"write",label:"Write access",description:"Create and edit resources."},
    {value:"comment",label:"Comment",description:"Leave comments on resources."},
    {value:"delete",label:"Delete access",description:"Permanently remove resources."},
    {value:"admin",label:"Admin",description:"Manage members and billing.",disabled:true}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:480}}>
      <CheckboxWithSelectAll legend="Workspace permissions" options={opts} value={sel} onChange={(v)=>setSel(v)} />
    </div>
  );
}""",
)

# ===========================================================================
# RADIOS
# ===========================================================================

RADIO_BASE_PROPS = """| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit for an icon-only / aria-label control). |
| `checked` / `defaultChecked` | `boolean` | `false` | Controlled / uncontrolled checked state. |
| `onChange` | `(event) => void` | — | Change callback. |
| `disabled` | `boolean` | — | Disables the control. |
| `required` | `boolean` | — | Marks the field required (renders `*`). |
| `invalid` | `boolean` | — | Sets `aria-invalid` + destructive styling. |
| `name` | `string` | — | Shared group name (groups radios). |
| `value` | `string \\| number \\| readonly string[]` (required) | — | Native form value. |
| `id` | `string` | generated | Input id (also the label `htmlFor`). |
| `aria-label` / `aria-labelledby` / `aria-describedby` | `string` | — | Override association. |"""

# 1. radio (reference)
register_radio(
    "radio",
    title="Radio",
    subcategory="Core",
    description="Native radio styled to the DevSnips select/input visual language with controlled and uncontrolled modes.",
    tags=["radio", "form", "selection", "react", "tailwind", "accessible", "interactive", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio-with-label", "radio-group", "radio-card"],
    props_doc={
        "export_name": "Radio",
        "usage": '<Radio label="Production" name="env" value="production" defaultChecked />',
        "table": RADIO_BASE_PROPS,
    },
    behavior_doc="A native `<input type=\"radio\">` styled with Tailwind + the `--ds-*` semantic tokens. The selected dot is a sibling element whose opacity tracks the tracked `isChecked` state. Controlled (`checked`/`onChange`) and uncontrolled (`defaultChecked`) modes are both supported.",
    a11y_doc="Real `<input type=\"radio\">` element — full native keyboard (Arrow keys move within a named group, Space + select), `aria-invalid` for errors, `aria-describedby` for associated text, visible `focus-visible` ring from `--ds-color-focus-ring`. When a label is provided it is wrapped in a `<label htmlFor>`.",
    notes_doc="This is the reference implementation for the Radios family — it establishes the shared 18px control size, full-round radius, border, focus ring, selected/disabled/error states, and dark-mode behavior that every other radio extends.",
    showcase="""function Showcase() {
  const [env, setEnv] = React.useState("production");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <Radio label="Production" name="env1" value="production" defaultChecked />
      <Radio label="Staging" name="env1" value="staging" />
      <Radio label="Selected (controlled)" name="env2" value="production" checked={env==="production"} onChange={(e)=>setEnv(e.target.value)} />
      <Radio label="Disabled" name="env3" value="production" disabled defaultChecked />
    </div>
  );
}""",
)

# 2. radio-with-label
register_radio(
    "radio-with-label",
    title="Radio With Label",
    subcategory="Labeling",
    description="Radio with a visibly-associated label wrapped in a clickable label element.",
    tags=["radio", "form", "selection", "label", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-with-helper", "radio-group"],
    props_doc={
        "export_name": "RadioWithLabel",
        "usage": '<RadioWithLabel label="Production" name="env" value="production" defaultChecked />',
        "table": RADIO_BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)"),
    },
    behavior_doc="Same native radio as the reference, but `label` is required and always wrapped in a `<label htmlFor>`, so clicking anywhere on the text selects the option. Renders a `*` when `required`.",
    a11y_doc="Native `<input type=\"radio\">` + `<label htmlFor>` association. `aria-invalid` for errors, `aria-describedby` for external helper/error text, visible `focus-visible` ring.",
    notes_doc="Use this when you only need a label and no helper or description. Reach for `radio-with-helper` or `radio-with-description` when extra context is needed.",
    showcase="""function Showcase() {
  const [env, setEnv] = React.useState("staging");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <RadioWithLabel label="Production" name="env" value="production" checked={env==="production"} onChange={(e)=>setEnv(e.target.value)} />
      <RadioWithLabel label="Staging" name="env" value="staging" checked={env==="staging"} onChange={(e)=>setEnv(e.target.value)} />
      <RadioWithLabel label="Development" name="env" value="development" checked={env==="development"} onChange={(e)=>setEnv(e.target.value)} />
    </div>
  );
}""",
)

# 3. radio-with-helper
register_radio(
    "radio-with-helper",
    title="Radio With Helper",
    subcategory="Labeling",
    description="Radio with a visible label plus helper text wired via aria-describedby.",
    tags=["radio", "form", "selection", "helper", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-with-label", "radio-with-error"],
    props_doc={
        "export_name": "RadioWithHelper",
        "usage": '<RadioWithHelper label="Production" helperText="Live traffic, real customers." name="env" value="production" defaultChecked />',
        "table": RADIO_BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `helperText` | `ReactNode` (required) | — | Supporting text linked with `aria-describedby`. |",
    },
    behavior_doc="Native radio + a label and a helper paragraph. The helper is linked to the input with `aria-describedby` so assistive tech announces it after the label. The helper is indented to align with the label text.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={helperId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="Use this when a label alone is not enough and a short helper line gives useful context. For validation messaging use `radio-with-error`.",
    showcase="""function Showcase() {
  const [env, setEnv] = React.useState("production");
  const opts = [
    {value:"production",label:"Production",helper:"Live traffic, real customers."},
    {value:"staging",label:"Staging",helper:"Pre-release verification."},
    {value:"development",label:"Development",helper:"Local and branch builds."}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:440}}>
      {opts.map((o)=>(
        <RadioWithHelper key={o.value} label={o.label} helperText={o.helper} name="env" value={o.value} checked={env===o.value} onChange={(e)=>setEnv(e.target.value)} />
      ))}
    </div>
  );
}""",
)

# 4. radio-with-error
register_radio(
    "radio-with-error",
    title="Radio With Error",
    subcategory="Validation",
    description="Radio with an associated validation message; sets aria-invalid and links the error via aria-describedby.",
    tags=["radio", "form", "selection", "error", "validation", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-with-helper", "radio-group"],
    props_doc={
        "export_name": "RadioWithError",
        "usage": '<RadioWithError label="Production" error="Production is currently unavailable." name="env" value="production" />',
        "table": RADIO_BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `error` | `string` | — | Error message (sets `aria-invalid`, destructive styling, `role=\"alert\"`). |\n| `helperText` | `ReactNode` | — | Shown when no error is present. |",
    },
    behavior_doc="Native radio with an optional error message. When `error` is set the input gets `aria-invalid=\"true\"`, the border + dot take the destructive token, and the message is rendered with `role=\"alert\"` and `aria-describedby`. The failure is communicated by border, dot, and text — not color alone.",
    a11y_doc="`aria-invalid=\"true\"` + `aria-describedby={messageId}` on the native input; error paragraph carries `role=\"alert\"`. Visible `focus-visible` ring.",
    notes_doc="The error state never relies on color alone — the border, the dot, and the message all change. Swap `error` for `helperText` to return to a neutral helper.",
    showcase="""function Showcase() {
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <RadioWithError label="Production" error="Production is currently unavailable for this workspace." name="env" value="production" />
      <RadioWithError label="Staging" helperText="Available for staging deploys." name="env" value="staging" />
    </div>
  );
}""",
)

# 5. radio-with-description
register_radio(
    "radio-with-description",
    title="Radio With Description",
    subcategory="Labeling",
    description="Radio with a strong label plus a supporting description wired via aria-describedby.",
    tags=["radio", "form", "selection", "description", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-with-helper", "radio-card"],
    props_doc={
        "export_name": "RadioWithDescription",
        "usage": '<RadioWithDescription label="Team workspace" description="Shared with your organization." name="workspace" value="team" defaultChecked />',
        "table": RADIO_BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `description` | `ReactNode` (required) | — | Supporting description linked with `aria-describedby`. |",
    },
    behavior_doc="Native radio with a bold label and a description block stacked beneath it. The description is linked with `aria-describedby`. The control is top-aligned so the circle lines up with the label.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={descId}` on the native input. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="Use this when the option needs more than a one-line label to be understood — e.g. a plan or workspace choice where the effect needs a sentence of explanation.",
    showcase="""function Showcase() {
  const [ws, setWs] = React.useState("team");
  const opts = [
    {value:"personal",label:"Personal workspace",description:"Private to your account, ideal for solo projects."},
    {value:"team",label:"Team workspace",description:"Shared with everyone in your organization."},
    {value:"enterprise",label:"Enterprise workspace",description:"SSO, audit log, and dedicated support."}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:480}}>
      {opts.map((o)=>(
        <RadioWithDescription key={o.value} label={o.label} description={o.description} name="workspace" value={o.value} checked={ws===o.value} onChange={(e)=>setWs(e.target.value)} />
      ))}
    </div>
  );
}""",
)

# 6. radio-disabled
register_radio(
    "radio-disabled",
    title="Radio Disabled",
    subcategory="States",
    description="Radio variant focused on the disabled non-interactive state.",
    tags=["radio", "form", "selection", "disabled", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-group"],
    props_doc={
        "export_name": "RadioDisabled",
        "usage": '<RadioDisabled label="Enterprise (requires upgrade)" name="plan" value="enterprise" />',
        "table": RADIO_BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `helperText` | `ReactNode` | — | Helper text (still readable when disabled). |\n| `disabled` | `boolean` | `true` | Defaults to disabled. |",
    },
    behavior_doc="Native radio with `disabled` set (defaults to `true`). The visual treatment uses reduced opacity + muted foreground so the control stays perceivable without looking interactive. Native disabled semantics are preserved (excluded from form submission, not focusable).",
    a11y_doc="Native `disabled` attribute carries the semantics. Helper text stays associated via `aria-describedby`. Reduced opacity + muted color keeps it perceivable.",
    notes_doc="Use `radio-disabled` for options that exist but cannot be chosen in this context (e.g. a plan that requires an upgrade).",
    showcase="""function Showcase() {
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <RadioDisabled label="Enterprise" helperText="Requires an upgrade to the Enterprise plan." name="plan" value="enterprise" />
      <RadioDisabled label="Archived region" helperText="No longer available for new deployments." name="plan" value="archived" defaultChecked />
    </div>
  );
}""",
)

# 7. radio-group
register_radio(
    "radio-group",
    title="Radio Group",
    subcategory="Group",
    description="Radio group where only one option may be selected, in a fieldset/legend.",
    tags=["radio", "form", "selection", "group", "fieldset", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-card-group", "checkbox-group"],
    props_doc={
        "export_name": "RadioGroup",
        "usage": '<RadioGroup legend="Deploy target" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="staging" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `legend` | `ReactNode` (required) | — | Group label rendered in `<legend>`. |\n| `options` | `{value,label,disabled?,description?}[]` (required) | — | Option list. |\n| `value` / `defaultValue` | `string` | `\"\"` | Controlled / uncontrolled selected value. |\n| `onChange` | `(value, event) => void` | — | Selection callback. |\n| `orientation` | `\"vertical\" \\| \"horizontal\"` | `\"vertical\"` | Layout. |\n| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |",
    },
    behavior_doc="A radio group: only one option may be selected. Wraps native `<input type=\"radio\">` elements sharing a `name` inside a `<fieldset>`/`<legend>`. Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes are both supported. Native arrow-key navigation moves within the named group.",
    a11y_doc="`<fieldset>` + `<legend>` group labeling. Each native input is wrapped in a `<label htmlFor>`; per-option descriptions are linked with `aria-describedby`. `aria-invalid` + `role=\"alert\"` error message. Visible `focus-visible` ring; arrow keys navigate natively.",
    notes_doc="Use this for an exclusive single choice. For multiple independent choices use `checkbox-group`. For card-style options use `radio-card-group`.",
    showcase="""function Showcase() {
  const [env, setEnv] = React.useState("staging");
  const opts = [
    {value:"production",label:"Production",description:"Live traffic, real customers."},
    {value:"staging",label:"Staging",description:"Pre-release verification."},
    {value:"development",label:"Development",description:"Local and branch builds.",disabled:true}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:480}}>
      <RadioGroup legend="Deploy target" options={opts} value={env} onChange={(v)=>setEnv(v)} helperText="Choose where this build will be deployed." />
      <RadioGroup legend="With error" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"}]} defaultValue="" error="Select a deploy target." />
    </div>
  );
}""",
)

# 8. radio-card
register_radio(
    "radio-card",
    title="Radio Card",
    subcategory="Card",
    description="Single selectable card wrapping a native radio; the whole card is a click target.",
    tags=["radio", "form", "selection", "card", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-card-group", "radio-with-description"],
    props_doc={
        "export_name": "RadioCard",
        "usage": '<RadioCard label="Team workspace" description="Shared with your organization." name="workspace" value="team" defaultChecked />',
        "table": RADIO_BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `description` | `ReactNode` | — | Supporting description linked with `aria-describedby`. |",
    },
    behavior_doc="A single selectable card wrapping a native radio. The entire card is a `<label htmlFor>` (clickable) while the real `<input type=\"radio\">` carries the semantics and value. The selected state is shown with an accent border, not color alone.",
    a11y_doc="`<label htmlFor>` card + native `<input type=\"radio\">`. `aria-invalid` when `invalid`, description linked with `aria-describedby`, visible `focus-visible` ring on the input (the card shows `focus-within` border emphasis).",
    notes_doc="Use this when an option needs more visual weight than a plain row — e.g. a plan or workspace choice. For a group of these use `radio-card-group`.",
    showcase="""function Showcase() {
  const [ws, setWs] = React.useState("team");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <RadioCard label="Personal workspace" description="Private to your account." name="ws1" value="personal" />
      <RadioCard label="Team workspace" description="Shared with everyone in your organization." name="ws1" value="team" checked={ws==="team"} onChange={(e)=>setWs(e.target.value)} />
      <RadioCard label="Enterprise workspace" description="SSO, audit log, dedicated support." name="ws1" value="enterprise" />
    </div>
  );
}""",
)

# 9. radio-card-group
register_radio(
    "radio-card-group",
    title="Radio Card Group",
    subcategory="Group",
    description="Group of selectable card radios in a fieldset/legend; only one may be selected.",
    tags=["radio", "form", "selection", "card", "group", "fieldset", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio-card", "radio-group", "checkbox-card-group"],
    props_doc={
        "export_name": "RadioCardGroup",
        "usage": '<RadioCardGroup legend="Workspace plan" options={[{value:"personal",label:"Personal"},{value:"team",label:"Team"}]} defaultValue="team" columns={3} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `legend` | `ReactNode` (required) | — | Group label in `<legend>`. |\n| `options` | `{value,label,description?,disabled?}[]` (required) | — | Card options. |\n| `value` / `defaultValue` | `string` | `\"\"` | Controlled / uncontrolled selected value. |\n| `onChange` | `(value, event) => void` | — | Selection callback. |\n| `columns` | `1 \\| 2 \\| 3` | `1` | Grid columns at the `sm` breakpoint and up. |\n| `disabled` / `required` / `invalid` / `error` / `helperText` / `name` / `id` | — | — | Standard field props. |",
    },
    behavior_doc="A group of selectable card radios inside a `<fieldset>`/`<legend>`. Only one card may be selected. Controlled and uncontrolled modes both supported. Each card is a clickable `<label>` wrapping a real `<input type=\"radio\">`. The grid collapses to a single column below the `sm` breakpoint.",
    a11y_doc="`<fieldset>` + `<legend>`. Each card is a `<label htmlFor>` wrapping a native radio; descriptions linked with `aria-describedby`; `aria-invalid` + `role=\"alert\"` error. Visible `focus-visible` ring; arrow keys navigate natively within the named group.",
    notes_doc="Use this when each option needs the visual weight of a card and exactly one selection is allowed. For multiple selections use `checkbox-card-group`.",
    showcase="""function Showcase() {
  const [plan, setPlan] = React.useState("team");
  const opts = [
    {value:"personal",label:"Personal",description:"For individual developers."},
    {value:"team",label:"Team",description:"For small teams up to 10."},
    {value:"business",label:"Business",description:"For growing organizations."},
    {value:"enterprise",label:"Enterprise",description:"SSO, audit log, support."}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:640}}>
      <RadioCardGroup legend="Workspace plan" options={opts} value={plan} onChange={(v)=>setPlan(v)} columns={2} helperText="Choose the plan that fits your team." />
    </div>
  );
}""",
)

# 10. radio-with-icons
register_radio(
    "radio-with-icons",
    title="Radio With Icons",
    subcategory="Labeling",
    description="Radio with an optional leading icon and selected indicator icon that communicate meaning.",
    tags=["radio", "form", "selection", "icon", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["radio", "radio-with-label", "radio-group"],
    props_doc={
        "export_name": "RadioWithIcons",
        "usage": '<RadioWithIcons label="Team workspace" icon={<Icon name="user" />} name="workspace" value="team" defaultChecked />',
        "table": RADIO_BASE_PROPS.replace("`label` | `ReactNode`", "`label` | `ReactNode` (required)") + "\n| `icon` | `ReactNode` | — | Leading icon that communicates meaning (color shifts on select). |\n| `selectedIcon` | `ReactNode` | — | Trailing indicator shown when selected. |",
    },
    behavior_doc="A radio with an optional leading icon that communicates meaning (e.g. a workspace-type glyph). Icons are ReactNode and must not be purely decorative — omit `icon` when none adds meaning. A trailing `selectedIcon` may be shown when the option is selected. Built on the native `<input type=\"radio\">`; the icon sits in the clickable label.",
    a11y_doc="`<label htmlFor>` + native `<input type=\"radio\">`. Icons are `aria-hidden` decoration — the label carries the accessible name. `aria-invalid` when `invalid`, visible `focus-visible` ring.",
    notes_doc="Only use icons that add meaning (e.g. distinguishing workspace types). Do not add a decorative icon to every basic radio. The leading icon is optional precisely so a plain labeled radio stays the default.",
    showcase="""function Showcase() {
  const [ws, setWs] = React.useState("team");
  const opts = [
    {value:"personal",label:"Personal workspace",icon:"user"},
    {value:"team",label:"Team workspace",icon:"users"},
    {value:"enterprise",label:"Enterprise workspace",icon:"settings"}
  ];
  return (
    <div className="ds-stack" style={{maxWidth:440}}>
      {opts.map((o)=>(
        <div key={o.value} style={{width:"100%"}}>
          <RadioWithIcons label={o.label} icon={<Icon name={o.icon} />} selectedIcon={<Icon name="check" />} name="ws" value={o.value} checked={ws===o.value} onChange={(e)=>setWs(e.target.value)} />
        </div>
      ))}
    </div>
  );
}""",
)
