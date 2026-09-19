"""GitHub raw provider (the default; mirrors the DevSnips CLI's data source).

- Registry:  {base_url}/{ref}/snippets-index.json
- Files:     {base_url}/{ref}/library/<registry path>/<filename>

Hard rules carried over from the CLI (cli/src/registry/resolver.js,
cli/src/install/downloader.js):
- HTTP responses whose content type is text/html are rejected (HTML error
  pages must never be served as registry or source content).
- Empty responses are treated as failures.
- The fetcher is injectable for tests (`fetcher=`), and redirects are limited
  to same-host https (no redirect abuse).
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable

from ..errors import FILE_NOT_FOUND, REGISTRY_INVALID, REGISTRY_UNAVAILABLE, DevSnipsError
from .provider import FilePayload, ProviderInfo, RegistryPayload, library_rel_path  # noqa: F401

FetchResult = tuple[int, bytes | None, str | None, str | None]
Fetcher = Callable[[str, dict, float, int | None], FetchResult]

DEFAULT_TIMEOUT_S = 30.0


class _SameHostRedirect(urllib.request.HTTPRedirectHandler):
    """Allow redirects only within the same https host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        original = urllib.parse.urlparse(req.full_url)
        if parsed.scheme != "https":
            raise urllib.error.HTTPError(newurl, code, "insecure redirect rejected", headers, fp)
        if (parsed.scheme, parsed.netloc) != (original.scheme, original.netloc):
            raise urllib.error.HTTPError(newurl, code, "cross-host redirect rejected", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_SameHostRedirect())


def _http_get(url: str, headers: dict, timeout_s: float, max_bytes: int | None) -> FetchResult:
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        response = _OPENER.open(request, timeout=timeout_s)
    except urllib.error.HTTPError as exc:
        if exc.code == 304:
            return 304, None, (exc.headers.get("ETag") if exc.headers else None), None
        raise
    etag = response.headers.get("ETag")
    content_type = response.headers.get("Content-Type")
    body = response.read(max_bytes + 1) if max_bytes else response.read()
    return int(getattr(response, "status", 200) or 200), body, etag, content_type


class GitHubRawProvider:
    def __init__(self, base_url: str, ref: str, timeout_s: float = DEFAULT_TIMEOUT_S,
                 fetcher: Fetcher | None = None):
        self.base_url = base_url.rstrip("/")
        self.ref = (ref or "main").strip()
        self.timeout_s = timeout_s
        self._fetch: Fetcher = fetcher or _http_get

    # ---------------------------------------------------------------- info --
    def describe(self) -> ProviderInfo:
        return ProviderInfo(
            source="github",
            ref=self.ref,
            origin=f"{self.base_url}/{self.ref}",
            can_list_files=False,  # GitHub raw cannot enumerate directories
        )

    # ----------------------------------------------------------- registry ---
    def load_registry(self, etag: str | None = None) -> RegistryPayload:
        url = f"{self.base_url}/{self.ref}/snippets-index.json"
        headers = {"Accept": "application/json"}
        if etag:
            headers["If-None-Match"] = etag
        try:
            status, body, new_etag, content_type = self._fetch(url, headers, self.timeout_s, None)
        except DevSnipsError:
            raise
        except Exception as exc:  # network layer
            raise DevSnipsError(REGISTRY_UNAVAILABLE,
                                f"could not reach the DevSnips registry: {exc}",
                                {"origin": url, "ref": self.ref}) from exc
        if status == 304:
            return RegistryPayload(data=None, etag=etag, not_modified=True, origin=url)
        if status != 200:
            raise DevSnipsError(REGISTRY_UNAVAILABLE, f"registry fetch failed: HTTP {status}",
                                {"origin": url, "ref": self.ref})
        if content_type and "text/html" in content_type.lower():
            raise DevSnipsError(REGISTRY_INVALID, "registry endpoint returned HTML",
                                {"origin": url, "ref": self.ref})
        if not body or not body.strip():
            raise DevSnipsError(REGISTRY_INVALID, "registry endpoint returned an empty body",
                                {"origin": url, "ref": self.ref})
        try:
            json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise DevSnipsError(REGISTRY_INVALID, f"registry returned invalid JSON: {exc}",
                                {"origin": url, "ref": self.ref}) from exc
        return RegistryPayload(data=body, etag=new_etag, origin=url)

    # -------------------------------------------------------------- files ---
    def read_file(self, rel_path: str, max_bytes: int | None = None) -> FilePayload:
        clean = (rel_path or "").strip().replace("\\", "/")
        if not clean or clean.startswith("/") or ".." in clean.split("/"):
            raise DevSnipsError(FILE_NOT_FOUND, f"unsafe path rejected: {rel_path!r}",
                                {"path": rel_path})
        url = f"{self.base_url}/{self.ref}/{clean}"
        try:
            status, body, etag, content_type = self._fetch(url, {}, self.timeout_s, max_bytes)
        except DevSnipsError:
            raise
        except Exception as exc:
            raise DevSnipsError(REGISTRY_UNAVAILABLE, f"could not fetch file: {exc}",
                                {"origin": url, "ref": self.ref, "path": clean}) from exc
        if status != 200:
            code = FILE_NOT_FOUND if status == 404 else REGISTRY_UNAVAILABLE
            raise DevSnipsError(code, f"file fetch failed: HTTP {status}",
                                {"origin": url, "ref": self.ref, "path": clean})
        if content_type and "text/html" in content_type.lower():
            raise DevSnipsError(FILE_NOT_FOUND, "file endpoint returned HTML (stale path?)",
                                {"origin": url, "ref": self.ref, "path": clean})
        if not body:
            raise DevSnipsError(FILE_NOT_FOUND, "file endpoint returned an empty body",
                                {"origin": url, "ref": self.ref, "path": clean})
        truncated = max_bytes is not None and len(body) > max_bytes
        if truncated:
            body = body[:max_bytes]
        return FilePayload(data=body, etag=etag, origin=url, truncated=truncated)

    def list_files(self, rel_dir: str) -> list[str] | None:
        return None  # GitHub raw cannot enumerate directories
