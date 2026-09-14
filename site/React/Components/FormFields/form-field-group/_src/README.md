# Form Field Group

Related controls grouped in a real fieldset + legend, with group-level description and validation described to the whole group — plus a horizontal orientation for compact choice rows.

## Usage

```tsx
<FormFieldGroup legend="Notification channels">
  <FormFieldDescription>Choose how you want to be notified.</FormFieldDescription>
  <label><input type="checkbox" name="channels" value="email" /> Email</label>
  <label><input type="checkbox" name="channels" value="push" /> Push</label>
  {noneSelected && (
    <FormFieldMessage tone="error">Select at least one channel.</FormFieldMessage>
  )}
</FormFieldGroup>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<FormFieldGroup legend="Notification channels">
  <FormFieldDescription>Choose how you want to be notified.</FormFieldDescription>
  <label><input type="checkbox" name="channels" value="email" /> Email</label>
  <label><input type="checkbox" name="channels" value="push" /> Push</label>
  {noneSelected && (
    <FormFieldMessage tone="error">Select at least one channel.</FormFieldMessage>
  )}
</FormFieldGroup>
```

## Props

### `<FormFieldGroup>`

| Name | Type | Default | Description |
|---|---|---|---|
| `legend` | `ReactNode` | (required) | The group's accessible name, rendered as the `<legend>`. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | `horizontal` lays the children out in a wrapping row. |
| `disabled` | `boolean` | `false` | Native `fieldset` disabled — every descendant control is disabled. |
| `className` | `string` | — | Extra classes on the `<fieldset>`. |
| `children` | `ReactNode` | — | Controls, nested `FormField`s, and group-level texts. |

A real `<fieldset>` + `<legend>`. `FormFieldDescription` / `FormFieldHelper` / `FormFieldMessage` placed directly inside describe the whole group (linked with `aria-describedby` on the fieldset); nested `FormField` children keep their own wiring.

### `<FormFieldDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Description text. |

Muted supporting text that frames the field (purpose, impact). Registered with the nearest provider and linked with `aria-describedby` — the attribute is only set while the description is rendered.

### `<FormFieldHelper>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Helper text. |

Muted persistent hint below the control (format, constraints), linked with `aria-describedby`. For validation feedback use `FormFieldMessage`.

### `<FormFieldMessage>`

| Name | Type | Default | Description |
|---|---|---|---|
| `tone` | `"error" \| "success"` | (required) | `error`: destructive text + alert icon, `role="alert"`, and the control flips to `aria-invalid="true"`. `success`: success text + check icon, `role="status"`. |
| `className` | `string` | — | Extra classes on the `<p>`. |
| `children` | `ReactNode` | — | Message text. |

Render the message only while the state holds (e.g. `{error && <FormFieldMessage tone="error">{error}</FormFieldMessage>}`); removing it clears the wiring. State is carried by icon + text + ARIA — never by color alone.

## Composition

- `FormField` — the root provider. Owns the control id (generated or via `controlId`), the `required` / `disabled` / `orientation` state, and the registry that description, helper, and message texts register into.
- `FormFieldLabel` — a real `<label htmlFor>` pointing at the control. Renders the required indicator (`*` + sr-only text) when the field is required, or a muted "(optional)" when `optional` is set.
- `FormFieldControl` — wraps exactly one control element (native `<input>` / `<select>` / `<textarea>` or a DevSnips component that forwards props to its control) and injects the wiring: `id`, `aria-describedby`, `aria-invalid` (only while an error message is rendered), `required`, `disabled`.
- `FormFieldDescription` — muted supporting text framing the field; registered, then linked with `aria-describedby`.
- `FormFieldHelper` — muted persistent hint below the control; registered, then linked with `aria-describedby`.
- `FormFieldMessage` — validation feedback. `tone="error"` announces with `role="alert"` and flips the control to `aria-invalid="true"`; `tone="success"` announces politely with `role="status"`. An icon + text carry the state — never color alone.
- `FormFieldGroup` — a real `<fieldset>` + `<legend>` for related controls; texts placed directly inside describe the whole group. `disabled` disables every descendant control natively.
- `useFormField` — hook exposing the field wiring (control id, described-by ids, error / required / disabled) for building custom controls.

