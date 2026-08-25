# Laboratory Activity No. 6 — Circular Queue Buffer Implementation

**Course Code:** CPEPRO8L — Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## Objectives

1. Implement a fixed-capacity Circular Queue from scratch.
2. Understand index-wrapping mathematical calculations (`(tail + 1) % capacity`).
3. Solve buffer overflow and underflow conditions.

## Files

- `lab6_circular_queue.py` — contains the `CircularQueue` class (`enqueue`, `dequeue`, `is_full`, `is_empty`, `display`), plus a test driver in `__main__`.

## Execution & Output

Run with:

```
python3 lab6_circular_queue.py
```

Console output (required test case):

```
Dequeued: 1
Queue array: [None, 2, 3, 4, None] | Head: 1 | Tail: 4
```

This matches the expected result exactly (`Dequeued: 1`).

## Report Analysis Questions

**1. Record queue states during a series of 10 enqueues and dequeues.**

Trace of a `CircularQueue(5)` through 10 operations (7 enqueues, 3 dequeues):

| # | Operation | Result | Queue array | Head | Tail |
|---|---|---|---|---|---|
| 1 | `enqueue(10)` | — | `[10, None, None, None, None]` | 0 | 1 |
| 2 | `enqueue(20)` | — | `[10, 20, None, None, None]` | 0 | 2 |
| 3 | `enqueue(30)` | — | `[10, 20, 30, None, None]` | 0 | 3 |
| 4 | `dequeue()` | `10` | `[None, 20, 30, None, None]` | 1 | 3 |
| 5 | `enqueue(40)` | — | `[None, 20, 30, 40, None]` | 1 | 4 |
| 6 | `enqueue(50)` | — | `[None, 20, 30, 40, 50]` | 1 | **0** |
| 7 | `enqueue(60)` | — | `[60, 20, 30, 40, 50]` | 1 | 1 |
| 8 | `dequeue()` | `20` | `[60, None, 30, 40, 50]` | 2 | 1 |
| 9 | `enqueue(70)` | — | `[60, 70, 30, 40, 50]` | 2 | 2 |
| 10 | `enqueue(80)` | **Overflow** | `[60, 70, 30, 40, 50]` | 2 | 2 |

At step 6, `tail` wraps from 4 back to 0 (`(4 + 1) % 5 = 0`), which is the circular behavior the array replaces a plain queue with. By step 10 the queue holds 5 live elements (`60, 70, 30, 40, 50`) — its full capacity — so `enqueue(80)` correctly triggers the overflow branch instead of silently overwriting data or crashing.

**2. Explain the purpose of using the `%` (modulo) operator in index calculations.**

In an ordinary array-backed queue, `head` and `tail` only ever increase, so once `tail` reaches the end of the array it cannot advance further even though slots freed up by earlier dequeues sit unused at the front — this is the "capacity leakage" the lab introduction describes. The modulo operator solves this by wrapping an index back to `0` the instant it would run past the last valid slot: `(tail + 1) % capacity` and `(head + 1) % capacity` both cycle through `0, 1, 2, ..., capacity-1, 0, 1, ...` indefinitely instead of growing without bound. This turns the fixed-size array into a logically circular buffer, letting the queue reuse freed slots at the front as soon as `tail` wraps around — exactly what happened at step 6 above, where `tail` moved from index 4 to index 0 to reuse the slot vacated by an earlier dequeue.
