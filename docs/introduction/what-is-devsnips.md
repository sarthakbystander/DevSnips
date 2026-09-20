# What is DevSnips

DevSnips is an open-source, agent-first UI resource library. It provides reusable UI resources — Components, Sections, and Templates — in three technologies (React, Tailwind CSS, Vanilla HTML/CSS/JS), packaged with machine-readable metadata so that AI coding agents can discover, evaluate, install, adapt, and verify them without human mediation.

The defining property is not the content. It is the interface contract around the content: every resource has a stable path, a metadata record, a registry entry, and an install command that an agent can act on programmatically.

## The problem it solves

When an AI coding agent is asked to build UI, it has two options: generate the UI from scratch, or reuse a vetted implementation. Generating from scratch is easy but produces unreviewed, inconsistent code and ignores existing solutions. Reusing existing UI is normally hard for agents because most component libraries are documented for humans — their inventories are scattered across prose, their installation assumes interactive tooling, and their metadata is not machine-queryable.

DevSnips exists to make reuse the reliable option. It exposes a structured inventory (the registry), a non-interactive installer (the CLI), and operational instructions (the agent skill), so the reuse path is as mechanical as the generation path.

## What a resource is

A **resource** is one leaf content folder under `library/` that can be identified, indexed, and installed. Three first-class types exist in every technology:

| Type | What it represents | Registry `type` |
|---|---|---|
| Component | One focused, reusable UI pattern (a button, an accordion, a table). | `component` |
| Section | A page-level composition intended to be composed into pages (hero, pricing, footer). | `section` |
| Template | A complete page or multi-page site starting point. | `template` |

Types are not interchangeable. A section is not a large component, and a template is not a bundle of sections. Agents select the smallest sufficient type for the request — see [Resource selection](../agents/resource-selection.md).

Resources are grouped into **families** (e.g. `Buttons`, `Hero`, `Pricing`), and each concrete implementation inside a family is a **variant** (e.g. `solid-button`, `hero-minimal`). The variant folder is the unit that the registry indexes and the CLI installs.

## How an agent interacts with DevSnips

The complete lifecycle:

```text
User request
    ↓
Agent understands the UI requirement
    ↓
Agent discovers the DevSnips registry (snippets-index.json)
    ↓
Agent filters by technology / type / family and matches tags
    ↓
Agent evaluates candidates via metadata (description, tags, features, files)
    ↓
Agent selects the smallest sufficient resource
    ↓
Agent installs it            npx devsnips add <path>
    ↓
Agent verifies the install   (mandatory — see [Installation](../agents/installation.md))
    ↓
Agent inspects the installed implementation
    ↓
Agent adapts it to the host project
    ↓
Agent validates the result   (build, runtime, accessibility, responsiveness)
```

Each stage has a dedicated page in the [Agents](../agents/overview.md) section.

## How humans interact with DevSnips

Humans are a first-class secondary audience:

- **Browsing and discovery** — the [website](https://devsnips.dev) is a generated static site with technology hubs, category pages, per-resource detail pages, search, and LLM-oriented digests (`llms.txt`, `llms-full.txt`). See [Website and discovery](../machine-readable/schemas.md#website-surfaces).
- **Direct consumption** — resources are plain files. `code.html` / `code.tsx` are copy-paste ready; `preview.html` is a runnable demo. A human can read the code and copy it without the CLI.
- **Contributing** — resources are folders with a defined file contract; contributions follow [Contributing](../contributing/overview.md).

## The moving parts

| Part | Role |
|---|---|
| `library/` | The canonical resources. The source of truth for content. |
| `metadata.json` (per resource) | Structured description of one resource. |
| `snippets-index.json` | The generated machine-readable registry of every resource. What the CLI resolves against. |
| `agents/resources/indexes/*.json` | Generated per-type indexes (components / sections / templates) with CLI-ready `install` commands. |
| The CLI (`npx devsnips`) | Non-interactive installer. Fetches the registry, resolves a path, downloads source files into `./devsnips/` in the user's project. |
| Project context (`devsnips/config.json`, `devsnips/AGENTS.md`) | Machine-readable install state plus agent instructions inside a user project. |
| Agent skill (`devsnips`) | Operational instructions governing how an agent should find, install, adapt, and verify resources. |
| Website | Generated discovery interface over the same registry. Not the canonical source. |
| Validators and QA tooling | Enforce structure, metadata validity, registry↔disk consistency, and resource quality bars. |

## What DevSnips is not

- Not an npm component package. Nothing is imported from a registry at runtime; source files are installed and become part of the consuming project.
- Not a design system runtime. Resources embed their own styling approach (Tailwind classes, or `--ds-*` CSS tokens with fallbacks for Vanilla).
- Not a hosted API. There is no HTTP API for the registry; it is a JSON file fetched from GitHub.

## Where to go next

- [Philosophy](philosophy.md) — why the architecture is shaped this way.
- [Architecture](architecture.md) — how the subsystems relate and the data flows between them.
- [Agent overview](../agents/overview.md) — the consume-side contract in depth.
