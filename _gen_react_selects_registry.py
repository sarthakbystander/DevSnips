"""Registry for the DevSnips React Selects generator.

Each ``register()`` call below adds one select variant's metadata + showcase +
README docs. The generator (``_gen_react_selects.py``) reads each component's
``code.tsx`` from disk and combines it with the spec here to write
``code.jsx``, ``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented content only (Environment, Team member, Project,
Country, Timezone, Language). No lorem ipsum, no marketing buzzwords.
"""
from _gen_react_selects import register

# Shared option sets reused across several showcases (defined as Python lists
# of dicts; the showcase JSX references them by name via a const in the
# Showcase function — but to keep each preview standalone, each Showcase
# declares its own inline options array).

FEAT = ["responsive", "light/dark", "reduced-motion", "focus-visible", "semantic HTML", "keyboard accessible"]
A11Y = ["focus-visible", "keyboard accessible", "ARIA", "semantic HTML", "associated labels"]

# ---------------------------------------------------------------------------
# 1. native-select
# ---------------------------------------------------------------------------
register(
    "native-select",
    title="Native Select",
    subcategory="Native",
    description="Genuine native select element styled to match the DevSnips select language.",
    tags=["select", "form", "native", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-label", "select-with-helper"],
    props_doc={
        "export_name": "NativeSelect",
        "usage": '<NativeSelect label="Environment" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `string` | `\"Select\"` | Visible label. |\n| `options` | `{value,label,disabled?}[]` | — | Option list. |\n| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled value. |\n| `onChange` | `(value, option) => void` | — | Selection callback. |\n| `size` | `\"sm\" \\| \"md\" \\| \"lg\"` | `\"md\"` | Control height. |\n| `placeholder` | `string` | `\"Select an option\"` | First disabled option. |\n| `disabled` | `boolean` | — | Disables the select. |\n| native `<select>` attrs | — | — | `name`, `id`, `aria-*`. |",
    },
    behavior_doc="Uses the browser's native `<select>` for full native behavior (form submission, mobile picker, platform conventions). A chevron overlay is positioned over the native control to match the custom select visual language.",
    a11y_doc="Native `<select>` + `<option>` elements are accessible by default. A visible `<label htmlFor>` associates the field; `aria-invalid` and `aria-describedby` wire error/helper text.",
    notes_doc="Use native-select when you need native form semantics and platform pickers (especially mobile). Use the custom `select` when you need custom interaction or styling the native control cannot provide.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  const [val, setVal] = React.useState("production");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <NativeSelect label="Environment" options={envs} value={val} onChange={(v)=>setVal(v)} />
      <NativeSelect label="With helper" helperText="Deploys trigger on selection." options={envs} defaultValue="staging" />
      <NativeSelect label="Error" error="Select a valid environment." options={envs} />
      <NativeSelect label="Disabled" options={envs} disabled defaultValue="production" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 2. select  (reference)
# ---------------------------------------------------------------------------
register(
    "select",
    title="Select",
    subcategory="Core",
    description="Custom accessible select implementing the WAI-ARIA combobox/listbox pattern with full keyboard navigation.",
    tags=["select", "dropdown", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["native-select", "searchable-select", "select-with-label", "select-with-error"],
    props_doc={
        "export_name": "Select",
        "usage": '<Select label="Environment" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `string` | `\"Select\"` | Visible label. |\n| `options` | `{value,label,disabled?}[]` | — | Option list. |\n| `value` / `defaultValue` | `string` | `\"\"` | Controlled / uncontrolled value. |\n| `onChange` | `(value, option) => void` | — | Selection callback. |\n| `size` | `\"sm\" \\| \"md\" \\| \"lg\"` | `\"md\"` | Control height. |\n| `placeholder` | `string` | `\"Select an option\"` | Placeholder text. |\n| `disabled` | `boolean` | — | Disables the trigger. |\n| `leadingIcon` | `ReactNode` | — | Icon at the trigger left. |\n| `error` / `success` / `helperText` | `string` | — | Message + state. |",
    },
    behavior_doc="Click the trigger (or focus + ArrowDown) to open the listbox. ArrowUp/Down moves the active option (skipping disabled), Home/End jump to the first/last enabled option, Enter/Space selects, Escape closes, Tab closes. Selecting closes the panel and returns focus to the trigger. Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes both supported.",
    a11y_doc="Trigger `<button aria-haspopup=\"listbox\" aria-expanded aria-controls aria-activedescendant>`; panel `role=\"listbox\"`; options `role=\"option\" aria-selected`. `aria-invalid` for errors, `aria-describedby` for helper/error/success text. Outside-click and Escape close. Visible `focus-visible` ring.",
    notes_doc="This is the reference implementation for the Selects family — it establishes the shared dimensions, border, radius, focus treatment, dropdown panel, option spacing, selected/hover/disabled states, and dark-mode behavior that every other select extends.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"},{value:"archived",label:"Archived",disabled:true}];
  const [val, setVal] = React.useState("production");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <Select label="Environment" options={envs} value={val} onChange={(v)=>setVal(v)} helperText="Selects deploy target on change." />
      <Select label="With error" error="Choose a deploy target." options={envs} />
      <Select label="Disabled" options={envs} disabled defaultValue="staging" />
      <Select label="Sizes" size="sm" options={envs} defaultValue="development" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 3. select-with-label
# ---------------------------------------------------------------------------
register(
    "select-with-label",
    title="Select With Label",
    subcategory="Label",
    description="Custom select with an always-rendered associated label.",
    tags=["select", "form", "label", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-helper", "select-with-error"],
    props_doc={
        "export_name": "SelectWithLabel",
        "usage": '<SelectWithLabel label="Project" options={[{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"}]} defaultValue="devsnips" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `string` | `\"Field\"` | Visible label (always rendered). |\n| `options` | `{value,label,disabled?}[]` | — | Option list. |\n| `value` / `defaultValue` | `string` | — | Controlled / uncontrolled. |\n| `onChange` | `(value, option) => void` | — | Selection callback. |\n| `size` / `placeholder` / `id` / `name` / `className` | — | — | Standard. |",
    },
    behavior_doc="Same combobox/listbox behavior as the reference `Select`: click/ArrowDown opens, ArrowUp/Down/Home/End navigate, Enter/Space selects, Escape closes.",
    a11y_doc="`<label htmlFor>` pairs the visible label with the trigger. Full ARIA listbox pattern.",
    notes_doc="Use when the label is the primary structural emphasis and must always be present.",
    showcase="""function Showcase() {
  const projects = [{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"},{value:"techflue",label:"TechFlue"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithLabel label="Project" options={projects} defaultValue="devsnips" />
      <SelectWithLabel label="Workspace" options={projects} defaultValue="lensdev" />
      <SelectWithLabel label="Repository" options={projects} placeholder="Choose a repository" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 4. select-with-helper
# ---------------------------------------------------------------------------
register(
    "select-with-helper",
    title="Select With Helper",
    subcategory="Feedback",
    description="Custom select with helper text linked through aria-describedby.",
    tags=["select", "form", "helper", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-label", "select-with-error"],
    props_doc={
        "export_name": "SelectWithHelper",
        "usage": '<SelectWithHelper label="Team member" helperText="Owner receives deploy notifications." options={opts} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `string` | `\"Select\"` | Visible label. |\n| `helperText` | `string` | — | Supporting text (`aria-describedby`). |\n| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |",
    },
    behavior_doc="Reference combobox/listbox behavior plus a helper message below the field.",
    a11y_doc="Helper text is linked to the trigger via `aria-describedby` and announced by screen readers.",
    notes_doc="Pair with `select-with-error` / `select-with-success` when validation feedback is needed.",
    showcase="""function Showcase() {
  const members = [{value:"sarthak",label:"Sarthak"},{value:"alex",label:"Alex"},{value:"maya",label:"Maya"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithHelper label="Team member" helperText="Owner receives deploy notifications." options={members} defaultValue="sarthak" />
      <SelectWithHelper label="Reviewer" helperText="Optional — defaults to the project owner." options={members} />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 5. select-with-error
# ---------------------------------------------------------------------------
register(
    "select-with-error",
    title="Select With Error",
    subcategory="Feedback",
    description="Custom select with an error message and aria-invalid state.",
    tags=["select", "form", "error", "validation", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-helper", "select-with-success"],
    props_doc={
        "export_name": "SelectWithError",
        "usage": '<SelectWithError label="Environment" error="Select a deploy target." options={opts} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `string` | `\"Select\"` | Visible label. |\n| `error` | `string` | — | Error message; sets `aria-invalid`. |\n| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |",
    },
    behavior_doc="Reference combobox/listbox behavior with a destructive border + error message when `error` is set.",
    a11y_doc="`aria-invalid=\"true\"` on the trigger; error message linked via `aria-describedby`. State is communicated by border + text, not color alone.",
    notes_doc="Clear the `error` prop once the user makes a valid selection.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithError label="Environment" error="Select a deploy target before saving." options={envs} />
      <SelectWithError label="Region" error="This region is at capacity." options={[{value:"us-east",label:"US East"},{value:"eu-west",label:"EU West"}]} />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 6. select-with-success
# ---------------------------------------------------------------------------
register(
    "select-with-success",
    title="Select With Success",
    subcategory="Feedback",
    description="Custom select with a success message and confirmation state.",
    tags=["select", "form", "success", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-helper", "select-with-error"],
    props_doc={
        "export_name": "SelectWithSuccess",
        "usage": '<SelectWithSuccess label="Environment" success="Deploy target verified." options={opts} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `string` | `\"Select\"` | Visible label. |\n| `success` | `string` | — | Success message; sets success border. |\n| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |",
    },
    behavior_doc="Reference combobox/listbox behavior with a success border + confirmation message.",
    a11y_doc="Success message linked via `aria-describedby`. State uses border + text + check indicator, not color alone.",
    notes_doc="Use to confirm a valid selection (e.g. a verified deploy target).",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithSuccess label="Environment" success="Deploy target verified." options={envs} defaultValue="production" />
      <SelectWithSuccess label="Database" success="Connection pool healthy." options={[{value:"pg",label:"Postgres"},{value:"mysql",label:"MySQL"}]} defaultValue="pg" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 7. select-disabled
# ---------------------------------------------------------------------------
register(
    "select-disabled",
    title="Select Disabled",
    subcategory="State",
    description="Custom select demonstrating the disabled, non-interactive state.",
    tags=["select", "form", "disabled", "state", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-readonly", "select-with-loading"],
    props_doc={
        "export_name": "SelectDisabled",
        "usage": '<SelectDisabled label="Environment" options={opts} disabled defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `disabled` | `boolean` | `true` | Disables the trigger. |\n| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |",
    },
    behavior_doc="When `disabled`, the trigger is non-interactive (`pointer-events-none`, muted surface, reduced opacity). ARIA is preserved so the control remains perceivable.",
    a11y_doc="`disabled` on the trigger; `aria-disabled` reflected. Disabled state uses opacity + muted surface, not just color.",
    notes_doc="Defaults to `disabled` to showcase the state; pass `disabled={false}` to make it interactive.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectDisabled label="Environment (locked)" options={envs} disabled defaultValue="production" />
      <SelectDisabled label="Region (locked)" options={[{value:"us-east",label:"US East"},{value:"eu-west",label:"EU West"}]} disabled defaultValue="us-east" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 8. select-readonly
# ---------------------------------------------------------------------------
register(
    "select-readonly",
    title="Select Readonly",
    subcategory="State",
    description="Custom select in a read-only state: value locked but readable, not greyed-out.",
    tags=["select", "form", "readonly", "state", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-disabled", "inline-edit-select"],
    props_doc={
        "export_name": "SelectReadonly",
        "usage": '<SelectReadonly label="Environment" options={opts} readOnly defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `readOnly` | `boolean` | `true` | Renders a static, non-editable display. |\n| `label` / `options` / `value` / `defaultValue` / `size` | — | — | As reference. |",
    },
    behavior_doc="When `readOnly`, the value renders as a static, non-interactive display (not a button) — readable but not changeable. Distinct from `disabled`: not greyed-out, just locked. Falls back to the interactive trigger when `readOnly={false}`.",
    a11y_doc="Static display uses `role=\"textbox\" aria-readonly=\"true\"` so screen readers announce a read-only value. A lock affordance signals the state non-color-wise.",
    notes_doc="Use for values a user can see but not edit (e.g. an inherited environment). For editable-but-currently-locked, see `inline-edit-select`.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectReadonly label="Environment (inherited)" options={envs} readOnly defaultValue="production" />
      <SelectReadonly label="Plan (inherited)" options={[{value:"team",label:"Team"},{value:"enterprise",label:"Enterprise"}]} readOnly defaultValue="team" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 9. select-with-leading-icon
# ---------------------------------------------------------------------------
register(
    "select-with-leading-icon",
    title="Select With Leading Icon",
    subcategory="Icon",
    description="Custom select with a meaningful leading icon inside the trigger.",
    tags=["select", "form", "icon", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-avatar", "searchable-select"],
    props_doc={
        "export_name": "SelectWithLeadingIcon",
        "usage": '<SelectWithLeadingIcon label="Repository" leadingIcon={<SearchIcon/>} options={opts} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `leadingIcon` | `ReactNode` | — | Icon rendered at the trigger left. |\n| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` | — | — | As reference. |",
    },
    behavior_doc="Reference combobox/listbox behavior. The leading icon is decorative (`aria-hidden`) and shifts the trigger content with `pl-9`.",
    a11y_doc="Leading icon is `aria-hidden`; the trigger remains fully labeled and keyboard-operable.",
    notes_doc="Use a leading icon only when it adds meaning (e.g. a search icon for a filterable context). Avoid decorative icons.",
    showcase="""function Showcase() {
  const projects = [{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"},{value:"techflue",label:"TechFlue"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithLeadingIcon label="Repository" options={projects} defaultValue="devsnips" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 10. select-with-placeholder
# ---------------------------------------------------------------------------
register(
    "select-with-placeholder",
    title="Select With Placeholder",
    subcategory="Presentation",
    description="Custom select emphasizing a prominent placeholder when nothing is selected.",
    tags=["select", "form", "placeholder", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-label", "native-select"],
    props_doc={
        "export_name": "SelectWithPlaceholder",
        "usage": '<SelectWithPlaceholder label="Project" placeholder="Choose a project" options={opts} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `placeholder` | `string` | `\"Choose\\u2026\"` | Placeholder when no value. |\n| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` | — | — | As reference. |",
    },
    behavior_doc="Reference combobox/listbox behavior. Placeholder shows in muted foreground until a selection is made.",
    a11y_doc="Placeholder is presentational; the field is labeled and keyboard-accessible.",
    notes_doc="Placeholders are never critical information — use them for guidance, not as a substitute for a label.",
    showcase="""function Showcase() {
  const projects = [{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"},{value:"techflue",label:"TechFlue"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithPlaceholder label="Project" placeholder="Choose a project" options={projects} />
      <SelectWithPlaceholder label="Workspace" placeholder="Select a workspace" options={projects} defaultValue="devsnips" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 11. searchable-select
# ---------------------------------------------------------------------------
register(
    "searchable-select",
    title="Searchable Select",
    subcategory="Search",
    description="Combobox select with a real search input that filters options.",
    tags=["select", "combobox", "search", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "combobox", "multi-select-with-search", "command-select"],
    props_doc={
        "export_name": "SearchableSelect",
        "usage": '<SearchableSelect label="Environment" options={opts} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,disabled?}[]` | — | Option list. |\n| `value` / `defaultValue` / `onChange` | — | — | Controlled / uncontrolled. |\n| `searchPlaceholder` | `string` | `\"Search options\"` | Input placeholder. |\n| `placeholder` / `size` / `label` / `id` / `name` / `className` | — | — | Standard. |",
    },
    behavior_doc="Trigger opens a panel with a search input (autofocused) above a filtered listbox. Typing filters options by label (case-insensitive substring). ArrowDown/Up moves the active option among filtered results, Home/End jump, Enter selects, Escape closes and clears the search. An empty-results state shows \"No matches\".",
    a11y_doc="Search input is `role=\"combobox\" aria-expanded aria-controls aria-activedescendant aria-autocomplete=\"list\"`; listbox `role=\"listbox\"`; options `role=\"option\" aria-selected`.",
    notes_doc="Use when the option list is long enough that filtering helps. For free-text input see `combobox`; for multiple selection with search see `multi-select-with-search`.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"},{value:"preview",label:"Preview"},{value:"sandbox",label:"Sandbox"}];
  const [val, setVal] = React.useState("production");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SearchableSelect label="Environment" options={envs} value={val} onChange={(v)=>setVal(v)} />
      <SearchableSelect label="Team member" searchPlaceholder="Search members" options={[{value:"sarthak",label:"Sarthak"},{value:"alex",label:"Alex"},{value:"maya",label:"Maya"},{value:"jordan",label:"Jordan"}]} />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 12. multi-select
# ---------------------------------------------------------------------------
register(
    "multi-select",
    title="Multi Select",
    subcategory="Multi",
    description="Custom listbox supporting multiple selections with restrained count summary.",
    tags=["select", "multi-select", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["multi-select-with-search", "select-with-checkboxes", "select"],
    props_doc={
        "export_name": "MultiSelect",
        "usage": '<MultiSelect label="Tags" options={opts} defaultValue={["backend"]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,disabled?}[]` | — | Option list. |\n| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled values. |\n| `onChange` | `(values: string[], options) => void` | — | Selection callback. |\n| `placeholder` / `size` / `label` / `id` / `name` / `className` | — | — | Standard. |",
    },
    behavior_doc="Trigger shows a restrained summary (0 → placeholder, 1-2 → labels joined by \", \", 3+ → \"N selected\"). Clicking/Enter/Space toggles an option's selection WITHOUT closing the panel (multi stays open). ArrowUp/Down/Home/End navigate; Escape closes.",
    a11y_doc="Options are `role=\"option\" aria-selected`; selected options use a checked indicator + `surface-selected` background + `font-medium`, not color alone.",
    notes_doc="Avoid turning selected values into a pile of pill badges — the count summary keeps the trigger restrained.",
    showcase="""function Showcase() {
  const tags = [{value:"frontend",label:"Frontend"},{value:"backend",label:"Backend"},{value:"infra",label:"Infrastructure"},{value:"design",label:"Design"},{value:"docs",label:"Documentation"}];
  const [sel, setSel] = React.useState(["backend","infra"]);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <MultiSelect label="Project tags" options={tags} value={sel} onChange={(v)=>setSel(v)} />
      <MultiSelect label="Notifications" options={[{value:"email",label:"Email"},{value:"push",label:"Push"},{value:"slack",label:"Slack"}]} defaultValue={["email"]} />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 13. multi-select-with-search
# ---------------------------------------------------------------------------
register(
    "multi-select-with-search",
    title="Multi Select With Search",
    subcategory="Multi",
    description="Multi-select combined with a search filter over the options.",
    tags=["select", "multi-select", "search", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["multi-select", "searchable-select", "command-select"],
    props_doc={
        "export_name": "MultiSelectWithSearch",
        "usage": '<MultiSelectWithSearch label="Members" options={opts} defaultValue={["sarthak"]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,disabled?}[]` | — | Option list. |\n| `value` / `defaultValue` | `string[]` | `[]` | Controlled / uncontrolled. |\n| `onChange` | `(values, options) => void` | — | Selection callback. |\n| `searchPlaceholder` / `placeholder` / `size` / `label` | — | — | Standard. |",
    },
    behavior_doc="Trigger shows a count summary. Panel has a search input + filtered checkbox options. Typing filters; ArrowDown/Up moves active among filtered; Enter/Space toggles (panel stays open); Escape closes and clears the search. Empty-results state included.",
    a11y_doc="Combobox + listbox + `role=\"option\" aria-selected` pattern. Focus remains predictable: the search input is the panel's primary focus.",
    notes_doc="Use when selecting multiple items from a large list (e.g. assigning many team members).",
    showcase="""function Showcase() {
  const members = [{value:"sarthak",label:"Sarthak"},{value:"alex",label:"Alex"},{value:"maya",label:"Maya"},{value:"jordan",label:"Jordan"},{value:"sam",label:"Sam"},{value:"rin",label:"Rin"}];
  const [sel, setSel] = React.useState(["sarthak","maya"]);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <MultiSelectWithSearch label="Assignees" options={members} value={sel} onChange={(v)=>setSel(v)} searchPlaceholder="Search members" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 14. select-with-groups
# ---------------------------------------------------------------------------
register(
    "select-with-groups",
    title="Select With Groups",
    subcategory="Grouped",
    description="Custom single-select with grouped options and accessible group dividers.",
    tags=["select", "groups", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["command-select", "select", "select-with-description"],
    props_doc={
        "export_name": "SelectWithGroups",
        "usage": '<SelectWithGroups label="Resource" groups={[{label:"Fruits",options:[...]},{label:"Vegetables",options:[...]}]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `groups` | `{label:string; options:{value,label,disabled?}[]}[]` | — | Grouped options. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="Group labels render as non-interactive dividers. Keyboard navigation skips group labels — only options are navigable for `activeIndex`. Selected option shows a check.",
    a11y_doc="Group labels are `role=\"presentation\"` dividers (muted uppercase). Options are `role=\"option\" aria-selected`.",
    notes_doc="Groups are visually distinguished by the muted divider, not excessive decoration.",
    showcase="""function Showcase() {
  const groups = [
    {label:"Environments", options:[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]},
    {label:"Regions", options:[{value:"us-east",label:"US East"},{value:"eu-west",label:"EU West"},{value:"ap-south",label:"AP South"}]},
  ];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithGroups label="Resource" groups={groups} defaultValue="production" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 15. select-with-description
# ---------------------------------------------------------------------------
register(
    "select-with-description",
    title="Select With Description",
    subcategory="Presentation",
    description="Custom single-select where options carry a label and a description.",
    tags=["select", "description", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-groups", "select-with-avatar"],
    props_doc={
        "export_name": "SelectWithDescription",
        "usage": '<SelectWithDescription label="Environment" options={[{value:"production",label:"Production",description:"Live production environment"}]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,description?,disabled?}[]` | — | Options with descriptions. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="Option rows show a label (medium) + description (muted `text-xs`). Rows stay compact. Selected option shows a check on the right. Full keyboard nav.",
    a11y_doc="Options are `role=\"option\" aria-selected`; description text is readable by screen readers.",
    notes_doc="Keep option rows compact — do not make them unnecessarily tall.",
    showcase="""function Showcase() {
  const envs = [
    {value:"production",label:"Production",description:"Live production environment"},
    {value:"staging",label:"Staging",description:"Pre-release testing environment"},
    {value:"development",label:"Development",description:"Local development environment"},
  ];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithDescription label="Environment" options={envs} defaultValue="production" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 16. select-with-avatar
# ---------------------------------------------------------------------------
register(
    "select-with-avatar",
    title="Select With Avatar",
    subcategory="Presentation",
    description="Custom select where each option may carry an avatar shown in trigger and rows.",
    tags=["select", "avatar", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-description", "select-with-leading-icon"],
    props_doc={
        "export_name": "SelectWithAvatar",
        "usage": '<SelectWithAvatar label="Assignee" options={[{value:"sarthak",label:"Sarthak",avatar:<Avatar/>}]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,avatar?:ReactNode,description?,disabled?}[]` | — | Options with optional avatar. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="The selected option's avatar + label show in the trigger. Option rows show the avatar + label (+ optional description). Avatar slot is a 20px circle; a fallback initials square renders when no avatar is supplied.",
    a11y_doc="Avatars are decorative (`aria-hidden`); the option label carries the accessible name.",
    notes_doc="Does not require an external avatar library — pass any ReactNode (image, initials, icon).",
    showcase="""function Showcase() {
  function initials(name){ return name.slice(0,2).toUpperCase(); }
  function Av({name}){ return <span className="inline-flex size-5 items-center justify-center rounded-full bg-[var(--ds-color-surface-subtle)] text-[10px] font-medium text-[var(--ds-color-foreground)]" aria-hidden="true">{initials(name)}</span>; }
  const members = [{value:"sarthak",label:"Sarthak",avatar:<Av name="Sarthak"/>},{value:"alex",label:"Alex",avatar:<Av name="Alex"/>},{value:"maya",label:"Maya",avatar:<Av name="Maya"/>}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithAvatar label="Assignee" options={members} defaultValue="sarthak" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 17. select-with-checkboxes
# ---------------------------------------------------------------------------
register(
    "select-with-checkboxes",
    title="Select With Checkboxes",
    subcategory="Presentation",
    description="Custom single-select where each option row shows a checkbox reflecting selection.",
    tags=["select", "checkbox", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["multi-select", "select", "select-with-clear"],
    props_doc={
        "export_name": "SelectWithCheckboxes",
        "usage": '<SelectWithCheckboxes label="Environment" options={opts} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,disabled?}[]` | — | Option list. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="Each option row has a checkbox indicator that reflects the selected state. Click/Enter/Space selects (single-select: selecting one checks it, the previous selection unchecks) and closes. Keyboard ArrowUp/Down/Home/End navigates.",
    a11y_doc="Options are `role=\"option\" aria-selected`; the checkbox glyph reflects `aria-selected` so state is communicated by shape + background, not color alone.",
    notes_doc="The checkbox is a visual affordance for the single-select state — it is not a multi-select. For multiple selection see `multi-select`.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithCheckboxes label="Environment" options={envs} defaultValue="production" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 18. select-with-clear
# ---------------------------------------------------------------------------
register(
    "select-with-clear",
    title="Select With Clear",
    subcategory="Interactive",
    description="Custom single-select with a clear control that resets the selection.",
    tags=["select", "clear", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-checkboxes", "searchable-select"],
    props_doc={
        "export_name": "SelectWithClear",
        "usage": '<SelectWithClear label="Environment" options={opts} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `clearLabel` | `string` | `\"Clear selection\"` | Accessible label for the clear button. |\n| `onChange` | `(value, option \\| null) => void` | — | Called with `null` on clear. |\n| `options` / `value` / `defaultValue` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="When a value is selected, an `x` clear button appears in the trigger. Clicking it resets the selection to empty and calls `onChange(null, null)`. The clear button stops propagation so it does not open the listbox.",
    a11y_doc="The clear button is a real `<button type=\"button\">` with an `aria-label` (default \"Clear selection\").",
    notes_doc="Clearing is a distinct action from selecting a different option.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  const [val, setVal] = React.useState("production");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithClear label="Environment" options={envs} value={val} onChange={(v)=>setVal(v||"")} />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 19. select-with-actions
# ---------------------------------------------------------------------------
register(
    "select-with-actions",
    title="Select With Actions",
    subcategory="Composite",
    description="Custom select whose dropdown panel has action rows (e.g. Add new, Manage).",
    tags=["select", "actions", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "creatable-select", "select-with-clear"],
    props_doc={
        "export_name": "SelectWithActions",
        "usage": '<SelectWithActions label="Project" options={opts} actions={[{label:"Add new\\u2026",onSelect:()=>{}}]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `actions` | `{label:string; onSelect:()=>void}[]` | — | Footer action rows. |\n| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="The dropdown panel renders options above a divider (`border-t`) and action buttons below. Selecting an action calls `onSelect` and closes the panel. Options use full listbox keyboard nav; actions are separate focusable buttons.",
    a11y_doc="Actions are real `<button>` elements with descriptive labels, reachable by keyboard.",
    notes_doc="Use for selects that need quick inline actions (create a new option, manage the list).",
    showcase="""function Showcase() {
  const projects = [{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"},{value:"techflue",label:"TechFlue"}];
  const [note, setNote] = React.useState("");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithActions label="Project" options={projects} defaultValue="devsnips" actions={[{label:"Add new project\\u2026",onSelect:()=>setNote("Add new project selected.")},{label:"Manage projects\\u2026",onSelect:()=>setNote("Manage projects selected.")}]} />
      {note ? <p className="text-xs text-[var(--ds-color-muted-foreground)]">{note}</p> : null}
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 20. select-with-loading
# ---------------------------------------------------------------------------
register(
    "select-with-loading",
    title="Select With Loading",
    subcategory="State",
    description="Custom select that shows a loading state with aria-busy while options load.",
    tags=["select", "loading", "state", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["async-select", "select-disabled", "select"],
    props_doc={
        "export_name": "SelectWithLoading",
        "usage": '<SelectWithLoading label="Environment" options={opts} loading />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `loading` | `boolean` | — | Shows a spinner + disables interaction (`aria-busy`). |\n| `options` / `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="While `loading` is true, the trigger is non-interactive (`pointer-events-none`), shows `aria-busy=\"true\"`, and a Spinner replaces the chevron. When loading completes, full listbox behavior resumes.",
    a11y_doc="`aria-busy=\"true\"` announces the loading state to assistive technology.",
    notes_doc="For asynchronous option fetching, see `async-select` which wraps this loading state around a `loadOptions` callback.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  const [loading, setLoading] = React.useState(true);
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SelectWithLoading label="Environment" options={envs} loading={loading} defaultValue="production" />
      <button type="button" className="ds-theme-toggle" onClick={()=>setLoading(l=>!l)}>{loading?"Stop loading":"Start loading"}</button>
    </div>
  );
}""",
)


# ---------------------------------------------------------------------------
# 21. async-select
# ---------------------------------------------------------------------------
register(
    "async-select",
    title="Async Select",
    subcategory="Async",
    description="Custom select that loads options asynchronously via a loadOptions callback.",
    tags=["select", "async", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select-with-loading", "creatable-select", "searchable-select"],
    props_doc={
        "export_name": "AsyncSelect",
        "usage": '<AsyncSelect label="Repository" loadOptions={(q)=>Promise.resolve(opts)} defaultOptions />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `loadOptions` | `(query: string) => Promise<{value,label,disabled?}[]>` | — | Async loader. |\n| `defaultOptions` | `{value,label}[] \\| boolean` | — | Initial options or `true` to load on mount. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |\n| `loadingPlaceholder` / `emptyMessage` | `string` | — | Loading + empty copy. |",
    },
    behavior_doc="On open (or mount when `defaultOptions === true`), calls `loadOptions(query)`. Shows a loading spinner (`aria-busy`) while pending, then results. If the promise rejects, shows an error state inside the panel. Empty state when no results. The component performs NO real network requests — it calls the consumer's `loadOptions`.",
    a11y_doc="`aria-busy=\"true\"` during load; loading/empty/error states are text-announced.",
    notes_doc="The preview simulates async loading with a `setTimeout`-wrapped promise. Wire `loadOptions` to your real data source in production.",
    showcase="""function Showcase() {
  const loader = (q) => new Promise((resolve) => {
    const all = [{value:"devsnips",label:"DevSnips"},{value:"lensdev",label:"LensDev"},{value:"techflue",label:"TechFlue"},{value:"atlas",label:"Atlas"},{value:"forge",label:"Forge"}];
    setTimeout(() => resolve(all.filter(o => o.label.toLowerCase().includes((q||"").toLowerCase()))), 600);
  });
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <AsyncSelect label="Repository" loadOptions={loader} defaultOptions placeholder="Search repositories" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 22. creatable-select
# ---------------------------------------------------------------------------
register(
    "creatable-select",
    title="Creatable Select",
    subcategory="Creatable",
    description="Combobox that lets users create a new option when no match exists.",
    tags=["select", "creatable", "combobox", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["combobox", "searchable-select", "select-with-actions"],
    props_doc={
        "export_name": "CreatableSelect",
        "usage": '<CreatableSelect label="Label" options={opts} onCreateOption={(v)=>{}} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,disabled?}[]` | — | Existing options. |\n| `onCreateOption` | `(value: string) => void` | — | Called when a new option is created. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `searchPlaceholder` / `createLabel` | — | — | Standard. |",
    },
    behavior_doc="Type to filter. When the query is non-empty and no exact-match option exists, a `Create \"<query>\"` row appears at the top. Selecting it calls `onCreateOption(query)`, appends the new option to the list, and selects it. ArrowDown/Up navigates, Enter creates/selects, Escape closes+clears.",
    a11y_doc="Combobox + listbox pattern; the create row is `role=\"option\"` with a descriptive label.",
    notes_doc="Implement real persistence in `onCreateOption` (e.g. POST to your API). The preview appends to local state for demonstration.",
    showcase="""function Showcase() {
  const base = [{value:"backend",label:"Backend"},{value:"frontend",label:"Frontend"},{value:"design",label:"Design"}];
  const [opts, setOpts] = React.useState(base);
  const [val, setVal] = React.useState("backend");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CreatableSelect label="Label" options={opts} value={val} onChange={(v)=>setVal(v)} onCreateOption={(v)=>{ setOpts(o=>[...o,{value:v,label:v}]); setVal(v); }} searchPlaceholder="Type to search or create" />
      <p className="text-xs text-[var(--ds-color-muted-foreground)]">Type a new label and choose Create.</p>
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 23. combobox
# ---------------------------------------------------------------------------
register(
    "combobox",
    title="Combobox",
    subcategory="Combobox",
    description="True WAI-ARIA combobox: a text input that filters and selects from a listbox.",
    tags=["combobox", "select", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["searchable-select", "creatable-select", "command-select"],
    props_doc={
        "export_name": "Combobox",
        "usage": '<Combobox label="Environment" options={opts} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label}[]` | — | Option list. |\n| `value` / `defaultValue` / `onChange` | — | — | Controlled / uncontrolled (value = selected value). |\n| `onInputChange` | `(query: string) => void` | — | Input change callback. |\n| `size` / `placeholder` / `label` / `id` / `name` / `className` | — | — | Standard. |",
    },
    behavior_doc="The text INPUT is the trigger (`role=\"combobox\" aria-autocomplete=\"list\"`). Typing filters the listbox below. ArrowDown opens + moves the active option, Enter selects (sets the input to the option label), Escape closes. Distinct from `searchable-select`: here the input itself is the trigger, not a button that opens a panel with a search box.",
    a11y_doc="Input `role=\"combobox\" aria-expanded aria-controls aria-activedescendant aria-autocomplete=\"list\"`; listbox `role=\"listbox\"`; options `role=\"option\" aria-selected`.",
    notes_doc="Use when the user may type a free value OR pick from the list. For pick-only with search, see `searchable-select`.",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"},{value:"preview",label:"Preview"}];
  const [val, setVal] = React.useState("production");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <Combobox label="Environment" options={envs} value={val} onChange={(v)=>setVal(v)} />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 24. command-select
# ---------------------------------------------------------------------------
register(
    "command-select",
    title="Command Select",
    subcategory="Command",
    description="Command-palette-style select with search over grouped options.",
    tags=["select", "command", "search", "groups", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["searchable-select", "select-with-groups", "combobox"],
    props_doc={
        "export_name": "CommandSelect",
        "usage": '<CommandSelect label="Command" groups={[{label:"Environments",options:[...]}]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `groups` | `{label:string; options:{value,label,disabled?}[]}[]` | — | Grouped options. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `searchPlaceholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="Search input + grouped options. Typing filters across all groups (empty groups hidden). ArrowDown/Up moves active among flattened filtered options (skipping group labels); Enter selects; Escape closes. Restrained elevation — no giant glow.",
    a11y_doc="Combobox + listbox; group labels are `role=\"presentation\"` dividers.",
    notes_doc="Keep the visual treatment consistent with DevSnips — elevated panel + border, no command-palette glow effects.",
    showcase="""function Showcase() {
  const groups = [
    {label:"Environments", options:[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]},
    {label:"Regions", options:[{value:"us-east",label:"US East"},{value:"eu-west",label:"EU West"}]},
  ];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CommandSelect label="Command" groups={groups} searchPlaceholder="Type a command" defaultValue="production" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 25. country-select
# ---------------------------------------------------------------------------
register(
    "country-select",
    title="Country Select",
    subcategory="Data",
    description="Single-select listbox for countries with a 2-letter ISO code badge (no emoji flags).",
    tags=["select", "country", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["timezone-select", "language-select", "select"],
    props_doc={
        "export_name": "CountrySelect",
        "usage": '<CountrySelect label="Country" options={[{value:"US",label:"United States",code:"US"}]} defaultValue="US" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,code:string,disabled?}[]` | — | Countries with 2-letter ISO code. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="Each option shows a small square 2-letter code badge (`font-mono text-[10px]`) + label. The trigger shows the selected country's badge + label. Full keyboard nav + ARIA listbox + outside-click.",
    a11y_doc="Code badge is `aria-hidden`; the option label carries the accessible name.",
    notes_doc="Uses a code-badge instead of emoji flags for a restrained, consistent look across platforms.",
    showcase="""function Showcase() {
  const countries = [{value:"US",label:"United States",code:"US"},{value:"CA",label:"Canada",code:"CA"},{value:"GB",label:"United Kingdom",code:"GB"},{value:"DE",label:"Germany",code:"DE"},{value:"IN",label:"India",code:"IN"},{value:"JP",label:"Japan",code:"JP"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <CountrySelect label="Country" options={countries} defaultValue="US" />
      <CountrySelect label="Billing country" options={countries} placeholder="Select a country" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 26. timezone-select
# ---------------------------------------------------------------------------
register(
    "timezone-select",
    title="Timezone Select",
    subcategory="Data",
    description="Single-select listbox for timezones with a mono offset display.",
    tags=["select", "timezone", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["country-select", "language-select", "select"],
    props_doc={
        "export_name": "TimezoneSelect",
        "usage": '<TimezoneSelect label="Timezone" options={[{value:"America/New_York",label:"New York",offset:"GMT-5"}]} />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,offset?,disabled?}[]` | — | Timezones with optional offset. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="Option rows + trigger show the offset in `font-mono` muted foreground. Full keyboard nav + ARIA listbox + outside-click + selected check.",
    a11y_doc="Offset is decorative; the label carries the accessible name.",
    notes_doc="Pass IANA timezone identifiers as `value` for integrations with date libraries.",
    showcase="""function Showcase() {
  const tzs = [{value:"America/New_York",label:"New York",offset:"GMT-5"},{value:"America/Los_Angeles",label:"Los Angeles",offset:"GMT-8"},{value:"Europe/London",label:"London",offset:"GMT+0"},{value:"Europe/Berlin",label:"Berlin",offset:"GMT+1"},{value:"Asia/Tokyo",label:"Tokyo",offset:"GMT+9"},{value:"Asia/Kolkata",label:"Kolkata",offset:"GMT+5:30"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <TimezoneSelect label="Timezone" options={tzs} defaultValue="America/New_York" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 27. language-select
# ---------------------------------------------------------------------------
register(
    "language-select",
    title="Language Select",
    subcategory="Data",
    description="Single-select listbox for languages with an optional native name.",
    tags=["select", "language", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["country-select", "timezone-select", "select"],
    props_doc={
        "export_name": "LanguageSelect",
        "usage": '<LanguageSelect label="Language" options={[{value:"en",label:"English",nativeName:"English"}]} defaultValue="en" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,nativeName?,disabled?}[]` | — | Languages. |\n| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |",
    },
    behavior_doc="Option rows + trigger show the label with the optional native name in muted text beside it. Full keyboard nav + ARIA listbox + outside-click + selected check.",
    a11y_doc="Native name is decorative; the label carries the accessible name.",
    notes_doc="Works for both programming languages (TypeScript/Python) and human languages (English, Chinese).",
    showcase="""function Showcase() {
  const langs = [{value:"en",label:"English",nativeName:"English"},{value:"es",label:"Spanish",nativeName:"Espa\u00f1ol"},{value:"de",label:"German",nativeName:"Deutsch"},{value:"zh",label:"Chinese",nativeName:"\u4e2d\u6587"},{value:"ja",label:"Japanese",nativeName:"\u65e5\u672c\u8a9e"},{value:"typescript",label:"TypeScript"}];
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <LanguageSelect label="Language" options={langs} defaultValue="en" />
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 28. select-group
# ---------------------------------------------------------------------------
register(
    "select-group",
    title="Select Group",
    subcategory="Composite",
    description="Layout wrapper that groups multiple related selects with consistent spacing.",
    tags=["select", "group", "layout", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-label", "native-select"],
    props_doc={
        "export_name": "SelectGroup",
        "usage": '<SelectGroup label="Location"><Select .../><Select .../></SelectGroup>',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` | `string` | `\"Group\"` | Group legend. |\n| `children` | `ReactNode` | — | The selects to lay out. |\n| `direction` | `\"row\" \\| \"column\"` | `\"column\"` | Layout direction. |\n| `className` | `string` | — | Extra classes. |",
    },
    behavior_doc="Renders a semantic `<fieldset><legend>` and arranges child selects in a column (`flex-col gap-4`) or responsive row grid (`grid gap-4`, 1 to 2 to 3 cols). It does NOT reimplement the select — it is a layout wrapper.",
    a11y_doc="`<fieldset><legend>` provides an accessible group label for the contained controls.",
    notes_doc="Use to keep alignment and spacing consistent across related selects (e.g. Country / Region / City).",
    showcase="""function Showcase() {
  const countries = [{value:"us",label:"United States"},{value:"ca",label:"Canada"},{value:"gb",label:"United Kingdom"}];
  const regions = [{value:"ny",label:"New York"},{value:"on",label:"Ontario"},{value:"eng",label:"England"}];
  return (
    <div style={{maxWidth:640}}>
      <SelectGroup label="Location" direction="row">
        <NativeSelect label="Country" options={countries} defaultValue="us" />
        <NativeSelect label="Region" options={regions} defaultValue="ny" />
        <NativeSelect label="City" options={[{value:"nyc",label:"New York City"},{value:"tor",label:"Toronto"}]} defaultValue="nyc" />
      </SelectGroup>
    </div>
  );
}""",
    extra=["native-select"],
)

# ---------------------------------------------------------------------------
# 29. inline-edit-select
# ---------------------------------------------------------------------------
register(
    "inline-edit-select",
    title="Inline Edit Select",
    subcategory="Editing",
    description="A displayed value that switches into an editable select on demand.",
    tags=["select", "inline-edit", "form", "react", "tailwind", "accessible", "interactive"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select-readonly", "select", "select-with-clear"],
    props_doc={
        "export_name": "InlineEditSelect",
        "usage": '<InlineEditSelect label="Environment" options={opts} defaultValue="production" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `label` / `options` / `value` / `defaultValue` / `onChange` / `size` | — | — | As reference. |\n| `editLabel` | `string` | `\"Edit\"` | `aria-label` for the edit trigger. |",
    },
    behavior_doc="Displays the selected value as static text with a hover affordance + edit pencil. Click/Enter starts editing (reveals a combobox). Selecting an option saves + returns to display. Escape reverts (cancels) + returns to display. Outside-click while editing closes and keeps the current selection.",
    a11y_doc="The edit trigger is a labeled button (`aria-label` default \"Edit\"); the editing combobox uses the full ARIA listbox pattern.",
    notes_doc="Use for values that are usually read but occasionally edited (e.g. a setting in a table row).",
    showcase="""function Showcase() {
  const envs = [{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}];
  const [val, setVal] = React.useState("production");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <InlineEditSelect label="Environment" options={envs} value={val} onChange={(v)=>setVal(v)} />
      <p className="text-xs text-[var(--ds-color-muted-foreground)]">Click the value or press Enter to edit. Escape cancels.</p>
    </div>
  );
}""",
)

# ---------------------------------------------------------------------------
# 30. segmented-select
# ---------------------------------------------------------------------------
register(
    "segmented-select",
    title="Segmented Select",
    subcategory="Segmented",
    description="Horizontal segmented selector with radiogroup semantics.",
    tags=["select", "segmented", "radiogroup", "form", "react", "tailwind", "accessible"],
    features=FEAT,
    accessibility=A11Y,
    interactive=True,
    related=["select", "select-with-label", "select-group"],
    props_doc={
        "export_name": "SegmentedSelect",
        "usage": '<SegmentedSelect label="View" options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}]} defaultValue="list" />',
        "table": "| Name | Type | Default | Description |\n|---|---|---:|---|\n| `options` | `{value,label,disabled?}[]` | — | Segments. |\n| `value` / `defaultValue` / `onChange` / `size` / `label` | — | — | Standard. |",
    },
    behavior_doc="A row of segments where exactly one is active. NOT a dropdown — a horizontal segmented control. Keyboard: ArrowLeft/Right/Up/Down moves between segments (roving tabindex), Home/End jump, Tab enters/exits the group. Active segment = `surface-active` + `font-medium` + border emphasis.",
    a11y_doc="`role=\"radiogroup\"` wrapper; each segment `role=\"radio\" aria-checked` with roving tabindex.",
    notes_doc="Use for a small, mutually-exclusive option set where all choices should be visible at once.",
    showcase="""function Showcase() {
  const views = [{value:"list",label:"List"},{value:"grid",label:"Grid"},{value:"board",label:"Board"}];
  const ranges = [{value:"7d",label:"7d"},{value:"30d",label:"30d"},{value:"90d",label:"90d"}];
  const [view, setView] = React.useState("list");
  return (
    <div className="ds-stack" style={{maxWidth:420}}>
      <SegmentedSelect label="View" options={views} value={view} onChange={(v)=>setView(v)} />
      <SegmentedSelect label="Range" options={ranges} defaultValue="30d" />
    </div>
  );
}""",
)
