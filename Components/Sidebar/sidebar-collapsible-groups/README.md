# Sidebar with Collapsible Groups

Independently collapsible navigation groups: the sidebar stays open while individual sections expand and collapse with aria-expanded, plus controlled expand-all / collapse-all coordination from outside the sidebar.

## Installation

Copy `code.tsx` (TypeScript) or `code.jsx` (plain JavaScript) into your project — it is a single self-contained module with no dependencies beyond React. Make sure your app loads Tailwind CSS and the DevSnips `--ds-*` design tokens (see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md)); the component consumes the tokens through Tailwind arbitrary values such as `bg-[var(--ds-color-surface)]`. No component-specific CSS file is required.

## Usage

```tsx
const [open, setOpen] = useState({ projects: true, components: false, admin: false });

<SidebarMenuCollapsible label="Projects" open={open.projects}
  onOpenChange={(o) => setOpen((m) => ({ ...m, projects: o }))}>
  <SidebarMenuSub>…</SidebarMenuSub>
</SidebarMenuCollapsible>

// Expand all / collapse all: setOpen({ projects: true, components: true, … })
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
const [open, setOpen] = useState({ projects: true, components: false, admin: false });

<SidebarMenuCollapsible label="Projects" open={open.projects}
  onOpenChange={(o) => setOpen((m) => ({ ...m, projects: o }))}>
  <SidebarMenuSub>…</SidebarMenuSub>
</SidebarMenuCollapsible>

// Expand all / collapse all: setOpen({ projects: true, components: true, … })
```

## Props

### `<SidebarProvider>`

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

Renders no DOM of its own — it is the state root + `matchMedia` owner.

### `<Sidebar>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | `"Sidebar"` | Accessible name of the `<nav>` landmark and the mobile dialog. |
| `className` | `string` | — | Extra classes on the desktop `<aside>` and the drawer panel. |
| `children` | `ReactNode` | — | `SidebarHeader` / `SidebarContent` / `SidebarFooter` / `SidebarRail`. |

Renders the children twice: once in the persistent desktop `<aside>` (hidden below the breakpoint) and once in the mobile drawer (mounted only while open, hidden at and above the breakpoint).

### `<SidebarHeader>` / `<SidebarContent>` / `<SidebarFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the region. |
| `children` | `ReactNode` | — | Region content. |

`SidebarHeader` is the 56px brand row (centers content in the collapsed rail). `SidebarContent` is the scrollable navigation region. `SidebarFooter` is pinned to the bottom with a separating top border. All three forward native `<div>` attributes.

### `<SidebarGroup>` / `<SidebarGroupLabel>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes. |
| `children` | `ReactNode` | — | Group content / label text. |

`SidebarGroup` wraps one section (label + menu). `SidebarGroupLabel` renders the uppercase eyebrow; in the collapsed rail it becomes sr-only so the section structure stays in the accessibility tree.

### `<SidebarMenu>` / `<SidebarMenuItem>`

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

In the mobile drawer, activating a link row also closes the drawer.

### `<SidebarMenuCollapsible>`

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

The trigger is a real `<button>` with `aria-expanded` + `aria-controls` pointing at the nested list and a rotating chevron. In the collapsed rail, activating it expands the sidebar and opens the group in one step.

### `<SidebarMenuSub>` / `<SidebarMenuSubItem>` / `<SidebarMenuSubButton>`

