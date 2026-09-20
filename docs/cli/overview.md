# CLI — overview

`devsnips` is the published npm package that installs DevSnips resources into a user project. It is non-interactive by design: no prompts, no wizards, deterministic behavior, explicit failures.

```bash
npx devsnips add <path>
npx devsnips init
npx devsnips --help
npx devsnips --version
```

## Facts

| Property | Value |
|---|---|
| Package | `devsnips` (npm) |
| Version | Read from `cli/package.json` (`npx devsnips --version`) |
| Runtime | Node.js >= 18 |
| Entry point | `cli/src/index.js` (`main` and `bin`) |
| Commands | `add <path>`, `init` |
| Flags | `--help` / `-h`, `--version` / `-v` |
| Working directory | Always the current working directory; all writes confined to `./devsnips/` under it |
| Network | Requires outbound HTTPS (registry + file downloads from GitHub Raw) |

## Where it reads from and writes to

- **Reads:** the remote registry `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json` (fetched once per process, memoized) and file downloads from `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/library/<path>/<file>`.
- **Writes:** only inside `./devsnips/` under the current working directory (enforced by a path-boundary security check). It never reads or writes the DevSnips repository's local `library/` tree.

## What it installs

Per resource, from the registry `files` manifest:

- Installed: source files (`code.html`, `code.tsx`, `code.jsx`, `pages/*.html`, `*.css`, `*.js`, `*.ts`) — plus `README.md` and `AGENTS.md` when the resource provides them.
- Never installed: `metadata.json`, `preview.html`.

Destination layout:

```text
./devsnips/<tech>/<category>/<family>/<variant>/       (lowercased, tech segment stripped)
```

Example: `Tailwind/Sections/AI-Product/agent-workflow/vercel` → `./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/`.

## Project context

The first `add` (or an explicit `init`) creates the DevSnips project context:

```text
./devsnips/
├── AGENTS.md      # instructions for agents working with DevSnips in this project (user-owned)
├── config.json    # machine-readable install state (CLI-managed)
└── <installed resources>
```

- `config.json` may be rewritten by the CLI (atomically, never destructively). Do not edit it by hand.
- `AGENTS.md` is created once and **never overwritten** by the CLI. Edit it freely to add project-specific instructions.

Details: [Configuration](configuration.md).

## What the CLI does not have

Verified absent — do not script against these or claim them:

- No `--force`, `--dry-run`, or overwrite behavior.
- No `list`, `search`, `remove`, or `update` commands.
- No JSON output mode; no `--config`, `--dir`, or `--output` options.
- No version pinning, offline mode, or local-registry mode.
- No interactive prompts.

To see what is available, query the registry; to uninstall, remove files and the `config.json` record manually.

## Pages in this section

| Page | Content |
|---|---|
| [add](add.md) | Full behavior of `npx devsnips add <path>`. |
| [init](init.md) | Project context initialization. |
| [Configuration](configuration.md) | `config.json` and project `AGENTS.md` contracts. |
| [Troubleshooting](troubleshooting.md) | Failure classes and fixes. |
| [CLI reference](../reference/cli-reference.md) | Concise syntax reference. |
