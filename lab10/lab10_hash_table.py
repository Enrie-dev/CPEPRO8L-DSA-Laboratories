class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.size = 0

    def _hash(self, key):
        # Sum of ASCII values modulo capacity
        return sum(ord(c) for c in str(key)) % self.capacity

    def put(self, key, value):
        idx = self._hash(key)
        temp = self.buckets[idx]
        while temp:
            if temp.key == key:      # key exists -> update value
                temp.value = value
                return
            temp = temp.next
        node = HashNode(key, value)  # insert at head of chain (O(1))
        node.next = self.buckets[idx]
        self.buckets[idx] = node
        self.size += 1

    def get(self, key):
        temp = self.buckets[self._hash(key)]
        while temp:
            if temp.key == key:
                return temp.value
            temp = temp.next
        return None

    def load_factor(self):
        return self.size / self.capacity

    def display(self):
        for idx in range(self.capacity):
            chain = []
            temp = self.buckets[idx]
            while temp:
                chain.append(f"[{temp.key}: {temp.value}]")
                temp = temp.next
            print(f"Bucket {idx}: " + " -> ".join(chain))


if __name__ == "__main__":
    print("=== Basic demo (capacity 5) ===")
    ht = HashTable(5)
    ht.put("Alice", 25)
    ht.put("Bob", 30)
    ht.put("Charlie", 35)
    ht.display()
    print(f"Load factor: {ht.load_factor():.2f}")

    print("\n=== Collision demo (capacity 5) ===")
    for k, v in [("Dave", 40), ("Eve", 28), ("Alice", 26)]:
        print(f"{k!r} -> bucket {ht._hash(k)}")
        ht.put(k, v)
    ht.display()
    print(f"Load factor: {ht.load_factor():.2f}")
    print("get('Alice') =", ht.get("Alice"), "(updated)")
