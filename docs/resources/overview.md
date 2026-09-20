# Resources — overview

A **resource** is one leaf content folder under `library/` that a consumer can identify, index, and install. This page defines the full resource model: types, hierarchy, identity, what makes a folder a resource, and the rules for adding and changing them. It is the deep reference for the resource model — the sibling pages ([Components](components.md), [Sections](sections.md), [Templates](templates.md), [Resource structure](resource-structure.md)) go per-type and per-tech.

## The three types

| Type | Meaning | Registry `type` value |
|---|---|---|
| Component | One focused, reusable UI pattern (button, accordion, dialog). | `component` |
| Section | A larger page-level composition (hero, pricing, footer, …). | `section` |
| Template | A complete page or multi-page site. | `template` |

Every type exists in every technology. **Types are not interchangeable** — do not upscale a component request into a template, and do not merge a section into a component. The registry carries both the Capitalized `category` (`Components`/`Sections`/`Templates`) and the lowercase `type`. See [Agent resource selection](../agents/resource-selection.md) for the consume-side boundary rules.

## Hierarchy

```text
Technology        React | Tailwind | Vanilla          (Capitalized on disk)
    ↓
Resource type     Components | Sections | Templates   (Capitalized on disk)
    ↓
Family            Buttons | Hero | Pricing | …        (Capitalized)
    ↓
Variant           solid-button | hero-minimal | …     (kebab-case — the resource)
```

In the registry the same hierarchy appears as fields: family records carry `tech`, `category` (Capitalized), and `type` (lowercase); variant records carry their own `type` and `path`.

Layout shapes that actually exist on disk (all are valid leaves):

- 2-level component: `library/Tailwind/Components/Accordions/basic-accordion/`
- 3-level component (Tailwind Buttons groups): `library/Tailwind/Components/Buttons/basic-button/primary/` — the `basic-button/` group folder carries its own `metadata.json` + `README.md` but is **not itself a resource**, because it contains leaf children.
- 2-level section: `library/Tailwind/Sections/Blog/minimal/`
- 3-level section (multi-concept Tailwind categories): `library/Tailwind/Sections/AI-Product/model-comparison/vercel/`
- Template: `library/Tailwind/Templates/meridian/`

## Identity and addressing

Three equivalent forms describe the same resource:

| Form | Example | Used by |
|---|---|---|
| Registry path (tech-first, trailing slash) | `React/Components/Buttons/solid-button/` | CLI, `snippets-index.json`, specialized indexes, website URLs |
| Filesystem path | `library/React/Components/Buttons/solid-button/` | The repository on disk; direct file access |
| Family + variant | tech `React` → category `Components` → family `Buttons` → variant `solid-button` | Identity inside the registry |

The **folder name is the canonical slug**. `metadata.json` values (`slug`, `name`, `id`) are descriptive; the path is authoritative for identity. The index generator strips the `library/` prefix so index paths are always tech-first and portable; the CLI adds it back when downloading (`library/` + registry path + filename) and requires the first path segment to be `tailwind`, `react`, or `vanilla`.

## What counts as a leaf (a resource)

A folder is a leaf when it has `metadata.json`, has **no direct child folder that also has `metadata.json`**, and shows the technology's file evidence. Grouping folders (e.g. the Tailwind Buttons groups) have `metadata.json` but are excluded because they contain leaf children.

The index generator and the validators use **deliberately different predicates**:

- Index generator (`rebuild_index.py`): Tailwind requires **both** `code.html` and `preview.html`; React accepts `code.tsx` **or** `preview.html`; Vanilla is any `metadata.json` folder without a child `metadata.json`.
- Validators (`validate.py`, `deep_check.py`): Tailwind and React accept **either** file, so a variant missing one of the pair is reported by the required-file checks instead of being silently reclassified as a grouping folder.

## Per-technology file requirements

"Required" = a failure in `validate.py` and/or `deep_check.py`. "Optional" = allowed and sometimes present.

