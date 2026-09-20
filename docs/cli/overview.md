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

## Command dispatch

Argument parsing is deliberately minimal — `process.argv.slice(2)`, no parser library:

| Input | Behavior |
|---|---|
| (no args) | `showHelp()` then `exit(1)` |
| `--help` / `-h` | `showHelp()` then `exit(0)` |
| `--version` / `-v` | `printVersion()` then `exit(0)` |
| `add <path>` | the `add` command |
| `add` with no path | prints usage + example, `exit(1)` |
| `init` | the `init` command |
| anything else | "Unknown command", lists `add`/`init`, `exit(1)` |

Help text, error formatting, and version printing live in `cli/src/utils/errors.js`; the version is read from `cli/package.json`.

## Where it reads from and writes to

- **Reads:** the remote registry `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json` (fetched once per process, memoized) and file downloads from `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/library/<path>/<file>`.
- **Writes:** only inside `./devsnips/` under the current working directory (enforced by a path-boundary security check). It never reads or writes the DevSnips repository's local `library/` tree.

**The CLI ignores the local `library/` tree entirely.** A resource that is not in the *published* registry cannot be installed, and a change not pushed to `main` is invisible to the CLI.

## The `add` command, step by step

`npx devsnips add <path>` runs this pipeline, in order:

1. **Normalize/validate the path** — rejects absolute paths and `..`; then requires the first segment to be `tailwind`, `react`, or `vanilla` (case-insensitive).
2. **Fetch the registry** — remote fetch, memoized per process.
3. **Resolve the resource** — matches the input against every `families[].variants[].path`, case-insensitively and ignoring trailing slashes. On failure it produces a "Did you mean one of these?" list (prefix matches, shortest first, max 5).
4. **Select source files** — filters the registry `files` manifest to the installable set; aborts with "No source files found" if empty.
5. **Download each file** — over HTTPS with a 30s timeout; HTML content-type responses and empty/whitespace-only bodies count as failures.
6. **Write** — computes the destination and writes each file.
7. **Update project context** — initializes `devsnips/` on first use and records the install, **only after files are on disk**. If this step fails, the CLI exits `1` and reports that files exist but were not recorded in `devsnips/config.json`.
8. **Report** — the destination directory and the written file names.

### Which files get installed

- Always excluded: `metadata.json`, `preview.html`.
- Always included when present: `README.md`, `AGENTS.md`.
- Included by extension: `.html`, `.jsx`, `.tsx`, `.js`, `.ts`, `.css`.
- Nested paths are preserved exactly as listed (e.g. a template's `pages/index.html`).

The candidate list comes from the variant's `files` manifest, so a resource with an incomplete manifest installs incompletely.

### Path handling

Two different paths are in play:

- **Source path (download):** `library/` + registry path + `/` + filename.
- **Destination path (write):** `./devsnips/<tech-slug>/<remaining-path-lowercased>/<filename>`, relative to the current working directory.

The leading technology segment is stripped and re-introduced as the tech slug (`Tailwind CSS`/`Tailwind` → `tailwind`, `Vanilla HTML/CSS/JS`/`Vanilla` → `vanilla`, `React` → `react`), so it appears exactly once and lowercased:

```text
input:  Tailwind/Sections/AI-Product/agent-workflow/vercel
output: ./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/
```

Write safety: the CLI refuses any path that resolves outside `./devsnips`, refuses to overwrite an existing file, and creates parent directories on demand. **There is no `--force` flag** — the existing-file error mentions it only as a future possibility.

## Project context

The first `add` (or an explicit `init`) creates the DevSnips project context:

```text
./devsnips/
├── AGENTS.md      # instructions for agents working with DevSnips in this project (user-owned)
├── config.json    # machine-readable install state (CLI-managed)
└── <installed resources>
```

Both files live under the current working directory's `devsnips/`. No output directory may be supplied — intentional, to keep writes inside the project boundary.

`config.json` (CLI-managed, v1):

```json
{ "version": 1, "project": {}, "resources": [] }
```

- `resources[]` entries are `{ path, technology, installedAt }`; duplicates are prevented by matching on `path`.
- Written atomically (temp file + rename), so a failed write never leaves truncated JSON.
- A malformed existing `config.json` is an **error**, never silently replaced — the file is left byte-for-byte untouched and the command exits `1`.
- `project` is preserved verbatim across rewrites. Do not edit `config.json` by hand.

`AGENTS.md` (user-owned):

- Created only when absent.
- **Never overwritten once it exists.** Do not add code that rewrites it.
- `config.json` may be rewritten by the CLI; `AGENTS.md` may not.

Details: [Configuration](configuration.md).

## The `init` command

- If both `config.json` and `AGENTS.md` exist, prints "already initialized" and exits `0` without touching anything.
- Otherwise creates `devsnips/`, `config.json` (if missing), and `AGENTS.md` (if missing), reporting which were created.
- Fails cleanly (exit `1`) on a malformed `config.json`, leaving it untouched.
- `add` performs the same initialization automatically on first successful install.

## Error taxonomy

All error paths exit non-zero.

| Class | Trigger | Behavior |
|---|---|---|
| Invalid path | path fails normalization | "Invalid component path" + required shape |
| Invalid repo path | first segment not a known tech | "Invalid repository path" + lists Tailwind/React/Vanilla |
| Component not found | no registry variant path match | "Component not found" + up to 5 similar paths + repo URL |
| No source files | installable file filter empty | "No source files found" |
| Download failed | non-200, HTML response, timeout, empty body | "Download failed" with file + component + error |
| Network error | `ENOTFOUND`/`ECONNRESET`/`ETIMEDOUT`, or non-200 registry fetch | "Network error" + connection hint |
| Filesystem error | write outside `devsnips/`, existing file, write failure | "Filesystem error" with path |
| Context update failed | config read/write failure after install | reports files installed but unrecorded; exit `1` |
| Unexpected | any other rejection in `add` | "✗ Unexpected error" + message; exit `1` |

The help text prints the path shape `<Technology>/<Category>/<Family>/<variant>/[style]` as guidance only — Tailwind components may be 2-level or 3-level.

## Tests

`npm test` (from `cli/`) runs the suites in order — downloader, config, agents, context, init — then `node src/index.js --help`. The suites use `node:assert` and `os.tmpdir()` sandboxes: no framework, no network access. Individual suites run directly as `node test/<file>.test.js`. There is **no** end-to-end `add` test — `add` performs network I/O.

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

## Go deeper

This page is the human-facing CLI reference. The implementation-anchored reference (exact module paths for every behavior, the registry resolver contract, and the config/agent file invariants) is maintained for agents in [`agents/resources/cli.md`](https://github.com/sarthakbystander/DevSnips/blob/main/agents/resources/cli.md).

