# Navbar with Sidebar Mobile Panel

The desktop navbar collapses into a compact side panel on small screens: overlay dismissal, body scroll lock with scrollbar compensation, Escape close, focus-on-open, and focus restoration — without ever trapping focus.

## Installation

Copy `code.tsx` (TypeScript) or `code.jsx` (plain JavaScript) into your project — it is a single self-contained module with no dependencies beyond React. Make sure your app loads Tailwind CSS and the DevSnips `--ds-*` design tokens (see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md)); the component consumes the tokens through Tailwind arbitrary values such as `bg-[var(--ds-color-surface)]`. No component-specific CSS file is required.

## Usage

```tsx
import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>…</NavbarContent>
  <NavbarToggle />
  <NavbarMobile placement="side">
    <div className="flex h-14 items-center justify-between border-b border-[var(--ds-color-border)] px-4">
      <span>Forge</span>
      <NavbarToggle />
    </div>
    <NavbarMobileContent className="flex-1 overflow-y-auto">
      <NavbarItem><NavbarLink href="/overview" active>Overview</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarMobileContent>
  </NavbarMobile>
</Navbar>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>…</NavbarContent>
  <NavbarToggle />
  <NavbarMobile placement="side">
    <div className="flex h-14 items-center justify-between border-b border-[var(--ds-color-border)] px-4">
      <span>Forge</span>
      <NavbarToggle />
    </div>
    <NavbarMobileContent className="flex-1 overflow-y-auto">
      <NavbarItem><NavbarLink href="/overview" active>Overview</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarMobileContent>
  </NavbarMobile>
</Navbar>
```

## Props

### `<Navbar>`

| Name | Type | Default | Description |
|---|---|---|---|
| `open` | `boolean` | — | Mobile-menu open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial mobile-menu open state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the mobile menu requests to open or close. |
| `label` | `string` | `"Main"` | Accessible name of the `<nav>` landmark. |
| `breakpoint` | `"sm" \| "md" \| "lg"` | `"md"` | Breakpoint below which the desktop content collapses into the mobile navigation. |
| `variant` | `"default" \| "transparent"` | `"default"` | `transparent` removes the surface + bottom border for use over a page header. |
| `className` | `string` | — | Extra classes on the `<nav>` (e.g. `sticky top-0 z-40`). |
| `children` | `ReactNode` | — | Brand, content, toggle, and mobile region. |

### `<NavbarBrand>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | `"/"` | Home URL the brand points at. |
| `className` | `string` | — | Extra classes (e.g. desktop centering for the centered pattern). |
| `children` | `ReactNode` | — | Any brand content: logo mark, wordmark, or both. |

A real `<a>`; every native anchor attribute is forwarded.

### `<NavbarContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the desktop content row. |
| `children` | `ReactNode` | — | `NavbarSection` regions (and, for the centered pattern, the brand). |

Hidden below the root `breakpoint` via a Tailwind responsive utility.

### `<NavbarSection>`

| Name | Type | Default | Description |
|---|---|---|---|
| `align` | `"start" \| "center" \| "end"` | `"start"` | Region of the bar: after the brand, centered, or trailing. |
| `className` | `string` | — | Extra classes on the region. |
| `children` | `ReactNode` | — | `NavbarItem` list items. |

Renders a `<ul role="list">` so the navigation region keeps list semantics.

### `<NavbarItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the item. |
| `children` | `ReactNode` | — | One `NavbarLink`, `NavbarAction`, or `NavbarDropdown`. |

A plain `<li>` wrapper — links, actions, and dropdowns are list items in both the desktop sections and the mobile region.

### `<NavbarLink>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | `"#"` | Navigation target. |
| `active` | `boolean` | `false` | Current page: `aria-current="page"` + the active surface. |
| `external` | `boolean` | `false` | Opens in a new tab (`target="_blank" rel="noreferrer"`) with a visible + sr-only indicator. |
| `disabled` | `boolean` | `false` | Renders a non-interactive `aria-disabled` span — never a dead anchor. |
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Visible label. |

A real `<a>`. Inside `NavbarMobileContent` it automatically switches to full-width stacked styling; activating it also closes an open mobile menu.

### `<NavbarAction>`

| Name | Type | Default | Description |
|---|---|---|---|
| `variant` | `"primary" \| "outline" \| "ghost"` | `"primary"` | Visual weight. |
| `href` | `string` | — | When present, renders a real `<a>` (e.g. a "Get started" link); otherwise a real `<button type="button">`. |
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Visible label. |

Bar-height (36px) action sharing the Buttons family's primary/outline/ghost language. Native button or anchor attributes are forwarded.

