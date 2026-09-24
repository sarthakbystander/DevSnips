"""Behaviour tests for scripts/tooling/indexing/rebuild_index.py.

Focus on the deterministic-ordering and leaf-detection fixes: a filesystem walk
must produce the same index regardless of `scandir` order.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from support import load_module

rebuild = load_module("scripts/tooling/indexing/rebuild_index.py")


def _make_leaf(folder: Path, *, code=True, preview=True, meta=True):
    folder.mkdir(parents=True, exist_ok=True)
    if code:
        (folder / "code.html").write_text("<html></html>", encoding="utf-8")
    if preview:
        (folder / "preview.html").write_text("<html></html>", encoding="utf-8")
    if meta:
        (folder / "metadata.json").write_text(
            json.dumps({"type": "component", "name": folder.name}),
            encoding="utf-8")


class LeafDetectionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_tailwind_leaf_requires_both_html_files(self):
        _make_leaf(self.root / "ok")
        self.assertTrue(rebuild.is_leaf(self.root / "ok", rebuild.TAILWIND))
        _make_leaf(self.root / "partial", preview=False)
        self.assertFalse(rebuild.is_leaf(self.root / "partial", rebuild.TAILWIND))

    def test_folder_with_child_metadata_is_not_a_leaf(self):
        parent = self.root / "group"
        _make_leaf(parent / "child")
        (parent / "metadata.json").write_text("{}", encoding="utf-8")
        self.assertFalse(rebuild.is_leaf(parent, rebuild.TAILWIND))

    def test_react_leaf_accepts_preview_only(self):
        _make_leaf(self.root / "tpl", code=False, preview=True)
        self.assertTrue(rebuild.is_leaf(self.root / "tpl", rebuild.REACT))

    def test_react_leaf_rejects_neither_source_file(self):
        _make_leaf(self.root / "empty", code=False, preview=False)
        self.assertFalse(rebuild.is_leaf(self.root / "empty", rebuild.REACT))


class OrderingTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_list_leaves_under_is_sorted_by_path(self):
        # Two families that share a variant folder name under different parents
        # are exactly the tie-break case the fix addresses.
        _make_leaf(self.root / "Buttons" / "icon-button" / "basic")
        _make_leaf(self.root / "Buttons" / "animated-button" / "basic")
        _make_leaf(self.root / "Buttons" / "3d-button" / "basic")
        leaves = list(rebuild.list_leaves_under(self.root / "Buttons", rebuild.TAILWIND))
        rels = [rel.as_posix() for rel, _ in leaves]
        self.assertEqual(rels, sorted(rels))

    def test_walk_order_does_not_change_result(self):
        _make_leaf(self.root / "b")
        _make_leaf(self.root / "a")
        _make_leaf(self.root / "c")
        first = [p.as_posix() for p, _ in
                 rebuild.list_leaves_under(self.root, rebuild.TAILWIND)]
        second = [p.as_posix() for p, _ in
                  rebuild.list_leaves_under(self.root, rebuild.TAILWIND)]
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(first))


class RelPathTests(unittest.TestCase):
    def test_strips_library_prefix_only(self):
        p = rebuild.ROOT / "library" / "Tailwind" / "Components"
        self.assertEqual(rebuild.rel_path(p), "Tailwind/Components")

    def test_non_library_path_is_unchanged(self):
        p = rebuild.ROOT / "scripts"
        self.assertEqual(rebuild.rel_path(p), "scripts")


if __name__ == "__main__":
    unittest.main()
