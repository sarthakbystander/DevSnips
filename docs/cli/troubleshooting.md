# CLI — troubleshooting

Error text is designed to name the failing path or file. Read the actual message before changing anything; do not retry with guessed flags (none exist).

## Failure classes

| Message | Cause | Fix |
|---|---|---|
| `Error: Missing component path` | `add` invoked without `<path>` | Supply the registry path. |
| `Invalid component path` | Absolute path, `..`, unsafe characters, empty string | Use a repository-relative registry path (letters, numbers, hyphens, slashes). |
| `Invalid repository path` | First segment is not `tailwind` / `react` / `vanilla` | Start with the technology name. Do not include a `library/` prefix. |
| `Component not found` (+ "Did you mean one of these?") | Path not in the current registry | Re-check the exact path in `snippets-index.json`. The suggestions are prefix matches (max 5, shortest first). |
| `No source files found` | The resolved variant's manifest has no installable files | The resource may carry only metadata/preview files; pick a different variant or fetch manually. |
| `Network error` / `Failed to fetch registry` | Registry unreachable: no network, HTTP non-200, DNS failure, timeout, invalid JSON | Check connectivity and retry. The registry is fetched from GitHub `main`; a corporate proxy or outage will surface here. |
| `Download failed` (+ file, resource, error) | One file failed: HTTP error, HTML response, empty content, 30s timeout | Transient network failures are the usual cause; retry. A consistent 404 means the registry and disk disagree — report it. |
| `Filesystem error — File already exists` | Destination file already present (no overwrite flag exists) | Remove the destination directory (or specific file) and re-run. |
| `Security violation: attempted write outside devsnips directory` | Destination escaped `./devsnips/` | Should not occur through normal use; report it if seen. |
| `config.json contains invalid JSON…` | Existing context file is corrupt | Fix or remove `devsnips/config.json`, then re-run. The CLI never replaces it automatically. |
| `Component files were installed, but the DevSnips project context could not be updated` | Context read/write failed after files were written | Fix `devsnips/config.json` and re-run `add`; the files exist but are unrecorded. |

## Common scenarios

**"It installed somewhere unexpected."** Destination is always `./devsnips/<tech>/<lowercased-path-without-tech-segment>/` under the current working directory. Check where you ran the command from.

**"I installed a resource and it's not recorded."** Either the context update failed (the CLI said so) or the files were fetched manually rather than via `add`. Manual fetches never touch `config.json`.

**"Re-running says the file already exists."** The CLI never overwrites. Remove `./devsnips/<tech>/<category>/<family>/<variant>/` and re-run. There is no `--force`.

**"The resource I want isn't found but I saw it on the website."** The CLI resolves against the registry published on `main`. A resource that exists only in a branch or a local checkout cannot be installed.

**"npx can't run / no network."** Fall back to fetching the files directly from `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/library/<registry path>/<file>`. Note that this path skips the project-context bookkeeping that `add` performs.

**"Unknown command: <x>"** Only `add` and `init` exist. There is no `list`, `search`, `remove`, `update`, or JSON mode. Query the registry directly for inventory.

## Verifying a suspicious install

Regardless of how it failed, an install is confirmed only when:

1. the command exited 0;
2. `./devsnips/<tech>/<category>/<family>/<variant>/` exists;
3. the files expected for that resource type/stack are present;
4. the content matches the requested resource (slug/family/variant);
5. no unexpected files were introduced.

See [Agent installation](../agents/installation.md) for the full contract.

## Where the CLI's behavior is defined

| Concern | Implementation |
|---|---|
| Command dispatch, help, version | `cli/src/index.js` |
| `add` orchestration | `cli/src/commands/add.js` |
| `init` | `cli/src/commands/init.js` |
| Registry fetch + resolution | `cli/src/registry/resolver.js` |
| File selection + download | `cli/src/install/downloader.js` |
| Destination + writes | `cli/src/install/writer.js`, `cli/src/utils/paths.js` |
| Project context | `cli/src/devsnips/config.js`, `agents.js`, `context.js` |
| Error formatting | `cli/src/utils/errors.js` |
| Tests | `cli/test/*.test.js` (`cd cli && npm test`) |
