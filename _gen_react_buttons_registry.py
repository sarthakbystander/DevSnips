"""Registry for the DevSnips React Buttons migration generator.

Calls `register()` (imported from _gen_react_buttons) once per button with
the full code.tsx body, the preview Showcase JS, and the README doc fields.
All visual decisions come from React/DESIGN_TOKENS.md and are expressed as
Tailwind utilities consuming the --ds-* semantic tokens.
"""
from _gen_react_buttons import register  # noqa: F401

# ---------------------------------------------------------------------------
# Shared class strings (Tailwind utilities + semantic token arbitrary values)
# ---------------------------------------------------------------------------
CX = """function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}"""

SPINNER = """function Spinner() {
  return (
    <svg className="h-[1em] w-[1em] shrink-0 animate-spin motion-reduce:animate-none" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="3" className="opacity-25" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}"""

SIZES_TS = """const SIZES: Record<ButtonSize, string> = {
  xs: "h-7 gap-1 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 gap-1.5 px-3 text-xs [&_svg]:size-[14px]",
  md: "h-9 gap-2 px-3.5 text-[13px] [&_svg]:size-4",
  lg: "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 gap-2 px-5 text-sm [&_svg]:size-5",
};"""

BASE = (
    "inline-flex select-none items-center justify-center whitespace-nowrap "
    "rounded-[var(--ds-radius-sm)] border font-medium leading-none "
    "transition-colors duration-150 ease-out motion-reduce:transition-none "
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] "
    "disabled:pointer-events-none disabled:opacity-50"
)

V_SOLID = (
    "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] "
    "hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] "
    "active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]"
)
V_OUTLINE = (
    "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] "
    "hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]"
)
V_SECONDARY = (
    "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] "
    "hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]"
)
V_GHOST = (
    "border-transparent bg-transparent text-[var(--ds-color-foreground)] "
    "hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]"
)
V_DESTRUCTIVE = (
    "border-transparent bg-[var(--ds-color-destructive)] text-[var(--ds-color-destructive-foreground)] "
    "hover:bg-[color-mix(in_srgb,var(--ds-color-destructive)_88%,#000)] "
    "active:bg-[color-mix(in_srgb,var(--ds-color-destructive)_80%,#000)]"
)
V_DESTRUCTIVE_OUTLINE = (
    "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-destructive)] "
    "hover:bg-[var(--ds-color-destructive-soft)] active:bg-[var(--ds-color-destructive-soft)]"
)
V_SUCCESS = (
    "border-transparent bg-[var(--ds-color-success)] text-[var(--ds-color-success-foreground)] "
    "hover:bg-[color-mix(in_srgb,var(--ds-color-success)_88%,#000)] "
    "active:bg-[color-mix(in_srgb,var(--ds-color-success)_80%,#000)]"
)

# Shared doc snippets reused across the family for consistency.
SIZES_DOC = "xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px."
A11Y_NATIVE = "Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl."
STATES_STD = "default · hover · active · focus-visible · loading (spinner + `aria-busy`, layout preserved) · disabled (reduced opacity)."

FEAT = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic HTML", "keyboard accessible"]
A11Y = ["focus-visible", "keyboard accessible", "ARIA", "semantic HTML", "reduced-motion"]


# =========================================================== solid-button ===
register(
    "solid-button",
    title="Solid Button",
    eyebrow="React Component",
    lede="The primary, high-emphasis action. A filled neutral surface built on color.primary and color.primary-foreground — the canonical confirmation control in the DevSnips React system.",
    subcategory="Primary",
    tags=["button", "react", "tailwind", "primary", "action", "interactive", "form"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["outline-button", "secondary-button", "ghost-button"],
    props_doc={
        "usage": "<SolidButton size=\"md\" onClick={save}>Save changes</SolidButton>",
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `size` | `xs \\| sm \\| md \\| lg \\| xl` | `md` |\n| `block` | `boolean` | `false` |\n| `loading` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` / `iconRight` | `ReactNode` | — |\n| `type` | `button \\| submit \\| reset` | `button` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>` (onClick, aria-*, etc.).",
    },
    variants_doc="Single filled variant built on `color.primary` / `color.primary-foreground`. See OutlineButton / SecondaryButton / GhostButton for other emphasis levels.",
    sizes_doc=SIZES_DOC,
    states_doc=STATES_STD,
    a11y_doc=A11Y_NATIVE,
    notes_doc="Keep exactly one solid button per prominent surface to preserve hierarchy. Pair with an OutlineButton for the cancel/secondary action.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — SolidButton
 * Filled primary action. High-emphasis: one per surface. Built on the
 * semantic tokens color.primary / color.primary-foreground from
 * React/DESIGN_TOKENS.md. Tailwind utilities consume the tokens via
 * arbitrary values (var(--ds-...)) so the button themes with the surface.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface SolidButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  /** Control height. `md` (36px) is the default. */
  size?: ButtonSize;
  /** Fill the available width (`w-full`). */
  block?: boolean;
  /** Show a spinner and disable interaction while an action is pending. */
  loading?: boolean;
  /** Leading icon node. */
  iconLeft?: ReactNode;
  /** Trailing icon node. */
  iconRight?: ReactNode;
}}

{CX}

{SPINNER}

{SIZES_TS}

export function SolidButton({{
  children,
  size = "md",
  block = false,
  loading = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}}: SolidButtonProps) {{
  const isDisabled = disabled || loading;
  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        "{V_SOLID}",
        SIZES[size],
        block && "w-full",
        className,
      )}}
      disabled={{isDisabled}}
      aria-busy={{loading || undefined}}
      {{...rest}}
    >
      {{loading ? <Spinner /> : iconLeft}}
      <span>{{children}}</span>
      {{!loading && iconRight}}
    </button>
  );
}}

export default SolidButton;
''',
    showcase=r'''function Showcase() {
  const [saving, setSaving] = React.useState(false);
  function simulate() { setSaving(true); setTimeout(() => setSaving(false), 1600); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → xl · md is default</span></div>
        <div className="ds-row">
          <SolidButton size="xs">Save</SolidButton>
          <SolidButton size="sm">Save changes</SolidButton>
          <SolidButton size="md">Save changes</SolidButton>
          <SolidButton size="lg">Save changes</SolidButton>
          <SolidButton size="xl">Create project</SolidButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>States</h2><span className="ds-note">default · loading · disabled</span></div>
        <div className="ds-row">
          <SolidButton onClick={simulate} loading={saving}>{saving ? "Saving…" : "Save changes"}</SolidButton>
          <SolidButton disabled>Save changes</SolidButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>With icons</h2><span className="ds-note">leading / trailing</span></div>
        <div className="ds-row">
          <SolidButton iconLeft={<Icon name="plus" className="shrink-0" />}>New project</SolidButton>
          <SolidButton iconRight={<Icon name="arrow-right" className="shrink-0" />}>Continue</SolidButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)
# =========================================================== outline-button =
register(
    "outline-button",
    title="Outline Button",
    eyebrow="React Component",
    lede="A bordered, transparent-fill medium-emphasis action. Pairs with a SolidButton to establish primary/secondary hierarchy on a surface.",
    subcategory="Secondary",
    tags=["button", "react", "tailwind", "secondary", "outline", "action", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["solid-button", "secondary-button", "ghost-button"],
    extra=["solid-button"],
    props_doc={
        "usage": "<OutlineButton onClick={cancel}>Cancel</OutlineButton>",
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `size` | `ButtonSize` | `md` |\n| `block` | `boolean` | `false` |\n| `loading` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` / `iconRight` | `ReactNode` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="Single outline variant: transparent fill, `border-strong`, hover lifts to `surface-hover`. See SolidButton/SecondaryButton/GhostButton for the other emphasis levels.",
    sizes_doc=SIZES_DOC,
    states_doc=STATES_STD,
    a11y_doc=A11Y_NATIVE,
    notes_doc="Use as the cancel/secondary action beside a SolidButton. The visible border keeps it a clear affordance without competing with the primary fill.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — OutlineButton
 * Bordered, transparent-fill medium-emphasis action. Transparent fill lifts
 * to color.surface-hover on hover; border uses color.border-strong.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface OutlineButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  size?: ButtonSize;
  block?: boolean;
  loading?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
}}

{CX}

{SPINNER}

{SIZES_TS}

export function OutlineButton({{
  children,
  size = "md",
  block = false,
  loading = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}}: OutlineButtonProps) {{
  const isDisabled = disabled || loading;
  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        "{V_OUTLINE}",
        SIZES[size],
        block && "w-full",
        className,
      )}}
      disabled={{isDisabled}}
      aria-busy={{loading || undefined}}
      {{...rest}}
    >
      {{loading ? <Spinner /> : iconLeft}}
      <span>{{children}}</span>
      {{!loading && iconRight}}
    </button>
  );
}}

export default OutlineButton;
''',
    showcase=r'''function Showcase() {
  const [saving, setSaving] = React.useState(false);
  function simulate() { setSaving(true); setTimeout(() => setSaving(false), 1400); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → xl</span></div>
        <div className="ds-row">
          <OutlineButton size="xs">Filter</OutlineButton>
          <OutlineButton size="sm">Cancel</OutlineButton>
          <OutlineButton size="md">Cancel</OutlineButton>
          <OutlineButton size="lg">Continue</OutlineButton>
          <OutlineButton size="xl">Get started</OutlineButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>States</h2><span className="ds-note">default · loading · disabled</span></div>
        <div className="ds-row">
          <OutlineButton onClick={simulate} loading={saving}>{saving ? "Cancelling…" : "Cancel"}</OutlineButton>
          <OutlineButton disabled>Cancel</OutlineButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>With a primary action</h2><span className="ds-note">paired hierarchy</span></div>
        <div className="ds-row">
          <SolidButton onClick={() => {}}>Save changes</SolidButton>
          <OutlineButton onClick={() => {}}>Discard</OutlineButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ========================================================= secondary-button =
register(
    "secondary-button",
    title="Secondary Button",
    eyebrow="React Component",
    lede="A tonal secondary-surface button for frequent, lower-stakes actions — lower emphasis than solid, higher than outline or ghost. Good for repeated toolbar controls.",
    subcategory="Secondary",
    tags=["button", "react", "tailwind", "secondary", "tonal", "toolbar", "action"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["solid-button", "outline-button", "ghost-button"],
    props_doc={
        "usage": "<SecondaryButton onClick={archive}>Archive</SecondaryButton>",
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `size` | `ButtonSize` | `md` |\n| `block` | `boolean` | `false` |\n| `loading` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` / `iconRight` | `ReactNode` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="Single tonal variant: `color.secondary` fill with `color.border`, hover lifts to `surface-active`. Sits between Solid and Outline in emphasis.",
    sizes_doc=SIZES_DOC,
    states_doc=STATES_STD,
    a11y_doc=A11Y_NATIVE,
    notes_doc="Use for repeated toolbar actions (Archive, Snooze, Share) where a solid fill would over-emphasize every item.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — SecondaryButton
 * Tonal secondary surface. color.secondary fill with color.border. Lower
 * emphasis than solid, higher than outline/ghost.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface SecondaryButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  size?: ButtonSize;
  block?: boolean;
  loading?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
}}

{CX}

{SPINNER}

{SIZES_TS}

export function SecondaryButton({{
  children,
  size = "md",
  block = false,
  loading = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}}: SecondaryButtonProps) {{
  const isDisabled = disabled || loading;
  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        "{V_SECONDARY}",
        SIZES[size],
        block && "w-full",
        className,
      )}}
      disabled={{isDisabled}}
      aria-busy={{loading || undefined}}
      {{...rest}}
    >
      {{loading ? <Spinner /> : iconLeft}}
      <span>{{children}}</span>
      {{!loading && iconRight}}
    </button>
  );
}}

