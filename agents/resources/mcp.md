# DevSnips — MCP integration

Everything an agent needs to know about `devsnips-mcp`, the read-only MCP server that exposes
the DevSnips UI library to AI coding agents over stdio.

Implementation: `integrations/mcp/`. Package: `devsnips-mcp` (PyPI). Console script
`devsnips-mcp`; module form `python -m devsnips_mcp`.

**Role:** MCP is a **consumer** of the existing registry — it reads `snippets-index.json` and
files from `library/<path>/<file>`. It is **never** a second source of truth and never
registers/writes resources. v1 is strictly read-only.

## Location and packaging

- Root: `integrations/mcp/`
- Manifest: `integrations/mcp/pyproject.toml` — name `devsnips-mcp`, version `0.1.0`,
  requires-python `>=3.10`, **single runtime dependency** `mcp>=1.28`.
- Console script: `devsnips-mcp = devsnips_mcp.server:main`
- Package source: `integrations/mcp/src/devsnips_mcp/` (src layout)
- Tests: `integrations/mcp/tests/` (plain `unittest`, no pytest; stdlib-only tests run
  without the SDK installed)
- Docs: `integrations/mcp/README.md`
- Build/QA: `ruff check src tests`, `mypy src/devsnips_mcp`, and
  `python -m unittest discover -s tests` from `integrations/mcp/`.

There is no repository-root Python package — the MCP lives under `integrations/mcp/`.

## SDK adapter (both release lines)

`src/devsnips_mcp/server.py` `create_server()` tries the current stable MCP SDK line first
(`from mcp.server import MCPServer`, spec 2026-07-28), and falls back to the v1.x maintenance
line (`from mcp.server.fastmcp import FastMCP`) on `ImportError`. Tool registration is
SDK-agnostic (`@mcp.tool()`). Stdio is the transport on both lines (`server.run()`).

**stdout is the JSON-RPC wire.** All logging goes to stderr (`setup_logging`); the tool layer
never prints to stdout. `test_stdio_smoke.py` asserts stdout carries protocol frames only.

## Tools (v1)

Registered by `src/devsnips_mcp/tools/__init__.py` `register_all()`. Every tool body runs
through `run_guarded()`, so a failure is always a structured JSON payload with a stable
`error.code`, never an exception crossing the transport.

| Tool | File | Purpose |
| --- | --- | --- |
| `search_resources` | `tools/search_resources.py` | Deterministic keyword/filter search |
| `get_resource` | `tools/get_resource.py` | Metadata + README + template AGENTS.md + file manifest |
| `get_resource_file` | `tools/get_resource_file.py` | One allowlisted source/doc file |
| `list_facets` | `tools/list_facets.py` | Technologies/types/categories/families inventory with counts |

All four return a JSON string; every response carries a `registry` provenance block
(source, ref, origin, schema_version, last_updated, fetched_at, stale, variant_count,
warnings).

## Tool contracts

### search_resources

```text
search_resources(query?, technology?, type?, category?, family?, tags?, tagsMode?,
                 styles?, features?, installableOnly?, limit?, offset?)
```

- `type`: `component` | `section` | `template` (validated).
- `category`: `Components` | `Sections` | `Templates` (validated).
- `technology`: any of the registered display names or a known alias (`react`, `tailwind`,
  `vanilla`, `html`, `css`, `js`, ...). Unknown technologies pass through as an exact
  display-name match (index-driven — future technologies work without MCP changes).
- `tagsMode`: `all` (AND, default) or `any` (OR).
- `limit` 1–50 default 10; `offset` >= 0.
- Returns `{ mode, items, total_matches, truncated, query, registry }`. `mode` is
  `exact` | `partial` | `fuzzy` | `filtered`.

Ranking is deterministic: field-weighted token scoring, exact-id bonus, type-intent
bonus/penalty, and a fixed tie-break (score desc → exact-name → shorter id → id ascending).
No randomness, no embeddings. See `search/engine.py`, `search/scoring.py`,
`search/tokenizer.py`.

