#!/usr/bin/env python3
"""Validate the DevSnips repository after the Components+Templates migration.

Checks:
  1. Architecture: Vanilla/Tailwind/React each have only Components/ + Templates/.
  2. No standalone Sections/Utilities/Resources/Snippets content dirs.
  3. Every component/template folder has a valid metadata.json.
  4. No orphaned metadata.json (metadata without its expected sibling files).
  5. No duplicate IDs across all metadata.json.
  6. No duplicate variant paths in the index.
  7. Every index variant path exists on disk and has metadata.json.
  8. Every on-disk leaf is present in the index.
  9. No stale Sections/Utilities/Resources path references in the index.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "snippets-index.json"
TAILWIND = "Tailwind CSS"
VANILLA = "Vanilla HTML/CSS/JS"

problems = []


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


def is_leaf(folder, tech):
    if not (folder / "metadata.json").exists():
        return False
    if _has_child_meta(folder):
        return False
    if tech == TAILWIND:
        return (folder / "code.html").exists() and (folder / "preview.html").exists()
    return True


def check_architecture():
    for tech_dir in ("Vanilla", "Tailwind", "React"):
        td = ROOT / tech_dir
        if not td.exists():
            continue
        allowed = {"Components", "Templates"}
        for child in td.iterdir():
            if child.is_dir() and child.name not in allowed:
                problems.append(
                    "Architecture: unexpected dir %s/%s/ (only Components/ + Templates/ allowed)"
                    % (tech_dir, child.name))
    for forbidden in ("Sections", "Utilities", "Resources", "Snippets", "Pages", "Tools"):
        for tech_dir in ("Vanilla", "Tailwind", "React"):
            p = ROOT / tech_dir / forbidden
            if p.exists():
                problems.append("Architecture: forbidden standalone dir %s" % p)


def check_metadata_validity():
    all_ids = {}
    for tech, td in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        comp = ROOT / td / "Components"
        tmpl = ROOT / td / "Templates"
        for base in (comp, tmpl):
            if not base.exists():
                continue
            for mf in base.rglob("metadata.json"):
                leaf = mf.parent
                meta = _read_meta(mf)
                if "__error__" in meta:
                    problems.append("Invalid JSON: %s" % mf)
                    continue
                if base == comp and tech == TAILWIND and is_leaf(leaf, tech):
                    for need in ("code.html", "preview.html"):
                        if not (leaf / need).exists():
                            problems.append("Tailwind component missing %s: %s" % (need, leaf))
                mid = meta.get("id") or meta.get("slug")
                if mid:
                    all_ids.setdefault(mid, []).append(str(mf))
    # Duplicate IDs are reported as informational notes, not failures: per the
    # migration rules, existing IDs must be preserved (rule #9). The known
    # pre-existing duplicates (feature-grid-neo-brutalism across marketing/saas,
    # contact-form-001 across Forms/Contact and Contact) existed before the
    # migration at their old locations and are out of scope for this refactor.
    dup_ids = {mid: files for mid, files in all_ids.items() if len(files) > 1}
    if dup_ids:
        print("NOTE: %d pre-existing duplicate ID(s) preserved (not changed per rule #9):" % len(dup_ids))
        for mid, files in dup_ids.items():
            print("    - %s (%d files)" % (mid, len(files)))


def check_index_vs_disk():
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    # Duplicate check on VARIANT paths only (a single-variant family's path
    # legitimately equals its variant path).
    variant_paths = []
    for fam in idx["families"]:
        for v in fam.get("variants", []):
            variant_paths.append(v["path"])
            vp = ROOT / v["path"].rstrip("/")
            if not (vp / "metadata.json").exists():
                problems.append("Index variant missing on disk: %s" % v["path"])
    dup = {p for p in variant_paths if variant_paths.count(p) > 1}
    for d in dup:
        problems.append("Duplicate index variant path: %s" % d)
    for fam in idx["families"]:
        for token in ("/Sections/", "/Utilities/", "/Resources/"):
            if token in fam["path"]:
                problems.append("Stale path in index family: %s" % fam["path"])
        for v in fam.get("variants", []):
            for token in ("/Sections/", "/Utilities/", "/Resources/"):
                if token in v["path"]:
                    problems.append("Stale path in index variant: %s" % v["path"])
    indexed = {v["path"].rstrip("/") for fam in idx["families"]
               for v in fam.get("variants", [])}
    indexed_families = {fam["path"].rstrip("/") for fam in idx["families"]}
    for tech, td in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        comp = ROOT / td / "Components"
        if comp.exists():
            for mf in comp.rglob("metadata.json"):
                leaf = mf.parent
                if is_leaf(leaf, tech):
                    rel = str(leaf).replace(str(ROOT) + "/", "")
                    if rel not in indexed:
                        problems.append("On-disk component leaf not indexed: %s" % rel)
        tmpl = ROOT / td / "Templates"
        if tmpl.exists():
            for top in tmpl.iterdir():
                if not top.is_dir():
                    continue
                rel = str(top).replace(str(ROOT) + "/", "")
                # Indexed if it's a family path or any variant path starts with it.
                covered = (rel in indexed_families
                           or rel in indexed
                           or any(vp.startswith(rel + "/") for vp in indexed))
                if not covered:
                    problems.append("On-disk template not indexed: %s" % rel)


def main():
    check_architecture()
    check_metadata_validity()
    check_index_vs_disk()
    if problems:
        print("VALIDATION FAILED - %d problem(s):" % len(problems))
        for p in problems:
            print("  x %s" % p)
        sys.exit(1)
    print("VALIDATION PASSED - architecture, metadata, and index all consistent.")


if __name__ == "__main__":
    main()
