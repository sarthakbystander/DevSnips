# DevSnips — Agent Workflows

Procedural playbooks. Each step names the exact repository path to inspect or run, so an agent
can follow them without re-deriving the architecture.

Prerequisite reading: `agents/resources/architecture.md` (layout),
`agents/resources/resources.md` (resource rules), `agents/resources/qa.md` (verification).

## 1. Understanding a task

1. Read the root `AGENTS.md` for repository history/context — but treat it as **stale**; it
   still describes pre-`library/` paths. Verify any path it names before trusting it.
2. Identify the technology and content type by locating the resource under
   `library/{React,Tailwind,Vanilla}/{Components,Sections,Templates}/`.
3. Read the leaf's `metadata.json` and `README.md` (if present) before its code.
4. Read the relevant framework doc: `agents/resources/frameworks/react.md`,
   `frameworks/tailwind.md`, or `frameworks/vanilla.md`.
5. Decide whether the change alters what is on disk. If it does, regeneration is required.

## 2. Modifying an existing resource

```text
1.  Inspect  library/<Tech>/<Type>/<Family>/<slug>/metadata.json
2.  Inspect  library/<Tech>/<Type>/<Family>/<slug>/README.md
3.  Inspect  library/<Tech>/<Type>/<Family>/<slug>/code.*
4.  Inspect  library/<Tech>/<Type>/<Family>/<slug>/preview.html
5.  Inspect  a sibling leaf in the same family for house style
6.  Modify   only the files that need to change; keep the folder name (it is the identity)
7.  Update   metadata.json ONLY if name/description/tags/features/style actually changed
8.  Run      python scripts/tooling/indexing/rebuild_index.py   (if metadata.json changed)
9.  Run      python scripts/tooling/validators/validate.py
10. Verify   the printed output; exit code must be 0
```

Do not rename the folder or change `id` to "improve" naming — `docs/COMPONENT_STRUCTURE.md` and
`docs/CONTRIBUTING.md` both require preserving existing IDs.

## 3. Adding a new resource

```text
1.  Inspect  library/<Tech>/<Type>/ to pick the right family (or add a new family folder)
2.  Inspect  a sibling leaf's file set (agents/resources/resources.md §4) and metadata (§5)
3.  Create   library/<Tech>/<Type>/<Family>/<kebab-slug>/ with exactly the required files
4.  Create   metadata.json with a correct `type` matching the folder bucket
5.  Create   README.md for a component variant (required) or a Vanilla template
6.  Create   AGENTS.md only if this is a template
7.  Run      python scripts/tooling/indexing/rebuild_index.py
8.  Check    the registry entry: snippets-index.json -> the family -> confirm name,
             variantsCount, type, and the variant's `files[]` manifest
9.  Run      python scripts/tooling/validators/deep_check.py
10. Run      python scripts/tooling/validators/validate.py
```

For a new **generated-style** Tailwind or Vanilla section family, the family display name comes
from `SECTION_FAMILY_NAMES` / `VANILLA_SECTION_FAMILY_NAMES` in
`scripts/tooling/indexing/rebuild_index.py`; add a mapping there if the derived name is poor.

## 4. Fixing a validator failure

```text
1. Run      python scripts/tooling/validators/validate.py
2. Read     the "problem(s)" lines verbatim — each names the offending path
3. Map the message to a rule in agents/resources/qa.md ("Common failure classes")
4. Inspect  the exact file the message names
5. Fix      the content, not the validator
6. Re-run   validate.py
7. If the message was index-related, run rebuild_index.py first, then validate.py
```

Never silence a validator to make a change pass. If a failure is pre-existing and unrelated,
`docs/CONTRIBUTING.md` requires you to say so in the pull request rather than fix it silently.

## 5. Modifying CLI behavior

```text
1.  Inspect  cli/src/index.js                (arg parsing / command dispatch)
2.  Inspect  cli/src/commands/add.js         (install flow)
3.  Inspect  cli/src/commands/init.js        (context init)
4.  Inspect  cli/src/registry/resolver.js    (registry fetch + path resolution)
5.  Inspect  cli/src/install/downloader.js   (which files install)
6.  Inspect  cli/src/install/writer.js       (destination layout + write safety)
7.  Inspect  cli/src/devsnips/{config,agents,context}.js   (project context)
8.  Inspect  cli/src/utils/{paths,errors}.js (validation + messaging)
9.  Modify   the module that owns the behavior; keep these module boundaries
10. Update   cli/test/ for the affected module (do not add a test framework)
11. Run      cd cli; npm test
12. Verify   node src/index.js --help still prints the documented flags
```

