"""Registry schema helpers (id/install derivation, schema-version gate)."""
from .schema import (
    DOCS_INSTALL,
    NEVER_INSTALL,
    SOURCE_EXTS,
    derive_id,
    install_command,
    is_installable,
    schema_supported,
)

__all__ = [
    "DOCS_INSTALL",
    "NEVER_INSTALL",
    "SOURCE_EXTS",
    "derive_id",
    "install_command",
    "is_installable",
    "schema_supported",
]
