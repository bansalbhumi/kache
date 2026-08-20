import time

class Node:
    def __init__(self, key: str, value: str, ttl: int = None):
        self.key   = key
        self.value = value
        # If ttl given, store absolute expiry timestamp. None = never expires.
        self.expires_at = time.time() + ttl if ttl else None
        self.prev  = None   # pointer to previous node
        self.next  = None   # pointer to next node

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at