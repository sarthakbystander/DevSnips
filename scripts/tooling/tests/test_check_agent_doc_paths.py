"""Behaviour tests for scripts/tooling/validators/check_agent_doc_paths.py."""
from __future__ import annotations

import unittest

from support import load_module

paths = load_module("scripts/tooling/validators/check_agent_doc_paths.py")


class IsCheckableTests(unittest.TestCase):
    def test_anchored_repo_paths_are_checked(self):
        for token in ("scripts/tooling/validators/validate.py",
                      "agents/resources/qa.md", "docs/", ".github/workflows/"):
            self.assertTrue(paths.is_checkable(token), token)

    def test_prose_and_globs_are_ignored(self):
        for token in ("HTML/CSS/JS", "pages/index.html", "./src/app.tsx",
                      "../sibling.md", "src/**/*.js", "https://example.com",
                      "library/{Tech}/{Type}/", "some file.txt"):
            self.assertFalse(paths.is_checkable(token), token)

    def test_declared_non_paths_are_ignored(self):
        for token in ("devsnips/", "website/", "feat/your-component"):
            self.assertFalse(paths.is_checkable(token), token)


class ElisionTests(unittest.TestCase):
    def test_strip_fences_blanks_fenced_regions_only(self):
        text = "before\n```\n`scripts/nope.py`\n```\nafter `docs/ok.md`"
        stripped = paths.strip_fences(text)
        self.assertNotIn("scripts/nope.py", stripped)
        self.assertIn("docs/ok.md", stripped)
        # Line count preserved so reported line numbers stay accurate.
        self.assertEqual(len(stripped.splitlines()), len(text.splitlines()))

    def test_tilde_fences_are_handled(self):
        text = "~~~\n`scripts/nope.py`\n~~~"
        self.assertNotIn("scripts/nope.py", paths.strip_fences(text))

    def test_strip_ignored_blanks_marked_regions(self):
        text = ("a\n" + paths.IGNORE_START + "\n`scripts/gone.py`\n"
                + paths.IGNORE_END + "\n`docs/ok.md`")
        stripped = paths.strip_ignored(text)
        self.assertNotIn("scripts/gone.py", stripped)
        self.assertIn("docs/ok.md", stripped)

    def test_prepare_applies_both_elisions(self):
        text = ("```\n`scripts/a.py`\n```\n"
                + paths.IGNORE_START + "\n`scripts/b.py`\n" + paths.IGNORE_END)
        prepared = paths.prepare(text)
        self.assertNotIn("scripts/a.py", prepared)
        self.assertNotIn("scripts/b.py", prepared)


class NormalizeTests(unittest.TestCase):
    def test_trims_wrapping_punctuation(self):
        self.assertEqual(paths.normalize("(`docs/overview.md`),"),
                         "docs/overview.md")

    def test_keeps_leading_dot_for_dot_github(self):
        self.assertEqual(paths.normalize(".github/workflows/"),
                         ".github/workflows/")


class ResolvesTests(unittest.TestCase):
    def test_real_paths_resolve(self):
        for token in ("scripts/tooling/validators/validate.py",
                      "docs/", "agents/resources/"):
            self.assertTrue(paths.resolves(token), token)

    def test_library_prefixed_registry_path_resolves(self):
        # Registry paths are tech-first and live under library/.
        self.assertTrue(paths.resolves("Tailwind/Templates"))

    def test_missing_path_does_not_resolve(self):
        self.assertFalse(paths.resolves("scripts/definitely-not-real.py"))


class ScanScopeTests(unittest.TestCase):
    def test_doc_globs_cover_resource_and_mcp_agent_docs(self):
        globs = set(paths.DOC_GLOBS)
        self.assertIn("agents/resources/*.md", globs)
        self.assertIn("library/**/AGENTS.md", globs)
        self.assertIn("integrations/mcp/**/*.md", globs)

    def test_library_agent_docs_are_reachable(self):
        from support import REPO_ROOT
        matched = {p for g in paths.DOC_GLOBS for p in REPO_ROOT.glob(g)}
        self.assertTrue(any("library/" in p.as_posix() for p in matched))


if __name__ == "__main__":
    unittest.main()