### get_resource

```text
get_resource(id, include?, maxBytes?)
```

- `id`: canonical registry id, e.g. `Tailwind/Components/Accordions/basic-accordion`.
- `include`: subset of `metadata`, `readme`, `agents`, `files`, `family` (default
  `metadata`+`readme`+`files`; templates auto-add `agents` when `AGENTS.md` exists).
- Returns metadata, docs (README/AGENTS), file manifest, and `files_complete` honesty flag.

`files_complete` is `true` only when the provider can walk the real tree (local checkout).
GitHub raw cannot enumerate directories; some React template manifests list only one level
of `src/**`, so `files_complete: false` + a `files_note` is returned in remote mode.

### get_resource_file

```text
get_resource_file(id, file, maxBytes?, truncate?)
```

- `file`: a file listed in the variant's manifest, plus the documented doc set
  (`README.md`, `AGENTS.md`, `metadata.json` by explicit request). `preview.html` is never
  bundled implicitly.
- `maxBytes`: byte cap (default server setting 512 KiB); `truncate: false` returns
  `file_too_large` instead of truncating.
- Returns `content`, `bytes`, `truncated`, `encoding_lossless`, `source`, `install`, `registry`.

### list_facets

```text
list_facets(facet?, technology?, includeVariants?)
```

- `facet`: `all` | `technologies` | `types` | `categories` | `families`.
- `includeVariants`: for the families facet, list variant ids (capped at 500).
- Inventory is read from the current registry, never hardcoded — so a technology or type
  added after this server shipped appears automatically.

## Registry and source of truth

- The MCP parses `snippets-index.json` (`src/devsnips_mcp/models.py` `parse_registry`)
  directly. A malformed family/variant is skipped with a warning, never fatal.
- Master index variants have **no `id` field** — `id` is the path minus the trailing slash
  (`src/devsnips_mcp/index/schema.py` `derive_id`).
- `install` (`npx devsnips add <id>`) is derived only when at least one file passes the
  CLI's installability predicate (`is_installable`), mirroring
  `cli/src/install/downloader.js` `getSourceFiles`.
- **Parity:** `tests/test_parity.py` asserts MCP-derived ids/installs/types agree with the
  specialized indexes (`agents/resources/indexes/*.json`) for every variant. This is a
  required gate against drift between MCP, the CLI, and the index contract.
- Schema gate: `SUPPORTED_REGISTRY_SCHEMA = {"2.0"}` (`src/devsnips_mcp/__init__.py`). An
  unknown version is served in degraded mode (`schema.supported: false`), never a hard
  failure — covered by `tests/test_contract.py`.

## Providers (data access)

`src/devsnips_mcp/registry/provider.py` defines the `RegistryProvider` protocol with exactly
three questions: `load_registry()`, `read_file()`, `list_files()`. Tools never see or accept
a URL — the provider is chosen server-side, so moving DevSnips from GitHub raw to a CDN or a
future registry API is a config change, not a tool-contract change.

- `GitHubRawProvider` (`registry/github.py`) — default. Registry from
  `{base_url}/{ref}/snippets-index.json`, files from `library/<path>/<file>`. Same-host HTTPS
  redirects only; HTML responses and empty bodies rejected.
- `LocalRepoProvider` (`registry/local.py`) — reads a DevSnips checkout; the only provider
  that can enumerate the real file tree (recovers nested files the manifest omits).
- Source selection (`tools/context.py` `_select_provider`): `DEVSNIPS_MCP_SOURCE`
  `auto` (default: prefer a local checkout when detected, else GitHub raw) | `github` |
  `local` | `http` (reserved for a future registry API).

Repo-relative path mapping mirrors the CLI (`library_rel_path` → `library/<path>/<file>`).

## Caching

