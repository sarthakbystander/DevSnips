"""Registry for the DevSnips React Textareas generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs.
The generator (``_gen_react_textareas.py``) reads each component's ``code.tsx``
from disk and combines it with the spec here to write ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented content only (project description, bug report,
release notes, internal notes, feedback, support message, commit message,
documentation summary). No lorem ipsum, no marketing buzzwords.
"""
from _gen_react_textareas import register

FEAT = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic HTML", "keyboard accessible", "native form control"]
A11Y = ["focus-visible", "keyboard accessible", "semantic HTML", "native textarea", "associated labels", "ARIA"]

# Shared props table for the base textarea control.
BASE_PROPS = """| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |
| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled value. |
| `onChange` | `(event) => void` | — | Native change callback. |
| `rows` | `number` | `3` | Visible rows — the natural height floor (with `min-h-[80px]`). |
| `placeholder` | `string` | — | Muted placeholder (never critical information). |
| `disabled` | `boolean` | — | Native disabled — not focusable, not submitted. |
| `readOnly` | `boolean` | — | Native read-only — focusable, selectable, submitted. |
| `required` / `name` / `id` | `boolean` / `string` | — | Native form semantics (`id` also the label `htmlFor`). |
| `minLength` / `maxLength` | `number` | — | Native length constraints. |
| `className` | `string` | — | Extra Tailwind classes merged onto the control. |
| other native props / `aria-*` | — | — | Passed through to the `<textarea>`. |"""

