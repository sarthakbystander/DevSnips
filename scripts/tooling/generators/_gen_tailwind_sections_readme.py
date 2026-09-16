#!/usr/bin/env python3
"""Generate missing README.md files for Tailwind Sections.

Scans Tailwind/Sections/ for variant folders that are missing README.md and
generates them with a template structure matching the variant's metadata.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # → repo root
TAILWIND_SECTIONS = ROOT / "library" / "Tailwind" / "Sections"


def _read_meta(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def generate_readme_template(meta, variant_name):
    """Generate a README.md template from metadata."""
    name = meta.get("name", variant_name)
    description = meta.get("description", "")
    features = meta.get("features", [])
    tags = meta.get("tags", [])
    
    readme = f"# {name}\n\n"
    
    if description:
        readme += f"{description}\n\n"
    
    if features:
        readme += "## Features\n\n"
        for feature in features:
            readme += f"- {feature}\n"
        readme += "\n"
    
    if tags:
        readme += "## Tags\n\n"
        readme += ", ".join(f"`{tag}`" for tag in tags)
        readme += "\n\n"
    
    readme += "## Usage\n\n"
    readme += "Copy the HTML from `code.html` and the CSS from the `<style>` block into your project.\n"
    readme += "Customize the Tailwind classes and content as needed.\n"
    
    return readme


def _has_child_meta(folder):
    for c in folder.iterdir():
        if c.is_dir() and (c / "metadata.json").exists():
            return True
    return False


def is_leaf(folder):
    """Tailwind section leaf: code.html + preview.html + metadata.json, no child metadata."""
    if not (folder / "metadata.json").exists():
        return False
    if _has_child_meta(folder):
        return False
    return (folder / "code.html").exists() and (folder / "preview.html").exists()


def main(check_mode=False):
    if not TAILWIND_SECTIONS.exists():
        print("library/Tailwind/Sections/ not found.")
        return 0
    
    missing_count = 0
    generated_count = 0
    
    for category in sorted(TAILWIND_SECTIONS.iterdir()):
        if not category.is_dir():
            continue
        # Each category sub-folder is its own family (e.g. Contact, Newsletter, etc.)
        for family in sorted(category.iterdir()):
            if not family.is_dir():
                continue
            # Each style under family is a variant
            for variant in sorted(family.iterdir()):
                if not variant.is_dir():
                    continue
                if is_leaf(variant):
                    readme_path = variant / "README.md"
                    if not readme_path.exists():
                        missing_count += 1
                        if not check_mode:
                            meta = _read_meta(variant / "metadata.json")
                            content = generate_readme_template(meta, variant.name)
                            readme_path.write_text(content, encoding="utf-8")
                            generated_count += 1
                            print(f"Generated: {readme_path.relative_to(ROOT)}")
    
    if check_mode:
        if missing_count > 0:
            print(f"Tailwind Sections: {missing_count} missing README.md file(s)")
            return 1
        else:
            print("Tailwind Sections: all README.md files present")
            return 0
    else:
        print(f"Generated {generated_count} Tailwind Sections README.md files")
        return 0


if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    sys.exit(main(check_mode))
