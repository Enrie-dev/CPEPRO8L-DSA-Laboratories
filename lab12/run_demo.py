"""Generates all evidence files into ./output : edge table, diagram, traces,
routing tables, BFS-vs-Dijkstra comparison and the expected/observed test table.

Run: python run_demo.py
"""
import math
import os

from graph import build_campus_graph, verify_against_source
from traversals import bfs, dfs_recursive, bfs_trace, dfs_trace, path_from_parent
from dijkstra import dijkstra, routing_table, reconstruct_path, NegativeWeightError
from graph import Graph
from test_graph import CASES

OUT = "output"
os.makedirs(OUT, exist_ok=True)
g = build_campus_graph()
verify_against_source(g)


def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")
    print(f"--- {name} ---\n{text}\n")


write("edge_table.md", g.edge_table())

# Traversal results + hand-trace tables from two starting vertices
parts = []
for s in ("Gate", "Dorm"):
    parts.append(bfs_trace(g, s))
    parts.append(dfs_trace(g, s))
    parts.append(f"Program results from {s}: BFS = {' '.join(bfs(g, s)[0])} ; "
                 f"DFS = {' '.join(dfs_recursive(g, s)[0])}")
write("traversal_traces.md", "\n\n".join(parts))

# Routing tables
write("routing_results.md", "\n\n".join(routing_table(g, s) for s in ("Gate", "Dorm")))

# BFS tree vs Dijkstra tree
src = "Gate"
_, bparent = bfs(g, src)
dist, prev = dijkstra(g, src)
lines = [f"BFS tree vs Dijkstra tree from {src}", "",
         "| Target | BFS path (min edges) | BFS hops | BFS weight | Dijkstra path (min weight) | Dijkstra weight | Same route? |",
         "|---|---|---:|---:|---|---:|---|"]
for t in g.vertices():
    bp = path_from_parent(bparent, t)
    dp = reconstruct_path(prev, dist, src, t)
    if bp is None:
        lines.append(f"| {t} | unreachable | - | - | unreachable | - | - |")
        continue
    bw = sum(g.weight(a, b) for a, b in zip(bp, bp[1:]))
    lines.append(f"| {t} | {' → '.join(bp)} | {len(bp)-1} | {bw} | {' → '.join(dp)} | {dist[t]} | "
                 f"{'yes' if bp == dp else 'NO'} |")
write("bfs_vs_dijkstra.md", "\n".join(lines))

# Rejected case: negative weight
bad = Graph(directed=True)
bad.add_edge("A", "B", 4)
bad.add_edge("A", "C", 5)
bad.add_edge("C", "B", -3)
try:
    dijkstra(bad, "A")
    msg = "NOT rejected (bug)"
except NegativeWeightError as e:
    msg = f"Rejected: {e}"
write("invalid_input.md", f"Negative-weight graph (A→B 4, A→C 5, C→B −3)\n\n{msg}\n\n"
      "True shortest A→B is 5 + (−3) = 2, but Dijkstra finalizes B at 4 first, so it would answer 4.")

# Expected / observed pass-fail table
rows = ["| # | Test case | Expected | Observed | Status |", "|--:|---|---|---|---|"]
passed = 0
for i, (name, expected, observed) in enumerate(CASES, 1):
    obs = observed()
    ok = obs == expected
    passed += ok
    show = lambda x: "∞" if x == math.inf else str(x)
    rows.append(f"| {i} | {name} | {show(expected)} | {show(obs)} | {'PASS' if ok else 'FAIL'} |")
write("test_report.md", "\n".join(rows) + f"\n\n{passed}/{len(CASES)} cases passed")

# Diagram
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pos = {"Gate": (0, 1), "Admin": (1.5, 2), "Library": (1.5, 0), "Canteen": (3.5, 2),
           "Lab": (3.5, 0), "Gym": (5.5, 2), "Dorm": (5.5, 0), "Annex": (7.2, 1)}
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for u, v, w in g.edges():
        (x1, y1), (x2, y2) = pos[u], pos[v]
        ax.plot([x1, x2], [y1, y2], color="gray", zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.08, str(w), ha="center", color="darkred", fontsize=11,
                bbox=dict(fc="white", ec="none", pad=1))
    for v, (x, y) in pos.items():
        ax.scatter([x], [y], s=1700, color="#cfe3ff", edgecolor="navy", zorder=2)
        ax.text(x, y, v, ha="center", va="center", fontsize=9, zorder=3)
    ax.set_title("Sample campus graph (undirected, weights in meters)")
    ax.set_xlim(-0.8, 8); ax.set_ylim(-0.7, 2.7); ax.axis("off")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "graph_diagram.png"), dpi=150)
    print("--- graph_diagram.png written ---")
except ImportError:
    print("matplotlib not installed: diagram skipped (edge_table.md still produced)")
