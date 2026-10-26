"""Automated tests. Run: python test_graph.py

CASES is a list of (name, expected, observed_callable) used both by unittest and by
run_demo.py to build the expected/observed pass/fail table.
Expected values were derived BY HAND (see hand traces in README) or by direct
weight summation, not copied from program output.
"""
import math
import random
import unittest

from graph import Graph, build_campus_graph, verify_against_source
from traversals import bfs, dfs_recursive, dfs_iterative, path_from_parent
from dijkstra import dijkstra, reconstruct_path, NegativeWeightError

G = build_campus_graph()


def path_cost(g, path):
    return sum(g.weight(a, b) for a, b in zip(path, path[1:]))


def neg_weight_rejected():
    g = Graph(directed=True)
    g.add_edge("A", "B", 4)
    g.add_edge("B", "C", -2)
    try:
        dijkstra(g, "A")
    except NegativeWeightError:
        return "NegativeWeightError"
    return "no error"


def cycle_graph_bfs():
    g = Graph()
    for u, v in [("A", "B"), ("B", "C"), ("C", "A")]:
        g.add_edge(u, v)
    return bfs(g, "A")[0]


def cycle_graph_dfs():
    g = Graph()
    for u, v in [("A", "B"), ("B", "C"), ("C", "A")]:
        g.add_edge(u, v)
    return dfs_recursive(g, "A")[0]


def diamond_tie():
    g = Graph()
    for u, v, w in [("S", "A", 1), ("S", "B", 1), ("A", "T", 2), ("B", "T", 2)]:
        g.add_edge(u, v, w)
    dist, prev = dijkstra(g, "S")
    p = reconstruct_path(prev, dist, "S", "T")
    return (dist["T"], p in (["S", "A", "T"], ["S", "B", "T"]))


def directed_one_way():
    g = Graph(directed=True)
    g.add_edge("A", "B", 1)
    dist, prev = dijkstra(g, "B")
    return dist["A"] == math.inf


def unknown_vertex():
    try:
        bfs(G, "Nowhere")
    except KeyError:
        return "KeyError"
    return "no error"


def bad_weight_type():
    try:
        Graph().add_edge("A", "B", "heavy")
    except TypeError:
        return "TypeError"
    return "no error"


CASES = [
    ("Graph matches source data (vertices, edges, weights)", True, lambda: verify_against_source(G)),
    ("BFS from Gate", ["Gate", "Admin", "Library", "Canteen", "Lab", "Gym", "Dorm"], lambda: bfs(G, "Gate")[0]),
    ("BFS from Dorm", ["Dorm", "Gym", "Lab", "Canteen", "Library", "Admin", "Gate"], lambda: bfs(G, "Dorm")[0]),
    ("DFS (recursive) from Gate", ["Gate", "Admin", "Canteen", "Gym", "Dorm", "Lab", "Library"], lambda: dfs_recursive(G, "Gate")[0]),
    ("DFS (iterative) from Gate", ["Gate", "Admin", "Canteen", "Gym", "Dorm", "Lab", "Library"], lambda: dfs_iterative(G, "Gate")[0]),
    ("DFS from Dorm", ["Dorm", "Gym", "Canteen", "Admin", "Gate", "Library", "Lab"], lambda: dfs_recursive(G, "Dorm")[0]),
    ("Isolated vertex: BFS from Annex", ["Annex"], lambda: bfs(G, "Annex")[0]),
    ("Isolated vertex: Annex unreachable from Gate (BFS)", None, lambda: path_from_parent(bfs(G, "Gate")[1], "Annex")),
    ("Cycle: BFS terminates, no repeats", ["A", "B", "C"], cycle_graph_bfs),
    ("Cycle: DFS terminates, no repeats", ["A", "B", "C"], cycle_graph_dfs),
    ("Dijkstra Gate→Lab distance (2+1+5)", 8, lambda: dijkstra(G, "Gate")[0]["Lab"]),
    ("Dijkstra Gate→Lab path", ["Gate", "Admin", "Library", "Lab"],
     lambda: reconstruct_path(*reversed(dijkstra(G, "Gate")), "Gate", "Lab")),
    ("Dijkstra Gate→Gym distance (2+7+2)", 11, lambda: dijkstra(G, "Gate")[0]["Gym"]),
    ("Dijkstra Gate→Library uses detour (2+1 < 4)", 3, lambda: dijkstra(G, "Gate")[0]["Library"]),
    ("Equal-cost alternatives: Gate→Dorm distance (8+6 = 11+3)", 14, lambda: dijkstra(G, "Gate")[0]["Dorm"]),
    ("Equal-cost alternatives: diamond S→T gives dist 3 and a valid path", (3, True), diamond_tie),
    ("Unreachable target: Gate→Annex distance", math.inf, lambda: dijkstra(G, "Gate")[0]["Annex"]),
    ("Unreachable target: path is None", None,
     lambda: reconstruct_path(*reversed(dijkstra(G, "Gate")), "Gate", "Annex")),
    ("Directed edge is one-way", True, directed_one_way),
    ("Negative weight rejected by Dijkstra", "NegativeWeightError", neg_weight_rejected),
    ("Unknown start vertex rejected", "KeyError", unknown_vertex),
    ("Non-numeric weight rejected", "TypeError", bad_weight_type),
]


def bellman_ford(g, source):
    """Independent reference implementation used only to cross-check Dijkstra."""
    dist = {v: math.inf for v in g.adj}
    dist[source] = 0
    for _ in range(len(g.adj) - 1):
        for u in g.adj:
            for v, w in g.adj[u].items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    return dist


class RoutingTests(unittest.TestCase):
    def test_cases(self):
        for name, expected, observed in CASES:
            with self.subTest(case=name):
                self.assertEqual(observed(), expected)

    def test_dfs_recursive_equals_iterative_everywhere(self):
        for s in G.vertices():
            self.assertEqual(dfs_recursive(G, s)[0], dfs_iterative(G, s)[0])

    def test_path_costs_match_distances(self):
        for s in G.vertices():
            dist, prev = dijkstra(G, s)
            for t in G.vertices():
                p = reconstruct_path(prev, dist, s, t)
                if p is not None:
                    self.assertEqual(path_cost(G, p), dist[t])

    def test_dijkstra_matches_bellman_ford_on_random_graphs(self):
        rng = random.Random(12)
        for trial in range(200):
            n = rng.randint(2, 12)
            g = Graph(directed=rng.random() < 0.5)
            for v in range(n):
                g.add_vertex(f"v{v:02d}")
            for _ in range(rng.randint(0, n * 3)):
                g.add_edge(f"v{rng.randrange(n):02d}", f"v{rng.randrange(n):02d}", rng.randint(0, 9))
            src = f"v{rng.randrange(n):02d}"
            self.assertEqual(dijkstra(g, src)[0], bellman_ford(g, src), f"trial {trial}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
