"""Id / filename resolution and path-safety gate tests."""
from __future__ import annotations

import unittest

from support import make_registry

from devsnips_mcp.errors import DevSnipsError
from devsnips_mcp.files.resolver import (
    canonicalize_id,
    rel_repo_path,
    resolve_file,
    resolve_variant,
    suggest_ids,
)
from devsnips_mcp.models import parse_registry


def registry():
    return parse_registry(make_registry())


class IdGateTests(unittest.TestCase):
    def test_accepts_canonical_ids(self):
        self.assertEqual(canonicalize_id("React/Components/Buttons/solid-button"),
                         "React/Components/Buttons/solid-button")
        self.assertEqual(canonicalize_id("  Tailwind/Templates/meridian/  "),
                         "Tailwind/Templates/meridian")
        self.assertEqual(canonicalize_id("Vanilla\\Components\\Buttons\\split-button"),
                         "Vanilla/Components/Buttons/split-button")

    def test_rejects_traversal_and_junk(self):
        for bad in ("../../etc/passwd", "React/../../secret", "/absolute/path",
                    "React/Components/..%2f..", "code.tsx", "library/React/Components/x"):
            with self.subTest(bad=bad):
                with self.assertRaises(DevSnipsError) as ctx:
                    canonicalize_id(bad)
                self.assertEqual(ctx.exception.code, "path_rejected")
        with self.assertRaises(DevSnipsError) as ctx:
            canonicalize_id("")
        self.assertEqual(ctx.exception.code, "invalid_argument")

    def test_unknown_id_is_resource_not_found_with_suggestions(self):
        with self.assertRaises(DevSnipsError) as ctx:
            resolve_variant(registry(), "React/Components/Sidebar/dark-sidebars")
        self.assertEqual(ctx.exception.code, "resource_not_found")
        self.assertTrue(ctx.exception.details["suggestions"])
        self.assertIn("React/Components/Sidebar/dark-sidebar",
                      ctx.exception.details["suggestions"])

    def test_prefix_suggestions(self):
        suggestions = suggest_ids(registry(), "Tailwind/Components/Buttons")
        self.assertIn("Tailwind/Components/Buttons/basic-button/primary", suggestions)
        self.assertLessEqual(len(suggestions), 5)

    def test_resolve_variant_canonicalizes_case_and_slash(self):
        variant = resolve_variant(registry(), "vanilla/sections/hero/hero-minimal/")
        self.assertEqual(variant.id, "Vanilla/Sections/Hero/hero-minimal")


class FileGateTests(unittest.TestCase):
    def setUp(self):
        self.registry = registry()
        self.variant = self.registry.by_id["React/Templates/spray-art-school"]

    def test_manifest_files_accepted(self):
        self.assertEqual(resolve_file(self.variant, "src/App.tsx"), "src/App.tsx")

    def test_doc_files_always_allowed_when_requested(self):
        self.assertEqual(resolve_file(self.variant, "README.md"), "README.md")
        self.assertEqual(resolve_file(self.variant, "AGENTS.md"), "AGENTS.md")

    def test_case_insensitive_manifest_match(self):
        self.assertEqual(resolve_file(self.variant, "SRC/APP.TSX"), "src/App.tsx")

    def test_unknown_file_rejected_with_allowlist(self):
        with self.assertRaises(DevSnipsError) as ctx:
            resolve_file(self.variant, "secrets.env")
        self.assertEqual(ctx.exception.code, "path_rejected")
        self.assertIn("allowed_files", ctx.exception.details)

    def test_traversal_rejected(self):
        for bad in ("../package.json", "/etc/passwd", "..\\windows", "src/../../x"):
            with self.subTest(bad=bad):
                with self.assertRaises(DevSnipsError) as ctx:
                    resolve_file(self.variant, bad)
                self.assertEqual(ctx.exception.code, "path_rejected")

    def test_repo_path_mapping_includes_library_prefix(self):
        self.assertEqual(
            rel_repo_path(self.variant, "src/main.tsx"),
            "library/React/Templates/spray-art-school/src/main.tsx")


if __name__ == "__main__":
    unittest.main()
