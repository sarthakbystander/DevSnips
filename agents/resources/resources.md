# DevSnips — Resource Specification

Canonical specification for what a DevSnips resource is, how it is addressed, what files it
must contain, and where each rule is enforced. Read this before touching anything in `library/`.

Related detail: `agents/resources/frameworks/{react,tailwind,vanilla}.md` (clone structure),
`agents/resources/qa.md` (how to verify), `agents/resources/cli.md` (how it is consumed),
`agents/resources/conventions.md` (naming).

## 1. What a resource is

A DevSnips **resource** is one leaf content folder under `library/` that a consumer can
identify, index, and install. Three first-class content types exist in all three technologies:

| Type | Meaning | Registry `type` |
|---|---|---|
| Component | One focused, reusable UI pattern. | `component` |
| Section | A larger page-level composition (hero, pricing, footer, …). | `section` |
| Template | A complete page or multi-page site. | `template` |

Types are not interchangeable: do not upscale a component request to a template, and do not
merge a section into a component. The registry carries both a Capitalized `category`
(`Components`/`Sections`/`Templates`) and the lowercase `type`.

## 2. Resource identity and addressing

Three equivalent address forms describe the same resource:

1. **Registry path** (used by the CLI and `snippets-index.json`) — tech-first, trailing slash:
   `React/Components/Buttons/solid-button/`
2. **Filesystem path** — the registry path prefixed with `library/`:
   `library/React/Components/Buttons/solid-button/`
3. **Family + variant** — the identity inside `snippets-index.json`: tech `React` →
   category `Components` → family `Buttons` → variant `solid-button`.

Enforcing/demonstrating code:

- `scripts/tooling/indexing/rebuild_index.py` — `rel_path()` strips the `library/` prefix, so
  index paths are always tech-first.
- `cli/src/install/downloader.js` — `buildRepoFilePath()` adds the prefix back when
  downloading (`library/` + registry path + `/` + filename).
- `cli/src/utils/paths.js` — `isValidRepoPath()` requires the first segment to be
  `tailwind`, `react`, or `vanilla` (case-insensitive).

The **folder name is the canonical slug**. `metadata.json` values (`slug`, `name`, `id`) are
descriptive; the path is authoritative for identity.

## 3. What counts as a leaf (variant)

A folder is a **leaf** when it has `metadata.json`, has **no direct child folder that also has
`metadata.json`**, and shows the tech's file evidence. Grouping folders (e.g. the Tailwind
Buttons groups) have `metadata.json` but are excluded because they contain leaf children.

Implementation — note the two predicates differ slightly:

## 4. Per-framework file requirements

"Required" = a failure in `scripts/tooling/validators/deep_check.py` and/or
`scripts/tooling/validators/validate.py`. "Optional" = allowed and sometimes present.

### 4.1 React

Repository location: `library/React/{Components,Sections,Templates}/`

Validation: `scripts/tooling/validators/validate.py`,
`scripts/tooling/validators/deep_check.py`

| Type | Required | Optional / notable |
|---|---|---|
| Component | `code.tsx`, `preview.html`, `metadata.json`, `README.md` | `code.jsx` parity build (missing → **warning**, not error, in `deep_check.py`) |
| Section | `code.tsx`, `preview.html`, `metadata.json` | **No `README.md`, no `code.jsx`** |
| Template | `preview.html`, `metadata.json`, `AGENTS.md` | full Vite/TS project: `index.html`, `package.json`, configs, `src/**`, `README.md` |

Observed examples:

- Component: `library/React/Components/Buttons/solid-button/`
- Section: `library/React/Sections/Hero/minimal/`
- Template: `library/React/Templates/spray-art-school/`

### 4.2 Tailwind

Repository location: `library/Tailwind/{Components,Sections,Templates}/`

Validation: `scripts/tooling/validators/validate.py`,
`scripts/tooling/validators/deep_check.py`

| Type | Required | Optional / notable |
|---|---|---|
| Component | `code.html`, `preview.html`, `metadata.json`, `README.md` | 3-level layout allowed (see below) |
| Section | `code.html`, `preview.html`, `metadata.json` | `README.md` optional but must be non-empty when present |
| Template | `preview.html`, `metadata.json`, `AGENTS.md` | `README.md`, `pages/**`, `assets/**` |

## 5. Metadata

Every leaf has `metadata.json`. **The schema is NOT uniform across technologies** — that is
intentional and historical. Do not invent fields; copy the shape of a sibling in the same
family. Verified key sets:

