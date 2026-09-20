# CLI — `add`

`npx devsnips add <path>` installs one DevSnips resource into the current project. Implementation: `cli/src/commands/add.js`.

## Syntax

```bash
npx devsnips add <path>
```

| Argument | Required | Meaning |
|---|---|---|
| `<path>` | Yes | The variant's registry path: `<Technology>/<Category>/<Family>/<variant>/[style]` |

The path is matched case-insensitively against the registry and is trailing-slash insensitive. Take the exact path from `snippets-index.json` (or the `id` field of a specialized index entry) — never from memory.

```bash
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add Vanilla/Components/Buttons/split-button
npx devsnips add Tailwind/Templates/meridian
```

## Execution order

1. **Normalize and validate** (`cli/src/utils/paths.js`). Rejects absolute paths, `..` traversal, unsafe characters, and any path whose first segment is not `tailwind` / `react` / `vanilla` (case-insensitive). Failures are fatal (exit 1).
2. **Fetch the registry** (`cli/src/registry/resolver.js`). Downloads `snippets-index.json` from GitHub `main`, memoized per process. The response must be an object with a `families` array; otherwise a network error is reported.
3. **Resolve the resource.** Exact match against every `families[].variants[].path` (case-insensitive, trailing-slash insensitive). On failure, `findSimilarPaths()` offers up to 5 prefix-matched suggestions, shortest first.
4. **Select source files** (`cli/src/install/downloader.js` `getSourceFiles()`), from the variant's `files` manifest:
   - Excluded always: `metadata.json`, `preview.html`.
   - Included when present: `README.md`, `AGENTS.md`.
   - Included by extension: `.html`, `.jsx`, `.tsx`, `.js`, `.ts`, `.css`.
   - Empty result → "No source files found", exit 1.
5. **Download each file** from `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/library/<path>/<file>`. 30-second timeout per file; an HTML content-type response or empty/whitespace content is a failure. Failures are fatal and name the file.
6. **Write** (`cli/src/install/writer.js`). Destination: `./devsnips/<tech-slug>/<lowercased path without its technology segment>/`. Every write is checked to stay inside `./devsnips/` (security boundary); an existing destination file is a fatal error — there is no overwrite flag.
7. **Update project context** (`cli/src/devsnips/context.js`). Creates `devsnips/config.json` and `devsnips/AGENTS.md` when absent, then records the installation — only after files are on disk. A context failure after a successful write exits 1 with a message stating that the files exist but were not recorded.
8. **Report** the destination directory and the written file names. Exit 0.

## Expected output (success)

```text
DevSnips

  Resolving component... ✓
  Downloading code.tsx... ✓
  Downloading code.jsx... ✓
  Downloading README.md... ✓
  Initializing DevSnips project context... ✓
  Created devsnips/AGENTS.md
  Created devsnips/config.json

✓ Component installed successfully

  Location: <cwd>/devsnips/react/components/buttons/solid-button
  Files:
    - code.tsx
    - code.jsx
    - README.md
```

(Exact file list depends on the resource's registry manifest. `metadata.json` and `preview.html` are never downloaded.)

## Filesystem changes

| Change | When |
|---|---|
| `./devsnips/<tech>/<category>/<family>/<variant>/` created, files written | Always, on success |
| `./devsnips/config.json` created | First successful install only |
| `./devsnips/AGENTS.md` created | First successful install only (never overwritten later) |
| Install record appended to `config.json` (`resources[]`) | Every successful install of a not-yet-recorded path |

Nothing outside `./devsnips/` is created or modified.

## Failure behavior

| Condition | Result |
|---|---|
| Missing `<path>` argument | Usage + example printed, exit 1 |
| Absolute path / `..` / unsafe characters | "Invalid component path", exit 1 |
| Wrong technology prefix | "Invalid repository path" (must start with Tailwind / React / Vanilla), exit 1 |
| Path not in registry | "Component not found" + up to 5 suggestions, exit 1 |
| No installable files | "No source files found", exit 1 |
| Registry unreachable (HTTP error, DNS, timeout, invalid JSON) | "Network error" + connection hint, exit 1 |
| Download failure (HTTP error, HTML response, empty content, timeout) | "Download failed" naming file + resource, exit 1 |
| Destination file already exists | "Filesystem error — File already exists. Remove it first…", exit 1 |
| Malformed existing `config.json` | Error naming the JSON problem; file left untouched, exit 1 |
| Context update fails after files written | Files installed but unrecorded; exit 1 with remediation message |

## Edge cases

- **Trailing slash** — accepted; registry paths carry one.
- **Lowercased input** — accepted; matching is case-insensitive.
- **`library/` prefix in input** — normalizePath does not strip it; the path would fail the technology-prefix check (`library/...` is not a valid first segment). Use the tech-first registry path.
- **Re-running for an installed resource** — the write fails ("File already exists"); remove the destination directory first. The `config.json` record is de-duplicated, so a re-recording never creates a second entry.
- **Grouped variants** — use the full path including the group level (e.g. `Tailwind/Components/Buttons/basic-button/primary`), not the group folder.
- **Templates** — installed like any resource; `pages/*` files land inside the destination preserving their relative names.