### `<NavbarToggle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | `"Open/Close navigation menu"` (state-dependent) | Accessible name override. |
| `className` | `string` | — | Extra classes. |

A real `<button type="button">` with `aria-expanded` and `aria-controls` pointing at the mobile region; visible only below the root `breakpoint`. The hamburger/close icon swaps with state (aria-hidden).

### `<NavbarMobile>`

| Name | Type | Default | Description |
|---|---|---|---|
| `placement` | `"panel" \| "side"` | `"panel"` | `panel`: full-width disclosure under the bar. `side`: compact side panel with overlay, body scroll lock, and focus-on-open. |
| `className` | `string` | — | Extra classes on the region. |
| `children` | `ReactNode` | — | `NavbarMobileContent` (plus, for `side`, an optional header row). |

Rendered only while the mobile menu is open; the element carries the id the toggle's `aria-controls` points at. Hidden at and above the root `breakpoint`.

### `<NavbarMobileContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the list. |
| `children` | `ReactNode` | — | `NavbarItem` list items. |

A `<ul role="list">`; marks its subtree as the mobile area so `NavbarLink` renders stacked full-width.

### `<NavbarDropdown>`

| Name | Type | Default | Description |
|---|---|---|---|
| `defaultOpen` | `boolean` | `false` | Initial open state (uncontrolled — the dropdown manages itself). |
| `placement` | `"bottom-start" \| "bottom-end"` | `"bottom-start"` | Panel alignment relative to the trigger; flips horizontally to stay in the viewport. |
| `className` | `string` | — | Extra classes on the relative wrapper. |
| `children` | `ReactNode` | — | `NavbarDropdownTrigger` + `NavbarDropdownContent`. |

### `<NavbarDropdownTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered aria-hidden). |
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Visible trigger label (a chevron is rendered after it). |

A real `<button type="button">` styled as a nav link, with `aria-haspopup="true"`, `aria-expanded`, and `aria-controls`. Click toggles; ArrowDown opens with the first item focused, ArrowUp with the last. Native button attributes (e.g. `aria-label` for icon-forward triggers) are forwarded.

### `<NavbarDropdownContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `aria-label` | `string` | — | Explicit accessible name; otherwise the panel is labelled by its trigger. |
| `className` | `string` | — | Extra classes (e.g. a wider `w-[min(36rem,100vw-2rem)]` for a mega menu). |
| `children` | `ReactNode` | — | `NavbarDropdownItem` entries, `NavbarDivider`, or grouped columns. |

Rendered only while open. Measures itself before paint and flips start ↔ end to stay in the viewport.

### `<NavbarDropdownItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | — | Navigation target. When omitted, the item renders a `<button>` action instead of an anchor. |
| `active` | `boolean` | `false` | Current page: `aria-current="page"` + the active surface. |
| `external` | `boolean` | `false` | Opens in a new tab with a visible + sr-only indicator. |
| `disabled` | `boolean` | `false` | Non-interactive `aria-disabled` span — skipped by arrow keys. |
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered aria-hidden). |
| `onSelect` | `() => void` | — | Called on activation before the dropdown closes. |
| `aria-label` | `string` | — | Accessible name override. |
| `children` | `ReactNode` | — | Visible label. |

### `<NavbarDivider>`

A `role="separator"` horizontal rule between dropdown groups. No props beyond `className`.

## Compound Components

Navbar is a compound component. Fifteen primitives compose the pattern:

```tsx
<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>
    <NavbarSection align="start">
      <NavbarItem><NavbarLink href="/docs" active>Docs</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarSection>
    <NavbarSection align="end">
      <NavbarItem><NavbarAction variant="ghost">Sign in</NavbarAction></NavbarItem>
      <NavbarItem><NavbarAction variant="primary" href="/signup">Get started</NavbarAction></NavbarItem>
    </NavbarSection>
  </NavbarContent>
  <NavbarToggle />
  <NavbarMobile>
    <NavbarMobileContent>
      <NavbarItem><NavbarLink href="/docs" active>Docs</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarMobileContent>
  </NavbarMobile>
</Navbar>
```

