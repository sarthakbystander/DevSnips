# Metadata — `metadata.json`

Every resource has a `metadata.json`. It is the structured record the index generator consumes and the description of record for the resource. **The schema is per-technology, not universal** — that is deliberate and historical. Do not invent fields; copy the shape of a sibling in the same family.

## Universal rules

- `metadata.json` is required on every leaf. Invalid JSON is a validation failure.
- `type` must be present and one of `component` / `section` / `template`, and must match the folder bucket (e.g. `type: "section"` outside `Sections/` fails validation).
- Booleans are real JSON booleans, not strings.
- `slug` should equal the folder name where present; the folder name is canonical regardless.
- Do not claim accessibility, responsiveness, browser support, or features the implementation does not provide.
- The registry does not copy every key — the generator reads `name`, `description`, `tags`, `features`, and `style`/`styles` (with a previous-index fallback), leaving other keys resource-local.

## Observed key sets per technology + type

These are the verified shapes. Copy the sibling nearest your resource, not this list verbatim.

### Tailwind component

Example: `library/Tailwind/Components/Buttons/basic-button/primary/metadata.json`

`name`, `component`, `variant`, `description`, `category`, `subcategory`, `tech[]`, `tags[]`, `searchTerms[]`, `related[]`, `styles[]`, `accessibility{object}`, `files{preview, code}`, `type`

### Tailwind section

Example: `library/Tailwind/Sections/Blog/minimal/metadata.json`

`id`, `slug` (= `<section>-<style>`), `name`, `technology: "tailwind"`, `category: "Sections"`, `subcategory`, `section`, `style`, `description`, `framework`, `language`, `tags[]`, `features[]`, `responsive`, `darkMode`, `accessibility` (boolean), `browserSupport[]`, `dependencies[]`, `type: "section"`

### Tailwind template

Example: `library/Tailwind/Templates/meridian/metadata.json`

`name`, `slug`, `technology: "tailwind"`, `category: "Templates"`, `type: "template"`, `pages` (integer), `style`, `responsive`, `darkMode`, `framework`, `language`, `tags[]`, `description`, `features[]`, `related[]`, `searchTerms[]`

### React component

Example: `library/React/Components/Buttons/solid-button/metadata.json`

`id`, `name`, `slug`, `component`, `family`, `variant`, `description`, `framework: "React"`, `language: "TSX"`, `languages[]`, `technology: "react"` (lowercase here — see note below), `type`, `category` (the family name), `subcategory`, `styling: "Tailwind CSS"`, `tags[]`, `features[]`, `responsive`, `darkMode`, `accessibility[]`, `interactive`, `dependencies[]`, `source`, `related[]`

### React section

Example: `library/React/Sections/Hero/minimal/metadata.json`

`id`, `name`, `technology: "React"` (capitalized here), `category: "Sections"`, `subcategory` (family), `family`, `direction` (Minimal | Dark Premium | Bento | Neo-Brutalist), `type: "section"`, `tags[]`, `responsive`, `browserSupport`, `dependencies[]`

### React template

Example: `library/React/Templates/spray-art-school/metadata.json`

`name`, `slug`, `technology: "react"`, `category: "Templates"`, `subcategory`, `type: "template"`, `pages`, `style`, `responsive`, `darkMode`, `lightMode`, `framework`, `language`, `languages[]`, `styling`, `tags[]`, `description`, `features[]`, `related[]`, `searchTerms[]`

### Vanilla component

Example: `library/Vanilla/Components/Buttons/split-button/metadata.json`

`id`, `name`, `description`, `technology: "vanilla"`, `category: "components"` (lowercase), `type: "component"`, `subcategory`, `tags[]`, `responsive`, `browserSupport[]`, `dependencies[]`, `source`, `slug` (= folder name), `component`, `family`, `variant`, `framework: "Vanilla HTML/CSS/JS"`, `language: "HTML"`, `darkMode`, `accessibility[]`, `related[]`, `features[]`

### Vanilla section

Example: `library/Vanilla/Sections/Hero/hero-minimal/metadata.json`

`id`, `name`, `slug`, `component`, `family`, `variant`, `description`, `framework`, `language`, `technology: "vanilla"`, `category: "sections"` (lowercase), `type: "section"`, `subcategory`, `tags[]`, `features[]`, `responsive`, `darkMode`, `accessibility[]`, `browserSupport[]`, `dependencies[]`, `source`, `related[]`

### Vanilla template

Example: `library/Vanilla/Templates/agency/metadata.json` — follow the sibling template shape (`type: "template"`, pages/style metadata).

## Known casing inconsistencies (do not silently "fix")

- React component metadata uses `technology: "react"`; React section metadata uses `technology: "React"`. The index builder tolerates this.
- Vanilla metadata uses lowercase `category` (`"components"`, `"sections"`) while Tailwind/React use Capitalized.
- `category` means different things per schema: in React components it holds the family name; elsewhere it holds the content type.

These are observed facts of the collection. Changing them requires checking `scripts/tooling/indexing/rebuild_index.py` first.

## Field semantics worth noting

| Field | Semantics |
|---|---|
| `id` | Kebab-case, often zero-padded (`solid-button-react-001`, `hero-minimal-001`). Keep stable — do not change an existing ID to make it look nicer. Duplicate IDs are reported as a NOTE by the validator, not a failure; new content must not add collisions. |
| `tags` | Lowercase search words. |
| `searchTerms` | Longer user-intent phrases. |
| `features` | Short human-readable phrases describing actual capabilities. |
| `responsive` / `darkMode` / `accessibility` | Capability claims — must be true of the implementation. Shape varies by schema (boolean, array, or object). |
| `dependencies` | What the implementation requires at runtime (e.g. Tailwind via CDN, Google Fonts). |
| `related` | Slugs of sibling variants suggested as alternatives. |
| `direction` (React sections) | One of the four section design directions. |
| `pages` (templates) | Number of pages in the template. |

## Editing metadata

Changing `name`/`description`/`tags`/`features`/`style` flows into the registry on regeneration. Changing `id` does not (IDs are preserved from the previous index). After any metadata change: regenerate the registry and run the validator — see [Validation](../contributing/validation.md).

