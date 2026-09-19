"""RegistryLoader tests: cache-first, ETag refresh, stale-on-failure, corruption."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from support import make_registry, make_synth_checkout

from devsnips_mcp.cache.store import KIND_REGISTRY, CacheStore, key_for
from devsnips_mcp.config import Settings
from devsnips_mcp.errors import DevSnipsError
from devsnips_mcp.registry import RegistryLoader
from devsnips_mcp.registry.provider import ProviderInfo

REGISTRY_JSON = json.dumps(make_registry()).encode("utf-8")


class StubProvider:
    """Scriptable provider for loader tests."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.etag_requests = []
        self.info = ProviderInfo(source="github", ref="main", origin="stub://main",
                                 can_list_files=False)

    def describe(self):
        return self.info

    def load_registry(self, etag=None):
        self.etag_requests.append(etag)
        outcome = self.responses.pop(0)
        if isinstance(outcome, DevSnipsError):
            raise outcome
        return outcome

    def read_file(self, rel_path, max_bytes=None):  # pragma: no cover
        raise NotImplementedError

    def list_files(self, rel_dir):  # pragma: no cover
        return None


class RegistryLoaderTests(unittest.TestCase):
    def setUp(self):
        self.cache_root = Path(tempfile.mkdtemp(prefix="devsnips-mcp-loader-"))
        self.addCleanup(shutil.rmtree, self.cache_root, ignore_errors=True)
        self.store = CacheStore(self.cache_root, max_bytes=8 * 1024 * 1024)
        self.settings = Settings.from_env({
            "DEVSNIPS_MCP_CACHE_DIR": str(self.cache_root),
            "DEVSNIPS_MCP_INDEX_TTL": "60",
        })

    def loader(self, provider):
        return RegistryLoader(self.settings, provider, self.store)

    def test_first_load_fetches_and_caches(self):
        provider = StubProvider([
            type("P", (), {"data": REGISTRY_JSON, "etag": '"e1"',
                           "not_modified": False, "origin": "stub://main"})(),
        ])
        registry, provenance = self.loader(provider).load()
        self.assertEqual(len(registry.by_id), 5)
        self.assertFalse(provenance["stale"])
        self.assertIsNotNone(provenance["fetched_at"])
        # second load comes from cache: no further provider calls
        registry2, provenance2 = self.loader(StubProvider([])).load()
        self.assertEqual(len(registry2.by_id), 5)
        self.assertFalse(provenance2["stale"])

    def test_stale_cache_triggers_conditional_refresh(self):
        loader = self.loader(StubProvider([
            type("P", (), {"data": REGISTRY_JSON, "etag": '"e1"',
                           "not_modified": False, "origin": "stub://main"})(),
        ]))
        _reg, _ = loader.load()
        # age the cache beyond TTL
        key = key_for("github", "main", "stub://main")
        _data, meta = self.store.get(KIND_REGISTRY, key)
        self.store.put(KIND_REGISTRY, key, REGISTRY_JSON,
                       {**meta, "fetched_at": 0})
        provider = StubProvider([
            type("P", (), {"data": None, "etag": '"e1"',
                           "not_modified": True, "origin": "stub://main"})(),
        ])
        _reg2, provenance2 = self.loader(provider).load()
        self.assertFalse(provenance2["stale"])
        self.assertEqual(provider.etag_requests, ['"e1"'])

    def test_refresh_failure_serves_stale_cache(self):
        loader = self.loader(StubProvider([
            type("P", (), {"data": REGISTRY_JSON, "etag": '"e1"',
                           "not_modified": False, "origin": "stub://main"})(),
        ]))
        loader.load()
        key = key_for("github", "main", "stub://main")
        _data, meta = self.store.get(KIND_REGISTRY, key)
        self.store.put(KIND_REGISTRY, key, REGISTRY_JSON, {**meta, "fetched_at": 0})
        provider = StubProvider([DevSnipsError("registry_unavailable", "down", {})])
        _registry, provenance = self.loader(provider).load()
        self.assertTrue(provenance["stale"])
        self.assertIn("refresh_error", provenance)

    def test_no_cache_and_network_failure_raises_unavailable(self):
        provider = StubProvider([DevSnipsError("registry_unavailable", "down", {})])
        with self.assertRaises(DevSnipsError) as ctx:
            self.loader(provider).load()
        self.assertEqual(ctx.exception.code, "registry_unavailable")

    def test_corrupt_cache_is_deleted_and_refetched(self):
        key = key_for("github", "main", "stub://main")
        self.store.put(KIND_REGISTRY, key, b"{corrupt json")
        provider = StubProvider([
            type("P", (), {"data": REGISTRY_JSON, "etag": '"e1"',
                           "not_modified": False, "origin": "stub://main"})(),
        ])
        registry, _ = self.loader(provider).load()
        self.assertEqual(len(registry.by_id), 5)

    def test_loader_against_real_local_checkout(self):
        root = make_synth_checkout()
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        from devsnips_mcp.registry.local import LocalRepoProvider
        loader = RegistryLoader(self.settings, LocalRepoProvider(root), self.store)
        registry, provenance = loader.load()
        self.assertEqual(provenance["source"], "local")
        self.assertEqual(len(registry.by_id), 5)
        self.assertFalse(provenance["stale"])


if __name__ == "__main__":
    unittest.main()
