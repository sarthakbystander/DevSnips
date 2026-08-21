"""Registry for the DevSnips React Form Fields generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference
``form-field/code.tsx``). The generator (``_gen_react_formfields.py``)
combines these with the reference ``code.tsx`` on disk to write ``code.tsx``
(derived), ``code.jsx``, ``preview.html``, ``metadata.json``, and
``README.md``.

Realistic, product-oriented demo content only (profiles, API tokens,
notifications, workspace settings). No lorem ipsum, no marketing buzzwords.
"""
from _gen_react_formfields import register

TAGS_BASE = ["form", "field", "label", "react", "tailwind", "accessible", "validation", "responsive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic HTML", "aria-describedby wiring", "control-agnostic"]
A11Y_BASE = ["label htmlFor + control id association", "aria-describedby registered ids", "no dangling ARIA references", "focus-visible", "semantic HTML"]

# Shared showcase controls. Each preview inlines these so the compound
# FormField primitives can wrap realistic native controls (input, select,
# textarea, checkbox, radio) — the FormField family never ships its own
# control implementations.
CONTROLS_JS = r"""const FIELD_BASE = "w-full min-w-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:opacity-60 aria-invalid:border-[var(--ds-color-destructive)] motion-reduce:transition-none";
const INPUT_CLS = FIELD_BASE + " h-9 px-3";
const SELECT_CLS = FIELD_BASE + " h-9 px-3";
const TEXTAREA_CLS = FIELD_BASE + " min-h-[80px] resize-y px-3 py-2";
const CHOICE_CLS = "size-4 shrink-0 accent-[var(--ds-color-primary)]";
const CHOICE_ROW_CLS = "flex items-center gap-2 text-sm leading-5 text-[var(--ds-color-foreground)]";
const BTN_PRIMARY = "inline-flex h-9 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-4 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";

function DemoSwitch(props) {
  // A composite control: it forwards every injected prop (id, required,
  // disabled, aria-*) to its underlying native input — the same contract
  // the DevSnips Switches family honors.
  return (
    <input
      type="checkbox"
      role="switch"
      {...props}
      className={"size-4 shrink-0 accent-[var(--ds-color-primary)] " + (props.className || "")}
    />
  );
}"""

# ---------------------------------------------------------------------------
# Shared props tables. The seven primitives + hook carry the same API
# family-wide.
# ---------------------------------------------------------------------------

FIELD_PROPS = r"""### `<FormField>`

| Name | Type | Default | Description |
|---|---|---|---|
| `controlId` | `string` | generated | Id given to the control; the label's `htmlFor` points at it. |
| `required` | `boolean` | `false` | Required indicator on the label + native `required` on the control. |
| `disabled` | `boolean` | `false` | Muted label + native `disabled` on the control. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | `horizontal` puts the label in a left column from `sm` up; stacks below `sm`. |
| `className` | `string` | — | Extra classes on the root element. |
| `children` | `ReactNode` | — | `FormFieldLabel`, `FormFieldControl`, descriptions, helpers, messages. |"""

LABEL_PROPS = r"""### `<FormFieldLabel>`

| Name | Type | Default | Description |
|---|---|---|---|
| `optional` | `boolean` | `false` | Show a muted "(optional)" indicator (for the optional fields of a mostly-required form). |
| `className` | `string` | — | Extra classes on the `<label>`. |
| `children` | `ReactNode` | — | Label text. |

A real `<label htmlFor>` pointing at the field's control — clicking it focuses the control."""

CONTROL_PROPS = r"""### `<FormFieldControl>`

| Name | Type | Default | Description |
|---|---|---|---|
| `children` | `ReactElement` (exactly one) | — | The control: a native `<input>` / `<select>` / `<textarea>`, or a DevSnips component that forwards props to its underlying control. |

Injects `id`, `aria-describedby` (registered description / helper / message ids, merged with any the control already carries), `aria-invalid="true"` (only while an error message is rendered), and `required` / `disabled` when the field sets them. Props already on the control win nowhere — the field owns `id`, `required`, and `disabled`; `aria-describedby` values are merged."""

DESCRIPTION_PROPS = r"""### `<FormFieldDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Description text. |

Muted supporting text that frames the field (purpose, impact). Registered with the nearest provider and linked with `aria-describedby` — the attribute is only set while the description is rendered."""

HELPER_PROPS = r"""### `<FormFieldHelper>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Helper text. |

Muted persistent hint below the control (format, constraints), linked with `aria-describedby`. For validation feedback use `FormFieldMessage`."""

MESSAGE_PROPS = r"""### `<FormFieldMessage>`

| Name | Type | Default | Description |
|---|---|---|---|
| `tone` | `"error" \| "success"` | (required) | `error`: destructive text + alert icon, `role="alert"`, and the control flips to `aria-invalid="true"`. `success`: success text + check icon, `role="status"`. |
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Message text. |

Render the message only while the state holds (e.g. `{error && <FormFieldMessage tone="error">{error}</FormFieldMessage>}`); removing it clears the wiring. State is carried by icon + text + ARIA — never by color alone."""