# 1. textarea (reference)
register(
    "textarea",
    title="Textarea",
    subcategory="Core",
    description="Native multi-line textarea styled to the DevSnips input visual language — the reference for the whole family.",
    tags=["textarea", "form", "input", "text", "multiline", "content", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["textarea-with-label", "textarea-with-helper", "textarea-disabled", "textarea-readonly"],
    props_doc={
        "export_name": "Textarea",
        "usage": '<Textarea label="Project description" placeholder="What does this project do?" rows={4} />',
        "table": BASE_PROPS,
    },
    behavior_doc="A real native `<textarea>` styled with Tailwind + the `--ds-*` semantic tokens. Default / hover / focus / focus-visible / filled / disabled / read-only states all come from native pseudo-classes; dark mode follows the token theme. Vertical resize stays enabled (the intentional DevSnips resize behavior — horizontal resize is off so layouts never break). Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) usage work natively with no duplicated state.",
    a11y_doc="Real `<textarea>` element — full native keyboard interaction, selection, copy/paste, and form semantics are preserved. Pass `label` for a visible `<label htmlFor>` or `aria-label`/`aria-labelledby` for a bare control. Supporting text uses `aria-describedby`. Visible `focus-visible` ring from `--ds-color-focus-ring`. Disabled uses the real `disabled` attribute; read-only uses real `readOnly`.",
    notes_doc="This is the reference implementation for the Textareas family — it establishes the shared full-width layout, `min-h-[80px]` floor, `px-3 py-2` padding, `text-sm` typography, `radius-sm`, 1px `color.border`, `color.input` background, muted placeholder, focus ring, `resize-y` behavior, disabled/read-only treatments, and dark-mode behavior that every other textarea extends.",
    showcase="""function Showcase() {
  const [notes, setNotes] = React.useState("Draft saved automatically.");
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <Textarea label="Project description" placeholder="What does this project do?" rows={4} />
      <Textarea label="Internal notes" value={notes} onChange={(e) => setNotes(e.target.value)} rows={3} />
      <Textarea aria-label="Quick note (bare control, labelled with aria-label)" placeholder="Write a quick note…" />
    </div>
  );
}""",
)

# 2. textarea-with-label
register(
    "textarea-with-label",
    title="Textarea With Label",
    subcategory="Labeling",
    description="Textarea with a properly associated visible label — clicking the label focuses the field.",
    tags=["textarea", "form", "input", "text", "multiline", "label", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["textarea", "textarea-with-description", "textarea-with-helper", "textarea-with-error"],
    props_doc={
        "export_name": "TextareaWithLabel",
        "usage": '<TextareaWithLabel label="Support message" required rows={4} />',
        "table": BASE_PROPS.replace("`label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |", "`label` | `ReactNode` (required) | — | Visible label above the control. |"),
    },
    behavior_doc="Same native textarea as the reference, but `label` is required and always rendered as `<label htmlFor>` above the control, so clicking the label text activates the field. Renders a `*` when `required` (the native `required` attribute carries the semantics; the asterisk is `aria-hidden`).",
    a11y_doc="`<label htmlFor>` association gives the control an accessible name and a larger click target. `required` is the native attribute (form validation + SR announcement); the visible asterisk is decorative and hidden from assistive tech. Visible `focus-visible` ring.",
    notes_doc="Use this when the field needs only a label. Reach for `textarea-with-description` when the user needs context before typing, or `textarea-with-helper` when guidance belongs below the field.",
    showcase="""function Showcase() {
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaWithLabel label="Support message" required rows={4} placeholder="Describe what you were trying to do when it broke." />
      <TextareaWithLabel label="Release notes" rows={3} placeholder="What changed since the last release?" />
      <TextareaWithLabel label="Commit message" rows={2} placeholder="fix: retry webhook delivery after timeout" />
    </div>
  );
}""",
)

# 3. textarea-with-description
register(
    "textarea-with-description",
    title="Textarea With Description",
    subcategory="Labeling",
    description="Textarea with a strong label plus a supporting description above the field, wired via aria-describedby.",
    tags=["textarea", "form", "input", "text", "multiline", "description", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["textarea-with-label", "textarea-with-helper", "textarea-with-error"],
    props_doc={
        "export_name": "TextareaWithDescription",
        "usage": '<TextareaWithDescription label="Bug report" description="Include steps to reproduce and what you expected to happen." rows={5} />',
        "table": BASE_PROPS.replace("`label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |", "`label` | `ReactNode` (required) | — | Visible label above the control. |") + "\n| `description` | `ReactNode` (required) | — | Supporting description linked with `aria-describedby`. |",
    },
    behavior_doc="Native textarea with a label and a muted description block stacked between the label and the control. The description frames the field before typing — what to include, the expected format, who will read it. It is linked to the control with `aria-describedby`.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={descriptionId}` on the native textarea, so screen readers announce both the name and the description. Visible `focus-visible` ring.",
    notes_doc="Use this when the field needs a sentence of explanation before the user starts typing — e.g. a bug report that needs repro steps, or a documentation summary with an expected scope. For shorter after-the-fact guidance, use `textarea-with-helper`.",
    showcase="""function Showcase() {
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaWithDescription label="Bug report" description="Include steps to reproduce, what you expected, and what actually happened." rows={5} placeholder="1. Open the deployment settings page…" />
      <TextareaWithDescription label="Documentation summary" description="Two or three sentences shown on the API reference index page." rows={3} />
    </div>
  );
}""",
)

# 4. textarea-with-helper
register(
    "textarea-with-helper",
    title="Textarea With Helper",
    subcategory="Labeling",
    description="Textarea with muted helper text below the field, wired via aria-describedby.",
    tags=["textarea", "form", "input", "text", "multiline", "helper", "hint", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["textarea-with-label", "textarea-with-description", "textarea-with-counter"],
    props_doc={
        "export_name": "TextareaWithHelper",
        "usage": '<TextareaWithHelper label="Feedback" helperText="Visible to the product team only." rows={4} />',
        "table": BASE_PROPS.replace("`label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |", "`label` | `ReactNode` (required) | — | Visible label above the control. |") + "\n| `helperText` | `ReactNode` (required) | — | Helper text below the control, linked with `aria-describedby`. |",
    },
    behavior_doc="Native textarea with a label above and muted helper text below the control. Helper text answers questions that come up while filling the field — visibility, formatting rules, what happens on submit. It is linked with `aria-describedby`.",
    a11y_doc="`<label htmlFor>` + `aria-describedby={helperId}` on the native textarea. The helper is plain text (not color-coded), so it reads the same for everyone. Visible `focus-visible` ring.",
    notes_doc="Description goes above the field (context before typing); helper goes below (guidance while typing). Do not stack both — pick the one that matches when the user needs the information.",
    showcase="""function Showcase() {
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaWithHelper label="Feedback" helperText="Visible to the product team only — never published." rows={4} placeholder="What worked, what didn't?" />
      <TextareaWithHelper label="Internal notes" helperText="Markdown is supported. @mention a teammate to notify them." rows={3} />
    </div>
  );
}""",
)

# 5. textarea-with-error
register(
    "textarea-with-error",
    title="Textarea With Error",
    subcategory="States",
    description="Textarea with a destructive error state and an associated inline message (aria-invalid + role=alert).",
    tags=["textarea", "form", "input", "text", "multiline", "error", "validation", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y + ["aria-invalid", "role=alert"],
    interactive=True,
    related=["textarea-with-label", "textarea-with-helper", "textarea-with-counter"],
    props_doc={
        "export_name": "TextareaWithError",
        "usage": '<TextareaWithError label="Bug report" error={message} rows={5} />',
        "table": BASE_PROPS.replace("`label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |", "`label` | `ReactNode` (required) | — | Visible label above the control. |") + "\n| `error` | `string` | — | Error message. When set: destructive border + `aria-invalid` + `role=\"alert\"` message. |",
    },
    behavior_doc="Native textarea with an inline error state driven by the `error` prop. While `error` is set the border switches to `color.destructive`, `aria-invalid=\"true\"` is applied, and the message renders below the field in a `role=\"alert\"` region linked with `aria-describedby`. Clearing `error` returns the field to the default state. The state is never color alone — the message text carries it.",
    a11y_doc="`aria-invalid=\"true\"` on the textarea while invalid; the message is a `role=\"alert\"` region associated with `aria-describedby`, so screen readers announce it when it appears. The visible message (`Error: …`) plus border means the state does not rely on red color alone. Visible `focus-visible` ring.",
    notes_doc="Keep the message specific and actionable (what is wrong + how to fix it). Validate on submit or blur — showing an error while the user is still typing their first characters is noise.",
    showcase="""function Showcase() {
  const [report, setReport] = React.useState("It broke.");
  const tooShort = report.length > 0 && report.length < 30;
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaWithError
        label="Bug report"
        rows={5}
        value={report}
        onChange={(e) => setReport(e.target.value)}
        error={tooShort ? "Add a little more detail — at least 30 characters so the team can reproduce it." : undefined}
      />
      <TextareaWithError
        label="Support message"
        rows={3}
        defaultValue=""
        error="Message is required before submitting."
      />
    </div>
  );
}""",
)

# 6. textarea-disabled
register(
    "textarea-disabled",
    title="Textarea Disabled",
    subcategory="States",
    description="Disabled textarea using the real native disabled attribute — not focusable, not submitted.",
    tags=["textarea", "form", "input", "text", "multiline", "disabled", "state", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["textarea", "textarea-readonly", "textarea-with-error"],
    props_doc={
        "export_name": "TextareaDisabled",
        "usage": '<TextareaDisabled label="Closure reason" defaultValue="Closed after the v2 migration completed." rows={3} />',
        "table": BASE_PROPS.replace("| `disabled` | `boolean` | — |", "| `disabled` | `boolean` | `true` |"),
    },
    behavior_doc="Native textarea with `disabled` defaulted to `true`. The native attribute does the work: the control leaves the tab order, cannot be focused or edited, and its value is NOT submitted with the form. The muted surface + reduced opacity come from the `:disabled` pseudo-class; the label gets a not-allowed cursor. Pass `disabled={false}` to flip it back to the normal reference textarea.",
    a11y_doc="Real `disabled` attribute — assistive tech announces the control as unavailable and skips it in the tab order. The value stays perceivable (readable muted text) rather than removed. Compare with `textarea-readonly`, which stays focusable and is submitted.",
    notes_doc="Use disabled for fields that are temporarily unavailable because of state (a closed ticket, a locked workspace). If the user should still be able to select and copy the text, use `textarea-readonly` instead.",
    showcase="""function Showcase() {
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaDisabled label="Closure reason" defaultValue="Closed after the v2 migration completed on Aug 12." rows={3} />
      <TextareaDisabled label="Workspace notes" placeholder="Unavailable on the Free plan." rows={3} />
    </div>
  );
}""",
)

# 7. textarea-readonly
register(
    "textarea-readonly",
    title="Textarea Readonly",
    subcategory="States",
    description="Read-only textarea using the real native readOnly attribute — focusable, selectable, submitted.",
    tags=["textarea", "form", "input", "text", "multiline", "readonly", "state", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["textarea", "textarea-disabled", "textarea-with-actions"],
    props_doc={
        "export_name": "TextareaReadonly",
        "usage": '<TextareaReadonly label="Generated summary" value={summary} rows={4} />',
        "table": BASE_PROPS.replace("| `readOnly` | `boolean` | — |", "| `readOnly` | `boolean` | `true` |"),
    },
    behavior_doc="Native textarea with `readOnly` defaulted to `true`. The value cannot be edited, but the control stays in the tab order, its text stays selectable and copyable, and its value IS submitted with the form. The subtle surface + muted text come from the `:read-only` pseudo-class — visually distinct from the muted `disabled` treatment. Pass `readOnly={false}` to flip it back.",
    a11y_doc="Real `readOnly` attribute — screen readers announce the field as read-only while it remains focusable, so the content is reachable and reviewable by keyboard users (unlike `disabled`, which is skipped). Visible `focus-visible` ring still applies.",
    notes_doc="Use read-only for values the user may inspect or copy but not change: a generated summary, an audit-trail entry, the rendered version of a template. Disabled and read-only are different states — this variant exists to keep that distinction honest.",
    showcase="""function Showcase() {
  const summary = "Sprint 34 closed 41 of 45 issues. The remaining four move to Sprint 35 with the billing webhook retries carrying over as the only blocker.";
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaReadonly label="Generated summary" value={summary} rows={4} />
      <TextareaReadonly label="Audit trail" defaultValue="2026-08-14 09:31 UTC — retention policy changed from 30 to 90 days by m.chen." rows={3} />
    </div>
  );
}""",
)

# 8. textarea-with-counter
register(
    "textarea-with-counter",
    title="Textarea With Counter",
    subcategory="Feedback",
    description="Textarea with a live character counter (current / maximum) derived from the real value.",
    tags=["textarea", "form", "input", "text", "multiline", "character-count", "counter", "maxlength", "react", "tailwind", "accessible", "native"],
    features=FEAT,
    accessibility=A11Y + ["aria-live counter"],
    interactive=True,
    related=["textarea-with-helper", "textarea-with-error", "textarea-with-actions"],
    props_doc={
        "export_name": "TextareaWithCounter",
        "usage": '<TextareaWithCounter label="Release notes" maxLength={280} helperText="Shown on the changelog page." rows={4} />',
        "table": BASE_PROPS.replace("`label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |", "`label` | `ReactNode` (required) | — | Visible label above the control. |") + "\n| `helperText` | `ReactNode` | — | Optional text beside the counter. |",
    },
    behavior_doc="Native textarea with a live character counter under the field. The count is computed from the actual value (controlled `value` or tracked uncontrolled text) — it updates on every keystroke and is never faked. When `maxLength` is supplied the counter reads `current / maximum` and the native attribute enforces the limit; at the limit the count gains weight + foreground color as a quiet, non-color-only cue. Without `maxLength` the counter is a plain character count.",
    a11y_doc="The counter region is linked with `aria-describedby` and marked `aria-live=\"polite\"`, so screen readers can read the count on demand and hear polite updates without focus theft. The at-limit cue is text weight + color together — not color alone. Native `maxLength` behavior (typing stops at the cap) is preserved.",
    notes_doc="Use for bounded content: changelog entries, status updates, short bios. For long-form content where a limit would be hostile, drop `maxLength` and keep the plain count, or use the plain `textarea`.",
    showcase="""function Showcase() {
  const [notes, setNotes] = React.useState("Added retry logic to the webhook dispatcher.");
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaWithCounter label="Release notes" rows={4} maxLength={280} helperText="Shown on the public changelog." value={notes} onChange={(e) => setNotes(e.target.value)} />
      <TextareaWithCounter label="Status update" rows={2} maxLength={120} defaultValue="Investigating elevated 5xx rates on the EU cluster." />
      <TextareaWithCounter label="Internal notes" rows={3} maxLength={undefined} placeholder="No limit — count only." />
    </div>
  );
}""",
)

# 9. textarea-auto-resize
register(
    "textarea-auto-resize",
    title="Textarea Auto Resize",
    subcategory="Behavior",
    description="Textarea that grows and shrinks with its content, capped at a configurable maximum height.",
    tags=["textarea", "form", "input", "text", "multiline", "auto-resize", "autogrow", "autosize", "react", "tailwind", "accessible", "native"],
    features=FEAT + ["auto-resize"],
    accessibility=A11Y,
    interactive=True,
    related=["textarea", "textarea-with-counter", "textarea-with-actions"],
    props_doc={
        "export_name": "TextareaAutoResize",
        "usage": '<TextareaAutoResize label="Commit message" maxHeight={240} rows={2} />',
        "table": BASE_PROPS + "\n| `maxHeight` | `number` | `320` | Height cap in px — the field scrolls past it instead of growing. |",
    },
    behavior_doc="Native textarea whose height tracks its content: it grows as lines are added, shrinks when they are removed, and stops at `maxHeight` (default 320px) where it scrolls. Measurement runs from the real value — initial content, uncontrolled typing, and controlled `value` updates all trigger it — plus once on viewport resize (wrapped lines reflow). Manual resize is disabled (`resize-none`) because the component owns the height; height changes are instant, so nothing animates and reduced-motion users see identical behavior. Without effects running it still renders as a normal `rows`-sized textarea.",
    a11y_doc="Same native semantics as the reference textarea — real focus, keyboard, selection, and form behavior. No live regions are needed because the resize is a visual nicety, not a state change. Visible `focus-visible` ring; `resize-none` is safe here because the field grows on its own.",
    notes_doc="Use for inputs where the content length varies wildly and scrolling a fixed box hides context: commit messages, review comments, support replies. Keep `maxHeight` sane so a paste of 500 lines cannot push the rest of the form off-screen.",
    showcase="""function Showcase() {
  const [msg, setMsg] = React.useState("fix: retry webhook delivery after timeout\\n\\nDeliveries that fail with a network error now retry up to 3 times with exponential backoff before surfacing in the failed-deliveries queue.");
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaAutoResize label="Commit message" rows={2} value={msg} onChange={(e) => setMsg(e.target.value)} />
      <TextareaAutoResize label="Feedback" rows={2} maxHeight={180} placeholder="Type several lines — the field grows, then scrolls past 180px." />
    </div>
  );
}""",
)

# 10. textarea-with-actions
register(
    "textarea-with-actions",
    title="Textarea With Actions",
    subcategory="Composite",
    description="Textarea with a contextual action bar — live character count plus real Clear and Copy buttons.",
    tags=["textarea", "form", "input", "text", "multiline", "actions", "clear", "copy", "character-count", "react", "tailwind", "accessible", "interactive"],
    features=FEAT + ["clear action", "copy-to-clipboard", "live character count"],
    accessibility=A11Y + ["aria-live feedback", "labelled action buttons"],
    interactive=True,
    related=["textarea-with-counter", "textarea-auto-resize", "textarea-readonly"],
    props_doc={
        "export_name": "TextareaWithActions",
        "usage": '<TextareaWithActions label="Support reply" maxLength={500} onCopy={(v) => console.log(v)} />',
        "table": BASE_PROPS.replace("`label` | `ReactNode` | — | Visible label (omit and pass `aria-label` for a bare control). |", "`label` | `ReactNode` (required) | — | Visible label above the control. |") + "\n| `clearLabel` / `copyLabel` / `copiedLabel` | `string` | `Clear` / `Copy` / `Copied` | Action labels. |\n| `resetMs` | `number` | `2000` | Delay before the copy label resets. |\n| `onClear` / `onCopy` | `() => void` / `(value) => void` | — | Action callbacks. |",
    },
    behavior_doc="Native textarea with an action bar below the field: a live character count on the left, and real Clear and Copy buttons on the right. Clear empties the value and returns focus to the field; Copy writes the current value to the clipboard (with a fallback for non-secure contexts) and confirms via a label swap + an `aria-live` status message. Both buttons disable while the field is empty, and both act on the real value in controlled and uncontrolled modes. The bar wraps on narrow screens.",
    a11y_doc="Both actions are real `<button type=\"button\">` elements with visible text labels, keyboard-operable, with visible `focus-visible` rings. Copy feedback is announced through a `role=\"status\"` / `aria-live=\"polite\"` region; the count is `aria-describedby` + polite live. Clear returns focus to the textarea so keyboard users are not stranded.",
    notes_doc="Every action here has a real job — clearing drafts and copying composed text. Do not add icon buttons for decoration; extend the bar only with actions that operate on the value (e.g. a template insert or a formatting command).",
    showcase="""function Showcase() {
  const [reply, setReply] = React.useState("Thanks for the report — I can reproduce this on 4.2.1. A fix ships in today's patch release; I'll confirm here once it is out.");
  return (
    <div className="grid gap-6" style={{maxWidth:560}}>
      <TextareaWithActions label="Support reply" rows={4} maxLength={500} value={reply} onChange={(e) => setReply(e.target.value)} onClear={() => setReply("")} />
      <TextareaWithActions label="Quick note" rows={3} placeholder="Compose, then copy or clear." />
    </div>
  );
}""",
)
