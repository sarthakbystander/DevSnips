"""Registry for the DevSnips React Breadcrumbs generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs.
The generator (``_gen_react_breadcrumbs.py``) reads each component's
``code.tsx`` from disk and combines it with the spec here to write
``code.jsx``, ``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented trails only (Home, Documentation, React,
Components, Products, Developer Tools, Design tokens). No lorem ipsum, no
marketing buzzwords.
"""
from _gen_react_breadcrumbs import register, KEYBOARD_MENU, STATES, RESPONSIVE_BASE

TAGS_BASE = ["breadcrumbs", "navigation", "react", "tailwind", "accessible", "responsive", "links", "hierarchy"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic nav landmark", "ordered list", 'aria-current="page"']
A11Y_BASE = ["nav landmark with aria-label", "ordered list structure", "real anchor links", 'aria-current="page"', "aria-hidden separators", "focus-visible"]

# Shared props tables. The six core primitives carry the same API family-wide.
BREADCRUMBS_PROPS = r"""### `<Breadcrumbs>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | `"Breadcrumb"` | Accessible label for the `<nav>` landmark. |
| `separator` | `ReactNode` | chevron icon | Default separator content for every `<BreadcrumbSeparator>` without children. |
| `className` | `string` | — | Extra classes on the `<nav>`. |
| `children` | `ReactNode` | — | `BreadcrumbList` composition. |"""

LIST_PROPS = r"""### `<BreadcrumbList>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<ol>`. |
| `children` | `ReactNode` | — | `BreadcrumbItem` + `BreadcrumbSeparator` elements. |"""

ITEM_PROPS = r"""### `<BreadcrumbItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<li>`. |
| `children` | `ReactNode` | — | Usually one `BreadcrumbLink` or `BreadcrumbCurrent`. |"""

LINK_PROPS = r"""### `<BreadcrumbLink>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` (required) | — | Destination URL — rendered as a real anchor with normal browser navigation. |
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered `aria-hidden`). |
| `className` | `string` | — | Extra classes on the anchor. |
| `children` | `ReactNode` | — | Visible label. |

All native anchor attributes (`target`, `rel`, `aria-label`, `title`, …) are forwarded."""

CURRENT_PROPS = r"""### `<BreadcrumbCurrent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered `aria-hidden`). |
| `className` | `string` | — | Extra classes on the span. |
| `children` | `ReactNode` | — | Visible label (rendered with `aria-current="page"`). |"""

SEPARATOR_PROPS = r"""### `<BreadcrumbSeparator>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the list item. |
| `children` | `ReactNode` | context `separator` | Custom separator content for this position only. |"""


def props_table(*extra):
    parts = [BREADCRUMBS_PROPS, LIST_PROPS, ITEM_PROPS, LINK_PROPS, CURRENT_PROPS, SEPARATOR_PROPS]
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
"""

# 1. breadcrumbs (reference)
register(
    "breadcrumbs",
    title="Breadcrumbs",
    subcategory="Core",
    description="Accessible breadcrumb navigation as a compound component: semantic nav landmark, ordered list, real anchor links, and an aria-current current page.",
    tags=TAGS_BASE,
    features=FEAT_BASE,
    accessibility=A11Y_BASE,
    interactive=False,
    related=["breadcrumbs-with-home", "breadcrumbs-with-current", "breadcrumbs-with-separator", "breadcrumbs-collapsed"],
    usage='''import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs";

<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation">Documentation</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/react">React</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/react/components">Components</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>''',
    props_doc=props_table(),
    composition_note="This is the reference composition — every other variant in the family uses the same six primitives and extends the same class constants, states, and accessibility model.",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Give the `<nav>` a more specific `label` (for example `label=\"Store breadcrumb\"`) when more than one breadcrumb trail lives on a page. The current page is distinguished by weight and color together — never by color alone.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Reference implementation for the Breadcrumbs family. It establishes the shared typography (`text-sm leading-5`), the 6px inline rhythm, the muted-link / foreground-current color model, the chevron default separator, the `radius-xs` focus ring, and the wrap-not-scroll responsive behavior that every other variant extends.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const hash = useDemoHash();
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Documentation</p>
        <Breadcrumbs>
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation/react">React</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation/react/components">Components</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Buttons</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Store</p>
        <Breadcrumbs label="Store breadcrumb">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/products">Products</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/products/developer-tools">Developer Tools</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>DevSnips</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>Links are real anchors — clicking one updates the demo location (<code>{hash || "(root)"}</code>) without a page reload. The last level is the current page, plain text with <code>aria-current="page"</code>, not a link.</p>
    </div>
  );
}''',
)

# 2. breadcrumbs-with-home
register(
    "breadcrumbs-with-home",
    title="Breadcrumbs With Home",
    subcategory="Content",
    description="Breadcrumb trail whose first level is the application home, rendered with a meaningful home icon that stays hidden from screen readers when a visible label is present.",
    tags=TAGS_BASE + ["icon", "home"],
    features=FEAT_BASE + ["leading home icon", "icon-only home link option"],
    accessibility=A11Y_BASE + ["icon aria-hidden", "aria-label on icon-only link"],
    interactive=False,
    related=["breadcrumbs", "breadcrumbs-with-icons", "breadcrumbs-with-current"],
    usage='''import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs-with-home";

// Icon + text — the icon is decorative and rendered aria-hidden:
<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/" icon={<HomeIcon />}>Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/products">Products</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>DevSnips</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>

// Icon-only home link — give it a real accessible name instead of text:
<BreadcrumbLink href="/" aria-label="Home" icon={<HomeIcon />} />''',
    props_doc=props_table(),
    composition_note="No new primitives — the home treatment is the `icon` prop on the first `BreadcrumbLink`. The icon is rendered `aria-hidden` because the visible \"Home\" text carries the accessible name; for an icon-only link, pass `aria-label=\"Home\"` so the link still has an accessible name.",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="The home icon never replaces the accessible name: it is decorative next to visible text (`aria-hidden`), and an icon-only home link must carry `aria-label=\"Home\"`. Do not use an emoji for the home glyph — pass any SVG node.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="The home level is the highest-traffic target in the trail, so it keeps the same 14px label rhythm as every other level — the icon adds recognition, not extra size.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const hash = useDemoHash();
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Icon + text</p>
        <Breadcrumbs>
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/" icon={<Icon name="home" />}>Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/products">Products</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/products/developer-tools">Developer Tools</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>DevSnips</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Icon-only home link</p>
        <Breadcrumbs label="Documentation breadcrumb">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/" aria-label="Home" icon={<Icon name="home" />} /></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation/components">Components</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Tabs</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>With visible \"Home\" text the icon is <code>aria-hidden</code> — decorative. The icon-only variant carries a real <code>aria-label=\"Home\"</code>. Demo location: <code>{hash || "(root)"}</code>.</p>
    </div>
  );
}''',
)

# 3. breadcrumbs-with-icons
register(
    "breadcrumbs-with-icons",
    title="Breadcrumbs With Icons",
    subcategory="Content",
    description="Breadcrumb levels with optional meaningful leading icons — passed as ReactNode, rendered aria-hidden, and never required on every item.",
    tags=TAGS_BASE + ["icon"],
    features=FEAT_BASE + ["optional per-level icons"],
    accessibility=A11Y_BASE + ["icon aria-hidden"],
    interactive=False,
    related=["breadcrumbs", "breadcrumbs-with-home", "breadcrumbs-with-separator"],
    usage='''import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs-with-icons";

<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/" icon={<HomeIcon />}>Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation" icon={<DocsIcon />}>Documentation</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      {/* Icons are optional — this level carries none. */}
      <BreadcrumbLink href="/documentation/components">Components</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent icon={<GridIcon />}>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>''',
    props_doc=props_table(),
    composition_note="No new primitives — `BreadcrumbLink` and `BreadcrumbCurrent` both accept an optional `icon` ReactNode. Icons communicate the level's meaning (a book for documentation, a grid for a component library); they are not decoration, and no level is required to have one.",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Every icon is rendered `aria-hidden` — the visible label carries the accessible name, so screen readers never hear a redundant or missing glyph description. No icon library dependency is introduced: pass any SVG ReactNode.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Icons inherit the 14px label size (`[&_svg]:size-3.5`) and the link's currentColor, so they track hover and theme changes with the text.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const hash = useDemoHash();
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Documentation</p>
        <Breadcrumbs>
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/" icon={<Icon name="home" />}>Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation" icon={<Icon name="book" />}>Documentation</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation/components" icon={<Icon name="grid" />}>Components</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Buttons</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Inventory</p>
        <Breadcrumbs label="Inventory breadcrumb">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/" icon={<Icon name="home" />}>Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/inventory">Inventory</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/inventory/warehouses" icon={<Icon name="folder" />}>Warehouses</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent icon={<Icon name="package" />}>North Depot</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>Icons are optional ReactNode values rendered <code>aria-hidden</code> — \"Buttons\" and \"Inventory\" carry none. Demo location: <code>{hash || "(root)"}</code>.</p>
    </div>
  );
}''',
)

# 4. breadcrumbs-with-current
register(
    "breadcrumbs-with-current",
    title="Breadcrumbs With Current",
    subcategory="States",
    description="Breadcrumb trail that explicitly distinguishes the current location: aria-current page text that is never a navigable link, via BreadcrumbCurrent or the current prop for data-driven trails.",
    tags=TAGS_BASE + ["current-page", "aria-current"],
    features=FEAT_BASE + ["current prop for data-driven trails"],
    accessibility=A11Y_BASE,
    interactive=False,
    related=["breadcrumbs", "breadcrumbs-with-home", "breadcrumbs-with-dropdown"],
    usage='''import { Fragment } from "react";
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbSeparator,
} from "./breadcrumbs-with-current";

const trail = [
  { label: "Home", href: "/" },
  { label: "Documentation", href: "/documentation" },
  { label: "Components", href: "/documentation/components" },
  { label: "Tabs", href: "/documentation/components/tabs", current: true },
];

// Data-driven: `current` turns the link into non-navigable current text,
// so every level maps through one component without branching.
<Breadcrumbs>
  <BreadcrumbList>
    {trail.map((level, index) => (
      <Fragment key={level.href}>
        {index > 0 ? <BreadcrumbSeparator /> : null}
        <BreadcrumbItem>
          <BreadcrumbLink href={level.href} current={level.current}>
            {level.label}
          </BreadcrumbLink>
        </BreadcrumbItem>
      </Fragment>
    ))}
  </BreadcrumbList>
</Breadcrumbs>

// Explicit composition uses <BreadcrumbCurrent> for the last level.''',
    props_doc=props_table(),
    composition_note="Two ways to mark the current page: compose `<BreadcrumbCurrent>` explicitly, or pass `current` to `<BreadcrumbLink>` — it then renders the same non-navigable `aria-current=\"page\"` text instead of an anchor, which keeps data-driven trails (route tables, CMS slugs) branch-free.",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="The current page is never a link to itself: `aria-current=\"page\"` marks it for assistive technology, and the medium-weight foreground treatment keeps the distinction subtle and token-driven — never color alone, since weight changes with it.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Use the `current` prop when levels come from data (every entry has an href, including the page you are on); use `<BreadcrumbCurrent>` when composing by hand.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const trail = [
    { label: "Home", href: "#/" },
    { label: "Documentation", href: "#/documentation" },
    { label: "Components", href: "#/documentation/components" },
    { label: "Tabs", href: "#/documentation/components/tabs", current: true },
  ];
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Data-driven trail (current prop)</p>
        <Breadcrumbs>
          <BreadcrumbList>
            {trail.map((level, index) => (
              <React.Fragment key={level.href}>
                {index > 0 ? <BreadcrumbSeparator /> : null}
                <BreadcrumbItem>
                  <BreadcrumbLink href={level.href} current={level.current}>
                    {level.label}
                  </BreadcrumbLink>
                </BreadcrumbItem>
              </React.Fragment>
            ))}
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Explicit composition (BreadcrumbCurrent)</p>
        <Breadcrumbs label="Store breadcrumb">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/products">Products</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>DevSnips</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>\"Tabs\" and \"DevSnips\" are the current page: plain medium-weight text with <code>aria-current="page"</code> — inspect them and you will find no anchor.</p>
    </div>
  );
}''',
)

# 5. breadcrumbs-with-dropdown
register(
    "breadcrumbs-with-dropdown",
    title="Breadcrumbs With Dropdown",
    subcategory="Composite",
    description="Breadcrumb trail where one level opens a keyboard-accessible menu of related pages — a real menu button with aria-haspopup and aria-expanded, containing real anchor links.",
    tags=TAGS_BASE + ["dropdown", "menu", "keyboard", "interactive"],
    features=FEAT_BASE + ["level dropdown menu", "Escape closes", "outside-click closes", "arrow-key menu navigation"],
    accessibility=A11Y_BASE + ["aria-haspopup=menu", "aria-expanded", "menu / menuitem roles", "Escape returns focus"],
    interactive=True,
    related=["breadcrumbs", "breadcrumbs-collapsed", "breadcrumbs-with-current"],
    usage='''import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
  BreadcrumbDropdown,
} from "./breadcrumbs-with-dropdown";

<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation">Documentation</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbDropdown
      label="Components"
      items={[
        { label: "Buttons", href: "/documentation/components/buttons", current: true },
        { label: "Inputs", href: "/documentation/components/inputs" },
        { label: "Selects", href: "/documentation/components/selects" },
        { label: "Tabs", href: "/documentation/components/tabs" },
        { label: "Breadcrumbs", href: "/documentation/components/breadcrumbs" },
      ]}
    />
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>''',
    props_doc=props_table("""### `<BreadcrumbDropdown>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` (required) | — | Visible trigger label — the name of this breadcrumb level. Also the menu's `aria-label`. |
| `items` | `BreadcrumbDropdownItem[]` (required) | — | Related pages offered at this level. |
| `aria-label` | `string` | `label` | Accessible name override for the trigger. |
| `className` | `string` | — | Extra classes on the wrapping list item. |

`BreadcrumbDropdownItem` = `{ label: ReactNode; href: string; icon?: ReactNode; current?: boolean }`. Set `current` on the item matching the page you are on — it is marked `aria-current="page"` and emphasized."""),
    composition_note="`<BreadcrumbDropdown>` renders its own `<li>` and slots between separators like any other level. Only that level becomes a menu — the rest of the trail stays plain breadcrumb navigation.",
    keyboard_doc=KEYBOARD_MENU,
    behavior_doc=STATES + """
- **Dropdown trigger** — styled as a breadcrumb link with a chevron; the chevron rotates 180° while open and the label takes the foreground color (`aria-expanded` state, not color alone).
- **Menu items** — `surface-hover` on hover/focus; the `current` item is medium weight with `aria-current="page"`.""",
    a11y_doc="The trigger is a real `<button>` with `aria-haspopup=\"menu\"` and `aria-expanded`; the menu is `role=\"menu\"` of real `<a role=\"menuitem\">` links, labelled by the level name. Escape closes and returns focus to the trigger; pointer interaction outside closes the menu. Focus moves into the menu on open and cycles with the arrow keys.",
    responsive_doc="""The trigger is a `min-w-0` flexible item, so a long level name truncates with the rest of the trail on narrow screens. The menu is absolutely positioned under its level with `min-w-[180px]`; keep item labels short enough to fit small viewports.

""" + RESPONSIVE_BASE,
    notes_doc="Use the dropdown when a level has meaningful siblings a reader may want to jump between (component categories, doc sections). Do not turn the whole trail into a menu — one level at most.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const hash = useDemoHash();
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Component library</p>
        <Breadcrumbs>
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbDropdown
              label="Components"
              items={[
                { label: "Buttons", href: "#/documentation/components/buttons", current: true },
                { label: "Inputs", href: "#/documentation/components/inputs" },
                { label: "Selects", href: "#/documentation/components/selects" },
                { label: "Tabs", href: "#/documentation/components/tabs" },
                { label: "Breadcrumbs", href: "#/documentation/components/breadcrumbs" },
              ]}
            />
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Buttons</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>Open \"Components\" with a click, Enter, or ArrowDown; move with the arrow keys, Escape closes. Menu items are real anchors — the demo location updates (<code>{hash || "(root)"}</code>) without a page reload. The current page is marked inside the menu.</p>
    </div>
  );
}''',
)

# 6. breadcrumbs-collapsed
register(
    "breadcrumbs-collapsed",
    title="Breadcrumbs Collapsed",
    subcategory="Layout",
    description="Long breadcrumb paths with middle levels collapsed behind an accessible ellipsis disclosure — the hidden levels stay reachable as real links from a keyboard-operable menu.",
    tags=TAGS_BASE + ["collapse", "ellipsis", "keyboard", "interactive", "long-paths"],
    features=FEAT_BASE + ["ellipsis disclosure", "hidden levels stay accessible", "Escape closes", "outside-click closes"],
    accessibility=A11Y_BASE + ["aria-haspopup=menu", "aria-expanded", "menu / menuitem roles", "Escape returns focus", "disclosure has accessible name"],
    interactive=True,
    related=["breadcrumbs", "breadcrumbs-max-width", "breadcrumbs-with-dropdown"],
    usage='''import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
  BreadcrumbEllipsis,
} from "./breadcrumbs-collapsed";

// Home / … / Components / Buttons
<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbEllipsis
      items={[
        { label: "Documentation", href: "/documentation" },
        { label: "React", href: "/documentation/react" },
      ]}
    />
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/react/components">Components</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>''',
    props_doc=props_table("""### `<BreadcrumbEllipsis>`

| Name | Type | Default | Description |
|---|---|---|---|
| `items` | `BreadcrumbEllipsisItem[]` (required) | — | The collapsed levels, in path order. |
| `label` | `string` | `"Show hidden breadcrumb levels"` | Accessible name for the disclosure button. |
| `className` | `string` | — | Extra classes on the wrapping list item. |

`BreadcrumbEllipsisItem` = `{ label: ReactNode; href: string; icon?: ReactNode }`."""),
    composition_note="`<BreadcrumbEllipsis>` renders its own `<li>` and slots between separators where the removed levels would have been. Keep the first level (Home) and the last one or two levels visible; collapse the middle.",
    keyboard_doc=KEYBOARD_MENU,
    behavior_doc=STATES + """
- **Ellipsis trigger** — compact `…` button; `surface-hover` on hover, `surface-active` + foreground while open (`aria-expanded` state, not color alone).
- **Menu items** — `surface-hover` on hover/focus; each is a real anchor link.""",
    a11y_doc="The collapsed levels are never hidden with CSS alone — they are real anchor links inside a `role=\"menu\"` disclosure. The trigger is a `<button aria-haspopup=\"menu\" aria-expanded>` named \"Show hidden breadcrumb levels\" (override with `label`), reachable in the normal tab order, so keyboard and screen-reader users can reach every level. Escape closes and returns focus to the trigger.",
    responsive_doc="""Collapsing is the preferred small-screen strategy: at 375px a five-level trail becomes Home / … / Components / Buttons, which fits without wrapping or scrolling while keeping every level reachable.

""" + RESPONSIVE_BASE,
    notes_doc="Choose which levels to collapse from your route data (typically `items.slice(1, -2)`). The ellipsis menu preserves path order, top to bottom.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const hash = useDemoHash();
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Five-level documentation path</p>
        <Breadcrumbs>
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbEllipsis
              items={[
                { label: "Documentation", href: "#/documentation" },
                { label: "React", href: "#/documentation/react" },
              ]}
            />
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation/react/components">Components</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Buttons</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Six-level settings path</p>
        <Breadcrumbs label="Settings breadcrumb">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbEllipsis
              label="Show hidden settings sections"
              items={[
                { label: "Workspace", href: "#/workspace" },
                { label: "Projects", href: "#/workspace/projects" },
                { label: "Atlas Analytics", href: "#/workspace/projects/atlas-analytics" },
              ]}
            />
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/workspace/projects/atlas-analytics/settings">Settings</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Billing</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>The \"…\" button is a real disclosure: click it or press Enter/ArrowDown, move with the arrow keys, Escape closes. Hidden levels are real anchors — the demo location updates (<code>{hash || "(root)"}</code>).</p>
    </div>
  );
}''',
)

# 7. breadcrumbs-max-width
register(
    "breadcrumbs-max-width",
    title="Breadcrumbs Max Width",
    subcategory="Layout",
    description="Breadcrumb trail that bounds long labels with max-width truncation while keeping the full text available through the title attribute — no clipped, meaningless navigation.",
    tags=TAGS_BASE + ["truncation", "max-width", "long-labels"],
    features=FEAT_BASE + ["label truncation", "auto title from label", "wraps on narrow screens"],
    accessibility=A11Y_BASE + ["full label via title", "full text in accessibility tree"],
    interactive=False,
    related=["breadcrumbs", "breadcrumbs-collapsed", "breadcrumbs-with-separator"],
    usage='''import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs-max-width";

<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/design-tokens">
        Design tokens and theming guidelines
      </BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Overriding tokens for white-label themes</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>

// Labels truncate at 9rem (14rem from sm up). The `title` attribute is
// auto-filled from string children — pass `title` explicitly when the
// label is a ReactNode:
<BreadcrumbLink href="/glossary" title="White-label theming">
  <em>White-label</em> theming
</BreadcrumbLink>''',
    props_doc=props_table(),
    composition_note="Same six primitives — this variant bakes a bounded `max-w` + `truncate` into `BreadcrumbLink` and `BreadcrumbCurrent` and auto-fills `title` from string children, so truncation never destroys the meaning of the trail.",
    keyboard_doc=None,
    behavior_doc=STATES + """
- **Truncated label** — ends in an ellipsis inside `max-w-[9rem]` (`sm:max-w-[14rem]`); hovering reveals the native `title` tooltip with the full text.""",
    a11y_doc="Truncation is purely visual CSS (`truncate`) — the full label remains in the accessibility tree, so screen readers announce the complete text. The `title` attribute (auto-filled from string children, or passed explicitly for ReactNode labels) exposes the full text to sighted users on hover.",
    responsive_doc="""Each label is capped at `max-w-[9rem]` below `sm` and `max-w-[14rem]` above, so no single verbose level can push the trail past the viewport. The list still wraps (`flex-wrap`) when several capped levels exceed the line — truncation bounds labels, wrapping handles volume. Neither creates page-level horizontal scrolling.""",
    notes_doc="Do not rely on `overflow-hidden` alone: without the `title` attribute and the full accessibility-tree text, clipping would destroy meaning. Tune the caps through the `LINK_CLASSES` / `CURRENT_CLASSES` constants if your density differs.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const hash = useDemoHash();
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Long labels</p>
        <Breadcrumbs>
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbLink href="#/documentation/design-tokens">
                Design tokens and theming guidelines
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbCurrent>Overriding tokens for white-label themes</BreadcrumbCurrent>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Deep path with a long level</p>
        <Breadcrumbs label="Catalog breadcrumb">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/catalog">Catalog</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbLink href="#/catalog/hand-cast-stoneware">
                Hand-cast stoneware vessels and tableware
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Rimmed Serving Bowl</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>Long labels truncate with an ellipsis — hover one to read the full text in the <code>title</code> tooltip. Screen readers announce the full label regardless. Demo location: <code>{hash || "(root)"}</code>.</p>
    </div>
  );
}''',
)

# 8. breadcrumbs-with-separator
register(
    "breadcrumbs-with-separator",
    title="Breadcrumbs With Separator",
    subcategory="Content",
    description="Breadcrumb trail with a configurable separator: set one separator node on the root for the whole trail, or override a single position — separators stay decorative and aria-hidden.",
    tags=TAGS_BASE + ["separator"],
    features=FEAT_BASE + ["configurable separator", "per-position override"],
    accessibility=A11Y_BASE,
    interactive=False,
    related=["breadcrumbs", "breadcrumbs-with-home", "breadcrumbs-with-icons"],
    usage='''import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs-with-separator";

// One separator for the whole trail:
<Breadcrumbs separator="/">
  <BreadcrumbList>
    <BreadcrumbItem><BreadcrumbLink href="/">Home</BreadcrumbLink></BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem><BreadcrumbLink href="/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem><BreadcrumbCurrent>Tabs</BreadcrumbCurrent></BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>

// A custom icon separator:
<Breadcrumbs separator={<ChevronRightIcon />}>…</Breadcrumbs>

// Override a single position in place:
<BreadcrumbSeparator>{">"}</BreadcrumbSeparator>''',
    props_doc=props_table(),
    composition_note="The separator is resolved per position: a `<BreadcrumbSeparator>` with children uses them, otherwise it falls back to the `separator` given to `<Breadcrumbs>` through context, otherwise the default chevron. Set it once on the root to restyle the whole trail.",
    keyboard_doc=None,
    behavior_doc=STATES,
    a11y_doc="Separators are structural decoration, not navigation: every separator renders an `aria-hidden` `role=\"presentation\"` list item, so it is never announced, never focusable, and never behaves like a link — whichever glyph you choose.",
    responsive_doc=RESPONSIVE_BASE,
    notes_doc="Keep separators restrained: a chevron, a slash, or a single angle bracket. The glyph inherits the muted-foreground token and the 14px icon sizing, so custom separators stay in the same visual language.",
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const hash = useDemoHash();
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Default chevron</p>
        <Breadcrumbs>
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Tabs</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Slash — separator=&quot;/&quot;</p>
        <Breadcrumbs separator="/" label="Documentation breadcrumb with slash separators">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/documentation/react">React</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbCurrent>Components</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <div className="space-y-2">
        <p className={LABEL}>Custom icon + one overridden position</p>
        <Breadcrumbs separator={<Icon name="arrow-right" />} label="Store breadcrumb with arrow separators">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink href="#/">Home</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink href="#/products">Products</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator>{">"}</BreadcrumbSeparator>
            <BreadcrumbItem><BreadcrumbCurrent>DevSnips</BreadcrumbCurrent></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumbs>
      </div>
      <p className={NOTE}>Separators are <code>aria-hidden</code> decoration — assistive technology announces only the levels. Demo location: <code>{hash || "(root)"}</code>.</p>
    </div>
  );
}''',
)
