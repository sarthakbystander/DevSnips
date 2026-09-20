# DevSnips MCP

`devsnips-mcp` is a lightweight, read-only [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes the DevSnips UI library to AI coding agents over stdio. This page covers what it does, how to connect, the full tool contracts, how it reads data, and its security model.

```
AI coding agent → devsnips-mcp → snippets-index.json → library/<path>/<file>
```

The MCP is a **consumer** of DevSnips, not a second database. It reads the same canonical registry (`snippets-index.json`) and the same `library/` tree that the CLI, the website, and the agent docs use. It never registers or writes resources; v1 is strictly read-only.

## Why use it

- Let an AI coding agent find the right component or section inside your editor.
- Fetch full template source, page by page, into context.
- Always current inventory — read from the live registry, never hardcoded.
- One runtime dependency (the MCP SDK), no database, no embeddings, no web server.

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

Run directly to confirm it starts:

```bash
devsnips-mcp
python -m devsnips_mcp
```

## Connect from a client

Clients that support stdio MCP servers launch the server as a subprocess. All major clients use the same `command`/`args` shape; they differ only in the config file location and whether `env` is honored.

### Claude Desktop — `claude_desktop_config.json`

```json
{ "mcpServers": { "devsnips": { "command": "devsnips-mcp", "args": [] } } }
```

### Cursor — `.cursor/mcp.json`

```json
{ "mcpServers": { "devsnips": { "command": "devsnips-mcp", "args": [] } } }
```

### Windsurf — `mcp_config.json`

```json
{ "mcpServers": { "devsnips": { "command": "devsnips-mcp", "args": [] } } }
```

### Using a local checkout (offline, complete file trees)

```json
{ "mcpServers": { "devsnips": {
    "command": "devsnips-mcp", "args": [],
    "env": { "DEVSNIPS_MCP_SOURCE": "local", "DEVSNIPS_MCP_LOCAL_ROOT": "/path/to/DevSnips" }
} } }
```

`local` mode is fully offline and can enumerate the complete file tree of a template. The default `auto` mode prefers a local checkout when one is detected, otherwise fetches from GitHub.

## How it reads data (providers)

Tools never see or accept a URL — data access is chosen server-side through a provider. This means moving DevSnips from GitHub raw to a CDN or a future registry API is a config change, not a tool-contract change.

- **GitHub raw (default).** Registry from `{base_url}/{ref}/snippets-index.json`, files from `library/<path>/<file>`. Same-host HTTPS redirects only; HTML responses and empty bodies are rejected.
- **Local checkout.** Reads a DevSnips checkout on disk; the only provider that can enumerate the real file tree (recovers nested files the manifest omits).
- **Source selection** (`DEVSNIPS_MCP_SOURCE`): `auto` (default: prefer local, else GitHub raw) · `github` · `local` · `http` (reserved for a future registry API, not yet implemented).

**stdout is the JSON-RPC wire.** All logging goes to stderr; the tool layer never prints to stdout. The server adapts to both MCP SDK lines (`MCPServer` on the current line, `FastMCP` on the v1 maintenance line).

## Caching

One directory of small files with JSON sidecar metadata: atomic writes, LRU eviction under a byte cap (registry entries never evicted), ETag/304 revalidation, and corruption recovery. The cache serves stale copies when the origin is unreachable, so the MCP stays useful offline. Defaults: index TTL 1 day, file TTL 7 days, per-OS cache directory.

## Tools and contracts

Every tool returns a JSON string and carries a `registry` provenance block (source, ref, origin, schema_version, last_updated, fetched_at, stale, variant_count, warnings). A failure is always a structured `{ error: { code, message, details } }` payload — never an exception across the transport.

| Tool | What it does |
|---|---|
| `search_resources` | Keyword + filter search over the whole library |
| `get_resource` | Metadata, README, template AGENTS.md, and the file manifest for one resource |
| `get_resource_file` | One allowlisted source/doc file from a resource |
| `list_facets` | List current technologies, types, categories, families (with counts) |

### search_resources

```text
search_resources(query?, technology?, type?, category?, family?, tags?, tagsMode?,
                 styles?, features?, installableOnly?, limit?, offset?)
```

- `type`: `component` | `section` | `template`; `category`: `Components` | `Sections` | `Templates`.
- `technology`: a registered display name or a known alias (`react`, `tailwind`, `vanilla`, …). Unknown technologies pass through as exact display-name matches, so future technologies work without MCP changes.
- `tagsMode`: `all` (AND, default) or `any` (OR). `limit` 1–50 (default 10), `offset` ≥ 0.
- Returns `{ mode, items, total_matches, truncated, query, registry }` where `mode` is `exact` | `partial` | `fuzzy` | `filtered`. Ranking is deterministic — field-weighted token scoring with a fixed tie-break; no embeddings, no randomness.

### get_resource

```text
get_resource(id, include?, maxBytes?)
```

- `id`: canonical registry id, e.g. `Tailwind/Components/Accordions/basic-accordion`.
- `include`: subset of `metadata`, `readme`, `agents`, `files`, `family` (default `metadata`+`readme`+`files`; templates auto-add `agents` when `AGENTS.md` exists).
- Returns metadata, docs, the file manifest, and a `files_complete` honesty flag — `true` only when the provider can walk the real tree (local checkout). In remote mode a template manifest may list only one level of `src/**`, so you get `files_complete: false` plus a `files_note`.

### get_resource_file

```text
get_resource_file(id, file, maxBytes?, truncate?)
```

- `file`: a file listed in the variant's manifest, plus the documented doc set (`README.md`, `AGENTS.md`, `metadata.json` by explicit request). `preview.html` is never bundled implicitly.
- `maxBytes`: byte cap (default 512 KiB); `truncate: false` returns `file_too_large` instead of truncating.
- Returns `content`, `bytes`, `truncated`, `encoding_lossless`, `source`, `install`, `registry`.

### list_facets

```text
list_facets(facet?, technology?, includeVariants?)
```

- `facet`: `all` | `technologies` | `types` | `categories` | `families`.
- `includeVariants`: for the families facet, list variant ids (capped at 500).
- Inventory is read from the current registry, never hardcoded — so a technology or type added after this server shipped appears automatically.

- Inventory is read from the current registry, never hardcoded — so a technology or type added after this server shipped appears automatically.

## Registry integrity

- The MCP parses `snippets-index.json` directly; a malformed family/variant is skipped with a warning, never fatal.
- Master index variants have **no `id` field** — `id` is the path minus the trailing slash.
- `install` (`npx devsnips add <id>`) is derived only when at least one file passes the CLI's installability predicate — mirroring the CLI exactly.
- **Parity:** a dedicated test asserts MCP-derived ids/installs/types agree with the specialized indexes for every variant — the gate against drift between MCP, the CLI, and the index contract.
- **Schema gate:** supported registry schema is `2.0`. An unknown version is served in degraded mode (`schema.supported: false`), never a hard failure.

## Security model

- **Read-only** — no write tools; nothing writes outside the cache directory.
- **Dual path gates** — (1) ids and filenames must match strict patterns (no `..`, no backslashes, no absolute paths, no URL-encoded separators, bounded length); (2) the id must exist in the loaded registry and the filename must be a member of that variant's manifest (+ documented doc set). A traversal string can never reach a fetch.
- **No arbitrary URLs** — tools never accept them; the provider is configured server-side.
- **Remote hardening** — same-host HTTPS redirects only; HTML error pages are never served as content; empty bodies treated as failures.
- **Error model** — stable codes (`invalid_argument`, `path_rejected`, `resource_not_found`, `file_not_found`, `not_installable`, `file_too_large`, `registry_unavailable`, `registry_invalid`, `schema_unsupported`, `internal_error`), each as structured JSON.

## Configuration reference

All settings are optional environment variables (no CLI flags — clients inject them via `env`). Key variables:

| Variable | Default | Purpose |
|---|---|---|
| `DEVSNIPS_MCP_SOURCE` | `auto` | `auto` \| `github` \| `local` \| `http` |
| `DEVSNIPS_MCP_REF` | `main` | git ref for the remote registry |
| `DEVSNIPS_MCP_LOCAL_ROOT` | — | path to a DevSnips checkout |
| `DEVSNIPS_MCP_CACHE_DIR` | platform cache dir | cache location |
| `DEVSNIPS_MCP_INDEX_TTL` | `86400` | registry TTL (seconds) |
| `DEVSNIPS_MCP_FILE_TTL` | `604800` | file TTL (seconds) |
| `DEVSNIPS_MCP_TIMEOUT` | `30` | network timeout (seconds) |
| `DEVSNIPS_MCP_MAX_FILE_BYTES` | `524288` | per-file retrieval cap |
| `DEVSNIPS_MCP_MAX_RESPONSE_BYTES` | `1048576` | per-tool-response cap |
| `DEVSNIPS_MCP_MAX_CACHE_BYTES` | `209715200` | total cache cap |
| `DEVSNIPS_MCP_LOG_LEVEL` | `WARNING` | logging level (stderr) |

See the package [README](https://github.com/sarthakbystander/DevSnips/tree/main/integrations/mcp) for the full table.

## Example agent prompts

```
Find a responsive SaaS pricing section for React.
Find a dark dashboard sidebar.
Find a minimal hero section using Tailwind.
List all template families.
Get the docs for Tailwind/Templates/ai-saas-platform.
```

For templates, read the resource's AGENTS.md (`get_resource`) before adapting it, and fetch multi-page templates page by page with `get_resource_file`, or install the whole template with the CLI command shown in its `install` field.

## Development

```bash
cd integrations/mcp
python -m unittest discover -s tests   # unit + contract + parity + integration + stdio smoke
ruff check src tests
mypy src/devsnips_mcp
```

Live network tests are opt-in via `DEVSNIPS_MCP_NETWORK_TESTS=1`.

## Go deeper

This page is the human-facing MCP reference. The implementation-anchored reference (provider protocol, cache internals, the search scoring pipeline, and the full test matrix) is maintained for agents in [`agents/resources/mcp.md`](https://github.com/sarthakbystander/DevSnips/blob/main/agents/resources/mcp.md).

