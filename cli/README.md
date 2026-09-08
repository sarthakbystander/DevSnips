# DevSnips CLI

Install UI components from the [DevSnips](https://github.com/sarthakbystander/DevSnips) library into your project.

## Requirements

- Node.js >= 18

## Usage

```bash
npx devsnips add <path>
```

### Examples

```bash
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Vanilla/Components/Buttons/split-button
```

Paths match the repository layout under `Tailwind/`, `React/`, or `Vanilla/`.

### Destination layout

Components are installed under:

```
./devsnips/<tech>/<category>/<family>/<variant>/
```

where `<tech>` is one of `tailwind`, `react`, or `vanilla`.

Example:

| Input | Output |
|-------|--------|
| `Tailwind/Sections/AI-Product/agent-workflow/vercel` | `./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/` |

The leading technology segment is stripped and normalized so it appears only once; remaining segments are lowercased for a consistent on-disk layout.

### Help

```bash
npx devsnips --help
```

## Notes

- Only source files (`code.html`, `code.jsx`, `code.tsx`, etc.) are installed. `metadata.json`, `preview.html`, and `README.md` are skipped.
- Existing files are not overwritten (remove them first if you need to reinstall).
- All writes are confined to the `./devsnips` directory under the current working directory.

## License

MIT — same as the DevSnips repository.
