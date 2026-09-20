# Terminology

Canonical vocabulary for DevSnips. Use these terms exactly; do not substitute synonyms (a resource is never a "snippet", "asset", or "package").

## Core terms

| Term | Definition |
|---|---|
| **Resource** | One leaf content folder under `library/` that can be identified, indexed, and installed. The atomic unit of the collection. |
| **Family** | A group of related resources (e.g. `Buttons`, `Hero`, `Pricing`). A Capitalized directory; may carry its own `metadata.json` + `README.md` when it has grouping content, but is not itself installable when it contains leaf children. |
| **Variant** | One concrete resource inside a family (e.g. `solid-button` inside `Buttons`). The installable leaf. |
| **Leaf** | A folder that qualifies as a resource: has `metadata.json`, no direct child folder with `metadata.json`, and shows the technology's file evidence (predicates differ slightly between the indexer and the validators by design). |
| **Component** | Resource type: one focused, reusable UI pattern. Registry `type: "component"`. |
| **Section** | Resource type: a page-level composition (hero, pricing, footer). Registry `type: "section"`. |
| **Template** | Resource type: a complete page or multi-page site. Registry `type: "template"`. |
| **Technology** | One of the three implementation stacks: `React`, `Tailwind CSS` (disk: `Tailwind`), `Vanilla HTML/CSS/JS` (disk: `Vanilla`). |
| **Registry** | `snippets-index.json` — the generated machine-readable inventory of every resource. |
| **Specialized indexes** | `agents/resources/indexes/{components,sections,templates}-index.json` — per-type derived indexes with `id` + `install` per variant. |
| **Registry path** | A resource's tech-first path, e.g. `React/Components/Buttons/solid-button/`. The canonical identity and the CLI id. |
| **Filesystem path** | `library/` + the registry path. Where the resource lives on disk. |
| **Project context** | The `devsnips/` directory in a user project: `config.json` + `AGENTS.md` + installed resources. |
| **Registry file manifest** | The `files[]` array on a variant record, built from disk; basis of what the CLI installs. |
| **Agent skill** | `agents/skills/devsnips/` — the published operational instructions for agents consuming DevSnips. |

## Field vocabulary

| Term | Meaning |
|---|---|
| `type` | Lowercase resource type: `component` / `section` / `template`. The filter key. |
| `category` | Capitalized content type: `Components` / `Sections` / `Templates`. The bucket/display form. Do not conflate with `type`. |
| `slug` | Kebab-case identifier; should equal the folder name where present. The folder name is canonical regardless. |
| `tags` | Lowercase search words. |
| `searchTerms` | Longer user-intent phrases. |
| `features` | Short human-readable capability phrases. |
| `styles` | Style vocabulary words (`minimal`, `neo-brutalism`, …). |

## Fixed file names

| File | Role |
|---|---|
| `code.html` | Tailwind/Vanilla implementation (snippet or self-contained page). |
| `code.tsx` | React primary implementation. |
| `code.jsx` | React JavaScript parity build (components only). |
| `preview.html` | Runnable demonstration; never installed. |
| `metadata.json` | Per-resource registry record. |
| `README.md` | Variant documentation. |
| `AGENTS.md` | Template-level agent instructions (templates only). |

## Commonly confused pairs

- **Registry vs website.** The registry is the JSON inventory; the website is a generated human/LLM discovery surface over the same data. The website is never canonical.
- **Variant vs family vs type.** `solid-button` is a variant; `Buttons` is a family; `component` is its type.
- **`tech` strings.** Filter with `React`, `Tailwind CSS`, `Vanilla HTML/CSS/JS` — exact registry strings. Disk directories are `React`, `Tailwind`, `Vanilla`.
- **Master vs specialized index.** The master carries paths and manifests; specialized indexes add `id` and `install` per variant. In the master, the variant `path` *is* the id.
- **Resource metadata vs registry entry.** Metadata is authored at the leaf; the registry entry is the indexed projection (only `name`, `description`, `tags`, `features`, `style`/`styles` are copied).

## Deprecated / never-used terms

- **Snippet** — never use for a resource, despite the repository name.
- **Page** — a template may contain pages; "page" is not a resource type.
- **Utilities / Resources / Snippets / Pages / Tools collections** — forbidden directory names under any technology.
