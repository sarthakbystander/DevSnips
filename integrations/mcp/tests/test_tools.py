"""Tool-level tests through a fake MCP registry (no SDK required).

The fake captures the decorated functions so the full tool path — context,
loader, engine, resolver, guard — is exercised without a transport. The real
SDK is exercised separately (in-process client when the SDK is installed, and
the stdio subprocess smoke test).
"""
from __future__ import annotations

import asyncio
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (import bootstrap: puts src/ on sys.path)
from support import make_synth_checkout

from devsnips_mcp.config import Settings
from devsnips_mcp.registry import RegistryLoader
from devsnips_mcp.registry.local import LocalRepoProvider
from devsnips_mcp.tools import register_all, set_context
from devsnips_mcp.tools.context import AppContext


class FakeMCP:
    def __init__(self):
        self.tools = {}

    def tool(self):
        def decorator(fn):
            self.tools[fn.__name__] = fn
            return fn
        return decorator


def call(fn, **kwargs):
    return json.loads(asyncio.run(fn(**kwargs)))


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.root = make_synth_checkout()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        cache = Path(tempfile.mkdtemp(prefix="devsnips-mcp-tools-"))
        self.addCleanup(shutil.rmtree, cache, ignore_errors=True)
        settings = Settings.from_env({"DEVSNIPS_MCP_CACHE_DIR": str(cache)})
        app = AppContext(settings)
        app.provider = LocalRepoProvider(self.root)
        app.loader = RegistryLoader(settings, app.provider, app.store)
        set_context(app)

        self.mcp = FakeMCP()
        register_all(self.mcp)
        self.tools = self.mcp.tools

    def tearDown(self):
        set_context(None)

    # ---------------------------------------------------- search_resources --
    def test_search_returns_items_and_provenance(self):
        payload = call(self.tools["search_resources"], query="dark sidebar")
        self.assertEqual(payload["mode"], "exact")
        self.assertEqual(payload["items"][0]["id"], "React/Components/Sidebar/dark-sidebar")
        self.assertEqual(payload["registry"]["source"], "local")
        self.assertIn("variant_count", payload["registry"])

    def test_search_invalid_limit_is_structured_error(self):
        payload = call(self.tools["search_resources"], query="button", limit=500)
        self.assertEqual(payload["error"]["code"], "invalid_argument")

    # --------------------------------------------------------- get_resource --
    def test_get_resource_docs_and_manifest(self):
        payload = call(self.tools["get_resource"], id="React/Templates/spray-art-school")
        self.assertEqual(payload["type"], "template")
        self.assertTrue(payload["installable"])
        self.assertIn("install", payload)
        self.assertIn("README.md", payload["docs"])
        self.assertIn("AGENTS.md", payload["docs"])
        # local provider enumerates the real tree → completeness is a real check
        self.assertFalse(payload["files_complete"])
        self.assertIn("src/components/Badge.tsx", payload["files_on_disk"])

    def test_get_resource_unknown_id_is_structured_error(self):
        payload = call(self.tools["get_resource"], id="React/Components/Nope/nope")
        self.assertEqual(payload["error"]["code"], "resource_not_found")
        self.assertTrue(payload["error"]["details"]["suggestions"])

    def test_get_resource_traversal_is_structured_error(self):
        payload = call(self.tools["get_resource"], id="../../etc/passwd")
        self.assertEqual(payload["error"]["code"], "path_rejected")

    # ---------------------------------------------------- get_resource_file --
    def test_get_resource_file_returns_content(self):
        payload = call(self.tools["get_resource_file"],
                       id="Tailwind/Components/Buttons/dark-button", file="code.html")
        self.assertIn("code.html", payload["content"])
        self.assertEqual(payload["file"], "code.html")
        self.assertIn("library/", payload["source"]["repo_path"])

    def test_get_resource_file_rejects_file_outside_manifest(self):
        payload = call(self.tools["get_resource_file"],
                       id="React/Templates/spray-art-school", file="src/components/Badge.tsx")
        self.assertEqual(payload["error"]["code"], "path_rejected")

    def test_get_resource_file_max_bytes_truncates(self):
        payload = call(self.tools["get_resource_file"],
                       id="Tailwind/Components/Buttons/dark-button",
                       file="code.html", maxBytes=5)
        self.assertTrue(payload["truncated"])
        self.assertLessEqual(payload["bytes"], 5)

    # ------------------------------------------------------------ list_facets --
    def test_list_facets_shape(self):
        payload = call(self.tools["list_facets"])
        self.assertEqual(payload["schema"]["version"], "2.0")
        techs = {t["name"]: t for t in payload["technologies"]}
        self.assertIn("React", techs)
        self.assertEqual(techs["React"]["resources"], 2)
        self.assertIn("stats", payload)

    def test_list_facets_families_scoped_by_technology(self):
        payload = call(self.tools["list_facets"], facet="families", technology="Tailwind")
        self.assertTrue(all(f["tech"] == "Tailwind CSS" for f in payload["families"]))

    def test_list_facets_invalid_facet(self):
        payload = call(self.tools["list_facets"], facet="bogus")
        self.assertEqual(payload["error"]["code"], "invalid_argument")


if __name__ == "__main__":
    unittest.main()
