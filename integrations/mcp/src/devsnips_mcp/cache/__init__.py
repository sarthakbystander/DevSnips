"""devsnips_mcp.cache — bounded, atomic, ETag-revalidating cache."""
from .paths import default_cache_dir
from .store import CacheStore

__all__ = ["CacheStore", "default_cache_dir"]
