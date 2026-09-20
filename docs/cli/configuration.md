# CLI — configuration (project context)

The DevSnips project context lives entirely inside `./devsnips/` under the current working directory. It consists of one machine-readable file (CLI-managed) and one instructions file (user-owned).

```text
./devsnips/
├── config.json     # machine-readable install state — CLI-managed
├── AGENTS.md       # instructions for AI agents — user-owned
└── <installed resources>/
```

## `devsnips/config.json`

Schema (version 1):

```json
{
  "version": 1,
  "project": {},
  "resources": [
    {
      "path": "Vanilla/Components/Buttons/split-button",
      "technology": "Vanilla HTML/CSS/JS",
      "installedAt": "2026-09-11T23:26:00.000Z"
    }
  ]
}
```

| Field | Type | Meaning |
|---|---|---|
| `version` | integer | Config schema version. Currently `1`. |
| `project` | object | Reserved for project metadata. The CLI never fabricates project/framework information it cannot know; `project` is preserved verbatim across rewrites. |
| `resources` | array | One record per successful installation, components/sections/templates alike. |
| `resources[].path` | string | The canonical registry path of the installed resource. |
| `resources[].technology` | string | The registry technology string (e.g. `Vanilla HTML/CSS/JS`). |
| `resources[].installedAt` | string | ISO-8601 timestamp of the installation. |

Behavioral contract:

- **CLI-managed.** Created when absent, updated automatically after each successful install. Do not edit it by hand.
- **Atomic writes.** Written via a same-directory temp file + rename, so a failed write never leaves truncated JSON.
- **Fail-safe on corruption.** A malformed existing `config.json` is an **error** (exit 1); the file is left byte-for-byte untouched and is never silently replaced.
- **De-duplicated.** Recording the same path twice does not create duplicate records.
- **Records only real installs.** The record is written only after resource files are on disk, so `resources[]` always reflects actual installations.

## `devsnips/AGENTS.md`

Instructions for AI coding agents working with DevSnips resources in this project. Created once by `init` or the first `add`, then **never overwritten by the CLI** — this is asserted by tests (`cli/test/agents.test.js`, `cli/test/context.test.js`) and stated in the implementation. You may edit it freely to add project-specific instructions.

Default content sections:

1. **General rules** — inspect the existing project before modifying UI; preserve the project's design language; reuse existing patterns; no unnecessary dependencies; keep UI responsive and accessible; avoid duplication; prefer existing project components.
2. **Resource adaptation** — installed resources are starting points; inspect the resource's `README.md` and source; adapt to project conventions; preserve intended functionality; do not blindly copy details that conflict with the project's architecture; reuse existing tokens, utilities, components.
3. **Quality checks** — responsive behavior, accessibility, keyboard interaction, focus states, hover/interaction states, contrast, typography and spacing consistency, overflow, semantic structure, and no unnecessary CSS/JS/dependencies.
4. **Important** — `config.json` is CLI-managed, do not edit manually; the instructions file itself must not be modified automatically; project-specific instructions may be appended below the defaults.

## What belongs where

| Information | Belongs in |
|---|---|
| What is installed, when | `config.json` |
| How agents should treat resources in *this* project | `AGENTS.md` (project-level, user-edited) |
| What a resource is and how it behaves | The resource's `metadata.json` / `README.md` |
| How the DevSnips system works | This documentation tree (`docs/`) |
| Operational consume-side rules | The `devsnips` agent skill |

## Deleting the context

There is no CLI command for removal. To reset the context, delete the `./devsnips/` directory (or individual installed resource folders plus their `resources[]` entries) manually. Removing files without updating `config.json` leaves stale records; agents should treat `config.json` records as "was installed", not "is currently present".
