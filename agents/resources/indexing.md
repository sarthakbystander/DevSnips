# DevSnips — Indexing

How `snippets-index.json` is produced, what it contains, and what depends on it. Documented
from the current implementation in `scripts/tooling/indexing/`.

**Do not hand-edit `snippets-index.json`.** It is generated; `docs/CONTRIBUTING.md` says the
same ("Do not edit ... by hand unless a maintainer specifically asks you to").

## Purpose and source of truth

`snippets-index.json` is the **single machine-readable registry** of every resource. It is what
the CLI resolves paths against, what the website/search layer reads, and what
`scripts/tooling/validators/validate.py` cross-checks the filesystem against.

The source of truth is the **filesystem under `library/`** plus each leaf's `metadata.json`.
The index is derived data. Paths inside the index are **tech-first** (no `library/` prefix) —
computed by `rel_path()` in `scripts/tooling/indexing/rebuild_index.py`, which strips the prefix
so the output is portable across platforms (the module documents a Windows bug where a naive
`str(p).replace()` would have written absolute machine-specific paths).

## The generator

Implementation: `scripts/tooling/indexing/rebuild_index.py`

```bash
python scripts/tooling/indexing/rebuild_index.py
```

Steps (module docstring + `main()`):

1. **Load the previous index** to preserve hand-curated family-level `description` / `tags` /
   `searchTerms` and variant-level fields.
2. **Re-scan the disk** for leaves under each content-type tree and rebuild each
   family/variant `path`, `category`, and `type` from the on-disk location.
3. **Cross-validate** — every indexed variant must exist on disk and every valid on-disk leaf
   must be indexed.
4. **Recompute stats** and `technologies[].families` from the final family set.
5. **Write the index only if validation found no problems**; otherwise print the problems and
   leave the file untouched.

Key internals:

- `TAILWIND_TREES` / `VANILLA_TREES` / `REACT_TREES` — the three `(bucket, type, is_template)`
  trees per technology: `("Components","component",False)`, `("Sections","section",False)`,
  `("Templates","template",True)`. To add a content type, change these, not the output file.
- `is_leaf()` — Tailwind requires `code.html` **and** `preview.html`; React accepts `code.tsx`
  **or** `preview.html`; Vanilla is any `metadata.json` folder without a child `metadata.json`.
- `list_leaves_under()` — recursive leaf discovery.
- `_template_leaves()` — a template family folder may itself carry `metadata.json` (single
  template) or contain sub-template leaf folders.
- `make_variant()` — builds each variant record, including the `files` manifest.
- `add_family()` — builds each family record.
- `validate()` — the pre-write problem list.

## The `files` manifest

`make_variant()` builds `variant.files` from what is actually on disk:

- direct files: `sorted(p.name ...)` — e.g. `code.html`, `metadata.json`, `preview.html`,
  `README.md`, `AGENTS.md`;
- plus `pages/*` (one level deep, prefixed `pages/`) — Tailwind and Vanilla templates;
- plus `src/*`, `components/*`, `data/*`, `sections/*`, `styles/*` (one level deep, prefixed) —
  React templates.

This manifest is what the CLI installs (`cli/src/install/downloader.js` `getSourceFiles()`), so
an incomplete manifest means an incomplete install. Files nested deeper than one level below
those directories are **not** listed — verified against
`library/Tailwind/Templates/ai-saas-platform/`, whose variant entry lists `pages/<file>.html`
entries.

## Registry shape

Top level: `version`, `lastUpdated`, `description`, `stats`, `families`, `technologies`,
`contributionGuidelines`.

`stats` includes `totalFamilies`, `totalVariants`, `totalStyles`, `technologies[]`, plus
per-technology type breakdowns (`tailwindByType`, `vanillaByType`, `reactByType`).

Family record: `name`, `path` (tech-first, trailing slash), `tech`, `type`, `category`
(Capitalized), optional `subcategory`, `description`, `variantsCount`, `tags[]`,
`searchTerms[]`, `variants[]`.

Variant record: `name`, `path`, `type`, `description`, optional `tags[]`, `features[]`,
`styles[]`, `files[]`.

Consume-side reading guidance lives at
`agents/skills/devsnips/references/registry_schema.md` — do not duplicate it here.

## Relationship to metadata and the filesystem

- `metadata.json` is the **per-leaf** record; the index is the **aggregate** record. The index
  copies a subset of metadata keys (see `agents/resources/resources.md` §5) and otherwise reuses
  curated values from the previous index.
