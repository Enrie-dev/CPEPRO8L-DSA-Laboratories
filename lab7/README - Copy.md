# Laboratory Activity No. 7 — Recursion Tracing & Binary Search

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## Objectives

1. Understand recursive execution, base cases, and call nesting.
2. Code and test recursive Binary Search.
3. Compare iterative and recursive space complexities.

## Description

This repository implements `recursive_binary_search(arr, low, high, target)` in
`lab7_recursive_search.py`. The array is sorted, and at each call the function
checks the midpoint of the current `[low, high]` window:

- **Base case:** if `low > high`, the search window is empty, so the target
  is not present and the function returns `-1`.
- If `arr[mid] == target`, the index `mid` is returned.
- If `arr[mid] > target`, the function recurses on the **left half**
  (`high = mid - 1`).
- If `arr[mid] < target`, the function recurses on the **right half**
  (`low = mid + 1`).

A `trace=True` flag was added to the function purely for this report — it
prints each call's `(low, high, target)` arguments, indented by recursion
depth, so the stack behavior is visible without a debugger.

## Execution & Output

Test data: `[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]`

Console capture from running `python3 lab7_recursive_search.py`:

```
Searching for 23 in [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
------------------------------------------------------------
Call(low=0, high=9, target=23) -> mid=4, arr[mid]=16
  arr[mid] < target -> recurse RIGHT (low=5, high=9)
  Call(low=5, high=9, target=23) -> mid=7, arr[mid]=56
    arr[mid] > target -> recurse LEFT (low=5, high=6)
    Call(low=5, high=6, target=23) -> mid=5, arr[mid]=23
      arr[mid] == target -> FOUND at index 5
------------------------------------------------------------
Element found at index: 5

Searching for 56 in [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
------------------------------------------------------------
Call(low=0, high=9, target=56) -> mid=4, arr[mid]=16
  arr[mid] < target -> recurse RIGHT (low=5, high=9)
  Call(low=5, high=9, target=56) -> mid=7, arr[mid]=56
    arr[mid] == target -> FOUND at index 7
------------------------------------------------------------
Element found at index: 7
```

### Profiling table — search for 56

| Call # | Depth | low | high | mid | arr[mid] | Decision                      |
|--------|-------|-----|------|-----|----------|--------------------------------|
| 1      | 0     | 0   | 9    | 4   | 16       | 16 < 56 → recurse right        |
| 2      | 1     | 5   | 9    | 7   | 56       | arr[mid] == target → return 7  |

Total recursive calls: **2**. Maximum stack depth: **2**.

## Report Analysis Questions

### 1. Execution stack trace diagram — searching for 56

```
Call Stack (grows downward as calls are made, unwinds upward as they return)

┌───────────────────────────────────────────────┐
│ recursive_binary_search(arr, 0, 9, 56)         │  <- initial call
│   low=0, high=9, mid=4, arr[mid]=16            │
│   16 < 56  →  recurse RIGHT                    │
└───────────────────────┬─────────────────────────┘
                         │ calls
                         ▼
┌───────────────────────────────────────────────┐
│ recursive_binary_search(arr, 5, 9, 56)         │  <- 2nd call (top of stack)
│   low=5, high=9, mid=7, arr[mid]=56            │
│   arr[mid] == target  →  return 7              │
└───────────────────────────────────────────────┘
                         │ returns 7
                         ▼
        Call 1 receives 7, returns 7 to main
```

Only two stack frames are ever created for this search: the array has 10
elements, and binary search halves the window on every call, so it takes
at most ⌈log₂(10)⌉ = 4 calls in the worst case — this particular search
resolves in 2 because the target is found on the second call.

### 2. Why missing base cases lead to stack overflow errors

A base case is the condition that stops the recursion. In this function,
the base case is `low > high`, which signals that the search window has
been exhausted and there is nowhere left to look.

If that check were removed (or written incorrectly), the function would
keep computing a `mid` and calling itself again even after `low` and `high`
crossed — and since the window would no longer be shrinking toward a valid
range, the recursion would never terminate. Every call to
`recursive_binary_search` pushes a **new stack frame** onto the program's
call stack to hold that call's local variables (`low`, `high`, `mid`) and
its return address. Without a base case to stop the calls, frames keep
being pushed and never popped, and the call stack — which has a fixed,
finite size set by the operating system/runtime — eventually runs out of
space. At that point the program raises a **stack overflow** error
(in Python, a `RecursionError: maximum recursion depth exceeded`),
because there is no more memory available to allocate additional frames.

In short: the base case bounds the depth of recursion; without it, depth
grows unboundedly and the finite call stack is exhausted.

## Files

- `lab7_recursive_search.py` — recursive binary search implementation and trace demo
- `README.md` — this file
