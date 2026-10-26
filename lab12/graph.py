"""Adjacency-list graph supporting directed/undirected and weighted/unweighted use."""


class Graph:
    """Adjacency-list graph.

    adj[u] is a dict {v: weight}.  Neighbor order is DETERMINISTIC: neighbors()
    always returns vertices in sorted (alphabetical) order, which is the
    ordering rule used by every traversal in this project.
    Unweighted edges are stored with weight 1.
    """

    def __init__(self, directed=False):
        self.directed = directed
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = {}

    def add_edge(self, u, v, weight=1):
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise TypeError(f"weight must be a number, got {weight!r}")
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u][v] = weight
        if not self.directed:
            self.adj[v][u] = weight

    def vertices(self):
        return sorted(self.adj)

    def neighbors(self, v):
        """Neighbors of v in sorted order."""
        if v not in self.adj:
            raise KeyError(f"unknown vertex {v!r}")
        return sorted(self.adj[v])

    def weight(self, u, v):
        return self.adj[u][v]

    def edges(self):
        """Edge list as sorted (u, v, w); undirected edges listed once (u < v)."""
        out = []
        for u in self.adj:
            for v, w in self.adj[u].items():
                if self.directed or u <= v:
                    out.append((u, v, w))
        return sorted(out)

    def has_negative_weight(self):
        return any(w < 0 for _, _, w in self.edges())

    def edge_table(self):
        """Markdown edge table (used as the 'labeled edge table' deliverable)."""
        kind = "directed" if self.directed else "undirected"
        lines = [f"Edge table ({kind}, {len(self.adj)} vertices, {len(self.edges())} edges)", "",
                 "| From | To | Weight |", "|---|---|---:|"]
        lines += [f"| {u} | {v} | {w} |" for u, v, w in self.edges()]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Sample dataset. REPLACE with the instructor-assigned graph if one is given.
# ---------------------------------------------------------------------------
CAMPUS_EDGES = [
    ("Gate", "Admin", 2), ("Gate", "Library", 4), ("Admin", "Library", 1),
    ("Admin", "Canteen", 7), ("Library", "Lab", 5), ("Canteen", "Lab", 3),
    ("Canteen", "Gym", 2), ("Lab", "Dorm", 6), ("Gym", "Dorm", 3),
]
CAMPUS_VERTICES = ["Admin", "Annex", "Canteen", "Dorm", "Gate", "Gym", "Lab", "Library"]


def build_campus_graph(directed=False):
    g = Graph(directed=directed)
    for v in CAMPUS_VERTICES:        # includes isolated vertex 'Annex'
        g.add_vertex(v)
    for u, v, w in CAMPUS_EDGES:
        g.add_edge(u, v, w)
    return g


def verify_against_source(g, vertices=CAMPUS_VERTICES, edges=CAMPUS_EDGES):
    """Task A.6: every source vertex/edge must appear in the structure (and nothing extra)."""
    assert set(g.adj) == set(vertices), "vertex set mismatch"
    for u, v, w in edges:
        assert g.adj[u].get(v) == w, f"edge {u}->{v} missing or wrong weight"
        if not g.directed:
            assert g.adj[v].get(u) == w, f"reverse edge {v}->{u} missing"
    expected = len(edges) * (1 if g.directed else 2)
    assert sum(len(n) for n in g.adj.values()) == expected, "unexpected extra edges"
    return True