Do not document a flag without adding it to `cli/src/index.js`. There is no `--force`, no
output-directory option, and no CLI-level config file.
## 6. Updating metadata

```text
1. Inspect  the target leaf's metadata.json
2. Inspect  a sibling leaf's metadata.json in the SAME family and technology
3. Modify   only keys that already exist in that family's shape
4. Verify   `type` still matches the folder bucket
5. Verify   any new `tags` are lowercase and useful for search
6. Run      python scripts/tooling/indexing/rebuild_index.py
7. Inspect  the resulting family/variant entry in snippets-index.json
8. Run      python scripts/tooling/validators/validate.py
```

Remember: `rebuild_index.py` falls back to the previous index for absent fields, so a value can
persist even after you delete it from `metadata.json`. Check the registry after regeneration.

## 7. Updating the index

Only ever via the generator.

```text
1. Confirm  every on-disk leaf has a valid metadata.json (else regeneration refuses to write)
2. Run      python scripts/tooling/indexing/rebuild_index.py
3. Verify   the printed "Validation: OK (indexed content matches disk exactly)" line
4. Verify   the printed "Wrote snippets-index.json" line
5. Run      python scripts/tooling/validators/validate.py
```

If step 3 prints `VALIDATION PROBLEMS`, the index was **not** written. Fix the listed problems
and re-run.

## 8. Framework-specific work

- **React** — `agents/resources/frameworks/react.md`. Sections ship `code.tsx` only; components
  are expected to keep `code.jsx` in parity with `code.tsx`.
- **Tailwind** — `agents/resources/frameworks/tailwind.md`. `code.html` must be a snippet with
  no DOCTYPE/CDN; previews are full pages that do include the CDN.
- **Vanilla** — `agents/resources/frameworks/vanilla.md`. `code.html` is self-contained; the
  quality bar in `scripts/qa/resources/qa_vanilla.py` is machine-enforced for interactive
  families.

Each framework doc ends with its own "inspect these files first" list.

## 9. QA after changes

```text
1. Run   python scripts/tooling/indexing/rebuild_index.py     (only if content changed)
2. Run   python scripts/tooling/validators/validate.py
3. Run   python scripts/tooling/validators/deep_check.py      (file-set changes)
4. Run   python scripts/tooling/validators/check_md_links.py  (Markdown edits)
5. Run   python scripts/tooling/validators/check_agent_doc_paths.py (agents/resources edits)
6. Run   python scripts/tooling/indexing/validate_indexes.py  (index regeneration)
7. Run   python scripts/qa/resources/qa_vanilla.py            (Vanilla changes)
8. Run   cd cli; npm test                                     (cli/ changes)
9. Run   the relevant browser harness                         (visual/interactive changes)
10. Report the exact commands run and their observed results — not a general claim
```

CI runs steps 1–8 on every push and pull request; run them locally first so a push does not fail.

## 10. Investigating a failure

```text
1. Read    the raw error text before changing anything
2. Locate  the code that produced it:
             validate.py messages                 -> scripts/tooling/validators/validate.py
             "NOT writing index ..."              -> scripts/tooling/indexing/rebuild_index.py
             broken-link / unresolved-path        -> scripts/tooling/validators/check_md_links.py
                                                      scripts/tooling/validators/check_agent_doc_paths.py
             CLI error text                       -> cli/src/utils/errors.js
             quality-bar "FAIL <path> <check>"    -> scripts/qa/resources/qa_vanilla.py
3. Inspect the offending artifact
4. Fix     the cause, then re-run only the checks it can affect
5. Re-run  the full flow in section 9 before reporting success
```

If the CLI cannot run (no network/node), do not fabricate what it would have produced — read the
files directly from the registry path plus the `library/` prefix, and say the CLI path was not
used (`agents/skills/devsnips/references/cli_reference.md`).

## 11. Reporting

State what changed, which paths were touched, which commands were run, and their observed
results. Do not report validation success without the printed `VALIDATION PASSED` line, and do
not report an install as working without independently verifying the destination directory
(`agents/skills/devsnips/SKILL.md` and
`agents/skills/devsnips/references/cli_reference.md` define the consume-side contract).