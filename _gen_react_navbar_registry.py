"""Registry for the DevSnips React Navbar generator.

Each ``register()`` call adds one variant's metadata + showcase + README
docs + ``tsx_header`` (the header doc comment of its derived ``code.tsx`` —
the shared core is identical family-wide; the variants are distinct
navigation *patterns* expressed through composition of the same 15
primitives). The generator (``_gen_react_navbar.py``) combines the spec
here with the authored reference ``navbar/code.tsx`` to write ``code.tsx``
(derived), ``code.jsx``, ``preview.html``, ``metadata.json``, ``README.md``.

Realistic, product-oriented demo content only (a developer-focused component
library called "Forge": overview, components, templates, docs, pricing,
changelog). No lorem ipsum, no marketing buzzwords, no emoji.
"""
from _gen_react_navbar import register

TAGS_BASE = ["navbar", "navigation", "header", "react", "tailwind", "accessible", "keyboard", "responsive", "interactive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic nav landmark", "real anchors", "aria-current active item", "mobile disclosure", "keyboard navigation"]
A11Y_BASE = ["semantic nav landmark", "aria-current='page' active item", "aria-expanded + aria-controls toggle", "aria-haspopup dropdown triggers", "focus restoration on close", "aria-disabled inactive items", "focus-visible ring"]

# ---------------------------------------------------------------------------
# Shared props tables (identical API family-wide)
# ---------------------------------------------------------------------------

NAVBAR_PROPS = r"""### `<Navbar>`

| Name | Type | Default | Description |
|---|---|---|---|
| `open` | `boolean` | — | Mobile-menu open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial mobile-menu open state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the mobile menu requests to open or close. |
| `label` | `string` | `"Main"` | Accessible name of the `<nav>` landmark. |
| `breakpoint` | `"sm" \| "md" \| "lg"` | `"md"` | Breakpoint below which the desktop content collapses into the mobile navigation. |
| `variant` | `"default" \| "transparent"` | `"default"` | `transparent` removes the surface + bottom border for use over a page header. |
| `className` | `string` | — | Extra classes on the `<nav>` (e.g. `sticky top-0 z-40`). |
| `children` | `ReactNode` | — | Brand, content, toggle, and mobile region. |"""

BRAND_PROPS = r"""### `<NavbarBrand>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | `"/"` | Home URL the brand points at. |
| `className` | `string` | — | Extra classes (e.g. desktop centering for the centered pattern). |
| `children` | `ReactNode` | — | Any brand content: logo mark, wordmark, or both. |

A real `<a>`; every native anchor attribute is forwarded."""

CONTENT_SECTION_ITEM_PROPS = r"""### `<NavbarContent>`

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

A plain `<li>` wrapper — links, actions, and dropdowns are list items in both the desktop sections and the mobile region."""

LINK_PROPS = r"""### `<NavbarLink>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | `"#"` | Navigation target. |
| `active` | `boolean` | `false` | Current page: `aria-current="page"` + the active surface. |
| `external` | `boolean` | `false` | Opens in a new tab (`target="_blank" rel="noreferrer"`) with a visible + sr-only indicator. |
| `disabled` | `boolean` | `false` | Renders a non-interactive `aria-disabled` span — never a dead anchor. |
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Visible label. |

A real `<a>`. Inside `NavbarMobileContent` it automatically switches to full-width stacked styling; activating it also closes an open mobile menu."""

ACTION_PROPS = r"""### `<NavbarAction>`

| Name | Type | Default | Description |
|---|---|---|---|
| `variant` | `"primary" \| "outline" \| "ghost"` | `"primary"` | Visual weight. |
| `href` | `string` | — | When present, renders a real `<a>` (e.g. a "Get started" link); otherwise a real `<button type="button">`. |
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Visible label. |

Bar-height (36px) action sharing the Buttons family's primary/outline/ghost language. Native button or anchor attributes are forwarded."""

TOGGLE_PROPS = r"""### `<NavbarToggle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | `"Open/Close navigation menu"` (state-dependent) | Accessible name override. |
| `className` | `string` | — | Extra classes. |

A real `<button type="button">` with `aria-expanded` and `aria-controls` pointing at the mobile region; visible only below the root `breakpoint`. The hamburger/close icon swaps with state (aria-hidden)."""

MOBILE_PROPS = r"""### `<NavbarMobile>`

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

A `<ul role="list">`; marks its subtree as the mobile area so `NavbarLink` renders stacked full-width."""

DROPDOWN_PROPS = r"""### `<NavbarDropdown>`

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

A `role="separator"` horizontal rule between dropdown groups. No props beyond `className`."""


def props_table():
    return "\n\n".join([
        NAVBAR_PROPS,
        BRAND_PROPS,
        CONTENT_SECTION_ITEM_PROPS,
        LINK_PROPS,
        ACTION_PROPS,
        TOGGLE_PROPS,
        MOBILE_PROPS,
        DROPDOWN_PROPS,
    ])


# ---------------------------------------------------------------------------
# Shared README docs
# ---------------------------------------------------------------------------

KEYBOARD_BASE = """| Key | Context | Behavior |
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

The trigger, items, and toggle are native `<button>` / `<a>` elements, so Enter/Space activation and Tab order follow normal browser behavior. Disabled entries use non-interactive `aria-disabled` spans: they are skipped by arrow-key navigation and removed from the tab order. Focus is never trapped — the mobile navigation is a disclosure, not a modal dialog."""

NOTES_BASE = """- The desktop content collapses purely through Tailwind responsive utilities at the configured `breakpoint` (default `md`); there is no JavaScript width detection. If the viewport is resized past the breakpoint while the mobile menu is open, the region hides visually while the state remains open — close it via the toggle or Escape before resizing, or manage `open` yourself.
- The mobile navigation is a disclosure, not a dialog: focus is never trapped, even in the `side` placement. If you need a true modal navigation drawer, compose the DevSnips Dialog family instead.
- Dropdown panels anchor to their trigger with `absolute` positioning inside a `relative` wrapper — no positioning library. The viewport flip covers horizontal overflow; a navbar at the very bottom edge of a short viewport can still clip a tall panel vertically (the panel caps its height and scrolls internally instead)."""


# ---------------------------------------------------------------------------
# Shared showcase helpers (plain JSX, inlined per preview)
# ---------------------------------------------------------------------------

SHOWCASE_HELPERS = r"""
const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const BODY_WRAP = "mx-auto w-full max-w-3xl px-4 sm:px-6";

const NAV_ROUTES = [
  { href: "#/overview", label: "Overview" },
  { href: "#/components", label: "Components" },
  { href: "#/templates", label: "Templates" },
  { href: "#/pricing", label: "Pricing" },
];

function useHashRoute() {
  const [route, setRoute] = React.useState(() => window.location.hash || "#/overview");
  React.useEffect(() => {
    function onHashChange() { setRoute(window.location.hash || "#/overview"); }
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);
  return route;
}

function ForgeMark() {
  return (
    <span aria-hidden="true" className="flex size-6 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] text-[11px] font-bold leading-none text-[var(--ds-color-primary-foreground)]">F</span>
  );
}

function DemoArticle({ route, sections }) {
  return (
    <div className={BODY_WRAP + " py-10"}>
      <p className={LABEL}>Current route</p>
      <h2 className="m-0 mt-1 text-2xl font-semibold tracking-tight text-[var(--ds-color-foreground)]">
        {route.replace("#/", "").replace(/^\w/, (c) => c.toUpperCase())}
      </h2>
      <p className="m-0 mt-2 max-w-prose text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
        The navbar links are hash routes in this preview: activating a link updates the location hash, the active item follows via <code>aria-current="page"</code>, and the page below reflects the current route.
      </p>
      {(sections || ["Release notes", "Documentation", "Support channels", "Company"]).map((title, i) => (
        <section key={title} aria-label={title} className="mt-10 border-t border-[var(--ds-color-border-subtle)] pt-6">
          <h3 className="m-0 text-base font-semibold text-[var(--ds-color-foreground)]">{title}</h3>
          <p className="m-0 mt-2 max-w-prose text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
            {i % 2 === 0
              ? "Forge publishes small, reviewable changes. Each section of the library documents its tokens, states, and keyboard model alongside the implementation so teams can adopt pieces incrementally without a migration project."
              : "Every interactive pattern ships with real focus management, an honest accessibility tree, and responsive behavior verified at 375, 768, and 1280 pixels. The goal is boring reliability: components you can paste into a product and forget about."}
          </p>
        </section>
      ))}
    </div>
  );
}
"""