export default SecondaryButton;
''',
    showcase=r'''function Showcase() {
  const [busy, setBusy] = React.useState(false);
  function simulate() { setBusy(true); setTimeout(() => setBusy(false), 1400); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → xl</span></div>
        <div className="ds-row">
          <SecondaryButton size="xs">Snooze</SecondaryButton>
          <SecondaryButton size="sm">Archive</SecondaryButton>
          <SecondaryButton size="md">Archive</SecondaryButton>
          <SecondaryButton size="lg">Share</SecondaryButton>
          <SecondaryButton size="xl">Invite members</SecondaryButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>States</h2><span className="ds-note">default · loading · disabled</span></div>
        <div className="ds-row">
          <SecondaryButton onClick={simulate} loading={busy}>{busy ? "Archiving…" : "Archive"}</SecondaryButton>
          <SecondaryButton disabled>Archive</SecondaryButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Toolbar row</h2><span className="ds-note">repeated secondary actions</span></div>
        <div className="ds-row">
          <SecondaryButton size="sm" iconLeft={<Icon name="archive" className="shrink-0" />}>Archive</SecondaryButton>
          <SecondaryButton size="sm" iconLeft={<Icon name="share" className="shrink-0" />}>Share</SecondaryButton>
          <SecondaryButton size="sm" iconLeft={<Icon name="duplicate" className="shrink-0" />}>Duplicate</SecondaryButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================== ghost-button =
register(
    "ghost-button",
    title="Ghost Button",
    eyebrow="React Component",
    lede="A borderless, transparent low-emphasis button that reveals a surface only on hover. Use for tertiary or incidental actions so the primary action keeps emphasis.",
    subcategory="Secondary",
    tags=["button", "react", "tailwind", "ghost", "tertiary", "navigation", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["solid-button", "outline-button", "secondary-button"],
    props_doc={
        "usage": "<GhostButton onClick={openHelp}>Help</GhostButton>",
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `size` | `ButtonSize` | `md` |\n| `active` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` / `iconRight` | `ReactNode` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`. `active` exposes `aria-pressed` and applies `surface-active`.",
    },
    variants_doc="Single ghost variant: no border, transparent fill, hover lifts to `surface-hover`. `active` applies `surface-active` + `aria-pressed` for a pressed/selected state conveyed by more than color.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · selected (`active`) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " The `active` prop sets `aria-pressed` and a surface change so selection is conveyed by background + state, not color alone.",
    notes_doc="Reserve ghost for incidental actions. A row of ghost buttons reads as quiet toolbar chrome; a single solid button in the same row keeps the primary action obvious.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — GhostButton
 * Transparent, borderless low-emphasis action. No border, transparent fill;
 * hover lifts to color.surface-hover. `active` applies surface-active +
 * aria-pressed for a selected state.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface GhostButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  size?: ButtonSize;
  /** Pressed / selected appearance. Sets `aria-pressed`. */
  active?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
}}

{CX}

{SIZES_TS}

export function GhostButton({{
  children,
  size = "md",
  active = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}}: GhostButtonProps) {{
  return (
    <button
      type={{type}}
      aria-pressed={{active || undefined}}
      className={{cx(
        "{BASE}",
        "{V_GHOST}",
        active && "bg-[var(--ds-color-surface-active)]",
        SIZES[size],
        className,
      )}}
      disabled={{disabled}}
      {{...rest}}
    >
      {{iconLeft}}
      <span>{{children}}</span>
      {{iconRight}}
    </button>
  );
}}

export default GhostButton;
''',
    showcase=r'''function Showcase() {
  const [active, setActive] = React.useState("list");
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → xl</span></div>
        <div className="ds-row">
          <GhostButton size="xs">Help</GhostButton>
          <GhostButton size="sm">Settings</GhostButton>
          <GhostButton size="md">Open preferences</GhostButton>
          <GhostButton size="lg">Browse plans</GhostButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Active / pressed</h2><span className="ds-note">aria-pressed + surface-active</span></div>
        <div className="ds-row">
          <GhostButton active={active === "list"} onClick={() => setActive("list")} iconLeft={<Icon name="filter" className="shrink-0" />}>List view</GhostButton>
          <GhostButton active={active === "grid"} onClick={() => setActive("grid")} iconLeft={<Icon name="settings" className="shrink-0" />}>Grid view</GhostButton>
          <GhostButton active={active === "board"} onClick={() => setActive("board")} iconLeft={<Icon name="archive" className="shrink-0" />}>Board view</GhostButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Disabled</h2><span className="ds-note">reduced opacity, affordance kept</span></div>
        <div className="ds-row"><GhostButton disabled>Unavailable</GhostButton></div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================== link-button =
register(
    "link-button",
    title="Link Button",
    eyebrow="React Component",
    lede="A button rendered as an inline link for terse secondary actions inside forms and rows. Reads as a link but still triggers onClick; for true navigation, pass an href.",
    subcategory="Secondary",
    tags=["button", "react", "tailwind", "link", "inline", "navigation", "tertiary"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["ghost-button", "outline-button"],
    props_doc={
        "usage": "<LinkButton onClick={forgot}>Forgot password?</LinkButton>\n<LinkButton href=\"/help\">View all</LinkButton>",
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `href` | `string` | — (renders `<a>` when set) |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` / `iconRight` | `ReactNode` | — |\n| `type` | `button \\| submit \\| reset` | `button` (button mode) |\n\nWhen `href` is set the component renders an `<a>` (with `aria-disabled` when disabled); otherwise a `<button>`.",
    },
    variants_doc="Single link variant: `color.link` text, underline on hover, no border or fill. When `href` is provided, renders a real anchor.",
    sizes_doc="Height is auto (inline). Font inherits the surrounding text size; use it inline with body copy.",
    states_doc="default · hover (underline + `link-hover`) · focus-visible · disabled (reduced opacity + `aria-disabled`).",
    a11y_doc="Button mode renders a native `<button>`; link mode renders a native `<a href>`. Focus-visible ring uses `color.focus-ring`. Disabled links use `aria-disabled` (not `tabindex=-1`) so the affordance stays perceivable; pair with JS that ignores activation when disabled.",
    notes_doc="Use for terse inline actions (\"View all\", \"Forgot password?\", \"Add label\"). For primary navigation, prefer a real anchor or a SolidButton.",
    tsx=f'''import type {{ ButtonHTMLAttributes, AnchorHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — LinkButton
 * Button styled as an inline link. color.link text, underline on hover, no
 * border or fill. Renders an <a> when href is set, a <button> otherwise.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface LinkButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "href"> {{
  /** Render as an anchor with this URL. */
  href?: string;
  /** Disabled state (button: disabled attr; anchor: aria-disabled). */
  disabled?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
}}

{CX}

const LINK =
  "inline-flex items-center gap-1.5 rounded-[var(--ds-radius-sm)] border-0 bg-transparent " +
  "p-0 font-medium leading-none text-[var(--ds-color-link)] underline-offset-4 " +
  "transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "hover:text-[var(--ds-color-link-hover)] hover:underline " +
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] " +
  "disabled:pointer-events-none disabled:opacity-50";

export function LinkButton({{
  children,
  href,
  disabled = false,
  iconLeft,
  iconRight,
  className,
  type = "button",
  onClick,
  ...rest
}}: LinkButtonProps) {{
  const content = (
    <>
      {{iconLeft}}
      <span>{{children}}</span>
      {{iconRight}}
    </>
  );
  if (href) {{
    return (
      <a
        href={{disabled ? undefined : href}}
        className={{cx(LINK, className)}}
        aria-disabled={{disabled || undefined}}
        onClick={{disabled ? (e: React.MouseEvent) => e.preventDefault() : onClick}}
        {{...rest}}
      >
        {{content}}
      </a>
    );
  }}
  return (
    <button
      type={{type}}
      className={{cx(LINK, className)}}
      disabled={{disabled}}
      onClick={{onClick}}
      {{...rest}}
    >
      {{content}}
    </button>
  );
}}

export default LinkButton;
''',
    showcase=r'''function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Inline in a row</h2><span className="ds-note">tertiary actions</span></div>
        <div className="ds-row">
          <LinkButton href="/docs">Read the docs</LinkButton>
          <LinkButton onClick={() => {}}>Forgot password?</LinkButton>
          <LinkButton href="/changelog">View changelog</LinkButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>With icons</h2><span className="ds-note">leading / trailing</span></div>
        <div className="ds-row">
          <LinkButton href="/pricing" iconRight={<Icon name="external" className="shrink-0" />}>See pricing</LinkButton>
          <LinkButton href="/settings" iconLeft={<Icon name="settings" className="shrink-0" />}>Account settings</LinkButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>States</h2><span className="ds-note">disabled</span></div>
        <div className="ds-row"><LinkButton href="/invite" disabled>Invite expired</LinkButton></div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ======================================================= destructive-button =
register(
    "destructive-button",
    title="Destructive Button",
    eyebrow="React Component",
    lede="A destructive action for irreversible operations. Filled by default; an outline variant is available for lower-emphasis destructive controls in dense rows.",
    subcategory="Primary",
    tags=["button", "react", "tailwind", "destructive", "danger", "delete", "action", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["solid-button", "outline-button"],
    extra=["ghost-button"],
    props_doc={
        "usage": '<DestructiveButton onClick={confirmDelete}>Delete project</DestructiveButton>\n<DestructiveButton variant="outline">Remove</DestructiveButton>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `variant` | `solid \\| outline` | `solid` |\n| `size` | `ButtonSize` | `md` |\n| `block` | `boolean` | `false` |\n| `loading` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` | `ReactNode` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="`solid` (default): filled `color.destructive` / `color.destructive-foreground`. `outline`: transparent fill, destructive text + border, hover lifts to `destructive-soft`.",
    sizes_doc=SIZES_DOC,
    states_doc=STATES_STD,
    a11y_doc=A11Y_NATIVE + " Always provide a confirming context (a dialog or an adjacent non-destructive Cancel) — destructive color signals intent but is never the only confirmation.",
    notes_doc="Reserve for irreversible actions. Pair with a confirmation step and a non-destructive escape. Don't use destructive styling for routine destructive-looking actions like \"Remove from list\".",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — DestructiveButton
 * Destructive action. `solid` (filled color.destructive) or `outline`
 * (transparent + destructive text/border, hover -> destructive-soft).
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type DestructiveVariant = "solid" | "outline";

export interface DestructiveButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  variant?: DestructiveVariant;
  size?: ButtonSize;
  block?: boolean;
  loading?: boolean;
  iconLeft?: ReactNode;
}}

{CX}

{SPINNER}

{SIZES_TS}

const VARIANTS: Record<DestructiveVariant, string> = {{
  solid: "{V_DESTRUCTIVE}",
  outline: "{V_DESTRUCTIVE_OUTLINE}",
}};

export function DestructiveButton({{
  children,
  variant = "solid",
  size = "md",
  block = false,
  loading = false,
  disabled,
  iconLeft,
  className,
  type = "button",
  ...rest
}}: DestructiveButtonProps) {{
  const isDisabled = disabled || loading;
  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        SIZES[size],
        block && "w-full",
        className,
      )}}
      disabled={{isDisabled}}
      aria-busy={{loading || undefined}}
      {{...rest}}
    >
      {{loading ? <Spinner /> : iconLeft}}
      <span>{{children}}</span>
    </button>
  );
}}

export default DestructiveButton;
''',
    showcase=r'''function Showcase() {
  const [busy, setBusy] = React.useState(false);
  function simulate() { setBusy(true); setTimeout(() => setBusy(false), 1500); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">solid · outline</span></div>
        <div className="ds-row">
          <DestructiveButton onClick={simulate} loading={busy} iconLeft={<Icon name="trash" className="shrink-0" />}>{busy ? "Deleting…" : "Delete project"}</DestructiveButton>
          <DestructiveButton variant="outline" iconLeft={<Icon name="trash" className="shrink-0" />}>Remove</DestructiveButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">outline, sm → xl</span></div>
        <div className="ds-row">
          <DestructiveButton variant="outline" size="sm">Remove</DestructiveButton>
          <DestructiveButton variant="outline" size="md">Remove member</DestructiveButton>
          <DestructiveButton variant="outline" size="lg">Revoke access</DestructiveButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Confirmation row</h2><span className="ds-note">pair with a non-destructive cancel</span></div>
        <div className="ds-row">
          <DestructiveButton block={false}>Delete permanently</DestructiveButton>
          <GhostButton onClick={() => {}}>Cancel</GhostButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# =========================================================== success-button =
register(
    "success-button",
    title="Success Button",
    eyebrow="React Component",
    lede="A positive-emphasis action for confirm, publish, approve, and complete flows. Contextual only — not a replacement for the primary action.",
    subcategory="Feedback",
    tags=["button", "react", "tailwind", "success", "confirm", "approve", "publish", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["solid-button", "loading-button"],
    props_doc={
        "usage": '<SuccessButton onClick={publish}>Publish</SuccessButton>\n<SuccessButton done>Approved</SuccessButton>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `size` | `ButtonSize` | `md` |\n| `block` | `boolean` | `false` |\n| `loading` | `boolean` | `false` |\n| `done` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` / `iconRight` | `ReactNode` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="Single filled variant built on `color.success` / `color.success-foreground`. `done` swaps the leading icon for a check for transient completion feedback.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · loading (spinner + `aria-busy`) · `done` (check icon) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " The `done` state is a visual confirmation; convey the same outcome to assistive tech via a live region on the owning surface.",
    notes_doc="Contextual only — confirm/approve/publish/complete. Don't use success styling for the main save action; that's the SolidButton's job.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — SuccessButton
 * Filled positive action. color.success / color.success-foreground. `done`
 * swaps the leading icon for a check for transient completion feedback.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface SuccessButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  size?: ButtonSize;
  block?: boolean;
  loading?: boolean;
  /** Show a check icon to signal completion. */
  done?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
}}

{CX}

{SPINNER}

function CheckIcon() {{
  return (
    <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}}

{SIZES_TS}

export function SuccessButton({{
  children,
  size = "md",
  block = false,
  loading = false,
  done = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}}: SuccessButtonProps) {{
  const isDisabled = disabled || loading;
  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        "{V_SUCCESS}",
        SIZES[size],
        block && "w-full",
        className,
      )}}
      disabled={{isDisabled}}
      aria-busy={{loading || undefined}}
      {{...rest}}
    >
      {{loading ? <Spinner /> : done ? <CheckIcon /> : iconLeft}}
      <span>{{children}}</span>
      {{!loading && !done && iconRight}}
    </button>
  );
}}

export default SuccessButton;
''',
    showcase=r'''function Showcase() {
  const [busy, setBusy] = React.useState(false);
  const [done, setDone] = React.useState(false);
  function simulate() {
    setBusy(true); setDone(false);
    setTimeout(() => { setBusy(false); setDone(true); setTimeout(() => setDone(false), 1800); }, 1400);
  }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → xl</span></div>
        <div className="ds-row">
          <SuccessButton size="xs">Approve</SuccessButton>
          <SuccessButton size="sm">Publish</SuccessButton>
          <SuccessButton size="md">Publish changes</SuccessButton>
          <SuccessButton size="lg">Approve request</SuccessButton>
          <SuccessButton size="xl">Launch site</SuccessButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>States</h2><span className="ds-note">loading → done</span></div>
        <div className="ds-row">
          <SuccessButton onClick={simulate} loading={busy} done={done}>{done ? "Approved" : "Approve"}</SuccessButton>
          <SuccessButton disabled>Approve</SuccessButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================= icon-button ===
register(
    "icon-button",
    title="Icon Button",
    eyebrow="React Component",
    lede="A square icon-only control. No visible label, so an accessible name is required. Matches control height; the icon slot is square (width equals height).",
    subcategory="Utility",
    tags=["button", "react", "tailwind", "icon", "toolbar", "utility", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["ghost-button", "close-button", "more-actions-button"],
    props_doc={
        "usage": '<IconButton icon={<Trash className="shrink-0" />} label="Delete row" />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `icon` | `ReactNode` | — (required) |\n| `label` | `string` | — (required: accessible name) |\n| `variant` | `ghost \\| outline \\| secondary \\| solid` | `ghost` |\n| `size` | `ButtonSize` | `md` |\n| `active` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`. `label` is always rendered as `aria-label`.",
    },
    variants_doc="ghost (default) · outline · secondary · solid. Same emphasis semantics as the labeled variants.",
    sizes_doc=SIZES_DOC + " Icon-only: the button is square (`w` == `h`); padding is removed.",
    states_doc="default · hover · active · focus-visible · selected (`active` → `aria-pressed` + `surface-active`) · disabled (reduced opacity).",
    a11y_doc="**Icon-only buttons must have an accessible name.** `label` is required and renders as `aria-label`. Renders a native `<button>`; focus-visible ring uses `color.focus-ring`. Meets 44px touch target at lg/xl. Never omit `label` — a button with no text and no aria-label is unnamed to screen readers.",
    notes_doc="Use where a label would be redundant given surrounding context (toolbar, card header, table row). When space allows, prefer a labeled button — it's more discoverable.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — IconButton
 * Square icon-only control. `label` is required for an accessible name
 * (rendered as aria-label). Maintains the size token's height; the --icon
 * modifier makes the button square.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type IconButtonVariant = "ghost" | "outline" | "secondary" | "solid";

export interface IconButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  /** Icon node (rendered at the size token for the chosen button size). */
  icon: ReactNode;
  /** Required accessible name (rendered as aria-label). */
  label: string;
  variant?: IconButtonVariant;
  size?: ButtonSize;
  /** Pressed / selected state. Sets aria-pressed. */
  active?: boolean;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<IconButtonVariant, string> = {{
  ghost: "{V_GHOST}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  solid: "{V_SOLID}",
}};

const ICON_ONLY: Record<ButtonSize, string> = {{
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
}};

export function IconButton({{
  icon,
  label,
  variant = "ghost",
  size = "md",
  active = false,
  disabled,
  className,
  type = "button",
  ...rest
}}: IconButtonProps) {{
  return (
    <button
      type={{type}}
      aria-label={{label}}
      aria-pressed={{active || undefined}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        active && "bg-[var(--ds-color-surface-active)]",
        ICON_ONLY[size],
        className,
      )}}
      disabled={{disabled}}
      {{...rest}}
    >
      {{icon}}
    </button>
  );
}}

export default IconButton;
''',
    showcase=r'''function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">ghost · outline · secondary · solid</span></div>
        <div className="ds-row">
          <IconButton icon={<Icon name="settings" />} label="Open settings" variant="ghost" />
          <IconButton icon={<Icon name="edit" />} label="Edit row" variant="outline" />
          <IconButton icon={<Icon name="archive" />} label="Archive" variant="secondary" />
          <IconButton icon={<Icon name="plus" />} label="Add item" variant="solid" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → xl, ghost</span></div>
        <div className="ds-row">
          <IconButton icon={<Icon name="bell" />} label="Notifications" size="sm" />
          <IconButton icon={<Icon name="bell" />} label="Notifications" size="md" />
          <IconButton icon={<Icon name="bell" />} label="Notifications" size="lg" />
          <IconButton icon={<Icon name="bell" />} label="Notifications" size="xl" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>States</h2><span className="ds-note">active · disabled</span></div>
        <div className="ds-row">
          <IconButton icon={<Icon name="pin" />} label="Pin, pressed" active />
          <IconButton icon={<Icon name="save" />} label="Save" disabled />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# =========================================================== loading-button =
register(
    "loading-button",
    title="Loading Button",
    eyebrow="React Component",
    lede="An action button with a first-class loading state. `loading` swaps the leading slot for a spinner, sets `aria-busy`, and disables the button so the action can't be double-fired.",
    subcategory="Feedback",
    tags=["button", "react", "tailwind", "loading", "spinner", "async", "feedback", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["solid-button", "refresh-button", "download-button"],
    props_doc={
        "usage": '<LoadingButton onClick={save} loading={saving}>{saving ? "Saving…" : "Save"}</LoadingButton>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `variant` | `solid \\| outline \\| secondary \\| destructive \\| success` | `solid` |\n| `size` | `ButtonSize` | `md` |\n| `block` | `boolean` | `false` |\n| `loading` | `boolean` | `false` |\n| `loadingLabel` | `ReactNode` | — (overrides children while loading) |\n| `iconLeft` | `ReactNode` | — |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="solid (default) · outline · secondary · destructive · success. Same token-faithful appearance as the standalone variant buttons.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · loading (spinner + `aria-busy`, disabled, layout preserved) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " Layout is preserved because the spinner occupies the same leading slot as the icon, so the label doesn't shift while pending.",
    notes_doc="The label may change during loading (via `loadingLabel` or by swapping `children`). The spinner occupies the icon slot so the button keeps its width and the label doesn't jump.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — LoadingButton
 * Action button with a first-class loading state. `loading` swaps the
 * leading slot for a spinner, sets aria-busy, and disables the button so
 * the action can't be double-fired. Layout is preserved (spinner occupies
 * the icon slot).
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type LoadingVariant = "solid" | "outline" | "secondary" | "destructive" | "success";

export interface LoadingButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  variant?: LoadingVariant;
  size?: ButtonSize;
  block?: boolean;
  loading?: boolean;
  /** Label shown while loading (defaults to children). */
  loadingLabel?: ReactNode;
  iconLeft?: ReactNode;
}}

{CX}

{SPINNER}

{SIZES_TS}

const VARIANTS: Record<LoadingVariant, string> = {{
  solid: "{V_SOLID}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  destructive: "{V_DESTRUCTIVE}",
  success: "{V_SUCCESS}",
}};

export function LoadingButton({{
  children,
  variant = "solid",
  size = "md",
  block = false,
  loading = false,
  loadingLabel,
  iconLeft,
  disabled,
  className,
  type = "button",
  ...rest
}}: LoadingButtonProps) {{
  const isDisabled = disabled || loading;
  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        SIZES[size],
        block && "w-full",
        className,
      )}}
      disabled={{isDisabled}}
      aria-busy={{loading || undefined}}
      {{...rest}}
    >
      {{loading ? <Spinner /> : iconLeft}}
      <span>{{loading && loadingLabel !== undefined ? loadingLabel : children}}</span>
    </button>
  );
}}

