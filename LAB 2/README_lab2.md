# Laboratory Activity No. 2 — Dynamic Array Builder & Capacity Allocation

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## 1. Objectives

At the end of this activity, the student is able to:

1. Implement a custom dynamic array class from scratch using Python's `ctypes` module.
2. Understand capacity scaling, memory doubling, and the cost of element copying.
3. Observe how index search works in O(1) constant time complexity.

## 2. Repository Contents

| File | Description |
|---|---|
| `lab2_dynamic_array.py` | Custom `DynamicArray` class built on `ctypes.py_object` arrays, with completed `__getitem__`, `append`, and `_resize` methods, plus a test driver. |
| `README.md` | This documentation file. |

The script was run with Python 3 in a Linux sandbox environment; the traces below are the actual console output.

## 3. Implementation Notes

The three `TODO` sections were completed as follows:

- **`__getitem__(index)`** — validates `0 <= index < self.size` and raises `IndexError` otherwise, then returns `self.array[index]`. Because `ctypes` arrays support direct indexed access, this lookup is a single memory-offset calculation regardless of array size — O(1).
- **`append(element)`** — checks whether `size == capacity`; if the array is full, it calls `_resize(2 * self.capacity)` to double the capacity *before* inserting. It then stores the element at `self.array[self.size]` and increments `self.size`.
- **`_resize(new_capacity)`** — prints a trace line showing the capacity change, allocates a new `ctypes` array of `new_capacity` slots via `_make_array`, copies all `self.size` existing elements into it one by one, then reassigns `self.array` and `self.capacity` to the new array/value.

## 4. Execution & Output

Script: `lab2_dynamic_array.py`

```
Appending 0 | Size: 1 | Capacity: 1 | Element at index 0: 0
  [RESIZE] size=1 hit capacity=1 -> allocating new capacity=2, copying 1 elements
Appending 1 | Size: 2 | Capacity: 2 | Element at index 1: 1
  [RESIZE] size=2 hit capacity=2 -> allocating new capacity=4, copying 2 elements
Appending 2 | Size: 3 | Capacity: 4 | Element at index 2: 2
Appending 3 | Size: 4 | Capacity: 4 | Element at index 3: 3
  [RESIZE] size=4 hit capacity=4 -> allocating new capacity=8, copying 4 elements
Appending 4 | Size: 5 | Capacity: 8 | Element at index 4: 4
Appending 5 | Size: 6 | Capacity: 8 | Element at index 5: 5
Appending 6 | Size: 7 | Capacity: 8 | Element at index 6: 6
Appending 7 | Size: 8 | Capacity: 8 | Element at index 7: 7
  [RESIZE] size=8 hit capacity=8 -> allocating new capacity=16, copying 8 elements
Appending 8 | Size: 9 | Capacity: 16 | Element at index 8: 8
Appending 9 | Size: 10 | Capacity: 16 | Element at index 9: 9
```

The `[RESIZE]` lines were added as the "print capacity change trace" step required by `_resize`; they only appear on the append calls that actually trigger a resize, so the growth pattern is visible directly in the log.

### Bonus: IndexError Validation Check

To confirm the `__getitem__` bounds check works, the class was also exercised with out-of-range indices after appending 5 elements (`0, 10, 20, 30, 40`):

```
  [RESIZE] size=1 hit capacity=1 -> allocating new capacity=2, copying 1 elements
  [RESIZE] size=2 hit capacity=2 -> allocating new capacity=4, copying 2 elements
  [RESIZE] size=4 hit capacity=4 -> allocating new capacity=8, copying 4 elements
Caught expected error: Index 10 out of bounds for size 5
Caught expected error: Index -1 out of bounds for size 5
```

Both an index past the end (`10`) and a negative index (`-1`) correctly raise `IndexError`, confirming the bounds check guards against invalid access in both directions.

## 5. Capacity Resize Table

| Append Call (i) | Size Before Append | Capacity Before Append | Resize Triggered? | New Capacity After |
|---:|---:|---:|:---:|---:|
| 0 | 0 | 1 | Yes (size hit capacity) | 2 |
| 1 | 1 | 2 | Yes | 4 |
| 2 | 2 | 4 | No | 4 |
| 3 | 3 | 4 | No | 4 |
| 4 | 4 | 4 | Yes | 8 |
| 5 | 5 | 8 | No | 8 |
| 6 | 6 | 8 | No | 8 |
| 7 | 7 | 8 | Yes | 16 |
| 8 | 8 | 16 | No | 16 |
| 9 | 9 | 16 | No | 16 |

**Exact sizes at which a resize occurred:** size **1**, size **2**, size **4**, and size **8** — i.e. every time `size` about to be appended equals the current `capacity`. This confirms the doubling schedule: capacity moves **1 → 2 → 4 → 8 → 16**, each resize triggering exactly when the array is completely full (`size == capacity`), which is the classic amortized-doubling growth pattern used by `std::vector` and CPython's own list implementation.

## 6. Analysis Questions

**Run the script and record the exact sizes where capacity resizes occur.**

Resizes occurred right before inserting the element that would have made `size` exceed `capacity` — concretely, when `size` was **1, 2, 4, and 8** (i.e., appending the 2nd, 3rd, 5th, and 9th elements each triggered a resize). Capacity doubled each time: 1 → 2 → 4 → 8 → 16. Once capacity reached 16, no further resize was needed for the remaining appends up to 10 elements, since 10 elements comfortably fit in a capacity-16 array.

**Explain why the dynamic array copies elements during resize. What is the time complexity of a single resize operation?**

A `ctypes` array (like a C array or Python's underlying list buffer) is a single contiguous block of memory whose size is fixed at allocation time — it cannot simply be "extended in place" without risking overwriting whatever memory happens to sit immediately after it. To grow the array, the implementation must request a brand-new, larger contiguous block from the memory allocator. That new block is a completely separate region of memory with no data in it, so every existing element has to be copied over from the old block into the new one before the old block can be discarded (and before any new elements can be appended). This copying step is exactly what the resize trace lines above show happening on each resize.

A single resize operation copies all `n` currently-stored elements, so it costs **O(n)** time in the worst case — linear in the number of elements at the moment of resizing. However, because capacity *doubles* rather than growing by a fixed amount, resizes become exponentially less frequent as the array grows (they only happen at sizes 1, 2, 4, 8, 16, 32, ...). When the cost of all resizes is spread out ("amortized") over a sequence of n `append` calls, the *average* cost per `append` works out to O(1) — this is the standard amortized-constant-time argument for dynamic arrays. It's why `append` on a Python `list` (or `push_back` on a C++ `std::vector`) is described as O(1) amortized, even though any *individual* append that happens to trigger a resize actually costs O(n) in that moment.
