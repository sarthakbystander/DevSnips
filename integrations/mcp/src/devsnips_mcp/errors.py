"""Structured error types for devsnips_mcp.

Every tool failure is returned as a JSON payload with a stable `code`, never
raised to the MCP transport. Codes are part of the tool contract.
"""
from __future__ import annotations

import json
import logging
import uuid
from typing import Any

logger = logging.getLogger("devsnips_mcp")

# Stable error codes (tool contract — additive only).
INVALID_ARGUMENT = "invalid_argument"
PATH_REJECTED = "path_rejected"
RESOURCE_NOT_FOUND = "resource_not_found"
FILE_NOT_FOUND = "file_not_found"
NOT_INSTALLABLE = "not_installable"
FILE_TOO_LARGE = "file_too_large"
REGISTRY_UNAVAILABLE = "registry_unavailable"
REGISTRY_INVALID = "registry_invalid"
SCHEMA_UNSUPPORTED = "schema_unsupported"
INTERNAL_ERROR = "internal_error"


class DevSnipsError(Exception):
    """A structured, tool-contract error."""

    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = dict(details or {})

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"error": {"code": self.code, "message": self.message}}
        if self.details:
            payload["error"]["details"] = self.details
        return payload


def error_payload(code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return DevSnipsError(code, message, details).to_payload()


def internal_error_payload(exc: BaseException) -> dict[str, Any]:
    trace_id = uuid.uuid4().hex[:12]
    logger.exception("internal error (trace_id=%s)", trace_id)
    return {"error": {
        "code": INTERNAL_ERROR,
        "message": f"Unexpected internal error (trace_id={trace_id}). See server logs.",
        "details": {"trace_id": trace_id, "exception": type(exc).__name__},
    }}


def dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