export default LoadingButton;
''',
    showcase=r'''function Showcase() {
  const [busy, setBusy] = React.useState(null);
  function run(v) { setBusy(v); setTimeout(() => setBusy(null), 1500); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">click to load</span></div>
        <div className="ds-row">
          <LoadingButton variant="solid" loading={busy === "save"} onClick={() => run("save")}>{busy === "save" ? "Saving…" : "Save"}</LoadingButton>
          <LoadingButton variant="outline" loading={busy === "sync"} onClick={() => run("sync")} loadingLabel="Syncing…">Sync</LoadingButton>
          <LoadingButton variant="destructive" loading={busy === "del"} onClick={() => run("del")} loadingLabel="Deleting…" iconLeft={<Icon name="trash" className="shrink-0" />}>Delete</LoadingButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → xl, solid</span></div>
        <div className="ds-row">
          <LoadingButton size="xs" loading>Working</LoadingButton>
          <LoadingButton size="sm" loading>Syncing</LoadingButton>
          <LoadingButton size="md" loading>Saving changes</LoadingButton>
          <LoadingButton size="lg" loading>Processing</LoadingButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Block</h2><span className="ds-note">full-width submit</span></div>
        <div className="ds-stack">
          <LoadingButton block loading>Submitting order…</LoadingButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)

# ======================================================= button-with-icon ===
register(
    "button-with-icon",
    title="Button With Icon",
    eyebrow="React Component",
    lede="A labeled button with a leading or trailing icon. Icons use the shared size token for the chosen button size, with the standard control gap keeping icon and label optically aligned.",
    subcategory="Composite",
    tags=["button", "react", "tailwind", "icon", "action", "composite", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["solid-button", "button-with-chevron", "icon-button"],
    props_doc={
        "usage": '<ButtonWithIcon icon="download" iconPosition="trailing">Export</ButtonWithIcon>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `icon` | `string` (icon name) | — |\n| `iconPosition` | `leading \\| trailing` | `leading` |\n| `variant` | `solid \\| outline \\| secondary \\| ghost` | `solid` |\n| `size` | `ButtonSize` | `md` |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`. Provide your own icon set; this component renders an `<Icon name>` helper slot — see Notes.",
    },
    variants_doc="solid (default) · outline · secondary · ghost.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " Decorative icons are marked `aria-hidden`; the label provides the accessible name.",
    notes_doc="The shipped `icon` prop accepts an icon name string rendered by a small inline `Icon` helper (drop in your own). To use a custom icon node, pass `iconLeft`/`iconRight` to SolidButton/OutlineButton/etc. instead.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — ButtonWithIcon
 * Labeled button with a leading/trailing icon. Icons use the shared size
 * token for the chosen button size; the 8px control gap keeps icon and
 * label optically aligned.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type WithIconVariant = "solid" | "outline" | "secondary" | "ghost";
export type IconPosition = "leading" | "trailing";

export interface ButtonWithIconProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  /** Icon name (rendered by the inline Icon helper). */
  icon?: string;
  iconPosition?: IconPosition;
  variant?: WithIconVariant;
  size?: ButtonSize;
  /** Override the leading slot with a custom icon node. */
  iconLeft?: ReactNode;
  /** Override the trailing slot with a custom icon node. */
  iconRight?: ReactNode;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<WithIconVariant, string> = {{
  solid: "{V_SOLID}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  ghost: "{V_GHOST}",
}};

function Icon({{ name, className }}: {{ name?: string; className?: string }}) {{
  if (!name) return null;
  // Minimal stroke icon set used by the preview. In a real project, import
  // your icon library here; the component only needs an SVG node.
  const common = {{ width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" }} as const;
  const paths: Record<string, ReactNode> = {{
    "download": <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />,
    "arrow-right": <><path d="M5 12h14" /><path d="m13 5 7 7-7 7" /></>,
    "plus": <><path d="M12 5v14" /><path d="M5 12h14" /></>,
    "save": <><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" /><path d="M17 21v-8H7v8" /><path d="M7 3v5h8" /></>,
  }};
  return <svg {{...common}}>{{paths[name]}}</svg>;
}}

export function ButtonWithIcon({{
  children,
  icon,
  iconPosition = "leading",
  variant = "solid",
  size = "md",
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}}: ButtonWithIconProps) {{
  const leading = iconPosition === "leading" ? (iconLeft ?? (icon ? <Icon name={{icon}} className="shrink-0" /> : null)) : iconLeft;
  const trailing = iconPosition === "trailing" ? (iconRight ?? (icon ? <Icon name={{icon}} className="shrink-0" /> : null)) : iconRight;
  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        SIZES[size],
        className,
      )}}
      disabled={{disabled}}
      {{...rest}}
    >
      {{leading}}
      <span>{{children}}</span>
      {{trailing}}
    </button>
  );
}}

export default ButtonWithIcon;
''',
    showcase=r'''function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Positions</h2><span className="ds-note">leading · trailing</span></div>
        <div className="ds-row">
          <ButtonWithIcon icon="download" iconPosition="leading">Export</ButtonWithIcon>
          <ButtonWithIcon icon="arrow-right" iconPosition="trailing">Continue</ButtonWithIcon>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">solid · outline · secondary · ghost</span></div>
        <div className="ds-row">
          <ButtonWithIcon icon="plus" variant="solid">New project</ButtonWithIcon>
          <ButtonWithIcon icon="download" variant="outline">Export</ButtonWithIcon>
          <ButtonWithIcon icon="save" variant="secondary">Save view</ButtonWithIcon>
          <ButtonWithIcon icon="arrow-right" variant="ghost" iconPosition="trailing">Next</ButtonWithIcon>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → xl, solid</span></div>
        <div className="ds-row">
          <ButtonWithIcon icon="plus" size="sm">Add</ButtonWithIcon>
          <ButtonWithIcon icon="plus" size="md">Add member</ButtonWithIcon>
          <ButtonWithIcon icon="plus" size="lg">Add team member</ButtonWithIcon>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ==================================================== button-with-chevron ===
register(
    "button-with-chevron",
    title="Button With Chevron",
    eyebrow="React Component",
    lede="A labeled button with a trailing chevron. `direction` controls orientation (down for menus/disclosure, right for advancing), and `open` rotates a down chevron to signal an expanded state.",
    subcategory="Composite",
    tags=["button", "react", "tailwind", "chevron", "menu", "disclosure", "composite", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["button-with-icon", "split-button", "more-actions-button"],
    props_doc={
        "usage": '<ButtonWithChevron open={open} onClick={toggle}>Sort by date</ButtonWithChevron>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `direction` | `down \\| right` | `down` |\n| `open` | `boolean` | `false` (rotates a `down` chevron 180°) |\n| `variant` | `solid \\| outline \\| secondary \\| ghost` | `outline` |\n| `size` | `ButtonSize` | `md` |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`. `aria-expanded` reflects `open` unless overridden by an `aria-expanded` prop.",
    },
    variants_doc="outline (default) · solid · secondary · ghost.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · open (chevron rotated, `aria-expanded`) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " When used as a disclosure/menu trigger, `aria-expanded` reflects `open` (pass it explicitly if you also control focus). The chevron rotation is a visual cue, not the only one — `aria-expanded` is the contract with assistive tech.",
    notes_doc="Use `direction=\"down\"` for menus and disclosure; `direction=\"right\"` for advancing/next. The chevron rotates via a `transition-transform` that respects reduced motion.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — ButtonWithChevron
 * Labeled button with a trailing chevron. `direction` controls orientation;
 * `open` rotates a down chevron 180° to signal an expanded state and sets
 * aria-expanded.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type ChevronVariant = "solid" | "outline" | "secondary" | "ghost";
export type ChevronDirection = "down" | "right";

export interface ButtonWithChevronProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  direction?: ChevronDirection;
  /** Expanded state (down chevron rotates 180°; sets aria-expanded). */
  open?: boolean;
  variant?: ChevronVariant;
  size?: ButtonSize;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<ChevronVariant, string> = {{
  solid: "{V_SOLID}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  ghost: "{V_GHOST}",
}};

function ChevronIcon({{ direction, open }}: {{ direction: ChevronDirection; open: boolean }}) {{
  const rotate = direction === "down" && open ? "rotate-180" : "rotate-0";
  return (
    <svg
      className={{cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", rotate)}}
      viewBox="0 0 24 24" fill="none" aria-hidden="true"
    >
      {{direction === "down"
        ? <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        : <path d="m9 6 6 6-6 6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />}}
    </svg>
  );
}}

export function ButtonWithChevron({{
  children,
  direction = "down",
  open = false,
  variant = "outline",
  size = "md",
  disabled,
  className,
  type = "button",
  "aria-expanded": ariaExpanded,
  ...rest
}}: ButtonWithChevronProps) {{
  return (
    <button
      type={{type}}
      aria-expanded={{ariaExpanded !== undefined ? ariaExpanded : open || undefined}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        SIZES[size],
        className,
      )}}
      disabled={{disabled}}
      {{...rest}}
    >
      <span>{{children}}</span>
      <ChevronIcon direction={{direction}} open={{open}} />
    </button>
  );
}}

export default ButtonWithChevron;
''',
    showcase=r'''function Showcase() {
  const [open, setOpen] = React.useState(false);
  const [tab, setTab] = React.useState("overview");
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Disclosure trigger</h2><span className="ds-note">down, open toggles chevron</span></div>
        <div className="ds-row">
          <ButtonWithChevron open={open} onClick={() => setOpen(o => !o)} variant="outline">{open ? "Hide filters" : "Show filters"}</ButtonWithChevron>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Directions</h2><span className="ds-note">down · right</span></div>
        <div className="ds-row">
          <ButtonWithChevron direction="down">Sort by date</ButtonWithChevron>
          <ButtonWithChevron direction="right" variant="ghost">Next step</ButtonWithChevron>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">outline · solid · secondary · ghost</span></div>
        <div className="ds-row">
          <ButtonWithChevron variant="solid">Create</ButtonWithChevron>
          <ButtonWithChevron variant="outline">Options</ButtonWithChevron>
          <ButtonWithChevron variant="secondary">More</ButtonWithChevron>
          <ButtonWithChevron variant="ghost">Advanced</ButtonWithChevron>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================ split-button ===
register(
    "split-button",
    title="Split Button",
    eyebrow="React Component",
    lede="A primary action paired with an attached, keyboard-navigable menu of alternatives. The leading button fires the default action; the chevron opens a menu. A shared border and negative margin keep it one composite control.",
    subcategory="Composite",
    tags=["button", "react", "tailwind", "split", "menu", "composite", "interactive", "action"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["button-with-chevron", "more-actions-button", "export-button"],
    props_doc={
        "usage": '<SplitButton label="Create project" actions={[{id:"blank",label:"Blank project"},{id:"import",label:"Import"}} onAction={handle} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `label` | `ReactNode` | — |\n| `actions` | `Array<{ id: string; label: ReactNode; icon?: string; destructive?: boolean }>` | `[]` |\n| `onAction` | `(id, action) => void` | — |\n| `variant` | `solid \\| outline` | `solid` |\n| `size` | `ButtonSize` | `md` |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="solid (default) · outline. The menu is always a bordered elevated surface (`surface-elevated`, `radius-md`, `shadow-md`).",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · open (menu, `aria-expanded`) · disabled (reduced opacity).",
    a11y_doc="The chevron trigger has `aria-haspopup=\"menu\"` + `aria-expanded`. The menu uses `role=\"menu\"` and items `role=\"menuitem\"`. **Keyboard**: trigger ArrowDown/Enter/Space opens; ArrowUp/Down move between items; Enter/Space activates; Escape closes and returns focus to the trigger; outside click closes. Selecting an item sets it as the new default and fires `onAction`.",
    notes_doc="Use for action variants (one default + alternatives). Don't use for navigation. The leading button fires the last-chosen action.",
    tsx=f'''import {{ useEffect, useRef, useState }} from "react";
import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — SplitButton
 * Primary action + attached action menu. The leading button fires the
 * default (last-chosen) action; the chevron opens a keyboard-navigable
 * menu (aria-haspopup="menu", aria-expanded).
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type SplitVariant = "solid" | "outline";

export interface SplitAction {{
  id: string;
  label: ReactNode;
  icon?: string;
  destructive?: boolean;
}}

export interface SplitButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {{
  label?: ReactNode;
  actions?: SplitAction[];
  onAction?: (id: string, action: SplitAction) => void;
  variant?: SplitVariant;
  size?: ButtonSize;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<SplitVariant, string> = {{
  solid: "{V_SOLID}",
  outline: "{V_OUTLINE}",
}};

// Minimal stroke icon set; swap for your icon library in a real project.
function Icon({{ name, className }}: {{ name?: string; className?: string }}) {{
  if (!name) return null;
  const common = {{ width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" }} as const;
  const paths: Record<string, ReactNode> = {{
    "upload": <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />,
    "duplicate": <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>,
    "trash": <><path d="M3 6h18" /><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" /></>,
    "edit": <><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" /></>,
    "share": <><circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><path d="m8.6 13.5 6.8 4" /><path d="m15.4 6.5-6.8 4" /></>,
  }};
  return <svg {{...common}}>{{paths[name]}}</svg>;
}}

const MENU =
  "absolute right-0 top-[calc(100%+4px)] z-40 min-w-[180px] rounded-[var(--ds-radius-md)] " +
  "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 " +
  "shadow-[var(--ds-shadow-md)]";
const ITEM =
  "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border-0 px-2 py-1.5 " +
  "text-left font-normal text-[13px] leading-none text-[var(--ds-color-foreground)] " +
  "bg-transparent transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)] " +
  "focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)]";

function ChevronIcon({{ open }}: {{ open: boolean }}) {{
  return (
    <svg className={{cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", open ? "rotate-180" : "rotate-0")}} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}}

export function SplitButton({{
  label,
  actions = [],
  onAction,
  variant = "solid",
  size = "md",
  disabled,
  className,
  ...rest
}}: SplitButtonProps) {{
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const itemRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {{
    if (!open) return;
    function onDown(e: MouseEvent) {{
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) setOpen(false);
    }}
    function onKey(e: KeyboardEvent) {{ if (e.key === "Escape") {{ setOpen(false); triggerRef.current?.focus(); }} }}
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {{ document.removeEventListener("mousedown", onDown); document.removeEventListener("keydown", onKey); }};
  }}, [open]);

  function openMenu() {{
    setOpen(true);
    setTimeout(() => itemRefs.current[0]?.focus(), 0);
  }}
  function choose(i: number) {{
    setOpen(false);
    setActive(i);
    onAction?.(actions[i].id, actions[i]);
    triggerRef.current?.focus();
  }}
  function onTriggerKey(e: React.KeyboardEvent) {{
    if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {{ e.preventDefault(); openMenu(); }}
  }}
  function onItemKey(e: React.KeyboardEvent, i: number) {{
    const n = actions.length;
    if (e.key === "ArrowDown") {{ e.preventDefault(); itemRefs.current[(i + 1) % n]?.focus(); }}
    else if (e.key === "ArrowUp") {{ e.preventDefault(); itemRefs.current[(i - 1 + n) % n]?.focus(); }}
    else if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); choose(i); }}
  }}

  const current = actions[active];

  return (
    <div ref={{containerRef}} className="relative inline-flex">
      <button
        type="button"
        ref={{triggerRef}}
        className={{cx(
          "{BASE}",
          VARIANTS[variant],
          SIZES[size],
          "rounded-r-none border-r-0",
          className,
        )}}
        disabled={{disabled}}
        onClick={{() => onAction?.(current?.id ?? "", current ?? ({{}} as SplitAction))}}
        onKeyDown={{onTriggerKey}}
        {{...rest}}
      >
        {{current?.icon ? <Icon name={{current.icon}} /> : null}}
        <span>{{current?.label ?? label}}</span>
      </button>
      <button
        type="button"
        className={{cx(
          "{BASE}",
          VARIANTS[variant],
          SIZES[size],
          "rounded-l-none",
          "px-0 [&_svg]:size-[1em]",
        )}}
        aria-haspopup="menu"
        aria-expanded={{open}}
        aria-label="More actions"
        disabled={{disabled}}
        onClick={{() => (open ? setOpen(false) : openMenu())}}
      >
        <ChevronIcon open={{open}} />
      </button>
      {{open && (
        <div role="menu" className={{MENU}}>
          {{actions.map((a, i) => (
            <button
              key={{a.id}}
              ref={{(el) => {{ itemRefs.current[i] = el; }}}}
              role="menuitem"
              tabIndex={{-1}}
              className={{cx(ITEM, a.destructive && "text-[var(--ds-color-destructive)]")}}
              onClick={{() => choose(i)}}
              onKeyDown={{(e) => onItemKey(e, i)}}
            >
              {{a.icon ? <Icon name={{a.icon}} /> : <span className="w-[1em]" />}}
              <span className="flex-1">{{a.label}}</span>
              {{i === active && (
                <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>
              )}}
            </button>
          ))}}
        </div>
      )}}
    </div>
  );
}}

export default SplitButton;
''',
    showcase=r'''function Showcase() {
  const [log, setLog] = React.useState("—");
  const actions = [
    { id: "blank", label: "Blank project" },
    { id: "import", label: "Import from repo", icon: "upload" },
    { id: "template", label: "From template" },
    { id: "duplicate", label: "Duplicate existing", icon: "duplicate" },
  ];
  function handle(id) { setLog(`action: ${id}`); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">solid · outline · last action: {log}</span></div>
        <div className="ds-row">
          <SplitButton label="Create project" actions={actions} onAction={handle} variant="solid" />
          <SplitButton label="Create project" actions={actions} onAction={handle} variant="outline" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → lg, solid</span></div>
        <div className="ds-row">
          <SplitButton size="sm" label="Create" actions={actions} onAction={handle} />
          <SplitButton size="md" label="Create project" actions={actions} onAction={handle} />
          <SplitButton size="lg" label="Create project" actions={actions} onAction={handle} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Disabled</h2><span className="ds-note">whole control disabled</span></div>
        <div className="ds-row"><SplitButton label="Create project" actions={actions} onAction={handle} disabled /></div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# =========================================================== button-group ===
register(
    "button-group",
    title="Button Group",
    eyebrow="React Component",
    lede="A joined row of related buttons. Inner buttons share borders (side radius removed, borders overlapped by 1px) so the group reads as one control. Pass children for full control, or the `items` prop for a quick group.",
    subcategory="Composite",
    tags=["button", "react", "tailwind", "group", "composite", "toolbar", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["segmented-button", "toggle-group", "outline-button"],
    extra=["solid-button", "outline-button"],
    props_doc={
        "usage": '<ButtonGroup label="Text alignment" items={[{id:"l",label:"Left"},{id:"c",label:"Center",active:true},{id:"r",label:"Right"}}] />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `items` | `Array<{ id?: string; label: ReactNode; icon?: string; active?: boolean; onClick?: () => void }>` | — |\n| `children` | `ReactNode` | — (renders children directly when no `items`) |\n| `variant` | `outline \\| solid \\| secondary \\| ghost` | `outline` |\n| `size` | `ButtonSize` | `md` |\n| `label` | `string` | — (group `aria-label`) |\n\nPlus all native `HTMLAttributes<HTMLDivElement>`.",
    },
    variants_doc="outline (default) · solid · secondary · ghost. Children render with their own variant; `items` use the shared `variant`.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · selected (`active` → `aria-pressed` + `surface-active`) · disabled (reduced opacity on each child).",
    a11y_doc="Renders a `role=\"group\"` container with `aria-label`. Each item is a native `<button>` with `aria-pressed` when `active`. Focus-visible ring on each child.",
    notes_doc="For mutually exclusive single-choice control, prefer SegmentedButton (radiogroup semantics). ButtonGroup is a loose toolbar row.",
    tsx=f'''import type {{ HTMLAttributes, ReactNode }} from "react";

/* DevSnips React — ButtonGroup
 * Joined row of related buttons. Inner buttons lose their side radius and
 * overlap borders by 1px so the group reads as one control.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type GroupVariant = "outline" | "solid" | "secondary" | "ghost";

export interface ButtonGroupItem {{
  id?: string;
  label: ReactNode;
  icon?: string;
  active?: boolean;
  onClick?: () => void;
}}

export interface ButtonGroupProps extends HTMLAttributes<HTMLDivElement> {{
  items?: ButtonGroupItem[];
  variant?: GroupVariant;
  size?: ButtonSize;
  /** Accessible group name (rendered as aria-label). */
  label?: string;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<GroupVariant, string> = {{
  outline: "{V_OUTLINE}",
  solid: "{V_SOLID}",
  secondary: "{V_SECONDARY}",
  ghost: "{V_GHOST}",
}};

const BASE_BTN =
  "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none " +
  "transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] " +
  "disabled:pointer-events-none disabled:opacity-50";

export function ButtonGroup({{
  items,
  children,
  variant = "outline",
  size = "md",
  label,
  className,
  ...rest
}}: ButtonGroupProps) {{
  return (
    <div role="group" aria-label={{label}} className={{cx("inline-flex", className)}} {{...rest}}>
      {{items
        ? items.map((it, i) => (
            <button
              key={{it.id ?? i}}
              type="button"
              aria-pressed={{it.active || undefined}}
              onClick={{it.onClick}}
              className={{cx(
                BASE_BTN,
                VARIANTS[variant],
                SIZES[size],
                "rounded-none border-r-0",
                i === 0 ? "rounded-l-[var(--ds-radius-sm)]" : "-ml-px",
                i === items.length - 1 && "rounded-r-[var(--ds-radius-sm)] border-r",
                it.active && "bg-[var(--ds-color-surface-active)]",
              )}}
            >
              {{it.icon ? <Icon name={{it.icon}} className="shrink-0" /> : null}}
              <span>{{it.label}}</span>
            </button>
          ))
        : children}}
    </div>
  );
}}

export default ButtonGroup;
''',
    showcase=r'''function Showcase() {
  const [align, setAlign] = React.useState("left");
  const aligns = [{id:"left",label:"Left",icon:"arrow-left"},{id:"center",label:"Center"},{id:"right",label:"Right",icon:"arrow-right"}];
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">outline · solid · secondary · ghost</span></div>
        <div className="ds-row">
          <ButtonGroup label="Text align" variant="outline" items={aligns.map(a => ({...a, active: align===a.id, onClick: () => setAlign(a.id)}))} />
          <ButtonGroup label="Actions" variant="solid" items={[{id:"save",label:"Save"},{id:"d",label:"Discard"}]} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → lg, outline</span></div>
        <div className="ds-row">
          <ButtonGroup size="sm" items={aligns} />
          <ButtonGroup size="md" items={aligns} />
          <ButtonGroup size="lg" items={aligns} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>With children</h2><span className="ds-note">custom buttons</span></div>
        <div className="ds-row">
          <ButtonGroup label="View">
            <SolidButton size="sm">Save</SolidButton>
            <OutlineButton size="sm" className="rounded-l-none -ml-px">Cancel</OutlineButton>
          </ButtonGroup>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ======================================================= segmented-button ===
register(
    "segmented-button",
    title="Segmented Button",
    eyebrow="React Component",
    lede="A joined single-choice control that behaves like a radiogroup: one selected option at a time. Use for 2–5 mutually exclusive options in compact toolbars.",
    subcategory="Selection",
    tags=["button", "react", "tailwind", "segmented", "radiogroup", "selection", "toggle", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["toggle-group", "button-group"],
    props_doc={
        "usage": '<SegmentedButton label="View" value={view} onChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}}] />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `options` | `Array<{ value: string; label: ReactNode; icon?: string }>` | — |\n| `value` | `string` | — (controlled) |\n| `onChange` | `(value: string) => void` | — |\n| `size` | `ButtonSize` | `sm` |\n| `label` | `string` | — (radiogroup `aria-label`) |\n\nPlus all native `HTMLAttributes<HTMLDivElement>`.",
    },
    variants_doc="Single segmented style: bordered container, selected segment uses `surface-active` + `aria-checked=\"true\"` (radiogroup semantics).",
    sizes_doc=SIZES_DOC + " Default is `sm` for compact toolbars.",
    states_doc="default · hover · focus-visible · selected (`aria-checked`, surface-active + font-weight) · disabled (via `disabled` on individual options).",
    a11y_doc="Renders `role=\"radiogroup\"` with `aria-label`. Each segment is a `role=\"radio\"` button with `aria-checked`. **Keyboard**: ArrowLeft/Right move between segments and select (roving selection, like a native radiogroup). Each segment has a focus-visible ring.",
    notes_doc="For multi-select, use ToggleGroup. SegmentedButton is strictly single-choice. Keep to 2–5 options; for more, use a Select.",
    tsx=f'''import {{ useRef }} from "react";
import type {{ HTMLAttributes, ReactNode, KeyboardEvent }} from "react";

/* DevSnips React — SegmentedButton
 * Joined single-choice control (radiogroup semantics). One selected option
 * at a time. ArrowLeft/Right rove selection and focus.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface SegmentedOption {{
  value: string;
  label: ReactNode;
  icon?: string;
  disabled?: boolean;
}}

export interface SegmentedButtonProps extends HTMLAttributes<HTMLDivElement> {{
  options: SegmentedOption[];
  value: string;
  onChange: (value: string) => void;
  size?: ButtonSize;
  label?: string;
}}

{CX}

{SIZES_TS}

const SEG_BASE =
  "inline-flex items-center justify-center gap-2 border-0 bg-transparent px-3 font-medium leading-none " +
  "transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)] " +
  "disabled:pointer-events-none disabled:opacity-50";

export function SegmentedButton({{
  options,
  value,
  onChange,
  size = "sm",
  label,
  className,
  ...rest
}}: SegmentedButtonProps) {{
  const refs = useRef<Array<HTMLButtonElement | null>>([]);
  const height = SIZES[size];

  function onKey(e: KeyboardEvent<HTMLButtonElement>, i: number) {{
    const n = options.length;
    let next = -1;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") next = (i + 1) % n;
    else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = (i - 1 + n) % n;
    if (next >= 0) {{
      e.preventDefault();
      const opt = options[next];
      if (!opt.disabled) {{
        onChange(opt.value);
        refs.current[next]?.focus();
      }}
    }}
  }}

  return (
    <div role="radiogroup" aria-label={{label}} className={{cx("inline-flex overflow-hidden rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)]", className)}} {{...rest}}>
      {{options.map((opt, i) => {{
        const selected = opt.value === value;
        return (
          <button
            key={{opt.value}}
            ref={{(el) => {{ refs.current[i] = el; }}}}
            type="button"
            role="radio"
            aria-checked={{selected}}
            disabled={{opt.disabled}}
            onClick={{() => onChange(opt.value)}}
            onKeyDown={{(e) => onKey(e, i)}}
            className={{cx(
              SEG_BASE,
              height,
              "rounded-none",
              i > 0 && "-ml-px border-l border-[var(--ds-color-border)]",
              selected ? "bg-[var(--ds-color-surface-active)] font-semibold" : "hover:bg-[var(--ds-color-surface-hover)]",
            )}}
          >
            {{opt.icon ? <Icon name={{opt.icon}} className="shrink-0" /> : null}}
            <span>{{opt.label}}</span>
          </button>
        );
      }})}}
    </div>
  );
}}

export default SegmentedButton;
''',
    showcase=r'''function Showcase() {
  const [view, setView] = React.useState("list");
  const [range, setRange] = React.useState("week");
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Single choice</h2><span className="ds-note">radiogroup semantics</span></div>
        <div className="ds-row">
          <SegmentedButton label="View" value={view} onChange={setView} options={[{value:"list",label:"List",icon:"filter"},{value:"grid",label:"Grid"},{value:"board",label:"Board"}]} />
          <SegmentedButton label="Time range" value={range} onChange={setRange} options={[{value:"day",label:"Day"},{value:"week",label:"Week"},{value:"month",label:"Month"},{value:"year",label:"Year"}]} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → lg</span></div>
        <div className="ds-row">
          <SegmentedButton size="xs" value={view} onChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}]} />
          <SegmentedButton size="sm" value={view} onChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}]} />
          <SegmentedButton size="md" value={view} onChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}]} />
          <SegmentedButton size="lg" value={view} onChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}]} />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)

# ============================================================ toggle-button =
register(
    "toggle-button",
    title="Toggle Button",
    eyebrow="React Component",
    lede="A single binary switch. Controlled via `pressed`, or uncontrolled via `defaultPressed`. Exposes `aria-pressed` and swaps to `surface-active` when on so the state is conveyed by more than color alone.",
    subcategory="Selection",
    tags=["button", "react", "tailwind", "toggle", "aria-pressed", "selection", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["toggle-group", "segmented-button", "ghost-button"],
    props_doc={
        "usage": '<ToggleButton pressed={on} onToggle={setOn}>Pinned</ToggleButton>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `pressed` | `boolean` | — (controlled; if omitted, uncontrolled) |\n| `defaultPressed` | `boolean` | `false` (uncontrolled initial) |\n| `onToggle` | `(pressed: boolean) => void` | — |\n| `label` | `string` | — (visible + accessible name when `showLabel`) |\n| `iconOff` / `iconOn` | `string` | — (icon name per state) |\n| `variant` | `ghost \\| outline \\| secondary` | `ghost` |\n| `size` | `ButtonSize` | `md` |\n| `showLabel` | `boolean` | `true` (icon-only when false; `label` becomes `aria-label`) |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="ghost (default) · outline · secondary.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · focus-visible · **pressed/on** (`aria-pressed=\"true\"` + `surface-active` + font-weight) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " `aria-pressed` reflects the pressed state and the surface changes so on/off is conveyed by background + state, not color alone. Icon-only toggles use `label` as `aria-label`.",
    notes_doc="For a joined set of toggles (single- or multi-select), use ToggleGroup. A standalone ToggleButton is one binary switch.",
    tsx=f'''import {{ useState }} from "react";
import type {{ ButtonHTMLAttributes }} from "react";

/* DevSnips React — ToggleButton
 * Single binary switch. Controlled (pressed) or uncontrolled
 * (defaultPressed). Exposes aria-pressed and swaps to surface-active when on.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type ToggleVariant = "ghost" | "outline" | "secondary";

export interface ToggleButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "value"> {{
  pressed?: boolean;
  defaultPressed?: boolean;
  onToggle?: (pressed: boolean) => void;
  label: string;
  iconOff?: string;
  iconOn?: string;
  variant?: ToggleVariant;
  size?: ButtonSize;
  showLabel?: boolean;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<ToggleVariant, string> = {{
  ghost: "{V_GHOST}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
}};

const ICON_ONLY: Record<ButtonSize, string> = {{
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
}};

function Icon({{ name, className }}: {{ name?: string; className?: string }}) {{
  if (!name) return null;
  const common = {{ width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" }} as const;
  const paths: Record<string, React.ReactNode> = {{
    "pin": <path d="M12 17v5" />,
    "bell": <><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" /></>,
    "star": <path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />,
    "bookmark": <path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z" />,
  }};
  return <svg {{...common}}>{{paths[name]}}</svg>;
}}

export function ToggleButton({{
  pressed: pressedProp,
  defaultPressed = false,
  onToggle,
  label,
  iconOff,
  iconOn,
  variant = "ghost",
  size = "md",
  showLabel = true,
  disabled,
  className,
  type = "button",
  ...rest
}}: ToggleButtonProps) {{
  const [internal, setInternal] = useState(defaultPressed);
  const isControlled = pressedProp !== undefined;
  const value = isControlled ? pressedProp : internal;
  function click() {{
    const next = !value;
    if (!isControlled) setInternal(next);
    onToggle?.(next);
  }}
  return (
    <button
      type={{type}}
      aria-pressed={{value}}
      aria-label={{showLabel ? undefined : label}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        value && "bg-[var(--ds-color-surface-active)] font-semibold",
        showLabel ? SIZES[size] : ICON_ONLY[size],
        className,
      )}}
      disabled={{disabled}}
      onClick={{click}}
      {{...rest}}
    >
      <Icon name={{value ? (iconOn ?? iconOff) : iconOff}} className="shrink-0" />
      {{showLabel && <span>{{label}}</span>}}
    </button>
  );
}}

export default ToggleButton;
''',
    showcase=r'''function Showcase() {
  const [pinned, setPinned] = React.useState(false);
  const [starred, setStarred] = React.useState(true);
  const [mute, setMute] = React.useState(false);
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Controlled</h2><span className="ds-note">aria-pressed</span></div>
        <div className="ds-row">
          <ToggleButton pressed={pinned} onToggle={setPinned} label="Pinned" iconOff="pin" iconOn="pin" />
          <ToggleButton pressed={starred} onToggle={setStarred} label="Starred" iconOff="star" iconOn="star" variant="outline" />
          <ToggleButton pressed={mute} onToggle={setMute} label="Muted" iconOff="bell" iconOn="bell" variant="secondary" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Icon-only</h2><span className="ds-note">label becomes aria-label</span></div>
        <div className="ds-row">
          <ToggleButton pressed={pinned} onToggle={setPinned} label="Pin issue" iconOff="pin" iconOn="pin" showLabel={false} />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================= toggle-group =
register(
    "toggle-group",
    title="Toggle Group",
    eyebrow="React Component",
    lede="A joined set of toggles. `type=\"single\"` behaves like a radiogroup (one on); `type=\"multiple\"` like a group of checkboxes. Selected segments use `surface-active` + `aria-pressed`, with arrow-key roving.",
    subcategory="Selection",
    tags=["button", "react", "tailwind", "toggle-group", "selection", "multi-select", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["toggle-button", "segmented-button", "button-group"],
    props_doc={
        "usage": '<ToggleGroup type="single" value={view} onValueChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}}] />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `options` | `Array<{ value: string; label: ReactNode; icon?: string; disabled?: boolean }>` | — |\n| `type` | `single \\| multiple` | `single` |\n| `value` | `string` (single) \\| `string[]` (multiple) | — (controlled) |\n| `defaultValue` | same shape as `value` | — (uncontrolled initial) |\n| `onValueChange` | `(value: string \\| null) \\| (string[]) => void` | — |\n| `size` | `ButtonSize` | `sm` |\n| `label` | `string` | — (group `aria-label`) |\n\nPlus all native `HTMLAttributes<HTMLDivElement>`.",
    },
    variants_doc="Single bordered container. Selected segments use `surface-active` + `aria-pressed=\"true\"`. Unselected are transparent; hover lifts to `surface-hover`.",
    sizes_doc=SIZES_DOC + " Default is `sm` for compact toolbars.",
    states_doc="default · hover · focus-visible · pressed (`aria-pressed`, surface-active + font-weight) · disabled (per option).",
    a11y_doc="Renders `role=\"group\"` with `aria-label`. Each segment is a native `<button>` with `aria-pressed`. **Keyboard**: ArrowLeft/Right move focus (roving); Space/Enter toggles. Single-select toggles behave like a radiogroup but expose `aria-pressed` (one true at a time).",
    notes_doc="For strictly single-choice radiogroup semantics, prefer SegmentedButton. ToggleGroup is for flexible single- or multi-select toggle sets.",
    tsx=f'''import {{ useRef, useState }} from "react";
import type {{ HTMLAttributes, ReactNode, KeyboardEvent }} from "react";

/* DevSnips React — ToggleGroup
 * Joined toggles, single or multi select. Selected segments use
 * surface-active + aria-pressed. Arrow keys rove focus.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type ToggleGroupType = "single" | "multiple";

export interface ToggleOption {{
  value: string;
  label: ReactNode;
  icon?: string;
  disabled?: boolean;
}}

export interface ToggleGroupProps extends HTMLAttributes<HTMLDivElement> {{
  options: ToggleOption[];
  type?: ToggleGroupType;
  value?: string | string[];
  defaultValue?: string | string[];
  onValueChange?: (value: string | null | string[]) => void;
  size?: ButtonSize;
  label?: string;
}}

{CX}

{SIZES_TS}

const SEG_BASE =
  "inline-flex items-center justify-center gap-2 border-0 bg-transparent px-3 font-medium leading-none " +
  "transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)] " +
  "disabled:pointer-events-none disabled:opacity-50";

export function ToggleGroup({{
  options,
  type = "single",
  value,
  defaultValue,
  onValueChange,
  size = "sm",
  label,
  className,
  ...rest
}}: ToggleGroupProps) {{
  const initialArr = defaultValue
    ? (Array.isArray(defaultValue) ? defaultValue : [defaultValue])
    : [];
  const [internal, setInternal] = useState<string[]>(initialArr);
  const isControlled = value !== undefined;
  const ctrlArr = Array.isArray(value) ? value : value ? [value] : [];
  const current = isControlled ? ctrlArr : internal;
  const refs = useRef<Array<HTMLButtonElement | null>>([]);

  function isActive(v: string) {{ return current.indexOf(v) !== -1; }}
  function toggle(v: string) {{
    let next: string[];
    if (type === "single") next = isActive(v) ? [] : [v];
    else next = isActive(v) ? current.filter((x) => x !== v) : [...current, v];
    if (!isControlled) setInternal(next);
    onValueChange?.(type === "single" ? next[0] ?? null : next);
  }}
  function onKey(e: KeyboardEvent<HTMLButtonElement>, i: number) {{
    const n = options.length;
    let next = -1;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") next = (i + 1) % n;
    else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = (i - 1 + n) % n;
    if (next >= 0) {{ e.preventDefault(); refs.current[next]?.focus(); }}
  }}

  return (
    <div role="group" aria-label={{label}} className={{cx("inline-flex overflow-hidden rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)]", className)}} {{...rest}}>
      {{options.map((opt, i) => {{
        const on = isActive(opt.value);
        return (
          <button
            key={{opt.value}}
            ref={{(el) => {{ refs.current[i] = el; }}}}
            type="button"
            aria-pressed={{on}}
            disabled={{opt.disabled}}
            onClick={{() => toggle(opt.value)}}
            onKeyDown={{(e) => onKey(e, i)}}
            className={{cx(
              SEG_BASE,
              SIZES[size],
              "rounded-none",
              i > 0 && "-ml-px border-l border-[var(--ds-color-border)]",
              on ? "bg-[var(--ds-color-surface-active)] font-semibold" : "hover:bg-[var(--ds-color-surface-hover)]",
            )}}
          >
            {{opt.icon ? <Icon name={{opt.icon}} className="shrink-0" /> : null}}
            <span>{{opt.label}}</span>
          </button>
        );
      }})}}
    </div>
  );
}}

export default ToggleGroup;
''',
    showcase=r'''function Showcase() {
  const [view, setView] = React.useState("list");
  const [tags, setTags] = React.useState(["frontend"]);
  const tagOpts = [{value:"frontend",label:"Frontend"},{value:"backend",label:"Backend"},{value:"design",label:"Design"},{value:"ops",label:"Ops"}];
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Single select</h2><span className="ds-note">one on at a time</span></div>
        <div className="ds-row">
          <ToggleGroup type="single" label="View" value={view} onValueChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"},{value:"board",label:"Board"}]} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Multiple select</h2><span className="ds-note">any combination</span></div>
        <div className="ds-row">
          <ToggleGroup type="multiple" label="Tags" value={tags} onValueChange={(v) => setTags(v)} options={tagOpts} />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================= close-button =
register(
    "close-button",
    title="Close Button",
    eyebrow="React Component",
    lede="A dismiss control for overlays. Icon-only (X), requires an accessible name (defaults to \"Close\"). Use inside dialogs, drawers, toasts, and banners; pair with Escape handling on the owning surface.",
    subcategory="Utility",
    tags=["button", "react", "tailwind", "close", "dismiss", "overlay", "utility", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["icon-button", "back-button"],
    props_doc={
        "usage": '<CloseButton onClick={closeDialog} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `label` | `string` | `\"Close\"` (rendered as `aria-label`) |\n| `variant` | `ghost \\| outline` | `ghost` |\n| `size` | `ButtonSize` | `md` |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="ghost (default) · outline.",
    sizes_doc=SIZES_DOC + " Icon-only: square (`w` == `h`).",
    states_doc="default · hover · focus-visible · disabled (reduced opacity).",
    a11y_doc="Icon-only, so an accessible name is **required** — `label` (default \"Close\") is rendered as `aria-label`. Focus-visible ring uses `color.focus-ring`. Pair with Escape handling on the owning dialog/drawer/banner.",
    notes_doc="Use inside dialogs, drawers, toasts, banners. The owning surface should close on Escape and move focus appropriately.",
    tsx=f'''import type {{ ButtonHTMLAttributes }} from "react";

/* DevSnips React — CloseButton
 * Dismiss control for overlays. Icon-only (X); requires an accessible name
 * (defaults to "Close"). 36px default; 32px in compact headers.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type CloseVariant = "ghost" | "outline";

export interface CloseButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  label?: string;
  variant?: CloseVariant;
  size?: ButtonSize;
}}

{CX}

const VARIANTS: Record<CloseVariant, string> = {{
  ghost: "{V_GHOST}",
  outline: "{V_OUTLINE}",
}};

const ICON_ONLY: Record<ButtonSize, string> = {{
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
}};

export function CloseButton({{
  label = "Close",
  variant = "ghost",
  size = "md",
  disabled,
  className,
  type = "button",
  ...rest
}}: CloseButtonProps) {{
  return (
    <button
      type={{type}}
      aria-label={{label}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        ICON_ONLY[size],
        className,
      )}}
      disabled={{disabled}}
      {{...rest}}
    >
      <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M18 6 6 18" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="m6 6 12 12" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>
  );
}}

export default CloseButton;
''',
    showcase=r'''function Showcase() {
  const [open, setOpen] = React.useState(true);
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">ghost · outline</span></div>
        <div className="ds-row">
          <CloseButton variant="ghost" onClick={() => {}} />
          <CloseButton variant="outline" onClick={() => {}} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → xl, ghost</span></div>
        <div className="ds-row">
          <CloseButton size="sm" />
          <CloseButton size="md" />
          <CloseButton size="lg" />
          <CloseButton size="xl" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>In context</h2><span className="ds-note">banner dismiss</span></div>
        <div className="ds-canvas" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16 }}>
          <span>Connection restored. You can resume editing.</span>
          <CloseButton onClick={() => setOpen(false)} label="Dismiss banner" />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================== back-button =
register(
    "back-button",
    title="Back Button",
    eyebrow="React Component",
    lede="Returns to the previous view. Leading arrow-left + label. Renders as a button (onClick, default) or a link (href). Icon-only mode needs a `label` prop for the accessible name.",
    subcategory="Navigation",
    tags=["button", "react", "tailwind", "back", "navigation", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["close-button", "link-button", "ghost-button"],
    props_doc={
        "usage": '<BackButton onClick={goBack}>Back to list</BackButton>\n<BackButton href="/projects" showLabel={false} label="Back" />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | `\"Back\"` |\n| `href` | `string` | — (renders `<a>` when set) |\n| `variant` | `ghost \\| outline` | `ghost` |\n| `size` | `ButtonSize` | `md` |\n| `showLabel` | `boolean` | `true` (icon-only when false; `children` becomes `aria-label`) |\n\nPlus all native button/anchor attributes depending on mode.",
    },
    variants_doc="ghost (default) · outline.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · focus-visible · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " Icon-only mode uses `children` (or \"Back\") as `aria-label` so the control stays named. Link mode renders a real `<a href>`.",
    notes_doc="Use above page content (back to list) or as a wizard footer action. For app-internal back, prefer onClick; for real navigation, pass `href`.",
    tsx=f'''import type {{ ButtonHTMLAttributes, AnchorHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — BackButton
 * Returns to the previous view. Leading arrow-left + label. Renders a
 * button (onClick) or a link (href). Icon-only mode needs a label for an
 * accessible name.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type BackVariant = "ghost" | "outline";

export interface BackButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "href"> {{
  href?: string;
  variant?: BackVariant;
  size?: ButtonSize;
  showLabel?: boolean;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<BackVariant, string> = {{
  ghost: "{V_GHOST}",
  outline: "{V_OUTLINE}",
}};

const ICON_ONLY: Record<ButtonSize, string> = {{
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
}};

function ArrowLeft() {{
  return (
    <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M19 12H5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      <path d="m11 19-7-7 7-7" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}}

export function BackButton({{
  children = "Back",
  href,
  variant = "ghost",
  size = "md",
  showLabel = true,
  className,
  type = "button",
  onClick,
  ...rest
}}: BackButtonProps) {{
  const cls = cx(
    "{BASE}",
    VARIANTS[variant],
    showLabel ? SIZES[size] : ICON_ONLY[size],
    className,
  );
  const content = (
    <>
      <ArrowLeft />
      {{showLabel && <span>{{children}}</span>}}
    </>
  );
  if (href) {{
    return <a href={{href}} className={{cls}} {{...rest}}>{{content}}</a>;
  }}
  return (
    <button
      type={{type}}
      className={{cls}}
      aria-label={{showLabel ? undefined : (typeof children === "string" ? children : "Back")}}
      onClick={{onClick}}
      {{...rest}}
    >
      {{content}}
    </button>
  );
}}

export default BackButton;
''',
    showcase=r'''function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">ghost · outline</span></div>
        <div className="ds-row">
          <BackButton href="/projects">Back to projects</BackButton>
          <BackButton href="/settings" variant="outline">Back to settings</BackButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → xl, ghost</span></div>
        <div className="ds-row">
          <BackButton size="sm" href="#">Back</BackButton>
          <BackButton size="md" href="#">Back to list</BackButton>
          <BackButton size="lg" href="#">Back to dashboard</BackButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Icon-only</h2><span className="ds-note">label becomes aria-label</span></div>
        <div className="ds-row">
          <BackButton href="#" showLabel={false} label="Back">Back</BackButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================== add-button ===
register(
    "add-button",
    title="Add Button",
    eyebrow="React Component",
    lede="A creation affordance with a leading plus. `label` is both the visible text and (when icon-only) the accessible name. Defaults to solid since adding is often the primary creation action on a surface.",
    subcategory="Utility",
    tags=["button", "react", "tailwind", "add", "create", "utility", "action", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=False,
    related=["solid-button", "floating-action-button", "icon-button"],
    props_doc={
        "usage": '<AddButton onClick={create}>Add member</AddButton>\n<AddButton showLabel={false} label="Add row" />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | `\"Add\"` |\n| `variant` | `solid \\| outline \\| secondary \\| ghost` | `solid` |\n| `size` | `ButtonSize` | `md` |\n| `showLabel` | `boolean` | `true` (icon-only when false; `children` becomes `aria-label`) |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="solid (default) · outline · secondary · ghost.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · active · focus-visible · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " Icon-only mode uses `children` (or \"Add\") as `aria-label`.",
    notes_doc="Reserve for creation actions. For a floating primary compose action, use FloatingActionButton instead.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — AddButton
 * Creation affordance with a leading plus. `label` is both the visible text
 * and (when icon-only) the accessible name. Defaults to solid since adding
 * is often the primary creation action.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type AddVariant = "solid" | "outline" | "secondary" | "ghost";

export interface AddButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  variant?: AddVariant;
  size?: ButtonSize;
  showLabel?: boolean;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<AddVariant, string> = {{
  solid: "{V_SOLID}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  ghost: "{V_GHOST}",
}};

const ICON_ONLY: Record<ButtonSize, string> = {{
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
}};

export function AddButton({{
  children = "Add",
  variant = "solid",
  size = "md",
  showLabel = true,
  disabled,
  className,
  type = "button",
  ...rest
}}: AddButtonProps) {{
  return (
    <button
      type={{type}}
      aria-label={{showLabel ? undefined : (typeof children === "string" ? children : "Add")}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        showLabel ? SIZES[size] : ICON_ONLY[size],
        className,
      )}}
      disabled={{disabled}}
      {{...rest}}
    >
      <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M12 5v14" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
        <path d="M5 12h14" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
      </svg>
      {{showLabel && <span>{{children}}</span>}}
    </button>
  );
}}

export default AddButton;
''',
    showcase=r'''function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">solid · outline · secondary · ghost</span></div>
        <div className="ds-row">
          <AddButton variant="solid">Add member</AddButton>
          <AddButton variant="outline">Add label</AddButton>
          <AddButton variant="secondary">Add field</AddButton>
          <AddButton variant="ghost">Add</AddButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → xl, solid</span></div>
        <div className="ds-row">
          <AddButton size="sm">Add</AddButton>
          <AddButton size="md">Add task</AddButton>
          <AddButton size="lg">Add new project</AddButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Icon-only</h2><span className="ds-note">toolbar density</span></div>
        <div className="ds-row">
          <AddButton showLabel={false} label="Add row" />
          <AddButton showLabel={false} label="Add column" variant="outline" />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# =========================================================== filter-button =
register(
    "filter-button",
    title="Filter Button",
    eyebrow="React Component",
    lede="Opens filters and shows the active count. `activeCount` renders a count chip and switches the button to `surface-active` so the filtered state is obvious. `open` rotates the leading icon and exposes `aria-expanded`.",
    subcategory="Utility",
    tags=["button", "react", "tailwind", "filter", "count", "toolbar", "utility", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["sort-button", "export-button", "outline-button"],
    props_doc={
        "usage": '<FilterButton activeCount={3} open={open} onToggle={toggle} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `activeCount` | `number` | `0` |\n| `open` | `boolean` | `false` (sets `aria-expanded`) |\n| `label` | `string` | `\"Filter\"` |\n| `variant` | `outline \\| secondary \\| ghost` | `outline` |\n| `size` | `ButtonSize` | `sm` |\n| `onToggle` | `() => void` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="outline (default) · secondary · ghost. When `activeCount > 0` the button uses `surface-active` and shows a count chip.",
    sizes_doc=SIZES_DOC + " Default is `sm` for toolbars.",
    states_doc="default · hover · focus-visible · open (`aria-expanded`, icon rotates) · active-filters (`surface-active` + count chip) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " `aria-expanded` reflects `open`; `aria-label` includes the active count (e.g. \"Filter, 3 active\"). The count chip is decorative (`aria-hidden`) because the count is already in the label.",
    notes_doc="Wire to a popover/panel of filter controls. Keep the count accurate so the state is trustworthy.",
    tsx=f'''import type {{ ButtonHTMLAttributes }} from "react";

/* DevSnips React — FilterButton
 * Opens filters + shows active count. activeCount renders a count chip and
 * switches to surface-active. open rotates the leading icon + aria-expanded.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type FilterVariant = "outline" | "secondary" | "ghost";

export interface FilterButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onChange"> {{
  activeCount?: number;
  open?: boolean;
  label?: string;
  variant?: FilterVariant;
  size?: ButtonSize;
  onToggle?: () => void;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<FilterVariant, string> = {{
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  ghost: "{V_GHOST}",
}};

export function FilterButton({{
  activeCount = 0,
  open = false,
  label = "Filter",
  variant = "outline",
  size = "sm",
  onToggle,
  className,
  type = "button",
  ...rest
}}: FilterButtonProps) {{
  const hasFilters = activeCount > 0;
  return (
    <button
      type={{type}}
      aria-expanded={{open || undefined}}
      aria-label={{hasFilters ? `${{label}}, ${{activeCount}} active` : label}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        hasFilters && "bg-[var(--ds-color-surface-active)] font-semibold",
        SIZES[size],
        className,
      )}}
      onClick={{onToggle}}
      {{...rest}}
    >
      <svg className={{cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", open ? "rotate-180" : "rotate-0")}} viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <span>{{label}}</span>
      {{hasFilters && (
        <span className="ml-1 inline-flex h-[18px] min-w-[18px] items-center justify-center rounded-full bg-[var(--ds-color-accent)] px-[5px] text-[11px] font-semibold leading-none text-[var(--ds-color-accent-foreground)]" aria-hidden="true">{{activeCount}}</span>
      )}}
    </button>
  );
}}

export default FilterButton;
''',
    showcase=r'''function Showcase() {
  const [open, setOpen] = React.useState(false);
  const [count, setCount] = React.useState(3);
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>States</h2><span className="ds-note">idle · active · open</span></div>
        <div className="ds-row">
          <FilterButton activeCount={0} open={false} onToggle={() => {}} label="Filter" />
          <FilterButton activeCount={count} open={open} onToggle={() => { setOpen(o => !o); }} />
          <FilterButton activeCount={7} open={false} variant="secondary" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → lg, outline</span></div>
        <div className="ds-row">
          <FilterButton size="xs" activeCount={2} />
          <FilterButton size="sm" activeCount={2} />
          <FilterButton size="md" activeCount={2} />
          <FilterButton size="lg" activeCount={2} />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================= sort-button =
register(
    "sort-button",
    title="Sort Button",
    eyebrow="React Component",
    lede="Sets the sort field and direction. Clicking toggles direction (desc → asc → none → desc). The active sort is shown via the field label + a rotated chevron, not color alone. `aria-label` conveys the current state.",
    subcategory="Utility",
    tags=["button", "react", "tailwind", "sort", "table", "toolbar", "utility", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["filter-button", "pagination-button", "outline-button"],
    props_doc={
        "usage": '<SortButton field="Created" direction={dir} onToggle={cycle} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `field` | `string` | `\"Created\"` |\n| `direction` | `asc \\| desc \\| null` | `desc` |\n| `variant` | `outline \\| secondary \\| ghost` | `outline` |\n| `size` | `ButtonSize` | `sm` |\n| `onToggle` | `() => void` | — (cycle direction on click) |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="outline (default) · secondary · ghost.",
    sizes_doc=SIZES_DOC + " Default is `sm` for table toolbars.",
    states_doc="default · hover · focus-visible · active-sort (`surface-active`, chevron rotated by direction) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " `aria-label` conveys the field and current direction (\"Sort by Created, currently descending\"). Direction is shown by chevron rotation + opacity, not color alone.",
    notes_doc="Cycle on click: desc → asc → none → desc. When `direction` is null, show no chevron emphasis.",
    tsx=f'''import type {{ ButtonHTMLAttributes }} from "react";

/* DevSnips React — SortButton
 * Sets sort field + direction. Click cycles direction (desc→asc→none→desc).
 * Active sort shown via field label + rotated chevron, not color alone.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type SortVariant = "outline" | "secondary" | "ghost";
export type SortDirection = "asc" | "desc" | null;

export interface SortButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onChange"> {{
  field?: string;
  direction?: SortDirection;
  variant?: SortVariant;
  size?: ButtonSize;
  onToggle?: () => void;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<SortVariant, string> = {{
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  ghost: "{V_GHOST}",
}};

export function SortButton({{
  field = "Created",
  direction = "desc",
  variant = "outline",
  size = "sm",
  onToggle,
  className,
  type = "button",
  ...rest
}}: SortButtonProps) {{
  const active = direction !== null;
  const dirLabel = direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "unsorted";
  return (
    <button
      type={{type}}
      aria-label={{`Sort by ${{field}}, currently ${{dirLabel}}`}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        active && "bg-[var(--ds-color-surface-active)] font-semibold",
        SIZES[size],
        className,
      )}}
      onClick={{onToggle}}
      {{...rest}}
    >
      <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M11 5h10" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
        <path d="M11 9h7" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
        <path d="M11 13h4" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
        <path d="m3 17 3 3 3-3" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M6 18V4" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
      </svg>
      <span>{{field}}</span>
      <svg
        className={{cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", direction === "asc" ? "rotate-180" : "rotate-0", !active && "opacity-50")}}
        viewBox="0 0 24 24" fill="none" aria-hidden="true"
      >
        <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>
  );
}}

export default SortButton;
''',
    showcase=r'''function Showcase() {
  const dirs = ["desc", "asc", null];
  const [i, setI] = React.useState(0);
  const [field] = React.useState("Created");
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Direction cycle</h2><span className="ds-note">click: desc → asc → none → desc</span></div>
        <div className="ds-row">
          <SortButton field={field} direction={dirs[i]} onToggle={() => setI(x => (x + 1) % 3)} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Fields</h2><span className="ds-note">different active columns</span></div>
        <div className="ds-row">
          <SortButton field="Name" direction="asc" />
          <SortButton field="Created" direction="desc" />
          <SortButton field="Owner" direction={null} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">xs → lg, outline</span></div>
        <div className="ds-row">
          <SortButton size="xs" field="Date" direction="desc" />
          <SortButton size="sm" field="Date" direction="desc" />
          <SortButton size="md" field="Date" direction="desc" />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)

# =========================================================== export-button =
register(
    "export-button",
    title="Export Button",
    eyebrow="React Component",
    lede="A menu trigger for export destinations. `formats` is a list of export targets; opens a keyboard-navigable menu (aria-haspopup=\"menu\"). Arrow keys move, Enter exports, Escape closes.",
    subcategory="Utility",
    tags=["button", "react", "tailwind", "export", "menu", "table", "toolbar", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["more-actions-button", "split-button", "download-button"],
    props_doc={
        "usage": '<ExportButton formats={[{id:"csv",label:"Export as CSV"},{id:"pdf",label:"Export as PDF"}}] onExport={handle} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `formats` | `Array<{ id: string; label: ReactNode; icon?: string }>` | `[]` |\n| `onExport` | `(id, format) => void` | — |\n| `label` | `string` | `\"Export\"` |\n| `variant` | `outline \\| secondary` | `outline` |\n| `size` | `ButtonSize` | `sm` |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="outline (default) · secondary. Menu is a bordered elevated surface.",
    sizes_doc=SIZES_DOC + " Default is `sm` for toolbars.",
    states_doc="default · hover · focus-visible · open (menu, `aria-expanded`) · disabled (reduced opacity).",
    a11y_doc="Trigger has `aria-haspopup=\"menu\"` + `aria-expanded`. Menu uses `role=\"menu\"`, items `role=\"menuitem\"`. **Keyboard**: ArrowUp/Down move, Enter/Space exports, Escape closes and returns focus to the trigger, outside click closes.",
    notes_doc="Use in table/report toolbars where multiple export targets exist. For a single target, use DownloadButton instead.",
    tsx=f'''import {{ useEffect, useRef, useState }} from "react";
import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — ExportButton
 * Menu trigger for export destinations. aria-haspopup="menu", keyboard
 * navigable. Arrow keys move, Enter exports, Escape closes.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type ExportVariant = "outline" | "secondary";

export interface ExportFormat {{
  id: string;
  label: ReactNode;
  icon?: string;
}}

export interface ExportButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {{
  formats?: ExportFormat[];
  onExport?: (id: string, format: ExportFormat) => void;
  label?: string;
  variant?: ExportVariant;
  size?: ButtonSize;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<ExportVariant, string> = {{
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
}};

const MENU =
  "absolute right-0 top-[calc(100%+4px)] z-40 min-w-[180px] rounded-[var(--ds-radius-md)] " +
  "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 " +
  "shadow-[var(--ds-shadow-md)]";
const ITEM =
  "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border-0 px-2 py-1.5 " +
  "text-left font-normal text-[13px] leading-none text-[var(--ds-color-foreground)] " +
  "bg-transparent transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)] " +
  "focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)]";

function Icon({{ name, className }}: {{ name?: string; className?: string }}) {{
  if (!name) return null;
  const common = {{ width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" }} as const;
  const paths: Record<string, ReactNode> = {{
    "download": <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />,
    "file": <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><path d="M14 2v6h6" /></>,
    "archive": <><rect x="3" y="4" width="18" height="4" rx="1" /><path d="M5 8v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8" /><path d="M10 12h4" /></>,
    "external": <><path d="M15 3h6v6" /><path d="M10 14 21 3" /></>,
  }};
  return <svg {{...common}}>{{paths[name]}}</svg>;
}}

export function ExportButton({{
  formats = [],
  onExport,
  label = "Export",
  variant = "outline",
  size = "sm",
  disabled,
  className,
  type = "button",
  ...rest
}}: ExportButtonProps) {{
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const itemRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {{
    if (!open) return;
    function onDown(e: MouseEvent) {{ if (containerRef.current && !containerRef.current.contains(e.target as Node)) setOpen(false); }}
    function onKey(e: KeyboardEvent) {{ if (e.key === "Escape") {{ setOpen(false); triggerRef.current?.focus(); }} }}
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {{ document.removeEventListener("mousedown", onDown); document.removeEventListener("keydown", onKey); }};
  }}, [open]);

  function openMenu() {{ setOpen(true); setTimeout(() => itemRefs.current[0]?.focus(), 0); }}
  function choose(i: number) {{ setOpen(false); onExport?.(formats[i].id, formats[i]); triggerRef.current?.focus(); }}
  function onKey(e: React.KeyboardEvent, i: number) {{
    const n = formats.length;
    if (e.key === "ArrowDown") {{ e.preventDefault(); itemRefs.current[(i + 1) % n]?.focus(); }}
    else if (e.key === "ArrowUp") {{ e.preventDefault(); itemRefs.current[(i - 1 + n) % n]?.focus(); }}
    else if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); choose(i); }}
  }}

  return (
    <div ref={{containerRef}} className="relative inline-flex">
      <button
        type={{type}}
        ref={{triggerRef}}
        aria-haspopup="menu"
        aria-expanded={{open}}
        className={{cx("{BASE}", VARIANTS[variant], SIZES[size], className)}}
        disabled={{disabled}}
        onClick={{() => (open ? setOpen(false) : openMenu())}}
        {{...rest}}
      >
        <Icon name="download" className="shrink-0" />
        <span>{{label}}</span>
        <svg className={{cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", open ? "rotate-180" : "rotate-0")}} viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </button>
      {{open && (
        <div role="menu" className={{MENU}}>
          {{formats.map((f, i) => (
            <button key={{f.id}} ref={{(el) => {{ itemRefs.current[i] = el; }}}} role="menuitem" tabIndex={{-1}} className={{ITEM}} onClick={{() => choose(i)}} onKeyDown={{(e) => onKey(e, i)}}>
              <Icon name={{f.icon ?? "download"}} className="shrink-0" />
              <span>{{f.label}}</span>
            </button>
          ))}}
        </div>
      )}}
    </div>
  );
}}

export default ExportButton;
''',
    showcase=r'''function Showcase() {
  const [last, setLast] = React.useState("—");
  const formats = [{id:"csv",label:"Export as CSV",icon:"download"},{id:"pdf",label:"Export as PDF",icon:"file"},{id:"json",label:"Export as JSON"},{id:"zip",label:"Export archive",icon:"archive"}];
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">last: {last}</span></div>
        <div className="ds-row">
          <ExportButton variant="outline" formats={formats} onExport={(id) => setLast(id)} />
          <ExportButton variant="secondary" formats={formats} onExport={(id) => setLast(id)} label="Export report" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → lg, outline</span></div>
        <div className="ds-row">
          <ExportButton size="sm" formats={formats} onExport={(id) => setLast(id)} />
          <ExportButton size="md" formats={formats} onExport={(id) => setLast(id)} />
          <ExportButton size="lg" formats={formats} onExport={(id) => setLast(id)} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Disabled</h2><span className="ds-note">no exports configured</span></div>
        <div className="ds-row"><ExportButton formats={[]} disabled label="No exports available" /></div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ========================================================== download-button =
register(
    "download-button",
    title="Download Button",
    eyebrow="React Component",
    lede="A direct download with progress feedback. Fires `onDownload` (wire to a real fetch/blob), surfaces a working state with a spinner, then a brief done state. Supports a `meta` line (e.g. \"CSV · 2.4 MB\").",
    subcategory="Feedback",
    tags=["button", "react", "tailwind", "download", "progress", "feedback", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["export-button", "loading-button", "refresh-button"],
    props_doc={
        "usage": '<DownloadButton meta="CSV · 2.4 MB" onDownload={fetchCsv}>Download</DownloadButton>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | `\"Download\"` |\n| `meta` | `ReactNode` | — (secondary line under the label) |\n| `href` | `string` | — (if provided, native anchor download) |\n| `variant` | `outline \\| solid \\| secondary` | `outline` |\n| `size` | `ButtonSize` | `md` |\n| `onDownload` | `() => void \\| Promise<void>` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="outline (default) · solid · secondary.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · focus-visible · working (spinner + `aria-busy`, disabled) · done (check icon) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " `aria-busy` reflects the working state. The label changes (\"Downloading…\") to convey progress beyond the spinner.",
    notes_doc="For multiple export targets, use ExportButton. DownloadButton is for a single file with progress feedback.",
    tsx=f'''import {{ useState }} from "react";
import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — DownloadButton
 * Direct download with progress feedback. Fires onDownload; shows a
 * spinner + "Downloading…" while pending, then a brief done state.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type DownloadVariant = "outline" | "solid" | "secondary";

export interface DownloadButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onChange"> {{
  meta?: ReactNode;
  href?: string;
  variant?: DownloadVariant;
  size?: ButtonSize;
  onDownload?: () => void | Promise<void>;
}}

{CX}

{SPINNER}

{SIZES_TS}

const VARIANTS: Record<DownloadVariant, string> = {{
  outline: "{V_OUTLINE}",
  solid: "{V_SOLID}",
  secondary: "{V_SECONDARY}",
}};

export function DownloadButton({{
  children = "Download",
  meta,
  href,
  variant = "outline",
  size = "md",
  onDownload,
  className,
  type = "button",
  ...rest
}}: DownloadButtonProps) {{
  const [state, setState] = useState<"idle" | "working" | "done">("idle");
  async function start(e: React.MouseEvent) {{
    if (state !== "idle") return;
    setState("working");
    try {{ await Promise.resolve(onDownload?.()); }}
    finally {{ setState("done"); setTimeout(() => setState("idle"), 1800); }}
  }}
  const label = state === "working" ? "Downloading…" : state === "done" ? "Downloaded" : children;
  return (
    <button
      type={{type}}
      className={{cx("{BASE}", VARIANTS[variant], SIZES[size], className)}}
      onClick={{start}}
      disabled={{state === "working"}}
      aria-busy={{state === "working" || undefined}}
      {{...rest}}
    >
      {{state === "working" ? <Spinner /> : (
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          {{state === "done"
            ? <path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            : <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><path d="m7 10 5 5 5-5" /><path d="M12 15V3" /></>}}
        </svg>
      )}}
      <span className="flex flex-col items-start leading-tight">
        <span>{{label}}</span>
        {{meta && <span className="text-[11px] font-normal text-[var(--ds-color-muted-foreground)]">{{meta}}</span>}}
      </span>
    </button>
  );
}}

export default DownloadButton;
''',
    showcase=r'''function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">click to download</span></div>
        <div className="ds-row">
          <DownloadButton variant="outline" meta="CSV · 2.4 MB" onDownload={() => {}}>Download</DownloadButton>
          <DownloadButton variant="solid" meta="PDF · 1.1 MB" onDownload={() => {}}>Download invoice</DownloadButton>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → lg, outline</span></div>
        <div className="ds-row">
          <DownloadButton size="sm" meta="CSV · 2.4 MB" onDownload={() => {}}>Download</DownloadButton>
          <DownloadButton size="md" meta="CSV · 2.4 MB" onDownload={() => {}}>Download report</DownloadButton>
          <DownloadButton size="lg" meta="Archive · 18 MB" onDownload={() => {}}>Download archive</DownloadButton>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ============================================================= copy-button ===
register(
    "copy-button",
    title="Copy Button",
    eyebrow="React Component",
    lede="Clipboard copy with transient feedback. Uses the async Clipboard API with an execCommand fallback. On success, swaps the icon to a check and the label to \"Copied\", then reverts. An `aria-live` region announces the copied state.",
    subcategory="Feedback",
    tags=["button", "react", "tailwind", "copy", "clipboard", "feedback", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["refresh-button", "download-button", "outline-button"],
    props_doc={
        "usage": '<CopyButton value={projectId} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `value` | `string` | — (text to copy) |\n| `label` | `string` | `\"Copy\"` |\n| `copiedLabel` | `string` | `\"Copied\"` |\n| `resetMs` | `number` | `2000` |\n| `onCopy` | `(value: string) => void` | — |\n| `variant` | `outline \\| secondary \\| ghost \\| solid` | `outline` |\n| `size` | `ButtonSize` | `sm` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="outline (default) · secondary · ghost · solid.",
    sizes_doc=SIZES_DOC + " Default is `sm`.",
    states_doc="default · hover · focus-visible · **copied** (check icon + \"Copied\" label + `aria-live` announcement, reverts after `resetMs`).",
    a11y_doc=A11Y_NATIVE + " An `aria-live=\"polite\"` region announces \"Copied\" so screen readers hear the result. `aria-label` includes the value being copied. Success is conveyed by icon + label change, not color alone.",
    notes_doc="Always pair with the value displayed nearby (a code/ID row) so the copy target is unambiguous. Gracefully degrades when the Clipboard API is unavailable.",
    tsx=f'''import {{ useCallback, useRef, useState }} from "react";
import type {{ ButtonHTMLAttributes }} from "react";

/* DevSnips React — CopyButton
 * Clipboard copy with transient feedback. Async Clipboard API + execCommand
 * fallback. aria-live announces the copied state; icon + label confirm
 * success without relying on color alone.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type CopyVariant = "outline" | "secondary" | "ghost" | "solid";

export interface CopyButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {{
  value: string;
  label?: string;
  copiedLabel?: string;
  resetMs?: number;
  onCopy?: (value: string) => void;
  variant?: CopyVariant;
  size?: ButtonSize;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<CopyVariant, string> = {{
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
  ghost: "{V_GHOST}",
  solid: "{V_SOLID}",
}};

function useCopy(resetMs: number) {{
  const [copied, setCopied] = useState(false);
  const t = useRef<ReturnType<typeof setTimeout> | null>(null);
  const copy = useCallback(async (text: string) => {{
    try {{
      if (navigator.clipboard && window.isSecureContext) {{ await navigator.clipboard.writeText(text); }}
      else {{
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
      }}
      setCopied(true);
      if (t.current) clearTimeout(t.current);
      t.current = setTimeout(() => setCopied(false), resetMs);
    }} catch {{ /* clipboard unavailable */ }}
  }}, [resetMs]);
  return [copied, copy] as const;
}}

export function CopyButton({{
  value,
  label = "Copy",
  copiedLabel = "Copied",
  resetMs = 2000,
  onCopy,
  variant = "outline",
  size = "sm",
  className,
  type = "button",
  ...rest
}}: CopyButtonProps) {{
  const [copied, copy] = useCopy(resetMs);
  async function handle() {{ await copy(value); onCopy?.(value); }}
  return (
    <button
      type={{type}}
      className={{cx("{BASE}", VARIANTS[variant], SIZES[size], className)}}
      onClick={{handle}}
      aria-label={{`${{copied ? copiedLabel : label}}: ${{value}}`}}
      {{...rest}}
    >
      <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        {{copied
          ? <path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          : <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>}}
      </svg>
      <span>{{copied ? copiedLabel : label}}</span>
      <span className="sr-only" role="status" aria-live="polite">{{copied ? copiedLabel : ""}}</span>
    </button>
  );
}}

export default CopyButton;
''',
    showcase=r'''function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">outline · secondary · ghost · solid</span></div>
        <div className="ds-row">
          <CopyButton variant="outline" value="prj_8x2k9" />
          <CopyButton variant="secondary" value="prj_8x2k9" />
          <CopyButton variant="ghost" value="prj_8x2k9" />
          <CopyButton variant="solid" value="prj_8x2k9" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>In context</h2><span className="ds-note">project ID row</span></div>
        <div className="ds-canvas" style={{ display: "flex", alignItems: "center", gap: 12, justifyContent: "space-between" }}>
          <code style={{ fontFamily: "var(--ds-font-mono)" }}>prj_8x2k9vq7</code>
          <CopyButton value="prj_8x2k9vq7" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → lg</span></div>
        <div className="ds-row">
          <CopyButton size="sm" value="abc" />
          <CopyButton size="md" value="abc" />
          <CopyButton size="lg" value="abc" />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# =========================================================== refresh-button =
register(
    "refresh-button",
    title="Refresh Button",
    eyebrow="React Component",
    lede="Re-fetch with in-flight feedback. `onRefresh` may return a Promise; while pending, the refresh icon spins (respecting reduced motion), the button is disabled, and `aria-busy` is set. Icon-only mode for compact toolbars.",
    subcategory="Feedback",
    tags=["button", "react", "tailwind", "refresh", "reload", "feedback", "interactive", "icon"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["copy-button", "download-button", "loading-button"],
    props_doc={
        "usage": '<RefreshButton onRefresh={refetch} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `onRefresh` | `() => void \\| Promise<void>` | — |\n| `label` | `string` | `\"Refresh\"` |\n| `showLabel` | `boolean` | `false` (icon-only when false; `label` becomes `aria-label`) |\n| `variant` | `ghost \\| outline \\| secondary` | `ghost` |\n| `size` | `ButtonSize` | `sm` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="ghost (default) · outline · secondary.",
    sizes_doc=SIZES_DOC + " Default is `sm`; icon-only by default for compact toolbars.",
    states_doc="default · hover · focus-visible · refreshing (spinner-spin icon + `aria-busy`, disabled) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " `aria-busy` reflects the refreshing state; `aria-label` is `label`. Reduced motion disables the spin animation.",
    notes_doc="Icon-only by default — place in a toolbar next to a data region. Pass `showLabel` for a labeled refresh action.",
    tsx=f'''import {{ useState }} from "react";
import type {{ ButtonHTMLAttributes }} from "react";

/* DevSnips React — RefreshButton
 * Re-fetch with in-flight feedback. onRefresh may return a Promise; while
 * pending the icon spins (reduced-motion safe), the button is disabled,
 * and aria-busy is set.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type RefreshVariant = "ghost" | "outline" | "secondary";

export interface RefreshButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {{
  onRefresh?: () => void | Promise<void>;
  label?: string;
  showLabel?: boolean;
  variant?: RefreshVariant;
  size?: ButtonSize;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<RefreshVariant, string> = {{
  ghost: "{V_GHOST}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
}};

const ICON_ONLY: Record<ButtonSize, string> = {{
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
}};

export function RefreshButton({{
  onRefresh,
  label = "Refresh",
  showLabel = false,
  variant = "ghost",
  size = "sm",
  className,
  type = "button",
  ...rest
}}: RefreshButtonProps) {{
  const [loading, setLoading] = useState(false);
  async function run() {{
    if (loading) return;
    setLoading(true);
    try {{ await Promise.resolve(onRefresh?.()); }}
    finally {{ setLoading(false); }}
  }}
  return (
    <button
      type={{type}}
      aria-label={{showLabel ? undefined : label}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        showLabel ? SIZES[size] : ICON_ONLY[size],
        className,
      )}}
      onClick={{run}}
      disabled={{loading}}
      aria-busy={{loading || undefined}}
      {{...rest}}
    >
      <svg className={{cx("h-[1em] w-[1em] shrink-0", loading && "animate-spin motion-reduce:animate-none")}} viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M3 12a9 9 0 0 1 15-6.7L21 8" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M21 3v5h-5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M21 12a9 9 0 0 1-15 6.7L3 16" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M3 21v-5h5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {{showLabel && <span>{{loading ? "Refreshing…" : label}}</span>}}
    </button>
  );
}}

export default RefreshButton;
''',
    showcase=r'''function Showcase() {
  function run() { return new Promise((r) => setTimeout(r, 1500)); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Icon-only</h2><span className="ds-note">toolbar density</span></div>
        <div className="ds-row">
          <RefreshButton onRefresh={run} label="Refresh activity" />
          <RefreshButton onRefresh={run} variant="outline" label="Refresh activity" />
          <RefreshButton onRefresh={run} variant="secondary" label="Refresh activity" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Labeled</h2><span className="ds-note">showLabel</span></div>
        <div className="ds-row">
          <RefreshButton onRefresh={run} showLabel label="Refresh activity" variant="outline" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → lg, ghost icon-only</span></div>
        <div className="ds-row">
          <RefreshButton size="sm" onRefresh={() => {}} />
          <RefreshButton size="md" onRefresh={() => {}} />
          <RefreshButton size="lg" onRefresh={() => {}} />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ====================================================== more-actions-button =
register(
    "more-actions-button",
    title="More Actions Button",
    eyebrow="React Component",
    lede="An overflow menu trigger. `actions` is a list of actions; opens a keyboard-navigable menu (aria-haspopup=\"menu\"). Destructive actions render in `destructive` color. Icon-only by default; pass `label` for the accessible name.",
    subcategory="Composite",
    tags=["button", "react", "tailwind", "more", "overflow", "menu", "composite", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["split-button", "export-button", "icon-button"],
    props_doc={
        "usage": '<MoreActionsButton label="More actions" actions={[{id:"edit",label:"Edit"},{id:"delete",label:"Delete",destructive:true}}] onAction={handle} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `actions` | `Array<{ id: string; label: ReactNode; icon?: string; destructive?: boolean }>` | `[]` |\n| `onAction` | `(id, action) => void` | — |\n| `label` | `string` | `\"More actions\"` (rendered as `aria-label`) |\n| `align` | `left \\| right` | `right` (menu alignment) |\n| `variant` | `ghost \\| outline \\| secondary` | `ghost` |\n| `size` | `ButtonSize` | `sm` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="ghost (default) · outline · secondary. Menu is a bordered elevated surface; destructive items use `destructive` color.",
    sizes_doc=SIZES_DOC + " Default is `sm`; icon-only (three-dots).",
    states_doc="default · hover · focus-visible · open (menu, `aria-expanded`) · disabled (reduced opacity).",
    a11y_doc="Trigger has `aria-haspopup=\"menu\"` + `aria-expanded` + `aria-label`. Menu uses `role=\"menu\"`, items `role=\"menuitem\"`. **Keyboard**: ArrowUp/Down move, Enter/Space activates, Escape closes and returns focus, outside click closes. Destructive items are visually marked with the destructive color (a cue, not the only signal — the label conveys intent).",
    notes_doc="Use in dense rows/headers where actions would otherwise overflow. For a primary action + alternatives, use SplitButton.",
    tsx=f'''import {{ useEffect, useRef, useState }} from "react";
import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — MoreActionsButton
 * Overflow menu trigger. aria-haspopup="menu", keyboard navigable.
 * Destructive items render in destructive color.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type MoreVariant = "ghost" | "outline" | "secondary";
export type MoreAlign = "left" | "right";

export interface MoreAction {{
  id: string;
  label: ReactNode;
  icon?: string;
  destructive?: boolean;
}}

export interface MoreActionsButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {{
  actions?: MoreAction[];
  onAction?: (id: string, action: MoreAction) => void;
  label?: string;
  align?: MoreAlign;
  variant?: MoreVariant;
  size?: ButtonSize;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<MoreVariant, string> = {{
  ghost: "{V_GHOST}",
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
}};

const ICON_ONLY: Record<ButtonSize, string> = {{
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
}};

const MENU =
  "absolute top-[calc(100%+4px)] z-40 min-w-[180px] rounded-[var(--ds-radius-md)] " +
  "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 " +
  "shadow-[var(--ds-shadow-md)]";
const ITEM =
  "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border-0 px-2 py-1.5 " +
  "text-left font-normal text-[13px] leading-none text-[var(--ds-color-foreground)] " +
  "bg-transparent transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)] " +
  "focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)]";

function Icon({{ name, className }}: {{ name?: string; className?: string }}) {{
  if (!name) return null;
  const common = {{ width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" }} as const;
  const paths: Record<string, ReactNode> = {{
    "edit": <><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" /></>,
    "duplicate": <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>,
    "share": <><circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><path d="m8.6 13.5 6.8 4" /><path d="m15.4 6.5-6.8 4" /></>,
    "archive": <><rect x="3" y="4" width="18" height="4" rx="1" /><path d="M5 8v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8" /><path d="M10 12h4" /></>,
    "trash": <><path d="M3 6h18" /><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" /></>,
    "pin": <path d="M12 17v5" />,
    "settings": <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" /></>,
  }};
  return <svg {{...common}}>{{paths[name]}}</svg>;
}}

export function MoreActionsButton({{
  actions = [],
  onAction,
  label = "More actions",
  align = "right",
  variant = "ghost",
  size = "sm",
  className,
  type = "button",
  ...rest
}}: MoreActionsButtonProps) {{
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const itemRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {{
    if (!open) return;
    function onDown(e: MouseEvent) {{ if (containerRef.current && !containerRef.current.contains(e.target as Node)) setOpen(false); }}
    function onKey(e: KeyboardEvent) {{ if (e.key === "Escape") {{ setOpen(false); triggerRef.current?.focus(); }} }}
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {{ document.removeEventListener("mousedown", onDown); document.removeEventListener("keydown", onKey); }};
  }}, [open]);

  function openMenu() {{ setOpen(true); setTimeout(() => itemRefs.current[0]?.focus(), 0); }}
  function choose(i: number) {{ setOpen(false); onAction?.(actions[i].id, actions[i]); triggerRef.current?.focus(); }}
  function onKey(e: React.KeyboardEvent, i: number) {{
    const n = actions.length;
    if (e.key === "ArrowDown") {{ e.preventDefault(); itemRefs.current[(i + 1) % n]?.focus(); }}
    else if (e.key === "ArrowUp") {{ e.preventDefault(); itemRefs.current[(i - 1 + n) % n]?.focus(); }}
    else if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); choose(i); }}
  }}

  return (
    <div ref={{containerRef}} className="relative inline-flex">
      <button
        type={{type}}
        ref={{triggerRef}}
        aria-haspopup="menu"
        aria-expanded={{open}}
        aria-label={{label}}
        className={{cx("{BASE}", VARIANTS[variant], ICON_ONLY[size], className)}}
        onClick={{() => (open ? setOpen(false) : openMenu())}}
        {{...rest}}
      >
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="5" r="1" fill="currentColor" />
          <circle cx="12" cy="12" r="1" fill="currentColor" />
          <circle cx="12" cy="19" r="1" fill="currentColor" />
        </svg>
      </button>
      {{open && (
        <div role="menu" className={{cx(MENU, align === "left" ? "left-0" : "right-0")}}>
          {{actions.map((a, i) => (
            <button
              key={{a.id}}
              ref={{(el) => {{ itemRefs.current[i] = el; }}}}
              role="menuitem"
              tabIndex={{-1}}
              className={{cx(ITEM, a.destructive && "text-[var(--ds-color-destructive)]")}}
              onClick={{() => choose(i)}}
              onKeyDown={{(e) => onKey(e, i)}}
            >
              {{a.icon ? <Icon name={{a.icon}} className="shrink-0" /> : <span className="w-[1em]" />}}
              <span className="flex-1">{{a.label}}</span>
            </button>
          ))}}
        </div>
      )}}
    </div>
  );
}}

export default MoreActionsButton;
''',
    showcase=r'''function Showcase() {
  const [last, setLast] = React.useState("—");
  const actions = [
    { id: "edit", label: "Edit details", icon: "edit" },
    { id: "duplicate", label: "Duplicate", icon: "duplicate" },
    { id: "share", label: "Share", icon: "share" },
    { id: "archive", label: "Archive", icon: "archive" },
    { id: "delete", label: "Delete", icon: "trash", destructive: true },
  ];
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">last: {last}</span></div>
        <div className="ds-row">
          <MoreActionsButton actions={actions} onAction={(id) => setLast(id)} variant="ghost" />
          <MoreActionsButton actions={actions} onAction={(id) => setLast(id)} variant="outline" />
          <MoreActionsButton actions={actions} onAction={(id) => setLast(id)} variant="secondary" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Align</h2><span className="ds-note">left · right</span></div>
        <div className="ds-row">
          <MoreActionsButton actions={actions} onAction={(id) => setLast(id)} align="left" />
          <MoreActionsButton actions={actions} onAction={(id) => setLast(id)} align="right" />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)

# ========================================================== command-button =
register(
    "command-button",
    title="Command Button",
    eyebrow="React Component",
    lede="Opens a command palette. A wide trigger with a search icon, placeholder text, and a kbd hint showing the platform shortcut. Wire `onOpen` to mount the palette; when `bindShortcut` is true, listens for the global shortcut (Cmd/Ctrl+K).",
    subcategory="Composite",
    tags=["button", "react", "tailwind", "command-palette", "search", "shortcut", "composite", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["more-actions-button", "split-button", "outline-button"],
    props_doc={
        "usage": '<CommandButton onOpen={openPalette} placeholder="Search or run a command…" shortcut="⌘K" />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `placeholder` | `string` | `\"Search or run a command…\"` |\n| `shortcut` | `string` | `\"⌘K\"` |\n| `onOpen` | `() => void` | — |\n| `variant` | `outline \\| secondary` | `outline` |\n| `size` | `ButtonSize` | `md` |\n| `bindShortcut` | `boolean` | `true` (listen for Cmd/Ctrl+K globally) |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="outline (default) · secondary. A wide trigger that reads as a search field; muted text + a kbd hint on the trailing edge.",
    sizes_doc=SIZES_DOC,
    states_doc="default · hover · focus-visible · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " The kbd hint is decorative (`aria-hidden`); the button's accessible name is the placeholder. When `bindShortcut` is on, Cmd/Ctrl+K calls `onOpen` so the palette is reachable without a visible click.",
    notes_doc="Use once per app for a global command palette. The trigger is a button (not an input) — it opens the palette, which holds the real search input.",
    tsx=f'''import {{ useEffect }} from "react";
import type {{ ButtonHTMLAttributes }} from "react";

/* DevSnips React — CommandButton
 * Opens a command palette. Wide trigger + search icon + placeholder + kbd
 * hint. bindShortcut listens for Cmd/Ctrl+K to call onOpen.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type CommandVariant = "outline" | "secondary";

export interface CommandButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {{
  placeholder?: string;
  shortcut?: string;
  onOpen?: () => void;
  variant?: CommandVariant;
  size?: ButtonSize;
  bindShortcut?: boolean;
}}

{CX}

{SIZES_TS}

const VARIANTS: Record<CommandVariant, string> = {{
  outline: "{V_OUTLINE}",
  secondary: "{V_SECONDARY}",
}};

const KBD =
  "inline-flex items-center rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] " +
  "bg-[var(--ds-color-surface-subtle)] px-1.5 py-0.5 font-mono text-[11px] leading-none " +
  "text-[var(--ds-color-muted-foreground)]";

export function CommandButton({{
  placeholder = "Search or run a command…",
  shortcut = "⌘K",
  onOpen,
  variant = "outline",
  size = "md",
  bindShortcut = true,
  className,
  type = "button",
  ...rest
}}: CommandButtonProps) {{
  useEffect(() => {{
    if (!bindShortcut) return;
    function onKey(e: KeyboardEvent) {{
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {{
        e.preventDefault();
        onOpen?.();
      }}
    }}
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }}, [bindShortcut, onOpen]);

  return (
    <button
      type={{type}}
      className={{cx(
        "{BASE}",
        VARIANTS[variant],
        SIZES[size],
        "w-full max-w-[420px] justify-between text-[var(--ds-color-muted-foreground)]",
        className,
      )}}
      onClick={{onOpen}}
      {{...rest}}
    >
      <span className="inline-flex items-center gap-2">
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="1.75" />
          <path d="m21 21-4.3-4.3" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <span>{{placeholder}}</span>
      </span>
      <kbd className={{KBD}} aria-hidden="true">{{shortcut}}</kbd>
    </button>
  );
}}

export default CommandButton;
''',
    showcase=r'''function Showcase() {
  const [opened, setOpened] = React.useState(0);
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">opened {opened}×</span></div>
        <div className="ds-stack">
          <CommandButton variant="outline" onOpen={() => setOpened(n => n + 1)} placeholder="Search or run a command…" />
          <CommandButton variant="secondary" onOpen={() => setOpened(n => n + 1)} placeholder="Search docs…" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Sizes</h2><span className="ds-note">sm → lg</span></div>
        <div className="ds-stack">
          <CommandButton size="sm" onOpen={() => setOpened(n => n + 1)} placeholder="Search…" shortcut="⌘K" />
          <CommandButton size="md" onOpen={() => setOpened(n => n + 1)} placeholder="Search or run a command…" />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>In context</h2><span className="ds-note">topbar placement</span></div>
        <div className="ds-canvas" style={{ maxWidth: 720 }}>
          <CommandButton onOpen={() => setOpened(n => n + 1)} />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ================================================ floating-action-button ===
register(
    "floating-action-button",
    title="Floating Action Button",
    eyebrow="React Component",
    lede="A primary compose action hovering over content. Circular, elevated (shadow-md), fixed to a corner. Icon + optional label (extended FAB). `aria-label` is required. Reserve one per screen for the primary creation action.",
    subcategory="Navigation",
    tags=["button", "react", "tailwind", "fab", "floating", "compose", "navigation", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["add-button", "solid-button", "sticky-action-button"],
    props_doc={
        "usage": '<FloatingActionButton icon={<Plus />} label="New invoice" position="bottom-right" onClick={create} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `icon` | `ReactNode` | — (required; the action icon) |\n| `label` | `string` | — (required: accessible name; visible when `extended`) |\n| `position` | `bottom-right \\| bottom-left \\| top-right` | `bottom-right` |\n| `extended` | `boolean` | `false` (icon+label pill when true) |\n| `disabled` | `boolean` | `false` |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`.",
    },
    variants_doc="Single solid circular FAB; extended mode renders an icon+label pill. Fixed to a viewport corner.",
    sizes_doc="Default 56px (icon-only) / 48px tall extended. Meets 44px touch target.",
    states_doc="default · hover (subtle lift) · focus-visible · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " `label` is required and rendered as `aria-label`. Hover lift respects reduced motion. The FAB is `position: fixed` — keep exactly one per screen.",
    notes_doc="Reserve for the single primary creation action on a screen (compose, new invoice, new ticket). Don't use for navigation; that's a navbar/back-button's job.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — FloatingActionButton
 * Primary compose action hovering over content. Circular, elevated,
 * fixed to a corner. aria-label required. One per screen.
 */

export type FabPosition = "bottom-right" | "bottom-left" | "top-right";

export interface FloatingActionButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  icon: ReactNode;
  label: string;
  position?: FabPosition;
  extended?: boolean;
}}

{CX}

const POS: Record<FabPosition, string> = {{
  "bottom-right": "bottom-6 right-6",
  "bottom-left": "bottom-6 left-6",
  "top-right": "top-6 right-6",
}};

export function FloatingActionButton({{
  icon,
  label,
  position = "bottom-right",
  extended = false,
  disabled,
  className,
  type = "button",
  ...rest
}}: FloatingActionButtonProps) {{
  return (
    <button
      type={{type}}
      aria-label={{label}}
      className={{cx(
        "fixed z-40 inline-flex items-center justify-center gap-2 rounded-full",
        "border border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]",
        "shadow-[var(--ds-shadow-md)] transition-transform duration-150 ease-out motion-reduce:transition-none",
        "hover:-translate-y-0.5 active:translate-y-0",
        "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
        "disabled:pointer-events-none disabled:opacity-50",
        extended ? "h-12 px-5 text-sm [&_svg]:size-5" : "size-14 p-0 [&_svg]:size-5",
        POS[position],
        className,
      )}}
      disabled={{disabled}}
      {{...rest}}
    >
      {{icon}}
      {{extended && <span>{{label}}</span>}}
    </button>
  );
}}

export default FloatingActionButton;
''',
    showcase=r'''function PlusIcon() {
  return (<svg className="shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 5v14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /><path d="M5 12h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></svg>);
}
function Showcase() {
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Circular</h2><span className="ds-note">corners</span></div>
        <div className="ds-row">
          <div className="ds-canvas" style={{ position: "relative", height: 120, overflow: "hidden" }}>
            <FloatingActionButton icon={<PlusIcon />} label="New invoice" onClick={() => {}} />
          </div>
          <div className="ds-canvas" style={{ position: "relative", height: 120, overflow: "hidden" }}>
            <FloatingActionButton icon={<PlusIcon />} label="New" position="bottom-left" onClick={() => {}} />
          </div>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Extended</h2><span className="ds-note">icon + label pill</span></div>
        <div className="ds-row">
          <div className="ds-canvas" style={{ position: "relative", height: 120, overflow: "hidden" }}>
            <FloatingActionButton extended icon={<PlusIcon />} label="New invoice" onClick={() => {}} />
          </div>
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Disabled</h2><span className="ds-note">reduced opacity</span></div>
        <div className="ds-canvas" style={{ position: "relative", height: 120, overflow: "hidden" }}>
          <FloatingActionButton icon={<PlusIcon />} label="New invoice, disabled" disabled />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ====================================================== sticky-action-button =
register(
    "sticky-action-button",
    title="Sticky Action Button",
    eyebrow="React Component",
    lede="A persistent primary CTA that sticks to the bottom of the viewport with a hairline top border and a translucent surface so content scrolls beneath. Use for the single primary action on long forms or review screens.",
    subcategory="Composite",
    tags=["button", "react", "tailwind", "sticky", "cta", "persistent", "composite", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["solid-button", "floating-action-button", "loading-button"],
    props_doc={
        "usage": '<StickyActionButton onClick={submit} loading={saving}>Submit order</StickyActionButton>',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `children` | `ReactNode` | — |\n| `variant` | `solid \\| destructive \\| success` | `solid` |\n| `loading` | `boolean` | `false` |\n| `disabled` | `boolean` | `false` |\n| `iconLeft` / `iconRight` | `ReactNode` | — |\n\nPlus all native `ButtonHTMLAttributes<HTMLButtonElement>`. The component renders a sticky bar wrapping the action.",
    },
    variants_doc="solid (default) · destructive · success. The bar is sticky with a hairline top border and a translucent backdrop-blurred surface.",
    sizes_doc="Always `lg` block (full-width) inside the bar — it's the single primary action on a long surface.",
    states_doc="default · hover · active · focus-visible · loading (spinner + `aria-busy`, disabled) · disabled (reduced opacity).",
    a11y_doc=A11Y_NATIVE + " The bar is a landmark-free wrapper; the action is a full-width block button so it's an unambiguous primary target. Reduced motion disables the bar's backdrop transition.",
    notes_doc="Use for the single primary action on long forms or review screens (Submit order, Confirm and pay). Pair with a non-destructive escape above if needed.",
    tsx=f'''import type {{ ButtonHTMLAttributes, ReactNode }} from "react";

/* DevSnips React — StickyActionButton
 * Persistent primary CTA. Sticks to the bottom of the viewport with a
 * hairline top border + translucent backdrop-blurred surface. Single
 * full-width block action.
 */

export type StickyVariant = "solid" | "destructive" | "success";

export interface StickyActionButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {{
  variant?: StickyVariant;
  loading?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
}}

{CX}

{SPINNER}

const SIZES_LG = "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]";

const VARIANTS: Record<StickyVariant, string> = {{
  solid: "{V_SOLID}",
  destructive: "{V_DESTRUCTIVE}",
  success: "{V_SUCCESS}",
}};

export function StickyActionButton({{
  children,
  variant = "solid",
  loading = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}}: StickyActionButtonProps) {{
  const isDisabled = disabled || loading;
  return (
    <div
      className={{cx(
        "sticky bottom-0 left-0 right-0 z-20 flex items-center gap-3",
        "border-t border-[var(--ds-color-border)] bg-[color-mix(in_srgb,var(--ds-color-background)_88%,transparent)]",
        "px-0 py-3 backdrop-blur",
        className,
      )}}
    >
      <button
        type={{type}}
        className={{cx(
          "{BASE}",
          VARIANTS[variant],
          SIZES_LG,
          "w-full",
          className,
        )}}
        disabled={{isDisabled}}
        aria-busy={{loading || undefined}}
        {{...rest}}
      >
        {{loading ? <Spinner /> : iconLeft}}
        <span>{{children}}</span>
        {{!loading && iconRight}}
      </button>
    </div>
  );
}}

export default StickyActionButton;
''',
    showcase=r'''function Showcase() {
  const [busy, setBusy] = React.useState(false);
  function run() { setBusy(true); setTimeout(() => setBusy(false), 1600); }
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Variants</h2><span className="ds-note">solid · destructive · success</span></div>
        <div className="ds-stack">
          <div className="ds-canvas" style={{ padding: 0, overflow: "hidden" }}>
            <div style={{ height: 96, padding: 16, color: "var(--ds-color-muted-foreground)", fontSize: 13 }}>Scrollable review content above the action…</div>
            <StickyActionButton variant="solid" onClick={run} loading={busy}>{busy ? "Submitting…" : "Submit order"}</StickyActionButton>
          </div>
          <div className="ds-canvas" style={{ padding: 0, overflow: "hidden" }}>
            <div style={{ height: 64, padding: 16, color: "var(--ds-color-muted-foreground)", fontSize: 13 }}>Account deletion review…</div>
            <StickyActionButton variant="destructive" iconLeft={<Icon name="trash" className="shrink-0" />}>Delete account permanently</StickyActionButton>
          </div>
          <div className="ds-canvas" style={{ padding: 0, overflow: "hidden" }}>
            <div style={{ height: 64, padding: 16, color: "var(--ds-color-muted-foreground)", fontSize: 13 }}>Publish review…</div>
            <StickyActionButton variant="success">Publish changes</StickyActionButton>
          </div>
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)


# ====================================================== pagination-button ===
register(
    "pagination-button",
    title="Pagination Button",
    eyebrow="React Component",
    lede="Page navigation for paginated lists and tables. Renders Prev, a windowed number set with ellipses, and Next. The active page uses `surface-active` + `aria-current=\"page\"`. Prev/Next disable at the bounds (kept perceivable, not removed).",
    subcategory="Navigation",
    tags=["button", "react", "tailwind", "pagination", "navigation", "table", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["back-button", "sort-button", "button-group"],
    props_doc={
        "usage": '<PaginationButton page={page} totalPages={12} onPageChange={setPage} />',
        "table": "| Prop | Type | Default |\n|---|---|---|\n| `page` | `number` | `1` (current) |\n| `totalPages` | `number` | `1` |\n| `onPageChange` | `(page: number) => void` | — |\n| `size` | `ButtonSize` | `sm` |\n| `siblingCount` | `number` | `1` (pages shown either side of current) |\n\nPlus all native `HTMLAttributes<HTMLElement>`.",
    },
    variants_doc="Single ghost style. Prev/Next are icon-only; numbered pages are square-ish buttons. Active page: `surface-active` + `aria-current=\"page\"` + border-strong.",
    sizes_doc=SIZES_DOC + " Default is `sm`.",
    states_doc="default · hover · focus-visible · current (`aria-current=\"page\"`, surface-active + border-strong) · disabled Prev/Next at bounds (`aria-disabled`, reduced opacity).",
    a11y_doc="Renders a `<nav aria-label=\"Pagination\">`. Each page button has `aria-label=\"Page N\"`; the current page has `aria-current=\"page\"`. Prev/Next have `aria-label` and `aria-disabled` at the bounds (kept visible so the affordance stays perceivable). Focus-visible ring on every control.",
    notes_doc="Keep `siblingCount` modest (1–2) so the control stays compact. For very large counts, consider a jump-to-page input alongside.",
    tsx=f'''import type {{ HTMLAttributes }} from "react";

/* DevSnips React — PaginationButton
 * Page navigation. Prev + windowed numbers (with ellipses) + Next. Active
 * page uses surface-active + aria-current="page". Prev/Next disable at the
 * bounds (aria-disabled, not removed).
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface PaginationButtonProps extends HTMLAttributes<HTMLElement> {{
  page?: number;
  totalPages?: number;
  onPageChange?: (page: number) => void;
  size?: ButtonSize;
  siblingCount?: number;
}}

{CX}

const SIZES: Record<ButtonSize, string> = {{
  xs: "h-7 min-w-7 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 min-w-8 px-2.5 text-xs [&_svg]:size-[14px]",
  md: "h-9 min-w-9 px-3 text-[13px] [&_svg]:size-4",
  lg: "h-10 min-w-10 px-3 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 min-w-11 px-3.5 text-sm [&_svg]:size-5",
}};

function range(s: number, e: number): number[] {{
  const r: number[] = [];
  for (let i = s; i <= e; i++) r.push(i);
  return r;
}}

export function PaginationButton({{
  page = 1,
  totalPages = 1,
  onPageChange,
  size = "sm",
  siblingCount = 1,
  className,
  ...rest
}}: PaginationButtonProps) {{
  function pages(): Array<number | "ellipsis"> {{
    if (totalPages <= 7) return range(1, totalPages);
    const left = Math.max(2, page - siblingCount);
    const right = Math.min(totalPages - 1, page + siblingCount);
    const out: Array<number | "ellipsis"> = [1];
    if (left > 2) out.push("ellipsis");
    out.push(...range(left, right));
    if (right < totalPages - 1) out.push("ellipsis");
    out.push(totalPages);
    return out;
  }}
  function go(p: number) {{ if (p >= 1 && p <= totalPages && p !== page) onPageChange?.(p); }}

  const BTN =
    "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none " +
    "transition-colors duration-150 ease-out motion-reduce:transition-none " +
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";
  const GHOST = "border-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]";
  const ELL = "inline-flex items-center justify-center text-[var(--ds-color-muted-foreground)]";

  return (
    <nav aria-label="Pagination" className={{cx("inline-flex items-center gap-1", className)}} {{...rest}}>
      <button
        type="button"
        className={{cx(BTN, GHOST, SIZES[size], "px-0", page <= 1 && "pointer-events-none opacity-50")}}
        aria-label="Previous page"
        aria-disabled={{page <= 1 || undefined}}
        disabled={{page <= 1}}
        onClick={{() => go(page - 1)}}
      >
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m15 6-6 6 6 6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </button>
      {{pages().map((p, i) =>
        p === "ellipsis" ? (
          <span key={{`e${{i}}`}} className={{cx(ELL, SIZES[size])}} aria-hidden="true">…</span>
        ) : (
          <button
            key={{p}}
            type="button"
            className={{cx(
              BTN,
              p === page
                ? "border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface-active)] font-semibold"
                : "border-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]",
              SIZES[size],
            )}}
            aria-current={{p === page ? "page" : undefined}}
            aria-label={{`Page ${{p}}`}}
            onClick={{() => go(p)}}
          >
            {{p}}
          </button>
        ),
      )}}
      <button
        type="button"
        className={{cx(BTN, GHOST, SIZES[size], "px-0", page >= totalPages && "pointer-events-none opacity-50")}}
        aria-label="Next page"
        aria-disabled={{page >= totalPages || undefined}}
        disabled={{page >= totalPages}}
        onClick={{() => go(page + 1)}}
      >
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m9 6 6 6-6 6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </button>
    </nav>
  );
}}

export default PaginationButton;
''',
    showcase=r'''function Showcase() {
  const [page, setPage] = React.useState(5);
  const [big, setBig] = React.useState(42);
  return (
    <div className="ds-stack">
      <section className="ds-section">
        <div className="ds-section-h"><h2>Few pages</h2><span className="ds-note">no ellipsis</span></div>
        <div className="ds-row">
          <PaginationButton page={page} totalPages={5} onPageChange={setPage} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Many pages</h2><span className="ds-note">windowed with ellipses</span></div>
        <div className="ds-row">
          <PaginationButton page={big} totalPages={90} onPageChange={setBig} />
        </div>
      </section>
      <section className="ds-section">
        <div className="ds-section-h"><h2>Bounds</h2><span className="ds-note">Prev/Next disabled at ends</span></div>
        <div className="ds-row">
          <PaginationButton page={1} totalPages={8} onPageChange={() => {}} />
          <PaginationButton page={8} totalPages={8} onPageChange={() => {}} />
        </div>
      </section>
    </div>
  );
}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
''',
)

print("registry loaded")
