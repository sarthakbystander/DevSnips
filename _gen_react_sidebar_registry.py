"""Registry for the DevSnips React Sidebar generator.

Each ``register()`` call adds one variant's metadata + showcase + README
docs + ``tsx_header`` (the header doc comment of its derived ``code.tsx`` —
the shared core is identical family-wide; the variants are distinct
navigation *patterns* expressed through composition of the same 19
exports). The generator (``_gen_react_sidebar.py``) combines the spec here
with the authored reference ``sidebar/code.tsx`` to write ``code.tsx``
(derived), ``code.jsx``, ``preview.html``, ``metadata.json``, ``README.md``.

Realistic, product-oriented demo content only (a developer-focused SaaS
console called "Forge": overview, projects, analytics, team, docs,
settings). No lorem ipsum, no marketing buzzwords, no emoji.
"""
from _gen_react_sidebar import register

TAGS_BASE = ["sidebar", "navigation", "drawer", "react", "tailwind", "accessible", "keyboard", "responsive", "interactive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic nav landmark", "real anchors", "aria-current active item", "collapsed icon rail", "mobile drawer", "keyboard navigation"]
A11Y_BASE = ["aside + nav landmark", "role=dialog aria-modal mobile drawer", "aria-current='page' active item", "aria-expanded collapsible parents", "focus trap + restoration in the drawer", "sr-only labels in the collapsed rail", "aria-disabled inactive items", "focus-visible ring"]

# ---------------------------------------------------------------------------
# Shared props tables (identical API family-wide)
# ---------------------------------------------------------------------------

PROVIDER_PROPS = r"""### `<SidebarProvider>`

| Name | Type | Default | Description |
|---|---|---|---|
| `collapsed` | `boolean` | — | Desktop collapsed (icon-rail) state (controlled). |
| `defaultCollapsed` | `boolean` | `false` | Initial collapsed state (uncontrolled). |
| `onCollapsedChange` | `(collapsed: boolean) => void` | — | Called whenever the collapsed state requests a change. |
| `mobileOpen` | `boolean` | — | Mobile drawer open state (controlled). |
| `defaultMobileOpen` | `boolean` | `false` | Initial mobile drawer open state (uncontrolled). |
| `onMobileOpenChange` | `(open: boolean) => void` | — | Called whenever the drawer requests to open or close. |
| `breakpoint` | `"sm" \| "md" \| "lg"` | `"md"` | Breakpoint below which the sidebar becomes a drawer. |
| `children` | `ReactNode` | — | The application shell (sidebar + main content). |

Renders no DOM of its own — it is the state root + `matchMedia` owner."""

SIDEBAR_PROPS = r"""### `<Sidebar>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | `"Sidebar"` | Accessible name of the `<nav>` landmark and the mobile dialog. |
| `className` | `string` | — | Extra classes on the desktop `<aside>` and the drawer panel. |
| `children` | `ReactNode` | — | `SidebarHeader` / `SidebarContent` / `SidebarFooter` / `SidebarRail`. |

Renders the children twice: once in the persistent desktop `<aside>` (hidden below the breakpoint) and once in the mobile drawer (mounted only while open, hidden at and above the breakpoint)."""

REGION_PROPS = r"""### `<SidebarHeader>` / `<SidebarContent>` / `<SidebarFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the region. |
| `children` | `ReactNode` | — | Region content. |

`SidebarHeader` is the 56px brand row (centers content in the collapsed rail). `SidebarContent` is the scrollable navigation region. `SidebarFooter` is pinned to the bottom with a separating top border. All three forward native `<div>` attributes."""

GROUP_PROPS = r"""### `<SidebarGroup>` / `<SidebarGroupLabel>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Group content / label text. |

`SidebarGroup` wraps one section (label + menu). `SidebarGroupLabel` renders the uppercase eyebrow; in the collapsed rail it becomes sr-only so the section structure stays in the accessibility tree."""

MENU_BUTTON_PROPS = r"""### `<SidebarMenu>` / `<SidebarMenuItem>`

The `<ul>` / `<li>` list structure for navigation rows; both forward native attributes.

### `<SidebarMenuButton>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | — | Navigation target. Present → real `<a>`; absent → real `<button type="button">`. |
| `active` | `boolean` | `false` | Current page: `aria-current="page"` + surface + inset indicator bar. |
| `disabled` | `boolean` | `false` | Non-interactive `aria-disabled` span — never a dead control. |
| `icon` | `ReactNode` | — | Leading icon, rendered `aria-hidden` at 16px. |
| `badge` | `ReactNode` | — | Trailing count/status chip; collapses to a dot + sr-only text in the rail. |
| `tooltip` | `string` | string `children` | Collapsed-rail tooltip text. |
| `onClick` | `() => void` | — | Action callback (button mode; runs before link navigation too). |
| `aria-label` | `string` | — | Accessible name override. |
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Visible label (truncates; sr-only in the collapsed rail). |

In the mobile drawer, activating a link row also closes the drawer."""

COLLAPSIBLE_PROPS = r"""### `<SidebarMenuCollapsible>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | — (required) | Visible + accessible label of the parent row. |
| `icon` | `ReactNode` | — | Leading icon (aria-hidden). |
| `badge` | `ReactNode` | — | Trailing badge, rendered before the chevron. |
| `active` | `boolean` | `false` | A descendant is current: parent-indication treatment (weight, no fill). |
| `disabled` | `boolean` | `false` | Non-interactive `aria-disabled` span. |
| `open` | `boolean` | — | Expanded state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial expanded state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called on every expand/collapse request. |
| `className` | `string` | — | Extra classes on the trigger row. |
| `children` | `ReactNode` | — | The nested level: one `<SidebarMenuSub>`. |

The trigger is a real `<button>` with `aria-expanded` + `aria-controls` pointing at the nested list and a rotating chevron. In the collapsed rail, activating it expands the sidebar and opens the group in one step."""

SUB_PROPS = r"""### `<SidebarMenuSub>` / `<SidebarMenuSubItem>` / `<SidebarMenuSubButton>`

`SidebarMenuSub` is the border-guided nested `<ul>` (it carries the id its collapsible's `aria-controls` points at, and renders nothing in the collapsed rail). `SidebarMenuSubItem` is the `<li>`. `SidebarMenuSubButton` is the 13px nested row — a real `<a>` when `href` is passed, a real `<button>` otherwise, a non-interactive `aria-disabled` span when `disabled`; `active` adds `aria-current="page"` + the active treatment."""

TRIGGER_RAIL_PROPS = r"""### `<SidebarTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes. |

A real 36px `<button type="button" aria-label="Toggle sidebar">` for the page header. Below the breakpoint it opens/closes the drawer; at and above it toggles the collapsed rail. `aria-expanded` + `aria-controls` follow the active mode. Render at most one per provider (it is the focus-restoration target). Native button attributes are forwarded.

### `<SidebarRail>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes. |

A thin edge hit area on the desktop sidebar border that toggles collapse (`aria-expanded` + `aria-controls`). Desktop only — renders nothing inside the mobile drawer."""

SEARCH_PROPS = r"""### `<SidebarSearch>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` | — | Query value (controlled). |
| `defaultValue` | `string` | `""` | Initial query (uncontrolled). |
| `onValueChange` | `(value: string) => void` | — | Called on every change, including clear (with `""`). |
| `placeholder` | `string` | `"Search navigation"` | Placeholder text. |
| `label` | `string` | `"Search navigation"` | Accessible name (sr-only `<label>`). |
| `disabled` | `boolean` | `false` | Disables the field. |
| `id` | `string` | generated | Explicit input id. |
| `className` | `string` | — | Extra classes on the wrapper. |

A real `<input type="search">` with a leading search icon and a clear button (rendered while the query is non-empty). Escape clears the query without closing the drawer. Hidden in the collapsed rail — filtering needs a keyboard."""

NAV_PROPS = r"""### `<SidebarNav>`

| Name | Type | Default | Description |
|---|---|---|---|
| `sections` | `SidebarNavSection[]` | — (required) | The navigation data (see *Navigation Data*). |
| `query` | `string` | `""` | Filter query — case-insensitive label match. |
| `emptyMessage` | `string` | `"No navigation items match …"` | `role="status"` message when nothing matches. |
| `className` | `string` | — | Extra classes on the sections wrapper. |

Parents with an active descendant auto-expand; manual toggles are remembered per item `id`. While a query is active, matching parents keep their subtree and parents of matching children stay visible and expanded.

### `useSidebar()`

Returns the provider context (`collapsed`, `mobileOpen`, `isDesktop`, `requestCollapsed`, `requestMobileOpen`, `closeMobile`, `breakpoint`, landmark ids) for custom shell content — for example a brand wordmark or user card that adapts to the collapsed rail. Throws when used outside `<SidebarProvider>`."""


def props_table() -> str:
    return "\n\n".join([
        PROVIDER_PROPS, SIDEBAR_PROPS, REGION_PROPS, GROUP_PROPS,
        MENU_BUTTON_PROPS, COLLAPSIBLE_PROPS, SUB_PROPS, TRIGGER_RAIL_PROPS,
        SEARCH_PROPS, NAV_PROPS,
    ])


