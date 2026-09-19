"""MCP tool registration + the guarded execution boundary.

Every tool body runs through `run_guarded`, so a failure is always a
structured JSON payload â€” never an exception crossing the transport. Tools
are registered with whatever server object the SDK adapter created (v2
MCPServer or v1 FastMCP).

Read-only guarantee: nothing here writes outside the cache dir.
"""

import logging
from collections.abc import Callable
from typing import Any

from ..errors import DevSnipsError, dumps, internal_error_payload
from .context import AppContext, get_context, set_context  # noqa: F401

logger = logging.getLogger("devsnips_mcp")


def run_guarded(tool_name: str, fn: Callable[[], dict[str, Any]]) -> str:
    """Execute a tool body; always return a JSON string, never raise."""
    try:
        return dumps(fn())
    except DevSnipsError as exc:
        logger.warning("%s failed: %s (%s)", tool_name, exc.code, exc.message)
        return dumps(exc.to_payload())
    except Exception as exc:  # noqa: BLE001 â€” the tool boundary must never raise
        return dumps(internal_error_payload(exc))


def register_all(mcp: Any) -> None:
    """Register every v1 tool on the server object."""
    from . import get_resource, get_resource_file, list_facets, search_resources

    search_resources.register(mcp)
    get_resource.register(mcp)
    get_resource_file.register(mcp)
    list_facets.register(mcp)
