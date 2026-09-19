# devsnips-mcp

A lightweight, read-only [MCP](https://modelcontextprotocol.io) server that exposes the
[DevSnips](https://github.com/sarthakbystander/DevSnips) UI library — components, sections
and templates — to AI coding agents over stdio.

It is a **consumer of the existing DevSnips registry** (`snippets-index.json`), never a
second source of truth. It adds no database, no web server, no embeddings, and only one
runtime dependency (the MCP SDK).

```
AI coding agent → devsnips-mcp → snippets-index.json → library/<path>/<file>
```

## What it does

| Tool | Purpose |
| --- | --- |
| `search_resources` | Deterministic keyword/filter search over the whole library |
| `get_resource` | Metadata, README, template AGENTS.md and file manifest for one resource |
| `get_resource_file` | One allowlisted source/doc file from a resource |
| `list_facets` | Current inventory: technologies, types, categories, families (with counts) |

Everything is read-only. Nothing writes outside the cache directory.

## Install

Requires Python 3.10+.

### Option 1 — from PyPI (published releases)

```bash
pip install devsnips-mcp
```

### Option 2 — directly from the DevSnips repository

Installs the latest `main` without waiting for a PyPI release:

```bash
pip install "devsnips-mcp @ git+https://github.com/sarthakbystander/DevSnips.git#subdirectory=integrations/mcp"
```

Run the server directly:

```bash
devsnips-mcp                # console script
python -m devsnips_mcp      # module form
```

## Connect from an MCP client

Clients that support stdio MCP servers launch the server as a subprocess. Configure the
command (and any `env` overrides) in the client's MCP configuration.

### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "devsnips": {
      "command": "devsnips-mcp",
      "args": []
    }
  }
}
```

### Cursor / Windsurf / VS Code (`.mcp.json` or settings)

```json
{
  "mcpServers": {
    "devsnips": {
      "command": "devsnips-mcp",
      "args": []
    }
  }
}
```

Most clients accept the same shape; the two things that vary per client are the config
file location and whether `env` is honored.

## Configuration

All settings are optional environment variables — no CLI flags. A client injects them
through its `env` block.

| Variable | Default | Purpose |
| --- | --- | --- |
| `DEVSNIPS_MCP_SOURCE` | `auto` | `auto` \| `github` \| `local` \| `http` |
| `DEVSNIPS_MCP_REF` | `main` | git ref for the remote registry |
| `DEVSNIPS_MCP_BASE_URL` | `https://raw.githubusercontent.com/sarthakbystander/DevSnips` | remote base |
| `DEVSNIPS_MCP_LOCAL_ROOT` | — | path to a DevSnips checkout (enables `local`) |
| `DEVSNIPS_MCP_CACHE_DIR` | platform cache dir | cache directory |
| `DEVSNIPS_MCP_INDEX_TTL` | `86400` | registry cache TTL (s) |
| `DEVSNIPS_MCP_FILE_TTL` | `604800` | file cache TTL (s) |
| `DEVSNIPS_MCP_TIMEOUT` | `30` | network timeout (s) |
| `DEVSNIPS_MCP_MAX_FILE_BYTES` | `524288` | per-file retrieval cap |
| `DEVSNIPS_MCP_MAX_RESPONSE_BYTES` | `1048576` | per-tool-response cap |
| `DEVSNIPS_MCP_MAX_CACHE_BYTES` | `209715200` | total cache cap |
| `DEVSNIPS_MCP_LOG_LEVEL` | `WARNING` | logging level (goes to stderr) |

`DEVSNIPS_MCP_SOURCE=local` reads a local DevSnips checkout (fastest, fully offline, and
can enumerate the complete file tree of a template, which the remote provider cannot).
`auto` prefers a local checkout when one is detected, else falls back to GitHub raw. `http`
is reserved for a future DevSnips registry API.

### Example (`local` mode)

```json
{
  "mcpServers": {
    "devsnips": {
      "command": "devsnips-mcp",
      "args": [],
      "env": {
        "DEVSNIPS_MCP_SOURCE": "local",
        "DEVSNIPS_MCP_LOCAL_ROOT": "/path/to/DevSnips"
      }
    }
  }
}
```

## Tool usage

Search first, then fetch — every response carries a `registry` provenance block
(source, ref, last-updated, stale flag, variant count).

### search_resources

```text
search_resources(
  query?, technology?, type?, category?, family?, tags?, tagsMode?, styles?,
  features?, installableOnly?, limit?, offset?)
```

```text
search_resources(query="responsive SaaS pricing section", technology="React")
search_resources(query="dark dashboard sidebar", type="component")
search_resources(technology="Tailwind CSS", type="section", family="Pricing")
```

Returns ranked items with `id`, `name`, `type`, `tech`, `category`, `family`, `path`,
`description`, `tags`, `features`, `styles`, `files`, `install`, `score`, `matched_fields`.

### get_resource

```text
get_resource(id, include?, maxBytes?)
```

Returns the canonical metadata plus README (and AGENTS.md for templates), and the file
manifest — without pulling source code into context.

### get_resource_file

```text
get_resource_file(id, file, maxBytes?, truncate?)
```

Fetch one file listed in the resource's manifest (plus README.md/AGENTS.md/metadata.json).
`preview.html` is retrievable only by explicit request.

### list_facets

```text
list_facets(facet?, technology?, includeVariants?)
```

Inventory with live counts — always read from the current registry, never hardcoded.

## Examples for agent prompts

```
"Find a responsive SaaS pricing section for React."
"Find a dark dashboard sidebar."
"Find a minimal hero section using Tailwind."
"List all template families."
```

For a template, prefer `get_resource(id)` to read its AGENTS.md before adapting it, and
fetch multi-page templates page by page with `get_resource_file`, or install the whole
template with the CLI command in its `install` field.

## Security model

- **Read-only** — no write tools; nothing writes outside the cache dir.
- **Path safelisting** — ids and filenames must match strict patterns, and every file is
  checked against the registry manifest allowlist. Arbitrary paths (`..`, absolute paths,
  backslashes, URL-encoded separators) are rejected before any fetch.
- **No arbitrary URLs** — tools never accept URLs; the provider is configured server-side.
- **Remote hardening** — HTML error pages are never treated as content; redirects are
  limited to same-host HTTPS.
- **Oversized responses** — per-file and per-response byte caps with explicit truncation.

## Registry parity

Derived `id` and `install` values mirror the specialized agent indexes
(`agents/resources/indexes/*.json`) and the CLI's installability predicate. This is pinned
by a parity test so any future drift fails loudly.

## Development

```bash
cd integrations/mcp
python -m unittest discover -s tests      # unit + integration + stdio smoke
python scripts/tooling/validators/validate.py   # repo-level validation (from repo root)
ruff check src tests
mypy src/devsnips_mcp
```

Live network tests are opt-in with `DEVSNIPS_MCP_NETWORK_TESTS=1`.

## Relationship to the DevSnips CLI

The CLI (`npx devsnips add <id>`) installs source into a user project; the MCP discovers
and reads the same resources for AI agents. Both resolve against the same registry and
share the same path conventions (`library/<path>/<file>`), installability rules and
`npx devsnips add <id>` install command, but they are separate processes with no runtime
dependency on each other.

## License

MIT. Part of the [DevSnips](https://github.com/sarthakbystander/DevSnips) project.
