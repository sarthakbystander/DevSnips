"""Registry parsing / model contract tests."""
from __future__ import annotations

import unittest

from support import make_family, make_registry, make_variant

from devsnips_mcp import models
from devsnips_mcp.index import schema


class ParseRegistryTests(unittest.TestCase):
    def test_parses_fixture_registry(self):
        registry = models.parse_registry(make_registry())
        self.assertEqual(len(registry.families), 4)
        self.assertEqual(len(registry.by_id), 5)
        self.assertEqual(registry.schema_version, "2.0")

    def test_derives_id_and_install_from_path(self):
        registry = models.parse_registry(make_registry())
        variant = registry.by_id["Tailwind/Components/Buttons/basic-button/primary"]
        self.assertEqual(variant.id, "Tailwind/Components/Buttons/basic-button/primary")
        self.assertEqual(variant.path, "Tailwind/Components/Buttons/basic-button/primary/")
        self.assertTrue(variant.installable)
        self.assertEqual(variant.install, "npx devsnips add Tailwind/Components/Buttons/basic-button/primary")

    def test_case_insensitive_resolution(self):
        registry = models.parse_registry(make_registry())
        variant = registry.resolve("react/templates/SPRAY-ART-SCHOOL")
        self.assertIsNotNone(variant)
        self.assertEqual(variant.id, "React/Templates/spray-art-school")

    def test_missing_optional_fields_degrade(self):
        family = make_family(
            "React/Sections/CTA", "React", "section",
            [{"path": "React/Sections/CTA/bento/", "type": "section", "name": "CTA — Bento"}],
            name="CTA", category="Sections")
        registry = models.parse_registry(make_registry([family]))
        variant = registry.by_id["React/Sections/CTA/bento"]
        self.assertEqual(variant.tags, ())
        self.assertEqual(variant.styles, ())
        self.assertEqual(variant.files, ())
        self.assertFalse(variant.installable)

    def test_malformed_records_are_skipped_with_warnings(self):
        families = [
            make_family("React/Components/Bad", "React", "component", []),
            make_family("React/Components/Good", "React", "component",
                        [make_variant("React/Components/Good/ok")]),
            "not-a-family",
        ]
        families[0]["variants"] = ["not-a-variant", {"name": "no path"}]
        registry = models.parse_registry(make_registry(families))
        self.assertEqual(len(registry.families), 2)
        self.assertEqual(len(registry.by_id), 1)
        self.assertTrue(any("skipped" in warning for warning in registry.warnings))

    def test_duplicate_ids_ignored(self):
        family = make_family(
            "Vanilla/Components/Buttons", "Vanilla HTML/CSS/JS", "component",
            [make_variant("Vanilla/Components/Buttons/a"),
             make_variant("Vanilla/Components/Buttons/a")],
            name="Buttons")
        registry = models.parse_registry(make_registry([family]))
        self.assertEqual(len(registry.by_id), 1)
        self.assertTrue(any("duplicate id" in w for w in registry.warnings))

    def test_unsupported_schema_version_is_a_warning_not_an_error(self):
        data = make_registry()
        data["version"] = "3.0"
        registry = models.parse_registry(data)
        self.assertEqual(registry.schema_version, "3.0")
        self.assertTrue(any("3.0" in w for w in registry.warnings))

    def test_missing_families_raises(self):
        with self.assertRaises(ValueError):
            models.parse_registry({"version": "2.0"})


class DerivedFieldParityTests(unittest.TestCase):
    """The MCP-side predicates must equal the published index predicates."""

    def test_installability_matches_cli_filter_semantics(self):
        cases = [
            (["README.md", "code.html", "metadata.json", "preview.html"], True),
            (["metadata.json", "preview.html"], False),
            (["AGENTS.md", "metadata.json"], True),
            (["src/App.tsx"], True),
            (["assets/logo.svg"], False),
        ]
        for files, expected in cases:
            with self.subTest(files=files):
                self.assertEqual(schema.is_installable(files), expected)

    def test_derive_id_strips_trailing_slash(self):
        self.assertEqual(schema.derive_id("React/Components/Buttons/a/"),
                         "React/Components/Buttons/a")
        self.assertEqual(schema.derive_id("React/Components/Buttons/a"),
                         "React/Components/Buttons/a")

    def test_schema_gate(self):
        self.assertTrue(schema.schema_supported("2.0"))
        self.assertFalse(schema.schema_supported("1.0"))
        self.assertFalse(schema.schema_supported(None))
        self.assertFalse(schema.schema_supported(2.0))


if __name__ == "__main__":
    unittest.main()
