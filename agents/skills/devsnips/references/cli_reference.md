# DevSnips CLI — usage & verification reference

Package: https://www.npmjs.com/package/devsnips

## Basic usage

```bash
npx devsnips add <path>
```

`<path>` is the variant's `path` field from the current `snippets-index.json`
(see `registry_schema.md`) — e.g.:

```bash
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add Vanilla/Components/Buttons/split-button
```

For anything uncertain about syntax, options, or current behavior, ask the
CLI itself rather than assuming from this doc or from training data:

```bash
npx devsnips --help
npx devsnips --version
```

Do not invent flags, output formats, or destination-directory conventions
that the installed CLI hasn't confirmed.

## Mandatory installation verification

Per SKILL.md's Phase 3 contract, installation success may **not** be reported
until every one of these is confirmed:

1. The `npx devsnips add <path>` command exited successfully (check the exit
   code / absence of an error in output — don't infer success from silence).
2. The expected directory exists:
   `./devsnips/<technology>/<category>/<family>/<variant>/`
3. The files expected for that resource type/stack exist inside it (see the
   file-set table in `registry_schema.md`).
4. The files correspond to the **requested** resource — check `metadata.json`
   inside the installed folder names the right `slug`/`family`/`variant`,
   not a sibling or a stale/cached copy.
5. No unexpected extra files were introduced (nothing outside what the
   resource's own `files` list in the registry describes).

If any of these fail, the installation is a **failure**, not a partial
success — report it as such (see SKILL.md's Failure Handling table) and do
not proceed to Integrate/Adapt as if the files exist.

## When the CLI is unavailable or fails

- If `npx devsnips` cannot run in the current environment (no network, no
  npm/node, sandboxed container without outbound access), fall back to
  reading the file(s) directly from the repository/raw source instead of
  fabricating what the CLI would have produced — fetch the exact `path` +
  filename from `registry_schema.md`'s file-set table via whatever fetch
  tool is available, and note to the user that the CLI path wasn't used.
- If the command fails, read the actual error text before retrying. Only
  retry with a change that's justified by that error (e.g. a corrected path
  confirmed against the current registry) — don't guess-and-check flags.
- Never claim an installation succeeded because a *previous* invocation in
  this conversation succeeded for a different resource. Verify every
  install independently.
