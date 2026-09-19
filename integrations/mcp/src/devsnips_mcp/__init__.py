"""devsnips_mcp — a read-only MCP server for the DevSnips UI library."""
from __future__ import annotations

__version__ = "0.1.0"

# Registry schema versions this server understands. An unknown version never
# hard-fails: the server serves in degraded mode and marks every response with
# schema.supported = False (see index/schema.py).
SUPPORTED_REGISTRY_SCHEMA = frozenset({"2.0"})

SERVER_NAME = "devsnips"