GROUP_PROPS = r"""### `<FormFieldGroup>`

| Name | Type | Default | Description |
|---|---|---|---|
| `legend` | `ReactNode` | (required) | The group's accessible name, rendered as the `<legend>`. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | `horizontal` lays the children out in a wrapping row. |
| `disabled` | `boolean` | `false` | Native `fieldset` disabled — every descendant control is disabled. |
| `className` | `string` | — | Extra classes on the `<fieldset>`. |
| `children` | `ReactNode` | — | Controls, nested `FormField`s, and group-level texts. |

A real `<fieldset>` + `<legend>`. `FormFieldDescription` / `FormFieldHelper` / `FormFieldMessage` placed directly inside describe the whole group (linked with `aria-describedby` on the fieldset); nested `FormField` children keep their own wiring."""

HOOK_PROPS = r"""### `useFormField()`

Returns the enclosing field's wiring — `{ controlId, required, disabled, orientation, describedBy, hasError }` — for building custom controls that participate without `<FormFieldControl>`. Throws outside a `<FormField>`."""

ALL_PROPS = "\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, DESCRIPTION_PROPS, HELPER_PROPS, MESSAGE_PROPS, GROUP_PROPS, HOOK_PROPS])

WIRING_BASE = r"""`FormField` generates a control id (or takes `controlId`) and hands it to `FormFieldLabel` (`htmlFor`) and `FormFieldControl` (`id`), so the label/control association is automatic and can never dangle. `FormFieldDescription`, `FormFieldHelper`, and `FormFieldMessage` each generate their own id and **register** it with the nearest provider in an effect; only then does the control's `aria-describedby` reference those ids — the attribute is omitted entirely while no text is rendered, and removed ids are unregistered on unmount. `FormFieldControl` merges these ids with any `aria-describedby` the control already carries.

An error `FormFieldMessage` additionally flips the control to `aria-invalid="true"` for as long as it is rendered; removing the message clears both the described-by id and the invalid state. `required` / `disabled` on `FormField` are forwarded to the control as the **native** attributes, so constraint validation, form submission, and assistive-technology announcements behave natively.

The wiring is control-agnostic: `FormFieldControl` clones its single child and merges props, so native elements and DevSnips components (which forward these props to their underlying control) both work. Custom controls can read the same wiring through `useFormField()`."""

A11Y_DOC = r"""- Label ↔ control: `FormFieldLabel` is a real `<label>` whose `htmlFor` is the control's `id` — clicking the label focuses the control, and assistive technology announces the label as the control's accessible name.
- Descriptions, helpers, and messages are linked with `aria-describedby` **by registration**: ids are generated, registered, and only then referenced. There are no dangling ARIA references, and `aria-describedby` is omitted entirely when nothing describes the control.
- Error messages render `role="alert"` (announced immediately on appearance) and set `aria-invalid="true"` on the control; success messages render `role="status"` (politely announced). Both pair an icon with text, so state is never communicated by color alone.
- `required` is the native attribute (announced as required), plus a destructive `*` marked `aria-hidden` with an sr-only "(required)" fallback — the visual asterisk is never the only indicator.
- `disabled` is the native attribute: the control leaves the tab order and cannot be edited.
- `FormFieldGroup` is a real `<fieldset>` + `<legend>`, so grouped controls (radios, checkboxes) get a programmatic group name; group-level texts describe the whole fieldset via `aria-describedby`."""

STATES_BASE = r"""- **Default** — foreground label, muted supporting text, control styled by its own component.
- **Required** — destructive `*` + sr-only "(required)" on the label; native `required` on the control.
- **Optional** — muted "(optional)" label indicator (a label choice, not a control state).
- **Disabled** — native `disabled` control (out of tab order, not editable) + muted label.
- **Error** — destructive message with alert icon, `role="alert"`, `aria-invalid="true"` on the control.
- **Success** — success-token message with check icon, `role="status"`.
- **Grouped** — `<fieldset>` + `<legend>`; group texts describe the whole group."""

RESPONSIVE_BASE = r"""The default vertical layout stacks label, description, control, and helper/message in one column at every width — full-width, `min-w-0`, no overflow. `orientation="horizontal"` uses a `10rem` label column + `minmax(0,1fr)` control column from `sm` up and collapses to the single-column stack below `sm`, so labels are never clipped and controls never overflow on narrow screens. `FormFieldGroup orientation="horizontal"` lays children out in a wrapping row (`flex-wrap`), so choice rows reflow instead of overflowing. Verified at 375 / 768 / 1280px with zero horizontal overflow."""

# ---------------------------------------------------------------------------
# Variants
# ---------------------------------------------------------------------------

