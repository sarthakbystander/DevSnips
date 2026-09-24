"""Shared loader so the tooling tests can import the standalone scripts.

The validators and indexers are standalone scripts, not a package, so they are
loaded by file path. Run the suite with

    python -m unittest discover -s scripts/tooling/tests

from the repository root.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def load_module(rel_path: str):
    """Import a repo file (relative to root) as a module by path."""
    path = REPO_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
