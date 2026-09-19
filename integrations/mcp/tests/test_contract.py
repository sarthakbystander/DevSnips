"""Contract tests: MCP behavior must survive registry schema evolution.

Fixtures cover: future schema versions, unknown technologies/types, renamed/
missing fields, empty registries, and oversized string values. Every tool call
must return a structured response — never raise.
"""
from __future__ import annotations

import asyncio
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401  (import bootstrap: puts src/ on sys.path)
from support import make_family, make_registry, make_variant

from devsnips_mcp.config import Settings
from devsnips_mcp.models import parse_registry
from devsnips_mcp.registry import RegistryLoader
from devsnips_mcp.tools import register_all, set_context
from devsnips_mcp.tools.context import AppContext


class StubProvider:
    def __init__(self, registry_data):
        self._data = registry_data
        self.origin = "stub://contract"

    def describe(self):
        from devsnips_mcp.registry.provider import ProviderInfo
        return ProviderInfo(source="github", ref="main", origin=self.origin,
                            can_list_files=False)

    def load_registry(self, etag=None):
        from devsnips_mcp.registry.provider import RegistryPayload
        return RegistryPayload(data=json.dumps(self._data).encode("utf-8"),
                               etag='"c1"', origin=self.origin)

    def read_file(self, rel_path, max_bytes=None):
        from devsnips_mcp.errors import FILE_NOT_FOUND, DevSnipsError
        raise DevSnipsError(FILE_NOT_FOUND, "no files in contract stub", {"path": rel_path})

    def list_files(self, rel_dir):
        return None


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


class ContractTests(unittest.TestCase):
    def _prepare(self, registry_data):
        cache = Path(tempfile.mkdtemp(prefix="devsnips-mcp-contract-"))
        self.addCleanup(shutil.rmtree, cache, ignore_errors=True)
        settings = Settings.from_env({"DEVSNIPS_MCP_CACHE_DIR": str(cache)})
        app = AppContext(settings)
        app.provider = StubProvider(registry_data)
        app.loader = RegistryLoader(settings, app.provider, app.store)
        set_context(app)
        fake = FakeMCP()
        register_all(fake)
        self.addCleanup(set_context, None)
        return fake.tools

    def test_future_schema_version_degrades_gracefully(self):
        data = make_registry()
        data["version"] = "9.9"
        tools = self._prepare(data)
        payload = call(tools["list_facets"])
        self.assertEqual(payload["schema"]["version"], "9.9")
        self.assertFalse(payload["schema"]["supported"])
        result = call(tools["search_resources"], query="dark sidebar")
        self.assertEqual(result["items"][0]["id"], "React/Components/Sidebar/dark-sidebar")
        self.assertTrue(result["registry"]["warnings"])

    def test_unknown_technology_and_type_are_served(self):
        data = make_registry([make_family(
            "Svelte/Layouts/Headers", "Svelte", "layout",
            [make_variant("Svelte/Layouts/Headers/basic", name="Basic Header",
                          type_="layout")],
            name="Headers", category="Layouts")])
        tools = self._prepare(data)
        result = call(tools["search_resources"], technology="Svelte", limit=50)
        self.assertEqual(result["items"][0]["id"], "Svelte/Layouts/Headers/basic")
        facets = call(tools["list_facets"])
        types = {t["type"] for t in facets["types"]}
        self.assertIn("layout", types)

    def test_renamed_and_missing_fields_do_not_break_tools(self):
        data = make_registry([make_family(
            "React/Components/Weird", "React", "component",
            [{"path": "React/Components/Weird/x/", "type": "component",
              "name": "X", "someNewField": {"nested": True}, "tags": "not-a-list"}],
            name="Weird")])
        tools = self._prepare(data)
        result = call(tools["search_resources"], query="X component")
        self.assertEqual(result["items"][0]["id"], "React/Components/Weird/x")
        detail = call(tools["get_resource"], id="React/Components/Weird/x")
        self.assertEqual(detail["tags"], [])

    def test_empty_families_registry(self):
        data = make_registry([])
        data["families"] = []
        tools = self._prepare(data)
        result = call(tools["search_resources"], query="button")
        self.assertEqual(result["items"], [])
        self.assertEqual(result["total_matches"], 0)

    def test_oversized_strings_are_returned_not_crash(self):
        data = make_registry([make_family(
            "React/Components/Huge", "React", "component",
            [make_variant("React/Components/Huge/blob", name="B" * 100000,
                          description="D" * 200000)],
            name="Huge")])
        tools = self._prepare(data)
        result = call(tools["search_resources"], query="B component", limit=1)
        self.assertEqual(result["items"][0]["id"], "React/Components/Huge/blob")

    def test_many_families_survive(self):
        families = [make_family(f"React/Components/F{i}", "React", "component",
                                [make_variant(f"React/Components/F{i}/a")],
                                name=f"F{i}")
                    for i in range(50)]
        tools = self._prepare(make_registry(families))
        facets = call(tools["list_facets"], facet="types")
        self.assertTrue(any(t["type"] == "component" and t["count"] == 50
                            for t in facets["types"]))

    def test_parser_rejects_non_object_and_missing_families(self):
        with self.assertRaises(ValueError):
            parse_registry(["not", "an", "object"])
        with self.assertRaises(ValueError):
            parse_registry({"version": "2.0"})


if __name__ == "__main__":
    unittest.main()
