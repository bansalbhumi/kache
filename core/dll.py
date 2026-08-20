from core.node import Node

class DoublyLinkedList:
    def __init__(self):
        self.head = Node('HEAD', '')   # dummy head (left sentinel)
        self.tail = Node('TAIL', '')   # dummy tail (right sentinel)
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert_after_head(self, node: Node):
        """Put node right after HEAD = mark as most recently used."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node: Node):
        """Unlink node from wherever it currently sits."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def remove_before_tail(self) -> Node:
        """Remove and return the LRU node (just before TAIL)."""
        lru = self.tail.prev
        if lru == self.head:
            return None   # list is empty
        self.remove(lru)
        return lru