- **Tailwind component** — `library/Tailwind/Components/Buttons/basic-button/primary/metadata.json`:
  `name, component, variant, description, category, subcategory, tech[], tags[], searchTerms[],
  related[], styles[], accessibility{object}, files{preview,code}, type`.
- **Tailwind section** — `library/Tailwind/Sections/Blog/minimal/metadata.json`:
  `id, slug, name, technology:"tailwind", category:"Sections", subcategory, section, style,
  description, framework, language, tags[], features[], responsive, darkMode,
  accessibility(bool), browserSupport[], dependencies[], type:"section"`.
- **Tailwind template** — `library/Tailwind/Templates/meridian/metadata.json`:
  `name, slug, technology:"tailwind", category:"Templates", type:"template", pages(int), style,
  responsive, darkMode, framework, language, tags[], description, features[], related[],
  searchTerms[]`.
- **React component** — `library/React/Components/Buttons/solid-button/metadata.json`:
  `id, name, slug, component, family, variant, description, framework:"React", language:"TSX",
  languages[], technology:"react", type, category (the family name, e.g. "Buttons"), subcategory,
  styling:"Tailwind CSS", tags[], features[], responsive, darkMode, accessibility[],
  interactive, dependencies[], source, related[]`.
- **React section** — `library/React/Sections/Hero/minimal/metadata.json`:
  `id, name, technology:"React", category:"Sections", subcategory (family), family, direction,
  type:"section", tags[], responsive, browserSupport, dependencies[]`.
- **React template** — `library/React/Templates/spray-art-school/metadata.json`:
  `name, slug, technology:"react", category:"Templates", subcategory, type:"template", pages,
  style, responsive, darkMode, lightMode, framework, language, languages[], styling, tags[],
  description, features[], related[], searchTerms[]`.
- **Vanilla component** — `library/Vanilla/Components/Buttons/split-button/metadata.json`:
  `id, name, description, technology:"vanilla", category:"components", type:"component",
  subcategory, tags[], responsive, browserSupport[], dependencies[], source, slug, component,
  family, variant, framework:"Vanilla HTML/CSS/JS", language:"HTML", darkMode, accessibility[],
  related[], features[]`.
- **Vanilla section** — `library/Vanilla/Sections/Hero/hero-minimal/metadata.json`:
  `id, name, slug, component, family, variant, description, framework, language,
  technology:"vanilla", category:"sections", type:"section", subcategory, tags[], features[],
  responsive, darkMode, accessibility[], browserSupport[], dependencies[], source, related[]`.
- **Vanilla template** — `library/Vanilla/Templates/agency/metadata.json`:
  `id, name, slug, component, family, variant:"default", description, framework, language,
  technology, category:"templates", type:"template", subcategory, tags[], features[],
  responsive, darkMode, browserSupport, dependencies, accessibility[], source, related[], files[]`.

Hard rules:

- **`type` is mandatory in every technology** and must match the folder bucket — `component`
  under `Components/`, `section` under `Sections/`, `template` under `Templates/`. Enforced by
  `scripts/tooling/validators/validate.py` (`type=component outside Components/`, …).
- `type` must be one of `component` / `section` / `template`; anything else fails validation.
- Boolean fields should be real JSON booleans. Some historical records use strings (e.g.
  `darkMode: "dark-first (fixed dark theme; no light-mode toggle)"`) — do not imitate those in
  new content.
- Do not claim accessibility, responsiveness, or features the implementation does not provide
  (`docs/COMPONENT_STRUCTURE.md`, "Required consistency rules").
- `id`/`slug` should be globally unique for new content. `validate.py` reports duplicates as an
  informational NOTE only; known pre-existing duplicates are deliberately preserved.
## 6. `code.*`, `preview.html`, `README.md`, `AGENTS.md`

### `code.*` — the copy-paste implementation

- Tailwind: `code.html` is a **snippet only** — no `<!DOCTYPE>`, no `<html>/<head>/<body>`, no
  Tailwind CDN. The optional header comment is documented in
  `library/Tailwind/Components/STYLE_TOKENS.md` and `docs/CONTRIBUTING.md`.