# 1. form-field (reference)
register(
    "form-field",
    title="Form Field",
    subcategory="Core",
    description="The structural layer around a form control: label, description, control, helper, and validation message with automatic id / aria-describedby / aria-invalid wiring.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["form-field-required", "form-field-with-error", "form-field-group", "form-field-horizontal"],
    usage="""<FormField>
  <FormFieldLabel>Email</FormFieldLabel>
  <FormFieldDescription>Used for sign-in and notifications.</FormFieldDescription>
  <FormFieldControl>
    <input type="email" placeholder="ada@example.com" />
  </FormFieldControl>
  <FormFieldHelper>We never share your email.</FormFieldHelper>
</FormField>""",
    props_doc=ALL_PROPS,
    composition_note="This reference shows the full vertical composition with four different controls — a text input, an email input, a `<select>`, and a `<textarea>` — proving the field wrapper is control-agnostic.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="This is the reference implementation for the Form Fields family — it establishes the shared vertical rhythm (8px gaps), the 13px label / 12px supporting-text type scale, the registration-based ARIA wiring, and the horizontal layout behavior every other variant uses. FormField never re-implements controls; compose it with the DevSnips Inputs, Selects, Textareas, Checkboxes, Radios, and Switches families.",
    tsx_header="""/**
 * DevSnips React Form Field — reference implementation.
 *
 * The structural layer around a form control: label, description, helper
 * text, validation messages, required/optional indicators, and disabled /
 * error / success state wiring. It composes with ANY control — a native
 * `<input>` / `<select>` / `<textarea>` or a DevSnips component that
 * forwards props to its underlying control — and never re-implements one.
 *
 * Composition: `<FormField>` (root provider) + `<FormFieldLabel>` +
 * `<FormFieldControl>` (wraps the control and injects `id`,
 * `aria-describedby`, `aria-invalid`, `required`, `disabled`) +
 * `<FormFieldDescription>` / `<FormFieldHelper>` / `<FormFieldMessage>`.
 * Related fields are grouped with `<FormFieldGroup>` (a real
 * `<fieldset>` + `<legend>`).
 *
 * Accessibility wiring is registration-based: description / helper /
 * message primitives register their generated ids with the nearest
 * provider, and only then are the ids referenced — `aria-describedby` is
 * never left pointing at nothing. An error `FormFieldMessage` flips the
 * control to `aria-invalid="true"` and announces itself with
 * `role="alert"`; a success message uses `role="status"`. State is never
 * communicated by color alone.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  return (
    <div className="w-full max-w-md space-y-6">
      <FormField>
        <FormFieldLabel>Display name</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} defaultValue="Ada Byron" />
        </FormFieldControl>
        <FormFieldHelper>Shown on your public profile.</FormFieldHelper>
      </FormField>
      <FormField>
        <FormFieldLabel>Email</FormFieldLabel>
        <FormFieldDescription>Used for sign-in and notifications.</FormFieldDescription>
        <FormFieldControl>
          <input className={INPUT_CLS} type="email" placeholder="ada@example.com" />
        </FormFieldControl>
        <FormFieldHelper>We never share your email.</FormFieldHelper>
      </FormField>
      <FormField>
        <FormFieldLabel>Role</FormFieldLabel>
        <FormFieldControl>
          <select className={SELECT_CLS} defaultValue="developer">
            <option value="developer">Developer</option>
            <option value="designer">Designer</option>
            <option value="manager">Engineering manager</option>
          </select>
        </FormFieldControl>
      </FormField>
      <FormField>
        <FormFieldLabel>Bio</FormFieldLabel>
        <FormFieldControl>
          <textarea className={TEXTAREA_CLS} placeholder="A sentence or two about your work." />
        </FormFieldControl>
      </FormField>
    </div>
  );
}""",
)

