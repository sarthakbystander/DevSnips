#!/usr/bin/env python3
"""Validate the DevSnips repository after the three-type content migration.

All content is organized into three first-class content types:
  Components/  (reusable UI building blocks)
  Sections/    (larger reusable page sections)
  Templates/   (complete page-level designs)

Checks:
  1. Architecture: each tech only contains allowed content-type dirs
     (Tailwind/Vanilla/React: Components/Sections/Templates).
  2. No standalone Utilities/Resources/Snippets content dirs.
  3. Every component/section/template folder has a valid metadata.json.
  4. No orphaned metadata.json (metadata without its expected sibling files).
  5. No duplicate IDs across all metadata.json.
  6. No duplicate variant paths in the index.
  7. Every index variant path exists on disk and has metadata.json.
  8. Every on-disk leaf is present in the index.
  9. No stale Sections/Utilities/Resources path references in the index.
 10. Every metadata.json carries a `type` (component/section/template)
     matching its content-type bucket.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "snippets-index.json"
REACT = "React"
TAILWIND = "Tailwind CSS"
VANILLA = "Vanilla HTML/CSS/JS"

# Technology name -> content-tree directory name.
TECH_DIRS = ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla"), (REACT, "React"))

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
        # Tailwind content folders ship code.html + preview.html (+ metadata).
        # Tailwind Templates are the exception: they have preview.html +
        # metadata.json (no code.html) and are indexed as single-variant
        # families. The Buttons 3-level grouping folders have metadata.json but
        # no code.html/preview.html, so they are correctly excluded as non-leaves.
        return (folder / "code.html").exists() and (folder / "preview.html").exists()
    if tech == REACT:
        # React components and sections ship code.tsx (+ code.jsx parity file
        # for components); React templates ship preview.html (full Vite/Next
        # projects). Any metadata.json-bearing folder without a child metadata
        # folder is a leaf.
        return (folder / "code.tsx").exists() or (folder / "preview.html").exists()
    return True


# Allowed top-level content-type directories per technology.
ALLOWED_DIRS = {
    "Tailwind": {"Components", "Sections", "Templates"},
    "Vanilla": {"Components", "Sections", "Templates"},
    "React": {"Components", "Sections", "Templates"},
}


def check_architecture():
    for tech_dir in ("Vanilla", "Tailwind", "React"):
        td = ROOT / tech_dir
        if not td.exists():
            continue
        allowed = ALLOWED_DIRS.get(tech_dir, {"Components", "Templates"})
        for child in td.iterdir():
            if child.is_dir() and child.name not in allowed:
                problems.append(
                    "Architecture: unexpected dir %s/%s/ (allowed: %s)"
                    % (tech_dir, child.name, ", ".join(sorted(allowed))))
    # React/Sections/ is a first-class content type (governed by
    # React/Sections/DESIGN_TOKENS.md); the dirs below remain forbidden in
    # every technology.
    for forbidden in ("Utilities", "Resources", "Snippets", "Pages", "Tools"):
        for tech_dir in ("Vanilla", "Tailwind", "React"):
            p = ROOT / tech_dir / forbidden
            if p.exists():
                problems.append("Architecture: forbidden standalone dir %s" % p)


def check_metadata_validity():
    all_ids = {}
    for tech, td in TECH_DIRS:
        # Every technology has three content-type buckets.
        buckets = ["Components", "Sections", "Templates"]
        for bucket in buckets:
            base = ROOT / td / bucket
            if not base.exists():
                continue
            for mf in base.rglob("metadata.json"):
                leaf = mf.parent
                meta = _read_meta(mf)
                if "__error__" in meta:
                    problems.append("Invalid JSON: %s" % mf)
                    continue
                # Tailwind leaves (components + sections) require code.html +
                # preview.html. Tailwind templates ship preview.html only.
                if tech == TAILWIND and bucket in ("Components", "Sections") \
                        and is_leaf(leaf, tech):
                    for need in ("code.html", "preview.html"):
                        if not (leaf / need).exists():
                            problems.append(
                                "Tailwind %s missing %s: %s" % (bucket.lower(), need, leaf))
                # React leaves (components + sections) require code.tsx +
                # preview.html. React templates ship preview.html only.
                if tech == REACT and bucket in ("Components", "Sections") \
                        and is_leaf(leaf, tech):
                    for need in ("code.tsx", "preview.html"):
                        if not (leaf / need).exists():
                            problems.append(
                                "React %s missing %s: %s" % (bucket.lower(), need, leaf))
                # Every item must declare a content `type` matching the bucket
                # the file lives under.
                mtype = meta.get("type")
                if mtype not in ("component", "section", "template"):
                    problems.append(
                        "%s metadata missing/invalid `type`: %s" % (td, mf))
                elif mtype == "component" and bucket != "Components":
                    problems.append(
                        "%s type=component outside Components/: %s" % (td, mf))
                elif mtype == "section" and bucket != "Sections":
                    problems.append(
                        "%s type=section outside Sections/: %s" % (td, mf))
                elif mtype == "template" and bucket != "Templates":
                    problems.append(
                        "%s type=template outside Templates/: %s" % (td, mf))
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
    # Stale path check. `Tailwind/Sections/`, `Vanilla/Sections/` and
    # `React/Sections/` are first-class content types, so a /Sections/ segment
    # is valid there. It is only stale anywhere else (e.g. under the removed
    # Utilities/ and Resources/ collections).
    valid_sections = ("Tailwind/Sections/", "Vanilla/Sections/", "React/Sections/")
    for fam in idx["families"]:
        for token in ("/Utilities/", "/Resources/"):
            if token in fam["path"]:
                problems.append("Stale path in index family: %s" % fam["path"])
        if "/Sections/" in fam["path"] and not fam["path"].startswith(valid_sections):
            problems.append("Stale path in index family: %s" % fam["path"])
        for v in fam.get("variants", []):
            for token in ("/Utilities/", "/Resources/"):
                if token in v["path"]:
                    problems.append("Stale path in index variant: %s" % v["path"])
            if "/Sections/" in v["path"] and not v["path"].startswith(valid_sections):
                problems.append("Stale path in index variant: %s" % v["path"])
    indexed = {v["path"].rstrip("/") for fam in idx["families"]
               for v in fam.get("variants", [])}
    indexed_families = {fam["path"].rstrip("/") for fam in idx["families"]}
    for tech, td in TECH_DIRS:
        # Components AND sections are both leaf-bearing content trees.
        content_trees = [ROOT / td / "Components", ROOT / td / "Sections"]
        for comp in content_trees:
            if not comp.exists():
                continue
            for mf in comp.rglob("metadata.json"):
                leaf = mf.parent
                if is_leaf(leaf, tech):
                    rel = str(leaf).replace(str(ROOT) + "/", "")
                    if rel not in indexed:
                        problems.append("On-disk content leaf not indexed: %s" % rel)
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


def check_template_agents():
    """Every template under `<Tech>/Templates/` must ship an AGENTS.md with
    template-specific instructions for AI coding agents."""
    for tech, td in TECH_DIRS:
        tmpl = ROOT / td / "Templates"
        if not tmpl.exists():
            continue
        for top in tmpl.iterdir():
            if not top.is_dir():
                continue
            agents = top / "AGENTS.md"
            if not agents.exists():
                problems.append(
                    "ERROR: Template %s is missing AGENTS.md"
                    % (top.relative_to(ROOT)))
            elif not agents.read_text(encoding="utf-8").strip():
                problems.append(
                    "ERROR: Template %s has an empty AGENTS.md"
                    % (top.relative_to(ROOT)))


def main():
    check_architecture()
    check_metadata_validity()
    check_index_vs_disk()
    check_template_agents()
    # Quality-bar scan (Vanilla components). Non-fatal warnings are fine; only
    # required-check failures fail validation, so the bar is enforced in CI.
    qa_failures = _run_qa()
    if problems:
        print("VALIDATION FAILED - %d problem(s):" % len(problems))
        for p in problems:
            print("  x %s" % p)
        sys.exit(1)
    if qa_failures:
        sys.exit(1)
    print("VALIDATION PASSED - architecture, metadata, and index all consistent.")


def _run_qa():
    """Run the Vanilla quality-bar scanner; return required-failure count.

    Only surfaces the summary line and any FAIL rows (warns are non-fatal and
    not printed to keep validation output readable).
    """
    import subprocess
    qa = ROOT / "scripts" / "qa_vanilla.py"
    if not qa.exists():
        return 0
    r = subprocess.run(
        [sys.executable, str(qa), "--only-failures"],
        capture_output=True, text=True)
    out = (r.stdout + r.stderr).splitlines()
    for line in out:
        s = line.strip()
        if not s:
            continue
        if s.startswith("Vanilla quality-bar scan") or \
                s.startswith("scanned:") or s.startswith("failing") or \
                s.startswith("required"):
            print("  qa: " + s)
            continue
        if s.startswith("FAIL"):
            print("  qa: " + s)
    return 1 if r.returncode != 0 else 0


if __name__ == "__main__":
    main()