- The index never contains keys that no leaf or curated map provides.
- `validate.py` requires two-way agreement: every index variant path must have a
  `metadata.json` on disk (`library/` + path), and every on-disk leaf must be indexed.

## Validation of the index

Implementation: `scripts/tooling/indexing/rebuild_index.py` `validate()` (pre-write) and
`scripts/tooling/validators/validate.py` `check_index_vs_disk()` (post-hoc gate).

`rebuild_index.py` reports: indexed variants missing on disk, on-disk leaves not indexed,
on-disk templates not indexed, duplicate family paths, stale `/Utilities/` or `/Resources/`
references, `/Sections/` appearing outside a valid `Tailwind/Sections/` / `Vanilla/Sections/` /
`React/Sections/` prefix, families/variants with a missing or invalid `type`, and templates
missing a non-empty `AGENTS.md`.

`validate.py` adds: index variant missing on disk, duplicate index variant path, stale paths,
on-disk content leaf not indexed, and on-disk template not indexed.

For the specialized indexes, `scripts/tooling/indexing/validate_indexes.py` is the dedicated
gate (see "Specialized type indexes" below) — run it after every regeneration.

## Consumers

- **CLI** — `cli/src/registry/resolver.js` fetches
  `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json`,
  requires a `families` array, and resolves `npx devsnips add <path>` against `variants[].path`.
  See `agents/resources/cli.md`.
- **Validation** — `scripts/tooling/validators/validate.py`.
- **Website** — `website/llms.txt`, `website/llms-full.txt`, `website/search-index.json` are
  published alongside the site (generators under `scripts/tooling/generators/`, principally
  `gen_site.py`).
- **Agents** — `agents/skills/devsnips/SKILL.md` and
  `agents/skills/devsnips/references/registry_schema.md` require reading the live registry
  rather than trusting documentation.
- **AI agents (per-type queries)** — `agents/resources/indexes/*.json` (see
  "How agents should use the indexes" below).

## Generated vs manually maintained

| Artifact | Status |
|---|---|
| `snippets-index.json` | **Generated** — `scripts/tooling/indexing/rebuild_index.py` |
| `agents/resources/indexes/*.json` | **Generated** — `scripts/tooling/indexing/build_resource_indexes.py` |
| `library/**/metadata.json` | **Canonical** (hand-authored per leaf) |
| `library/Tailwind/Components/STYLE_TOKENS.md`, `library/React/DESIGN_TOKENS.md`, `library/React/Sections/DESIGN_TOKENS.md`, `library/Vanilla/Components/DESIGN_TOKENS.md`, `library/Vanilla/Templates/design-tokens.md` | **Canonical** shared references |
| `library/Vanilla/Sections/sections-index.html`, `sections-showcase.html` | **Canonical** browse galleries |
| `library/Tailwind/index.html`, `library/React/index.html` | **Canonical** browse pages |
| `website/**` (mirrors, `llms.txt`, `search-index.json`) | **Derived** publishing artifact |

## Stale-data risks

1. **A stale index is invisible to the CLI.** The CLI reads the registry from GitHub `main`, so
   nothing local is installable until the regenerated index is pushed.
2. **Regeneration preserves curated fields indefinitely.** Removing a key from `metadata.json`
   does not necessarily remove it from the index.
3. **`scripts/tooling/indexing/update_index.py` is legacy.** It writes `library/`-prefixed paths
   and uses package-relative imports, so its output disagrees with the current format. Use
   `rebuild_index.py` only.
4. **`update_index.py` also recomputes stats itself** — a second reason not to run both.
5. `rebuild_index.py` **refuses to write** when validation fails: a silent "nothing happened"
   run means the disk and the index disagree. Read the printed problems; don't retry blindly.

## Related

- `agents/resources/resources.md` — the leaf/file/metadata rules the index encodes.
- `agents/resources/qa.md` — the validation gate that follows regeneration.
- `agents/resources/workflows.md` — the regeneration procedure per task type.

## Curated data that survives regeneration

`rebuild_index.py` preserves (path-matched, with a `Components/` ← `Sections/` old-path fallback
for families that moved):

- family-level `description`, `tags`, `searchTerms`;
- variant-level `name`, `description`, `tags`, `features`, `styles`.

It also applies curated display names for generated Tailwind/Vanilla section families, which
have no family-level `metadata.json`:

