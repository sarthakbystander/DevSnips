"""devsnips-mcp server entry point.

SDK adapter: the server code is identical on both MCP Python SDK release lines.

- Current stable line (pip install mcp â†’ 2.x, spec 2026-07-28):
      from mcp.server import MCPServer
- v1.x maintenance line:
      from mcp.server.fastmcp import FastMCP

stdio is the transport on both (`mcp.run()` defaults to stdio). stdout is the
wire â€” logging is configured to stderr and the tool layer never prints.

Run:
    devsnips-mcp                 # console script
    python -m devsnips_mcp       # module form
    mcp run server.py            # via the SDK's [cli] extra (dev only)
"""

import logging
import sys

from . import SERVER_NAME, __version__
from .config import Settings


def setup_logging(level: str = "WARNING") -> None:
    """Logging MUST go to stderr: stdout is the stdio JSON-RPC wire."""
    logging.basicConfig(
        stream=sys.stderr,
        level=getattr(logging, level.upper(), logging.WARNING),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def create_server(name: str = SERVER_NAME):
    """Build the MCP server object and register the v1 tools (SDK-agnostic)."""
    try:  # current stable line (mcp 2.x)
        from mcp.server import MCPServer
        server = MCPServer(name)
    except ImportError:  # v1.x maintenance line
        # On mcp 2.x this module path exists but only raises ModuleNotFoundError,
        # so type checkers cannot see FastMCP on it. The branch is unreachable there.
        from mcp.server.fastmcp import FastMCP  # type: ignore[attr-defined]
        server = FastMCP(name)

    from .tools import register_all
    register_all(server)
    return server


def main() -> None:
    settings = Settings.from_env()
    setup_logging(settings.log_level)
    logging.getLogger("devsnips_mcp").info(
        "devsnips-mcp %s starting (source=%s ref=%s)", __version__,
        settings.source, settings.ref)
    server = create_server()
    server.run()  # blocks; stdio transport


if __name__ == "__main__":
    main()
