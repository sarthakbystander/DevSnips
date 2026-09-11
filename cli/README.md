# DevSnips CLI

Install UI components from the [DevSnips](https://github.com/sarthakbystander/DevSnips) library into your project.

## Requirements

- Node.js >= 18

## Usage

```bash
npx devsnips add <path>
npx devsnips init
```

### Examples

```bash
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Vanilla/Components/Buttons/split-button
npx devsnips init
```

Paths match the repository layout under `Tailwind/`, `React/`, or `Vanilla/`.

### Destination layout

Components, sections, and templates are installed under:

```
./devsnips/<tech>/<category>/<family>/<variant>/
```

where `<tech>` is one of `tailwind`, `react`, or `vanilla`.

Example:

| Input | Output |
|-------|--------|
| `Tailwind/Sections/AI-Product/agent-workflow/vercel` | `./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/` |

The leading technology segment is stripped and normalized so it appears only once; remaining segments are lowercased for a consistent on-disk layout.

### Project context

DevSnips maintains project context inside:

```text
./devsnips/
├── AGENTS.md
├── config.json
└── <installed resources>
```

- `AGENTS.md` provides project-wide instructions for AI coding agents working with DevSnips resources.
- `config.json` stores machine-readable DevSnips project state and installed resources.

The context is initialized automatically the first time `add` is used, or manually with:

```bash
npx devsnips init
```

Existing `AGENTS.md` files are never overwritten by the CLI. You may edit this file to add project-specific instructions.

### Help and version

```bash
npx devsnips --help
npx devsnips --version
```

## Notes

- Any registry entry can be installed: components, sections, or templates
- Source files (`code.html`, `code.jsx`, `code.tsx`, `pages/*.html`, etc.) are installed.
- `README.md` is installed when present.
- `AGENTS.md` is installed when present in the resource directory (this is separate from the project-level `devsnips/AGENTS.md`).
- `metadata.json` and `preview.html` are skipped.
- Existing files are not overwritten (remove them first if you need to reinstall).
- All writes are confined to the `./devsnips` directory under the current working directory.
- The `devsnips/config.json` file is updated automatically after each successful installation.
- The `devsnips/AGENTS.md` file is created only once and never overwritten.

## License

MIT — same as the DevSnips repository.