# Shared composition snippets used across showcases.
DESKTOP_LINKS = """{NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}"""

MOBILE_LINKS = """{NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
          <NavbarItem>
            <NavbarLink href="https://github.com" external>GitHub</NavbarLink>
          </NavbarItem>
          <NavbarItem>
            <NavbarLink href="#/enterprise" disabled>Enterprise</NavbarLink>
          </NavbarItem>"""

# 1. navbar (reference)
register(
    "navbar",
    title="Navbar",
    subcategory="Core",
    description="The canonical site navbar: a semantic nav landmark with a brand, a primary navigation list (active, external, and disabled items), an action area, and a mobile disclosure — the reference implementation every other variant in the family composes.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["navbar-with-actions", "navbar-with-dropdown", "navbar-with-mobile-menu", "navbar-sticky"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarAction, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>
    <NavbarSection align="start">
      <NavbarItem><NavbarLink href="/overview" active>Overview</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/components">Components</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/templates">Templates</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="https://github.com" external>GitHub</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/enterprise" disabled>Enterprise</NavbarLink></NavbarItem>
    </NavbarSection>
    <NavbarSection align="end">
      <NavbarItem><NavbarAction href="/get-started">Get started</NavbarAction></NavbarItem>
    </NavbarSection>
  </NavbarContent>
  <NavbarToggle />
  <NavbarMobile>
    <NavbarMobileContent>
      <NavbarItem><NavbarLink href="/overview" active>Overview</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/components">Components</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/templates">Templates</NavbarLink></NavbarItem>
    </NavbarMobileContent>
  </NavbarMobile>
</Navbar>''',
    props_doc=props_table(),
    composition_note="This is the reference composition — brand, one `start` navigation section, one `end` action, and the mobile region. Every other variant in the family uses the same primitives, class constants, states, and accessibility model.",
    behavior_doc="""The bar is a single 56px row: brand on the leading edge, navigation links in the `start` section, one primary action in the `end` section. All four link states of the system are demonstrated:

- **Active** — the current page's link carries `active` (`aria-current="page"` + the active surface).
- **Idle** — muted foreground; hover shifts to the hover surface with foreground text.
- **External** — `external` adds `target="_blank" rel="noreferrer"`, a visible indicator glyph, and sr-only text.
- **Disabled** — `disabled` renders a non-interactive `aria-disabled` span (an unavailable "Enterprise" tier), never a dead anchor.

Below the `md` breakpoint the desktop content collapses and the toggle discloses the same links stacked full-width. Activating any mobile link closes the menu.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The reference composition keeps one navigation landmark (`label=\"Main\"`), one current item, and a logical tab order (brand → links → action → toggle → mobile region).",
    responsive_doc="At 375px only the brand and toggle remain; the panel discloses the full navigation under the bar. At 768px the desktop row appears (the `md` breakpoint). At 1280px the bar content caps at `max-w-6xl` and centers.",
    controlled_doc="The reference uses the default uncontrolled mobile menu. See `navbar-with-mobile-menu` for a parent-owned (controlled) example.",
    notes_doc="Reference implementation for the Navbar family. It establishes the shared geometry (56px bar, 36px actions, radius-sm links), the surface/border model, the four link states, the focus-ring treatment, and the mobile disclosure behavior that every other variant extends.\n\n" + NOTES_BASE,
    tsx_header="",
    showcase=SHOWCASE_HELPERS + '''
function ReferenceNav() {
  const route = useHashRoute();
  return (
    <Navbar>
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
          <NavbarItem>
            <NavbarLink href="https://github.com" external>GitHub</NavbarLink>
          </NavbarItem>
          <NavbarItem>
            <NavbarLink href="#/enterprise" disabled>Enterprise</NavbarLink>
          </NavbarItem>
        </NavbarSection>
        <NavbarSection align="end">
          <NavbarItem>
            <NavbarAction variant="primary" href="#/get-started">Get started</NavbarAction>
          </NavbarItem>
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
          <NavbarItem>
            <NavbarLink href="https://github.com" external>GitHub</NavbarLink>
          </NavbarItem>
          <NavbarItem>
            <NavbarLink href="#/enterprise" disabled>Enterprise</NavbarLink>
          </NavbarItem>
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <ReferenceNav />
      <DemoArticle route={route} />
    </div>
  );
}''',
)

# 2. navbar-with-actions
register(
    "navbar-with-actions",
    title="Navbar with Actions",
    subcategory="Composite",
    description="Brand and primary navigation plus a trailing action area: a ghost Sign in button and a primary Get started link, with a realistic sign-in state change driven entirely by local component state.",
    tags=TAGS_BASE + ["actions", "sign-in", "cta"],
    features=FEAT_BASE + ["ghost/outline/primary actions", "sign-in state demo"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["navbar", "navbar-with-user-menu", "navbar-centered"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarAction, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>
    <NavbarSection align="start">
      <NavbarItem><NavbarLink href="/overview" active>Overview</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarSection>
    <NavbarSection align="end">
      <NavbarItem><NavbarAction variant="ghost" onClick={signIn}>Sign in</NavbarAction></NavbarItem>
      <NavbarItem><NavbarAction variant="primary" href="/get-started">Get started</NavbarAction></NavbarItem>
    </NavbarSection>
  </NavbarContent>
  <NavbarToggle />
  <NavbarMobile>…</NavbarMobile>
</Navbar>''',
    props_doc=props_table(),
    composition_note="Actions live in their own `NavbarSection align=\"end\"` — each wrapped in a `NavbarItem` so the region keeps list semantics. `NavbarAction` renders a `<button>` by default and an `<a>` when `href` is passed, so navigation-style actions (Get started) and command-style actions (Sign in) stay honest elements.",
    behavior_doc="""The action area demonstrates the three `NavbarAction` weights with realistic behavior:

- **Sign in** (ghost, `<button>`) — activates a local signed-in state; the action area swaps to an account label and a Sign out ghost button. The state is demo-only (no auth), driven by `useState` in the showcase.
- **Get started** (primary, `<a>`) — a navigation action pointing at the signup route.
- **Talk to sales** (outline, `<a>`) — a secondary navigation action, hidden below `sm` where the action area would crowd the bar.

Keeping command actions as buttons and navigation actions as anchors preserves honest semantics: middle-clicking "Get started" opens a new tab; "Sign in" does not pretend to be a link.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Actions sit in the same `<ul>` region as any other section content, so assistive technology announces them as list items of the navigation. The ghost Sign in button has a text label — no icon-only ambiguity.",
    responsive_doc="The outline action is hidden below `sm` (`hidden sm:inline-flex` via `className`) so the trailing area never crowds the bar at 375px; the ghost + primary pair fits comfortably. All actions keep the 36px touch target.",
    controlled_doc="The mobile menu is uncontrolled here; the signed-in demo state is ordinary showcase `useState`, unrelated to the navbar's own state model.",
    notes_doc="A realistic marketing/app-shell action area without product-specific coupling — the Sign in flow is local state only and is meant to be wired to a real auth handler.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — with actions.
 *
 * Brand + primary navigation + a trailing action area. Demonstrates the
 * three `NavbarAction` weights (ghost Sign in button, outline secondary
 * link, primary Get started link) with a realistic local sign-in state
 * change. Built entirely from the shared Navbar primitives; see the
 * `navbar` reference for the full system documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function ActionsNav() {
  const route = useHashRoute();
  const [signedIn, setSignedIn] = React.useState(false);
  return (
    <Navbar>
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
        </NavbarSection>
        <NavbarSection align="end">
          {signedIn ? (
            <>
              <NavbarItem>
                <span className="px-2 text-sm text-[var(--ds-color-muted-foreground)]">Signed in as ada@forge.dev</span>
              </NavbarItem>
              <NavbarItem>
                <NavbarAction variant="ghost" onClick={() => setSignedIn(false)}>Sign out</NavbarAction>
              </NavbarItem>
            </>
          ) : (
            <>
              <NavbarItem>
                <NavbarAction variant="ghost" onClick={() => setSignedIn(true)}>Sign in</NavbarAction>
              </NavbarItem>
              <NavbarItem className="hidden sm:flex">
                <NavbarAction variant="outline" href="#/contact-sales">Talk to sales</NavbarAction>
              </NavbarItem>
              <NavbarItem>
                <NavbarAction variant="primary" href="#/get-started">Get started</NavbarAction>
              </NavbarItem>
            </>
          )}
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
          <NavbarItem>
            {signedIn ? (
              <NavbarAction variant="ghost" onClick={() => setSignedIn(false)}>Sign out</NavbarAction>
            ) : (
              <NavbarAction variant="ghost" onClick={() => setSignedIn(true)}>Sign in</NavbarAction>
            )}
          </NavbarItem>
          <NavbarItem>
            <NavbarAction variant="primary" href="#/get-started" className="w-full">Get started</NavbarAction>
          </NavbarItem>
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <ActionsNav />
      <DemoArticle route={route} sections={["Why Forge", "Pricing model", "Security"]} />
    </div>
  );
}''',
)

# 3. navbar-centered
register(
    "navbar-centered",
    title="Centered Navbar",
    subcategory="Layout",
    description="The brand sits at the horizontal center of the bar on desktop with navigation distributed around it — a link group on each side — while small screens fall back to the standard brand-left, toggle-right row.",
    tags=TAGS_BASE + ["centered", "layout", "brand"],
    features=FEAT_BASE + ["centered brand", "balanced side sections"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["navbar", "navbar-with-actions"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

// The brand stays in normal flow on small screens and centers itself at
// the md breakpoint; the two sections flank it in the remaining space.
<Navbar>
  <NavbarBrand href="/" className="md:absolute md:left-1/2 md:-translate-x-1/2">Forge</NavbarBrand>
  <NavbarContent>
    <NavbarSection align="start" className="flex-1">
      <NavbarItem><NavbarLink href="/components">Components</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/templates">Templates</NavbarLink></NavbarItem>
    </NavbarSection>
    <NavbarSection align="end">
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/changelog">Changelog</NavbarLink></NavbarItem>
    </NavbarSection>
  </NavbarContent>
  <NavbarToggle />
  <NavbarMobile>…</NavbarMobile>
</Navbar>''',
    props_doc=props_table(),
    composition_note="The centered layout is pure composition: `NavbarBrand` carries `md:absolute md:left-1/2 md:-translate-x-1/2` (the bar is already `relative`), taking it out of flow at the `md` breakpoint so it sits at the exact center; the `start` section gets `flex-1` so the two link groups occupy the flanks. Below `md` the brand returns to normal flow on the left and the toggle sits on the right.",
    behavior_doc="""The desktop bar is symmetric: two links on the left, two on the right, the brand dead-center regardless of how wide either group is (absolute centering is independent of the flanking content).

The centered pattern trades link capacity for brand prominence — keep each flank to two or three short labels. Below the breakpoint the layout intentionally collapses to the standard mobile pattern instead of trying to keep the brand centered; a centered brand between a toggle and dead space is less usable than a predictable left/right row.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="DOM order stays logical (brand → left links → right links → toggle) even though the brand is visually centered — visual order and focus order match because the flanking sections contain no focusable content that would overlap the centered brand.",
    responsive_doc="At 375px: brand left, toggle right (standard mobile row). At 768px and 1280px: the brand centers absolutely and the sections distribute. Because the brand leaves the flow at `md`, verify at build time that the flanking link groups are short enough not to run under it — this composition keeps each side to two links.",
    controlled_doc="The mobile menu is uncontrolled.",
    notes_doc="The centering classes live on `NavbarBrand` via `className` — they are additive (the base brand sets no position), so there are no conflicting utilities. Keep the flanking sections short and symmetric in label length.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — centered.
 *
 * The brand sits at the horizontal center of the bar on desktop with
 * navigation sections flanking it, collapsing to the standard brand-left /
 * toggle-right row below the breakpoint. Built entirely from the shared
 * Navbar primitives; see the `navbar` reference for the full system
 * documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function CenteredNav() {
  const route = useHashRoute();
  return (
    <Navbar>
      <NavbarBrand href="#/overview" className="md:absolute md:left-1/2 md:-translate-x-1/2"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start" className="flex-1">
          <NavbarItem><NavbarLink href="#/components" active={route === "#/components"}>Components</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/templates" active={route === "#/templates"}>Templates</NavbarLink></NavbarItem>
        </NavbarSection>
        <NavbarSection align="end">
          <NavbarItem><NavbarLink href="#/pricing" active={route === "#/pricing"}>Pricing</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/changelog" active={route === "#/changelog"}>Changelog</NavbarLink></NavbarItem>
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          <NavbarItem><NavbarLink href="#/components" active={route === "#/components"}>Components</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/templates" active={route === "#/templates"}>Templates</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/pricing" active={route === "#/pricing"}>Pricing</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/changelog" active={route === "#/changelog"}>Changelog</NavbarLink></NavbarItem>
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <CenteredNav />
      <DemoArticle route={route} sections={["Editorial", "Gallery", "Stockists"]} />
    </div>
  );
}''',
)

# 4. navbar-with-dropdown
register(
    "navbar-with-dropdown",
    title="Navbar with Dropdown",
    subcategory="Navigation",
    description="Primary navigation containing dropdown menus: disclosure-style panels of real links with full keyboard support, Escape and outside-pointer close, focus restoration, disabled items, and viewport-aware alignment.",
    tags=TAGS_BASE + ["dropdown", "submenu", "disclosure"],
    features=FEAT_BASE + ["navigation dropdowns", "roving dropdown focus", "viewport-aware alignment", "disabled dropdown items"],
    accessibility=A11Y_BASE + ["aria-haspopup='true' trigger", "Escape closes + restores focus", "outside-pointer close"],
    interactive=True,
    related=["navbar", "navbar-with-mega-menu", "navbar-with-user-menu"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarDropdown, NavbarDropdownTrigger, NavbarDropdownContent,
  NavbarDropdownItem, NavbarDivider, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>
    <NavbarSection align="start">
      <NavbarItem><NavbarLink href="/overview" active>Overview</NavbarLink></NavbarItem>
      <NavbarItem>
        <NavbarDropdown>
          <NavbarDropdownTrigger>Components</NavbarDropdownTrigger>
          <NavbarDropdownContent>
            <NavbarDropdownItem href="/components/buttons">Buttons</NavbarDropdownItem>
            <NavbarDropdownItem href="/components/inputs">Inputs</NavbarDropdownItem>
            <NavbarDropdownItem href="/components/navbar" active>Navbar</NavbarDropdownItem>
            <NavbarDropdownItem disabled>Charts — coming soon</NavbarDropdownItem>
            <NavbarDivider />
            <NavbarDropdownItem href="/components" >All components</NavbarDropdownItem>
          </NavbarDropdownContent>
        </NavbarDropdown>
      </NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarSection>
  </NavbarContent>
  <NavbarToggle />
  <NavbarMobile>…</NavbarMobile>
</Navbar>''',
    props_doc=props_table(),
    composition_note="A `NavbarDropdown` sits inside a `NavbarItem` like any link. The panel holds real navigation links (`NavbarDropdownItem href=…`), one disabled entry, and a `NavbarDivider` before the catch-all link. The second dropdown (`Resources`, near the trailing edge) demonstrates the automatic start → end alignment flip.",
    behavior_doc="""Navigation dropdowns follow the disclosure pattern, not the ARIA menu pattern: the panel contains real anchors, so links keep their native behavior (middle-click, open-in-new-tab, link semantics) instead of being demoted to `role="menuitem"` buttons.

- **Open** — click, Enter/Space, ArrowDown (focus first item), or ArrowUp (focus last item) on the trigger.
- **Move** — ArrowUp/ArrowDown cycle enabled items with wrap-around; Home/End jump to the ends.
- **Close** — Escape (focus returns to the trigger), Tab (focus moves on naturally), selecting an item, or a pointer down outside the dropdown.
- **Disabled** — "Charts — coming soon" is a non-interactive `aria-disabled` span: skipped by arrow keys, out of the tab order.
- **Placement** — the panel measures itself before paint and flips start ↔ end when it would overflow the viewport; width is capped at `100vw - 1.5rem` and height scrolls internally.

Each dropdown owns its open state; opening one and then interacting elsewhere closes it via the outside-pointer path. On mobile the same destinations are listed flat — dropdown chrome adds nothing in a stacked list.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The trigger is a real `<button>` with `aria-haspopup=\"true\"`, `aria-expanded`, and `aria-controls`; the panel is labelled by its trigger. Links stay real anchors — the deliberate reason this variant does not use `role=\"menu\"`/`menuitem`.",
    responsive_doc="Dropdowns live in the desktop content row (`hidden md:flex`); below the breakpoint the mobile region lists the same destinations flat. The panel's alignment flip and width cap keep it on-screen at 768px and 1280px, including for triggers near the trailing edge.",
    controlled_doc="Dropdowns manage their own open state (seed with `defaultOpen` if ever needed). The mobile menu here is uncontrolled.",
    notes_doc="Focus moves into the panel on every open — including pointer opens — so keyboard and mouse users get identical focus geometry. If you prefer pointer opens to leave focus on the trigger, track the opening gesture in `onOpenChange`-style wrapper state.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — with dropdown navigation.
 *
 * Primary navigation containing disclosure dropdowns: real `<a>` links in a
 * labelled panel with roving DOM focus, Escape / outside-pointer close,
 * focus restoration, disabled items, and viewport-aware alignment. Built
 * entirely from the shared Navbar primitives; see the `navbar` reference
 * for the full system documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function DropdownNav() {
  const route = useHashRoute();
  return (
    <Navbar>
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          <NavbarItem><NavbarLink href="#/overview" active={route === "#/overview"}>Overview</NavbarLink></NavbarItem>
          <NavbarItem>
            <NavbarDropdown>
              <NavbarDropdownTrigger>Components</NavbarDropdownTrigger>
              <NavbarDropdownContent>
                <NavbarDropdownItem href="#/components/buttons">Buttons</NavbarDropdownItem>
                <NavbarDropdownItem href="#/components/inputs">Inputs</NavbarDropdownItem>
                <NavbarDropdownItem href="#/components/dialogs">Dialogs</NavbarDropdownItem>
                <NavbarDropdownItem href="#/components/navbar" active={route === "#/components/navbar"}>Navbar</NavbarDropdownItem>
                <NavbarDropdownItem disabled>Charts — coming soon</NavbarDropdownItem>
                <NavbarDivider />
                <NavbarDropdownItem href="#/components">All components</NavbarDropdownItem>
              </NavbarDropdownContent>
            </NavbarDropdown>
          </NavbarItem>
          <NavbarItem><NavbarLink href="#/templates" active={route === "#/templates"}>Templates</NavbarLink></NavbarItem>
        </NavbarSection>
        <NavbarSection align="end">
          <NavbarItem>
            <NavbarDropdown placement="bottom-end">
              <NavbarDropdownTrigger>Resources</NavbarDropdownTrigger>
              <NavbarDropdownContent>
                <NavbarDropdownItem href="#/docs">Documentation</NavbarDropdownItem>
                <NavbarDropdownItem href="#/guides">Guides</NavbarDropdownItem>
                <NavbarDropdownItem href="#/api">API reference</NavbarDropdownItem>
                <NavbarDivider />
                <NavbarDropdownItem href="https://github.com" external>GitHub</NavbarDropdownItem>
              </NavbarDropdownContent>
            </NavbarDropdown>
          </NavbarItem>
          <NavbarItem><NavbarLink href="#/pricing" active={route === "#/pricing"}>Pricing</NavbarLink></NavbarItem>
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          <NavbarItem><NavbarLink href="#/overview" active={route === "#/overview"}>Overview</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/components" active={route === "#/components"}>Components</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/templates" active={route === "#/templates"}>Templates</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/docs">Documentation</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/api">API reference</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/pricing" active={route === "#/pricing"}>Pricing</NavbarLink></NavbarItem>
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <DropdownNav />
      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
        <p className={NOTE}>Try the Components and Resources dropdowns: ArrowDown opens with the first item focused, arrows cycle, Escape closes and refocuses the trigger, Tab closes, and clicking outside closes. The Resources panel flips its alignment to stay inside the viewport.</p>
      </div>
      <DemoArticle route={route} sections={["Component index", "Recently updated"]} />
    </div>
  );
}''',
)

# 5. navbar-with-mobile-menu
register(
    "navbar-with-mobile-menu",
    title="Navbar with Mobile Menu",
    subcategory="Mobile",
    description="The responsive collapse pattern in depth: below the breakpoint the desktop navigation becomes a toggle-disclosed mobile region with aria-expanded / aria-controls wiring, Escape and outside-pointer close, and predictable focus — shown in both uncontrolled and controlled state modes.",
    tags=TAGS_BASE + ["mobile", "hamburger", "disclosure", "controlled"],
    features=FEAT_BASE + ["controlled + uncontrolled mobile state", "Escape close", "outside-pointer close", "focus restoration"],
    accessibility=A11Y_BASE + ["toggle aria-expanded/aria-controls wiring", "focus restored to toggle on close"],
    interactive=True,
    related=["navbar", "navbar-with-sidebar-mobile"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

// Uncontrolled — the navbar owns the state:
<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>…</NavbarContent>
  <NavbarToggle />
  <NavbarMobile>
    <NavbarMobileContent>
      <NavbarItem><NavbarLink href="/overview" active>Overview</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarMobileContent>
  </NavbarMobile>
</Navbar>

// Controlled — the parent owns the state:
const [open, setOpen] = useState(false);
<Navbar open={open} onOpenChange={setOpen} label="Main">…</Navbar>''',
    props_doc=props_table(),
    composition_note="The mobile region is a first-class part of the composition: `NavbarToggle` + `NavbarMobile` + `NavbarMobileContent`. The toggle references the actual region through `aria-controls`, and links inside `NavbarMobileContent` automatically render stacked and full-width.",
    behavior_doc="""Two navbars demonstrate the state model end to end (resize the preview below 768px to use them):

- **Uncontrolled** (`label="Main"`) — the navbar owns the mobile state; nothing to wire up.
- **Controlled** (`label="Controlled demo"`) — the showcase owns `open` + `onOpenChange`; the state readout next to the bar proves every internal request (toggle, Escape, outside pointer, link activation) flows through the parent's handler.

In both modes the behavior is identical: the toggle's `aria-expanded` tracks state and its `aria-controls` points at the region; Escape closes from anywhere; a pointer down outside the navbar closes; activating a link closes (and navigates); and when the region unmounts, focus is restored to the toggle instead of being stranded on `<body>`.

The panel is absolutely positioned under the bar, so opening/closing it never shifts page layout, and its height caps at `100dvh - 4rem` with internal scrolling.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The two demo navbars carry distinct landmark labels (`Main` / `Controlled demo`) — required whenever more than one `<nav>` is on the page. The toggle's accessible name reflects state (\"Open/Close navigation menu\") and its icon is aria-hidden.",
    responsive_doc="This variant exists to be resized: at 1280px the desktop row is fully visible and the toggle is hidden; at 768px the `md` breakpoint flips (desktop content hides, toggle appears); at 375px the panel is the only navigation. Both state modes behave identically at every width.",
    controlled_doc="The controlled demo is the canonical example: `const [open, setOpen] = useState(false); <Navbar open={open} onOpenChange={setOpen}>`. Every close path — toggle, Escape, outside pointer, link activation — reports through `onOpenChange`.",
    notes_doc="Both demos render on one page, so each `Navbar` gets a distinct `label`. The controlled demo's readout text is showcase state, not part of the component.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — with mobile menu.
 *
 * The responsive collapse pattern in depth: below the breakpoint the
 * desktop navigation becomes a toggle-disclosed mobile region with
 * aria-expanded / aria-controls wiring, Escape and outside-pointer close,
 * and predictable focus restoration — in both uncontrolled and controlled
 * state modes. Built entirely from the shared Navbar primitives; see the
 * `navbar` reference for the full system documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function UncontrolledNav() {
  const route = useHashRoute();
  return (
    <Navbar label="Main">
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function ControlledNav() {
  const route = useHashRoute();
  const [open, setOpen] = React.useState(false);
  return (
    <div>
      <Navbar label="Controlled demo" open={open} onOpenChange={setOpen}>
        <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
        <NavbarContent>
          <NavbarSection align="start">
            {NAV_ROUTES.map((r) => (
              <NavbarItem key={r.href}>
                <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
              </NavbarItem>
            ))}
          </NavbarSection>
        </NavbarContent>
        <NavbarToggle />
        <NavbarMobile>
          <NavbarMobileContent>
            {NAV_ROUTES.map((r) => (
              <NavbarItem key={r.href}>
                <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
              </NavbarItem>
            ))}
          </NavbarMobileContent>
        </NavbarMobile>
      </Navbar>
      <p className={NOTE + " px-4 py-2 sm:px-6"}>Parent state: the mobile menu is <b>{open ? "open" : "closed"}</b>. The parent owns it via <code>open</code> + <code>onOpenChange</code>.</p>
    </div>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <UncontrolledNav />
      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
        <p className={NOTE}>Resize below 768px: the desktop row collapses and the toggle discloses the navigation. Escape closes from anywhere, clicking outside closes, activating a link closes, and focus returns to the toggle.</p>
      </div>
      <ControlledNav />
      <DemoArticle route={route} sections={["Responsive guidance"]} />
    </div>
  );
}''',
)

# 6. navbar-with-mega-menu
register(
    "navbar-with-mega-menu",
    title="Navbar with Mega Menu",
    subcategory="Navigation",
    description="A wider dropdown pattern containing grouped navigation links: labelled groups in a multi-column panel with the same keyboard model, Escape/outside-pointer close, and viewport-aware alignment as the simple dropdown.",
    tags=TAGS_BASE + ["mega-menu", "dropdown", "grouped"],
    features=FEAT_BASE + ["grouped mega menu", "group labels", "multi-column panel", "keyboard navigation"],
    accessibility=A11Y_BASE + ["labelled groups", "aria-haspopup='true' trigger"],
    interactive=True,
    related=["navbar-with-dropdown", "navbar"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarDropdown, NavbarDropdownTrigger, NavbarDropdownContent,
  NavbarDropdownItem, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

<NavbarDropdown>
  <NavbarDropdownTrigger>Platform</NavbarDropdownTrigger>
  <NavbarDropdownContent className="w-[min(36rem,calc(100vw-2rem))]">
    <div className="grid gap-4 p-3 sm:grid-cols-3">
      <div role="group" aria-labelledby="mm-product">
        <p id="mm-product">Product</p>
        <NavbarDropdownItem href="/analytics">Analytics</NavbarDropdownItem>
        <NavbarDropdownItem href="/automation">Automation</NavbarDropdownItem>
      </div>
      <div role="group" aria-labelledby="mm-resources">…</div>
      <div role="group" aria-labelledby="mm-company">…</div>
    </div>
  </NavbarDropdownContent>
</NavbarDropdown>''',
    props_doc=props_table(),
    composition_note="A mega menu is a `NavbarDropdownContent` with a wider `className` (`w-[min(36rem,calc(100vw-2rem))]` — additive, never conflicting with the base `min-w`) and grouped children: each column is a `role=\"group\"` labelled by a real text heading via `aria-labelledby`. Items are the same `NavbarDropdownItem` anchors as the simple dropdown.",
    behavior_doc="""The mega menu reuses the entire dropdown interaction model — nothing is re-implemented for the wider panel:

- Trigger: click, Enter/Space, ArrowDown (focus first item), ArrowUp (focus last item).
- Panel: ArrowUp/ArrowDown move through ALL enabled items in DOM order (column by column), Home/End jump to the ends, Escape closes and refocuses the trigger, Tab closes naturally, outside pointer closes.
- Groups carry meaningful labels ("Product", "Resources", "Company") rendered as real headings and wired with `role="group"` + `aria-labelledby`, so screen-reader users hear the group context when entering it.
- The panel flips start ↔ end to stay in the viewport, caps its width at `100vw - 2rem`, and caps its height with internal scrolling; at narrow widths the grid falls back to a single column.

Keep mega menus to navigation: links with short labels and optional leading icons that communicate meaning. Avoid marketing cards, images, or forms inside the panel.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Group headings are real text (not aria-only), wired to their group with `aria-labelledby`. Icons are aria-hidden decoration; every item's accessible name comes from its visible label.",
    responsive_doc="The mega menu lives in the desktop row; below the breakpoint the mobile region lists the same destinations flat. The grid collapses to one column under `sm`, and the panel width cap keeps the menu inside the viewport at 768px and 1280px.",
    controlled_doc="The dropdown manages its own open state; the mobile menu is uncontrolled.",
    notes_doc="The panel's inner `p-3` grid wrapper composes with the base `p-1` panel padding (different elements, no conflicting utilities). Arrow-key order follows DOM order, so author columns in reading order.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — with mega menu.
 *
 * A wider dropdown pattern containing grouped navigation links: labelled
 * groups in a multi-column panel reusing the shared dropdown interaction
 * model (roving DOM focus, Escape / outside-pointer close, focus
 * restoration, viewport-aware alignment). Built entirely from the shared
 * Navbar primitives; see the `navbar` reference for the full system
 * documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
const MM_HEAD = "m-0 px-2 pb-1 pt-1 text-[11px] font-medium uppercase tracking-[0.05em] text-[var(--ds-color-muted-foreground)]";
function MegaNav() {
  const route = useHashRoute();
  return (
    <Navbar>
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          <NavbarItem>
            <NavbarDropdown>
              <NavbarDropdownTrigger>Platform</NavbarDropdownTrigger>
              <NavbarDropdownContent className="w-[min(36rem,calc(100vw-2rem))]">
                <div className="grid gap-4 p-3 sm:grid-cols-3">
                  <div role="group" aria-labelledby="mm-product">
                    <p id="mm-product" className={MM_HEAD}>Product</p>
                    <NavbarDropdownItem href="#/analytics" icon={<Icon name="grid" />}>Analytics</NavbarDropdownItem>
                    <NavbarDropdownItem href="#/automation" icon={<Icon name="refresh" />}>Automation</NavbarDropdownItem>
                    <NavbarDropdownItem href="#/repositories" icon={<Icon name="archive" />}>Repositories</NavbarDropdownItem>
                  </div>
                  <div role="group" aria-labelledby="mm-resources">
                    <p id="mm-resources" className={MM_HEAD}>Resources</p>
                    <NavbarDropdownItem href="#/docs" icon={<Icon name="book" />}>Documentation</NavbarDropdownItem>
                    <NavbarDropdownItem href="#/guides" icon={<Icon name="file" />}>Guides</NavbarDropdownItem>
                    <NavbarDropdownItem href="#/api" icon={<Icon name="command" />}>API reference</NavbarDropdownItem>
                  </div>
                  <div role="group" aria-labelledby="mm-company">
                    <p id="mm-company" className={MM_HEAD}>Company</p>
                    <NavbarDropdownItem href="#/about" icon={<Icon name="users" />}>About</NavbarDropdownItem>
                    <NavbarDropdownItem href="#/blog" icon={<Icon name="edit" />}>Blog</NavbarDropdownItem>
                    <NavbarDropdownItem disabled icon={<Icon name="bell" />}>Press kit</NavbarDropdownItem>
                  </div>
                </div>
              </NavbarDropdownContent>
            </NavbarDropdown>
          </NavbarItem>
          <NavbarItem><NavbarLink href="#/pricing" active={route === "#/pricing"}>Pricing</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/changelog" active={route === "#/changelog"}>Changelog</NavbarLink></NavbarItem>
        </NavbarSection>
        <NavbarSection align="end">
          <NavbarItem><NavbarLink href="#/sign-in">Sign in</NavbarLink></NavbarItem>
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          <NavbarItem><NavbarLink href="#/analytics">Analytics</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/automation">Automation</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/repositories">Repositories</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/docs">Documentation</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/guides">Guides</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/api">API reference</NavbarLink></NavbarItem>
          <NavbarItem><NavbarLink href="#/pricing" active={route === "#/pricing"}>Pricing</NavbarLink></NavbarItem>
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <MegaNav />
      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
        <p className={NOTE}>Open Platform: ArrowDown moves through every item column by column, group headings announce context, Escape closes and refocuses the trigger. The disabled Press kit entry is skipped by arrow keys.</p>
      </div>
      <DemoArticle route={route} sections={["Platform overview", "Customer stories"]} />
    </div>
  );
}''',
)

# 7. navbar-sticky
register(
    "navbar-sticky",
    title="Sticky Navbar",
    subcategory="Positioning",
    description="The sticky navigation pattern: the bar pins to the viewport top while page content scrolls beneath it, implemented with pure CSS position — no scroll listeners, no JavaScript.",
    tags=TAGS_BASE + ["sticky", "position", "scroll"],
    features=FEAT_BASE + ["sticky positioning", "no scroll JS", "elevated while pinned"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["navbar", "navbar-transparent"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

// Sticky is a composition concern, not a component variant: add the
// positioning utilities to the root.
<Navbar className="sticky top-0 z-40">
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>…</NavbarContent>
  <NavbarToggle />
  <NavbarMobile>…</NavbarMobile>
</Navbar>

// In a real app, add a scroll-aware shadow via a tiny scroll listener or
// an IntersectionObserver sentinel — the base component deliberately
// ships no scroll JavaScript.''',
    props_doc=props_table(),
    composition_note="Sticky behavior is one `className` on `<Navbar>`: `sticky top-0 z-40`. The base component sets no position, so the utilities are additive and conflict-free. The mobile panel and dropdowns anchor to the `<nav>`, so they stick with it.",
    behavior_doc="""The bar pins to the top of the viewport while the (deliberately long) page below scrolls — scroll this preview to see it. The behavior is pure CSS `position: sticky`; there are no scroll listeners, no `window.scrollY` reads, and no layout-shifting state changes.

While pinned, the bar keeps its surface and bottom border, which is enough separation for content scrolling beneath (per the design tokens: sticky navigation uses `shadow-sm` or a border — this composition uses the border). The `z-40` keeps the bar above page content, and the mobile panel + dropdown panels inherit the stacking context.

Anchor scrolling with `href="#section"` naturally stops below the bar only if you add `scroll-margin-top` to your targets — the component cannot know your bar height, so that remains a page-level concern.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Sticky positioning does not change the accessibility tree: the landmark, tab order, and mobile disclosure behave exactly as the reference. Focus rings are never clipped because the panel and dropdowns render inside the sticky stacking context.",
    responsive_doc="Sticky works identically at 375/768/1280: the bar pins, the mobile panel opens beneath it without shifting layout (it is absolutely positioned), and the `max-w-6xl` content row keeps its padding.",
    controlled_doc="The mobile menu is uncontrolled.",
    notes_doc="No scroll JavaScript is included by design. If you need a shadow or background change only after scroll, add a 5-line IntersectionObserver sentinel in your app — do not bake scroll state into the component.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — sticky.
 *
 * The bar pins to the viewport top with pure CSS `position: sticky` — no
 * scroll listeners, no layout-shifting JavaScript. Sticky is a composition
 * concern (`className="sticky top-0 z-40"` on the root), not a component
 * variant. Built entirely from the shared Navbar primitives; see the
 * `navbar` reference for the full system documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function StickyNav() {
  const route = useHashRoute();
  return (
    <Navbar className="sticky top-0 z-40">
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
        </NavbarSection>
        <NavbarSection align="end">
          <NavbarItem><NavbarLink href="#/sign-in">Sign in</NavbarLink></NavbarItem>
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <StickyNav />
      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
        <p className={NOTE}>Scroll this page: the bar stays pinned with pure CSS position: sticky — no scroll listeners. The mobile panel opens beneath it without shifting the layout.</p>
      </div>
      <DemoArticle route={route} sections={["Section one", "Section two", "Section three", "Section four", "Section five", "Section six", "Section seven", "Section eight"]} />
    </div>
  );
}''',
)

# 8. navbar-transparent
register(
    "navbar-transparent",
    title="Transparent Navbar",
    subcategory="Appearance",
    description="A navbar intended to sit over a page header or hero: the surface and bottom border are removed through the variant prop and the semantic token system, with no gradients, no glassmorphism, and no backdrop blur.",
    tags=TAGS_BASE + ["transparent", "hero", "overlay"],
    features=FEAT_BASE + ["transparent surface", "overlaid on page header", "no gradients/glassmorphism"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["navbar", "navbar-sticky"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

// `variant="transparent"` removes the surface + border; position it over
// the page header with absolute utilities and pad the header accordingly.
<div className="relative">
  <Navbar variant="transparent" className="absolute inset-x-0 top-0 z-40">
    <NavbarBrand href="/">Forge</NavbarBrand>
    <NavbarContent>…</NavbarContent>
    <NavbarToggle />
    <NavbarMobile>…</NavbarMobile>
  </Navbar>
  <header className="border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-6 pb-16 pt-28">
    …hero content…
  </header>
</div>

// In a real app, switch to variant="default" (or add the surface classes)
// once the header scrolls away — the two variants share every token, so the
// swap is a single prop.''',
    props_doc=props_table(),
    composition_note="`Navbar variant=\"transparent\"` swaps the root's surface classes for `bg-transparent border-transparent` — a first-class prop, not a className override, so there are no conflicting utilities. Positioning (`absolute inset-x-0 top-0 z-40`) is composition on the same root.",
    behavior_doc="""The transparent variant demonstrates how the token system handles an alternate surface: nothing about the links, actions, focus rings, or dropdown panels changes — they already reference semantic tokens (`surface-hover`, `surface-active`, `foreground`, `border`), which read correctly on any quiet background. The header below uses a flat `surface-subtle` fill with a hairline border — deliberately no gradients, no glassmorphism, no backdrop blur.

Because the navbar is absolutely positioned over the header, the header supplies its own top padding (`pt-28`) so content never runs under the bar. When the mobile menu opens, its panel keeps the SOLID surface (a transparent floating panel over content would be unreadable) — only the bar itself is transparent.

In a real product, pair this with a scroll position or route change that swaps `variant=\"transparent\"` → `variant=\"default\"`; the swap is one prop and both variants share geometry, so there is no layout shift.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Removing the surface changes visuals only: the landmark, contrast (foreground tokens on the quiet header surface), focus rings, and mobile disclosure are unchanged. The mobile panel keeps a solid surface token so menu content never sits directly on imagery.",
    responsive_doc="Identical collapse behavior to the reference at 375/768/1280; the absolute positioning spans the full width at every breakpoint and the header's fluid padding keeps the hero clear of the bar.",
    controlled_doc="The mobile menu is uncontrolled.",
    notes_doc="The transparent treatment is only as good as what sits under it: use it over quiet, low-contrast headers (flat surfaces, hairlines, type). Over photography or busy artwork, keep the default surface — no overlay treatment makes that accessible.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — transparent.
 *
 * Intended for use over a page header or hero: `variant="transparent"`
 * removes the surface and bottom border while every link, action, focus
 * ring, and panel keeps reading the same semantic tokens — no gradients,
 * no glassmorphism, no backdrop blur. Built entirely from the shared
 * Navbar primitives; see the `navbar` reference for the full system
 * documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function TransparentNav() {
  const route = useHashRoute();
  return (
    <div className="relative">
      <Navbar variant="transparent" className="absolute inset-x-0 top-0 z-40">
        <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
        <NavbarContent>
          <NavbarSection align="start">
            {NAV_ROUTES.map((r) => (
              <NavbarItem key={r.href}>
                <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
              </NavbarItem>
            ))}
          </NavbarSection>
          <NavbarSection align="end">
            <NavbarItem>
              <NavbarAction variant="primary" href="#/get-started">Get started</NavbarAction>
            </NavbarItem>
          </NavbarSection>
        </NavbarContent>
        <NavbarToggle />
        <NavbarMobile>
          <NavbarMobileContent>
            {NAV_ROUTES.map((r) => (
              <NavbarItem key={r.href}>
                <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
              </NavbarItem>
            ))}
          </NavbarMobileContent>
        </NavbarMobile>
      </Navbar>
      <header className="border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)]">
        <div className="mx-auto w-full max-w-3xl px-4 pb-16 pt-28 sm:px-6">
          <p className={LABEL}>Forge 4.2</p>
          <h2 className="m-0 mt-2 text-3xl font-semibold tracking-tight text-[var(--ds-color-foreground)] sm:text-4xl">
            A component library that reads like documentation
          </h2>
          <p className="m-0 mt-3 max-w-prose text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
            Tokens first, states honest, keyboard complete. The navbar above uses the transparent variant — the same semantic tokens, no surface — over this flat header.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <a href="#/get-started" className="inline-flex h-9 items-center rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-3 text-sm font-medium text-[var(--ds-color-primary-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:opacity-90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none">Get started</a>
            <a href="#/docs" className="inline-flex h-9 items-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none">Read the docs</a>
          </div>
        </div>
      </header>
    </div>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <TransparentNav />
      <DemoArticle route={route} sections={["Release highlights", "Upgrade guide"]} />
    </div>
  );
}''',
)

# 9. navbar-with-sidebar-mobile
register(
    "navbar-with-sidebar-mobile",
    title="Navbar with Sidebar Mobile Panel",
    subcategory="Mobile",
    description="The desktop navbar collapses into a compact side panel on small screens: overlay dismissal, body scroll lock with scrollbar compensation, Escape close, focus-on-open, and focus restoration — without ever trapping focus.",
    tags=TAGS_BASE + ["mobile", "sidebar", "drawer", "overlay"],
    features=FEAT_BASE + ["side panel placement", "overlay close", "body scroll lock", "focus-on-open"],
    accessibility=A11Y_BASE + ["overlay dismissal", "scroll lock with compensation", "no focus trap"],
    interactive=True,
    related=["navbar-with-mobile-menu", "navbar"],
    usage='''import {
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
</Navbar>''',
    props_doc=props_table(),
    composition_note="Same composition as the standard mobile menu with `placement=\"side\"` on `NavbarMobile`. The side panel conventionally adds a header row (brand + a second `NavbarToggle` acting as the close button) — both toggles share the same state, so either one closes the panel.",
    behavior_doc="""The side panel behaves like a compact navigation drawer while staying a disclosure, not a dialog:

- **Open** — the bar toggle discloses a fixed 18rem panel on the leading edge with an overlay over the page. Focus moves into the panel (its first focusable element) so keyboard users land inside it.
- **Close** — Escape (from anywhere), the overlay (pointer down), the panel's own close toggle, the bar toggle, or activating a link. Focus returns to the bar toggle.
- **Body interaction** — page scroll is locked while the panel is open, with scrollbar-width `padding-right` compensation so the page does not shift horizontally.
- **No focus trap** — Tab always moves forward naturally. A navigation panel is not a modal dialog; if you need modality, use the Dialog family.

The panel is 18rem wide and capped at `100vw - 4rem`, so a strip of the page (and the overlay) always remains visible as a dismissal affordance.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The overlay is a non-focusable, aria-hidden dismissal surface (pointer-only), mirroring the Dialog family's overlay; the panel keeps the region id the toggle's `aria-controls` references. Focus-on-open lands inside the panel and restoration returns it to the bar toggle, so focus is never stranded.",
    responsive_doc="The side panel is the mobile navigation — it only exists below the `md` breakpoint (both panel and overlay carry `md:hidden`). At 375px the panel takes 18rem of the 23.4rem viewport, leaving a visible overlay strip; at 768px the desktop row returns.",
    controlled_doc="The mobile menu is uncontrolled; pass `open` + `onOpenChange` to the root to own it (see `navbar-with-mobile-menu`).",
    notes_doc="The two toggles share one state and one ref-claim: the bar toggle permanently owns the focus-restore target, so closing from the panel's own toggle still returns focus correctly. Scroll lock + compensation are released on close or unmount.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — with sidebar mobile panel.
 *
 * The desktop navbar collapses into a compact side panel on small screens:
 * overlay dismissal, body scroll lock with scrollbar compensation, Escape
 * close, focus-on-open, and focus restoration — a navigation disclosure,
 * never a focus trap. Built entirely from the shared Navbar primitives;
 * see the `navbar` reference for the full system documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function SidebarNav() {
  const route = useHashRoute();
  return (
    <Navbar>
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
        </NavbarSection>
        <NavbarSection align="end">
          <NavbarItem><NavbarLink href="#/sign-in">Sign in</NavbarLink></NavbarItem>
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile placement="side">
        <div className="flex h-14 shrink-0 items-center justify-between border-b border-[var(--ds-color-border)] px-4">
          <span className="flex items-center gap-2 text-sm font-semibold text-[var(--ds-color-foreground)]"><ForgeMark />Forge</span>
          <NavbarToggle />
        </div>
        <NavbarMobileContent className="min-h-0 flex-1 overflow-y-auto">
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
          <NavbarItem>
            <NavbarLink href="https://github.com" external>GitHub</NavbarLink>
          </NavbarItem>
        </NavbarMobileContent>
        <div className="shrink-0 border-t border-[var(--ds-color-border)] p-4">
          <NavbarAction variant="primary" href="#/get-started" className="w-full">Get started</NavbarAction>
        </div>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <SidebarNav />
      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
        <p className={NOTE}>Resize below 768px and open the menu: a side panel slides in with an overlay. Escape, the overlay, the panel close button, or a link all close it; focus moves into the panel on open and returns to the bar toggle on close; page scroll locks without a layout shift.</p>
      </div>
      <DemoArticle route={route} sections={["Mobile patterns", "Drawer vs dialog", "Gesture support"]} />
    </div>
  );
}''',
)

# 10. navbar-with-user-menu
register(
    "navbar-with-user-menu",
    title="Navbar with User Menu",
    subcategory="Composite",
    description="A navbar containing a user/account menu built from the same dropdown architecture as every other variant: profile and settings links, a separator, a destructive-adjacent sign-out action, full keyboard support, Escape, outside-pointer close, and focus restoration.",
    tags=TAGS_BASE + ["user", "account", "menu", "avatar"],
    features=FEAT_BASE + ["account dropdown", "avatar trigger", "sign-out action", "separator groups"],
    accessibility=A11Y_BASE + ["accessible trigger name", "focus restoration on close"],
    interactive=True,
    related=["navbar-with-actions", "navbar-with-dropdown"],
    usage='''import {
  Navbar, NavbarBrand, NavbarContent, NavbarSection, NavbarItem,
  NavbarLink, NavbarDropdown, NavbarDropdownTrigger, NavbarDropdownContent,
  NavbarDropdownItem, NavbarDivider, NavbarToggle, NavbarMobile, NavbarMobileContent,
} from "./navbar";

<NavbarSection align="end">
  <NavbarItem>
    <NavbarDropdown placement="bottom-end">
      <NavbarDropdownTrigger aria-label="Account menu">
        <Avatar />Ada Rivers
      </NavbarDropdownTrigger>
      <NavbarDropdownContent>
        <NavbarDropdownItem href="/profile">Profile</NavbarDropdownItem>
        <NavbarDropdownItem href="/settings">Settings</NavbarDropdownItem>
        <NavbarDropdownItem href="/usage" disabled>Usage (unavailable)</NavbarDropdownItem>
        <NavbarDivider />
        <NavbarDropdownItem onSelect={signOut}>Sign out</NavbarDropdownItem>
      </NavbarDropdownContent>
    </NavbarDropdown>
  </NavbarItem>
</NavbarSection>''',
    props_doc=props_table(),
    composition_note="The account menu is a `NavbarDropdown` in the `end` section — the exact same architecture as the navigation dropdowns, not a second menu implementation. The trigger's children are free-form (an initials avatar + the user's name); `aria-label=\"Account menu\"` gives it a stable accessible name. Items with `href` are links; the sign-out item omits `href` and renders a `<button>` with `onSelect`.",
    behavior_doc="""The account menu reuses the dropdown behavior wholesale:

- Trigger: click, Enter/Space, ArrowDown/ArrowUp — the chevron rotates while open.
- Panel: profile/settings links (real anchors), a disabled usage entry, a `NavbarDivider`, and a sign-out action (`<button>` + `onSelect`). Arrow keys cycle, Home/End jump, Escape closes and refocuses the trigger, Tab closes naturally, outside pointer closes.
- Selecting sign out runs `onSelect` and closes; the demo flips to a signed-out state with a Sign in ghost action to reverse it.

`placement="bottom-end"` aligns the panel with the trailing trigger; the viewport flip still applies if the panel would overflow.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The trigger has a stable accessible name via `aria-label` (its visible children include an aria-hidden avatar, so the name never depends on initials). The sign-out action is a real `<button>` — actions that change session state are not links.",
    responsive_doc="The user name is hidden below `sm` (`hidden sm:inline`), leaving the 36px avatar trigger — a comfortable touch target. The `bottom-end` panel stays attached to the trailing trigger at every width, flipping if needed. On mobile the account links are listed flat in the mobile region.",
    controlled_doc="The dropdown manages its own open state; the mobile menu is uncontrolled. The signed-in state in the preview is ordinary showcase state.",
    notes_doc="Keep account menus short: profile, settings, optionally billing, a separator, sign out. Destructive-adjacent actions like sign out use the default item tone — reserve `destructive` styling for irreversible actions.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Navbar — with user menu.
 *
 * A navbar containing a user/account menu built from the shared dropdown
 * architecture: profile and settings links (real anchors), a separator, a
 * sign-out action (real button), full keyboard support, Escape /
 * outside-pointer close, and focus restoration. Built entirely from the
 * shared Navbar primitives; see the `navbar` reference for the full system
 * documentation.
 */""",
    showcase=SHOWCASE_HELPERS + '''
function Avatar() {
  return (
    <span aria-hidden="true" className="flex size-6 shrink-0 items-center justify-center rounded-full bg-[var(--ds-color-primary)] text-[10px] font-semibold leading-none text-[var(--ds-color-primary-foreground)]">AR</span>
  );
}
function UserMenuNav() {
  const route = useHashRoute();
  const [signedIn, setSignedIn] = React.useState(true);
  return (
    <Navbar>
      <NavbarBrand href="#/overview"><ForgeMark />Forge</NavbarBrand>
      <NavbarContent>
        <NavbarSection align="start">
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
        </NavbarSection>
        <NavbarSection align="end">
          {signedIn ? (
            <NavbarItem>
              <NavbarDropdown placement="bottom-end">
                <NavbarDropdownTrigger aria-label="Account menu for Ada Rivers">
                  <Avatar />
                  <span className="hidden sm:inline">Ada Rivers</span>
                </NavbarDropdownTrigger>
                <NavbarDropdownContent>
                  <NavbarDropdownItem href="#/profile" icon={<Icon name="user" />}>Profile</NavbarDropdownItem>
                  <NavbarDropdownItem href="#/settings" icon={<Icon name="settings" />}>Settings</NavbarDropdownItem>
                  <NavbarDropdownItem href="#/usage" disabled icon={<Icon name="download" />}>Usage (unavailable)</NavbarDropdownItem>
                  <NavbarDivider />
                  <NavbarDropdownItem icon={<Icon name="logout" />} onSelect={() => setSignedIn(false)}>Sign out</NavbarDropdownItem>
                </NavbarDropdownContent>
              </NavbarDropdown>
            </NavbarItem>
          ) : (
            <NavbarItem>
              <NavbarAction variant="ghost" onClick={() => setSignedIn(true)}>Sign in</NavbarAction>
            </NavbarItem>
          )}
        </NavbarSection>
      </NavbarContent>
      <NavbarToggle />
      <NavbarMobile>
        <NavbarMobileContent>
          {NAV_ROUTES.map((r) => (
            <NavbarItem key={r.href}>
              <NavbarLink href={r.href} active={route === r.href}>{r.label}</NavbarLink>
            </NavbarItem>
          ))}
          {signedIn ? (
            <>
              <NavbarItem><NavbarLink href="#/profile">Profile</NavbarLink></NavbarItem>
              <NavbarItem><NavbarLink href="#/settings">Settings</NavbarLink></NavbarItem>
            </>
          ) : null}
        </NavbarMobileContent>
      </NavbarMobile>
    </Navbar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <div className="w-full">
      <UserMenuNav />
      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:px-6">
        <p className={NOTE}>Open the account menu from the avatar trigger: arrow keys cycle the items, the disabled Usage entry is skipped, Escape closes and refocuses the trigger, and Sign out flips the bar to its signed-out state.</p>
      </div>
      <DemoArticle route={route} sections={["Workspace", "Recent activity"]} />
    </div>
  );
}''',
)
