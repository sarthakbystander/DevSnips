# DevSnips — CLI

Everything an agent needs to know about `devsnips`, the published installer. This file covers
the **implementation**; for consume-side usage rules see
`agents/skills/devsnips/references/cli_reference.md` and `agents/skills/devsnips/SKILL.md`.

## Location and packaging

- Package root: `cli/`
- Manifest: `cli/package.json` — name `devsnips`, `main`/`bin` → `./src/index.js`,
  `engines.node >= 18`, published `files` = `src/**/*`, `README.md`, `LICENSE`.
- Docs: `cli/README.md`. License: `cli/LICENSE`. Lockfile: `cli/package-lock.json`.
- Published as the npm package `devsnips`; invoked as `npx devsnips <command>`.

There is **no** `package.json` at the repository root. All CLI commands run from `cli/`.

## Command structure

Implementation: `cli/src/index.js`

Argument parsing is deliberately minimal — `process.argv.slice(2)`, no parser library:

| Input | Behavior |
|---|---|
| (no args) | `showHelp()` then `exit(1)` |
| `--help` / `-h` | `showHelp()` then `exit(0)` |
| `--version` / `-v` | `printVersion()` then `exit(0)` |
| `add <path>` | `runAddCommand(args[1])` from `cli/src/commands/add.js` |
| `add` with no path | prints usage + example, `exit(1)` |
| `init` | `runInitCommand()` from `cli/src/commands/init.js` |
| anything else | "Unknown command", lists `add`/`init`, `exit(1)` |

Help text, error formatting, and version printing live in `cli/src/utils/errors.js`
(`showHelp`, `exitWithError`, `exitWithNetworkError`, `exitWithFilesystemError`,
`printVersion`). The version is read from `cli/package.json`.

## `add`

Implementation: `cli/src/commands/add.js`

Tests: `cli/test/downloader.test.js` (file selection), `cli/test/context.test.js`
(install recording). There is **no** end-to-end `add` test — `add` performs network I/O.

Behavior, in order:

1. **Normalize/validate the path** — `cli/src/utils/paths.js` `normalizePath()` (rejects
   absolute paths and `..`), then `isValidRepoPath()` (first segment must be `tailwind`,
   `react`, or `vanilla`, case-insensitive).
2. **Fetch the registry** — `cli/src/registry/resolver.js` `fetchRegistry()`.
3. **Resolve the component** — `resolveComponent()` matches the input against every
   `families[].variants[].path`, case-insensitively and ignoring trailing slashes. On failure,
   `findSimilarPaths()` produces a "Did you mean one of these?" list (prefix matches, shortest
   first, max 5).
4. **Select source files** — `cli/src/install/downloader.js` `getSourceFiles(resolved.files,
   resolved.technology)`; aborts with "No source files found" if the result is empty.
5. **Download each file** — `downloadFile()` over `https`, 30s timeout, HTML content-type
   rejected; empty/whitespace-only content counts as failure.
6. **Write** — `cli/src/install/writer.js` `calculateDestination()` +
   `getDestinationFilePath()` + `writeFile()`.
7. **Update project context** — `cli/src/devsnips/context.js` `initializeContext()` and, only
   after files are on disk, `updateContextAfterInstall(canonicalPath, technology)`.
   If this step fails, the CLI exits `1` and reports that files exist but were not recorded in
   `devsnips/config.json`.
## Path handling and installation output

Implementation: `cli/src/install/downloader.js` (`buildRepoFilePath`),
`cli/src/install/writer.js` (`calculateDestination`), `cli/src/utils/paths.js`
(`toTechSlug`, `buildDestinationPath`, `isPathWithinBase`).

Two different paths are in play:

- **Source path** (download): `library/` + registry path + `/` + filename. If the registry path
  already starts with `library/`, the prefix is not added twice.
- **Destination path** (write): `./devsnips/<tech-slug>/<remaining-path-lowercased>/<filename>`,
  relative to `process.cwd()`.

`calculateDestination()` **strips** the leading technology segment from the canonical path and
re-introduces it as the tech slug, so the technology appears exactly once and in slug form.
Remaining segments are lowercased.

Tech slug mapping (`cli/src/utils/paths.js` `TECH_SLUG_MAP`): `Tailwind CSS`/`Tailwind` →
`tailwind`, `Vanilla HTML/CSS/JS`/`Vanilla` → `vanilla`, `React` → `react`.

```text
input:  Tailwind/Sections/AI-Product/agent-workflow/vercel
output: ./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/
```

Write safety (`cli/src/install/writer.js` `writeFile`):

- refuses any path that resolves outside `./devsnips` (`isPathWithinBase` security check);
- refuses to overwrite an existing file (`allowOverwrite` defaults to `false`; `add` always
  passes `false`);
- creates parent directories on demand.

There is **no `--force` flag**. The existing-file error text mentions `--force` "once that flag
is available" — do not document it as working, and do not add it without wiring it through
`cli/src/index.js` and `cli/src/commands/add.js`.

## Which files get installed

Implementation: `cli/src/install/downloader.js` `getSourceFiles()`
Test: `cli/test/downloader.test.js`

