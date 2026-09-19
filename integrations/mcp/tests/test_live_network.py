"""Live network tests — opt-in via DEVSNIPS_MCP_NETWORK_TESTS=1.

Hits the real registry on GitHub main (the same endpoint the DevSnips CLI
resolves against) and fetches a known source file plus a template page that is
verified present in the manifest.
"""
from __future__ import annotations

import json
import os
import unittest

from support import MASTER_INDEX, require_repo_index

from devsnips_mcp.config import Settings
from devsnips_mcp.registry import GitHubRawProvider
from devsnips_mcp.registry.provider import library_rel_path

BASE_URL = "https://raw.githubusercontent.com/sarthakbystander/DevSnips"


@unittest.skipUnless(os.environ.get("DEVSNIPS_MCP_NETWORK_TESTS") == "1",
                     "set DEVSNIPS_MCP_NETWORK_TESTS=1 to run live network tests")
class LiveNetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile

        cls.cache = tempfile.mkdtemp(prefix="devsnips-mcp-live-")
        cls.settings = Settings.from_env({
            "DEVSNIPS_MCP_CACHE_DIR": cls.cache,
            "DEVSNIPS_MCP_SOURCE": "github",
            "DEVSNIPS_MCP_TIMEOUT": "30",
        })
        cls.provider = GitHubRawProvider(BASE_URL, "main", cls.settings.timeout_s)

    def test_registry_fetches_and_parses(self):
        from devsnips_mcp.models import parse_registry
        payload = self.provider.load_registry()
        registry = parse_registry(json.loads(payload.data.decode("utf-8")))
        self.assertGreater(len(registry.by_id), 900)
        self.assertEqual(registry.schema_version, "2.0")

    def test_known_source_file_fetches(self):
        payload = self.provider.read_file(
            "library/React/Components/Accordion/accordion/code.tsx")
        self.assertEqual(payload.truncated, False)
        self.assertGreater(len(payload.data), 0)
        # Real .tsx files may not contain the literal "code" (imports from react,
        # JSX, etc.) — assert only that the payload is fetchable UTF-8 source.
        payload.data.decode("utf-8")  # must not raise

    def test_template_page_from_manifest_fetches(self):
        require_repo_index(self)
        master = json.loads(MASTER_INDEX.read_text(encoding="utf-8"))
        for family in master["families"]:
            if family["path"].rstrip("/") == "Tailwind/Templates/ai-saas-platform":
                files = family["variants"][0]["files"]
                self.assertIn("pages/pricing.html", files)
                payload = self.provider.read_file(
                    library_rel_path(family["variants"][0]["path"], "pages/pricing.html"))
                self.assertGreater(len(payload.data), 0)
                return
        self.fail("ai-saas-platform not found in the registry")


if __name__ == "__main__":
    unittest.main()
