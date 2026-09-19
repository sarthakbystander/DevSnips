"""Schema gate + derived-field helpers for the DevSnips registry.

`is_installable` / `derive_id` / `install_command` deliberately mirror:

- scripts/tooling/indexing/build_resource_indexes.py  (is_installable, make_variant_entry)
- scripts/tooling/indexing/validate_indexes.py        (cli_would_install)
- cli/src/install/downloader.js                       (getSourceFiles)

tests/test_parity.py asserts byte-level agreement with the published specialized
indexes so any future drift between MCP and the CLI/indexes fails loudly.
"""
from __future__ import annotations

from collections.abc import Iterable

# Mirrors cli/src/install/downloader.js::getSourceFiles
SOURCE_EXTS = frozenset({".html", ".jsx", ".tsx", ".js", ".ts", ".css"})
NEVER_INSTALL = frozenset({"metadata.json", "preview.html"})
DOCS_INSTALL = frozenset({"README.md", "AGENTS.md"})

from .. import SUPPORTED_REGISTRY_SCHEMA


def schema_supported(version: object) -> bool:
    return isinstance(version, str) and version in SUPPORTED_REGISTRY_SCHEMA


def derive_id(path: str) -> str:
    """Canonical resource id: registry path without the trailing slash."""
    return (path or "").strip().rstrip("/")


def is_installable(files: Iterable[str]) -> bool:
    """Mirror of the CLI's installable-file predicate.

    The CLI errors with 'No source files found' only when NOTHING passes its
    filter, so an install command is derived only when at least one file passes.
    """
    for name in files or ():
        if name in NEVER_INSTALL:
            continue
        if name in DOCS_INSTALL:
            return True
        dot = name.rfind(".")
        if dot != -1 and name[dot:] in SOURCE_EXTS:
            return True
    return False


def install_command(resource_id: str) -> str:
    return f"npx devsnips add {resource_id}"