- Always excluded: `metadata.json`, `preview.html`.
- Always included when present: `README.md`, `AGENTS.md`.
- Included by extension: `.html`, `.jsx`, `.tsx`, `.js`, `.ts`, `.css`.
- Nested paths are preserved exactly as listed, e.g. a template's `pages/index.html`,
  `pages/about.html`. The test asserts these install verbatim while `metadata.json` and
  `preview.html` do not.

The candidate list comes from `variant.files` in the registry, so a resource with an incomplete
`files` manifest installs incompletely. `files` is generated by
`scripts/tooling/indexing/rebuild_index.py` `make_variant()`.

## Project context: `devsnips/config.json` and `devsnips/AGENTS.md`

Implementation: `cli/src/devsnips/config.js`, `cli/src/devsnips/agents.js`,
`cli/src/devsnips/context.js`. Tests: `cli/test/config.test.js`, `cli/test/agents.test.js`,
`cli/test/context.test.js`, `cli/test/init.test.js`.

Both files live under `process.cwd()/devsnips/` (`getDevSnipsDirectory()`). No output directory
may be supplied by the caller — intentional, to keep writes inside the project boundary.

`config.json` (CLI-managed, v1):

```json
{ "version": 1, "project": {}, "resources": [] }
```

- `resources[]` entries are `{ path, technology, installedAt }` added by `recordInstallation()`;
  duplicates are prevented by matching on `path`.
- Written atomically (temp file + rename) with 2-space indentation and a trailing newline, so a
## Errors

Implementation: `cli/src/utils/errors.js`. All error paths exit non-zero.

| Class | Trigger | Behavior |
|---|---|---|
| Invalid path | `normalizePath()` returns null | "Invalid component path" + required shape |
| Invalid repo path | first segment not a known tech | "Invalid repository path" + lists Tailwind/React/Vanilla |
| Component not found | no registry variant path match | "Component not found" + up to 5 similar paths + repo URL |
| No source files | `getSourceFiles()` empty | "No source files found" |
| Download failed | non-200, HTML response, timeout, empty body | "Download failed" with file + component + error |
| Network error | `ENOTFOUND`/`ECONNRESET`/`ETIMEDOUT`, or non-200 registry fetch | "Network error" + connection hint |
| Filesystem error | write outside `devsnips/`, existing file, write failure | "Filesystem error" with path |
| Context update failed | config read/write failure after install | reports files installed but unrecorded; exit `1` |
| Unexpected | any other rejection in `add` | "✗ Unexpected error" + message; exit `1` |

`showHelp()` prints the path shape `<Technology>/<Category>/<Family>/<variant>/[style]`. Treat
that as guidance only — Tailwind components may be 2-level or 3-level
(`agents/resources/frameworks/tailwind.md`).

## Tests and how to run them

Manifest script: `cli/package.json` `scripts.test` runs, in order,
`cli/test/downloader.test.js`, `cli/test/config.test.js`, `cli/test/agents.test.js`,
`cli/test/context.test.js`, `cli/test/init.test.js`, then `node src/index.js --help`.

```bash
cd cli
npm test
```

Individual suites can be run directly as `node test/<file>.test.js`. They use `node:assert` and
`os.tmpdir()` sandboxes — no framework, no network access.

## Not in the CLI

Verified absent; do not document these as features: `--force`, `--dry-run`, `list`/`search`,
`remove`/`update`, a JSON output mode, `--config`/`--dir`/`--output`, version pinning, an
offline or local-registry mode, and any interactive prompt.
  failed write never leaves truncated JSON.
- A malformed existing `config.json` is an **error**, never silently replaced; the file is left
  byte-for-byte untouched and the command exits `1`.
- `project` is preserved verbatim across rewrites.

`AGENTS.md` (user-owned):

- Created only when absent, from `getDefaultAgentsContent()` (`# DevSnips Agent Instructions`,
  general rules, resource-adaptation rules, quality checks).
- **Never overwritten once it exists** — asserted by `cli/test/agents.test.js` and
  `cli/test/context.test.js`. Do not add code that rewrites it; the module header states the
  same contract.
- `config.json` may be rewritten by the CLI; `AGENTS.md` may not.

## `init`

Implementation: `cli/src/commands/init.js`; tests `cli/test/init.test.js`.

- If both `config.json` and `AGENTS.md` exist (`isContextInitialized()`), prints
  "DevSnips project context already initialized." and exits `0` without touching anything.
- Otherwise creates `devsnips/`, `config.json` (if missing), and `AGENTS.md` (if missing),
  reporting which were created.
- Fails cleanly (exit `1`) on a malformed `config.json`, leaving it untouched.
- `add` performs the same initialization automatically on first successful install.
8. **Report** — destination directory and the written file names.

## Resource resolution

Implementation: `cli/src/registry/resolver.js`

Constants:

- `REGISTRY_URL` =
  `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json`
- `GITHUB_RAW_BASE` = `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/`

The registry is fetched **remotely** and memoized per process (`cachedRegistry`). It must be an
object with a `families` array, else a network error is reported. `resolveComponent()` returns
`{ family, variant, canonicalPath, technology, type, category, files }`, where `technology` is
`family.tech` and `files` is `variant.files` (defaulting to `[]`).

**The CLI ignores the local `library/` tree entirely.** A resource that is not in the published
registry cannot be installed, and a change not pushed to `main` is invisible to the CLI.
Registry shape: `agents/resources/indexing.md`.