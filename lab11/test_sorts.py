"""Correctness tests for all six algorithms (run: python test_sorts.py)."""
import copy
import random
import unittest

from sorting_algorithms import ALGORITHMS


def make_datasets(seed=11):
    rng = random.Random(seed)
    return {
        "empty": [],
        "one item": [42],
        "two items": [2, 1],
        "all equal": [7] * 50,
        "duplicates": [rng.randint(0, 5) for _ in range(200)],
        "already sorted": list(range(100)),
        "reverse sorted": list(range(100, 0, -1)),
        "random": [rng.randint(-1000, 1000) for _ in range(300)],
        "negatives": [-5, 3, -1, 0, -5, 8, 3],
    }


class SortingTests(unittest.TestCase):
    def test_all_algorithms_all_datasets(self):
        for algo_name, algo in ALGORITHMS.items():
            for ds_name, ds in make_datasets().items():
                with self.subTest(algorithm=algo_name, dataset=ds_name):
                    data = copy.deepcopy(ds)
                    expected = sorted(ds)  # independent reference check only
                    algo(data)
                    self.assertEqual(data, expected)

    def test_counters_are_non_negative(self):
        for algo_name, algo in ALGORITHMS.items():
            with self.subTest(algorithm=algo_name):
                c = algo(make_datasets()["random"])
                self.assertGreaterEqual(c.comparisons, 0)
                self.assertGreaterEqual(c.movements, 0)

    def test_sorted_input_is_linear_for_bubble_and_insertion(self):
        data = list(range(100))
        self.assertEqual(ALGORITHMS["Bubble Sort"](data[:]).comparisons, 99)
        self.assertEqual(ALGORITHMS["Insertion Sort"](data[:]).comparisons, 99)

    def test_stable_algorithms(self):
        """Bubble, Insertion and Merge must keep equal keys in original order."""
        class Item:
            def __init__(self, key, tag):
                self.key, self.tag = key, tag
            def __lt__(self, o): return self.key < o.key
            def __gt__(self, o): return self.key > o.key
        for name in ("Bubble Sort", "Insertion Sort", "Merge Sort"):
            with self.subTest(algorithm=name):
                rng = random.Random(1)
                items = [Item(rng.randint(0, 4), i) for i in range(100)]
                ALGORITHMS[name](items)
                for a, b in zip(items, items[1:]):
                    if a.key == b.key:
                        self.assertLess(a.tag, b.tag)


if __name__ == "__main__":
    unittest.main(verbosity=2)