- `Navbar` — the root `<nav>` landmark. Owns the mobile-menu state (controlled via `open` + `onOpenChange`, or uncontrolled via `defaultOpen`), the landmark label, the responsive `breakpoint`, and the `default` / `transparent` surface variant.
- `NavbarBrand` — a real `<a>` home link wrapping any ReactNode brand (logo mark, wordmark, or both).
- `NavbarContent` — the desktop content row, hidden below the breakpoint. Contains `NavbarSection` regions.
- `NavbarSection` — a `<ul>` region aligned `start`, `center`, or `end`; its children are `NavbarItem` list items.
- `NavbarItem` — a `<li>` wrapping one link, action, or dropdown.
- `NavbarLink` — a real `<a>` navigation link with `active` (`aria-current="page"`), `external` (`target="_blank"` + indicator), and `disabled` (non-interactive `aria-disabled` span — never a dead anchor).
- `NavbarAction` — a bar-height action: a real `<button>` by default, a real `<a>` when `href` is passed. `primary` / `outline` / `ghost` variants.
- `NavbarToggle` — the mobile-menu button: `aria-expanded`, `aria-controls` pointing at the mobile region, dynamic accessible name, hamburger/close icon swap.
- `NavbarMobile` — the collapsible mobile region referenced by `aria-controls`. `placement="panel"` (full-width disclosure under the bar) or `placement="side"` (compact side panel with overlay, scroll lock, and focus-on-open).
- `NavbarMobileContent` — the `<ul>` inside the mobile region; links inside it automatically switch to full-width stacked styling.
- `NavbarDropdown` — a navigation dropdown root (disclosure pattern). Owns its open state and panel placement.
- `NavbarDropdownTrigger` — a real `<button>` styled as a nav link, with `aria-haspopup="true"`, `aria-expanded`, `aria-controls`, and a rotating chevron.
- `NavbarDropdownContent` — the absolutely positioned panel, labelled by its trigger. Rendered only while open; flips its alignment to stay in the viewport.
- `NavbarDropdownItem` — one entry: a real `<a>` when `href` is passed, otherwise a real `<button>` action. Supports `active`, `external`, `disabled`, `icon`, and `onSelect`.
- `NavbarDivider` — a `role="separator"` rule between dropdown groups.

Same composition as the standard mobile menu with `placement="side"` on `NavbarMobile`. The side panel conventionally adds a header row (brand + a second `NavbarToggle` acting as the close button) — both toggles share the same state, so either one closes the panel.

## Navigation Behavior

The side panel behaves like a compact navigation drawer while staying a disclosure, not a dialog:

- **Open** — the bar toggle discloses a fixed 18rem panel on the leading edge with an overlay over the page. Focus moves into the panel (its first focusable element) so keyboard users land inside it.
- **Close** — Escape (from anywhere), the overlay (pointer down), the panel's own close toggle, the bar toggle, or activating a link. Focus returns to the bar toggle.
- **Body interaction** — page scroll is locked while the panel is open, with scrollbar-width `padding-right` compensation so the page does not shift horizontally.
- **No focus trap** — Tab always moves forward naturally. A navigation panel is not a modal dialog; if you need modality, use the Dialog family.

The panel is 18rem wide and capped at `100vw - 4rem`, so a strip of the page (and the overlay) always remains visible as a dismissal affordance.

## Keyboard Interaction

| Key | Context | Behavior |
|---|---|---|
| `Tab` / `Shift+Tab` | bar | Move through brand, links, actions, dropdown triggers, and the toggle in DOM order |
| `Enter` / `Space` | dropdown trigger | Toggle the dropdown; focus moves to the first item |
| `ArrowDown` | dropdown trigger | Open the dropdown, focus the first item |
| `ArrowUp` | dropdown trigger | Open the dropdown, focus the last item |
| `ArrowDown` / `ArrowUp` | dropdown panel | Move focus to the next / previous enabled item, wrapping at the ends |
| `Home` / `End` | dropdown panel | Focus the first / last enabled item |
| `Enter` | link / item | Follow the link / activate the item (native behavior) |
| `Escape` | dropdown panel | Close the dropdown and return focus to its trigger |
| `Tab` | dropdown panel | Close the dropdown and move focus forward naturally |
| `Escape` | anywhere (mobile menu open) | Close the mobile navigation and return focus to the toggle |

The trigger, items, and toggle are native `<button>` / `<a>` elements, so Enter/Space activation and Tab order follow normal browser behavior. Disabled entries use non-interactive `aria-disabled` spans: they are skipped by arrow-key navigation and removed from the tab order. Focus is never trapped — the mobile navigation is a disclosure, not a modal dialog.

## Accessibility

The structure follows the WAI-ARIA disclosure navigation pattern.

