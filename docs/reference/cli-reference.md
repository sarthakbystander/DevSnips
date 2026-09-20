# CLI reference

Concise, authoritative syntax reference for the `devsnips` CLI. Behavioral detail: [CLI section](../cli/overview.md).

## Synopsis

```text
npx devsnips <command> [options]
```

## Commands

### `add <path>`

Install one resource into the current project.

```bash
npx devsnips add <Technology>/<Category>/<Family>/<variant>/[style]
```

| Argument | Required | Description |
|---|---|---|
| `<path>` | yes | Registry path of the variant. Case-insensitive; trailing slash optional. No `library/` prefix, no absolute paths, no `..`. |

Behavior: fetch registry → resolve path → download source files → write under `./devsnips/<tech>/…` → record in `devsnips/config.json`. Exits 0 on success; non-zero with a named error otherwise. Never overwrites existing files. Full detail: [add](../cli/add.md).

Examples:

```bash
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add Vanilla/Components/Buttons/split-button
npx devsnips add Tailwind/Templates/meridian
```

### `init`

Initialize the DevSnips project context (`./devsnips/config.json`, `./devsnips/AGENTS.md`) without installing anything. Idempotent; local-only (no network). Full detail: [init](../cli/init.md).

```bash
npx devsnips init
```

### Global flags

| Flag | Effect | Exit code |
|---|---|---|
| `--help`, `-h` | Print help | 0 |
| `--version`, `-v` | Print package version | 0 |
| *(no arguments)* | Print help | 1 |
| *(unknown command)* | Error listing available commands | 1 |

## Complete behavior table

| Input | Behavior |
|---|---|
| `npx devsnips add <path>` | Install resource at path |
| `npx devsnips add` | Usage + example, exit 1 |
| `npx devsnips init` | Create project context (idempotent) |
| `npx devsnips --help` / `-h` | Help, exit 0 |
| `npx devsnips --version` / `-v` | Version, exit 0 |
| `npx devsnips` | Help, exit 1 |
| `npx devsnips <anything else>` | "Unknown command" + available commands, exit 1 |

## Path format

```text
<Technology>/<Category>/<Family>/<variant>/[style]
Technology ∈ {Tailwind, React, Vanilla}   (case-insensitive on input)
Category  ∈ {Components, Sections, Templates}
```

Guidance only — some families use an extra level (Tailwind Buttons groups, multi-concept Tailwind sections). Always take the exact path from the registry or a specialized index `id`.

## Destination layout

```text
./devsnips/<tech>/<category>/<family>/<variant>/
<tech> ∈ {tailwind, react, vanilla}   (leading tech segment stripped and normalized; remaining segments lowercased)
```

## What is installed vs skipped

| File | Installed |
|---|---|
| `code.html`, `code.tsx`, `code.jsx`, `pages/*.html`, `*.css`, `*.js`, `*.ts` | Yes |
| `README.md`, `AGENTS.md` | Yes, when the resource provides them |
| `metadata.json` | No |
| `preview.html` | No |

## Not available

Confirmed absent; do not use or script against: `--force`, `--dry-run`, `list`, `search`, `remove`, `update`, JSON output, `--config`/`--dir`/`--output`, version pinning, offline/local-registry mode, interactive prompts.

## Exit codes

`0` = success (including `init` on an already-initialized project). `1` = any failure, with a specific error class printed to stderr.
