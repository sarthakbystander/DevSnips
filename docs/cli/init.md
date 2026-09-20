# CLI — `init`

`npx devsnips init` creates the DevSnips project context in the current working directory without installing anything. Implementation: `cli/src/commands/init.js`; tests: `cli/test/init.test.js`.

## Syntax

```bash
npx devsnips init
```

No arguments or options. Requires network access? No — `init` is fully local.

## Behavior

1. If **both** `devsnips/config.json` and `devsnips/AGENTS.md` already exist, print "DevSnips project context already initialized." and exit 0 without touching anything (idempotent).
2. Otherwise:
   - create `./devsnips/` (if missing);
   - create `./devsnips/config.json` if missing — `{ "version": 1, "project": {}, "resources": [] }`;
   - create `./devsnips/AGENTS.md` if missing — the default agent instructions;
   - report which files were created; exit 0.

## Expected output

First run:

```text
DevSnips

  Initializing DevSnips project context... ✓
  Created devsnips/AGENTS.md
  Created devsnips/config.json

✓ DevSnips project initialized successfully
```

Subsequent run:

```text
DevSnips

  DevSnips project context already initialized.
```

## Failure behavior

| Condition | Result |
|---|---|
| Existing `devsnips/config.json` is malformed JSON or not an object | "✗ Initialization failed" with the parse error; the file is left byte-for-byte untouched; exit 1 |
| Filesystem write failure | "✗ Initialization failed" with the OS error; exit 1 |

A malformed `config.json` is an error, never silently replaced. Fix or remove the file and re-run.

## Filesystem changes

| Change | When |
|---|---|
| `./devsnips/` directory | Created if missing |
| `./devsnips/config.json` | Created only when missing |
| `./devsnips/AGENTS.md` | Created only when missing — never overwritten once it exists |

## Relationship to `add`

`add` performs the same initialization automatically on the first successful install, so `init` is optional. Use it when you want the context (notably the agent instructions file) present before any install. The contracts of the two created files are described in [Configuration](configuration.md).

## Notes for agents

- Running `init` in a project that already has the context is a safe no-op.
- `init` never reports the project's stack; `config.json`'s `project` object is CLI-protected and left empty by the CLI itself (the CLI never fabricates project information it cannot know).
- After `init`, an agent should read `devsnips/AGENTS.md` before doing UI work — it carries the adaptation rules and quality checks that govern how installed resources are used in that project.
