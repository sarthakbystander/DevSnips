"""Behaviour tests for scripts/tooling/validators/check_md_links.py."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from support import load_module

md_links = load_module("scripts/tooling/validators/check_md_links.py")


class CheckFileTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "target.md").write_text("hi", encoding="utf-8")
        (self.root / "sub").mkdir()
        (self.root / "sub" / "child.md").write_text("hi", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _check(self, body: str):
        doc = self.root / "doc.md"
        doc.write_text(body, encoding="utf-8")
        return md_links.check_file(doc)

    def test_resolves_sibling_and_nested(self):
        self.assertEqual(self._check("[a](target.md)\n[b](sub/child.md)"), [])

    def test_reports_missing_target_with_line_number(self):
        broken = self._check("line one\n[junk](missing.md)\n")
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0][0], 2)
        self.assertEqual(broken[0][2], "missing.md")

    def test_ignores_external_and_mailto(self):
        body = "[x](https://example.com)\n[y](mailto:a@b.c)\n"
        self.assertEqual(self._check(body), [])

    def test_ignores_query_string(self):
        self.assertEqual(self._check("[b](target.md?q=1)"), [])

    def test_percent_decodes_path(self):
        spaced = self.root / "with space.md"
        spaced.write_text("hi", encoding="utf-8")
        self.assertEqual(self._check("[a](with%20space.md)"), [])

    def test_title_suffix_is_ignored(self):
        self.assertEqual(self._check('[a](target.md "Title")'), [])

    def test_absolute_repo_path_resolves_from_root(self):
        # /scripts/... resolves against the real repo root, independent of cwd.
        self.assertEqual(self._check("[a](/scripts/tooling/tests/support.py)"), [])


class AnchorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "target.md").write_text(
            "# Hello World\n\n## Install & Use\n\n### Repeated\n\n### Repeated\n",
            encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _check(self, body: str):
        doc = self.root / "doc.md"
        doc.write_text(body, encoding="utf-8")
        return md_links.check_file(doc)

    def test_valid_heading_anchor_resolves(self):
        self.assertEqual(self._check("[a](target.md#hello-world)"), [])
        self.assertEqual(self._check("[a](target.md#install--use)"), [])

    def test_duplicate_heading_gets_numeric_suffix(self):
        self.assertEqual(self._check("[a](target.md#repeated-1)"), [])

    def test_unknown_anchor_reported(self):
        broken = self._check("[a](target.md#does-not-exist)")
        self.assertEqual(len(broken), 1)

    def test_bare_same_file_anchor_is_checked(self):
        self.assertEqual(self._check("# Doc\n\n[top](#doc)"), [])
        self.assertEqual(len(self._check("# Doc\n\n[bad](#nope)")), 1)

    def test_fragment_on_non_markdown_file_is_ignored(self):
        (self.root / "asset.txt").write_text("x", encoding="utf-8")
        self.assertEqual(self._check("[a](asset.txt#whatever)"), [])


class MarkdownFilesTests(unittest.TestCase):
    def test_skips_vendor_directories(self):
        names = [p.parts[-1] for p in md_links.markdown_files()]
        self.assertIn("AGENTS.md", names)
        self.assertFalse(any("node_modules" in p.parts for p in md_links.markdown_files()))


if __name__ == "__main__":
    unittest.main()
