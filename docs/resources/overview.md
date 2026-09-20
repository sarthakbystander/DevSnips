# Resources — overview

A **resource** is one leaf content folder under `library/` that a consumer can identify, index, and install. This section defines the resource model: types, hierarchy, addressing, and the per-technology file contracts.

## The three types

| Type | Meaning | Registry `type` value |
|---|---|---|
| Component | One focused, reusable UI pattern. | `component` |
| Section | A larger page-level composition (hero, pricing, footer, …). | `section` |
| Template | A complete page or multi-page site. | `template` |

Every type exists in every technology. Types are not interchangeable — see [Agent resource selection](../agents/resource-selection.md) for the boundary rules from the consume side.

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
- 3-level component (Tailwind Buttons groups): `library/Tailwind/Components/Buttons/basic-button/primary/` — the `basic-button/` group folder carries its own `metadata.json` + `README.md` but is not itself a resource, because it contains leaf children.
- 2-level section: `library/Tailwind/Sections/Blog/minimal/`
- 3-level section (multi-concept Tailwind categories): `library/Tailwind/Sections/AI-Product/model-comparison/vercel/`
- Template: `library/Tailwind/Templates/meridian/`

## What counts as a leaf

A folder is a leaf (a resource) when it has `metadata.json`, has no direct child folder that also has `metadata.json`, and shows the technology's file evidence. The index generator and the validators use slightly different predicates on purpose:

- Index generator (`rebuild_index.py`): Tailwind requires **both** `code.html` and `preview.html`; React accepts `code.tsx` **or** `preview.html`; Vanilla accepts any `metadata.json` folder without a child `metadata.json`.
- Validators (`validate.py`, `deep_check.py`): Tailwind and React accept **either** file, so a variant missing one of the pair is reported by the required-file checks instead of being silently reclassified as a grouping folder.

## Addressing

Three equivalent forms describe the same resource:

| Form | Example | Used by |
|---|---|---|
| Registry path (tech-first, trailing slash) | `React/Components/Buttons/solid-button/` | CLI, `snippets-index.json`, specialized indexes, website URLs |
| Filesystem path | `library/React/Components/Buttons/solid-button/` | The repository on disk; direct file access |
| Family + variant | tech `React` → category `Components` → family `Buttons` → variant `solid-button` | Identity inside the registry |

The CLI accepts the registry path (case-insensitive, trailing slash optional). The folder name is the canonical slug; `metadata.json` fields are descriptive.

## Pages in this section

| Page | Content |
|---|---|
| [Components](components.md) | The component type, per technology. |
| [Sections](sections.md) | The section type, per technology. |
| [Templates](templates.md) | The template type, per technology. |
| [Technologies](technologies.md) | What each technology means, its conventions and limits. |
| [Resource structure](resource-structure.md) | The exact file contract per tech + type, with real examples. |

## Related

- [Registry schema](../machine-readable/registry.md) — how resources appear in `snippets-index.json`.
- [Metadata](../machine-readable/metadata.md) — the `metadata.json` field reference.
- [Terminology](../reference/terminology.md) — family, variant, leaf, registry path.