Group-level texts (description, helper, message) register against the **fieldset**, while a `FormField` nested inside the group keeps its own per-control wiring — the nearest provider wins.

## Field Wiring

`FormField` generates a control id (or takes `controlId`) and hands it to `FormFieldLabel` (`htmlFor`) and `FormFieldControl` (`id`), so the label/control association is automatic and can never dangle. `FormFieldDescription`, `FormFieldHelper`, and `FormFieldMessage` each generate their own id and **register** it with the nearest provider in an effect; only then does the control's `aria-describedby` reference those ids — the attribute is omitted entirely while no text is rendered, and removed ids are unregistered on unmount. `FormFieldControl` merges these ids with any `aria-describedby` the control already carries.

An error `FormFieldMessage` additionally flips the control to `aria-invalid="true"` for as long as it is rendered; removing the message clears both the described-by id and the invalid state. `required` / `disabled` on `FormField` are forwarded to the control as the **native** attributes, so constraint validation, form submission, and assistive-technology announcements behave natively.

The wiring is control-agnostic: `FormFieldControl` clones its single child and merges props, so native elements and DevSnips components (which forward these props to their underlying control) both work. Custom controls can read the same wiring through `useFormField()`.

## Accessibility

- Label ↔ control: `FormFieldLabel` is a real `<label>` whose `htmlFor` is the control's `id` — clicking the label focuses the control, and assistive technology announces the label as the control's accessible name.
- Descriptions, helpers, and messages are linked with `aria-describedby` **by registration**: ids are generated, registered, and only then referenced. There are no dangling ARIA references, and `aria-describedby` is omitted entirely when nothing describes the control.
- Error messages render `role="alert"` (announced immediately on appearance) and set `aria-invalid="true"` on the control; success messages render `role="status"` (politely announced). Both pair an icon with text, so state is never communicated by color alone.
- `required` is the native attribute (announced as required), plus a destructive `*` marked `aria-hidden` with an sr-only "(required)" fallback — the visual asterisk is never the only indicator.
- `disabled` is the native attribute: the control leaves the tab order and cannot be edited.
- `FormFieldGroup` is a real `<fieldset>` + `<legend>`, so grouped controls (radios, checkboxes) get a programmatic group name; group-level texts describe the whole fieldset via `aria-describedby`.

## States

- **Default** — foreground label, muted supporting text, control styled by its own component.
- **Required** — destructive `*` + sr-only "(required)" on the label; native `required` on the control.
- **Optional** — muted "(optional)" label indicator (a label choice, not a control state).
- **Disabled** — native `disabled` control (out of tab order, not editable) + muted label.
- **Error** — destructive message with alert icon, `role="alert"`, `aria-invalid="true"` on the control.
- **Success** — success-token message with check icon, `role="status"`.
- **Grouped** — `<fieldset>` + `<legend>`; group texts describe the whole group.

## Responsive Behavior

The default vertical layout stacks label, description, control, and helper/message in one column at every width — full-width, `min-w-0`, no overflow. `orientation="horizontal"` uses a `10rem` label column + `minmax(0,1fr)` control column from `sm` up and collapses to the single-column stack below `sm`, so labels are never clipped and controls never overflow on narrow screens. `FormFieldGroup orientation="horizontal"` lays children out in a wrapping row (`flex-wrap`), so choice rows reflow instead of overflowing. Verified at 375 / 768 / 1280px with zero horizontal overflow.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This form field variant uses the semantic color, typography, and spacing tokens — including `color.muted-foreground` for supporting text, `color.destructive` for the error state, `color.success` for the success state, and `color.focus-ring` on the wrapped control.

## Notes

The demo groups notification-channel checkboxes with a live “select at least one” group error, and lays a radio plan-picker out in a wrapping horizontal row. Use a group for radios/checkboxes that share one question; use individual `FormField`s for unrelated fields.
