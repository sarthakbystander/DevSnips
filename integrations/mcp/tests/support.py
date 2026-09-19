"""Shared test support: import bootstrap + synthetic registry fixtures.

stdlib-only. Importing this module puts `src/` on sys.path so tests run with
`python -m unittest discover -s tests` from integrations/mcp/ — no install, no
environment variables required.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

REPO_ROOT = Path(__file__).resolve().parents[3]
MASTER_INDEX = REPO_ROOT / "snippets-index.json"
COMPONENTS_INDEX = REPO_ROOT / "agents" / "resources" / "indexes" / "components-index.json"
SECTIONS_INDEX = REPO_ROOT / "agents" / "resources" / "indexes" / "sections-index.json"
TEMPLATES_INDEX = REPO_ROOT / "agents" / "resources" / "indexes" / "templates-index.json"

TECHS = ("Tailwind CSS", "Vanilla HTML/CSS/JS", "React")


def make_variant(path: str, name: str | None = None, type_: str = "component",
                 description: str = "", tags=None, features=None, styles=None,
                 files=None) -> dict:
    return {
        "name": name or path.rstrip("/").rsplit("/", 1)[-1],
        "path": path if path.endswith("/") else path + "/",
        "type": type_,
        "description": description,
        "tags": list(tags or []),
        "features": list(features or []),
        "styles": list(styles or []),
        "files": list(files or ["README.md", "code.html", "metadata.json", "preview.html"]),
    }


def make_family(path: str, tech: str, type_: str, variants: list,
                name: str | None = None, category: str | None = None, tags=None,
                search_terms=None) -> dict:
    category = category or {"component": "Components", "section": "Sections",
                            "template": "Templates"}[type_]
    family = {
        "name": name or path.rstrip("/").rsplit("/", 1)[-1],
        "path": path if path.endswith("/") else path + "/",
        "tech": tech,
        "type": type_,
        "category": category,
        "description": "fixture family",
        "variantsCount": len(variants),
        "variants": variants,
    }
    if tags:
        family["tags"] = list(tags)
    if search_terms:
        family["searchTerms"] = list(search_terms)
    return family


def default_fixture_families() -> list:
    tailwind_buttons = make_family(
        "Tailwind/Components/Buttons", "Tailwind CSS", "component",
        [
            make_variant("Tailwind/Components/Buttons/basic-button/primary",
                         name="Primary Button", styles=["basic"],
                         tags=["button", "primary", "solid"],
                         features=["focus rings"],
                         description="Primary action buttons."),
            make_variant("Tailwind/Components/Buttons/dark-button",
                         name="Dark Button", styles=["dark", "dashboard"],
                         tags=["button", "dark", "dashboard"],
                         description="Dark-mode dashboard button."),
        ],
        name="Buttons", tags=["button", "cta"],
        search_terms=["solid button", "primary button", "submit button"])
    react_sidebar = make_family(
        "React/Components/Sidebar", "React", "component",
        [
            make_variant("React/Components/Sidebar/dark-sidebar", name="Dark Sidebar",
                         tags=["sidebar", "dark", "dashboard"],
                         styles=["dark"], features=["responsive", "light/dark"],
                         files=["README.md", "code.tsx", "metadata.json", "preview.html"],
                         description="Dark dashboard sidebar navigation."),
        ],
        name="Sidebar", tags=["sidebar", "navigation"])
    vanilla_hero = make_family(
        "Vanilla/Sections/Hero", "Vanilla HTML/CSS/JS", "section",
        [make_variant("Vanilla/Sections/Hero/hero-minimal", name="Hero — Minimal",
                      type_="section", tags=["hero", "minimal"],
                      files=["README.md", "code.html", "metadata.json"])],
        name="Hero", category="Sections")
    react_template = make_family(
        "React/Templates/spray-art-school", "React", "template",
        [
            make_variant("React/Templates/spray-art-school", name="SPRAY — Art School",
                         type_="template",
                         tags=["art-school", "multipage"],
                         files=["AGENTS.md", "README.md", "index.html", "metadata.json",
                                "package.json", "preview.html", "src/App.tsx", "src/main.tsx"],
                         description="Four-page React + TypeScript template."),
        ],
        name="SPRAY — Art School", category="Templates")
    return [tailwind_buttons, react_sidebar, vanilla_hero, react_template]


def make_registry(families: list | None = None) -> dict:
    if families is None:
        families = default_fixture_families()
    dict_families = [f for f in families if isinstance(f, dict)]
    return {
        "version": "2.0",
        "lastUpdated": "2026-09-18",
        "description": "fixture registry",
        "stats": {"totalFamilies": len(dict_families),
                  "totalVariants": sum(len(f["variants"]) for f in dict_families)},
        "families": families,
        "technologies": [{"name": tech, "path": f"library/{tech.split()[0]}/",
                          "status": "active", "families": []} for tech in TECHS],
    }


def make_synth_checkout(families: list | None = None) -> Path:
    """A minimal DevSnips checkout in a temp dir (registry + library files)."""
    registry = make_registry(families)
    root = Path(tempfile.mkdtemp(prefix="devsnips-mcp-test-"))
    (root / "snippets-index.json").write_text(json.dumps(registry), encoding="utf-8")
    for family in registry["families"]:
        for variant in family["variants"]:
            base = root / "library" / variant["path"].rstrip("/")
            base.mkdir(parents=True, exist_ok=True)
            for filename in variant["files"]:
                target = base / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"// fixture: {filename}\n", encoding="utf-8")
            # nested file NOT in the manifest (mirrors the React-template gap)
            if variant["type"] == "template":
                nested = base / "src" / "components"
                nested.mkdir(parents=True, exist_ok=True)
                (nested / "Badge.tsx").write_text("// nested\n", encoding="utf-8")
    return root


def require_repo_index(testcase: unittest.TestCase):
    if not MASTER_INDEX.exists():
        testcase.skipTest("snippets-index.json not found (not running inside the repo)")

