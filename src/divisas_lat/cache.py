import time
import threading
from typing import Any, Optional


class CacheEntry:
    def __init__(self, data: Any, expires_at: float):
        self.data = data
        self.expires_at = expires_at


class MemoryCache:
    """Thread-safe memory cache for Divisas.lat SDK."""
    
    def __init__(self, default_ttl_seconds: int = 3600):
        self.default_ttl = default_ttl_seconds
        self._cache = {}
        self._lock = threading.Lock()

    def set(self, key: str, item: Any) -> None:
        if self.default_ttl <= 0:
            return

        expires_at = time.time() + self.default_ttl
        entry = CacheEntry(data=item, expires_at=expires_at)
        
        with self._lock:
            self._cache[key] = entry
            
            # Prevent unbounded growth
            if len(self._cache) > 1000:
                self._cleanup_locked()

    def get(self, key: str) -> Optional[Any]:
        if self.default_ttl <= 0:
            return None

        with self._lock:
            entry = self._cache.get(key)
            if entry:
                if entry.expires_at > time.time():
                    return entry.data
                else:
                    del self._cache[key]
        return None

    def _cleanup_locked(self) -> None:
        """Removes elements until the cache size is 500. Assumes lock is held."""
        # Clean expired first
        now = time.time()
        expired_keys = [k for k, v in self._cache.items() if v.expires_at <= now]
        for k in expired_keys:
            del self._cache[k]
            
        # If still too big, remove arbitrary elements
        if len(self._cache) > 500:
            keys_to_remove = list(self._cache.keys())[:len(self._cache) - 500]
            for k in keys_to_remove:
                del self._cache[k]