- `SECTION_FAMILY_NAMES` — e.g. `"AI-Product"` → `"AI Product (Tailwind)"`.
- `VANILLA_SECTION_FAMILY_NAMES` — Vanilla section families; the sections-side Navigation
  family is named to disambiguate it from the legacy `Components/Navigation` family.

If a newly added family shows an odd registry name, add an entry to the relevant map in
`scripts/tooling/indexing/rebuild_index.py` rather than editing the JSON.

## Specialized type indexes

Location: `agents/resources/indexes/`

- `agents/resources/indexes/components-index.json` — components only
- `agents/resources/indexes/sections-index.json` — sections only
- `agents/resources/indexes/templates-index.json` — templates only

**Generator:** `scripts/tooling/indexing/build_resource_indexes.py` — the one-command entry
point for the whole index system:

```bash
python scripts/tooling/indexing/build_resource_indexes.py
```

It imports the scanner and validation of `rebuild_index.py` (the filesystem scanner is never
duplicated), rebuilds the master, then derives the three specialized indexes from the **same
in-memory family set**. It refuses to write anything when `rebuild_index.validate()` reports a
problem.

**Schema (each specialized index):** `version`, `type`, `description`, `generatedBy`,
`masterIndex` (`"snippets-index.json"`), `pathConvention`, `stats` (`families`,
`resources`, `installable`, `byTechnology`), `families[]` (sorted by path). Each family entry
carries `name`, `path`, `tech`, `type`, `category`, `variantsCount`, `variants[]` (sorted by
path). Each variant entry contains only fields backed by real data — `id` (canonical
CLI-resolvable id, `npx devsnips add <id>`), `name`, `type`, `path`, plus optional
`description` / `files` / `tags` / `features` / `styles` (omitted entirely when empty) and
`install` (the exact CLI command, derived only when `cli/src/install/downloader.js`
`getSourceFiles()` would find installable files).

**Path convention:** identical to the master — tech-first, WITHOUT the `library/` prefix. The
on-disk location of every entry is `library/<path>`.

**Validator:** `scripts/tooling/indexing/validate_indexes.py`

```bash
python scripts/tooling/indexing/validate_indexes.py
```

It re-scans the disk with `rebuild_index`'s scanner (exact leaf-detection parity, including
`_template_leaves` for template roots that have no root `code.html`) and fails loudly on:
stale entries (indexed path missing on disk), missing resources (disk leaf absent from the
specialized index), duplicate ids/paths, wrong `type` vs parent index, wrong family
`variantsCount`, family/variant path-prefix mismatches, sort-order violations, master↔
specialized count mismatches, and JSON parse errors. Exit 0 = indexes match the repository.

**Determinism:** two runs over the same repository state produce byte-identical specialized
indexes (families/variants sorted by path, fixed key order, no timestamps). The master keeps
its existing `lastUpdated` date, which is the only intentional non-determinism.

## How agents should use the indexes

Load the specialized index for the type you need instead of scanning `library/` or parsing the
full master:

1. **Pick the index by type** — components → `agents/resources/indexes/components-index.json`,
   sections → `sections-index.json`, templates → `templates-index.json`.
2. **Filter on family fields** — `tech` (`"React"`, `"Tailwind CSS"`,
   `"Vanilla HTML/CSS/JS"`), `category`, `type`. Family `path` prefixes tell you where the
   family lives on disk (`library/<path>`).
3. **Drill into `variants[]`** — each entry's `id` is the canonical CLI id and its on-disk
   location is `library/<path>`. `files` is the manifest; `install` gives the exact
   `npx devsnips add <id>` command when the CLI can install it (no `install` field = nothing
   installable — check `cli/src/install/downloader.js` before assuming a failure).
4. **Answer typical queries without leaving the index:**
   - "Find React button components" → components-index, `tech == "React"`, family path
     containing `Components/Buttons`.
   - "Find Tailwind pricing sections" → sections-index, `tech == "Tailwind CSS"`, family path
     containing `Sections/Pricing`.
   - "Install the split button" → components-index entry
     `React/Components/Buttons/split-button` → its `install` field.
   - "Which files does this resource contain?" → the entry's `files` array; deeper structure
     lives at `library/<path>` on disk.
5. **Verify before acting** — indexes are generated snapshots. If an entry disagrees with the
   disk, the disk wins; regenerate and re-run
   `python scripts/tooling/indexing/validate_indexes.py` rather than patching the JSON.