`src/devsnips_mcp/cache/` — one directory of small files, JSON sidecar metadata, atomic
writes (`os.replace`), LRU eviction under a byte cap (registry entries never evicted),
ETag/304 revalidation, corruption recovery, per-OS default cache dir (stdlib only). Cache
serves stale copies when the origin is unreachable, so the MCP stays useful offline.

## Configuration

All settings are optional environment variables (no CLI flags — MCP clients inject them via
their `env` block). See `src/devsnips_mcp/config.py` `Settings.from_env()`. Key variables:

- `DEVSNIPS_MCP_SOURCE` (`auto`), `DEVSNIPS_MCP_REF` (`main`),
  `DEVSNIPS_MCP_BASE_URL` (GitHub raw), `DEVSNIPS_MCP_LOCAL_ROOT`
- `DEVSNIPS_MCP_CACHE_DIR`, `DEVSNIPS_MCP_INDEX_TTL` (`86400`),
  `DEVSNIPS_MCP_FILE_TTL` (`604800`), `DEVSNIPS_MCP_TIMEOUT` (`30`),
  `DEVSNIPS_MCP_MAX_FILE_BYTES` (`524288`), `DEVSNIPS_MCP_MAX_RESPONSE_BYTES` (`1048576`),
  `DEVSNIPS_MCP_MAX_CACHE_BYTES` (`209715200`), `DEVSNIPS_MCP_LOG_LEVEL` (`WARNING`)

## Security model

- **Read-only** — no write tools; nothing writes outside the cache dir.
- **Dual path gates** (`src/devsnips_mcp/files/resolver.py`): (1) ids and filenames must
  match strict regex patterns (no `..`, no backslashes, no absolute paths, no URL-encoded
  separators, bounded length); (2) the id must exist in the loaded registry and the filename
  must be a member of that variant's manifest (+ documented doc set). A traversal string can
  never reach a fetch.
- **No arbitrary URLs** — tools never accept them; the provider is configured server-side.
- **Remote hardening** (`registry/github.py`): same-host HTTPS redirects only; HTML error
  pages never served as content; empty bodies treated as failures.

## Error model

`src/devsnips_mcp/errors.py` — stable codes: `invalid_argument`, `path_rejected`,
`resource_not_found`, `file_not_found`, `not_installable`, `file_too_large`,
`registry_unavailable`, `registry_invalid`, `schema_unsupported`, `internal_error`. Errors
are returned as structured JSON (`{ error: { code, message, details } }`), never raised to
the transport. `internal_error` carries a `trace_id` for log correlation.

## Relationship to the CLI

The CLI (`cli/`, `npx devsnips add <id>`) installs source into a user project; the MCP
discovers and reads the same resources for AI agents. Both resolve against the same registry
and share path conventions, installability rules and the `npx devsnips add <id>` install
command — but they are separate processes with no runtime dependency on each other.

## Testing

From `integrations/mcp/`:

```bash
python -m unittest discover -s tests
ruff check src tests
mypy src/devsnips_mcp
```

- Unit: models, schema gate, search determinism, path/file resolver, cache (TTL, 304,
  atomicity, LRU, corruption), providers (stubbed fetcher).
- Contract: future schema versions, unknown technologies/types, renamed/missing fields,
  empty registries, oversized strings — every tool returns structured JSON, never raises.
- Parity: derived ids/installs vs specialized indexes for every variant.
- Integration: tool-level tests through a fake MCP registry; in-process client tests and a
  real stdio subprocess smoke test when the SDK is installed.
- Live network: opt-in via `DEVSNIPS_MCP_NETWORK_TESTS=1`.

Current expected result: 101 tests pass, 3 skipped (live-network opt-in).

## Not in the MCP (v1)

Verified absent; do not document these as features: any write/install tool, HTTP/SSE
transport, hosted server, embeddings/vector search, a second registry, PyPI publishing
tooling, or a Registry API. `http` source is reserved but has no provider implementation yet.
