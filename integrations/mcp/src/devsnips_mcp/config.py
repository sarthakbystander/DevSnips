"""devsnips_mcp configuration.

All settings come from environment variables with sane defaults. There is no
CLI flag parser on purpose: MCP clients launch this server as a subprocess and
configure it through their own JSON config (`env` block), so environment
variables are the lowest-friction, client-agnostic configuration surface.

Every variable is optional:

    DEVSNIPS_MCP_SOURCE            auto | github | local | http   (default: auto)
    DEVSNIPS_MCP_REF               git ref for the remote registry (default: main)
    DEVSNIPS_MCP_BASE_URL          remote base URL (default: raw.githubusercontent.com/.../DevSnips)
    DEVSNIPS_MCP_LOCAL_ROOT        path to a DevSnips checkout (enables the local provider)
    DEVSNIPS_MCP_CACHE_DIR         cache directory override
    DEVSNIPS_MCP_INDEX_TTL         registry TTL seconds (default: 86400)
    DEVSNIPS_MCP_FILE_TTL          file TTL seconds (default: 604800)
    DEVSNIPS_MCP_TIMEOUT           network timeout seconds (default: 30)
    DEVSNIPS_MCP_MAX_FILE_BYTES    per-file retrieval cap (default: 524288)
    DEVSNIPS_MCP_MAX_RESPONSE_BYTES per-tool-response cap (default: 1048576)
    DEVSNIPS_MCP_MAX_CACHE_BYTES   total cache cap (default: 209715200)
    DEVSNIPS_MCP_LOG_LEVEL         logging level (default: WARNING)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .cache.paths import default_cache_dir

DEFAULT_BASE_URL = "https://raw.githubusercontent.com/sarthakbystander/DevSnips"
DEFAULT_REF = "main"
SOURCES = ("auto", "github", "local", "http")


def _env(environ: dict[str, str], name: str, default: str | None = None) -> str | None:
    value = environ.get(name)
    return value if value not in (None, "") else default


@dataclass(frozen=True)
class Settings:
    source: str = "auto"
    ref: str = DEFAULT_REF
    base_url: str = DEFAULT_BASE_URL
    local_root: Path | None = None
    cache_dir: Path = None  # type: ignore[assignment]  # set in from_env
    index_ttl_s: int = 86400
    file_ttl_s: int = 7 * 86400
    timeout_s: float = 30.0
    max_file_bytes: int = 512 * 1024
    max_response_bytes: int = 1024 * 1024
    max_files_per_response: int = 25
    max_cache_bytes: int = 200 * 1024 * 1024
    log_level: str = "WARNING"

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> Settings:
        env = dict(os.environ if environ is None else environ)
        source = (_env(env, "DEVSNIPS_MCP_SOURCE", "auto") or "auto").strip().lower()
        if source not in SOURCES:
            source = "auto"
        ref = (_env(env, "DEVSNIPS_MCP_REF", DEFAULT_REF) or DEFAULT_REF).strip()
        base_url = (_env(env, "DEVSNIPS_MCP_BASE_URL", DEFAULT_BASE_URL) or DEFAULT_BASE_URL).rstrip("/")
        local_raw = _env(env, "DEVSNIPS_MCP_LOCAL_ROOT")
        local_root = Path(local_raw).expanduser() if local_raw else None
        cache_raw = _env(env, "DEVSNIPS_MCP_CACHE_DIR")
        cache_dir = Path(cache_raw).expanduser() if cache_raw else default_cache_dir(env)
        return cls(
            source=source,
            ref=ref,
            base_url=base_url,
            local_root=local_root,
            cache_dir=cache_dir,
            index_ttl_s=_int(env, "DEVSNIPS_MCP_INDEX_TTL", 86400),
            file_ttl_s=_int(env, "DEVSNIPS_MCP_FILE_TTL", 7 * 86400),
            timeout_s=_float(env, "DEVSNIPS_MCP_TIMEOUT", 30.0),
            max_file_bytes=_int(env, "DEVSNIPS_MCP_MAX_FILE_BYTES", 512 * 1024),
            max_response_bytes=_int(env, "DEVSNIPS_MCP_MAX_RESPONSE_BYTES", 1024 * 1024),
            max_files_per_response=_int(env, "DEVSNIPS_MCP_MAX_FILES_PER_RESPONSE", 25),
            max_cache_bytes=_int(env, "DEVSNIPS_MCP_MAX_CACHE_BYTES", 200 * 1024 * 1024),
            log_level=(_env(env, "DEVSNIPS_MCP_LOG_LEVEL", "WARNING") or "WARNING").upper(),
        )


def _int(env: dict[str, str], name: str, default: int) -> int:
    raw = _env(env, name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _float(env: dict[str, str], name: str, default: float) -> float:
    raw = _env(env, name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default
