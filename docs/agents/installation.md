# Agent installation

Installation is a single non-interactive command. The behavioral detail lives in [CLI → add](../cli/add.md); this page covers what an agent must do around it.

## The command

```bash
npx devsnips add <path>
```

`<path>` is the variant's registry path, e.g.:

```bash
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add Vanilla/Components/Buttons/split-button
```

Path shape: `<Technology>/<Category>/<Family>/<variant>/[style]`. Treat that as guidance — some families (e.g. Tailwind Buttons groups, multi-concept Tailwind sections) carry an extra level. Always take the exact path from the registry, not from memory.

## What the CLI does

1. Normalizes and validates the path (rejects absolute paths, `..`, unsafe characters; first segment must be `tailwind`, `react`, or `vanilla`, case-insensitively).
2. Fetches the registry from GitHub `main` and resolves the path against every `families[].variants[].path` (case-insensitive, trailing-slash insensitive). On failure it prints up to 5 similar paths.
3. Selects installable files from the variant's `files` manifest: source files (`code.html`, `code.tsx`, `code.jsx`, `pages/*.html`, `*.css`, `*.js`, `*.ts`) plus `README.md` and `AGENTS.md` when present. `metadata.json` and `preview.html` are never installed.
4. Downloads each file from GitHub Raw (30-second timeout; HTML responses and empty content are failures) and writes them under the project's `./devsnips/` directory — never anywhere else.
5. Creates the project context on first install (`devsnips/config.json`, `devsnips/AGENTS.md`) and records the installation in `config.json` **only after** files are on disk.

Existing files are never overwritten. To reinstall, remove the destination first.

## Mandatory installation verification

Installation success may not be reported until all of these are confirmed:

1. The command exited successfully — check the exit code and output; do not infer success from silence.
2. The expected directory exists: `./devsnips/<technology>/<category>/<family>/<variant>/` (lowercased, technology segment normalized — e.g. `./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/`).
3. The files expected for that type and stack exist inside it (per the registry `files` manifest minus `metadata.json` and `preview.html`).
4. The files correspond to the *requested* resource — the installed folder's `metadata.json` (installed when present) or `README.md` names the right slug/family/variant, not a sibling.
5. No unexpected extra files were introduced.

If any check fails, the installation is a failure, not a partial success. Report it as such and do not proceed to integration as if the files exist.

## Failure behavior

| Failure | CLI behavior |
|---|---|
| Invalid path syntax | "Invalid component path" / "Invalid repository path", exit 1 |
| Unknown resource | "Component not found" + up to 5 "Did you mean one of these?" suggestions, exit 1 |
| No installable files | "No source files found", exit 1 |
| Download failure (network, 404, HTML response, empty content) | "Download failed" naming the file, exit 1 |
| Destination file already exists | "Filesystem error: File already exists…", exit 1 |
| Registry unreachable | "Network error" with connection hint, exit 1 |
| Context update fails after files were written | Reports that files exist at the destination but were not recorded in `config.json`; exit 1 |

## When the CLI cannot run

If `npx devsnips` cannot run (no network, no npm/node, sandboxed container), fall back to reading the files directly from the repository at `library/<registry path>/<filename>` using whatever fetch mechanism is available — and state that the CLI path was not used. Do not fabricate what the CLI would have produced. Note that CLI-run installs additionally create the project context; a manual fetch does not, so `devsnips/config.json` will not list manually-fetched resources.

## Re-installing and idempotency

There is no `--force` flag. If the destination files already exist, remove them first. The install record in `config.json` is de-duplicated: re-running `add` for an already-recorded resource does not create a second record.
