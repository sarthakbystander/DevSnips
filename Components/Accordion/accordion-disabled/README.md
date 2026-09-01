# Disabled Accordion Items

Items disabled at the `<AccordionItem>` level: the trigger renders as a natively disabled button — unfocusable, not activatable by pointer or keyboard, exposed as disabled to assistive technology, and skipped by Tab. Disabled items can never open.

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

<Accordion type="single" defaultValue="staging">
  <AccordionItem value="staging">
    <AccordionTrigger>Staging</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
  <AccordionItem value="production" disabled>
    <AccordionTrigger>Production</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
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

<Accordion type="single" defaultValue="staging">
  <AccordionItem value="staging">
    <AccordionTrigger>Staging</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
  <AccordionItem value="production" disabled>
    <AccordionTrigger>Production</AccordionTrigger>
    <AccordionContent>…</AccordionContent>
  </AccordionItem>
</Accordion>
```

## Props

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

`disabled` lives on `AccordionItem`, not the trigger — disabling is a property of the whole entry. Pair a disabled item with a visible reason (in the trigger text or adjacent copy) so the state is never a mystery.

## Behavior

Passing `disabled` to an `AccordionItem` disables the whole entry. The trigger renders with the native `disabled` attribute, which gives the correct behavior for free: the button cannot be clicked, cannot be activated with Enter/Space, is removed from the Tab order, and is announced as disabled (dimmed/unavailable) by screen readers.

The toggle handler also guards against disabled items, so even a programmatic toggle request is refused — a disabled item cannot open through any path. Native `disabled` is used instead of `aria-disabled` because the item must be inert, not merely announced as disabled.

## Keyboard Interaction

Accordion triggers are real `<button type="button">` elements, so the keyboard model is the native button model: Tab moves focus through the triggers and through any interactive elements inside open regions, and Enter or Space toggles the focused item. Disabled triggers are natively `disabled`, so Tab skips them entirely and they cannot be activated by pointer or keyboard.

Arrow-key navigation and roving tabindex are deliberately NOT implemented: the WAI-ARIA accordion pattern marks them as optional, and triggers that behave like ordinary buttons keep Tab order predictable — every focusable element stays exactly one Tab stop.

A disabled trigger is removed from the Tab order entirely (native `disabled`), so keyboard users skip over it rather than landing on a control that does nothing.

## Accessibility

- Every trigger is a real `<button type="button">` with `aria-expanded` and `aria-controls` referencing its region's stable id; the region is `role="region"` with `aria-labelledby` pointing back at the trigger. Both ids derive from the accordion instance's `useId` base plus the item's `value`, so multiple accordions (including nested ones) never collide.
- The trigger sits inside an `<h3>` heading, so the accordion participates in the page outline.
- The leading `icon` and the trailing chevron are `aria-hidden="true"` — state is exposed by `aria-expanded`, never by the glyph. The `badge` pill is plain text inside the button and joins the accessible name; keep it short and meaningful (for example `"3 errors"`, not a bare `"!"`).
- The closed region uses the CSS `visibility` transition: while closed it is `visibility: hidden`, which removes it from the accessibility tree AND the tab order — collapsed content can never be announced or focused.
- Disabled items use the native `disabled` attribute: the state is exposed to assistive technology and the trigger leaves the tab order. No redundant `aria-disabled`.

- The demo pairs each disabled item with a visible reason (`requires approval` / `Enterprise plan`), because a control that is merely grey invites confusion. The 50% opacity is a supplement, never the only signal.

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

- Prefer `disabled` over hiding the item when the user should know the section exists but cannot use it yet.
- `disabled` is per-item; disabling every item of an accordion is valid but usually means the whole section should be hidden instead.
- Every visual value comes from the `--ds-*` semantic tokens; light and dark themes flip through the same token block. No component-specific CSS file, no inline styles, no hardcoded hex.
