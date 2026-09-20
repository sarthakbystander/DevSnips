# FAQ

Answers grounded in actual project behavior. Where a question depends on live data, the answer says where to read it.

## Product

### What is DevSnips?

An open-source, agent-first UI resource library. It provides reusable UI resources — Components, Sections, and Templates in React, Tailwind CSS, and Vanilla HTML/CSS/JS — with machine-readable metadata, a JSON registry, and a CLI, so AI coding agents can discover, evaluate, install, adapt, and verify them programmatically. Humans browse the same collection via the website or by reading the source files directly. See [What is DevSnips](introduction/what-is-devsnips.md).

### Who is DevSnips for?

Primarily AI coding agents and developers building agentic workflows. Secondarily, any developer who wants copy-paste-ready, metadata-described UI resources. The interface contract is designed for non-interactive consumption first.

### How do AI agents use it?

Through the lifecycle: query the registry → filter by technology/type/tags → select the smallest sufficient resource → `npx devsnips add <path>` → verify files on disk → inspect → adapt to the project → validate. The operational instructions live in the `devsnips` agent skill; the reasoning is documented in the [Agents section](agents/overview.md).

### Is there an MCP server or an API?

No. There is no HTTP API. There is an MCP server (`devsnips-mcp`, a read-only stdio server under `integrations/mcp/`) — see [DevSnips MCP](mcp/overview.md). The machine-readable surfaces are files: `snippets-index.json`, the specialized indexes, `website/search-index.json`, `llms.txt`, and `llms-full.txt`.

## Resources

### What is a resource?

One leaf content folder under `library/` that can be identified, indexed, and installed — the atomic unit of the collection. See [Resources overview](resources/overview.md).

### What is the difference between Components, Sections, and Templates?

- **Component** — one focused, reusable UI pattern (a button, an accordion). `type: "component"`.
- **Section** — a page-level composition intended to be composed into pages (hero, pricing, footer). `type: "section"`.
- **Template** — a complete page or multi-page site starting point. `type: "template"`.

They are not interchangeable: do not install a template for a one-section request, and do not merge a section into a component.

### What technologies are supported?

Exactly three: React, Tailwind CSS, and Vanilla HTML/CSS/JS. All three carry all three resource types. Registry strings are `React`, `Tailwind CSS`, and `Vanilla HTML/CSS/JS`. See [Technologies](resources/technologies.md).

### How many resources are there?

Read `stats` in the current `snippets-index.json`. Documentation deliberately never quotes counts because they change.

### Where are resources installed?

Into `./devsnips/<tech>/<category>/<family>/<variant>/` under the current working directory, lowercased, with the leading technology segment normalized so it appears once. Example: `Tailwind/Sections/AI-Product/agent-workflow/vercel` → `./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/`. The CLI never writes outside `./devsnips/`.

### Can I use resources without the CLI?

Yes. Resources are plain files; fetch the implementation file directly from `library/<registry path>/` in the repository or via raw GitHub URLs. Note that manual fetching skips the project-context bookkeeping (`devsnips/config.json`) that `add` performs.

## CLI

### How does the CLI work?

`npx devsnips add <path>` fetches the registry from GitHub `main`, resolves the path against it, downloads the resource's source files (plus `README.md`/`AGENTS.md` when present), writes them into `./devsnips/`, and records the install. `npx devsnips init` creates the project context without installing. See [CLI overview](cli/overview.md).

### Which files get installed?

Source files (`code.html`, `code.tsx`, `code.jsx`, `pages/*.html`, CSS/JS/TS) plus `README.md` and `AGENTS.md` when the resource provides them. `metadata.json` and `preview.html` are never installed.

### Why won't it overwrite existing files?

By design. There is no `--force` flag. Remove the destination files and re-run.

### The command failed — what now?

Read the error message; it names the failing path or file. The failure classes and fixes are tabulated in [Troubleshooting](cli/troubleshooting.md). Common causes: wrong path (resolve it in the registry first), no network, destination already exists, malformed `devsnips/config.json`.

### Does the CLI support listing or searching?

No. There is no `list`, `search`, `remove`, or `update` command. Query the registry JSON directly for inventory.

## Metadata and registry

### How does metadata work?

Every resource has a `metadata.json` describing it — type, name, description, tags, features, capabilities. Schemas are per-technology; contributors copy a sibling's shape. The registry generator reads a defined subset of fields into `snippets-index.json`. See [Metadata](machine-readable/metadata.md).

### What is the registry schema?

Documented in full in [Registry](machine-readable/registry.md). Top level: `version`, `lastUpdated`, `description`, `stats`, `families`, `technologies`, `contributionGuidelines`. Families carry `variants[]`; a variant's `path` is the CLI id.

### Can I hand-edit `snippets-index.json`?

No. It is generated by `scripts/tooling/indexing/rebuild_index.py`, which preserves curated fields across regenerations — there is no reason to patch it, and hand edits create a second source of truth. The generator also refuses to write when disk and index disagree.

### Where does the registry's data come from?

The filesystem under `library/` plus each resource's `metadata.json`. The registry is derived data; the disk is canonical.

## Contributing

### How can I contribute?

Classify your resource (component/section/template + technology), create the folder with the exact file contract, write metadata from a sibling schema, regenerate the registry, run the validators, and open a PR reporting the commands you ran. Full procedure: [Creating resources](contributing/creating-resources.md).

### Do I need to add a README or AGENTS.md to my resource?

Per the file contract: components need `README.md` (required for Tailwind and React; the Vanilla convention is to include it); sections carry it optionally (non-empty when present); **every template requires an `AGENTS.md`**. Components and sections never carry `AGENTS.md`.

### Do I need to regenerate anything after changing content?

Yes. Any add/move/rename/delete or metadata change requires `python scripts/tooling/indexing/rebuild_index.py`, then `python scripts/tooling/validators/validate.py`. See [Validation](contributing/validation.md).

### Is there CI?

No. Validation runs only when a human or agent runs it. The PR template asks you to report the validation commands and their results.

## Troubleshooting

### The registry entry disagrees with the files on disk.

The disk wins. Regenerate the registry and run `python scripts/tooling/indexing/validate_indexes.py`. Never patch the JSON by hand.

### I saw a resource on the website but the CLI can't find it.

The CLI resolves against the registry on `main`. A resource that exists only in a branch, a fork, or a local checkout is not installable until it is merged and the registry is regenerated.

### My install succeeded but the resource isn't in `devsnips/config.json`.

Either the context update failed (the CLI would have printed that files were installed but unrecorded) or you fetched the files manually. Fix the config issue and re-run the command once fixed.

### Where do I report something that looks broken?

Open a GitHub issue on `sarthakbystander/DevSnips` with the exact commands run, their full output, and the affected registry path.