KEYBOARD_BASE = """- **Tab / Shift+Tab** move through the navigation rows, collapsible parents, the search field, and the trigger in DOM order — links behave like links, buttons like buttons (no roving tabindex: navigation lists are a series of ordinary tab stops per the disclosure-navigation pattern).
- **Enter** activates links and buttons; **Space** activates buttons (native behavior — no custom key handlers).
- Collapsible parents are real buttons: Enter/Space toggles `aria-expanded`, and the nested links are ordinary tab stops while the parent is open.
- In the mobile drawer, Tab/Shift+Tab wrap at the drawer boundaries (modal behavior), **Escape** closes the drawer and returns focus to the `SidebarTrigger`, and the built-in "Close navigation" button is the last tab stop.
- In `SidebarSearch`, Escape clears the current query without closing the drawer; the clear control is a real button.
- Activating a collapsed `SidebarMenuCollapsible` icon expands the sidebar and opens its group in one step, so rail users never reach a dead end.
- The `SidebarRail` is a real button (`aria-expanded`) reachable in the tab order directly after the sidebar content."""

NOTES_BASE = """- Geometry is fixed by the shared class constants: 256px expanded, 64px collapsed rail, 288px drawer capped at `100vw - 3rem`, 56px header row. Override via `className` on `<Sidebar>` when a product genuinely needs different geometry.
- The collapsed state is intentionally not persisted — persist the controlled value in your application shell (`localStorage`, a cookie) if the product needs it.
- `SidebarNav` renders up to three indentation levels; deeper hierarchies belong in a different pattern (a tree view or a docs sidebar).
- The previews use hash routing (`#/overview`, `#/projects/backlog`, …) so navigation is demonstrable without a router; `href` values are plain URLs and any router can supply `active`.
- Render at most one `SidebarTrigger` per provider — it is the focus-restoration target for the drawer."""

# ---------------------------------------------------------------------------
# Shared showcase helpers (demo shell, brand, route hook, nav data)
# ---------------------------------------------------------------------------

SHOWCASE_HELPERS = r"""
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const DEMO_BUTTON = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const DEMO_BUTTON_PRIMARY = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] shadow-[var(--ds-shadow-xs)] transition-opacity duration-150 ease-out hover:opacity-90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";

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

function BrandLink() {
  const { collapsed } = useSidebar("BrandLink");
  return (
    <a href="#/overview" aria-label="Forge home" className="flex min-w-0 items-center gap-2 rounded-[var(--ds-radius-sm)] text-sm font-semibold leading-5 tracking-tight text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none">
      <ForgeMark />
      <span className={collapsed ? "sr-only" : "truncate"}>Forge</span>
    </a>
  );
}

function UserBlock() {
  const { collapsed } = useSidebar("UserBlock");
  return (
    <div className={"flex items-center gap-2.5 px-1 py-1" + (collapsed ? " justify-center" : "")}>
      <span aria-hidden="true" className="flex size-7 shrink-0 items-center justify-center rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] text-[11px] font-semibold leading-none text-[var(--ds-color-muted-foreground)]">AK</span>
      <span className={collapsed ? "sr-only" : "min-w-0"}>
        <span className="block truncate text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">Ava Khan</span>
        <span className="block truncate text-xs leading-4 text-[var(--ds-color-muted-foreground)]">ava@forge.dev</span>
      </span>
    </div>
  );
}

function AppShell({ providerProps, sidebar, title, children }) {
  return (
    <SidebarProvider {...(providerProps || {})}>
      <div className="flex w-full items-start">
        {sidebar}
        <div className="min-w-0 flex-1">
          <header className="sticky top-0 z-20 flex h-14 items-center gap-3 border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-4 sm:px-6">
            <SidebarTrigger />
            <p className="m-0 min-w-0 flex-1 truncate text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">{title}</p>
            <span className="hidden shrink-0 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] px-2 py-0.5 text-[11px] font-medium leading-4 text-[var(--ds-color-muted-foreground)] sm:inline-flex">production</span>
          </header>
          <main>{children}</main>
        </div>
      </div>
    </SidebarProvider>
  );
}

function DemoPage({ route, intro, children }) {
  const title = (route || "#/overview").replace(/^#\//, "").split("/").map((s) => s.replace(/^\w/, (c) => c.toUpperCase())).join(" / ");
  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <p className={LABEL}>Current route</p>
      <h2 className="m-0 mt-1 text-2xl font-semibold tracking-tight text-[var(--ds-color-foreground)]">{title}</h2>
      <p className="m-0 mt-2 max-w-prose text-sm leading-6 text-[var(--ds-color-muted-foreground)]">{intro}</p>
      {children}
      <section aria-label="About this workspace" className="mt-10 border-t border-[var(--ds-color-border-subtle)] pt-6">
        <h3 className="m-0 text-base font-semibold text-[var(--ds-color-foreground)]">About this workspace</h3>
        <p className="m-0 mt-2 max-w-prose text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
          Forge is a component-library workspace: teams track design-system work in projects, review adoption in analytics, and coordinate releases with their contributors. The navigation links in this preview are hash routes — activating one updates the location hash, the active sidebar item follows via aria-current, and this page reflects the current route.
        </p>
        <p className="m-0 mt-3 max-w-prose text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
          The sidebar is one composition rendered into two surfaces: a persistent desktop landmark and a mobile drawer. Resize the preview across 375, 768, and 1280 pixels to see the responsive model — the desktop column collapses to an icon rail, and below the breakpoint the navigation becomes an overlaid drawer with focus management.
        </p>
      </section>
    </div>
  );
}

function HelpFooter() {
  return (
    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton href="#/help" icon={<Icon name="help-circle" />}>Help and support</SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  );
}

const APP_NAV = [
  {
    id: "platform",
    label: "Platform",
    items: [
      { id: "overview", label: "Overview", href: "#/overview", icon: <Icon name="grid" /> },
      {
        id: "projects", label: "Projects", icon: <Icon name="folder" />,
        children: [
          { id: "projects-active", label: "Active sprint", href: "#/projects/active" },
          { id: "projects-backlog", label: "Backlog", href: "#/projects/backlog" },
          { id: "projects-releases", label: "Releases", href: "#/projects/releases" },
        ],
      },
      { id: "analytics", label: "Analytics", href: "#/analytics", icon: <Icon name="bar-chart" /> },
      { id: "team", label: "Team", href: "#/team", icon: <Icon name="users" /> },
    ],
  },
  {
    id: "workspace",
    label: "Workspace",
    items: [
      { id: "docs", label: "Documentation", href: "#/docs", icon: <Icon name="book" /> },
      { id: "settings", label: "Settings", href: "#/settings", icon: <Icon name="settings" /> },
    ],
  },
];

function withActive(sections, route) {
  return sections.map((section) => ({
    ...section,
    items: section.items.map((item) => ({
      ...item,
      active: item.href !== undefined && item.href === route,
      children: item.children
        ? item.children.map((child) => ({ ...child, active: child.href === route }))
        : undefined,
    })),
  }));
}
"""

# ---------------------------------------------------------------------------
# 1. sidebar (reference)
# ---------------------------------------------------------------------------

