"""Parity test: MCP-derived ids/installs must equal the specialized indexes.

The specialized indexes (agents/resources/indexes/*.json) are generated from the
same in-memory family set as the master registry and cross-validated by
scripts/tooling/indexing/validate_indexes.py. If MCP's derived fields ever drift
from the CLI/index contract, this test fails before any user sees it.
"""
from __future__ import annotations

import json
import unittest

from support import (
    COMPONENTS_INDEX,
    MASTER_INDEX,
    SECTIONS_INDEX,
    TEMPLATES_INDEX,
    require_repo_index,
)

from devsnips_mcp import models
from devsnips_mcp.index import schema


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class SpecializedIndexParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        require_repo_index(cls)
        cls.master = load(MASTER_INDEX)
        cls.registry = models.parse_registry(cls.master)
        cls.specialized = {
            "component": load(COMPONENTS_INDEX),
            "section": load(SECTIONS_INDEX),
            "template": load(TEMPLATES_INDEX),
        }

    def test_id_and_install_match_for_every_variant(self):
        total = 0
        mismatched = []
        for index_payload in self.specialized.values():
            for family in index_payload["families"]:
                for entry in family["variants"]:
                    total += 1
                    variant = self.registry.by_id.get(entry["id"])
                    if variant is None:
                        mismatched.append(f"{entry['id']} missing from parsed master")
                        continue
                    if variant.id != entry["id"]:
                        mismatched.append(f"id drift: {variant.id} != {entry['id']}")
                    if variant.type != entry["type"]:
                        mismatched.append(f"type drift: {entry['id']}")
                    expected_install = entry.get("install")
                    actual_install = variant.install or None
                    if actual_install != expected_install:
                        mismatched.append(
                            f"install drift: {entry['id']}: "
                            f"{actual_install!r} != {expected_install!r}")
        self.assertEqual(mismatched, [])
        self.assertGreater(total, 900)  # live collection is 1000+; guard the scale
        self.assertEqual(total, len(self.registry.by_id))

    def test_type_partition_across_indexes(self):
        seen = {}
        for type_, index_payload in self.specialized.items():
            for family in index_payload["families"]:
                for entry in family["variants"]:
                    self.assertNotIn(entry["id"], seen)
                    seen[entry["id"]] = type_
        self.assertEqual(set(seen.values()), {"component", "section", "template"})

    def test_every_registry_variant_is_in_exactly_one_index(self):
        indexed = set()
        for index_payload in self.specialized.values():
            for family in index_payload["families"]:
                for entry in family["variants"]:
                    indexed.add(entry["id"])
        self.assertEqual(set(self.registry.by_id), indexed)

    def test_master_stats_agree_with_parsed_registry(self):
        stats = self.master["stats"]
        self.assertEqual(stats["totalVariants"], len(self.registry.by_id))
        self.assertEqual(stats["totalFamilies"], len(self.registry.families))

    def test_installability_predicate_matches_index_and_cli_contract(self):
        # spot-check the mirrored predicate against the specialized index entries
        components = self.specialized["component"]
        entry = components["families"][0]["variants"][0]
        variant = self.registry.by_id[entry["id"]]
        self.assertEqual(variant.installable, "install" in entry)
        self.assertEqual(schema.is_installable(variant.files), variant.installable)


if __name__ == "__main__":
    unittest.main()