`SidebarMenuSub` is the border-guided nested `<ul>` (it carries the id its collapsible's `aria-controls` points at, and renders nothing in the collapsed rail). `SidebarMenuSubItem` is the `<li>`. `SidebarMenuSubButton` is the 13px nested row — a real `<a>` when `href` is passed, a real `<button>` otherwise, a non-interactive `aria-disabled` span when `disabled`; `active` adds `aria-current="page"` + the active treatment.

### `<SidebarTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes. |

A real 36px `<button type="button" aria-label="Toggle sidebar">` for the page header. Below the breakpoint it opens/closes the drawer; at and above it toggles the collapsed rail. `aria-expanded` + `aria-controls` follow the active mode. Render at most one per provider (it is the focus-restoration target). Native button attributes are forwarded.

### `<SidebarRail>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes. |

A thin edge hit area on the desktop sidebar border that toggles collapse (`aria-expanded` + `aria-controls`). Desktop only — renders nothing inside the mobile drawer.

### `<SidebarSearch>`

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

A real `<input type="search">` with a leading search icon and a clear button (rendered while the query is non-empty). Escape clears the query without closing the drawer. Hidden in the collapsed rail — filtering needs a keyboard.

### `<SidebarNav>`

| Name | Type | Default | Description |
|---|---|---|---|
| `sections` | `SidebarNavSection[]` | — (required) | The navigation data (see *Navigation Data*). |
| `query` | `string` | `""` | Filter query — case-insensitive label match. |
| `emptyMessage` | `string` | `"No navigation items match …"` | `role="status"` message when nothing matches. |
| `className` | `string` | — | Extra classes on the sections wrapper. |

Parents with an active descendant auto-expand; manual toggles are remembered per item `id`. While a query is active, matching parents keep their subtree and parents of matching children stay visible and expanded.

### `useSidebar()`

Returns the provider context (`collapsed`, `mobileOpen`, `isDesktop`, `requestCollapsed`, `requestMobileOpen`, `closeMobile`, `breakpoint`, landmark ids) for custom shell content — for example a brand wordmark or user card that adapts to the collapsed rail. Throws when used outside `<SidebarProvider>`.

## Compound Components

Sidebar is a compound component. Nineteen exports compose the pattern:

```tsx
<SidebarProvider>
  <Sidebar label="Main">
    <SidebarHeader>
      <a href="/" className="brand">Acme</a>
    </SidebarHeader>
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
                <SidebarMenuSubItem><SidebarMenuSubButton href="/projects/active">Active sprint</SidebarMenuSubButton></SidebarMenuSubItem>
              </SidebarMenuSub>
            </SidebarMenuCollapsible>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter>
      <SidebarMenuButton onClick={signOut}>Sign out</SidebarMenuButton>
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
  <main>
    <SidebarTrigger />
    …page content…
  </main>
</SidebarProvider>
```

- `SidebarProvider` — the state root (renders no DOM of its own). Owns the desktop `collapsed` state (controlled via `collapsed` + `onCollapsedChange`, or uncontrolled via `defaultCollapsed`), the mobile drawer state (`mobileOpen` + `onMobileOpenChange`, or `defaultMobileOpen`), and the responsive `breakpoint` (`sm` / `md` / `lg`, default `md`). Also owns the single `matchMedia` listener, drawer Escape handling, scroll-lock bookkeeping, and focus restoration.
- `Sidebar` — renders the navigation surface TWICE from the same children: a persistent desktop `<aside>` landmark (visible at and above the breakpoint; `w-64` expanded, `w-16` collapsed) and a mobile modal drawer (`role="dialog" aria-modal="true"`, overlay, focus trap, close button) rendered only while open below the breakpoint. Only one is exposed at a time.
- `SidebarHeader` — the 56px header region (brand, workspace switcher); centers its content in the collapsed rail.
- `SidebarContent` — the scrollable navigation region (`overflow-y-auto`).
- `SidebarFooter` — the bottom-pinned region separated by a top border (user area, settings/help/logout actions).
- `SidebarGroup` — one navigation section; `SidebarGroupLabel` — its uppercase eyebrow label (kept in the accessibility tree as sr-only when collapsed).
- `SidebarMenu` / `SidebarMenuItem` — the `<ul>` / `<li>` list structure for navigation rows.
- `SidebarMenuButton` — the primary row control: a real `<a href>` when `href` is passed, a real `<button type="button">` otherwise, and a non-interactive `aria-disabled` span when `disabled`. Supports `active` (`aria-current="page"` + surface treatment + inset indicator bar), `icon`, `badge`, and `tooltip` (collapsed-rail label).
- `SidebarMenuCollapsible` — an expandable parent row (`aria-expanded` + `aria-controls`, rotating chevron, `active` descendant indication). Controlled (`open` + `onOpenChange`) or uncontrolled (`defaultOpen`). In the collapsed rail, activating it expands the sidebar and opens the group.
- `SidebarMenuSub` / `SidebarMenuSubItem` / `SidebarMenuSubButton` — the nested level: a border-guided `<ul>` with smaller rows (13px), same active/disabled semantics as top-level rows.
- `SidebarTrigger` — the 36px mode control for page headers: opens/closes the drawer below the breakpoint, toggles collapse at/above it (`aria-expanded` + `aria-controls` reflect the active mode).
- `SidebarRail` — a thin edge hit area on the desktop sidebar border that toggles collapse (desktop only; renders nothing in the drawer).
- `SidebarSearch` — a labelled `type="search"` field with a clear button; Escape clears the query without closing the drawer. Hidden in the collapsed rail.
- `SidebarNav` — the typed data-driven renderer (see *Navigation Data*): renders sections/groups/collapsibles from `SidebarNavSection[]`, auto-expands parents with an active descendant, and filters by `query` with a status-message empty state.
- `useSidebar()` — the context escape hatch for custom content (e.g. adapting a brand wordmark or user card to the collapsed state).

Three controlled `SidebarMenuCollapsible` parents driven by one state map, with page-level Expand all / Collapse all buttons — the coordination pattern for workspaces with many optional sections.

## Navigation Data

`SidebarNav` renders navigation from typed data instead of hand composition:

```tsx
export interface SidebarNavItem {
  id: string;                  // stable id (expansion bookkeeping)
  label: string;               // visible + accessible label
  href?: string;               // navigation target
  icon?: ReactNode;            // leading icon (aria-hidden)
  badge?: ReactNode;           // trailing count/status badge
  disabled?: boolean;          // non-interactive aria-disabled row
  active?: boolean;            // current page (aria-current="page")
  children?: SidebarNavItem[]; // nested level (up to three levels render)
}

export interface SidebarNavSection {
  id: string;
  label?: string;              // group eyebrow label
  items: SidebarNavItem[];
}

<SidebarContent>
  <SidebarNav sections={SECTIONS} query={query} emptyMessage="Nothing found" />
</SidebarContent>
```

Rendering rules:

- Items with `children` render as `SidebarMenuCollapsible` parents; leaf items render as `SidebarMenuButton` links/actions. Nested children render as `SidebarMenuSubButton` rows (three levels of indentation maximum — deeper trees belong in a different navigation pattern).
- A parent with an active descendant opens automatically and shows the parent-indication treatment; manual toggles are remembered per session (`overrides` map keyed by item `id`).
- `query` filters case-insensitively by label. A matching child keeps its parent chain visible (and expanded); a matching parent keeps its whole subtree. When nothing matches, a `role="status"` empty message renders instead of the tree.

The data model is framework-neutral: `href` values are plain URLs. In a routed app, derive `active` from the current route when building the sections.

## Responsive Behavior

The family switches modes by breakpoint, driven by one `matchMedia` listener in the provider plus Tailwind responsive utilities — no resize handlers per component:

- **At and above the breakpoint** (`md` = 768px by default): the persistent `<aside>` renders as a 256px navigation column; `SidebarTrigger` / `SidebarRail` toggle it to a 64px icon rail (labels become sr-only, badges become dots, rows expose measured tooltips, `SidebarSearch` hides, group labels stay in the accessibility tree).
- **Below the breakpoint**: the desktop landmark is `display: none` and the sidebar becomes a modal drawer (`w-72`, capped at `100vw - 3rem`) with an overlay, scroll lock, focus trap, Escape / outside-pointer close, and focus restoration. A resize to desktop while the drawer is open closes it cleanly.
- Activating any navigation link inside the drawer closes it (navigation proceeds).
- Long labels truncate with `min-w-0` + `truncate` instead of forcing overflow; the rail keeps a fixed 64px width so it never overflows the layout.

Groups behave identically in the drawer and the column. At 375px the chevron-affording rows keep their full-width hit areas; collapsing unused sections is how small screens keep long navigations manageable.

## Accessibility

The structure follows the WAI-ARIA disclosure navigation pattern, plus the modal-dialog pattern for the mobile drawer.

- The desktop sidebar is a real `<aside>` containing a `<nav aria-label>` landmark; the mobile drawer is `role="dialog" aria-modal="true"` with the same labelled `<nav>` inside. Only one is exposed at a time (the desktop landmark is `display: none` below the breakpoint; the drawer is only mounted while open).
- Navigation rows are real `<a href>` elements (normal browser navigation, middle-click, screen-reader link semantics); toggles and actions are real `<button type="button">` elements. No `div` click handlers, no nested interactive elements.
- Disabled rows render as non-interactive spans with `aria-disabled="true"` — never dead anchors or focusable-but-inert controls.
- Collapsed-rail rows keep their full label in the accessibility tree (sr-only text) and expose a measured, fixed-position tooltip on hover/focus — the tooltip never takes pointer events and is hidden from assistive technology because the sr-only label already names the control.
- The mobile drawer moves focus to its first navigation control on open, traps Tab/Shift+Tab at its boundaries, closes on Escape and outside pointer down, locks body scroll with scrollbar-width compensation, and returns focus to the `SidebarTrigger` on close. A built-in close button ("Close navigation") is the last tab stop.
- Group labels remain available to screen readers when the rail is collapsed (sr-only), and collapsible parents expose `aria-expanded` + `aria-controls` pointing at the nested list.
- Every interactive element has a visible `focus-visible` ring via the `--ds-color-focus-ring` token, and all transitions are disabled under `prefers-reduced-motion`.

Every group control exposes its own `aria-expanded` + `aria-controls`; the group state is per-control, so screen-reader users get an honest per-section disclosure. External coordination changes the same attributes — no hidden state paths.

## Keyboard Interaction

- **Tab / Shift+Tab** move through the navigation rows, collapsible parents, the search field, and the trigger in DOM order — links behave like links, buttons like buttons (no roving tabindex: navigation lists are a series of ordinary tab stops per the disclosure-navigation pattern).
- **Enter** activates links and buttons; **Space** activates buttons (native behavior — no custom key handlers).
- Collapsible parents are real buttons: Enter/Space toggles `aria-expanded`, and the nested links are ordinary tab stops while the parent is open.
- In the mobile drawer, Tab/Shift+Tab wrap at the drawer boundaries (modal behavior), **Escape** closes the drawer and returns focus to the `SidebarTrigger`, and the built-in "Close navigation" button is the last tab stop.
- In `SidebarSearch`, Escape clears the current query without closing the drawer; the clear control is a real button.
- Activating a collapsed `SidebarMenuCollapsible` icon expands the sidebar and opens its group in one step, so rail users never reach a dead end.
- The `SidebarRail` is a real button (`aria-expanded`) reachable in the tab order directly after the sidebar content.

## Active Navigation

Pass `active` to the `SidebarMenuButton` / `SidebarMenuSubButton` that represents the current page (or set `active: true` in the `SidebarNavItem` data). The current item renders with the active surface, foreground text, medium weight, AND a 2px inset indicator bar — never color alone — and exposes `aria-current="page"` to assistive technology. In a routed app, derive `active` from the current route:

```tsx
<SidebarMenuButton href="/analytics" active={pathname.startsWith("/analytics")}>Analytics</SidebarMenuButton>
```

Exactly one item in the navigation should be current at a time. A collapsible parent with an active descendant receives the parent-indication treatment (medium-weight foreground text, no surface fill) via its own `active` prop — `aria-current` stays on the actual page link.

Collapsible-group behavior:

- **Independent state** — each group expands and collapses on its own (`aria-expanded` + rotating chevron per group); the sidebar itself never closes.
- **External coordination** — the Expand all / Collapse all buttons drive the same controlled map from the page, proving the groups are honest controlled components, not self-locked widgets.
- **Active descendants survive** — collapsing a group that contains the current page only hides the rows visually; the current item keeps `aria-current` and the parent keeps its indication, and re-opening restores exactly the same tree.
- **Rail interaction** — in the collapsed rail, activating any group icon expands the sidebar with THAT group open (the others keep their state).

## Controlled and Uncontrolled State

Both state slices support controlled and uncontrolled usage:

- **Collapsed (desktop)** — uncontrolled via `defaultCollapsed`, or controlled via `collapsed` + `onCollapsedChange`. Every internal toggle point (`SidebarTrigger`, `SidebarRail`, a collapsed `SidebarMenuCollapsible` activation) flows through `onCollapsedChange`.
- **Mobile drawer** — uncontrolled via `defaultMobileOpen`, or controlled via `mobileOpen` + `onMobileOpenChange`. Trigger clicks, Escape, overlay pointer downs, drawer close-button clicks, and in-drawer navigation all flow through `onMobileOpenChange`.

```tsx
const [collapsed, setCollapsed] = useState(false);
const [mobileOpen, setMobileOpen] = useState(false);
<SidebarProvider collapsed={collapsed} onCollapsedChange={setCollapsed}
                 mobileOpen={mobileOpen} onMobileOpenChange={setMobileOpen}>
  …
</SidebarProvider>
```

`SidebarMenuCollapsible` manages its own expansion (uncontrolled `defaultOpen` or controlled `open` + `onOpenChange`); `SidebarNav` keeps a per-item override map on top of the active-descendant default. The collapsed state is intentionally NOT persisted — persistence belongs to the application shell (store the controlled value in `localStorage` or a cookie if you need it).

This variant is the controlled-expansion reference — one state map, three controlled parents, external coordination:

```tsx
const [open, setOpen] = useState({ projects: true, components: false, admin: false });
const setAll = (v) => setOpen({ projects: v, components: v, admin: v });
```

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This sidebar variant uses the semantic color, radius, shadow, typography, and motion tokens, and follows the navigation rules (sidebar width 240–280px, clear active state, quiet state changes, mobile navigation as an accessible drawer).

## Notes and Limitations

Demonstrates per-group controlled expansion with external coordination — the pattern for settings-heavy or section-heavy workspaces.

- Geometry is fixed by the shared class constants: 256px expanded, 64px collapsed rail, 288px drawer capped at `100vw - 3rem`, 56px header row. Override via `className` on `<Sidebar>` when a product genuinely needs different geometry.
- The collapsed state is intentionally not persisted — persist the controlled value in your application shell (`localStorage`, a cookie) if the product needs it.
- `SidebarNav` renders up to three indentation levels; deeper hierarchies belong in a different pattern (a tree view or a docs sidebar).
- The previews use hash routing (`#/overview`, `#/projects/backlog`, …) so navigation is demonstrable without a router; `href` values are plain URLs and any router can supply `active`.
- Render at most one `SidebarTrigger` per provider — it is the focus-restoration target for the drawer.
