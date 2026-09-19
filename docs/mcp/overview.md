# DevSnips MCP

`devsnips-mcp` is a lightweight, read-only [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
server that exposes the DevSnips UI library to AI coding agents. Agents can search the
library, fetch resources and their documentation, and pull individual source files — over a
standard stdio MCP connection launched by your coding client.

```
AI coding agent → devsnips-mcp → snippets-index.json → library/<path>/<file>
```

The MCP is a **consumer** of DevSnips, not a second database. It reads the same canonical
registry (`snippets-index.json`) and the same `library/` tree that the CLI, the website, and
the agent docs use.

## Why use it

- Let an AI coding agent find the right component or section inside your editor.
- Fetch full template source, page by page, into context.
- Always current inventory — read from the live registry, never hardcoded.
- One runtime dependency, no database, no embeddings, no web server.

## Install

Requires Python 3.10+.

```bash
pip install devsnips-mcp
```

Run directly to confirm it starts:

```bash
devsnips-mcp
python -m devsnips_mcp
```

## Connect from a client

Clients that support stdio MCP servers launch the server as a subprocess. All major clients
use the same `command`/`args` shape; they differ only in the config file location and
whether `env` is honored.

### Claude Desktop — `claude_desktop_config.json`

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

### Cursor — `.cursor/mcp.json`

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

### Windsurf — `mcp_config.json`

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

### Using a local checkout (offline, complete file trees)

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

`local` mode is fully offline and can enumerate the complete file tree of a template. The
default `auto` mode prefers a local checkout when one is detected, otherwise fetches from
GitHub.

## Tools

| Tool | What it does |
| --- | --- |
| `search_resources` | Keyword + filter search over the whole library |
| `get_resource` | Metadata, README, template AGENTS.md, and the file manifest for one resource |
| `get_resource_file` | One allowlisted source/doc file from a resource |
| `list_facets` | List current technologies, types, categories, families (with counts) |

Search is deterministic and keyword-based — the same query always returns the same results,
no embeddings.

## Example agent prompts

```
Find a responsive SaaS pricing section for React.
Find a dark dashboard sidebar.
Find a minimal hero section using Tailwind.
List all template families.
Get the docs for Tailwind/Templates/ai-saas-platform.
```

For templates, read the resource's AGENTS.md (`get_resource`) before adapting it, and fetch
multi-page templates page by page with `get_resource_file`, or install the whole template
with the CLI command shown in its `install` field.

## Configuration reference

All settings are optional environment variables. See the package
[README](https://github.com/sarthakbystander/DevSnips/tree/main/integrations/mcp) for the
full table and defaults. Key variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DEVSNIPS_MCP_SOURCE` | `auto` | `auto` \| `github` \| `local` \| `http` |
| `DEVSNIPS_MCP_REF` | `main` | git ref for the remote registry |
| `DEVSNIPS_MCP_LOCAL_ROOT` | — | path to a DevSnips checkout |
| `DEVSNIPS_MCP_CACHE_DIR` | platform cache dir | cache location |
| `DEVSNIPS_MCP_LOG_LEVEL` | `WARNING` | logging level (stderr) |

## Security

The MCP is intentionally read-only. It never writes outside its cache directory, never
accepts arbitrary URLs or paths (every file is checked against the registry manifest
allowlist), and caps oversized responses. See the package README for details.

## Development

```bash
cd integrations/mcp
python -m unittest discover -s tests
ruff check src tests
mypy src/devsnips_mcp
```

Deep agent-facing reference: `agents/resources/mcp.md`.
