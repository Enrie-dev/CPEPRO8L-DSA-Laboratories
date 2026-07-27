# Laboratory Activity No. 1 — Python Object References and Asymptotic Complexity Profiling

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## 1. Objectives

At the end of this activity, the student is able to:

1. Differentiate between mutable and immutable object references using the `id()` function.
2. Demonstrate how variable assignment copies references, not data, causing side effects.
3. Write a profiling program using Python's `time` module to measure execution time.
4. Compare microsecond measurements to verify O(1), O(n), and O(n²) growth curves.

## 2. Repository Contents

| File | Description |
|---|---|
| `task1_references.py` | Demonstrates reference sharing and mutation between two variables pointing at the same list object. |
| `task2_profiling.py` | Benchmarks a constant-time, linear-time, and quadratic-time function across increasing input sizes. |
| `README.md` | This documentation file. |

Both scripts were run with Python 3 in a Linux sandbox environment; the traces below are the actual console output.

## 3. Task 1 — Execution & Output

Script: `task1_references.py`

```
--- TASK 1: OBJECT ID COMPARISON ---
Address of list_a (id): 140142128925504
Address of list_b (id): 140142128925504
Are list_a and list_b pointing to the same object? True

After appending 40 to list_b:
list_a: [10, 20, 30, 40]
list_b: [10, 20, 30, 40]

After reassigning list_b = [100, 200]:
Address of list_a (id): 140142128925504
Address of list_b (id): 140142124507776
list_a: [10, 20, 30, 40]
list_b: [100, 200]
Are list_a and list_b pointing to the same object now? False
```

(Exact numeric addresses will differ on every machine and every run — the CPython memory allocator assigns them dynamically — but the *pattern* is always the same: identical ids before reassignment, differing ids after.)

### Analysis Questions

**1. Why did the value of `list_a` change when you appended a number to `list_b`?**

`list_b = list_a` does not create a new list — it copies the *reference* (the memory address) into a second variable name. Both `list_a` and `list_b` are just labels pointing at the same underlying `list` object, confirmed by `id(list_a) == id(list_b)` and `list_a is list_b` returning `True`. Because lists are mutable, calling `list_b.append(40)` mutates the one object that both names refer to. Since there is only ever one object in memory, the change is visible through either name.

**2. What happens to the memory reference if you assign a new list to `list_b` using `list_b = [100, 200]`? Explain using the output of `id()`.**

`list_b = [100, 200]` does not mutate the existing object — it creates a brand-new list object in a different memory location and rebinds the name `list_b` to point at it. This is confirmed in the trace: after reassignment, `id(list_a)` stays `140142128925504` (unchanged) while `id(list_b)` becomes `140142124507776` (a new address), and `list_a is list_b` now evaluates to `False`. `list_a` still points to the original, mutated object `[10, 20, 30, 40]`, completely unaffected by what `list_b` is now bound to. This is the core distinction between *mutating* an object (affects every reference to it) and *reassigning* a name (only affects that one label).

## 4. Task 2 — Execution & Output

Script: `task2_profiling.py`

```
--- Benchmarking N = 100 ---
Constant time: 1.82 us
Linear time:   6.55 us
Quadratic time: 801.47 us

--- Benchmarking N = 500 ---
Constant time: 1.66 us
Linear time:   19.91 us
Quadratic time: 48479.07 us

--- Benchmarking N = 1000 ---
Constant time: 2.55 us
Linear time:   34.81 us
Quadratic time: 84698.40 us

--- Benchmarking N = 5000 ---
Constant time: 4.23 us
Linear time:   134.91 us
Quadratic time: 1589250.59 us

--- Benchmarking N = 10000 ---
Constant time: 4.44 us
Linear time:   244.32 us
Quadratic time: SKIPPED (too slow)
```

### Comparative Table

| N | O(1) — constant_time_check (μs) | O(n) — linear_time_sum (μs) | O(n²) — quadratic_time_pairs (μs) |
|---:|---:|---:|---:|
| 100 | 1.82 | 6.55 | 801.47 |
| 500 | 1.66 | 19.91 | 48,479.07 |
| 1,000 | 2.55 | 34.81 | 84,698.40 |
| 5,000 | 4.23 | 134.91 | 1,589,250.59 |
| 10,000 | 4.44 | 244.32 | SKIPPED (too slow) |

*(Raw microsecond values will vary slightly run-to-run and machine-to-machine due to CPU load, caching, and JIT/interpreter warm-up — but the growth pattern between columns is consistent and reproducible.)*

### Observation: How does the Quadratic function scale compared to the Linear function as N increases?

- Going from N=100 to N=1,000 (10×), the **linear** function's time grows about 5–6×, staying roughly proportional to N — a doubling of input size roughly doubles the work, consistent with O(n).
- Over the same range, the **quadratic** function's time grows over 100×, consistent with O(n²): a 10× increase in N produces roughly a 10² = 100× increase in runtime.
- At N=5,000, `quadratic_time_pairs` took about **1.59 seconds**, while `linear_time_sum` finished in about **135 microseconds** — over 11,000 times faster — despite doing "only" 5,000× less conceptual work in a mathematical sense; the disparity is precisely what O(n) vs O(n²) predicts.
- The **constant-time** function stayed essentially flat (1.6–4.4 μs) across every N, confirming it does the same fixed amount of work (return the first element) regardless of input size.
- N=10,000 was skipped for the quadratic function per the lab hint, since 100,000,000 inner-loop iterations would take on the order of tens of seconds — impractical for a quick benchmark run, and a real demonstration of why O(n²) algorithms are avoided on large inputs in practice.

## 5. Conclusions

**Why understanding object references is crucial in Python:**

Because Python variables are labels rather than boxes that hold data directly, assignment (`b = a`) for a mutable object like a list, dictionary, or set does not create an independent copy — it creates a second name pointing at the *same* object. Code that assumes `b = a` gives it a "safe" working copy will introduce subtle bugs: mutating `b` silently corrupts `a` too, because there was only ever one object. This matters enormously when building data structures such as linked lists, stacks, and trees, where nodes routinely hold references to other nodes. Accidentally aliasing two node references instead of creating a genuinely new node can corrupt an entire structure. Recognizing when a "copy" is really just a shared reference is a prerequisite for writing correct code with these structures, and knowing when to use `copy()`, `deepcopy()`, or explicit reconstruction to avoid aliasing bugs.

**How Big-O notation translates to actual execution speedups:**

Big-O notation is a mathematical abstraction that describes how an algorithm's cost grows *relative to input size*, ignoring constant factors and hardware specifics. The benchmark data makes that abstraction concrete: the O(1) function's runtime barely moved across a 100× range of input sizes, the O(n) function's runtime scaled roughly in step with N, and the O(n²) function's runtime exploded far faster than N itself — turning a sub-millisecond operation at N=100 into a 1.5-second operation at N=5,000. In practice, this is exactly why algorithm selection matters more than micro-optimizing constant factors: no amount of low-level tuning of a quadratic algorithm rescues it from being outperformed by an unoptimized linear one once N grows large enough. Big-O is what lets a developer *predict* that outcome before ever running the code — the profiling numbers here simply confirm the prediction empirically.
