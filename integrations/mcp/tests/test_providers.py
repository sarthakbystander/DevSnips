"""Provider tests: GitHubRawProvider with a stubbed fetcher + LocalRepoProvider."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from support import make_registry, make_synth_checkout

from devsnips_mcp.errors import DevSnipsError
from devsnips_mcp.registry import GitHubRawProvider
from devsnips_mcp.registry.local import LocalRepoProvider

BASE = "https://raw.githubusercontent.com/sarthakbystander/DevSnips"
REGISTRY_JSON = json.dumps(make_registry()).encode("utf-8")


class GitHubRegistryTests(unittest.TestCase):
    def provider(self, fetcher):
        return GitHubRawProvider(BASE, "main", timeout_s=5, fetcher=fetcher)

    def test_registry_url_shape(self):
        seen = {}

        def fetch(url, headers, timeout, max_bytes):
            seen["url"] = url
            seen["headers"] = headers
            return 200, REGISTRY_JSON, None, "text/plain"

        payload = self.provider(fetch).load_registry()
        self.assertEqual(seen["url"], f"{BASE}/main/snippets-index.json")
        self.assertIn(b"families", payload.data)

    def test_conditional_get_sends_etag(self):
        seen = {}

        def fetch(url, headers, timeout, max_bytes):
            seen["headers"] = headers
            return 304, None, None, None

        payload = self.provider(fetch).load_registry(etag='"etag-1"')
        self.assertTrue(payload.not_modified)
        self.assertEqual(seen["headers"].get("If-None-Match"), '"etag-1"')

    def test_error_status_maps_to_registry_unavailable(self):
        def fetch(url, headers, timeout, max_bytes):
            return 500, None, None, None

        with self.assertRaises(DevSnipsError) as ctx:
            self.provider(fetch).load_registry()
        self.assertEqual(ctx.exception.code, "registry_unavailable")

    def test_html_response_is_rejected(self):
        def fetch(url, headers, timeout, max_bytes):
            return 200, b"<html>not json</html>", None, "text/html"

        with self.assertRaises(DevSnipsError) as ctx:
            self.provider(fetch).load_registry()
        self.assertEqual(ctx.exception.code, "registry_invalid")

    def test_empty_response_is_rejected(self):
        def fetch(url, headers, timeout, max_bytes):
            return 200, b"   ", None, "text/plain"

        with self.assertRaises(DevSnipsError) as ctx:
            self.provider(fetch).load_registry()
        self.assertEqual(ctx.exception.code, "registry_invalid")

    def test_network_error_maps_to_unavailable(self):
        def fetch(url, headers, timeout, max_bytes):
            raise TimeoutError("timed out")

        with self.assertRaises(DevSnipsError) as ctx:
            self.provider(fetch).load_registry()
        self.assertEqual(ctx.exception.code, "registry_unavailable")


class GitHubFileTests(unittest.TestCase):
    def _fetch(self, body=b"code", ctype="text/plain", status=200):
        seen = {}

        def fetch(url, headers, timeout, max_bytes):
            seen["url"] = url
            if status == 200:
                data = body[:max_bytes] + b"!" if max_bytes and len(body) > max_bytes else body
                return status, data, None, ctype
            return status, None, None, None

        return GitHubRawProvider(BASE, "main", timeout_s=5, fetcher=fetch), seen

    def test_file_url_shape(self):
        provider, seen = self._fetch()
        payload = provider.read_file("library/React/Components/Accordion/accordion/code.tsx")
        self.assertEqual(seen["url"],
                         f"{BASE}/main/library/React/Components/Accordion/accordion/code.tsx")
        self.assertEqual(payload.data, b"code")

    def test_404_maps_to_file_not_found(self):
        provider, _seen = self._fetch(status=404)
        with self.assertRaises(DevSnipsError) as ctx:
            provider.read_file("library/React/Components/Ghost/file.tsx")
        self.assertEqual(ctx.exception.code, "file_not_found")

    def test_html_file_response_rejected(self):
        provider, _seen = self._fetch(body=b"<html></html>", ctype="text/html")
        with self.assertRaises(DevSnipsError) as ctx:
            provider.read_file("library/React/Components/Ghost/file.tsx")
        self.assertEqual(ctx.exception.code, "file_not_found")

    def test_truncation_flag(self):
        provider, _seen = self._fetch(body=b"abcdef")
        payload = provider.read_file("library/x/y.txt", max_bytes=3)
        self.assertTrue(payload.truncated)
        self.assertEqual(payload.data, b"abc")

    def test_unsafe_rel_path_rejected(self):
        provider, _seen = self._fetch()
        for bad in ("../../etc/passwd", "/abs", ""):
            with self.subTest(bad=bad), self.assertRaises(DevSnipsError):
                provider.read_file(bad)

    def test_cannot_list_files(self):
        provider, _seen = self._fetch()
        self.assertIsNone(provider.list_files("library/React/Components/Buttons"))


class LocalProviderTests(unittest.TestCase):
    def setUp(self):
        self.root = make_synth_checkout()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.provider = LocalRepoProvider(self.root)

    def test_describe(self):
        info = self.provider.describe()
        self.assertEqual(info.source, "local")
        self.assertTrue(info.can_list_files)

    def test_reads_registry(self):
        payload = self.provider.load_registry()
        data = json.loads(payload.data.decode("utf-8"))
        self.assertEqual(data["version"], "2.0")

    def test_reads_library_file(self):
        payload = self.provider.read_file(
            "library/Tailwind/Components/Buttons/dark-button/code.html")
        self.assertIn(b"code.html", payload.data)

    def test_missing_file_is_file_not_found(self):
        with self.assertRaises(DevSnipsError) as ctx:
            self.provider.read_file("library/React/Components/Sidebar/dark-sidebar/ghost.tsx")
        self.assertEqual(ctx.exception.code, "file_not_found")

    def test_lists_full_tree_including_unmanifested_files(self):
        listing = self.provider.list_files("library/React/Templates/spray-art-school")
        self.assertIsNotNone(listing)
        self.assertIn("src/components/Badge.tsx", listing)
        self.assertIn("src/App.tsx", listing)

    def test_containment_rejects_traversal(self):
        self.assertIsNone(self.provider._contained("library/../../outside.txt"))

    def test_rejects_non_checkout_root(self):
        empty = Path(tempfile.mkdtemp(prefix="devsnips-mcp-empty-"))
        self.addCleanup(shutil.rmtree, empty, ignore_errors=True)
        with self.assertRaises(DevSnipsError):
            LocalRepoProvider(empty)


if __name__ == "__main__":
    unittest.main()
