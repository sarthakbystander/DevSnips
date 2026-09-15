#!/usr/bin/env python3
"""Build the self-contained preview.html for a modular Vanilla template.

Inlines pages/style.css into the <link> and pages/script.js into the <script>,
producing a single preview.html that opens directly with no backend.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
code = (root / "pages/code.html").read_text(encoding="utf-8")
css = (root / "pages/style.css").read_text(encoding="utf-8")
js = (root / "pages/script.js").read_text(encoding="utf-8")

out = code.replace(
    '<link rel="stylesheet" href="style.css">',
    "<style>\n" + css + "\n</style>",
)
out = out.replace(
    '<script src="script.js" defer></script>',
    "<script>\n" + js + "\n</script>",
)
(root / "preview.html").write_text(out, encoding="utf-8")
print("preview.html written:", len(out), "bytes")
