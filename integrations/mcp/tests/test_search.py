"""Deterministic search tests (ordering, filters, modes, determinism)."""
from __future__ import annotations

import unittest

from support import default_fixture_families, make_family, make_registry, make_variant

from devsnips_mcp.errors import DevSnipsError
from devsnips_mcp.models import parse_registry
from devsnips_mcp.search.engine import SearchEngine
from devsnips_mcp.search.tokenizer import tokenize


def engine():
    return SearchEngine(parse_registry(make_registry()))


class TokenizerTests(unittest.TestCase):
    def test_stopwords_plurals_and_mojibake(self):
        tokens = tokenize("Find a responsive SaaS dashboards using â€” tokens")
        self.assertNotIn("a", tokens)
        self.assertNotIn("using", tokens)
        self.assertIn("dashboard", tokens)   # stemmed from "dashboards"
        self.assertIn("responsive", tokens)

    def test_deterministic_token_order(self):
        self.assertEqual(tokenize("dark dashboard sidebar"),
                         tokenize("DARK Dashboard SIDEBAR"))


class SearchRankingTests(unittest.TestCase):
    def test_exact_id_pins_rank_one(self):
        result = engine().search(query="React/Templates/spray-art-school")
        self.assertEqual(result["mode"], "exact")
        self.assertEqual(result["items"][0]["id"], "React/Templates/spray-art-school")
        self.assertGreater(result["items"][0]["score"], 40)

    def test_exact_name_phrase_outranks_looser_matches(self):
        result = engine().search(query="dark sidebar")
        self.assertEqual(result["items"][0]["id"], "React/Components/Sidebar/dark-sidebar")
        self.assertIn("name_phrase", result["items"][0]["matched_fields"])

    def test_type_intent_prefers_sections(self):
        result = engine().search(query="minimal hero section")
        self.assertEqual(result["items"][0]["type"], "section")
        self.assertEqual(result["items"][0]["id"], "Vanilla/Sections/Hero/hero-minimal")

    def test_family_search_terms_surface(self):
        result = engine().search(query="submit button")
        ids = [item["id"] for item in result["items"]]
        self.assertIn("Tailwind/Components/Buttons/basic-button/primary", ids)
        self.assertIn("family_search_terms", result["items"][0]["matched_fields"])

    def test_plurals_and_stopwords_match(self):
        result = engine().search(query="find the dark dashboards")
        ids = [item["id"] for item in result["items"]]
        self.assertIn("React/Components/Sidebar/dark-sidebar", ids)
        self.assertIn("Tailwind/Components/Buttons/dark-button", ids)

    def test_partial_mode_when_no_full_match(self):
        result = engine().search(query="dark quantum sidebar")
        self.assertEqual(result["mode"], "partial")
        self.assertTrue(result["items"])

    def test_determinism_same_query_same_order(self):
        first = engine().search(query="dark button component", limit=20)
        second = engine().search(query="dark button component", limit=20)
        self.assertEqual([i["id"] for i in first["items"]],
                         [i["id"] for i in second["items"]])


class SearchFilterTests(unittest.TestCase):
    def test_technology_aliases(self):
        for alias in ("react", "React", "REACT"):
            result = engine().search(technology=alias, limit=50)
            self.assertTrue(result["items"])
            self.assertTrue(all(item["tech"] == "React" for item in result["items"]))

    def test_type_filter_validates(self):
        with self.assertRaises(DevSnipsError):
            engine().search(type="widget")

    def test_tags_all_mode(self):
        result = engine().search(tags=["sidebar", "dark"], limit=50)
        self.assertEqual([item["id"] for item in result["items"]],
                         ["React/Components/Sidebar/dark-sidebar"])

    def test_tags_any_mode(self):
        result = engine().search(tags=["hero", "multipage"], tags_mode="any", limit=50)
        ids = {item["id"] for item in result["items"]}
        self.assertIn("Vanilla/Sections/Hero/hero-minimal", ids)
        self.assertIn("React/Templates/spray-art-school", ids)

    def test_installable_only_excludes_non_installable(self):
        families = default_fixture_families()
        families[1]["variants"][0]["files"] = ["metadata.json", "preview.html"]
        eng = SearchEngine(parse_registry(make_registry(families)))
        result = eng.search(technology="React", installable_only=True, limit=50)
        ids = {item["id"] for item in result["items"]}
        self.assertNotIn("React/Components/Sidebar/dark-sidebar", ids)
        self.assertIn("React/Templates/spray-art-school", ids)

    def test_unknown_technology_filter_passes_through(self):
        families = default_fixture_families() + [make_family(
            "Svelte/Components/Accordion", "Svelte", "component",
            [make_variant("Svelte/Components/Accordion/basic", name="Basic Accordion")],
            name="Accordion")]
        eng = SearchEngine(parse_registry(make_registry(families)))
        result = eng.search(technology="Svelte", limit=50)
        self.assertEqual([item["id"] for item in result["items"]],
                         ["Svelte/Components/Accordion/basic"])

    def test_paging_and_limit_validation(self):
        result = engine().search(limit=50, offset=3)
        self.assertTrue(result["truncated"])
        with self.assertRaises(DevSnipsError):
            engine().search(limit=500)
        with self.assertRaises(DevSnipsError):
            engine().search(offset=-1)

    def test_filtered_only_query(self):
        result = engine().search(technology="Tailwind CSS", limit=50)
        self.assertEqual(result["mode"], "filtered")
        self.assertEqual(result["total_matches"], 2)


if __name__ == "__main__":
    unittest.main()
