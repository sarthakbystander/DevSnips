"""RegistryProvider interface + payload types.

A provider answers exactly three questions:

1. load_registry()  → the authoritative registry bytes (snippets-index.json)
2. read_file()      → one file from the canonical library tree
3. list_files()     → the real file tree of a resource (None = cannot enumerate)

Resource paths passed to read_file/list_files are ALWAYS tech-first registry
paths (`React/Components/...`); providers map them to their own storage
(`library/<path>` for GitHub and local checkouts). Tools never see or accept a
URL — swapping GitHub for a CDN or a future DevSnips API is a config change,
not a tool-contract change.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderInfo:
    source: str            # "github" | "local" | "http"
    ref: str
    origin: str            # base URL or local root (for humans/logs)
    can_list_files: bool   # True only when the provider can walk the real tree


@dataclass
class RegistryPayload:
    """Result of load_registry(). data is None exactly when not_modified."""
    data: bytes | None
    etag: str | None
    not_modified: bool = False
    origin: str = ""


@dataclass
class FilePayload:
    data: bytes
    etag: str | None = None
    origin: str = ""
    truncated: bool = False


class RegistryProvider(Protocol):
    def describe(self) -> ProviderInfo: ...

    def load_registry(self, etag: str | None = None) -> RegistryPayload: ...

    def read_file(self, rel_path: str, max_bytes: int | None = None) -> FilePayload: ...

    def list_files(self, rel_dir: str) -> list[str] | None:
        """Relative POSIX paths under rel_dir, or None when not enumerable."""
        ...


def library_rel_path(resource_path: str, filename: str) -> str:
    """Registry path + filename → canonical on-disk repo path (library/<path>/<file>).

    Mirrors cli/src/install/downloader.js::buildRepoFilePath.
    """
    base = (resource_path or "").strip().rstrip("/")
    return f"library/{base}/{filename}"
