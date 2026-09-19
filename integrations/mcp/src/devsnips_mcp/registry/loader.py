"""Registry loading: cache-first, lazy refresh, degraded-mode friendly.

Load order (never blocks MCP initialize — tools build the registry lazily):
1. Fresh cache           → serve immediately (no network).
2. Stale cache           → serve it, try one conditional refresh (ETag / 304).
3. No cache              → fetch synchronously on first use; failure raises
                           REGISTRY_UNAVAILABLE with an actionable hint.
Parse failures delete the corrupt cache entry and raise REGISTRY_INVALID.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from typing import Any

from ..cache.store import KIND_REGISTRY, CacheStore, key_for
from ..config import Settings
from ..errors import REGISTRY_INVALID, REGISTRY_UNAVAILABLE, DevSnipsError
from ..models import Registry, parse_registry
from .provider import RegistryProvider


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RegistryLoader:
    def __init__(self, settings: Settings, provider: RegistryProvider, store: CacheStore):
        self.settings = settings
        self.provider = provider
        self.store = store
        self._registry: Registry | None = None
        self._provenance: dict[str, Any] | None = None

    # ------------------------------------------------------------- public ---
    def load(self) -> tuple[Registry, dict[str, Any]]:
        if self._registry is not None and self._provenance is not None:
            return self._registry, self._provenance
        key = self._cache_key()
        info = self.provider.describe()

        cached = self.store.get(KIND_REGISTRY, key)
        if cached is not None:
            data, meta = cached
            try:
                registry = self._parse(data, origin=str(meta.get("origin", info.origin)))
            except DevSnipsError:
                # _parse already deleted the corrupt entry; fall through to a
                # fresh fetch from the origin.
                registry = None
            if registry is not None:
                fresh = self.store.is_fresh(meta, self.settings.index_ttl_s)
                if fresh:
                    provenance = self._provenance_for(registry, info, meta, stale=False)
                    self._remember(registry, provenance)
                    return registry, provenance
                # Stale: serve it, attempt one conditional refresh.
                etag = meta.get("etag") if isinstance(meta.get("etag"), str) else None
                try:
                    payload = self.provider.load_registry(etag=etag)
                except DevSnipsError as exc:
                    provenance = self._provenance_for(registry, info, meta, stale=True)
                    provenance["refresh_error"] = {"code": exc.code, "message": exc.message}
                    self._remember(registry, provenance)
                    return registry, provenance
                if payload.not_modified:
                    self.store.touch(KIND_REGISTRY, key)
                    fresh_meta = dict(meta)
                    fresh_meta["fetched_at"] = time.time()
                    provenance = self._provenance_for(registry, info, fresh_meta, stale=False)
                    self._remember(registry, provenance)
                    return registry, provenance
                return self._store_and_parse(payload)

        # No cache: fetch synchronously.
        payload = self.provider.load_registry()
        if payload.data is None:  # defensive: 304 without a cache entry
            raise DevSnipsError(REGISTRY_UNAVAILABLE,
                                "registry origin returned 304 without a cached copy",
                                {"origin": payload.origin})
        return self._store_and_parse(payload)

    def provenance(self) -> dict[str, Any]:
        if self._provenance is None:
            self.load()
        assert self._provenance is not None
        return dict(self._provenance)

    # ------------------------------------------------------------ private ---
    def _cache_key(self) -> str:
        info = self.provider.describe()
        return key_for(info.source, info.ref, info.origin)

    def _store_and_parse(self, payload) -> tuple[Registry, dict[str, Any]]:
        key = self._cache_key()
        info = self.provider.describe()
        meta = {"origin": payload.origin, "ref": info.ref, "etag": payload.etag,
                "fetched_at": time.time()}
        data = payload.data or b""
        registry = self._parse(data, origin=payload.origin)  # may raise REGISTRY_INVALID
        self.store.put(KIND_REGISTRY, key, data, meta)
        provenance = self._provenance_for(registry, info, meta, stale=False)
        self._remember(registry, provenance)
        return registry, provenance

    def _parse(self, data: bytes, origin: str) -> Registry:
        try:
            return parse_registry(json.loads(data.decode("utf-8")))
        except (UnicodeDecodeError, ValueError) as exc:
            # Corrupt cache → delete so the next attempt refetches from origin.
            self.store.delete(KIND_REGISTRY, self._cache_key())
            raise DevSnipsError(REGISTRY_INVALID, f"registry is not valid JSON: {exc}",
                                {"origin": origin, "bytes": len(data)}) from exc

    def _provenance_for(self, registry: Registry, info, meta: dict[str, Any], stale: bool) -> dict[str, Any]:
        fetched_at = meta.get("fetched_at")
        fetched_iso = (_utcnow_iso() if not isinstance(fetched_at, (int, float))
                       else datetime.fromtimestamp(float(fetched_at), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        return {
            "source": info.source,
            "ref": info.ref,
            "origin": str(meta.get("origin", info.origin)),
            "schema_version": registry.schema_version,
            "last_updated": registry.last_updated,
            "fetched_at": fetched_iso,
            "stale": stale,
            "variant_count": len(registry.by_id),
            "warnings": list(registry.warnings),
        }

    def _remember(self, registry: Registry, provenance: dict[str, Any]) -> None:
        self._registry = registry
        self._provenance = provenance
