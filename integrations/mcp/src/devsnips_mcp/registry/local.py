"""Local DevSnips checkout provider.

Reads the registry and the `library/` tree straight from a checkout. This is
the only provider that can enumerate the real file tree of a resource — which
recovers nested files the registry manifest omits (verified gap: React
templates list only one level of `src/**`).
"""
from __future__ import annotations

import os
from pathlib import Path

from ..errors import FILE_NOT_FOUND, REGISTRY_INVALID, REGISTRY_UNAVAILABLE, DevSnipsError
from .provider import FilePayload, ProviderInfo, RegistryPayload, library_rel_path

TECH_DIRS = ("React", "Tailwind", "Vanilla")
REGISTRY_FILE = "snippets-index.json"


class LocalRepoProvider:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        if not (self.root / REGISTRY_FILE).is_file():
            raise DevSnipsError(REGISTRY_INVALID, "not a DevSnips checkout",
                                {"root": str(self.root), "missing": REGISTRY_FILE})
        missing = [d for d in TECH_DIRS if not (self.root / "library" / d).is_dir()]
        if missing:
            raise DevSnipsError(REGISTRY_INVALID, "not a DevSnips checkout",
                                {"root": str(self.root), "missing_dirs": missing})

    # ---------------------------------------------------------------- info --
    def describe(self) -> ProviderInfo:
        return ProviderInfo(source="local", ref="local", origin=str(self.root), can_list_files=True)

    # ----------------------------------------------------------- registry ---
    def load_registry(self, etag: str | None = None) -> RegistryPayload:
        path = self.root / REGISTRY_FILE
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise DevSnipsError(REGISTRY_UNAVAILABLE, f"cannot read {REGISTRY_FILE}: {exc}",
                                {"origin": str(path)}) from exc
        return RegistryPayload(data=data, etag=None, origin=str(path))

    # -------------------------------------------------------------- files ---
    def read_file(self, rel_path: str, max_bytes: int | None = None) -> FilePayload:
        target = self._contained(rel_path)
        if target is None or not target.is_file():
            raise DevSnipsError(FILE_NOT_FOUND, f"file not found in checkout: {rel_path}",
                                {"path": rel_path, "origin": str(self.root)})
        limit = max_bytes if max_bytes else None
        with target.open("rb") as fh:
            data = fh.read(limit + 1) if limit else fh.read()
        truncated = limit is not None and len(data) > limit
        if truncated:
            data = data[:limit]
        return FilePayload(data=data, origin=str(target), truncated=truncated)

    def list_files(self, rel_dir: str) -> list[str] | None:
        base = self._contained(rel_dir)
        if base is None or not base.is_dir():
            return None
        found: list[str] = []
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for name in sorted(filenames):
                absolute = Path(dirpath) / name
                found.append(absolute.relative_to(base).as_posix())
        return found

    # ------------------------------------------------------------- safety ---
    def _contained(self, rel_path: str) -> Path | None:
        """Resolve rel_path under the checkout root, refusing escapes.

        rel_path is a repo-relative path such as `library/<tech>/.../file` or
        `snippets-index.json`. Anything resolving outside the checkout root is
        rejected (path-traversal defense).
        """
        clean = (rel_path or "").strip().replace("\\", "/")
        if not clean or clean.startswith("/") or ".." in clean.split("/"):
            return None
        candidate = (self.root / clean).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError:
            return None
        return candidate


def file_rel_path(resource_path: str, filename: str) -> str:
    return library_rel_path(resource_path, filename)