| Tech | Type | Required | Optional / notable |
|---|---|---|---|
| React | Component | `code.tsx`, `preview.html`, `metadata.json`, `README.md` | `code.jsx` parity build (missing → **warning**, not error) |
| React | Section | `code.tsx`, `preview.html`, `metadata.json` | **No** `README.md`, **no** `code.jsx` |
| React | Template | `preview.html`, `metadata.json`, `AGENTS.md` | full Vite/TS project: `index.html`, `package.json`, `src/**`, `README.md` |
| Tailwind | Component | `code.html`, `preview.html`, `metadata.json`, non-empty `README.md` | `code.html` is a snippet (no DOCTYPE/CDN); `preview.html` is a full page |
| Tailwind | Section | `code.html`, `preview.html`, `metadata.json` | `README.md` optional but must be non-empty when present |
| Tailwind | Template | `preview.html`, `metadata.json`, `AGENTS.md` | `README.md`, `pages/**`, `assets/**` |
| Vanilla | Component | `metadata.json` | `code.html` + `README.md` are the universal convention but **not** machine-enforced |
| Vanilla | Section | `metadata.json` | `code.html`, `README.md` (non-empty when present) |
| Vanilla | Template | `metadata.json`, `AGENTS.md`, `preview.html` **or** non-empty `pages/`, plus `README.md` | modular `pages/`, `css/`, `js/`, `assets/` |

The full file contract with real examples lives in [Resource structure](resource-structure.md).

## Metadata

Every leaf has `metadata.json`. **The schema is NOT uniform across technologies** — that is intentional and historical. Do not invent fields; copy the shape of a sibling in the same family.

Hard rules:

- **`type` is mandatory in every technology** and must match the folder bucket (`component` under `Components/`, `section` under `Sections/`, `template` under `Templates/`). `validate.py` cross-checks this and fails on a mismatch.
- The registry does **not** copy every metadata key. `rebuild_index.py` reads only `name`, `description`, `tags`, `features`, and `style`/`styles` for each variant, and falls back to the previous index for anything absent — so removing a curated field from `metadata.json` does not necessarily erase it from the index.

The per-technology field reference lives in [Metadata](../machine-readable/metadata.md).

## The template `AGENTS.md`

Every template root carries a resource-level `AGENTS.md` — guidance for adapting *that* template (its structure, pages, constraints). It is:

- **Required and validated** — `validate.py` and `rebuild_index.py` both enforce that it exists and is non-empty.
- **Distinct** from the repository root `AGENTS.md` and from `agents/`. See [AGENTS.md context files](../contributing/agent-files.md).
- **Installed by the CLI** when it appears in the registry `files` manifest.

## Completeness and installability

A resource is **complete** when:

1. its leaf files satisfy its tech+type requirement above;
2. its `metadata.json` is valid and has a matching `type`;
3. it is present in `snippets-index.json` (regenerate with `rebuild_index.py`);
4. `validate.py` passes.

A resource is **installable** only if its registry `files` manifest contains at least one file whose extension is `.html`, `.jsx`, `.tsx`, `.js`, `.ts`, or `.css` — or a `README.md`/`AGENTS.md`. That is exactly the filter the CLI applies. `metadata.json` and `preview.html` never reach an install destination, so a resource whose only artifact is `preview.html` is **discoverable but not installable**.

## Adding, modifying, removing

- **Adding.** Pick the tech + type, create `library/<Tech>/<Type>/<Family>/<kebab-slug>/` with the required file set, copy `metadata.json` from a sibling, then run `rebuild_index.py` and `validate.py`. Never create `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, or `Tools/` — `validate.py` rejects them.
- **Modifying.** Editing content in place does not change identity — keep the folder name and `slug`. Changes to `name`/`description`/`tags`/`features`/`style` flow into the index on regeneration; changing `id` does not (IDs are preserved).
- **Removing.** Delete the leaf folder and regenerate. The generator cross-validates index↔disk and **refuses to write** on mismatch, so a stale entry is caught immediately. Record the reason in `CHANGELOG.md` when removing a published resource.

Full procedures: [Creating resources](../contributing/creating-resources.md).

## Pages in this section

| Page | Content |
|---|---|
| [Components](components.md) | The component type, per technology. |
| [Sections](sections.md) | The section type, per technology. |
| [Templates](templates.md) | The template type, per technology. |
| [Technologies](technologies.md) | What each technology means, its conventions and limits. |
| [Resource structure](resource-structure.md) | The exact file contract per tech + type, with real examples. |

## Go deeper

This page is the human-facing resource model. The canonical, implementation-anchored specification (with the enforcing code paths for every rule and the full per-technology metadata key sets) is maintained for agents in [`agents/resources/resources.md`](https://github.com/sarthakbystander/DevSnips/blob/main/agents/resources/resources.md).

## Related

- [Registry schema](../machine-readable/registry.md) — how resources appear in `snippets-index.json`.
- [Metadata](../machine-readable/metadata.md) — the `metadata.json` field reference.
- [Terminology](../reference/terminology.md) — family, variant, leaf, registry path.
