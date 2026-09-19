"""CacheStore — one directory, JSON sidecar metadata, atomic writes, LRU cap.

Design notes (see integrations/mcp/implementation_plan.md §15):
- Entries live in kind-specific subdirectories (`registry/`, `files/`).
- Each entry is `<key>.bin` (payload) + `<key>.json` (sidecar metadata:
  origin, ref, etag, fetched_at epoch, bytes).
- Writes go to a temp file in the same directory followed by `os.replace`,
  so a truncated payload or metadata file is never observable (mirrors the
  atomic-write convention of the DevSnips CLI).
- Change detection hashes the *decoded* payload, so CRLF/working-tree
  differences can never produce false "changed" verdicts.
- `registry` entries are never evicted; when the total cache exceeds the cap,
  the oldest non-registry entries (by fetched_at) are deleted first.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

KIND_REGISTRY = "registry"
KIND_FILES = "files"
_META_SUFFIX = ".json"
_DATA_SUFFIX = ".bin"


def key_for(*parts: str) -> str:
    digest = hashlib.sha256(" ".join(parts).encode("utf-8")).hexdigest()
    return digest[:16]


def content_hash(data: bytes) -> str:
    """Hash the *normalized* payload: newline-insensitive by design."""
    normalized = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest()


class CacheStore:
    def __init__(self, root: Path, max_bytes: int = 200 * 1024 * 1024):
        self.root = Path(root)
        self.max_bytes = int(max_bytes)

    # ---------------------------------------------------------------- paths --
    def _dir(self, kind: str) -> Path:
        return self.root / kind

    def paths(self, kind: str, key: str) -> tuple[Path, Path]:
        base = self._dir(kind) / key
        return base.with_suffix(_DATA_SUFFIX), base.with_suffix(_META_SUFFIX)

    # ----------------------------------------------------------------- read --
    def get(self, kind: str, key: str) -> tuple[bytes, dict[str, Any]] | None:
        data_path, meta_path = self.paths(kind, key)
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            data = data_path.read_bytes()
        except (OSError, ValueError):
            # Corrupted or missing: clean up so a refetch starts from scratch.
            self.delete(kind, key)
            return None
        if not isinstance(meta, dict):
            self.delete(kind, key)
            return None
        return data, meta

    def get_text(self, kind: str, key: str) -> tuple[str, dict[str, Any]] | None:
        entry = self.get(kind, key)
        if entry is None:
            return None
        data, meta = entry
        try:
            return data.decode("utf-8"), meta
        except UnicodeDecodeError:
            self.delete(kind, key)
            return None

    @staticmethod
    def is_fresh(meta: dict[str, Any], ttl_s: int) -> bool:
        fetched_at = meta.get("fetched_at")
        if not isinstance(fetched_at, (int, float)):
            return False
        return (time.time() - float(fetched_at)) < ttl_s

    # ---------------------------------------------------------------- write --
    def put(self, kind: str, key: str, data: bytes, meta: dict[str, Any] | None = None) -> None:
        directory = self._dir(kind)
        directory.mkdir(parents=True, exist_ok=True)
        data_path, meta_path = self.paths(kind, key)
        record: dict[str, Any] = {
            "fetched_at": time.time(),
            "bytes": len(data),
            "sha256": content_hash(data),
        }
        record.update(meta or {})
        self._atomic_write(data_path, data)
        self._atomic_write(meta_path, json.dumps(record, ensure_ascii=False).encode("utf-8"))
        self.evict()

    def touch(self, kind: str, key: str) -> None:
        """Refresh fetched_at without rewriting the payload (304 revalidation)."""
        _data_path, meta_path = self.paths(kind, key)
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        if not isinstance(meta, dict):
            return
        meta["fetched_at"] = time.time()
        self._atomic_write(meta_path, json.dumps(meta, ensure_ascii=False).encode("utf-8"))

    def _atomic_write(self, path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".")
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(handle, "wb") as fh:
                fh.write(data)
            os.replace(tmp_path, path)
        except OSError:
            tmp_path.unlink(missing_ok=True)
            raise

    # ------------------------------------------------------------- eviction --
    def delete(self, kind: str, key: str) -> None:
        data_path, meta_path = self.paths(kind, key)
        data_path.unlink(missing_ok=True)
        meta_path.unlink(missing_ok=True)

    def total_bytes(self) -> int:
        total = 0
        for directory in (self._dir(KIND_REGISTRY), self._dir(KIND_FILES)):
            if directory.exists():
                for path in directory.glob("*" + _DATA_SUFFIX):
                    try:
                        total += path.stat().st_size
                    except OSError:
                        continue
        return total

    def evict(self) -> None:
        if self.total_bytes() <= self.max_bytes:
            return
        candidates = []
        files_dir = self._dir(KIND_FILES)
        if files_dir.exists():
            for meta_path in files_dir.glob("*" + _META_SUFFIX):
                try:
                    meta = json.loads(meta_path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    meta = {}
                fetched_at = meta.get("fetched_at")
                key = meta_path.name[: -len(_META_SUFFIX)]
                candidates.append((fetched_at if isinstance(fetched_at, (int, float)) else 0.0, key))
        candidates.sort()
        for _fetched_at, key in candidates:
            if self.total_bytes() <= self.max_bytes:
                break
            self.delete(KIND_FILES, key)

    def clear(self) -> None:
        for kind in (KIND_REGISTRY, KIND_FILES):
            directory = self._dir(kind)
            if not directory.exists():
                continue
            for path in directory.iterdir():
                try:
                    path.unlink()
                except OSError:
                    pass
