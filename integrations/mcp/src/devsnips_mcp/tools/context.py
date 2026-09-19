"""Shared application context: settings, provider, cache, loader, engine."""

import logging
from pathlib import Path
from typing import Any, Optional

from ..cache.store import KIND_FILES, CacheStore, key_for
from ..config import Settings
from ..errors import DevSnipsError
from ..models import Registry
from ..registry import GitHubRawProvider, RegistryLoader
from ..registry.local import LocalRepoProvider
from ..registry.provider import RegistryProvider
from ..search.engine import SearchEngine

logger = logging.getLogger("devsnips_mcp")

REPO_MARKERS = ("snippets-index.json",)
LIBRARY_MARKERS = ("library/React", "library/Tailwind", "library/Vanilla")


def _discover_local_root(start: Path | None = None) -> Path | None:
    """Walk up from CWD looking for a DevSnips checkout (registry + library trees)."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in REPO_MARKERS) \
                and all((candidate / marker).is_dir() for marker in LIBRARY_MARKERS):
            return candidate
    return None


def _select_provider(settings: Settings) -> RegistryProvider:
    source = settings.source
    if source == "local":
        root = settings.local_root or _discover_local_root()
        if root is None:
            raise DevSnipsError(
                "registry_unavailable",
                "DEVSNIPS_MCP_SOURCE=local but no DevSnips checkout was found",
                {"hint": "set DEVSNIPS_MCP_LOCAL_ROOT to a DevSnips checkout root"})
        return LocalRepoProvider(root)
    if source in ("github", "http"):
        return GitHubRawProvider(settings.base_url, settings.ref, settings.timeout_s)
    # auto: prefer a real checkout when one is available (offline, complete trees)
    root = settings.local_root or _discover_local_root()
    if root is not None:
        try:
            return LocalRepoProvider(root)
        except DevSnipsError:
            pass
    return GitHubRawProvider(settings.base_url, settings.ref, settings.timeout_s)


class AppContext:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings.from_env()
        self.store = CacheStore(self.settings.cache_dir, self.settings.max_cache_bytes)
        self.provider: RegistryProvider = _select_provider(self.settings)
        self.loader = RegistryLoader(self.settings, self.provider, self.store)
        self._engine: SearchEngine | None = None
        self._engine_registry_id: str | None = None

    # ----------------------------------------------------------- registry ---
    def registry_with_provenance(self) -> tuple[Registry, dict[str, Any]]:
        return self.loader.load()

    def engine(self, registry: Registry) -> SearchEngine:
        marker = f"{self.loader.provenance().get('origin')}|{registry.last_updated}"
        if self._engine is None or self._engine_registry_id != marker:
            self._engine = SearchEngine(registry)
            self._engine_registry_id = marker
        return self._engine

    # -------------------------------------------------------------- files ---
    def read_resource_bytes(self, rel_repo_path: str,
                            max_bytes: int | None = None) -> tuple[bytes, dict[str, Any]]:
        """Fetch one file via the provider with a file cache.

        Returns (data, info) where info carries origin/etag/cached/stale/truncated.
        Truncated reads (provider-level cap) are never cached.
        """
        info = self.provider.describe()
        key = key_for(info.source, info.ref, info.origin, rel_repo_path)
        cap = max_bytes or self.settings.max_file_bytes
        cached = self.store.get_text(KIND_FILES, key)
        if cached is not None and CacheStore.is_fresh(cached[1], self.settings.file_ttl_s):
            text, meta = cached
            return text.encode("utf-8"), {
                "origin": meta.get("origin", ""), "etag": meta.get("etag"),
                "cached": True, "stale": False, "truncated": False,
            }
        try:
            payload = self.provider.read_file(rel_repo_path, max_bytes=cap)
        except DevSnipsError:
            if cached is not None:  # offline: serve the stale copy
                text, meta = cached
                return text.encode("utf-8"), {
                    "origin": meta.get("origin", ""), "etag": meta.get("etag"),
                    "cached": True, "stale": True, "truncated": False,
                }
            raise
        if payload.truncated:
            return payload.data, {"origin": payload.origin, "etag": payload.etag,
                                  "cached": False, "stale": False, "truncated": True}
        self.store.put(KIND_FILES, key, payload.data,
                       {"origin": payload.origin, "etag": payload.etag, "path": rel_repo_path})
        return payload.data, {"origin": payload.origin, "etag": payload.etag,
                              "cached": False, "stale": False, "truncated": False}

    def read_resource_text(self, rel_repo_path: str,
                           max_bytes: int | None = None) -> tuple[str, dict[str, Any]]:
        data, info = self.read_resource_bytes(rel_repo_path, max_bytes)
        try:
            text = data.decode("utf-8")
            info["encoding_lossless"] = True
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")
            info["encoding_lossless"] = False
        return text, info


_CONTEXT: Optional["AppContext"] = None


def get_context() -> AppContext:
    """Lazily build the context on first tool call (never at import time)."""
    global _CONTEXT
    if _CONTEXT is None:
        _CONTEXT = AppContext()
    return _CONTEXT


def set_context(value: AppContext | None) -> None:
    """Test seam: inject a context (e.g. with a stubbed provider); None resets."""
    global _CONTEXT
    _CONTEXT = value
