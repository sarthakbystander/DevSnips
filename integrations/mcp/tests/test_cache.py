"""CacheStore tests: TTL, atomicity, LRU eviction, corruption recovery."""
from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path

import support  # noqa: F401  (import bootstrap: puts src/ on sys.path)

from devsnips_mcp.cache.store import KIND_FILES, CacheStore, content_hash, key_for


class CacheStoreTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="devsnips-mcp-cache-"))
        self.store = CacheStore(self.root, max_bytes=4096)

    def test_put_get_roundtrip(self):
        key = key_for("test", "entry")
        self.store.put(KIND_FILES, key, b"hello", {"origin": "origin-a"})
        data, meta = self.store.get(KIND_FILES, key)
        self.assertEqual(data, b"hello")
        self.assertEqual(meta["origin"], "origin-a")
        self.assertEqual(meta["sha256"], content_hash(b"hello"))

    def test_missing_entry_is_none(self):
        self.assertIsNone(self.store.get(KIND_FILES, key_for("nope")))

    def test_freshness_and_touch(self):
        key = key_for("test", "fresh")
        self.store.put(KIND_FILES, key, b"x")
        self.assertTrue(self.store.is_fresh(self.store.get(KIND_FILES, key)[1], ttl_s=60))
        # simulate age
        _data, meta = self.store.get(KIND_FILES, key)
        meta["fetched_at"] -= 120
        self.store.put(KIND_FILES, key, b"x", {"fetched_at": meta["fetched_at"]})
        self.assertFalse(self.store.is_fresh(self.store.get(KIND_FILES, key)[1], ttl_s=60))
        self.store.touch(KIND_FILES, key)
        self.assertTrue(self.store.is_fresh(self.store.get(KIND_FILES, key)[1], ttl_s=60))

    def test_corrupt_entries_are_removed(self):
        key = key_for("test", "corrupt")
        data_path, meta_path = self.store.paths(KIND_FILES, key)
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data_path.write_bytes(b"\xff\xfe\xfa")
        meta_path.write_text("not-json", encoding="utf-8")
        self.assertIsNone(self.store.get(KIND_FILES, key))
        self.assertFalse(data_path.exists())
        self.assertFalse(meta_path.exists())

    def test_atomic_writes_leave_no_temp_files(self):
        key = key_for("test", "atomic")
        self.store.put(KIND_FILES, key, b"payload")
        leftovers = list((self.root / KIND_FILES).glob("*.tmp*"))
        self.assertEqual(leftovers, [])

    def test_lru_eviction_under_cap(self):
        blob = b"z" * 3000  # cap is 4096 → only one large entry fits
        first = key_for("test", "old")
        second = key_for("test", "new")
        self.store.put(KIND_FILES, first, blob, {"fetched_at": time.time() - 500})
        self.store.put(KIND_FILES, second, blob, {"fetched_at": time.time()})
        self.assertIsNone(self.store.get(KIND_FILES, first))
        self.assertIsNotNone(self.store.get(KIND_FILES, second))

    def test_registry_entries_are_not_evicted(self):
        from devsnips_mcp.cache.store import KIND_REGISTRY
        blob = b"z" * 2000
        reg_key = key_for("github", "main")
        old_key = key_for("test", "old-file")
        self.store.put(KIND_REGISTRY, reg_key, blob)
        self.store.put(KIND_FILES, old_key, blob, {"fetched_at": time.time() - 500})
        self.store.put(KIND_FILES, key_for("test", "new-file"), blob)
        self.assertIsNotNone(self.store.get(KIND_REGISTRY, reg_key))

    def test_content_hash_is_newline_insensitive(self):
        self.assertEqual(content_hash(b"a\r\nb"), content_hash(b"a\nb"))

    def test_clear(self):
        key = key_for("test", "clear")
        self.store.put(KIND_FILES, key, b"x")
        self.store.clear()
        self.assertIsNone(self.store.get(KIND_FILES, key))


if __name__ == "__main__":
    unittest.main()
