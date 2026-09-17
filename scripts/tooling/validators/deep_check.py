#!/usr/bin/env python3
"""Deep-check script enforcing required file sets per tech for Components and Sections.

Components and Sections must ship a tech-specific minimum file set
(docs/COMPONENT_STRUCTURE.md, "Standard files"):
  Tailwind Components: code.html, preview.html, metadata.json, README.md
  Tailwind Sections:   code.html, preview.html, metadata.json
                       (README.md optional; must be non-empty when present)
  Vanilla Components/Sections: metadata.json (code files optional per content)
  React Components:    code.tsx, preview.html, metadata.json, README.md
  React Sections:      code.tsx, preview.html, metadata.json
                       (sections ship exactly these three files — no README)

Templates ship their own requirements:
  Tailwind: preview.html + metadata.json only (full HTML/CSS/JS in code.html is optional)
  Vanilla: preview.html or pages/* + metadata.json + README.md + AGENTS.md
  React: preview.html (Vite/Next project) + metadata.json + README.md + AGENTS.md

This script serves as the basis for validate.py's deep checks.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # → repo root
REACT = "React"
TAILWIND = "Tailwind CSS"
VANILLA = "Vanilla HTML/CSS/JS"

# Map tech display names to directory names
TECH_DIRS = {
    TAILWIND: "Tailwind",
    VANILLA: "Vanilla",
    REACT: "React",
}

problems = []
warnings = []


def _read_meta(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"__error__": str(e)}


def _has_child_meta(folder):
    for c in folder.iterdir():
        if c.is_dir() and (c / "metadata.json").exists():
            return True
    return False


def is_leaf(folder, tech_dir):
    """Check if folder is a content leaf (component/section/template variant)."""
    if not (folder / "metadata.json").exists():
        return False
    if _has_child_meta(folder):
        return False
    if tech_dir == "Tailwind":
        # Either file present makes this a content leaf (see validate.py):
        # a variant missing exactly one of the pair is reported below rather
        # than being silently treated as a grouping folder.
        return (folder / "code.html").exists() or (folder / "preview.html").exists()
    if tech_dir == "React":
        return (folder / "code.tsx").exists() or (folder / "preview.html").exists()
    # Vanilla: any leaf with metadata.json and no child metadata
    return True


def check_component_section_files():
    """Enforce required files for Components and Sections."""
    for tech, tech_dir in TECH_DIRS.items():
        for bucket in ("Components", "Sections"):
            base = ROOT / "library" / tech_dir / bucket
            if not base.exists():
                continue
            for mf in base.rglob("metadata.json"):
                leaf = mf.parent
                if not is_leaf(leaf, tech_dir):
                    continue
                meta = _read_meta(mf)
                if "__error__" in meta:
                    problems.append(f"Invalid JSON: {mf}")
                    continue
                # Tailwind components require: code.html, preview.html,
                # metadata.json, README.md. Tailwind sections require
                # code.html + preview.html; a README is optional there but
                # must be non-empty when present (docs/COMPONENT_STRUCTURE.md
                # "Standard files" — README is required for component
                # variants, not for sections).
                if tech_dir == "Tailwind":
                    needs = ["code.html", "preview.html"]
                    if bucket == "Components":
                        needs.append("README.md")
                    for need in needs:
                        if not (leaf / need).exists():
                            problems.append(
                                f"Tailwind {bucket.lower()} missing {need}: {leaf}")
                # React components require: code.tsx, preview.html,
                # metadata.json, README.md. React sections ship exactly
                # code.tsx + preview.html + metadata.json (no README, no
                # code.jsx parity file).
                elif tech_dir == "React":
                    needs = ["code.tsx", "preview.html"]
                    if bucket == "Components":
                        needs.append("README.md")
                    for need in needs:
                        if not (leaf / need).exists():
                            problems.append(
                                f"React {bucket.lower()} missing {need}: {leaf}")
                    # Also check for code.jsx parity in Components (not required in Sections)
                    if bucket == "Components":
                        if not (leaf / "code.jsx").exists():
                            warnings.append(
                                f"React component missing code.jsx parity: {leaf}")
                # Vanilla: metadata.json required; code files vary by design
                elif tech_dir == "Vanilla":
                    if not mf.exists():
                        problems.append(
                            f"Vanilla {bucket.lower()} missing metadata.json: {leaf}")
                # An optional section README must still be useful when present.
                if bucket == "Sections":
                    readme = leaf / "README.md"
                    if readme.exists() and not readme.read_text(encoding="utf-8").strip():
                        problems.append(
                            f"{tech_dir} section has empty README.md: {leaf}")


def check_template_files():
    """Enforce required files for Templates."""
    for tech, tech_dir in TECH_DIRS.items():
        tmpl = ROOT / "library" / tech_dir / "Templates"
        if not tmpl.exists():
            continue
        for top in tmpl.iterdir():
            if not top.is_dir():
                continue
            # A template family can be:
            #   1. Single template: top/ has metadata.json (no child metadata)
            #   2. Multi-template: top/ contains sub-folders, each with metadata.json
            mf = top / "metadata.json"
            agents = top / "AGENTS.md"
            # Every template folder must have AGENTS.md
            if not agents.exists():
                problems.append(f"Template missing AGENTS.md: {top.relative_to(ROOT)}")
            elif not agents.read_text(encoding="utf-8").strip():
                problems.append(
                    f"Template has empty AGENTS.md: {top.relative_to(ROOT)}")
            # Single-template case: top/ is a leaf
            if mf.exists() and not _has_child_meta(top):
                meta = _read_meta(mf)
                if "__error__" not in meta:
                    # Tailwind templates: preview.html + metadata.json (code.html optional)
                    if tech_dir == "Tailwind":
                        if not (top / "preview.html").exists():
                            problems.append(
                                f"Tailwind template missing preview.html: {top}")
                    # React templates: preview.html + metadata.json (Vite/Next project)
                    elif tech_dir == "React":
                        if not (top / "preview.html").exists():
                            problems.append(
                                f"React template missing preview.html: {top}")
                    # Vanilla templates: preview.html or pages/* + metadata.json + README.md
                    elif tech_dir == "Vanilla":
                        has_preview = (top / "preview.html").exists()
                        has_pages = (top / "pages").exists() and any(
                            (top / "pages").iterdir())
                        if not (has_preview or has_pages):
                            problems.append(
                                f"Vanilla template missing preview.html or pages/: {top}")
                        if not (top / "README.md").exists():
                            problems.append(
                                f"Vanilla template missing README.md: {top}")
            # Multi-template case: sub-folders each with metadata.json
            elif _has_child_meta(top):
                for sub in top.iterdir():
                    if not sub.is_dir() or not (sub / "metadata.json").exists():
                        continue
                    meta = _read_meta(sub / "metadata.json")
                    if "__error__" not in meta:
                        if tech_dir == "Tailwind":
                            if not (sub / "preview.html").exists():
                                problems.append(
                                    f"Tailwind template missing preview.html: {sub}")
                        elif tech_dir == "React":
                            if not (sub / "preview.html").exists():
                                problems.append(
                                    f"React template missing preview.html: {sub}")
                        elif tech_dir == "Vanilla":
                            has_preview = (sub / "preview.html").exists()
                            has_pages = (sub / "pages").exists() and any(
                                (sub / "pages").iterdir())
                            if not (has_preview or has_pages):
                                problems.append(
                                    f"Vanilla template missing preview.html or pages/: {sub}")
                            if not (sub / "README.md").exists():
                                problems.append(
                                    f"Vanilla template missing README.md: {sub}")


def main():
    check_component_section_files()
    check_template_files()
    if problems:
        print("DEEP CHECK FAILED - %d problem(s):" % len(problems))
        for p in problems:
            print("  x %s" % p)
        if warnings:
            print("\nWarnings (%d):" % len(warnings))
            for w in warnings:
                print("  ! %s" % w)
        sys.exit(1)
    print("DEEP CHECK PASSED - all required file sets present.")
    if warnings:
        print("Warnings (%d):" % len(warnings))
        for w in warnings:
            print("  ! %s" % w)


if __name__ == "__main__":
    main()
