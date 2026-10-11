from cachetools import TTLCache
import config

class ResponseCache:
    def __init__(self, maxsize: int = config.CACHE_MAX_SIZE, ttl: int = config.CACHE_TTL_SECONDS):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _normalize_key(text: str) -> str:
        return text.strip().lower()

    def get(self, text: str) -> str | None:
        key = self._normalize_key(text)
        if key in self._cache:
            self.hits += 1
            return self._cache[key]
        self.misses += 1
        return None

    def set(self, text: str, response: str):
        key = self._normalize_key(text)
        self._cache[key] = response

    def clear(self):
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    @property
    def size(self) -> int:
        return len(self._cache)

    @property
    def stats(self) -> dict:
        total = self.hits + self.misses
        hit_ratio = round((self.hits / total) * 100, 1) if total > 0 else 0.0
        return {
            "cached_entries": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "total_queries": total,
            "hit_ratio_percent": hit_ratio,
            "ttl_minutes": config.CACHE_TTL_SECONDS // 60
        }

cache = ResponseCache()
