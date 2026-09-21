# Getting started with DevSnips

The fastest path from "I need a UI" to "it's in my project." DevSnips has three consumption paths — pick the one that matches how you work. All three resolve against the same registry.

## Pick your path

| Path | Best for | Entry point |
|---|---|---|
| **CLI** | Copying source into your project | `npx devsnips add <path>` |
| **MCP server** | Letting an AI coding agent find/read resources inside your editor | `pip install devsnips-mcp` |
| **Browse / copy** | Exploring visually first | the website, or `library/` on disk |

This tutorial uses the CLI, the most common path.

## 1. Find a resource

Resources are addressed by a tech-first registry path:

```text
<Technology>/<Category>/<Family>/<variant>/[style]
```

- Technology: `React`, `Tailwind`, `Vanilla`
- Category: `Components`, `Sections`, `Templates`
- e.g. `React/Components/Buttons/solid-button`

To see what's available without the CLI, browse the registry or the website. Query options: [Machine-readable overview](../machine-readable/overview.md).

## 2. Install it

From your project root (Node.js 18+ required):

```bash
npx devsnips add React/Components/Buttons/solid-button
```

The CLI resolves the path against the published registry, downloads the source files, and writes them under `./devsnips/`:

```text
./devsnips/react/components/buttons/solid-button/
```

The technology segment is stripped from the input and re-introduced as the lowercase tech slug; the remaining segments are lowercased. See [CLI — path handling](../cli/overview.md#path-handling).

The first install also creates the project context:

```text
./devsnips/
├── AGENTS.md      # agent instructions (user-owned, never overwritten)
├── config.json    # install state (CLI-managed)
└── react/components/buttons/solid-button/…
```

## 3. Use it

Open the installed files and copy the markup into your app. The CLI never installs `metadata.json` or `preview.html`; it installs the source (`code.*`, `pages/*`, `*.css`, `*.js`) plus `README.md`/`AGENTS.md` when present.

```bash
npx devsnips --help      # full usage
npx devsnips init        # create the project context without installing
```

## 4. Verify what is installed

`devsnips/config.json` records every install (`{ path, technology, installedAt }`). Do not edit it by hand. To remove a resource, delete its files and its `config.json` entry.

## Common next steps

- **Customize the resource** → [Install & customize](install-and-customize.md)
- **Compose several into a page** → [Build a landing page](build-a-landing-page.md)
- **Author your own resource** → [Author a resource](author-a-resource.md)
- **Troubleshooting** → [CLI troubleshooting](../cli/troubleshooting.md)

## Go deeper

- [CLI overview](../cli/overview.md) — the full `add` pipeline, error taxonomy, project-context contract.
- [Machine-readable overview](../machine-readable/overview.md) — every queryable surface.