- The root is a semantic `<nav>` landmark with an accessible name (`label`, default "Main") — pass a distinct label when more than one navbar is on the page.
- Navigation links are real `<a href>` elements (normal browser navigation, middle-click, and screen-reader link semantics); actions and toggles are real `<button>` elements. No `div` click handlers, no nested interactive elements.
- The mobile toggle is a real `<button>` with `aria-expanded` and `aria-controls` pointing at the actual mobile region; its accessible name reflects the state ("Open/Close navigation menu").
- Dropdown triggers carry `aria-haspopup="true"` + `aria-expanded` + `aria-controls`; the panel is labelled by its trigger. Navigation dropdowns intentionally do NOT use `role="menu"`/`role="menuitem"` — the panel contains real links, and the ARIA menu pattern is for action menus, not navigation.
- The mobile navigation is NOT a modal dialog: focus is never trapped. The `side` placement moves focus into the panel on open and restores it to the toggle on close, but Tab always moves forward naturally.
- Disabled links and dropdown items render as non-interactive spans with `aria-disabled="true"` — they are skipped by arrow keys, removed from the tab order, and never presented as followable links.
- External links announce themselves with `target="_blank" rel="noreferrer"`, a visible (aria-hidden) indicator glyph, and screen-reader-only "(opens in a new tab)" text.
- Every interactive element has a visible `focus-visible` ring via the `--ds-color-focus-ring` token, and all transitions are disabled under `prefers-reduced-motion`.

The overlay is a non-focusable, aria-hidden dismissal surface (pointer-only), mirroring the Dialog family's overlay; the panel keeps the region id the toggle's `aria-controls` references. Focus-on-open lands inside the panel and restoration returns it to the bar toggle, so focus is never stranded.

## Active Navigation

Pass `active` to the `NavbarLink` or `NavbarDropdownItem` that represents the current page. Active items render with the `--ds-color-surface-active` background and foreground text (background + color, never color alone) and expose `aria-current="page"` to assistive technology. In a routed app, derive `active` from the current route:

```tsx
<NavbarLink href="/docs" active={pathname.startsWith("/docs")}>Docs</NavbarLink>
```

Exactly one item in a navigation region should be current at a time.

## Responsive Behavior

The family collapses by breakpoint, not by JavaScript width detection: below the configured `breakpoint` (`sm` / `md` / `lg`, default `md`) `NavbarContent` is hidden with a Tailwind responsive utility and the `NavbarToggle` appears; the `NavbarMobile` region is likewise hidden at and above the breakpoint. No resize listeners are involved.

- The bar is a single 56px row (`h-14`) with `max-w-6xl` content width and fluid horizontal padding (`px-4 sm:px-6`); long link labels truncate (`min-w-0` + `truncate`) instead of forcing overflow.
- The `panel` mobile placement is absolutely positioned under the bar, so opening/closing it never shifts page layout; it caps its height at `100dvh - 4rem` and scrolls internally.
- Dropdown panels cap their width at `100vw - 1.5rem` and height at `min(24rem, 100dvh - 6rem)` with internal scrolling, and flip their horizontal alignment (start ↔ end) to stay inside the viewport.
- All controls keep comfortable touch targets: 36px (h-9) actions/toggles, 32px+ link hit areas.

The side panel is the mobile navigation — it only exists below the `md` breakpoint (both panel and overlay carry `md:hidden`). At 375px the panel takes 18rem of the 23.4rem viewport, leaving a visible overlay strip; at 768px the desktop row returns.

## Controlled and Uncontrolled State

The mobile menu supports both state modes:

- **Uncontrolled** (default) — `<Navbar>` owns the state; optionally seed it with `defaultOpen`.
- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state. Every internal request (toggle click, Escape, outside pointer, link activation) flows through `onOpenChange`.

```tsx
const [open, setOpen] = useState(false);
<Navbar open={open} onOpenChange={setOpen}>…</Navbar>
```

`NavbarDropdown` manages its own open state internally (seed with `defaultOpen`); it closes itself on selection, Escape, Tab, or outside pointer interaction, and restores focus to its trigger.

The mobile menu is uncontrolled; pass `open` + `onOpenChange` to the root to own it (see `navbar-with-mobile-menu`).

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This navbar variant uses the semantic color, radius, shadow, typography, and motion tokens, and follows the navigation rules (48–56px top-nav height, subtle bottom border, quiet state changes).

## Notes and Limitations

The two toggles share one state and one ref-claim: the bar toggle permanently owns the focus-restore target, so closing from the panel's own toggle still returns focus correctly. Scroll lock + compensation are released on close or unmount.

- The desktop content collapses purely through Tailwind responsive utilities at the configured `breakpoint` (default `md`); there is no JavaScript width detection. If the viewport is resized past the breakpoint while the mobile menu is open, the region hides visually while the state remains open — close it via the toggle or Escape before resizing, or manage `open` yourself.
- The mobile navigation is a disclosure, not a dialog: focus is never trapped, even in the `side` placement. If you need a true modal navigation drawer, compose the DevSnips Dialog family instead.
- Dropdown panels anchor to their trigger with `absolute` positioning inside a `relative` wrapper — no positioning library. The viewport flip covers horizontal overflow; a navbar at the very bottom edge of a short viewport can still clip a tall panel vertically (the panel caps its height and scrolls internally instead).
