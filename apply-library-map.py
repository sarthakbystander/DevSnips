# apply-library-map.py  — run from DevSnips repo root
from pathlib import Path
import re

# --- CLI: map downloads to library/ ---
p = Path("cli/src/install/downloader.js")
t = p.read_text(encoding="utf-8")
old = """function buildRepoFilePath(componentPath, filename) {
  const base = stripTrailingSlash(componentPath);
  return `${base}/${filename}`;
}"""
new = """function buildRepoFilePath(componentPath, filename) {
  const base = stripTrailingSlash(componentPath);
  // Map registry path → library/ on-disk location (user-facing paths stay tech-first)
  const repoBase = base.startsWith('library/') ? base : `library/${base}`;
  return `${repoBase}/${filename}`;
}"""
if old not in t:
    raise SystemExit("buildRepoFilePath block not found — check cli/src/install/downloader.js")
p.write_text(t.replace(old, new), encoding="utf-8")
print("OK: CLI library mapping")

# --- root index.html ---
p = Path("index.html")
t = p.read_text(encoding="utf-8")
for a, b in [
    ('href="Tailwind/index.html"', 'href="library/Tailwind/index.html"'),
    ('href="Vanilla/Sections/sections-index.html"', 'href="library/Vanilla/Sections/sections-index.html"'),
    ('href="React/"', 'href="library/React/"'),
]:
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("OK: index.html")

# --- library discovery HTML ---
for html in Path("library").rglob("index.html"):
    t = html.read_text(encoding="utf-8")
    orig = t
    t = t.replace('href="components/index.html"', 'href="Components/index.html"')
    t = t.replace('href="sections/index.html"', 'href="Sections/index.html"')
    t = t.replace('href="templates/index.html"', 'href="Templates/index.html"')
    t = t.replace('href="../components/index.html"', 'href="../Components/index.html"')
    t = t.replace('href="../sections/index.html"', 'href="../Sections/index.html"')
    t = t.replace('href="../templates/index.html"', 'href="../Templates/index.html"')
    t = t.replace("var href = '../../' + firstVar.path + 'preview.html';",
                  "var href = '../../library/' + firstVar.path + 'preview.html';")
    t = t.replace("var href = '../../' + fam.path + entry;",
                  "var href = '../../library/' + fam.path + entry;")
    t = t.replace("var href = '../../' + v.path + entry;",
                  "var href = '../../library/' + v.path + entry;")
    if t != orig:
        html.write_text(t, encoding="utf-8")
        print("OK:", html)

# --- tooling ROOT → library/ ---
for base in [
    Path("scripts/qa/resources"),
    Path("scripts/tooling/utilities"),
    Path("scripts/tooling/validators"),
    Path("scripts/tooling/generators"),
    Path("scripts/tooling/indexing"),
]:
    if not base.exists():
        continue
    for py in base.glob("*.py"):
        t = py.read_text(encoding="utf-8")
        orig = t
        t = re.sub(
            r"ROOT = Path\(__file__\)\.resolve\(\)\.parent\.parent\b",
            "ROOT = Path(__file__).resolve().parents[3]  # → repo root",
            t,
        )
        t = re.sub(
            r"ROOT = Path\(__file__\)\.resolve\(\)\.parents\[1\]",
            "ROOT = Path(__file__).resolve().parents[3]  # → repo root",
            t,
        )
        t = re.sub(r'ROOT / "React"', 'ROOT / "library" / "React"', t)
        t = re.sub(r'ROOT / "Tailwind"', 'ROOT / "library" / "Tailwind"', t)
        t = re.sub(r'ROOT / "Vanilla"', 'ROOT / "library" / "Vanilla"', t)
        t = re.sub(r"ROOT / tech_dir\b", 'ROOT / "library" / tech_dir', t)
        t = re.sub(r"ROOT / td\b", 'ROOT / "library" / td', t)
        t = t.replace(
            'vp = ROOT / v["path"].rstrip("/")',
            'vp = ROOT / "library" / v["path"].rstrip("/")',
        )
        t = t.replace(
            "tree = ROOT / root_dir / category",
            'tree = ROOT / "library" / root_dir / category',
        )
        t = t.replace(
            'tmpl = ROOT / root_dir / "Templates"',
            'tmpl = ROOT / "library" / root_dir / "Templates"',
        )
        if t != orig:
            py.write_text(t, encoding="utf-8")
            print("OK:", py)

print("Done.")