- Vanilla: `code.html` is the single self-contained source (inline `<style>` + `<script>`),
  safe to open standalone (`docs/COMPONENT_STRUCTURE.md`: "Vanilla components use a single
  self-contained source file").
- React: `code.tsx` is the primary implementation; `code.jsx` is the JavaScript parity build.
  Section variants ship `code.tsx` only, on purpose.
- Templates: no single `code.*` file. The implementation lives in `pages/**` (Tailwind/Vanilla)
  or `src/**` (React).

### `preview.html` — the runnable demo

- Present on every Tailwind component/section, every React component/section, and every
  template.
- **Never installed by the CLI** — `cli/src/install/downloader.js` `getSourceFiles()` excludes
  `preview.html` and `metadata.json` unconditionally, asserted by
  `cli/test/downloader.test.js`.
- Tailwind previews are full `<!DOCTYPE html>` pages using the Tailwind CDN plus demo framing.
- React previews are self-contained pages loading React UMD + Tailwind CDN and mounting a
  showcase; see `agents/resources/frameworks/react.md`.

### `README.md` — variant documentation

- Required for Tailwind **component** variants and React **component** variants, and must be
  non-empty (`deep_check.py`, `validate.py`).
- Optional for Tailwind and React **section** variants, but **must be non-empty when present**
  (`deep_check.py`).
- Convention (not machine-enforced) for Vanilla variants: what the variant is, when to use it,
  customization, accessibility notes, responsive behavior, dependencies
  (`docs/CONTRIBUTING.md`).
- Required for Vanilla **templates** (`deep_check.py`).
- Installed by the CLI when listed in the registry's `files` array.

### `AGENTS.md` — template-level agent instructions

- **Required at the root of every template** in all three technologies, and must be
  non-empty. Enforced twice: `scripts/tooling/validators/validate.py`
  (`check_template_agents`) and `scripts/tooling/indexing/rebuild_index.py` (`validate()`).
- Distinct from the repository root `AGENTS.md` and from `agents/`. It is resource-level
  guidance for adapting *that* template.
- Examples: `library/Tailwind/Templates/meridian/AGENTS.md`,
  `library/React/Templates/spray-art-school/AGENTS.md`,
  `library/Vanilla/Templates/agency/AGENTS.md`.
- Installed by the CLI when listed in the registry `files` (`cli/src/install/downloader.js`).

## 7. Dependencies and accessibility

- **Dependencies are data, not installs.** They are recorded in `metadata.json`
  (`dependencies[]` for sections; a descriptive `"React 18, React Router 6, …"` string in
  React template metadata) and are never vendored. The library's default is zero build step.
## 8. Completeness and installation compatibility

A resource is *complete* when:

1. its leaf files satisfy §4 for its tech+type;
2. its `metadata.json` satisfies §5;
3. it is present in `snippets-index.json` (regenerate with
   `scripts/tooling/indexing/rebuild_index.py`);
4. `scripts/tooling/validators/validate.py` passes.

A resource is *installable* only if its registry entry carries at least one file whose
extension is `.html`, `.jsx`, `.tsx`, `.js`, `.ts`, `.css` — or `README.md`/`AGENTS.md`.
`cli/src/install/downloader.js` `getSourceFiles()` filters on exactly that list, and
`cli/src/commands/add.js` aborts with "No source files found" when the result is empty. That
is why `metadata.json` and `preview.html` never reach an install destination, and why a
resource whose only artifact is `preview.html` is discoverable but not installable.

Destination layout is computed by `cli/src/install/writer.js` `calculateDestination()`:
`./devsnips/<tech-slug>/<rest-of-path-lowercased>/`.

## 9. Rules for adding, modifying, and removing resources

### Adding

1. Choose the technology and content type that match the intent (§1). Do not create
   `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, or `Tools/` — `validate.py`
   `check_architecture()` fails on them.
2. Create `library/<Tech>/<Type>/<Family>/<kebab-slug>/` with the §4 file set.
3. Copy the `metadata.json` shape from a sibling in the same family (§5), including `type`.
4. Run `python scripts/tooling/indexing/rebuild_index.py` then
   `python scripts/tooling/validators/validate.py` (see `agents/resources/workflows.md`).
5. If it is a new family, check that the registry produced sensible family naming — curated
   names for generated Tailwind/Vanilla section families live in `SECTION_FAMILY_NAMES` /
   `VANILLA_SECTION_FAMILY_NAMES` inside `scripts/tooling/indexing/rebuild_index.py`.

### Modifying

- Changing content **in place** does not change identity. Keep the folder name and `slug`.
- Changing `metadata.json` `name`/`description`/`tags`/`features`/`style` flows into the index
  on regeneration; changing `id` does not (IDs are preserved).
- Cross-tree moves (e.g. `Components/` → `Sections/`) require updating `type` and the registry
  path, then regenerating. `rebuild_index.py` contains an old-path fallback that carries
  curated variant data forward across such moves.

### Removing

- Delete the leaf folder, then regenerate. `rebuild_index.py` cross-validates index ↔ disk and
  **refuses to write** on mismatch, so a stale index entry is caught immediately.
- Do not leave an orphaned `metadata.json`; `validate.py` reports on-disk leaves that are not
  indexed and index variants that are not on disk.
- Prefer a documented reason in `CHANGELOG.md` for removing published resources.

## 10. Where to go next

- Framework-specific structure and quirks: `agents/resources/frameworks/react.md`,
  `frameworks/tailwind.md`, `frameworks/vanilla.md`.
- How the CLI consumes a resource: `agents/resources/cli.md`.
- How the registry is produced: `agents/resources/indexing.md`.
- How a resource is verified: `agents/resources/qa.md`.
- Naming/format conventions: `agents/resources/conventions.md`.
- Consume-side agent workflow: `agents/skills/devsnips/SKILL.md`.
- Conventional dependencies, from real metadata: Tailwind CSS via CDN, Google Fonts, Pico CSS
  (CDN, e.g. `library/Vanilla/Templates/agency/`), React + React Router + Framer Motion
  (`library/React/Templates/spray-art-school/`). Adding anything else is out of convention.
- **Accessibility is part of the quality bar, not a field.** Native semantics first; ARIA only
  to supplement. See `docs/COMPONENT_STRUCTURE.md` ("Accessibility expectations") and
  `agents/skills/devsnips/references/accessibility_responsive_checklist.md`.
- Vanilla accessibility/animation is machine-checked — see
  `scripts/qa/resources/qa_vanilla.py` and `agents/resources/frameworks/vanilla.md`.
- **Responsive** means usable at mobile widths without horizontal overflow, not
  pixel-identical across breakpoints.

The registry does **not** copy every metadata key. `rebuild_index.py` `make_variant()` reads
`name`, `description`, `tags`, `features`, and `style`/`styles`, and falls back to the previous
index for anything absent — so removing a curated field from `metadata.json` does not
necessarily erase it from the index.
Layout shapes actually present:

- 2-level component: `library/Tailwind/Components/Accordions/basic-accordion/`
- 3-level component (Buttons only): `library/Tailwind/Components/Buttons/basic-button/primary/`
  where `basic-button/` holds `metadata.json` + `README.md` plus its variants.
- 2-level section: `library/Tailwind/Sections/Blog/minimal/`
- 3-level section: `library/Tailwind/Sections/AI-Product/model-comparison/vercel/`
- Template: `library/Tailwind/Templates/meridian/`

### 4.3 Vanilla

Repository location: `library/Vanilla/{Components,Sections,Templates}/`

Validation: `scripts/tooling/validators/validate.py`,
`scripts/tooling/validators/deep_check.py`, `scripts/qa/resources/qa_vanilla.py`

| Type | Required | Optional / notable |
|---|---|---|
| Component | `metadata.json` | `code.html`, `README.md` are the universal convention but **not** machine-enforced for Vanilla |
| Section | `metadata.json` | `code.html`, `README.md` (non-empty when present) |
| Template | `metadata.json`, `AGENTS.md`, `preview.html` **or** a non-empty `pages/`, plus `README.md` | modular `pages/{code.html,style.css,script.js}`, `css/`, `js/`, `assets/` |

Observed examples:

- Component: `library/Vanilla/Components/Buttons/split-button/`
- Section: `library/Vanilla/Sections/Hero/hero-minimal/`
- Template (modular): `library/Vanilla/Templates/agency/`
- Template (multi-page with shared `css/`/`js/`/`assets/`): `library/Vanilla/Templates/saas-dashboard/`
- `scripts/tooling/indexing/rebuild_index.py` `is_leaf()` — Tailwind requires **both**
  `code.html` **and** `preview.html`; React accepts `code.tsx` **or** `preview.html`;
  Vanilla is always a leaf (metadata + no child metadata).
- `scripts/tooling/validators/validate.py` `is_leaf()` and
  `scripts/tooling/validators/deep_check.py` `is_leaf()` — Tailwind / React accept **either**
  file, deliberately, so a variant missing one of the pair is *reported by the required-file
  checks* instead of being silently reclassified as a grouping folder.