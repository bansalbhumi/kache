import os
from core.dll import DoublyLinkedList
from core.node import Node

class LRUCache:
    def __init__(self, capacity: int = None):
        # Read from env variable if not passed directly
        self.capacity = capacity or int(os.getenv('MAX_KEYS', 100))
        self.map = {}               # key -> Node
        self.dll = DoublyLinkedList()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, key: str):
        """Return value if key exists and not expired. None otherwise."""
        if key not in self.map:
            self.misses += 1
            return None

        node = self.map[key]

        # Lazy TTL check — expire on access
        if node.is_expired():
            self._delete(key)
            self.misses += 1
            return None

        # Move to front = mark as most recently used
        self.dll.remove(node)
        self.dll.insert_after_head(node)
        self.hits += 1
        return node.value

    def set(self, key: str, value: str, ttl: int = None):
        """Insert or update a key."""
        if key in self.map:
            # Update existing node
            node = self.map[key]
            node.value = value
            import time
            node.expires_at = time.time() + ttl if ttl else None
            self.dll.remove(node)
            self.dll.insert_after_head(node)
        else:
            # Evict if at capacity
            if len(self.map) >= self.capacity:
                self._evict()
            node = Node(key, value, ttl)
            self.map[key] = node
            self.dll.insert_after_head(node)

    def delete(self, key: str) -> bool:
        """Manually delete a key. Returns True if existed."""
        if key not in self.map:
            return False
        self._delete(key)
        return True

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            'capacity':    self.capacity,
            'current_size': len(self.map),
            'hits':        self.hits,
            'misses':      self.misses,
            'evictions':   self.evictions,
            'hit_rate':    round(self.hits / total, 3) if total else 0.0,
            'miss_rate':   round(self.misses / total, 3) if total else 0.0,
        }

    # ── private helpers ─────────────────────────────────────────────
    def _delete(self, key: str):
        node = self.map.pop(key)
        self.dll.remove(node)

    def _evict(self):
        lru = self.dll.remove_before_tail()
        if lru:
            del self.map[lru.key]
            self.evictions += 1