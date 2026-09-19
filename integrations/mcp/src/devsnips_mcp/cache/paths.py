"""Per-OS cache directory resolution (stdlib only — no platformdirs)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

APP_DIR_NAME = "devsnips-mcp"


def default_cache_dir(environ: dict[str, str] | None = None) -> Path:
    """Resolve the default cache directory for the current platform.

    - Windows: %LOCALAPPDATA%\\devsnips-mcp\\cache
    - macOS:   ~/Library/Caches/devsnips-mcp
    - Linux:   $XDG_CACHE_HOME/devsnips-mcp  (fallback ~/.cache/devsnips-mcp)
    """
    env = dict(os.environ if environ is None else environ)

    def _get(name: str) -> str | None:
        value = env.get(name)
        return value if value not in (None, "") else None

    override = _get("DEVSNIPS_MCP_CACHE_DIR")
    if override:
        return Path(override).expanduser()

    if sys.platform.startswith("win"):
        base = _get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / APP_DIR_NAME / "cache"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / APP_DIR_NAME
    base = _get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / APP_DIR_NAME
