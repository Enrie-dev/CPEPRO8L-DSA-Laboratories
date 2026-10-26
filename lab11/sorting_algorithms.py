"""Six sorting algorithms with comparison/movement counters.

Every function sorts a list IN PLACE (merge sort writes results back into the
input list) and returns a ``Counter`` describing the work done.  No built-in
sorting function is used.

Counter definitions
-------------------
comparisons : number of key-vs-key comparisons between data elements.
movements   : number of element writes/swaps into the list. A swap counts as 1.
"""


class Counter:
    """Tracks comparisons and data movements for one sort run."""

    __slots__ = ("comparisons", "movements")

    def __init__(self):
        self.comparisons = 0
        self.movements = 0

    def __repr__(self):
        return f"Counter(comparisons={self.comparisons}, movements={self.movements})"


# --------------------------------------------------------------------------
# Elementary sorts  (O(n^2) average/worst, O(1) auxiliary space)
# --------------------------------------------------------------------------
def bubble_sort(data):
    """Bubble sort with early exit when a pass makes no swap (stable)."""
    c = Counter()
    n = len(data)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            c.comparisons += 1
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                c.movements += 1
                swapped = True
        if not swapped:
            break
    return c


def selection_sort(data):
    """Selection sort: n-1 swaps at most, always ~n^2/2 comparisons (not stable)."""
    c = Counter()
    n = len(data)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            c.comparisons += 1
            if data[j] < data[smallest]:
                smallest = j
        if smallest != i:
            data[i], data[smallest] = data[smallest], data[i]
            c.movements += 1
    return c


def insertion_sort(data):
    """Insertion sort: shifts larger items right, O(n) on sorted input (stable)."""
    c = Counter()
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0:
            c.comparisons += 1
            if data[j] > key:
                data[j + 1] = data[j]
                c.movements += 1
                j -= 1
            else:
                break
        if j + 1 != i:
            data[j + 1] = key
            c.movements += 1
    return c


# --------------------------------------------------------------------------
# Advanced sorts
# --------------------------------------------------------------------------
def merge_sort(data):
    """Top-down merge sort (stable). Extra storage: one O(n) buffer, allocated once."""
    c = Counter()
    n = len(data)
    if n < 2:
        return c
    buffer = [None] * n

    def sort(lo, hi):  # sorts data[lo:hi]
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        # merge data[lo:mid] and data[mid:hi] through buffer
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            c.comparisons += 1
            if data[j] < data[i]:
                buffer[k] = data[j]
                j += 1
            else:
                buffer[k] = data[i]
                i += 1
            k += 1
        while i < mid:
            buffer[k] = data[i]
            i += 1
            k += 1
        while j < hi:
            buffer[k] = data[j]
            j += 1
            k += 1
        for k in range(lo, hi):
            data[k] = buffer[k]
        c.movements += 2 * (hi - lo)  # write to buffer + copy back

    sort(0, n)
    return c


def quick_sort(data):
    """Quick sort, in place (not stable).

    Pivot strategy: MEDIAN-OF-THREE (first, middle, last element) with a
    Hoare-style partition.  Median-of-three avoids the O(n^2) behaviour that a
    first/last-element pivot shows on already sorted or reverse-sorted input,
    and the Hoare partition stops on equal keys, which splits duplicate-heavy
    data evenly.  Recursion is applied to the smaller partition and the larger
    one is handled by looping, so stack depth is O(log n).
    """
    c = Counter()

    def median_of_three(lo, hi):
        mid = (lo + hi) // 2
        a, b, d = data[lo], data[mid], data[hi]
        c.comparisons += 3
        if a <= b:
            if b <= d:
                return b
            return d if a <= d else a
        if a <= d:
            return a
        return d if b <= d else b

    def sort(lo, hi):  # inclusive bounds
        while lo < hi:
            pivot = median_of_three(lo, hi)
            i, j = lo - 1, hi + 1
            while True:
                i += 1
                c.comparisons += 1
                while data[i] < pivot:
                    i += 1
                    c.comparisons += 1
                j -= 1
                c.comparisons += 1
                while data[j] > pivot:
                    j -= 1
                    c.comparisons += 1
                if i >= j:
                    break
                data[i], data[j] = data[j], data[i]
                c.movements += 1
            # partitions: [lo..j] and [j+1..hi]
            if j - lo < hi - (j + 1):
                sort(lo, j)
                lo = j + 1
            else:
                sort(j + 1, hi)
                hi = j

    sort(0, len(data) - 1)
    return c


def heap_sort(data):
    """Heap sort with an in-place max-heap (not stable, O(1) extra space)."""
    c = Counter()
    n = len(data)

    def sift_down(root, size):
        while True:
            child = 2 * root + 1
            if child >= size:
                return
            if child + 1 < size:
                c.comparisons += 1
                if data[child + 1] > data[child]:
                    child += 1
            c.comparisons += 1
            if data[child] > data[root]:
                data[root], data[child] = data[child], data[root]
                c.movements += 1
                root = child
            else:
                return

    for start in range(n // 2 - 1, -1, -1):  # build heap
        sift_down(start, n)
    for end in range(n - 1, 0, -1):          # extract max
        data[0], data[end] = data[end], data[0]
        c.movements += 1
        sift_down(0, end)
    return c


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}
