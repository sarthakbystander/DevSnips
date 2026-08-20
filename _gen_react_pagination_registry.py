"""Registry for the DevSnips React Pagination generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs.
The generator (``_gen_react_pagination.py``) reads each component's
``code.tsx`` from disk and combines it with the spec here to write
``code.jsx``, ``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented demo content only (component libraries, guide
chapters, user directories, files, orders, case studies, customers, activity
logs). No lorem ipsum, no marketing buzzwords.
"""
from _gen_react_pagination import (
    register,
    LOGIC_BASE,
    STATES,
    RESPONSIVE_BASE,
)

TAGS_BASE = ["pagination", "navigation", "react", "tailwind", "accessible", "responsive", "pages"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic nav landmark", 'aria-current="page"', "keyboard accessible"]
A11Y_BASE = ["nav landmark with aria-label", 'aria-current="page"', "accessible control labels", "aria-disabled disabled states", "focus-visible", "native anchors or buttons"]

# Shared props tables. The seven core primitives carry the same API family-wide.
PAGINATION_PROPS = r"""### `<Pagination>`

| Name | Type | Default | Description |
|---|---|---|---|
| `page` | `number` | — | Current page, 1-based (controlled). |
| `defaultPage` | `number` | `1` | Initial page, 1-based (uncontrolled). |
| `totalPages` | `number` (required) | — | Total number of pages. |
| `onPageChange` | `(page: number) => void` | — | Called with the next 1-based page. |
| `buildHref` | `(page: number) => string` | — | Builds a URL per page; controls render as real anchors. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Control density (32px / 36px / 44px). |
| `disabled` | `boolean` | `false` | Disable every control in the navigation. |
| `label` | `string` | `"Pagination"` | Accessible label for the `<nav>` landmark. |
| `className` | `string` | — | Extra classes on the `<nav>`. |
| `children` | `ReactNode` | — | `PaginationContent` composition. |"""

CONTENT_PROPS = r"""### `<PaginationContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<ul>`. |
| `children` | `ReactNode` | — | `PaginationItem` elements. |"""

ITEM_PROPS = r"""### `<PaginationItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<li>`. |
| `children` | `ReactNode` | — | Usually one page control or an ellipsis. |"""

LINK_PROPS = r"""### `<PaginationLink>`

| Name | Type | Default | Description |
|---|---|---|---|
| `page` | `number` (required) | — | 1-based page number this control navigates to. |
| `href` | `string` | — | Explicit URL (overrides `buildHref`); renders a real anchor. |
| `disabled` | `boolean` | `false` | Disable this page control (non-interactive span). |
| `aria-label` | `string` | `"Go to page N"` / `"Page N"` | Accessible name override. |
| `className` | `string` | — | Extra classes on the control. |
| `children` | `ReactNode` | the page number | Visible content. |"""

STEP_PROPS = r"""### `<PaginationPrevious>` / `<PaginationNext>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | — | Explicit URL for the target page (overrides `buildHref`). |
| `label` | `string` | `"Previous"` / `"Next"` | Visible label (also the accessible name). |
| `className` | `string` | — | Extra classes on the control. |

Previous disables automatically on the first page; Next on the last page."""

ELLIPSIS_PROPS = r"""### `<PaginationEllipsis>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the marker. |

Informational only: an `aria-hidden` "…" glyph plus a screen-reader-only "More pages" text. Never a button."""


def props_table(*extra):
    parts = [PAGINATION_PROPS, CONTENT_PROPS, ITEM_PROPS, LINK_PROPS, STEP_PROPS, ELLIPSIS_PROPS]
    parts.extend(extra)
    return "\n\n".join(parts)


# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = """function useDemoHash() {
  const [hash, setHash] = React.useState(() => window.location.hash);
  React.useEffect(() => {
    const onChange = () => setHash(window.location.hash);
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  return hash;
}
const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const LIST = "m-0 list-none divide-y divide-[var(--ds-color-border)] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-0";
const ROW = "flex items-center justify-between gap-4 px-4 py-2.5";
const ROW_NAME = "text-sm font-medium text-[var(--ds-color-foreground)]";
const ROW_META = "shrink-0 text-xs tabular-nums text-[var(--ds-color-muted-foreground)]";
"""

# 1. pagination (reference)
register(
    "pagination",
    title="Pagination",
    subcategory="Core",
    description="Accessible page navigation as a compound component: semantic nav landmark, numbered page controls, previous/next steppers, and an aria-current current page.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=True,
    related=["pagination-with-numbers", "pagination-with-previous-next", "pagination-with-ellipsis", "pagination-disabled"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "./pagination";

const [page, setPage] = useState(1);

<Pagination page={page} totalPages={5} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationItem><PaginationLink page={1} /></PaginationItem>
    <PaginationItem><PaginationLink page={2} /></PaginationItem>
    <PaginationItem><PaginationLink page={3} /></PaginationItem>
    <PaginationItem><PaginationLink page={4} /></PaginationItem>
    <PaginationItem><PaginationLink page={5} /></PaginationItem>
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>

// Uncontrolled:
<Pagination defaultPage={1} totalPages={5}>…</Pagination>

// URL-based pagination (controls render as real anchors):
<Pagination page={page} totalPages={5} buildHref={(p) => `/components?page=${p}`}>…</Pagination>''',
    props_doc=props_table(),
    composition_note="This is the reference composition — every other variant in the family uses the same primitives and extends the same class constants, states, and accessibility model.",
    logic_doc=LOGIC_BASE,
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Give the `<nav>` a more specific `label` (for example `label=\"Orders pagination\"`) when more than one pagination control lives on a page. The current page is distinguished by border, surface, and `aria-current` together — never by color alone.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Reference implementation for the Pagination family. It establishes the shared control geometry (36px `md` height, `radius-sm`, `tabular-nums`), the idle/active/disabled color model, the chevron-plus-text steppers, the `focus-visible` ring, and the wrap-not-scroll responsive behavior that every other variant extends.",
    showcase=DEMO_HELPERS + '''
const COMPONENTS_DATA = [
  ["Accordion", "Disclosure"], ["Alert", "Feedback"], ["Avatar", "Data display"], ["Badge", "Data display"],
  ["Breadcrumbs", "Navigation"], ["Button", "Actions"], ["Button Group", "Actions"], ["Calendar", "Forms"],
  ["Card", "Layout"], ["Carousel", "Data display"], ["Chart", "Data display"], ["Checkbox", "Forms"],
  ["Combobox", "Forms"], ["Command Palette", "Navigation"], ["Context Menu", "Overlay"], ["Data Table", "Data display"],
  ["Date Picker", "Forms"], ["Dialog", "Overlay"], ["Drawer", "Overlay"], ["Dropdown", "Overlay"],
  ["File Upload", "Forms"], ["Form", "Forms"], ["Input", "Forms"], ["List", "Data display"],
  ["Menu", "Navigation"], ["Meter", "Data display"], ["Modal", "Overlay"], ["Navbar", "Navigation"],
  ["Pagination", "Navigation"], ["Popover", "Overlay"], ["Progress", "Feedback"], ["Radio", "Forms"],
  ["Search", "Forms"], ["Segmented Control", "Forms"], ["Select", "Forms"], ["Sidebar", "Navigation"],
  ["Skeleton", "Feedback"], ["Slider", "Forms"], ["Stepper", "Navigation"], ["Switch", "Forms"],
];
const PAGE_SIZE = 8;
function ComponentLibrary() {
  const [page, setPage] = React.useState(1);
  const totalPages = Math.ceil(COMPONENTS_DATA.length / PAGE_SIZE);
  const start = (page - 1) * PAGE_SIZE;
  const visible = COMPONENTS_DATA.slice(start, start + PAGE_SIZE);
  return (
    <div className="space-y-3">
      <ul className={LIST}>
        {visible.map(([name, family]) => (
          <li key={name} className={ROW}>
            <span className={ROW_NAME}>{name}</span>
            <span className={ROW_META}>{family}</span>
          </li>
        ))}
      </ul>
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-3">
        <p className={NOTE}>Showing {start + 1}–{start + visible.length} of {COMPONENTS_DATA.length} components</p>
        <Pagination page={page} totalPages={totalPages} onPageChange={setPage}>
          <PaginationContent>
            <PaginationItem><PaginationPrevious /></PaginationItem>
            {Array.from({ length: totalPages }, (_, i) => (
              <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
            ))}
            <PaginationItem><PaginationNext /></PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
function UrlPagination() {
  const hash = useDemoHash();
  const match = hash.match(/page\\/(\\d+)/);
  const page = match ? Math.min(Math.max(1, parseInt(match[1], 10)), 5) : 1;
  return (
    <div className="space-y-3">
      <p className={NOTE}>Controls are real anchors — the URL drives the current page. Current URL: <code>{hash || "#/"}</code></p>
      <Pagination page={page} totalPages={5} buildHref={(p) => `#/components/page/${p}`}>
        <PaginationContent>
          <PaginationItem><PaginationPrevious /></PaginationItem>
          {Array.from({ length: 5 }, (_, i) => (
            <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
          ))}
          <PaginationItem><PaginationNext /></PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Component library — state-driven</p>
        <ComponentLibrary />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>URL-based pagination</p>
        <UrlPagination />
      </div>
    </div>
  );
}''',
)

# 2. pagination-with-previous-next
STATUS_PROPS = r"""### `<PaginationStatus>`

| Name | Type | Default | Description |
|---|---|---|---|
| `format` | `(page: number, totalPages: number) => string` | `"Page X of Y"` | Formats the status text. |
| `className` | `string` | — | Extra classes on the span. |

Rendered in an `aria-live="polite"` region so page changes are announced without moving focus."""

register(
    "pagination-with-previous-next",
    title="Pagination with Previous/Next",
    subcategory="Navigation",
    description="Previous/next-only page navigation for readers, wizards, and detail views where numbered pages add no value, with a live Page X of Y status.",
    tags=TAGS_BASE + ["previous", "next", "stepper"],
    features=FEAT_BASE + ["boundary-aware steppers", "aria-live page status"],
    accessibility=A11Y_BASE + ["aria-live status text"],
    interactive=True,
    related=["pagination", "pagination-with-numbers", "pagination-disabled"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationPrevious,
  PaginationNext,
  PaginationStatus,
} from "./pagination-with-previous-next";

const [page, setPage] = useState(1);

<Pagination page={page} totalPages={12} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationItem><PaginationStatus /></PaginationItem>
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>''',
    props_doc=props_table(STATUS_PROPS),
    composition_note="This variant adds `PaginationStatus`, a plain-text \"Page X of Y\" readout. Place it between the steppers so the current position is visible and announced even without numbered pages.",
    logic_doc=LOGIC_BASE + """

Previous/next-only navigation leans entirely on the boundary logic: Previous renders as a non-interactive `aria-disabled` span while `page === 1`, and Next while `page === totalPages`. The steppers always move exactly one page; there is no way to jump past the ends.""",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Because there are no numbered links, the `PaginationStatus` readout is the position indicator: it updates in an `aria-live=\"polite\"` region on every page change. The steppers keep visible text labels, so the controls never rely on icons alone.",
    responsive_doc="""With only two steppers and a status text, this treatment fits narrow screens without wrapping tricks. The list still uses `flex-wrap`, so a long custom `label` wraps cleanly instead of overflowing.""",
    notes_doc="Use for linear content: documentation chapters, checkout steps, invoice or ticket detail views. If the user needs to jump to a specific page, use the numbered or ellipsis variants instead.",
    showcase=DEMO_HELPERS + '''
const CHAPTERS = [
  ["Getting started", "Install nothing: copy a component folder into your project and define the design tokens once."],
  ["Design tokens", "Every component consumes the shared --ds-* semantic tokens for color, radius, typography, and motion."],
  ["Buttons", "Thirty button patterns, from solid primaries to split buttons and command shortcuts."],
  ["Inputs", "Text fields with labels, helper text, validation, and leading icons."],
  ["Selects", "Native and custom select patterns with full keyboard support."],
  ["Checkboxes", "Single checkboxes, groups, cards, and select-all with real indeterminate state."],
  ["Radios", "Radio groups with fieldset semantics and native arrow-key navigation."],
  ["Switches", "Settings toggles built on native checkbox inputs with role=switch."],
  ["Textareas", "Multi-line input with counters, auto-resize, and action bars."],
  ["Tabs", "Compound tabs with roving tabindex and panels that stay mounted."],
  ["Breadcrumbs", "Trail navigation with real links, separators, and collapsed levels."],
  ["Pagination", "Page navigation with numbered links, ellipsis ranges, and page-size controls."],
];
function GuideReader() {
  const [page, setPage] = React.useState(1);
  const chapter = CHAPTERS[page - 1];
  return (
    <div className="space-y-3">
      <article className="space-y-2 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-5">
        <p className={LABEL}>React Components Guide · Chapter {page}</p>
        <h3 className="m-0 text-base font-semibold text-[var(--ds-color-foreground)]">{chapter[0]}</h3>
        <p className="m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{chapter[1]}</p>
      </article>
      <div className="flex justify-center">
        <Pagination page={page} totalPages={CHAPTERS.length} onPageChange={setPage} label="Guide chapters">
          <PaginationContent>
            <PaginationItem><PaginationPrevious /></PaginationItem>
            <PaginationItem><PaginationStatus /></PaginationItem>
            <PaginationItem><PaginationNext /></PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Documentation reader — linear navigation</p>
        <GuideReader />
      </div>
    </div>
  );
}''',
)

# 3. pagination-with-numbers
register(
    "pagination-with-numbers",
    title="Pagination with Numbers",
    subcategory="Navigation",
    description="Explicit numbered page navigation for small, known page counts: one aria-labeled control per page with aria-current on the active page.",
    tags=TAGS_BASE + ["numbers", "page-numbers"],
    features=FEAT_BASE + ["one control per page"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["pagination", "pagination-with-ellipsis", "pagination-compact"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
} from "./pagination-with-numbers";

const [page, setPage] = useState(1);
const totalPages = 6;

<Pagination page={page} totalPages={totalPages} onPageChange={setPage}>
  <PaginationContent>
    {Array.from({ length: totalPages }, (_, i) => (
      <PaginationItem key={i + 1}>
        <PaginationLink page={i + 1} />
      </PaginationItem>
    ))}
  </PaginationContent>
</Pagination>''',
    props_doc=props_table(),
    composition_note="This variant composes only numbered `PaginationLink` controls — no steppers. Map one `PaginationLink` per page; each renders its page number as the default `children` and computes its own accessible name.",
    logic_doc=LOGIC_BASE + """

Numbered pagination renders every page explicitly, so it is intended for small page counts (roughly up to 8). Mapping `Array.from({ length: totalPages })` guarantees the controls and the `totalPages` prop never disagree. For larger datasets, switch to the ellipsis variant, which windows the range instead of rendering hundreds of buttons.""",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Every numbered control has an explicit accessible name: \"Go to page N\" for inactive pages and \"Page N\" with `aria-current=\"page\"` for the active one — assistive technology never hears a bare \"3\".",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Use for short, stable lists: a handful of search result pages, a small catalog, an admin list. Above ~8 pages the row gets crowded on mobile — move to `pagination-with-ellipsis`.",
    showcase=DEMO_HELPERS + '''
const FIRST = ["Aaron", "Beatriz", "Chen", "Dalia", "Elias", "Farah", "Gabriel", "Hana", "Ivan", "Julia", "Kenji", "Lara"];
const LAST = ["Alvarez", "Berg", "Costa", "Diallo"];
const ROLES = ["Engineer", "Designer", "Product manager", "Analyst"];
const USERS = FIRST.flatMap((first) => LAST.map((last) => ({ name: first + " " + last })));
const PAGE_SIZE = 8;
function UserDirectory() {
  const [page, setPage] = React.useState(1);
  const totalPages = Math.ceil(USERS.length / PAGE_SIZE);
  const start = (page - 1) * PAGE_SIZE;
  const visible = USERS.slice(start, start + PAGE_SIZE);
  return (
    <div className="space-y-3">
      <ul className={LIST}>
        {visible.map((user, index) => (
          <li key={user.name} className={ROW}>
            <span className={ROW_NAME}>{user.name}</span>
            <span className={ROW_META}>{ROLES[(start + index) % ROLES.length]}</span>
          </li>
        ))}
      </ul>
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-3">
        <p className={NOTE}>Page {page} of {totalPages} · {USERS.length} users</p>
        <Pagination page={page} totalPages={totalPages} onPageChange={setPage} label="Users pagination">
          <PaginationContent>
            {Array.from({ length: totalPages }, (_, i) => (
              <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
            ))}
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>User directory — six explicit pages</p>
        <UserDirectory />
      </div>
    </div>
  );
}''',
)

# 4. pagination-with-ellipsis
RANGE_PROPS = r"""### `getPaginationRange(currentPage, totalPages, siblingCount?)`

Returns an array of 1-based page numbers and `"ellipsis"` markers. Always includes the first page, the last page, and `siblingCount` pages on each side of the current page; hidden ranges collapse to a single marker. When every page fits (`totalPages <= 2 * siblingCount + 5`) all pages are returned — no marker is produced.

### `<PaginationPages>`

| Name | Type | Default | Description |
|---|---|---|---|
| `siblingCount` | `number` | `1` | Pages shown on each side of the current page. |

Renders the computed range as `<PaginationItem>` children of `<PaginationContent>`: numbered `PaginationLink` controls plus `PaginationEllipsis` markers."""

register(
    "pagination-with-ellipsis",
    title="Pagination with Ellipsis",
    subcategory="Layout",
    description="Windowed page navigation for large datasets: first/last pages plus a sibling window around the current page, with hidden ranges collapsed to a non-interactive ellipsis.",
    tags=TAGS_BASE + ["ellipsis", "large-datasets", "windowed"],
    features=FEAT_BASE + ["windowed page range", "getPaginationRange helper"],
    accessibility=A11Y_BASE + ["aria-hidden ellipsis with sr-only text"],
    interactive=True,
    related=["pagination", "pagination-with-numbers", "pagination-with-page-size"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationPages,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-with-ellipsis";

const [page, setPage] = useState(25);

<Pagination page={page} totalPages={50} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationPages />
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>

// Wider window:
<PaginationPages siblingCount={2} />''',
    props_doc=props_table(RANGE_PROPS),
    composition_note="`PaginationPages` renders the computed range between the steppers. The ellipsis variant never renders more than `2 * siblingCount + 5` page positions, no matter how large `totalPages` grows.",
    logic_doc=LOGIC_BASE + """

`getPaginationRange(currentPage, totalPages, siblingCount = 1)` produces the visible range:

- Page 1 of 50 → `1 2 … 50`
- Page 3 of 50 → `1 2 3 4 … 50`
- Page 25 of 50 → `1 … 24 25 26 … 50`
- Page 50 of 50 → `1 … 49 50`
- 5 total pages → `1 2 3 4 5` (everything fits, so no ellipsis)

An ellipsis is only emitted when a range is actually hidden — there is never a marker between adjacent pages, and never more than two markers.""",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="The ellipsis is informational, not a control: the glyph is `aria-hidden` and a screen-reader-only \"More pages\" text carries the meaning. It is not focusable and cannot be activated — hidden pages are reached through the first/last window and the steppers.",
    responsive_doc="""Windowing is the mobile strategy: at any width the control row stays short (7 positions at `siblingCount={1}`), and `flex-wrap` covers the rare narrow overflow. Reduce `siblingCount` rather than shrinking controls on very dense screens.""",
    notes_doc="Use for large datasets: file managers, log viewers, admin tables, search results. The algorithm handles first/last/current pages, small counts, and both boundaries without special cases in your code.",
    showcase=DEMO_HELPERS + '''
const PREFIXES = ["quarterly-report", "design-spec", "meeting-notes", "roadmap", "budget", "changelog", "architecture", "user-research", "release-plan", "api-draft"];
const FILES = Array.from({ length: 500 }, (_, i) => ({
  name: PREFIXES[i % PREFIXES.length] + "-" + String(Math.floor(i / PREFIXES.length) + 1).padStart(3, "0") + ".pdf",
  size: ((i * 37) % 900 + 48) + " KB",
}));
const PAGE_SIZE = 10;
function FileBrowser() {
  const [page, setPage] = React.useState(1);
  const totalPages = Math.ceil(FILES.length / PAGE_SIZE);
  const start = (page - 1) * PAGE_SIZE;
  const visible = FILES.slice(start, start + PAGE_SIZE);
  return (
    <div className="space-y-3">
      <ul className={LIST}>
        {visible.map((file) => (
          <li key={file.name} className={ROW}>
            <span className="flex min-w-0 items-center gap-2">
              <span aria-hidden="true" className="inline-flex shrink-0 text-[var(--ds-color-muted-foreground)] [&_svg]:size-3.5"><Icon name="file" /></span>
              <span className={ROW_NAME + " truncate"}>{file.name}</span>
            </span>
            <span className={ROW_META}>{file.size}</span>
          </li>
        ))}
      </ul>
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-3">
        <p className={NOTE}>{FILES.length} files · range {getPaginationRange(page, totalPages).map((i) => (i === "ellipsis" ? "…" : i)).join(" ")}</p>
        <Pagination page={page} totalPages={totalPages} onPageChange={setPage} label="Files pagination">
          <PaginationContent>
            <PaginationItem><PaginationPrevious /></PaginationItem>
            <PaginationPages />
            <PaginationItem><PaginationNext /></PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
function SmallDataset() {
  const [page, setPage] = React.useState(1);
  return (
    <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-3">
      <p className={NOTE}>4 pages — everything fits, no ellipsis is rendered</p>
      <Pagination page={page} totalPages={4} onPageChange={setPage} label="Small dataset pagination">
        <PaginationContent>
          <PaginationItem><PaginationPrevious /></PaginationItem>
          <PaginationPages />
          <PaginationItem><PaginationNext /></PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>File browser — 50 pages</p>
        <FileBrowser />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Small dataset</p>
        <SmallDataset />
      </div>
    </div>
  );
}''',
)

# 5. pagination-compact
register(
    "pagination-compact",
    title="Compact Pagination",
    subcategory="Density",
    description="Compact pagination (32px controls, size=sm) for dense interfaces such as table footers and admin lists — same system, smaller density.",
    tags=TAGS_BASE + ["compact", "dense", "table"],
    features=FEAT_BASE + ["32px controls", "size=sm"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["pagination", "pagination-large", "pagination-with-numbers"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-compact";

const [page, setPage] = useState(1);

// size="sm" is the default in this variant:
<Pagination page={page} totalPages={6} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    {Array.from({ length: 6 }, (_, i) => (
      <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
    ))}
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>''',
    props_doc=props_table(),
    composition_note="Identical primitives to the reference — the only change is the default `size` of `\"sm\"` (32px controls, 13px labels). Pass `size=\"md\"` to opt back into the default density.",
    logic_doc=LOGIC_BASE,
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Compact does not mean cramped: controls stay 32px tall with full `focus-visible` rings and unchanged accessible names. Touch targets remain usable; nothing is shrunk below the small density of the DevSnips Buttons/Inputs families.",
    responsive_doc="""Built for tight layouts: pair with `flex-wrap` footers (status text on the left, pagination on the right) and the row collapses gracefully at 375px. The smaller footprint also makes it the right choice inside cards and panels.""",
    notes_doc="Use in dense, productivity-focused surfaces: data-table footers, admin lists, log viewers. For marketing or editorial pages, prefer the reference or large treatments.",
    showcase=DEMO_HELPERS + '''
const STATUSES = ["Paid", "Shipped", "Pending", "Refunded"];
const STATUS_CLASSES = {
  Paid: "border-[var(--ds-color-success)] bg-[var(--ds-color-success-soft)] text-[var(--ds-color-success)]",
  Shipped: "border-[var(--ds-color-accent)] bg-[var(--ds-color-accent-soft)] text-[var(--ds-color-accent)]",
  Pending: "border-[var(--ds-color-warning)] text-[var(--ds-color-warning)]",
  Refunded: "border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] text-[var(--ds-color-muted-foreground)]",
};
const ORDERS = Array.from({ length: 60 }, (_, i) => ({
  id: "#" + (10420 + i),
  status: STATUSES[i % STATUSES.length],
  total: "$" + ((i * 53) % 420 + 18).toFixed(2),
}));
const PAGE_SIZE = 10;
function OrdersTable() {
  const [page, setPage] = React.useState(1);
  const totalPages = Math.ceil(ORDERS.length / PAGE_SIZE);
  const start = (page - 1) * PAGE_SIZE;
  const visible = ORDERS.slice(start, start + PAGE_SIZE);
  return (
    <div className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]">
      <ul className="m-0 list-none divide-y divide-[var(--ds-color-border)] p-0">
        {visible.map((order) => (
          <li key={order.id} className="flex items-center gap-3 px-4 py-2">
            <span className="text-[13px] font-medium tabular-nums text-[var(--ds-color-foreground)]">{order.id}</span>
            <span className={"inline-flex items-center rounded-[var(--ds-radius-xs)] border px-1.5 py-0.5 text-[11px] font-medium leading-3 " + STATUS_CLASSES[order.status]}>{order.status}</span>
            <span className="ml-auto text-[13px] tabular-nums text-[var(--ds-color-muted-foreground)]">{order.total}</span>
          </li>
        ))}
      </ul>
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-t border-[var(--ds-color-border)] px-4 py-2.5">
        <p className={NOTE}>{start + 1}–{start + visible.length} of {ORDERS.length} orders</p>
        <Pagination page={page} totalPages={totalPages} onPageChange={setPage} label="Orders pagination">
          <PaginationContent>
            <PaginationItem><PaginationPrevious /></PaginationItem>
            {Array.from({ length: totalPages }, (_, i) => (
              <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
            ))}
            <PaginationItem><PaginationNext /></PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Orders table — dense footer</p>
        <OrdersTable />
      </div>
    </div>
  );
}''',
)

# 6. pagination-large
register(
    "pagination-large",
    title="Large Pagination",
    subcategory="Density",
    description="Large pagination (44px controls, size=lg) for prominent content navigation such as featured articles and case studies — comfortable touch targets.",
    tags=TAGS_BASE + ["large", "touch"],
    features=FEAT_BASE + ["44px controls", "size=lg"],
    accessibility=A11Y_BASE + ["44px touch targets"],
    interactive=True,
    related=["pagination", "pagination-compact", "pagination-with-previous-next"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-large";

const [page, setPage] = useState(1);

// size="lg" is the default in this variant:
<Pagination page={page} totalPages={8} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationItem><PaginationLink page={1} /></PaginationItem>
    <PaginationItem><PaginationLink page={2} /></PaginationItem>
    <PaginationItem><PaginationLink page={3} /></PaginationItem>
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>''',
    props_doc=props_table(),
    composition_note="Identical primitives to the reference — the only change is the default `size` of `\"lg\"` (44px controls). Pass `size=\"md\"` to opt back into the default density.",
    logic_doc=LOGIC_BASE,
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="The 44px control height meets comfortable touch-target guidance without any extra work, and every state (idle, current, disabled, focus-visible) scales with the same tokens.",
    responsive_doc="""Large controls wrap earlier, which is the intent: `flex-wrap` moves overflowing controls to a new line at full size instead of shrinking them. For prominent destinations, compose fewer numbers — previous/next plus two or three pages reads better than a dense row.""",
    notes_doc="Use for prominent, content-first navigation: featured articles, case studies, editorial archives, marketing pages. For dense admin surfaces, prefer the compact variant.",
    showcase=DEMO_HELPERS + '''
const CASE_STUDIES = [
  ["Northline Retail — Storefront rebuild", "Retail", "Replacing a legacy theme with tokenized components cut page weight by 41%."],
  ["Vesper Labs — Security dashboard", "Security", "A dense findings table with windowed pagination for 40,000 tracked assets."],
  ["Stratum — Treasury ops", "Fintech", "Approval queues rendered as compact lists with previous/next navigation."],
  ["Meridian — Incident command", "DevOps", "Timeline views paginate by event window to keep responders oriented."],
  ["Atlas Analytics — Reports", "Analytics", "Long reports split into anchored pages so links stay shareable."],
  ["Baseline — Conference site", "Events", "Session archives organized as numbered pages with large touch targets."],
  ["Krat Adventure — Booking flow", "Travel", "Step-based pagination guides travelers through a five-part itinerary."],
  ["Quiet Place — Journal", "Publishing", "Editorial archives with a single featured essay per page."],
];
function CaseStudies() {
  const [page, setPage] = React.useState(1);
  const study = CASE_STUDIES[page - 1];
  return (
    <div className="space-y-4">
      <article className="space-y-2 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-6">
        <p className={LABEL}>{study[1]}</p>
        <h3 className="m-0 text-lg font-semibold leading-6 text-[var(--ds-color-foreground)]">{study[0]}</h3>
        <p className="m-0 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">{study[2]}</p>
      </article>
      <div className="flex justify-center">
        <Pagination page={page} totalPages={CASE_STUDIES.length} onPageChange={setPage} label="Case studies pagination">
          <PaginationContent>
            <PaginationItem><PaginationPrevious /></PaginationItem>
            {Array.from({ length: CASE_STUDIES.length }, (_, i) => (
              <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
            ))}
            <PaginationItem><PaginationNext /></PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Case studies — prominent navigation</p>
        <CaseStudies />
      </div>
    </div>
  );
}''',
)

# 7. pagination-with-page-size
PAGE_SIZE_PROPS = r"""### `<PaginationPageSize>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `number` | — | Selected page size (controlled). |
| `defaultValue` | `number` | first option | Initial page size (uncontrolled). |
| `onValueChange` | `(pageSize: number) => void` | — | Called with the selected page size. |
| `options` | `number[]` | `[10, 20, 50, 100]` | Selectable page sizes. |
| `label` | `string` | `"Rows per page"` | Visible label for the select. |
| `id` | `string` | — | Explicit id for the label/select association. |
| `className` | `string` | — | Extra classes on the wrapper. |

A real, explicitly labeled native `<select>` — rendered OUTSIDE the `<nav>` landmark, because choosing a page size is a filter, not navigation."""

register(
    "pagination-with-page-size",
    title="Pagination with Page Size",
    subcategory="Composite",
    description="Pagination combined with a Rows per page selector: a labeled native select beside the nav landmark that changes the page size and resets the current page.",
    tags=TAGS_BASE + ["page-size", "rows-per-page", "select"],
    features=FEAT_BASE + ["page-size select", "native select control"],
    accessibility=A11Y_BASE + ["labeled native select", "select outside nav landmark"],
    interactive=True,
    related=["pagination", "pagination-with-ellipsis", "pagination-compact"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
  PaginationPageSize,
} from "./pagination-with-page-size";

const [page, setPage] = useState(1);
const [pageSize, setPageSize] = useState(20);
const totalPages = Math.ceil(totalItems / pageSize);

<div className="flex flex-wrap items-center justify-between gap-4">
  <PaginationPageSize
    value={pageSize}
    onValueChange={(size) => { setPageSize(size); setPage(1); }}
    options={[10, 20, 50]}
  />
  <Pagination page={page} totalPages={totalPages} onPageChange={setPage}>
    <PaginationContent>
      <PaginationItem><PaginationPrevious /></PaginationItem>
      {Array.from({ length: totalPages }, (_, i) => (
        <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
      ))}
      <PaginationItem><PaginationNext /></PaginationItem>
    </PaginationContent>
  </Pagination>
</div>''',
    props_doc=props_table(PAGE_SIZE_PROPS),
    composition_note="The page-size selector is a sibling of `<Pagination>`, never a child: render both inside a plain flex row. `PaginationPageSize` is styled with the same input tokens as the DevSnips Select family, so the two controls read as one system without sharing semantics.",
    logic_doc=LOGIC_BASE + """

Changing the page size changes `totalPages`, so always reset to page 1 in `onValueChange` (as in the example above) — otherwise the current page can point past the end of the resized list. Recompute `totalPages` as `Math.ceil(totalItems / pageSize)` and pass it to `<Pagination>`; the clamp inside the root guards any remaining edge.""",
    keyboard_doc="""| Key | Behavior |
|---|---|
| `Tab` / `Shift+Tab` | Move focus through the page-size select and the page controls |
| `Enter` / `Space` | Activate the focused button (state-driven pagination) |
| `ArrowUp` / `ArrowDown` (select focused) | Move through page-size options (native behavior) |

The page-size control is a native `<select>`, so it keeps its full native keyboard and screen-reader behavior.""",
    behavior_doc=STATES,
    a11y_doc="The select has a persistent visible `<label>` (\"Rows per page\") — not a placeholder — and lives outside the `<nav aria-label=\"Pagination\">` landmark, so screen-reader users hear a filter control followed by a navigation landmark rather than a mixed-up widget.",
    responsive_doc="""Place both controls in a `flex flex-wrap items-center justify-between` row: at 375px the select and the nav stack onto separate lines at full size. Never shrink the select below the input height to keep them on one line.""",
    notes_doc="Use for data tables and admin lists where the user controls density. Pair with the ellipsis variant when large page sizes can produce many pages.",
    showcase=DEMO_HELPERS + '''
const FIRST = ["Aaron", "Beatriz", "Chen", "Dalia", "Elias", "Farah", "Gabriel", "Hana", "Ivan", "Julia", "Kenji", "Lara"];
const LAST = ["Alvarez", "Berg", "Costa", "Diallo", "Evans", "Fontaine", "Garcia", "Haupt"];
const COMPANIES = ["Northline", "Vesper Labs", "Stratum", "Meridian", "Atlas", "Baseline", "Krat", "Quiet Place"];
const CUSTOMERS = FIRST.flatMap((first) => LAST.map((last, j) => ({ name: first + " " + last, company: COMPANIES[j % COMPANIES.length] }))).slice(0, 87);
function CustomerList() {
  const [page, setPage] = React.useState(1);
  const [pageSize, setPageSize] = React.useState(20);
  const totalPages = Math.ceil(CUSTOMERS.length / pageSize);
  const start = (page - 1) * pageSize;
  const visible = CUSTOMERS.slice(start, start + pageSize);
  return (
    <div className="space-y-3">
      <ul className={LIST}>
        {visible.map((customer) => (
          <li key={customer.name} className={ROW}>
            <span className={ROW_NAME}>{customer.name}</span>
            <span className={ROW_META}>{customer.company}</span>
          </li>
        ))}
      </ul>
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-3">
        <PaginationPageSize
          value={pageSize}
          onValueChange={(size) => { setPageSize(size); setPage(1); }}
          options={[10, 20, 50]}
        />
        <p className={NOTE}>Showing {start + 1}–{Math.min(start + pageSize, CUSTOMERS.length)} of {CUSTOMERS.length} customers</p>
        <Pagination page={page} totalPages={totalPages} onPageChange={setPage} label="Customers pagination">
          <PaginationContent>
            <PaginationItem><PaginationPrevious /></PaginationItem>
            {Array.from({ length: totalPages }, (_, i) => (
              <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
            ))}
            <PaginationItem><PaginationNext /></PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Customers — 87 rows, adjustable density</p>
        <CustomerList />
      </div>
    </div>
  );
}''',
)

# 8. pagination-disabled
register(
    "pagination-disabled",
    title="Disabled Pagination",
    subcategory="States",
    description="Disabled-state patterns for page navigation: boundary-disabled steppers, an individually disabled page control, and a fully disabled navigation.",
    tags=TAGS_BASE + ["disabled", "states", "boundaries"],
    features=FEAT_BASE + ["boundary-disabled steppers", "per-control disabled", "aria-disabled spans"],
    accessibility=A11Y_BASE + ["disabled controls removed from tab order"],
    interactive=True,
    related=["pagination", "pagination-with-previous-next", "pagination-with-numbers"],
    usage='''import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-disabled";

// Boundary disabling is automatic — Previous is disabled on page 1:
<Pagination page={1} totalPages={5} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationItem><PaginationLink page={1} /></PaginationItem>
    <PaginationItem><PaginationLink page={2} /></PaginationItem>
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>

// Disable one page (e.g. results still loading):
<PaginationLink page={3} disabled />

// Disable the whole navigation:
<Pagination disabled page={2} totalPages={5} onPageChange={setPage}>…</Pagination>''',
    props_doc=props_table(),
    composition_note="No new primitives — this variant documents and demonstrates the three disabled paths built into the core: automatic boundary disabling on the steppers, `disabled` on a single `PaginationLink`, and `disabled` on the `<Pagination>` root.",
    logic_doc=LOGIC_BASE + """

Every disabled path renders the control as a non-interactive `<span aria-disabled=\"true\">` instead of an anchor or button: it stays visible (50% opacity, same geometry, no layout shift) but leaves the tab order and cannot be activated by click, Enter, or Space. When a boundary control becomes enabled again it returns to its normal element.""",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Disabled controls are announced as \"dimmed\"/unavailable via `aria-disabled` and are skipped by keyboard focus, so users cannot land on a control that does nothing. The current page keeps `aria-current=\"page\"` even while the navigation is disabled, preserving position context.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Do not fake disabled states with `pointer-events: none` on active elements — a disabled control must be a genuinely non-interactive element. This variant's demos cover the first page, the last page, an unavailable middle page, and a fully disabled navigation.",
    showcase=DEMO_HELPERS + '''
const ACTIVITY = [
  "Deployed v2.4.1 to production", "Merged PR #482 — Fix table overflow", "Added pagination to the orders view",
  "Rolled back migration 0042", "Updated design tokens for dark mode", "Closed issue #217 — Focus ring in dialogs",
  "Published the Buttons family README", "Enabled branch protection on main", "Rotated CI cache keys",
  "Tagged release v2.4.0", "Archived the legacy tooltip package", "Reviewed 6 pull requests",
  "Provisioned the staging database", "Drafted the Pagination spec", "Onboarded two contributors",
];
const PAGE_SIZE = 3;
const TOTAL_PAGES = Math.ceil(ACTIVITY.length / PAGE_SIZE);
function ActivityNav({ page, onPageChange, disabledPage }) {
  return (
    <Pagination page={page} totalPages={TOTAL_PAGES} onPageChange={onPageChange} label="Activity pagination">
      <PaginationContent>
        <PaginationItem><PaginationPrevious /></PaginationItem>
        {Array.from({ length: TOTAL_PAGES }, (_, i) => (
          <PaginationItem key={i + 1}><PaginationLink page={i + 1} disabled={disabledPage === i + 1} /></PaginationItem>
        ))}
        <PaginationItem><PaginationNext /></PaginationItem>
      </PaginationContent>
    </Pagination>
  );
}
function ActivityList({ page }) {
  const start = (page - 1) * PAGE_SIZE;
  return (
    <ul className={LIST}>
      {ACTIVITY.slice(start, start + PAGE_SIZE).map((entry) => (
        <li key={entry} className="px-4 py-2.5 text-sm text-[var(--ds-color-foreground)]">{entry}</li>
      ))}
    </ul>
  );
}
function FirstPageDemo() {
  const [page, setPage] = React.useState(1);
  return (
    <div className="space-y-3">
      <ActivityList page={page} />
      <ActivityNav page={page} onPageChange={setPage} />
      <p className={NOTE}>Page 1 — Previous renders as a non-interactive aria-disabled span.</p>
    </div>
  );
}
function LastPageDemo() {
  const [page, setPage] = React.useState(TOTAL_PAGES);
  return (
    <div className="space-y-3">
      <ActivityList page={page} />
      <ActivityNav page={page} onPageChange={setPage} />
      <p className={NOTE}>Page {TOTAL_PAGES} of {TOTAL_PAGES} — Next is disabled at the last page.</p>
    </div>
  );
}
function UnavailablePageDemo() {
  const [page, setPage] = React.useState(2);
  return (
    <div className="space-y-3">
      <ActivityNav page={page} onPageChange={setPage} disabledPage={3} />
      <p className={NOTE}>Page 3 is still loading and cannot be activated; the other pages work.</p>
    </div>
  );
}
function FullyDisabledDemo() {
  return (
    <div className="space-y-3">
      <Pagination disabled page={2} totalPages={TOTAL_PAGES} label="Disabled pagination">
        <PaginationContent>
          <PaginationItem><PaginationPrevious /></PaginationItem>
          {Array.from({ length: TOTAL_PAGES }, (_, i) => (
            <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
          ))}
          <PaginationItem><PaginationNext /></PaginationItem>
        </PaginationContent>
      </Pagination>
      <p className={NOTE}>disabled on the root — every control is inert while data reloads.</p>
    </div>
  );
}
function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>First page</p>
        <FirstPageDemo />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Last page</p>
        <LastPageDemo />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Unavailable page</p>
        <UnavailablePageDemo />
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Entire navigation disabled</p>
        <FullyDisabledDemo />
      </div>
    </div>
  );
}''',
)