# 2. form-field-required
register(
    "form-field-required",
    title="Form Field Required",
    subcategory="Labeling",
    description="Required fields: the label gains a destructive asterisk plus an sr-only indicator, and the control receives the native required attribute — so native form validation and assistive technology both agree.",
    tags=TAGS_BASE + ["required", "constraint-validation"],
    features=FEAT_BASE + ["native required", "native form validation"],
    accessibility=A11Y_BASE + ["native required attribute", "aria-hidden asterisk + sr-only (required)"],
    interactive=True,
    related=["form-field", "form-field-optional", "form-field-with-error"],
    usage="""<form onSubmit={handleSubmit}>
  <FormField required>
    <FormFieldLabel>Email</FormFieldLabel>
    <FormFieldControl>
      <input type="email" name="email" />
    </FormFieldControl>
  </FormField>
  <button type="submit">Create account</button>
</form>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, MESSAGE_PROPS]),
    composition_note="Mark the whole field required with one `required` prop on `<FormField>` — the label indicator and the native control attribute stay in sync automatically.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo is a real `<form>`: submitting with an empty required field is blocked by native constraint validation (the browser flags the control invalid); filling every required field lets the submit through. `required` on `FormField` is forwarded to the control by `FormFieldControl`, so there is one source of truth.",
    tsx_header="""/**
 * DevSnips React Form Field — required state.
 *
 * `required` on `<FormField>` does three things together: the label renders
 * a destructive `*` (aria-hidden) plus an sr-only "(required)" so the state
 * is not shape/color alone, and `FormFieldControl` forwards a native
 * `required` to the control — native constraint validation, form
 * submission blocking, and assistive-technology announcement all work.
 * Same compound core as the reference `form-field`; this variant's preview
 * demonstrates the required state inside a real `<form>`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  const [saved, setSaved] = React.useState(false);
  return (
    <form
      className="w-full max-w-md space-y-6"
      onSubmit={(e) => { e.preventDefault(); setSaved(true); }}
    >
      <FormField required>
        <FormFieldLabel>Full name</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} name="name" autoComplete="name" />
        </FormFieldControl>
      </FormField>
      <FormField required>
        <FormFieldLabel>Email</FormFieldLabel>
        <FormFieldDescription>Used for sign-in and notifications.</FormFieldDescription>
        <FormFieldControl>
          <input className={INPUT_CLS} type="email" name="email" autoComplete="email" />
        </FormFieldControl>
      </FormField>
      <FormField>
        <FormFieldLabel optional>Company</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} name="company" autoComplete="organization" />
        </FormFieldControl>
      </FormField>
      <div className="flex items-center gap-3">
        <button type="submit" className={BTN_PRIMARY}>Create account</button>
        {saved && (
          <p role="status" className="text-sm leading-5 text-[var(--ds-color-success)]">Account created.</p>
        )}
      </div>
    </form>
  );
}""",
)

# 3. form-field-optional
register(
    "form-field-optional",
    title="Form Field Optional",
    subcategory="Labeling",
    description="Optional fields: a muted (optional) indicator on the label — the clear alternative to marking every required field when most of the form is required.",
    tags=TAGS_BASE + ["optional", "labeling"],
    features=FEAT_BASE + ["optional indicator"],
    accessibility=A11Y_BASE + ["text-based optional indicator (not color alone)"],
    interactive=True,
    related=["form-field", "form-field-required"],
    usage="""<FormField>
  <FormFieldLabel optional>Company</FormFieldLabel>
  <FormFieldControl>
    <input name="company" />
  </FormFieldControl>
  <FormFieldHelper>We use this to tailor your invoice.</FormFieldHelper>
</FormField>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, HELPER_PROPS]),
    composition_note="`optional` lives on `FormFieldLabel` — it is a label indicator, not a control state, so the control itself stays untouched.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Guideline: when most fields in a form are required, mark the optional ones (`optional`); when most are optional, mark the required ones (`required` on `FormField`). The demo mixes both conventions so the indicators can be compared side by side.",
    tsx_header="""/**
 * DevSnips React Form Field — optional indicator.
 *
 * `optional` on `<FormFieldLabel>` renders a muted "(optional)" next to the
 * label text — real text, so the state is never communicated by styling
 * alone. The control is untouched (no attributes injected). Use it on the
 * optional fields of a mostly-required form; use `required` on
 * `<FormField>` for the inverse. Same compound core as the reference
 * `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  return (
    <div className="w-full max-w-md space-y-6">
      <FormField required>
        <FormFieldLabel>Email</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} type="email" placeholder="ada@example.com" />
        </FormFieldControl>
      </FormField>
      <FormField>
        <FormFieldLabel optional>Company</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} placeholder="DevSnips" />
        </FormFieldControl>
        <FormFieldHelper>We use this to tailor your invoice.</FormFieldHelper>
      </FormField>
      <FormField>
        <FormFieldLabel optional>Phone</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} type="tel" placeholder="+1 555 0100" />
        </FormFieldControl>
        <FormFieldHelper>Include the country code.</FormFieldHelper>
      </FormField>
    </div>
  );
}""",
)

# 4. form-field-with-description
register(
    "form-field-with-description",
    title="Form Field With Description",
    subcategory="Content",
    description="Supporting description text between the label and the control — frames the field's purpose and is linked to the control with aria-describedby.",
    tags=TAGS_BASE + ["description", "help-text"],
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["form-field", "form-field-with-helper", "form-field-with-error"],
    usage="""<FormField>
  <FormFieldLabel>Token name</FormFieldLabel>
  <FormFieldDescription>
    A descriptive name so you can revoke the right token later.
  </FormFieldDescription>
  <FormFieldControl>
    <input placeholder="ci-deploy" />
  </FormFieldControl>
</FormField>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, DESCRIPTION_PROPS]),
    composition_note="A description frames the field **before** the control (purpose, impact); a helper sits **below** it (format, constraints). Reach for `form-field-with-helper` for the latter.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo renders the same pattern over three different controls (input, select, textarea) — the description wiring is identical for each because `FormFieldControl` injects it.",
    tsx_header="""/**
 * DevSnips React Form Field — with description.
 *
 * `<FormFieldDescription>` renders muted supporting text that frames the
 * field before typing (purpose, impact). It registers its generated id with
 * the field, and `FormFieldControl` links it to the control with
 * `aria-describedby` — the attribute exists only while the description is
 * rendered, never dangling. Same compound core as the reference
 * `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  return (
    <div className="w-full max-w-md space-y-6">
      <FormField>
        <FormFieldLabel>Token name</FormFieldLabel>
        <FormFieldDescription>A descriptive name so you can revoke the right token later.</FormFieldDescription>
        <FormFieldControl>
          <input className={INPUT_CLS} placeholder="ci-deploy" />
        </FormFieldControl>
      </FormField>
      <FormField>
        <FormFieldLabel>Scopes</FormFieldLabel>
        <FormFieldDescription>Scopes limit what the token can read or change.</FormFieldDescription>
        <FormFieldControl>
          <select className={SELECT_CLS} defaultValue="read">
            <option value="read">Read-only</option>
            <option value="write">Read and write</option>
            <option value="admin">Admin</option>
          </select>
        </FormFieldControl>
      </FormField>
      <FormField>
        <FormFieldLabel>Notes</FormFieldLabel>
        <FormFieldDescription>Visible to every member of the workspace.</FormFieldDescription>
        <FormFieldControl>
          <textarea className={TEXTAREA_CLS} placeholder="Used by the staging deploy pipeline." />
        </FormFieldControl>
      </FormField>
    </div>
  );
}""",
)

# 5. form-field-with-helper
register(
    "form-field-with-helper",
    title="Form Field With Helper",
    subcategory="Content",
    description="Persistent helper text below the control — format and constraint hints, linked to the control with aria-describedby.",
    tags=TAGS_BASE + ["helper", "hint", "help-text"],
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["form-field", "form-field-with-description", "form-field-with-error"],
    usage="""<FormField>
  <FormFieldLabel>Password</FormFieldLabel>
  <FormFieldControl>
    <input type="password" autoComplete="new-password" />
  </FormFieldControl>
  <FormFieldHelper>At least 12 characters.</FormFieldHelper>
</FormField>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, HELPER_PROPS]),
    composition_note="Helper text is persistent guidance, not feedback — it never appears or disappears as the value changes. For validation feedback use `form-field-with-error` / `form-field-with-success`.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Helper text answers “how is this used” — character formats, constraints, defaults. Because it is linked with `aria-describedby`, screen readers announce it after the label when the control receives focus.",
    tsx_header="""/**
 * DevSnips React Form Field — with helper text.
 *
 * `<FormFieldHelper>` renders a persistent muted hint below the control
 * (format, constraints — “how is this used”). It registers its generated id
 * and is linked to the control with `aria-describedby`; unlike a
 * description it sits below the control, and unlike a message it never
 * appears or disappears with validation state. Same compound core as the
 * reference `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  return (
    <div className="w-full max-w-md space-y-6">
      <FormField required>
        <FormFieldLabel>Password</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} type="password" autoComplete="new-password" />
        </FormFieldControl>
        <FormFieldHelper>At least 12 characters.</FormFieldHelper>
      </FormField>
      <FormField>
        <FormFieldLabel>Username</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} placeholder="ada-byron" />
        </FormFieldControl>
        <FormFieldHelper>Lowercase letters, numbers, and dashes.</FormFieldHelper>
      </FormField>
      <FormField>
        <FormFieldLabel>Deploy key</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} placeholder="dk_live_…" />
        </FormFieldControl>
        <FormFieldHelper>Starts with dk_live_. Keep it secret.</FormFieldHelper>
      </FormField>
    </div>
  );
}""",
)

# 6. form-field-with-error
register(
    "form-field-with-error",
    title="Form Field With Error",
    subcategory="Feedback",
    description="Error state: a destructive message with an alert icon in a role=alert live region, aria-invalid on the control, and a destructive control border — cleared by removing the message.",
    tags=TAGS_BASE + ["error", "validation", "aria-invalid", "alert"],
    features=FEAT_BASE + ["role=alert", "aria-invalid wiring", "live validation demo"],
    accessibility=A11Y_BASE + ["role=\"alert\" error announcement", "aria-invalid on the control"],
    interactive=True,
    related=["form-field", "form-field-with-success", "form-field-required"],
    usage="""<FormField>
  <FormFieldLabel>Work email</FormFieldLabel>
  <FormFieldControl>
    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
  </FormFieldControl>
  {error && <FormFieldMessage tone="error">{error}</FormFieldMessage>}
</FormField>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, MESSAGE_PROPS]),
    composition_note="The error state is message-driven: render `<FormFieldMessage tone=\"error\">` while the value is invalid and the field wires `aria-invalid` + `aria-describedby` for you. Remove the message to clear the state.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo validates a live email field as you type (invalid format → error, valid → cleared) and shows a static server-side error (“already registered”) next to it. The demo controls style their invalid border with Tailwind's `aria-invalid:` variant, so the visual state follows the same attribute assistive technology reads.",
    tsx_header="""/**
 * DevSnips React Form Field — error state.
 *
 * Rendering `<FormFieldMessage tone="error">` puts the field into the error
 * state: the message is destructive text with an alert icon in a
 * `role="alert"` live region, its id is added to the control's
 * `aria-describedby`, and the control flips to `aria-invalid="true"` for as
 * long as the message is rendered. Remove the message to clear the state —
 * no separate `error` prop to keep in sync. State is carried by icon +
 * text + ARIA, never by color alone. Same compound core as the reference
 * `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  const [email, setEmail] = React.useState("");
  const invalid = email.length > 0 && !/^\\S+@\\S+\\.\\S+$/.test(email);
  return (
    <div className="w-full max-w-md space-y-6">
      <FormField>
        <FormFieldLabel>Work email</FormFieldLabel>
        <FormFieldDescription>Validated as you type.</FormFieldDescription>
        <FormFieldControl>
          <input
            className={INPUT_CLS}
            type="email"
            placeholder="ada@devsnips.dev"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FormFieldControl>
        {invalid && <FormFieldMessage tone="error">Enter a valid email address.</FormFieldMessage>}
      </FormField>
      <FormField>
        <FormFieldLabel>Invite email</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} type="email" defaultValue="ada@devsnips.dev" />
        </FormFieldControl>
        <FormFieldMessage tone="error">This email is already registered.</FormFieldMessage>
      </FormField>
    </div>
  );
}""",
)

# 7. form-field-with-success
register(
    "form-field-with-success",
    title="Form Field With Success",
    subcategory="Feedback",
    description="Success state: a success-token message with a check icon in a role=status live region, linked to the control with aria-describedby — positive validation feedback without color-only signaling.",
    tags=TAGS_BASE + ["success", "validation", "status"],
    features=FEAT_BASE + ["role=status", "polite live region"],
    accessibility=A11Y_BASE + ["role=\"status\" success announcement"],
    interactive=True,
    related=["form-field", "form-field-with-error"],
    usage="""<FormField>
  <FormFieldLabel>Username</FormFieldLabel>
  <FormFieldControl>
    <input value={name} onChange={(e) => setName(e.target.value)} />
  </FormFieldControl>
  {available && <FormFieldMessage tone="success">Username is available.</FormFieldMessage>}
</FormField>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, MESSAGE_PROPS]),
    composition_note="Success uses the same `FormFieldMessage` primitive as error — `tone=\"success\"` swaps the icon, color token, and live-region role. It never sets `aria-invalid`.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo checks username availability as you type (3+ characters → available) and shows a static verified-endpoint example. `role=\"status\"` is a polite live region, so the confirmation is announced without interrupting the user.",
    tsx_header="""/**
 * DevSnips React Form Field — success state.
 *
 * Rendering `<FormFieldMessage tone="success">` confirms a valid value:
 * success-token text with a check icon in a `role="status"` polite live
 * region, linked to the control with `aria-describedby`. It never touches
 * `aria-invalid` — that attribute belongs to the error state only. State is
 * carried by icon + text + ARIA, never by color alone. Same compound core
 * as the reference `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  const [name, setName] = React.useState("");
  const available = name.trim().length >= 3;
  return (
    <div className="w-full max-w-md space-y-6">
      <FormField>
        <FormFieldLabel>Username</FormFieldLabel>
        <FormFieldHelper>At least 3 characters.</FormFieldHelper>
        <FormFieldControl>
          <input
            className={INPUT_CLS}
            placeholder="ada-byron"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </FormFieldControl>
        {available && <FormFieldMessage tone="success">Username is available.</FormFieldMessage>}
      </FormField>
      <FormField>
        <FormFieldLabel>Webhook endpoint</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} type="url" defaultValue="https://api.devsnips.dev/hooks/deploys" />
        </FormFieldControl>
        <FormFieldMessage tone="success">Endpoint verified — events are flowing.</FormFieldMessage>
      </FormField>
    </div>
  );
}""",
)

# 8. form-field-disabled
register(
    "form-field-disabled",
    title="Form Field Disabled",
    subcategory="States",
    description="Disabled state: the control receives the native disabled attribute (out of the tab order, not editable) and the label is muted — driven from the FormField so composite controls work too.",
    tags=TAGS_BASE + ["disabled", "state"],
    features=FEAT_BASE + ["native disabled", "dynamic disable/enable"],
    accessibility=A11Y_BASE + ["native disabled attribute"],
    interactive=True,
    related=["form-field", "form-field-with-error", "form-field-group"],
    usage="""<FormField disabled>
  <FormFieldLabel>Account email</FormFieldLabel>
  <FormFieldControl>
    <input type="email" defaultValue="ada@devsnips.dev" />
  </FormFieldControl>
  <FormFieldHelper>Managed by your organization.</FormFieldHelper>
</FormField>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, HELPER_PROPS]),
    composition_note="`disabled` on `FormField` is forwarded to the wrapped control as the native attribute — including composite controls that forward props (the DevSnips contract).",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo pairs a statically disabled input + select with a dynamic one: a “Lock security settings” checkbox toggles `disabled` on a field wrapping a composite switch control, proving the wiring reaches through composition. Disabled fields are not submitted with the form — use read-only controls when the value must be submitted.",
    tsx_header="""/**
 * DevSnips React Form Field — disabled state.
 *
 * `disabled` on `<FormField>` forwards the native `disabled` attribute to
 * the wrapped control (out of the tab order, not editable, announced as
 * unavailable) and mutes the label. The prop flows through
 * `FormFieldControl`, so composite controls that forward props to their
 * underlying native element are disabled too. Same compound core as the
 * reference `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  const [locked, setLocked] = React.useState(true);
  return (
    <div className="w-full max-w-md space-y-6">
      <FormField disabled>
        <FormFieldLabel>Account email</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} type="email" defaultValue="ada@devsnips.dev" />
        </FormFieldControl>
        <FormFieldHelper>Managed by your organization.</FormFieldHelper>
      </FormField>
      <FormField disabled>
        <FormFieldLabel>Plan</FormFieldLabel>
        <FormFieldControl>
          <select className={SELECT_CLS} defaultValue="pro">
            <option value="free">Free</option>
            <option value="pro">Pro</option>
            <option value="team">Team</option>
          </select>
        </FormFieldControl>
      </FormField>
      <label className={CHOICE_ROW_CLS}>
        <input type="checkbox" className={CHOICE_CLS} checked={locked} onChange={(e) => setLocked(e.target.checked)} />
        Lock security settings
      </label>
      <FormField disabled={locked}>
        <FormFieldLabel>Two-factor authentication</FormFieldLabel>
        <FormFieldControl>
          <DemoSwitch defaultChecked />
        </FormFieldControl>
        <FormFieldHelper>Unlock security settings to change this.</FormFieldHelper>
      </FormField>
    </div>
  );
}""",
)

# 9. form-field-group
register(
    "form-field-group",
    title="Form Field Group",
    subcategory="Composite",
    description="Related controls grouped in a real fieldset + legend, with group-level description and validation described to the whole group — plus a horizontal orientation for compact choice rows.",
    tags=TAGS_BASE + ["fieldset", "legend", "group", "checkbox", "radio"],
    features=FEAT_BASE + ["fieldset + legend", "group-level validation", "wrapping row orientation"],
    accessibility=A11Y_BASE + ["fieldset + legend group name", "group-level aria-describedby"],
    interactive=True,
    related=["form-field", "form-field-with-error", "form-field-horizontal"],
    usage="""<FormFieldGroup legend="Notification channels">
  <FormFieldDescription>Choose how you want to be notified.</FormFieldDescription>
  <label><input type="checkbox" name="channels" value="email" /> Email</label>
  <label><input type="checkbox" name="channels" value="push" /> Push</label>
  {noneSelected && (
    <FormFieldMessage tone="error">Select at least one channel.</FormFieldMessage>
  )}
</FormFieldGroup>""",
    props_doc="\n\n".join([GROUP_PROPS, DESCRIPTION_PROPS, HELPER_PROPS, MESSAGE_PROPS]),
    composition_note="Group-level texts (description, helper, message) register against the **fieldset**, while a `FormField` nested inside the group keeps its own per-control wiring — the nearest provider wins.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The demo groups notification-channel checkboxes with a live “select at least one” group error, and lays a radio plan-picker out in a wrapping horizontal row. Use a group for radios/checkboxes that share one question; use individual `FormField`s for unrelated fields.",
    tsx_header="""/**
 * DevSnips React Form Field — grouped controls.
 *
 * `<FormFieldGroup>` is a real `<fieldset>` + `<legend>`: related controls
 * (radios, checkboxes, address blocks) get a programmatic group name, and
 * `disabled` disables every descendant natively. Description / helper /
 * message primitives placed directly inside register against the fieldset
 * and are linked to it with `aria-describedby`; nested `<FormField>`
 * children keep their own wiring (nearest provider wins).
 * `orientation="horizontal"` lays the children out in a wrapping row.
 * Same compound core as the reference `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  const [channels, setChannels] = React.useState(["email"]);
  const toggle = (value) => setChannels((prev) =>
    prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
  );
  const noneSelected = channels.length === 0;
  const channelRow = (value, label) => (
    <label key={value} className={CHOICE_ROW_CLS}>
      <input type="checkbox" className={CHOICE_CLS} checked={channels.includes(value)} onChange={() => toggle(value)} />
      {label}
    </label>
  );
  return (
    <div className="w-full max-w-md space-y-6">
      <FormFieldGroup legend="Notification channels">
        <FormFieldDescription>Choose how you want to be notified.</FormFieldDescription>
        {channelRow("email", "Email")}
        {channelRow("push", "Push")}
        {channelRow("sms", "SMS")}
        {noneSelected && <FormFieldMessage tone="error">Select at least one channel.</FormFieldMessage>}
      </FormFieldGroup>
      <FormFieldGroup legend="Plan" orientation="horizontal">
        <label className={CHOICE_ROW_CLS}>
          <input type="radio" name="plan" className={CHOICE_CLS} defaultChecked />
          Free
        </label>
        <label className={CHOICE_ROW_CLS}>
          <input type="radio" name="plan" className={CHOICE_CLS} />
          Pro
        </label>
        <label className={CHOICE_ROW_CLS}>
          <input type="radio" name="plan" className={CHOICE_CLS} />
          Team
        </label>
        <FormFieldHelper>Change anytime.</FormFieldHelper>
      </FormFieldGroup>
    </div>
  );
}""",
)

# 10. form-field-horizontal
register(
    "form-field-horizontal",
    title="Form Field Horizontal",
    subcategory="Layout",
    description="Horizontal orientation: label in a fixed left column, control and supporting text on the right — a settings-page layout that collapses to the vertical stack below sm.",
    tags=TAGS_BASE + ["horizontal", "layout", "settings"],
    features=FEAT_BASE + ["horizontal label column", "collapses below sm"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["form-field", "form-field-group"],
    usage="""<FormField orientation="horizontal">
  <FormFieldLabel>Workspace name</FormFieldLabel>
  <FormFieldControl>
    <input defaultValue="DevSnips" />
  </FormFieldControl>
  <FormFieldHelper>Shown in the sidebar and on invoices.</FormFieldHelper>
</FormField>""",
    props_doc="\n\n".join([FIELD_PROPS, LABEL_PROPS, CONTROL_PROPS, DESCRIPTION_PROPS, HELPER_PROPS, MESSAGE_PROPS]),
    composition_note="In the horizontal layout the label takes the left column and everything else — control, description, helper, message — takes the right column, in source order. Place `FormFieldDescription` after the control for the classic settings-page alignment.",
    wiring_doc=WIRING_BASE,
    a11y_doc=A11Y_DOC,
    states_doc=STATES_BASE,
    responsive_doc="""From `sm` (640px) up, the root becomes a two-column grid: a `10rem` label column and a `minmax(0,1fr)` control column with a 16px gutter; the label is top-aligned with the 36px control via padding. Below `sm` the grid collapses to the single-column vertical stack — the label sits above the control, nothing clips, nothing overflows. The control column is `minmax(0,1fr)` so long inputs shrink correctly. Verified at 375 / 768 / 1280px with zero horizontal overflow.""",
    notes_doc="The demo is a workspace-settings panel: name, public URL (with helper), and visibility (with a description placed after the control). Resize below 640px to see every field collapse to the vertical stack.",
    tsx_header="""/**
 * DevSnips React Form Field — horizontal orientation.
 *
 * `orientation="horizontal"` puts the label in a fixed `10rem` left column
 * and the control + supporting text in a `minmax(0,1fr)` right column from
 * `sm` up (a settings-page layout); below `sm` the field collapses to the
 * single-column vertical stack, so labels never clip and controls never
 * overflow. The label is top-aligned with the 36px control. Same compound
 * core as the reference `form-field`.
 */""",
    showcase=CONTROLS_JS + """

function Showcase() {
  return (
    <div className="w-full max-w-2xl space-y-6">
      <FormField orientation="horizontal">
        <FormFieldLabel>Workspace name</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} defaultValue="DevSnips" />
        </FormFieldControl>
        <FormFieldHelper>Shown in the sidebar and on invoices.</FormFieldHelper>
      </FormField>
      <FormField orientation="horizontal">
        <FormFieldLabel>Public URL</FormFieldLabel>
        <FormFieldControl>
          <input className={INPUT_CLS} defaultValue="devsnips.dev/acme" />
        </FormFieldControl>
        <FormFieldHelper>Changing the URL breaks existing links.</FormFieldHelper>
      </FormField>
      <FormField orientation="horizontal">
        <FormFieldLabel>Visibility</FormFieldLabel>
        <FormFieldControl>
          <select className={SELECT_CLS} defaultValue="private">
            <option value="private">Private</option>
            <option value="workspace">Workspace</option>
            <option value="public">Public</option>
          </select>
        </FormFieldControl>
        <FormFieldDescription>Private workspaces are only visible to invited members.</FormFieldDescription>
      </FormField>
    </div>
  );
}""",
)
