# Accordion with Actions

Accordion regions that contain real actions — buttons and links inside the expanded content. The trigger itself stays a single clean button (no nested controls); actions live in the region, where they are fully keyboard reachable and operable while the item is open.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Accordion, {
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
</Accordion>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Accordion, {
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
</Accordion>
```

## Props

### `<AccordionContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the inner content div (padding, typography overrides). |
| `children` | `ReactNode` | — | Region content — paragraphs, lists, real controls. |

The region element is `role="region"` with `aria-labelledby` pointing at its trigger; `className` and forwarded attributes (for example `aria-busy`) land on the inner content div. Content stays mounted while closed so state inside it survives a close/reopen cycle.

### `<AccordionItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` | required | Unique, id-safe identifier for the item within the accordion. It keys the open state and derives the trigger/region ids, so keep it stable and free of whitespace. |
| `disabled` | `boolean` | `false` | Disable the item: the trigger becomes natively `disabled` — unfocusable, not activatable, exposed as disabled to assistive technology. |
| `className` | `string` | — | Extra classes on the item div. |
| `children` | `ReactNode` | — | One `AccordionTrigger` + one `AccordionContent`. |

Every other attribute of a plain `<div>` is forwarded.

### `<AccordionTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Leading visual affordance, rendered `aria-hidden` — it supplements the trigger text, never replaces it. |
| `badge` | `ReactNode` | — | Short status/count content rendered as a neutral pill before the chevron. It is plain text inside the button, so it joins the accessible name — keep it short and meaningful. |
| `description` | `ReactNode` | — | A short supporting line under the title. Also part of the accessible name — keep it brief. |
| `onClick` | `(event) => void` | — | Runs before the toggle; call `event.preventDefault()` to veto it. |
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | The trigger title (required — it is the accessible name). |

The rendered element is a real `<button type="button">` wrapped in an `<h3>`; every other button attribute (`aria-*`, `data-*`, …) is forwarded. `disabled` is set on `<AccordionItem>`, not here.

## Composition

- `Accordion` — the root provider: owns the open-item state (controlled `value` + `onValueChange`, or uncontrolled `defaultValue`), picks the expansion mode (`type="single"` default, `type="multiple"`), and derives the stable per-instance id base every trigger/region pair is built from.
- `AccordionItem` — one entry in the divided list (`border-b`, removed on the last item). Requires a unique id-safe `value`; computes its own open state from the root and derives the trigger/region ids.
- `AccordionTrigger` — the disclosure control: a real `<button type="button">` inside an `<h3>` heading, with `aria-expanded` + `aria-controls`, an optional leading `icon` (`aria-hidden`), an optional trailing `badge` pill, an optional `description` line, and the rotating chevron (also `aria-hidden`).
- `AccordionContent` — the collapsible region: `role="region"` labelled by its trigger, animated with the CSS grid-rows trick (no JavaScript measurement), hidden from the accessibility tree and tab order while closed.

Compose only what an entry needs — a bare trigger + content pair is valid; so is the full icon + description + badge composition.

Compose actions from the DevSnips button treatments (the demo uses the family's small primary/outline/ghost/destructive classes) and real anchors. Never put a button inside `AccordionTrigger` — a control inside a control is invalid HTML and breaks both.

## Behavior

Regions are ordinary content containers, so real controls compose naturally: buttons trigger actions, anchors navigate. Because the closed region is removed from the tab order (`visibility: hidden`), keyboard users only ever reach the actions of open items — there are no ghost tab stops.

Actions stay reachable at every viewport: the demo wraps them in a `flex flex-wrap` row so they reflow onto multiple lines at 375px instead of overflowing. Focus rings on actions use the standard `color.focus-ring` token.

## Keyboard Interaction

Accordion triggers are real `<button type="button">` elements, so the keyboard model is the native button model: Tab moves focus through the triggers and through any interactive elements inside open regions, and Enter or Space toggles the focused item. Disabled triggers are natively `disabled`, so Tab skips them entirely and they cannot be activated by pointer or keyboard.

Arrow-key navigation and roving tabindex are deliberately NOT implemented: the WAI-ARIA accordion pattern marks them as optional, and triggers that behave like ordinary buttons keep Tab order predictable — every focusable element stays exactly one Tab stop.

Actions inside an open region are part of the normal Tab order: Tab from a trigger moves into its open region's first control, and Enter/Space activates it. When the item closes, its actions leave the tab order with it.

## Accessibility

- Every trigger is a real `<button type="button">` with `aria-expanded` and `aria-controls` referencing its region's stable id; the region is `role="region"` with `aria-labelledby` pointing back at the trigger. Both ids derive from the accordion instance's `useId` base plus the item's `value`, so multiple accordions (including nested ones) never collide.
- The trigger sits inside an `<h3>` heading, so the accordion participates in the page outline.
- The leading `icon` and the trailing chevron are `aria-hidden="true"` — state is exposed by `aria-expanded`, never by the glyph. The `badge` pill is plain text inside the button and joins the accessible name; keep it short and meaningful (for example `"3 errors"`, not a bare `"!"`).
- The closed region uses the CSS `visibility` transition: while closed it is `visibility: hidden`, which removes it from the accessibility tree AND the tab order — collapsed content can never be announced or focused.
- Disabled items use the native `disabled` attribute: the state is exposed to assistive technology and the trigger leaves the tab order. No redundant `aria-disabled`.

## States

- **Trigger (idle)** — `color.foreground` title, `color.muted-foreground` icon/chevron; hover applies a `color.surface-hover` wash; keyboard focus shows a 2px `color.focus-ring` outline drawn inset (`-outline-offset-2`) so it is never clipped by bordered containers.
- **Trigger (open)** — the chevron rotates 180° over 200ms (`motion-reduce` makes the flip instant); `aria-expanded` flips with it. The state is also visible in the open region below, never carried by color alone.
- **Trigger (disabled)** — native `disabled`: 50% opacity, no pointer events, removed from the tab order.
- **Region** — height animates with the CSS grid-rows trick (`0fr` ↔ `1fr`, 200ms, `ease-out`), and a discrete `visibility` transition hides closed content from the accessibility tree and tab order once the collapse completes. Under `prefers-reduced-motion` every transition is removed and state changes are instant.
- **Region content** — body-sm on `color.muted-foreground`; mounted in both states so component state inside a region survives a close/reopen cycle.

## Responsive Behavior

The accordion is fluid-width (`w-full min-w-0`) and fills its container at every viewport. Trigger titles and descriptions wrap (`break-words`), the text column is `flex-1 min-w-0`, and the icon, badge, and chevron are `shrink-0` so they never push text off-screen. Region content wraps and long words break. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`); no component-specific values are invented. Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This accordion follows the token system rules: 1px `color.border` dividers, `color.surface-hover` trigger feedback, body-sm text, the `color.focus-ring` token for keyboard focus (drawn inset so bordered containers never clip it), and `color.muted-foreground` for supporting text, icons, and badges.

## Notes

- Destructive actions (like Delete project below) should still confirm elsewhere — the accordion region is an entry point, not a confirmation pattern.
- Every visual value comes from the `--ds-*` semantic tokens; light and dark themes flip through the same token block. No component-specific CSS file, no inline styles, no hardcoded hex.
