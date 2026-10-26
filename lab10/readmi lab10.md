# Laboratory Activity No. 10: Hash Tables and Collision Resolution

**Course:** CPEPRO8L – Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## Objectives
1. Implement a custom hash mapping function (sum of ASCII values modulo capacity).
2. Design a collision resolution mechanism using linked-list buckets (separate chaining).
3. Observe how load factor affects search efficiency.

## Files
- `lab10_hash_table.py` – `HashNode` and `HashTable` with `_hash`, `put`, `get`, `load_factor`, `display`.

## Implementation Notes
- `_hash(key)` = `sum(ord(c) for c in key) % capacity`.
- `put` hashes the key, walks the chain to update an existing key, otherwise inserts a new node at the head of the chain.
- `get` hashes the key and walks only that bucket's chain.

## Execution & Output
Run: `python lab10_hash_table.py`

```
=== Basic demo (capacity 5) ===
Bucket 0: [Bob: 30]
Bucket 1: [Charlie: 35]
Bucket 2:
Bucket 3: [Alice: 25]
Bucket 4:
Load factor: 0.60

=== Collision demo (capacity 5) ===
'Dave' -> bucket 4
'Eve' -> bucket 3
'Alice' -> bucket 3
Bucket 0: [Bob: 30]
Bucket 1: [Charlie: 35]
Bucket 2:
Bucket 3: [Eve: 28] -> [Alice: 26]
Bucket 4: [Dave: 40]
Load factor: 1.00
get('Alice') = 26 (updated)
```

## Report Analysis Questions

### 1. Hash table entries demonstrating a collision event

| Key   | ASCII sum | Sum mod 5 | Bucket |
|-------|-----------|-----------|--------|
| Alice | 478       | 3         | 3      |
| Eve   | 288       | 3         | 3      |

`Eve` and `Alice` both hash to **bucket 3**, so `Eve` was chained in front of `Alice`:
`Bucket 3: [Eve: 28] -> [Alice: 26]`. The later `put("Alice", 26)` updated the existing node instead of adding a new one.

### 2. Chaining vs. linear probing: search efficiency

| Aspect | Chaining | Linear probing |
|---|---|---|
| Storage | Entries live in linked lists outside the array | Entries stored in the array itself |
| Average search | O(1 + α), α = n/m | ≈ ½(1 + 1/(1−α)) probes for a hit |
| Worst case | O(n) (all keys in one chain) | O(n) |
| Behavior as α → 1 | Degrades gradually (chains grow linearly) | Degrades sharply; clustering makes probe runs long |
| Load factor limit | Can exceed 1 | Must stay below 1 (table can fill) |
| Deletion | Simple (unlink node) | Needs tombstones |
| Cache locality | Poorer (pointer chasing) | Better (contiguous memory) |

**Conclusion:** Chaining tolerates high load factors better and is simpler to delete from, so its search time degrades gracefully. Linear probing is faster at low load factors because of cache locality, but primary clustering makes its search cost grow rapidly as the load factor approaches 1. In this lab, at load factor 1.00, chaining still searches in at most 2 nodes for the longest chain.
