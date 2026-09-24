"""Tests for validate.py's duplicate-id classification policy.

The registry keys on the tech-first path, so the same descriptive `id` may
legitimately appear across technologies (Tailwind/React id parity). Only a
collision inside one technology + content type + subcategory is a failure.
"""
from __future__ import annotations

import unittest

from support import load_module

validate = load_module("scripts/tooling/validators/validate.py")


def entry(path, tech, bucket, sub=""):
    return (path, tech, bucket, sub)


class DuplicateIdTests(unittest.TestCase):
    def test_unique_ids_produce_no_duplicates(self):
        collisions, informational = validate.classify_duplicate_ids({
            "hero-split": [entry("a/metadata.json", "React", "Sections", "hero")],
            "team-minimal": [entry("b/metadata.json", "Tailwind CSS", "Sections", "team")],
        })
        self.assertEqual(collisions, {})
        self.assertEqual(informational, {})

    def test_cross_technology_echo_is_informational(self):
        collisions, informational = validate.classify_duplicate_ids({
            "team-minimal": [
                entry("React/Sections/team-minimal/metadata.json", "React", "Sections", "team"),
                entry("Tailwind/Sections/team-minimal/metadata.json", "Tailwind CSS", "Sections", "team"),
            ],
        })
        self.assertEqual(collisions, {})
        self.assertIn("team-minimal", informational)

    def test_same_tech_type_subcategory_is_a_collision(self):
        collisions, informational = validate.classify_duplicate_ids({
            "pricing-simple": [
                entry("Tailwind/Sections/a/metadata.json", "Tailwind CSS", "Sections", "pricing"),
                entry("Tailwind/Sections/b/metadata.json", "Tailwind CSS", "Sections", "pricing"),
            ],
        })
        self.assertIn("pricing-simple", collisions)
        self.assertEqual(informational, {})

    def test_different_subcategory_same_tech_is_informational(self):
        collisions, informational = validate.classify_duplicate_ids({
            "card": [
                entry("Tailwind/Components/a/metadata.json", "Tailwind CSS", "Components", "cards"),
                entry("Tailwind/Components/b/metadata.json", "Tailwind CSS", "Components", "pricing"),
            ],
        })
        self.assertEqual(collisions, {})
        self.assertIn("card", informational)

    def test_subcategory_is_case_insensitive(self):
        collisions, _ = validate.classify_duplicate_ids({
            "card": [
                entry("Tailwind/Components/a/metadata.json", "Tailwind CSS", "Components", "Cards"),
                entry("Tailwind/Components/b/metadata.json", "Tailwind CSS", "Components", "cards"),
            ],
        })
        self.assertIn("card", collisions)


if __name__ == "__main__":
    unittest.main()
