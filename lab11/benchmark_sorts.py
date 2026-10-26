"""Controlled benchmark for the six sorting algorithms.

Fairness controls
-----------------
* Datasets are generated ONCE per (size, condition) from a fixed seed, so every
  algorithm sorts identical values.
* Every trial sorts a fresh copy (list.copy()); the copy is made OUTSIDE the
  timed region.
* Only the sort call is timed, with time.perf_counter().
* TRIALS timed runs per algorithm/condition; the MEDIAN is reported.
* Correctness is verified after each run (outside the timed region).
* Comparison/movement counts are recorded from a separate untimed-by-median
  run's counter (the counters are deterministic, so one value per cell).
* Quadratic algorithms are skipped for a size once any run of that
  algorithm/condition exceeds TIME_LIMIT seconds; the skip is recorded.

Run:  python benchmark_sorts.py
Output: results.csv, runtime_chart.png
"""
import csv
import random
import statistics
import time

from sorting_algorithms import ALGORITHMS

SIZES = [500, 1000, 2000, 4000]
CONDITIONS = ["random", "sorted", "reverse", "duplicates"]
TRIALS = 5
TIME_LIMIT = 20.0  # seconds per single run; larger sizes skipped after this
SEED = 2026
QUADRATIC = {"Bubble Sort", "Selection Sort", "Insertion Sort"}


def make_data(condition, n, rng):
    if condition == "random":
        return [rng.randint(0, n * 10) for _ in range(n)]
    if condition == "sorted":
        return list(range(n))
    if condition == "reverse":
        return list(range(n, 0, -1))
    if condition == "duplicates":  # only ~10 distinct values
        return [rng.randint(0, 9) for _ in range(n)]
    raise ValueError(condition)


def run_benchmark():
    rng = random.Random(SEED)
    datasets = {(c, n): make_data(c, n, rng) for n in SIZES for c in CONDITIONS}
    rows = []
    too_slow = set()  # (algorithm, condition) pairs that hit the time limit

    for n in SIZES:
        for cond in CONDITIONS:
            source = datasets[(cond, n)]
            expected = sorted(source)  # reference, outside timing
            for name, algo in ALGORITHMS.items():
                if (name, cond) in too_slow:
                    rows.append(dict(algorithm=name, condition=cond, size=n,
                                     median_s="", min_s="", max_s="",
                                     comparisons="", movements="",
                                     note=f"skipped: previous size exceeded {TIME_LIMIT}s limit"))
                    print(f"n={n:<5} {cond:<10} {name:<15} SKIPPED")
                    continue
                times = []
                counter = None
                for _ in range(TRIALS):
                    work = source.copy()          # fresh copy, not timed
                    start = time.perf_counter()
                    counter = algo(work)
                    elapsed = time.perf_counter() - start
                    assert work == expected, f"{name} failed on {cond} n={n}"
                    times.append(elapsed)
                    if elapsed > TIME_LIMIT:
                        break
                if max(times) > TIME_LIMIT and name in QUADRATIC:
                    too_slow.add((name, cond))
                rows.append(dict(algorithm=name, condition=cond, size=n,
                                 median_s=f"{statistics.median(times):.6f}",
                                 min_s=f"{min(times):.6f}",
                                 max_s=f"{max(times):.6f}",
                                 comparisons=counter.comparisons,
                                 movements=counter.movements, note=""))
                print(f"n={n:<5} {cond:<10} {name:<15} "
                      f"median={statistics.median(times):.5f}s "
                      f"cmp={counter.comparisons} mov={counter.movements}")
    return rows


def save_csv(rows, path="results.csv"):
    fields = ["algorithm", "condition", "size", "median_s", "min_s", "max_s",
              "comparisons", "movements", "note"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def save_chart(rows, path="runtime_chart.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for ax, cond in zip(axes.flat, CONDITIONS):
        for name in ALGORITHMS:
            pts = [(r["size"], float(r["median_s"])) for r in rows
                   if r["algorithm"] == name and r["condition"] == cond and r["median_s"] != ""]
            if pts:
                xs, ys = zip(*pts)
                ax.plot(xs, ys, marker="o", label=name)
        ax.set_title(f"{cond} data")
        ax.set_xlabel("input size n")
        ax.set_ylabel("median runtime (s)")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(True, which="both", alpha=0.3)
    axes[0][0].legend(fontsize=8)
    fig.suptitle(f"Sorting runtime growth (median of {TRIALS} trials, log-log)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)


if __name__ == "__main__":
    results = run_benchmark()
    save_csv(results)
    save_chart(results)
    print("\nWrote results.csv and runtime_chart.png")