register(
    "sidebar",
    title="Sidebar",
    subcategory="Core",
    description="The canonical application sidebar: a persistent desktop navigation landmark (expandable to an icon rail), a mobile modal drawer with overlay and focus management, and header / content / footer regions with grouped navigation — the reference implementation every other variant in the family composes.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["sidebar-collapsed", "sidebar-mobile", "sidebar-with-groups", "sidebar-dashboard"],
    usage='''import {
  SidebarProvider, Sidebar, SidebarHeader, SidebarContent, SidebarFooter,
  SidebarGroup, SidebarGroupLabel, SidebarMenu, SidebarMenuItem,
  SidebarMenuButton, SidebarMenuCollapsible, SidebarMenuSub,
  SidebarMenuSubItem, SidebarMenuSubButton, SidebarTrigger, SidebarRail,
} from "./sidebar";

<SidebarProvider>
  <div className="flex">
    <Sidebar label="Main">
      <SidebarHeader><a href="/">Acme</a></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Platform</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="/overview" active icon={<GridIcon />}>Overview</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Projects" icon={<FolderIcon />}>
                <SidebarMenuSub>
                  <SidebarMenuSubItem>
                    <SidebarMenuSubButton href="/projects/active">Active sprint</SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                  <SidebarMenuSubItem>
                    <SidebarMenuSubButton href="/projects/backlog">Backlog</SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem><SidebarMenuButton href="/help">Help and support</SidebarMenuButton></SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
    <main>
      <SidebarTrigger />
      …page content…
    </main>
  </div>
</SidebarProvider>''',
    props_doc=props_table(),
    composition_note="This is the reference composition — a header brand, two labeled groups (one plain, one with an expandable parent), a footer help link, the collapse rail, and the page-header trigger. Every other variant in the family uses the same primitives, class constants, states, and accessibility model.",
    behavior_doc="The reference keeps one navigation landmark, one current item (derived from the preview's hash route), and a logical tab order (brand → groups → footer → rail → trigger → page). The `Projects` parent demonstrates the disclosure pattern: `aria-expanded`, a rotating chevron, and a border-guided nested list.",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The reference composition exposes exactly one current item at a time (`aria-current=\"page\"` follows the hash route), one labelled landmark per surface, and sr-only group labels + row labels when the rail is collapsed.",
    responsive_doc="At 1280px the sidebar is a 256px column next to the content. At 768px (the default `md` breakpoint) the same desktop landmark renders; below 768px the trigger opens the drawer instead. Collapse via the trigger or the rail to get the 64px icon rail with measured tooltips.",
    controlled_doc="The reference uses the default uncontrolled provider state. See `sidebar-collapsed` for a controlled `collapsed` example and `sidebar-mobile` for a controlled `mobileOpen` example.",
    notes_doc="Reference implementation for the Sidebar family. It establishes the shared geometry (256px column, 64px rail, 288px drawer, 56px header), the surface/border model, the four row states (idle/hover/active/disabled), the disclosure pattern for nested navigation, and the drawer behavior every other variant extends.\n\n" + NOTES_BASE,
    tsx_header="",
    showcase=SHOWCASE_HELPERS + r'''
function ReferenceSidebar({ route }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Platform</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/overview" active={route === "#/overview"} icon={<Icon name="grid" />}>Overview</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Projects" icon={<Icon name="folder" />} active={route.indexOf("#/projects") === 0} defaultOpen={route.indexOf("#/projects") === 0}>
                <SidebarMenuSub>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/active" active={route === "#/projects/active"}>Active sprint</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/backlog" active={route === "#/projects/backlog"}>Backlog</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/releases" active={route === "#/projects/releases"}>Releases</SidebarMenuSubButton></SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/analytics" active={route === "#/analytics"} icon={<Icon name="bar-chart" />}>Analytics</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/team" active={route === "#/team"} icon={<Icon name="users" />}>Team</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Workspace</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/docs" active={route === "#/docs"} icon={<Icon name="book" />}>Documentation</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/settings" active={route === "#/settings"} icon={<Icon name="settings" />}>Settings</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <AppShell sidebar={<ReferenceSidebar route={route} />} title="Forge Console">
      <DemoPage route={route} intro="The reference sidebar: grouped navigation, an expandable Projects section, a footer help link, a collapse rail on the sidebar edge, and the header trigger that toggles the rail on desktop and opens the drawer on mobile." />
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 2. sidebar-collapsed
# ---------------------------------------------------------------------------

register(
    "sidebar-collapsed",
    title="Sidebar (Collapsed Rail)",
    subcategory="State",
    description="The desktop icon-rail mode: a 64px sidebar with icon-only navigation rows, measured tooltips that expose full labels on hover/focus, sr-only accessible names, badge dots, and one-step expansion — including activating a collapsed parent icon to expand the sidebar and open its group.",
    tags=TAGS_BASE + ["collapsed", "icon-rail", "tooltip"],
    features=FEAT_BASE + ["icon-only rail", "measured tooltips", "sr-only labels", "badge dots", "controlled collapsed state"],
    accessibility=A11Y_BASE + ["tooltip labels on icon-only rows", "accessible names preserved in the rail"],
    interactive=True,
    related=["sidebar", "sidebar-with-badges", "sidebar-dashboard"],
    usage='''const [collapsed, setCollapsed] = useState(true);

<SidebarProvider collapsed={collapsed} onCollapsedChange={setCollapsed}>
  <div className="flex">
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Platform</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="/overview" icon={<GridIcon />} tooltip="Overview">Overview</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="/inbox" icon={<InboxIcon />} badge={4}>Inbox</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
    <main><SidebarTrigger />…</main>
  </div>
</SidebarProvider>

// Activating a collapsed <SidebarMenuCollapsible> icon calls
// onCollapsedChange(false) and opens its group in one step.''',
    props_doc=props_table(),
    composition_note="Same composition as the reference, driven by a controlled `collapsed` value seeded `true` — every row carries an icon and a tooltip label, and the Inbox row carries a badge so the rail's badge-dot behavior is visible.",
    behavior_doc="""Collapsed behavior, row by row:

- **Labels** — the visible label becomes sr-only (the accessible name never leaves the tree), icons center, and a measured fixed-position tooltip shows the full label on hover and keyboard focus.
- **Badges** — the count chip collapses to a dot indicator while the count itself stays in the accessibility tree (sr-only), so "Inbox, 4" is still announced.
- **Collapsible parents** — the chevron and nested list hide; activating the parent icon expands the sidebar AND opens the group in one step, so rail users never reach a dead end.
- **Search and group labels** — `SidebarSearch` hides (filtering needs a keyboard-width field); group labels become sr-only.

The demo exposes Expand/Collapse buttons driving the controlled state, plus the trigger and rail as built-in toggle points.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The rail is not a second-class navigation: every row keeps its accessible name (sr-only label), the current page keeps `aria-current=\"page\"` with the inset indicator bar, and tooltips are a redundant visual affordance (aria-hidden) on top of real accessible names — never the only carrier of meaning.",
    responsive_doc="The rail is a desktop mode (it exists at and above the breakpoint). Below the breakpoint the drawer always renders the full expanded layout — collapsing is meaningless in an overlay. The rail keeps a fixed 64px width, so it can never cause horizontal overflow.",
    controlled_doc="""This variant is the controlled `collapsed` reference:

```tsx
const [collapsed, setCollapsed] = useState(true);
<SidebarProvider collapsed={collapsed} onCollapsedChange={setCollapsed}>…</SidebarProvider>
```

Trigger clicks, rail clicks, and collapsed-parent activations all flow through `onCollapsedChange` — watch the demo's state readout as you use any of them.""",
    notes_doc="Establishes the collapsed-rail system: 64px fixed width, centered 16px icons, sr-only labels, measured tooltips (fixed position so the content scroll container cannot clip them), badge dots with sr-only counts, hidden group labels/search, and one-step expand-and-open for collapsible parents.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — collapsed rail variant.
 *
 * Desktop icon-rail mode: 64px icon-only rows with measured fixed-position
 * tooltips, sr-only accessible labels, badge dots, and one-step
 * expand-and-open for collapsible parents. The implementation core is
 * identical to the reference `sidebar` — this variant is the collapsed
 * *pattern* (controlled `collapsed` state, icon-forward composition).
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function CollapsedSidebar({ route }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Platform</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/overview" active={route === "#/overview"} icon={<Icon name="grid" />}>Overview</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Projects" icon={<Icon name="folder" />} active={route.indexOf("#/projects") === 0}>
                <SidebarMenuSub>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/active" active={route === "#/projects/active"}>Active sprint</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/backlog" active={route === "#/projects/backlog"}>Backlog</SidebarMenuSubButton></SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/analytics" active={route === "#/analytics"} icon={<Icon name="bar-chart" />}>Analytics</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/inbox" active={route === "#/inbox"} icon={<Icon name="inbox" />} badge={4}>Inbox</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/team" active={route === "#/team"} icon={<Icon name="users" />}>Team</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Workspace</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/docs" active={route === "#/docs"} icon={<Icon name="book" />}>Documentation</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/settings" active={route === "#/settings"} icon={<Icon name="settings" />}>Settings</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [collapsed, setCollapsed] = React.useState(true);
  return (
    <AppShell
      providerProps={{ collapsed: collapsed, onCollapsedChange: setCollapsed }}
      sidebar={<CollapsedSidebar route={route} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="The sidebar loads collapsed: a 64px icon rail with tooltips on hover and focus. Expand it with the header trigger, the edge rail, the buttons below, or by activating the Projects icon — every toggle point drives the same controlled state.">
        <div className="mt-6 flex flex-wrap items-center gap-2">
          <button type="button" className={DEMO_BUTTON} onClick={() => setCollapsed(true)}>Collapse</button>
          <button type="button" className={DEMO_BUTTON_PRIMARY} onClick={() => setCollapsed(false)}>Expand</button>
          <p role="status" className="m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
            Rail state: <strong className="font-medium text-[var(--ds-color-foreground)]">{collapsed ? "collapsed" : "expanded"}</strong>
          </p>
        </div>
        <p className="m-0 mt-4 max-w-prose text-sm leading-6 text-[var(--ds-color-muted-foreground)]">
          While collapsed, hover or keyboard-focus any icon row to see its measured tooltip, and note that the Inbox count collapses to a dot while staying in the accessibility tree. Activating the Projects icon expands the sidebar and opens the group in one step.
        </p>
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 3. sidebar-mobile
# ---------------------------------------------------------------------------

register(
    "sidebar-mobile",
    title="Sidebar (Mobile Drawer)",
    subcategory="Responsive",
    description="The mobile navigation drawer, demonstrated explicitly: a controlled drawer with an overlay, dialog semantics, a focus trap, body scroll lock, Escape and outside-pointer close, focus restoration to the trigger, and an event log of every open/close request.",
    tags=TAGS_BASE + ["mobile", "drawer", "overlay", "focus-trap"],
    features=FEAT_BASE + ["modal drawer", "overlay", "scroll lock", "focus trap", "focus restoration", "controlled open state"],
    accessibility=A11Y_BASE + ["role=dialog aria-modal", "Escape + outside-pointer close", "focus returns to the trigger"],
    interactive=True,
    related=["sidebar", "sidebar-collapsed", "sidebar-dashboard"],
    usage='''const [mobileOpen, setMobileOpen] = useState(false);

<SidebarProvider mobileOpen={mobileOpen} onMobileOpenChange={setMobileOpen}>
  <div className="flex">
    <Sidebar label="Main">…navigation…</Sidebar>
    <main>
      <SidebarTrigger />  {/* opens the drawer below the breakpoint */}
      …page content…
    </main>
  </div>
</SidebarProvider>

// The drawer is a modal dialog: overlay, focus trap, scroll lock,
// Escape / outside-pointer close, focus restored to the trigger.''',
    props_doc=props_table(),
    composition_note="The same reference composition, driven by a controlled `mobileOpen` value. The demo adds an explicit Open button and a live event log so every drawer request (trigger, Escape, overlay pointer, close button, in-drawer navigation) is observable.",
    behavior_doc="""The drawer is the mobile form of the SAME navigation — not a shrunken sidebar:

- **Open** — the trigger (or any call to `onMobileOpenChange(true)`) mounts the drawer: overlay, `role="dialog" aria-modal="true"`, focus moves to the first navigation control, body scroll locks with scrollbar-width compensation.
- **Close paths** — Escape, the built-in "Close navigation" button (last tab stop), a pointer down on the overlay, or activating any navigation link inside the drawer. Every path flows through `onMobileOpenChange` and restores focus to the trigger.
- **Tab containment** — Tab/Shift+Tab wrap at the drawer boundaries while it is open; the background is inert to pointer and keyboard alike.
- **Resize** — resizing to desktop while the drawer is open closes it cleanly and releases the scroll lock.

Resize the preview below 768px to exercise the drawer; above the breakpoint the same composition renders as the persistent column.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The drawer implements the modal-dialog pattern honestly: `role=\"dialog\"` + `aria-modal=\"true\"` + an accessible name (the `label` prop), a real focus trap, a visible close control, scroll lock, and focus restoration. It deliberately does NOT fake modality with an overlay alone.",
    responsive_doc="At 375px the drawer is 288px wide (capped at `100vw - 3rem`), the overlay covers the rest of the viewport, and long labels truncate safely. At 768px the persistent column takes over and the drawer cannot be opened. No horizontal overflow at any width — the drawer is `fixed` and the column is `display: none` below the breakpoint.",
    controlled_doc="""This variant is the controlled `mobileOpen` reference:

```tsx
const [mobileOpen, setMobileOpen] = useState(false);
<SidebarProvider mobileOpen={mobileOpen} onMobileOpenChange={setMobileOpen}>…</SidebarProvider>
```

The demo logs every request — open it with the explicit button, then close it via Escape, the overlay, the close button, or a navigation link, and watch the log update.""",
    notes_doc="Establishes the drawer behavior contract for the family: dialog semantics, focus trap + restoration, scroll lock with scrollbar compensation, four close paths, and the auto-close-on-desktop-resize guard.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — mobile drawer variant.
 *
 * The mobile form of the sidebar: a modal navigation drawer (role=dialog,
 * aria-modal) with an overlay, focus trap, body scroll lock, Escape /
 * outside-pointer / close-button / navigation close paths, and focus
 * restoration to the trigger. The implementation core is identical to the
 * reference `sidebar` — this variant documents and demonstrates the
 * controlled `mobileOpen` pattern.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function MobileSidebar({ route }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarNav sections={withActive(APP_NAV, route)} />
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const [log, setLog] = React.useState([]);
  function record(open) {
    setMobileOpen(open);
    setLog((current) => ["Drawer " + (open ? "opened" : "closed") + " (" + new Date().toLocaleTimeString() + ")"].concat(current).slice(0, 4));
  }
  return (
    <AppShell
      providerProps={{ mobileOpen: mobileOpen, onMobileOpenChange: record }}
      sidebar={<MobileSidebar route={route} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="The drawer is the mobile form of the navigation. Resize the preview below 768px and open it with the header trigger or the button below: overlay, focus trap, scroll lock, Escape / outside-pointer close, and focus restoration — all driven by a controlled state you can observe in the event log.">
        <div className="mt-6 flex flex-wrap items-center gap-2">
          <button type="button" className={DEMO_BUTTON_PRIMARY} onClick={() => record(true)}>Open navigation drawer</button>
          <p className="m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
            (below the 768px breakpoint — on desktop this opens nothing visible)
          </p>
        </div>
        <div className="mt-6">
          <p className={LABEL}>Drawer event log</p>
          {log.length === 0 ? (
            <p role="status" className="m-0 mt-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">No drawer events yet.</p>
          ) : (
            <ul className="m-0 mt-2 list-none space-y-1 p-0">
              {log.map((entry) => (
                <li key={entry} className="rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-subtle)] bg-[var(--ds-color-surface)] px-3 py-1.5 text-sm leading-5 text-[var(--ds-color-foreground)]">{entry}</li>
              ))}
            </ul>
          )}
        </div>
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 4. sidebar-with-groups
# ---------------------------------------------------------------------------

register(
    "sidebar-with-groups",
    title="Sidebar with Groups",
    subcategory="Structure",
    description="Sectioned navigation: multiple labeled groups (Platform, Workspace, Admin) with a clear hierarchy, an unlabeled primary group, and group labels that stay in the accessibility tree when the rail is collapsed.",
    tags=TAGS_BASE + ["groups", "sections", "labels"],
    features=FEAT_BASE + ["labeled navigation groups", "section hierarchy", "sr-only group labels in the rail"],
    accessibility=A11Y_BASE + ["section structure announced via group labels"],
    interactive=True,
    related=["sidebar", "sidebar-collapsible-groups", "sidebar-dashboard"],
    usage='''<SidebarContent>
  <SidebarGroup>
    <SidebarMenu>…primary items…</SidebarMenu>
  </SidebarGroup>
  <SidebarGroup>
    <SidebarGroupLabel>Workspace</SidebarGroupLabel>
    <SidebarMenu>…workspace items…</SidebarMenu>
  </SidebarGroup>
  <SidebarGroup>
    <SidebarGroupLabel>Admin</SidebarGroupLabel>
    <SidebarMenu>…admin items…</SidebarMenu>
  </SidebarGroup>
</SidebarContent>''',
    props_doc=props_table(),
    composition_note="Three labeled groups plus one unlabeled primary group. Group labels are optional per group — the primary navigation needs no eyebrow, secondary sections read better with one.",
    behavior_doc="""Groups give the navigation a reading order:

- **Unlabeled primary group** — the top-level destinations (Overview, Inbox) need no eyebrow; they are the product's front door.
- **Labeled groups** — `Workspace` and `Admin` eyebrows separate secondary and privileged destinations. Labels are 11px uppercase eyebrows, visually quiet and clearly not interactive.
- **Collapsed rail** — labels become sr-only: the rail stays visually clean while screen readers still announce the section structure.

Groups are purely structural — for groups the user can collapse, see `sidebar-collapsible-groups`.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Group labels are real text (not aria-described decoration): expanded they are visible eyebrows, collapsed they become sr-only, and the `<ul>` list structure underneath keeps its list semantics either way.",
    responsive_doc="Groups stack identically in the drawer and the column; the 16px inter-group gap and eyebrow rhythm survive both surfaces. At 375px group labels truncate nothing (they are short by design) and the sections read top to bottom.",
    controlled_doc="Groups carry no state of their own — the provider's collapsed/mobile state governs presentation. For collapsible groups with independent open state, see `sidebar-collapsible-groups`.",
    notes_doc="Demonstrates the section model: optional labels, quiet eyebrow typography, consistent 16px section gaps, and sr-only label preservation in the rail.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — grouped navigation variant.
 *
 * Sectioned navigation with labeled groups (Platform / Workspace / Admin)
 * and an unlabeled primary group. Group labels stay in the accessibility
 * tree when the rail is collapsed. The implementation core is identical
 * to the reference `sidebar` — this variant is the grouping *pattern*.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function GroupedSidebar({ route }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/overview" active={route === "#/overview"} icon={<Icon name="grid" />}>Overview</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/inbox" active={route === "#/inbox"} icon={<Icon name="inbox" />}>Inbox</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Workspace</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/projects" active={route === "#/projects"} icon={<Icon name="folder" />}>Projects</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/analytics" active={route === "#/analytics"} icon={<Icon name="bar-chart" />}>Analytics</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/docs" active={route === "#/docs"} icon={<Icon name="book" />}>Documentation</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Admin</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/members" active={route === "#/members"} icon={<Icon name="users" />}>Members</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/billing" active={route === "#/billing"} icon={<Icon name="package" />}>Billing</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/audit-log" active={route === "#/audit-log"} icon={<Icon name="file" />}>Audit log</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <AppShell sidebar={<GroupedSidebar route={route} />} title="Forge Console">
      <DemoPage route={route} intro="Sectioned navigation: an unlabeled primary group, then Workspace and Admin eyebrows. Collapse the sidebar with the edge rail — the labels leave the visual tree but stay in the accessibility tree." />
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 5. sidebar-with-nested-navigation
# ---------------------------------------------------------------------------

register(
    "sidebar-with-nested-navigation",
    title="Sidebar with Nested Navigation",
    subcategory="Navigation",
    description="Expandable nested navigation: collapsible parent rows with aria-expanded, border-guided child lists, an active child that keeps its parent indicated, and a deliberate two-to-three-level depth cap with sensible indentation.",
    tags=TAGS_BASE + ["nested", "collapsible", "submenu", "tree"],
    features=FEAT_BASE + ["expandable parents", "aria-expanded disclosure", "border-guided nested lists", "active descendant indication"],
    accessibility=A11Y_BASE + ["disclosure pattern for nested levels"],
    interactive=True,
    related=["sidebar-with-active-state", "sidebar-collapsible-groups", "sidebar-dashboard"],
    usage='''<SidebarMenuItem>
  <SidebarMenuCollapsible label="Projects" icon={<FolderIcon />} active={childIsActive}>
    <SidebarMenuSub>
      <SidebarMenuSubItem>
        <SidebarMenuSubButton href="/projects/active" active>Active sprint</SidebarMenuSubButton>
      </SidebarMenuSubItem>
      <SidebarMenuSubItem>
        <SidebarMenuSubButton href="/projects/backlog">Backlog</SidebarMenuSubButton>
      </SidebarMenuSubItem>
    </SidebarMenuSub>
  </SidebarMenuCollapsible>
</SidebarMenuItem>''',
    props_doc=props_table(),
    composition_note="Two collapsible parents (Projects, Documentation) plus a third-level example: the `Components` child carries its own always-visible nested list, demonstrating the family's deliberate depth cap — collapsibles own the first nested level, and a third level renders as an indented static list rather than another disclosure.",
    behavior_doc="""Nested navigation behavior:

- **Expandable parents** — `SidebarMenuCollapsible` owns its open state (`defaultOpen` seeds it); the trigger carries `aria-expanded` + `aria-controls` pointing at the actual nested list, and the chevron rotates with state.
- **Active descendants** — when a child route is current, the parent receives the `active` prop: medium-weight foreground text (indication WITHOUT the surface fill, which belongs to the current page itself). The current child carries `aria-current="page"`.
- **Depth cap** — the first nested level is a disclosure; the third level (`Components → Buttons / Inputs / Tables`) renders as an indented static list. Deeper trees belong in a docs-sidebar or tree-view pattern, not in a flyout of disclosures.
- **Guide borders** — nested lists sit on a 1px border guide aligned under the parent icon, so hierarchy reads at a glance in both themes.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Each parent is one tab stop with honest `aria-expanded`; nested links are ordinary tab stops while open and are removed from the tab order while closed (the list unmounts). The parent indication never uses `aria-current` — that stays on the actual page link.",
    responsive_doc="Nested lists indent with a border guide rather than large padding, so even three levels fit the 288px drawer at 375px without truncation. In the collapsed rail, parents collapse to icons and activating one expands the sidebar with its group already open.",
    controlled_doc="Each `SidebarMenuCollapsible` is independently controllable (`open` + `onOpenChange`). For many parents driven from one state map — plus expand-all/collapse-all — see `sidebar-collapsible-groups`. For automatic expansion driven by the active route, see `sidebar-with-active-state`.",
    notes_doc="Establishes the nesting model: disclosure parents, border-guided sub lists, parent-with-active-descendant indication, and the two-to-three-level depth cap.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — nested navigation variant.
 *
 * Expandable parent rows (aria-expanded disclosure), border-guided child
 * lists, active-descendant indication, and a deliberate depth cap: the
 * first nested level is a disclosure, the third an indented static list.
 * The implementation core is identical to the reference `sidebar` — this
 * variant is the nesting *pattern*.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function NestedSidebar({ route }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Platform</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/overview" active={route === "#/overview"} icon={<Icon name="grid" />}>Overview</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Projects" icon={<Icon name="folder" />} active={route.indexOf("#/projects") === 0} defaultOpen>
                <SidebarMenuSub>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/active" active={route === "#/projects/active"}>Active sprint</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem>
                    <SidebarMenuSubButton href="#/projects/components" active={route === "#/projects/components"}>Components</SidebarMenuSubButton>
                    <SidebarMenuSub>
                      <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/components/buttons" active={route === "#/projects/components/buttons"}>Buttons</SidebarMenuSubButton></SidebarMenuSubItem>
                      <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/components/inputs" active={route === "#/projects/components/inputs"}>Inputs</SidebarMenuSubButton></SidebarMenuSubItem>
                      <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/components/tables" active={route === "#/projects/components/tables"}>Tables</SidebarMenuSubButton></SidebarMenuSubItem>
                    </SidebarMenuSub>
                  </SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/backlog" active={route === "#/projects/backlog"}>Backlog</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/releases" active={route === "#/projects/releases"} disabled>Releases (soon)</SidebarMenuSubButton></SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Documentation" icon={<Icon name="book" />} active={route.indexOf("#/docs") === 0}>
                <SidebarMenuSub>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/docs/guides" active={route === "#/docs/guides"}>Guides</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/docs/api" active={route === "#/docs/api"}>API reference</SidebarMenuSubButton></SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <AppShell sidebar={<NestedSidebar route={route} />} title="Forge Console">
      <DemoPage route={route} intro="Nested navigation with real disclosure behavior: expand Projects and Documentation with click or keyboard (aria-expanded, rotating chevron), navigate to a child route, and note the parent indication. The Components child shows the third level as an indented static list — the deliberate depth cap." />
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 6. sidebar-with-active-state
# ---------------------------------------------------------------------------

register(
    "sidebar-with-active-state",
    title="Sidebar with Active State",
    subcategory="Navigation",
    description="Realistic route-driven navigation built on the typed SidebarNav renderer: aria-current on the current page, automatic parent expansion when a child route is active, and parent indication that never steals the current page's treatment.",
    tags=TAGS_BASE + ["active", "routing", "aria-current", "data-driven"],
    features=FEAT_BASE + ["route-driven active item", "auto-expanding parents", "typed SidebarNav renderer"],
    accessibility=A11Y_BASE + ["exactly one aria-current item", "parent indication without aria-current"],
    interactive=True,
    related=["sidebar-with-nested-navigation", "sidebar-with-search", "sidebar-dashboard"],
    usage='''const sections: SidebarNavSection[] = [
  {
    id: "platform",
    label: "Platform",
    items: [
      { id: "overview", label: "Overview", href: "/overview", icon: <GridIcon /> },
      {
        id: "projects", label: "Projects", icon: <FolderIcon />,
        children: [
          { id: "projects-active", label: "Active sprint", href: "/projects/active" },
          { id: "projects-backlog", label: "Backlog", href: "/projects/backlog" },
        ],
      },
    ],
  },
];

// Derive `active` from the current route, then render:
<SidebarNav sections={withActive(sections, pathname)} />''',
    props_doc=props_table(),
    composition_note="This variant is the data-driven reference: navigation is declared as `SidebarNavSection[]` data and rendered by `SidebarNav`, with `active` derived from the preview's hash route — the pattern a routed app uses with `pathname`.",
    behavior_doc="""Active-state behavior end to end:

- **Current page** — exactly one row carries `aria-current="page"` with the active surface, medium weight, AND the 2px inset indicator bar (state survives color-blindness and dark mode).
- **Active child, closed parent** — navigate directly to a child route (e.g. open the preview at `#/projects/backlog`): the Projects parent renders already expanded, because `SidebarNav` auto-expands parents with an active descendant.
- **Parent indication** — the parent of the current page gets medium-weight foreground text WITHOUT the surface fill or `aria-current`; scanning the tree, the current page is always unambiguous.
- **Manual override wins** — collapse the parent of the active child by hand and it stays closed until you navigate again (per-item override map).""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="`aria-current=\"page\"` appears exactly once per navigation landmark at all times, on the row that represents the current route. The parent indication is conveyed by weight + the disclosure state — complementary cues, never a second `aria-current`.",
    responsive_doc="The active treatment is identical in the column, the rail (indicator bar + surface), and the drawer. Navigating from inside the drawer closes it, so the user lands on the new route with focus back on the trigger.",
    controlled_doc="""The renderer composes controlled collapsibles internally: the expansion state is `override ?? auto(active descendant)`. Setting the override map is how "collapse the parent of the current page" stays possible.

```tsx
<SidebarNav sections={withActive(SECTIONS, pathname)} />
```

`withActive` in the demo is a 10-line mapper — derive `active` however your router exposes the current path.""",
    notes_doc="Demonstrates the route-driven model: `active` derived from the location, auto-expanding parents, per-item manual overrides, and exactly-one-current invariant.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — active state variant.
 *
 * Route-driven navigation rendered from typed SidebarNav data: one
 * aria-current item, auto-expanding parents with an active descendant,
 * parent indication without aria-current, and per-item expansion
 * overrides. The implementation core is identical to the reference
 * `sidebar` — this variant is the active-state *pattern*.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function ActiveSidebar({ route }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarNav sections={withActive(APP_NAV, route)} />
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  return (
    <AppShell sidebar={<ActiveSidebar route={route} />} title="Forge Console">
      <DemoPage route={route} intro="Navigation rendered from typed data via SidebarNav, with the active item derived from the hash route. Navigate into Projects: the parent auto-expands, the child takes aria-current, and the parent keeps a weight-only indication. Open this preview directly at #/projects/backlog to see the auto-expanded parent on load.">
        <div className="mt-6 flex flex-wrap gap-2">
          <a className={DEMO_BUTTON} href="#/overview">Go to Overview</a>
          <a className={DEMO_BUTTON} href="#/projects/backlog">Go to Projects / Backlog</a>
          <a className={DEMO_BUTTON} href="#/analytics">Go to Analytics</a>
        </div>
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 7. sidebar-with-badges
# ---------------------------------------------------------------------------

register(
    "sidebar-with-badges",
    title="Sidebar with Badges",
    subcategory="Content",
    description="Notification and status badges on navigation rows: tabular count chips that never break layout, text status chips, a live count that genuinely updates, and the collapsed rail's dot-plus-sr-only badge treatment.",
    tags=TAGS_BASE + ["badges", "counts", "notifications", "status"],
    features=FEAT_BASE + ["count badges", "status badges", "live badge updates", "badge dots in the rail"],
    accessibility=A11Y_BASE + ["badges readable in the accessibility tree"],
    interactive=True,
    related=["sidebar-collapsed", "sidebar-dashboard"],
    usage='''<SidebarMenuItem>
  <SidebarMenuButton href="/inbox" icon={<InboxIcon />} badge={unreadCount}>
    Inbox
  </SidebarMenuButton>
</SidebarMenuItem>
<SidebarMenuItem>
  <SidebarMenuButton href="/labs" icon={<SparklesIcon />} badge="Beta">
    Labs
  </SidebarMenuButton>
</SidebarMenuItem>

// Collapsed rail: the chip becomes a dot; the count stays sr-only.''',
    props_doc=props_table(),
    composition_note="Badges on three rows: a live Inbox count (with a working " + '"Mark all read"' + " action), a static Notifications count, and a Beta status chip on Labs — the three badge kinds the system supports.",
    behavior_doc="""Badge behavior:

- **Count chips** — small bordered pills with tabular numerals, sitting in the row's `ml-auto` trailing slot. They never stretch the row, wrap, or push the label: the label truncates first.
- **Status chips** — short text ("Beta") in the same geometry for state that is not a number.
- **Live updates** — the Inbox count is real state: "Mark all read" clears it, and the row settles back to icon + label without a layout jump.
- **Collapsed rail** — chips become a 6px dot at the row's corner while the count text stays in the accessibility tree (sr-only), so "Inbox, 4" remains announced. The dot is a supplementary signal, never the only carrier.

Badges communicate counts and status — they are not decoration. Rows without something to say carry no badge.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Badge text is part of the row's accessible name in both modes (visible chip when expanded, sr-only when collapsed). The count updates are not announced aggressively — navigation badges are ambient information; a live region would be noise on every poll.",
    responsive_doc="Chips keep their 20px height at every width and truncate nothing; in the drawer they render exactly as in the expanded column. At 375px a long label truncates before the badge moves.",
    controlled_doc="Badges are pure presentation — the demo's Inbox count is ordinary React state. Feed counts from your data layer and pass them as `badge`.",
    notes_doc="Establishes the badge system: 20px tabular count chips, text status chips, dot-plus-sr-only collapsed treatment, and layout stability (labels truncate, badges never wrap).\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — badges variant.
 *
 * Notification count chips and status chips on navigation rows: tabular
 * numerals in a trailing slot that never breaks layout, live count
 * updates, and the collapsed rail's dot + sr-only treatment. The
 * implementation core is identical to the reference `sidebar` — this
 * variant is the badge *pattern*.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function BadgesSidebar({ route, inboxCount, onMarkAllRead }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Platform</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/overview" active={route === "#/overview"} icon={<Icon name="grid" />}>Overview</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/inbox" active={route === "#/inbox"} icon={<Icon name="inbox" />} badge={inboxCount > 0 ? inboxCount : undefined}>Inbox</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/notifications" active={route === "#/notifications"} icon={<Icon name="bell" />} badge={12}>Notifications</SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/labs" active={route === "#/labs"} icon={<Icon name="sparkles" />} badge="Beta">Labs</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Inbox actions</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton onClick={onMarkAllRead} disabled={inboxCount === 0} icon={<Icon name="check" />}>Mark all read</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [inboxCount, setInboxCount] = React.useState(4);
  return (
    <AppShell
      sidebar={<BadgesSidebar route={route} inboxCount={inboxCount} onMarkAllRead={() => setInboxCount(0)} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="Badges that mean something: a live Inbox count (use Mark all read to clear it), a static Notifications count, and a Beta status chip. Collapse the sidebar with the edge rail to see chips become dots while the counts stay in the accessibility tree.">
        <p role="status" className="m-0 mt-6 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
          Unread inbox items: <strong className="font-medium text-[var(--ds-color-foreground)]">{inboxCount}</strong>
        </p>
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 8. sidebar-with-user
# ---------------------------------------------------------------------------

register(
    "sidebar-with-user",
    title="Sidebar with User Area",
    subcategory="Content",
    description="A user/profile area pinned to the sidebar footer: identity block (avatar, name, email) that adapts to the collapsed rail, account actions as real rows, and a clear border separation between navigation and account space.",
    tags=TAGS_BASE + ["user", "profile", "account", "footer"],
    features=FEAT_BASE + ["user identity block", "account actions", "rail-adaptive footer"],
    accessibility=A11Y_BASE + ["decorative avatar", "real account links/actions"],
    interactive=True,
    related=["sidebar-with-footer-actions", "sidebar-dashboard"],
    usage='''<SidebarFooter>
  <div className="user-block">
    <Avatar name="Ava Khan" />
    <div>
      <p>Ava Khan</p>
      <p>ava@acme.dev</p>
    </div>
  </div>
  <SidebarMenu>
    <SidebarMenuItem>
      <SidebarMenuButton href="/account" icon={<UserIcon />}>Account</SidebarMenuButton>
    </SidebarMenuItem>
    <SidebarMenuItem>
      <SidebarMenuButton onClick={signOut} icon={<LogoutIcon />}>Sign out</SidebarMenuButton>
    </SidebarMenuItem>
  </SidebarMenu>
</SidebarFooter>''',
    props_doc=props_table(),
    composition_note="The footer composes a custom identity block (plain layout, driven by `useSidebar()` so it adapts to the rail) above two account rows — one link, one action. This is the intended way to build user areas: custom layout + the family's row primitives, not a special-case component.",
    behavior_doc="""The user area is a footer composition, not a widget:

- **Identity block** — initials avatar (decorative, `aria-hidden`), name, and email. In the collapsed rail the text becomes sr-only and the avatar centers — the account is still identifiable and announced.
- **Account actions** — `Account` is a real link; `Sign out` is a real button action. Both are ordinary `SidebarMenuButton` rows with the family's full state system (hover, focus ring, tooltips in the rail).
- **Separation** — the footer's top border and bottom pinning keep account space visually distinct from navigation at every height.
- **`useSidebar()`** — the identity block reads `collapsed` from context to adapt its layout; that hook is the supported escape hatch for custom shell content.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The avatar is decorative (`aria-hidden`) because the adjacent name text identifies the user; the block carries no interactive role of its own. Actions are real rows with accessible names from their visible labels (sr-only-preserved in the rail).",
    responsive_doc="The footer pins to the bottom of both surfaces. In the drawer the identity block always renders expanded; in the rail it collapses to the centered avatar. The email truncates instead of overflowing at any width.",
    controlled_doc="The identity block is plain React reading `useSidebar()` — no extra state model. `Sign out` is your handler; the demo logs the action.",
    notes_doc="Demonstrates the user-area pattern: decorative avatar, sr-only collapse adaptation via `useSidebar()`, account rows as standard primitives, and footer separation.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — user area variant.
 *
 * A user/profile area pinned to the footer: an identity block that adapts
 * to the collapsed rail via useSidebar(), account actions as standard
 * rows, and clear footer separation. The implementation core is identical
 * to the reference `sidebar` — this variant is the user-area *pattern*.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function UserSidebar({ route, onSignOut }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarNav sections={withActive(APP_NAV, route)} />
      </SidebarContent>
      <SidebarFooter>
        <UserBlock />
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton href="#/account" active={route === "#/account"} icon={<Icon name="user" />}>Account</SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={onSignOut} icon={<Icon name="logout" />}>Sign out</SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [lastAction, setLastAction] = React.useState(null);
  return (
    <AppShell
      sidebar={<UserSidebar route={route} onSignOut={() => setLastAction("Sign out requested at " + new Date().toLocaleTimeString())} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="The user area pinned to the footer: identity block, account link, and a real sign-out action. Collapse the sidebar — the name and email leave the visual tree but stay announced, and the avatar keeps the account identifiable.">
        <p role="status" className="m-0 mt-6 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
          {lastAction || "No account action taken yet."}
        </p>
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 9. sidebar-with-footer-actions
# ---------------------------------------------------------------------------

register(
    "sidebar-with-footer-actions",
    title="Sidebar with Footer Actions",
    subcategory="Composite",
    description="Settings, help, and sign-out-style actions in the footer: real links and real buttons with the family's full interaction states, separated from navigation by the footer border, and fully keyboard accessible in both surfaces.",
    tags=TAGS_BASE + ["footer", "actions", "settings", "logout"],
    features=FEAT_BASE + ["footer action rows", "real buttons and links", "working action feedback"],
    accessibility=A11Y_BASE + ["actions announced as links/buttons"],
    interactive=True,
    related=["sidebar-with-user", "sidebar-dashboard"],
    usage='''<SidebarFooter>
  <SidebarMenu>
    <SidebarMenuItem>
      <SidebarMenuButton href="/settings" icon={<SettingsIcon />}>Settings</SidebarMenuButton>
    </SidebarMenuItem>
    <SidebarMenuItem>
      <SidebarMenuButton href="/help" icon={<HelpIcon />}>Help and support</SidebarMenuButton>
    </SidebarMenuItem>
    <SidebarMenuItem>
      <SidebarMenuButton onClick={signOut} icon={<LogoutIcon />}>Sign out</SidebarMenuButton>
    </SidebarMenuItem>
  </SidebarMenu>
</SidebarFooter>''',
    props_doc=props_table(),
    composition_note="Three footer action rows — two links (Settings, Help) and one real button action (Sign out) with genuine demo feedback — below the standard grouped navigation. No user block: see `sidebar-with-user` for that composition.",
    behavior_doc="""Footer actions behave like the rest of the system:

- **Links are links** — Settings and Help navigate (hash routes in the preview); they get the active treatment when current.
- **Actions are buttons** — Sign out is a real `<button type="button">`: Enter/Space activates it, and the demo signs the workspace out for real (the page reports the state and offers a way back).
- **Same states everywhere** — hover, `focus-visible` ring, active, disabled, rail tooltips: footer rows are the same primitive as navigation rows, so nothing behaves differently at the bottom of the sidebar.
- **Separation** — the footer's top border separates account chrome from navigation; the region pins to the bottom regardless of content height.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Footer actions keep their accessible names in the rail (sr-only labels + tooltips), and the sign-out feedback is a `role=\"status\"` region so the result is announced without moving focus.",
    responsive_doc="Footer rows behave identically in the column, the rail, and the drawer — including closing the drawer when a footer LINK is activated (actions that do not navigate keep the drawer open).",
    controlled_doc="Actions are ordinary callbacks. The demo's sign-out flow is local state; wire the real thing to your auth layer.",
    notes_doc="Establishes the footer-action pattern: links vs buttons chosen honestly, status feedback for non-navigating actions, and border separation.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — footer actions variant.
 *
 * Settings / help / sign-out actions in the footer: real links and real
 * buttons with the family's full state system, status feedback for
 * non-navigating actions, and border separation from navigation. The
 * implementation core is identical to the reference `sidebar` — this
 * variant is the footer-actions *pattern*.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function ActionsSidebar({ route, onSignOut }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarNav sections={withActive(APP_NAV, route)} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton href="#/settings" active={route === "#/settings"} icon={<Icon name="settings" />}>Settings</SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton href="#/help" active={route === "#/help"} icon={<Icon name="help-circle" />}>Help and support</SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={onSignOut} icon={<Icon name="logout" />}>Sign out</SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [signedOutAt, setSignedOutAt] = React.useState(null);
  return (
    <AppShell
      sidebar={<ActionsSidebar route={route} onSignOut={() => setSignedOutAt(new Date().toLocaleTimeString())} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="Footer actions as honest controls: Settings and Help are real links (they navigate and take the active treatment), Sign out is a real button with genuine feedback below.">
        {signedOutAt ? (
          <div role="status" className="mt-6 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4">
            <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">Signed out at {signedOutAt}</p>
            <p className="m-0 mt-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">The demo session ended. Sign back in to continue.</p>
            <button type="button" className={DEMO_BUTTON_PRIMARY + " mt-3"} onClick={() => setSignedOutAt(null)}>Sign back in</button>
          </div>
        ) : (
          <p role="status" className="m-0 mt-6 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">Workspace session active.</p>
        )}
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 10. sidebar-with-search
# ---------------------------------------------------------------------------

register(
    "sidebar-with-search",
    title="Sidebar with Search",
    subcategory="Filtering",
    description="A working navigation filter: a labelled search field that genuinely filters the tree case-insensitively, keeps parents of matching children visible and expanded, renders a status-message empty state, and clears via button or Escape.",
    tags=TAGS_BASE + ["search", "filter", "find"],
    features=FEAT_BASE + ["real navigation filtering", "parent-preserving matches", "empty state", "clear + Escape reset"],
    accessibility=A11Y_BASE + ["labelled search field", "role=status empty state"],
    interactive=True,
    related=["sidebar-with-active-state", "sidebar-dashboard"],
    usage='''const [query, setQuery] = useState("");

<SidebarContent>
  <SidebarSearch value={query} onValueChange={setQuery} />
  <SidebarNav sections={sections} query={query} emptyMessage="No pages match" />
</SidebarContent>''',
    props_doc=props_table(),
    composition_note="`SidebarSearch` + the data-driven `SidebarNav` with its `query` prop — filtering is a renderer concern, so hand-composed trees can reuse the exported `filterNavItems`-equivalent logic by switching to `SidebarNav` data.",
    behavior_doc="""Search behavior — all real, nothing decorative:

- **Filtering** — case-insensitive substring match on labels, applied live on every keystroke. Non-matching branches disappear; matching rows render in their normal position.
- **Parent preservation** — a matching child keeps its parent chain visible AND expanded (query results are useless if you cannot see where they live); a matching parent keeps its whole subtree.
- **Empty state** — a query with no matches renders a `role="status"` message naming the query, not a blank hole.
- **Reset** — the clear button (rendered while the query is non-empty) or Escape inside the field resets to the full tree; Escape does NOT close the drawer.
- **Structure preserved** — filtering never mutates the data or the expansion overrides; clearing restores the tree exactly as it was.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The field has a persistent accessible name (sr-only `<label>`), results are ordinary rows (no special result semantics needed — the tree itself is filtered), and the empty state is a polite status region. The clear button has an explicit accessible name.",
    responsive_doc="Search renders in the expanded column and the drawer; it hides in the collapsed rail (a 64px field is not a field). At 375px the field and results use the drawer's full 288px.",
    controlled_doc="""The query is ordinary controlled state in the demo:

```tsx
const [query, setQuery] = useState("");
<SidebarSearch value={query} onValueChange={setQuery} />
<SidebarNav sections={SECTIONS} query={query} />
```

`SidebarSearch` also works uncontrolled (`defaultValue` + `onValueChange`).""",
    notes_doc="Establishes the search pattern: renderer-level filtering, parent-preserving matches, status-message empty state, and non-destructive reset.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — search variant.
 *
 * A working navigation filter: labelled search field, live
 * case-insensitive filtering, parent-preserving matches, a role=status
 * empty state, and clear/Escape reset. The implementation core is
 * identical to the reference `sidebar` — this variant is the search
 * *pattern* (SidebarSearch + SidebarNav query).
 */""",
    showcase=SHOWCASE_HELPERS + r'''
const SEARCH_NAV = [
  {
    id: "platform",
    label: "Platform",
    items: [
      { id: "overview", label: "Overview", href: "#/overview", icon: <Icon name="grid" /> },
      {
        id: "projects", label: "Projects", icon: <Icon name="folder" />,
        children: [
          { id: "projects-active", label: "Active sprint", href: "#/projects/active" },
          { id: "projects-backlog", label: "Backlog", href: "#/projects/backlog" },
          { id: "projects-releases", label: "Releases", href: "#/projects/releases" },
        ],
      },
      { id: "analytics", label: "Analytics", href: "#/analytics", icon: <Icon name="bar-chart" /> },
      { id: "reports", label: "Reports", href: "#/reports", icon: <Icon name="file" /> },
      { id: "team", label: "Team", href: "#/team", icon: <Icon name="users" /> },
    ],
  },
  {
    id: "workspace",
    label: "Workspace",
    items: [
      { id: "docs", label: "Documentation", href: "#/docs", icon: <Icon name="book" /> },
      {
        id: "settings", label: "Settings", icon: <Icon name="settings" />,
        children: [
          { id: "settings-general", label: "General", href: "#/settings/general" },
          { id: "settings-members", label: "Members", href: "#/settings/members" },
          { id: "settings-billing", label: "Billing", href: "#/settings/billing" },
          { id: "settings-api", label: "API tokens", href: "#/settings/api" },
        ],
      },
      { id: "integrations", label: "Integrations", href: "#/integrations", icon: <Icon name="layers" /> },
    ],
  },
];
function SearchSidebar({ route, query, onQueryChange }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarSearch value={query} onValueChange={onQueryChange} placeholder="Filter navigation" />
        <SidebarNav sections={withActive(SEARCH_NAV, route)} query={query} />
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [query, setQuery] = React.useState("");
  return (
    <AppShell
      sidebar={<SearchSidebar route={route} query={query} onQueryChange={setQuery} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="A working navigation filter. Try “settings” (a parent keeps its subtree), “billing” (a child keeps its parent chain), or “zzz” (the empty state). Clear with the field button or Escape.">
        <p role="status" className="m-0 mt-6 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
          {query === "" ? "Full navigation shown." : "Filtering navigation by: " + query}
        </p>
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 11. sidebar-collapsible-groups
# ---------------------------------------------------------------------------

register(
    "sidebar-collapsible-groups",
    title="Sidebar with Collapsible Groups",
    subcategory="Structure",
    description="Independently collapsible navigation groups: the sidebar stays open while individual sections expand and collapse with aria-expanded, plus controlled expand-all / collapse-all coordination from outside the sidebar.",
    tags=TAGS_BASE + ["collapsible", "groups", "expand", "controlled"],
    features=FEAT_BASE + ["independent group state", "expand-all / collapse-all", "aria-expanded group controls"],
    accessibility=A11Y_BASE + ["independent aria-expanded per group"],
    interactive=True,
    related=["sidebar-with-groups", "sidebar-with-nested-navigation"],
    usage='''const [open, setOpen] = useState({ projects: true, components: false, admin: false });

<SidebarMenuCollapsible label="Projects" open={open.projects}
  onOpenChange={(o) => setOpen((m) => ({ ...m, projects: o }))}>
  <SidebarMenuSub>…</SidebarMenuSub>
</SidebarMenuCollapsible>

// Expand all / collapse all: setOpen({ projects: true, components: true, … })''',
    props_doc=props_table(),
    composition_note="Three controlled `SidebarMenuCollapsible` parents driven by one state map, with page-level Expand all / Collapse all buttons — the coordination pattern for workspaces with many optional sections.",
    behavior_doc="""Collapsible-group behavior:

- **Independent state** — each group expands and collapses on its own (`aria-expanded` + rotating chevron per group); the sidebar itself never closes.
- **External coordination** — the Expand all / Collapse all buttons drive the same controlled map from the page, proving the groups are honest controlled components, not self-locked widgets.
- **Active descendants survive** — collapsing a group that contains the current page only hides the rows visually; the current item keeps `aria-current` and the parent keeps its indication, and re-opening restores exactly the same tree.
- **Rail interaction** — in the collapsed rail, activating any group icon expands the sidebar with THAT group open (the others keep their state).""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="Every group control exposes its own `aria-expanded` + `aria-controls`; the group state is per-control, so screen-reader users get an honest per-section disclosure. External coordination changes the same attributes — no hidden state paths.",
    responsive_doc="Groups behave identically in the drawer and the column. At 375px the chevron-affording rows keep their full-width hit areas; collapsing unused sections is how small screens keep long navigations manageable.",
    controlled_doc="""This variant is the controlled-expansion reference — one state map, three controlled parents, external coordination:

```tsx
const [open, setOpen] = useState({ projects: true, components: false, admin: false });
const setAll = (v) => setOpen({ projects: v, components: v, admin: v });
```""",
    notes_doc="Demonstrates per-group controlled expansion with external coordination — the pattern for settings-heavy or section-heavy workspaces.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — collapsible groups variant.
 *
 * Independently collapsible navigation groups driven by one controlled
 * state map, with external expand-all / collapse-all coordination. The
 * sidebar itself stays open. The implementation core is identical to the
 * reference `sidebar` — this variant is the collapsible-groups *pattern*.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
function CollapsibleGroupsSidebar({ route, open, onGroupChange }) {
  return (
    <Sidebar label="Main">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton href="#/overview" active={route === "#/overview"} icon={<Icon name="grid" />}>Overview</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Projects" icon={<Icon name="folder" />} active={route.indexOf("#/projects") === 0} open={open.projects} onOpenChange={(o) => onGroupChange("projects", o)}>
                <SidebarMenuSub>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/active" active={route === "#/projects/active"}>Active sprint</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/backlog" active={route === "#/projects/backlog"}>Backlog</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/projects/releases" active={route === "#/projects/releases"}>Releases</SidebarMenuSubButton></SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Components" icon={<Icon name="layers" />} active={route.indexOf("#/components") === 0} open={open.components} onOpenChange={(o) => onGroupChange("components", o)}>
                <SidebarMenuSub>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/components/buttons" active={route === "#/components/buttons"}>Buttons</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/components/inputs" active={route === "#/components/inputs"}>Inputs</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/components/tables" active={route === "#/components/tables"}>Tables</SidebarMenuSubButton></SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <SidebarMenuCollapsible label="Admin" icon={<Icon name="settings" />} active={route.indexOf("#/admin") === 0} open={open.admin} onOpenChange={(o) => onGroupChange("admin", o)}>
                <SidebarMenuSub>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/admin/members" active={route === "#/admin/members"}>Members</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/admin/billing" active={route === "#/admin/billing"}>Billing</SidebarMenuSubButton></SidebarMenuSubItem>
                  <SidebarMenuSubItem><SidebarMenuSubButton href="#/admin/audit-log" active={route === "#/admin/audit-log"}>Audit log</SidebarMenuSubButton></SidebarMenuSubItem>
                </SidebarMenuSub>
              </SidebarMenuCollapsible>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <HelpFooter />
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [open, setOpen] = React.useState({ projects: true, components: false, admin: false });
  function onGroupChange(id, next) {
    setOpen((current) => ({ ...current, [id]: next }));
  }
  function setAll(next) {
    setOpen({ projects: next, components: next, admin: next });
  }
  return (
    <AppShell
      sidebar={<CollapsibleGroupsSidebar route={route} open={open} onGroupChange={onGroupChange} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="Independently collapsible groups driven by one controlled state map. Toggle each group in the sidebar, or coordinate them from here — the sidebar stays open throughout.">
        <div className="mt-6 flex flex-wrap items-center gap-2">
          <button type="button" className={DEMO_BUTTON} onClick={() => setAll(true)}>Expand all</button>
          <button type="button" className={DEMO_BUTTON} onClick={() => setAll(false)}>Collapse all</button>
          <p role="status" className="m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
            Open groups: <strong className="font-medium text-[var(--ds-color-foreground)]">{["projects", "components", "admin"].filter((id) => open[id]).join(", ") || "none"}</strong>
          </p>
        </div>
      </DemoPage>
    </AppShell>
  );
}''',
)

# ---------------------------------------------------------------------------
# 12. sidebar-dashboard
# ---------------------------------------------------------------------------

register(
    "sidebar-dashboard",
    title="Sidebar (Dashboard Composition)",
    subcategory="Composite",
    description="A realistic complete SaaS console navigation: grouped data-driven navigation with nested sections, badges, an active route, a user area with account actions, and the full responsive model — the composition to copy for real applications.",
    tags=TAGS_BASE + ["dashboard", "saas", "console", "composition"],
    features=FEAT_BASE + ["full console composition", "nested + badges + active", "user area", "data-driven"],
    accessibility=A11Y_BASE + ["one landmark, one current item"],
    interactive=True,
    related=["sidebar", "sidebar-with-user", "sidebar-with-badges", "sidebar-with-search"],
    usage='''<SidebarProvider>
  <div className="flex">
    <Sidebar label="Console">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarNav sections={withActive(CONSOLE_NAV, pathname)} />
      </SidebarContent>
      <SidebarFooter>
        <UserBlock />
        <SidebarMenu>
          <SidebarMenuItem><SidebarMenuButton href="/settings" icon={<SettingsIcon />}>Settings</SidebarMenuButton></SidebarMenuItem>
          <SidebarMenuItem><SidebarMenuButton onClick={signOut} icon={<LogoutIcon />}>Sign out</SidebarMenuButton></SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
    <main><SidebarTrigger />…</main>
  </div>
</SidebarProvider>''',
    props_doc=props_table(),
    composition_note="The full composition: brand header, data-driven navigation (groups + nesting + badges + active route), a footer user area with settings/help/sign-out, the edge rail, and the header trigger — every family feature in one realistic console.",
    behavior_doc="""The dashboard demonstrates the system under realistic load:

- **Navigation** — `Overview`, nested `Projects` (Active sprint / Backlog / Releases), `Analytics`, `Team` in the Platform group; `Documentation`, `Settings` in Workspace; an `Inbox` with a live count.
- **Active route** — hash-routed like a real app: one `aria-current` item, auto-expanding parent, parent indication.
- **Footer** — user identity block, Settings link, Help link, and a real Sign out action with status feedback.
- **Responsive model** — collapse to the icon rail with the trigger or edge rail; below 768px the whole console navigates through the drawer.

This is the composition to copy into a product, then prune: remove the rail if the product never collapses, drop the search if the navigation is short, keep the state model.""",
    keyboard_doc=KEYBOARD_BASE,
    a11y_doc="The full composition keeps the invariants under load: one labelled landmark per surface, exactly one `aria-current` item, honest links vs buttons, sr-only rail labels, and the drawer's dialog behavior on mobile.",
    responsive_doc="Exercised continuously in the demo: 375px (drawer), 768px (column at the breakpoint), 1280px (column + rail toggle). The console's header trigger is always the first control of the main content.",
    controlled_doc="The console uses uncontrolled provider state (the common case); every state slice is controllable — see `sidebar-collapsed` and `sidebar-mobile` for the controlled references.",
    notes_doc="The flagship composition — every feature in one realistic console navigation. Copy it, then prune to what the product needs.\n\n" + NOTES_BASE,
    tsx_header="""/**
 * DevSnips React Sidebar — dashboard composition variant.
 *
 * A realistic SaaS console navigation: data-driven groups + nesting +
 * badges + active route, a footer user area with account actions, and the
 * full responsive model (column / rail / drawer). The implementation core
 * is identical to the reference `sidebar` — this variant is the flagship
 * composition pattern.
 */""",
    showcase=SHOWCASE_HELPERS + r'''
const CONSOLE_NAV = [
  {
    id: "platform",
    label: "Platform",
    items: [
      { id: "overview", label: "Overview", href: "#/overview", icon: <Icon name="grid" /> },
      {
        id: "projects", label: "Projects", icon: <Icon name="folder" />,
        children: [
          { id: "projects-active", label: "Active sprint", href: "#/projects/active" },
          { id: "projects-backlog", label: "Backlog", href: "#/projects/backlog" },
          { id: "projects-releases", label: "Releases", href: "#/projects/releases" },
        ],
      },
      { id: "analytics", label: "Analytics", href: "#/analytics", icon: <Icon name="bar-chart" /> },
      { id: "team", label: "Team", href: "#/team", icon: <Icon name="users" /> },
      { id: "inbox", label: "Inbox", href: "#/inbox", icon: <Icon name="inbox" />, badge: 4 },
    ],
  },
  {
    id: "workspace",
    label: "Workspace",
    items: [
      { id: "docs", label: "Documentation", href: "#/docs", icon: <Icon name="book" /> },
      { id: "integrations", label: "Integrations", href: "#/integrations", icon: <Icon name="layers" />, badge: "Beta" },
      { id: "settings", label: "Settings", href: "#/settings", icon: <Icon name="settings" /> },
    ],
  },
];
function DashboardSidebar({ route, onSignOut }) {
  return (
    <Sidebar label="Console">
      <SidebarHeader><BrandLink /></SidebarHeader>
      <SidebarContent>
        <SidebarNav sections={withActive(CONSOLE_NAV, route)} />
      </SidebarContent>
      <SidebarFooter>
        <UserBlock />
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton href="#/settings" active={route === "#/settings"} icon={<Icon name="settings" />}>Settings</SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton href="#/help" active={route === "#/help"} icon={<Icon name="help-circle" />}>Help and support</SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={onSignOut} icon={<Icon name="logout" />}>Sign out</SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
function Showcase() {
  const route = useHashRoute();
  const [signedOutAt, setSignedOutAt] = React.useState(null);
  return (
    <AppShell
      sidebar={<DashboardSidebar route={route} onSignOut={() => setSignedOutAt(new Date().toLocaleTimeString())} />}
      title="Forge Console"
    >
      <DemoPage route={route} intro="A complete console navigation: grouped data-driven sections, nested Projects, an Inbox count, a Beta integration, the active route, and a footer user area. Collapse it to the rail, or resize below 768px to navigate from the drawer.">
        {signedOutAt ? (
          <div role="status" className="mt-6 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4">
            <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">Signed out at {signedOutAt}</p>
            <button type="button" className={DEMO_BUTTON_PRIMARY + " mt-3"} onClick={() => setSignedOutAt(null)}>Sign back in</button>
          </div>
        ) : null}
      </DemoPage>
    </AppShell>
  );
}''',
)
