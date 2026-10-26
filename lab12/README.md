# Laboratory Activity No. 12: Graph Traversals and Shortest-Path Routing

**Course:** CPEPRO8L – Data Structures and Algorithms  |  **Term:** First Semester, AY 2026–2027

## Objectives
1. Represent unweighted and weighted graphs using adjacency lists.
2. Implement and trace Breadth-First Search and Depth-First Search.
3. Implement Dijkstra's single-source shortest-path algorithm with a priority queue (`heapq`).
4. Verify traversal and shortest-path results using hand traces and independent test cases.

## Environment
- Python 3.11+ (developed on 3.12), standard modules only: `collections`, `heapq`, `math` (plus `unittest`, `random`, `os` for tests/demo)
- Optional: `matplotlib` only to draw `output/graph_diagram.png`

## Execution Commands
```
python test_graph.py     # automated tests
python run_demo.py       # regenerates every file in output/
```

## Dataset and Design Decisions
- **Graph:** sample campus-routing graph (8 buildings, 9 undirected weighted edges, weights in meters). It includes a cycle, equal-cost alternative routes (Gate→Dorm) and an isolated vertex (`Annex`). *Replace `CAMPUS_EDGES`/`CAMPUS_VERTICES` in `graph.py` with the instructor-assigned graph if one is given.*
- **Direction:** undirected by default (`Graph(directed=True)` supported and tested).
- **Neighbor ordering rule:** neighbors are always processed in **alphabetical order** (`Graph.neighbors()` returns sorted names), making all traversals deterministic.
- **Tie-breaking in Dijkstra:** heap keyed by `(distance, vertex)`; a predecessor is replaced only on a strictly shorter distance, so the first-discovered equal-cost route is kept.
- **Validation:** `Dijkstra` raises `NegativeWeightError` before running; unknown vertices raise `KeyError`; non-numeric weights raise `TypeError`.

Edge table (undirected, 8 vertices, 9 edges)

| From | To | Weight |
|---|---|---:|
| Admin | Canteen | 7 |
| Admin | Gate | 2 |
| Admin | Library | 1 |
| Canteen | Gym | 2 |
| Canteen | Lab | 3 |
| Dorm | Gym | 3 |
| Dorm | Lab | 6 |
| Gate | Library | 4 |
| Lab | Library | 5 |

![Graph diagram](output/graph_diagram.png)

`verify_against_source()` confirms every source vertex/edge/weight (and its reverse for undirected) appears in the structure with nothing extra.

## Traversal Results (BFS / DFS)
Run from two start vertices: **Gate** and **Dorm**. Full traces are in `output/traversal_traces.md`; the Gate traces are shown here. The DFS trace uses an explicit stack with visited-marking on pop, so a vertex can sit on the stack more than once; later copies are skipped.

BFS trace from Gate

| Selected | Queue (front→back) | Visited | Order so far |
|---|---|---|---|
| - | [Gate] | {Gate} |  |
| Gate | [Admin, Library] | {Admin, Gate, Library} | Gate |
| Admin | [Library, Canteen] | {Admin, Canteen, Gate, Library} | Gate Admin |
| Library | [Canteen, Lab] | {Admin, Canteen, Gate, Lab, Library} | Gate Admin Library |
| Canteen | [Lab, Gym] | {Admin, Canteen, Gate, Gym, Lab, Library} | Gate Admin Library Canteen |
| Lab | [Gym, Dorm] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Library Canteen Lab |
| Gym | [Dorm] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Library Canteen Lab Gym |
| Dorm | [] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Library Canteen Lab Gym Dorm |

DFS trace from Gate

| Selected (popped) | Stack (bottom→top) | Visited | Order so far |
|---|---|---|---|
| - | [Gate] | {} |  |
| Gate | [Library, Admin] | {Gate} | Gate |
| Admin | [Library, Library, Canteen] | {Admin, Gate} | Gate Admin |
| Canteen | [Library, Library, Lab, Gym] | {Admin, Canteen, Gate} | Gate Admin Canteen |
| Gym | [Library, Library, Lab, Dorm] | {Admin, Canteen, Gate, Gym} | Gate Admin Canteen Gym |
| Dorm | [Library, Library, Lab, Lab] | {Admin, Canteen, Dorm, Gate, Gym} | Gate Admin Canteen Gym Dorm |
| Lab | [Library, Library, Lab, Library] | {Admin, Canteen, Dorm, Gate, Gym, Lab} | Gate Admin Canteen Gym Dorm Lab |
| Library | [Library, Library, Lab] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |
| Lab (already visited, skip) | [Library, Library] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |
| Library (already visited, skip) | [Library] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |
| Library (already visited, skip) | [] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |

Program results from Gate: BFS = Gate Admin Library Canteen Lab Gym Dorm ; DFS = Gate Admin Canteen Gym Dorm Lab Library

**Dorm results:** BFS = Dorm Gym Lab Canteen Library Admin Gate; DFS = Dorm Gym Canteen Admin Gate Library Lab.

**Manual check (Gate, BFS):** Gate's sorted neighbors are Admin, Library → queue [Admin, Library]. Admin adds Canteen; Library adds Lab; Canteen adds Gym; Lab adds Dorm. Order: Gate Admin Library Canteen Lab Gym Dorm, which matches the program. **Manual check (Gate, DFS):** Gate→Admin→Canteen→Gym→Dorm→Lab→Library, which matches the program (recursive and iterative versions agree from every start vertex).

## Dijkstra Shortest Paths
Routing table from Gate

| Target | Distance | Path |
|---|---:|---|
| Admin | 2 | Gate → Admin |
| Annex | unreachable | - |
| Canteen | 9 | Gate → Admin → Canteen |
| Dorm | 14 | Gate → Admin → Library → Lab → Dorm |
| Gate | 0 | Gate |
| Gym | 11 | Gate → Admin → Canteen → Gym |
| Lab | 8 | Gate → Admin → Library → Lab |
| Library | 3 | Gate → Admin → Library |

Routing table from Dorm

| Target | Distance | Path |
|---|---:|---|
| Admin | 12 | Dorm → Gym → Canteen → Admin |
| Annex | unreachable | - |
| Canteen | 5 | Dorm → Gym → Canteen |
| Dorm | 0 | Dorm |
| Gate | 14 | Dorm → Gym → Canteen → Admin → Gate |
| Gym | 3 | Dorm → Gym |
| Lab | 6 | Dorm → Lab |
| Library | 11 | Dorm → Lab → Library |

**Manual weight verification**
- Gate → Lab: Gate–Admin 2 + Admin–Library 1 + Library–Lab 5 = **8**; the alternative Gate–Library–Lab = 4 + 5 = 9 is longer.
- Gate → Gym: Gate–Admin 2 + Admin–Canteen 7 + Canteen–Gym 2 = **11**; via Lab it would be 8 + 3 + 2 = 13.
- Gate → Dorm: via Lab 8 + 6 = 14 and via Gym 11 + 3 = 14 are **equal**; the program keeps the first-found route (via Lab).
- `Annex` is isolated, so every other vertex is reported **unreachable** from it.

**Rejected / unsupported case**
Negative-weight graph (A→B 4, A→C 5, C→B −3)

Rejected: negative weight -3 on edge C->B: Dijkstra requires non-negative weights

True shortest A→B is 5 + (−3) = 2, but Dijkstra finalizes B at 4 first, so it would answer 4.

## BFS Tree vs Weighted Shortest-Path Tree (from Gate)
BFS tree vs Dijkstra tree from Gate

| Target | BFS path (min edges) | BFS hops | BFS weight | Dijkstra path (min weight) | Dijkstra weight | Same route? |
|---|---|---:|---:|---|---:|---|
| Admin | Gate → Admin | 1 | 2 | Gate → Admin | 2 | yes |
| Annex | unreachable | - | - | unreachable | - | - |
| Canteen | Gate → Admin → Canteen | 2 | 9 | Gate → Admin → Canteen | 9 | yes |
| Dorm | Gate → Library → Lab → Dorm | 3 | 15 | Gate → Admin → Library → Lab → Dorm | 14 | NO |
| Gate | Gate | 0 | 0 | Gate | 0 | yes |
| Gym | Gate → Admin → Canteen → Gym | 3 | 11 | Gate → Admin → Canteen → Gym | 11 | yes |
| Lab | Gate → Library → Lab | 2 | 9 | Gate → Admin → Library → Lab | 8 | NO |
| Library | Gate → Library | 1 | 4 | Gate → Admin → Library | 3 | NO |

BFS minimizes the number of edges, Dijkstra minimizes total weight. They agree for Admin, Canteen and Gym, but differ for Library, Lab and Dorm, where the direct edge Gate–Library (weight 4) has fewer hops than the detour through Admin (2 + 1 = 3) but is more costly.

## Expected vs Observed Tests
| # | Test case | Expected | Observed | Status |
|--:|---|---|---|---|
| 1 | Graph matches source data (vertices, edges, weights) | True | True | PASS |
| 2 | BFS from Gate | ['Gate', 'Admin', 'Library', 'Canteen', 'Lab', 'Gym', 'Dorm'] | ['Gate', 'Admin', 'Library', 'Canteen', 'Lab', 'Gym', 'Dorm'] | PASS |
| 3 | BFS from Dorm | ['Dorm', 'Gym', 'Lab', 'Canteen', 'Library', 'Admin', 'Gate'] | ['Dorm', 'Gym', 'Lab', 'Canteen', 'Library', 'Admin', 'Gate'] | PASS |
| 4 | DFS (recursive) from Gate | ['Gate', 'Admin', 'Canteen', 'Gym', 'Dorm', 'Lab', 'Library'] | ['Gate', 'Admin', 'Canteen', 'Gym', 'Dorm', 'Lab', 'Library'] | PASS |
| 5 | DFS (iterative) from Gate | ['Gate', 'Admin', 'Canteen', 'Gym', 'Dorm', 'Lab', 'Library'] | ['Gate', 'Admin', 'Canteen', 'Gym', 'Dorm', 'Lab', 'Library'] | PASS |
| 6 | DFS from Dorm | ['Dorm', 'Gym', 'Canteen', 'Admin', 'Gate', 'Library', 'Lab'] | ['Dorm', 'Gym', 'Canteen', 'Admin', 'Gate', 'Library', 'Lab'] | PASS |
| 7 | Isolated vertex: BFS from Annex | ['Annex'] | ['Annex'] | PASS |
| 8 | Isolated vertex: Annex unreachable from Gate (BFS) | None | None | PASS |
| 9 | Cycle: BFS terminates, no repeats | ['A', 'B', 'C'] | ['A', 'B', 'C'] | PASS |
| 10 | Cycle: DFS terminates, no repeats | ['A', 'B', 'C'] | ['A', 'B', 'C'] | PASS |
| 11 | Dijkstra Gate→Lab distance (2+1+5) | 8 | 8 | PASS |
| 12 | Dijkstra Gate→Lab path | ['Gate', 'Admin', 'Library', 'Lab'] | ['Gate', 'Admin', 'Library', 'Lab'] | PASS |
| 13 | Dijkstra Gate→Gym distance (2+7+2) | 11 | 11 | PASS |
| 14 | Dijkstra Gate→Library uses detour (2+1 < 4) | 3 | 3 | PASS |
| 15 | Equal-cost alternatives: Gate→Dorm distance (8+6 = 11+3) | 14 | 14 | PASS |
| 16 | Equal-cost alternatives: diamond S→T gives dist 3 and a valid path | (3, True) | (3, True) | PASS |
| 17 | Unreachable target: Gate→Annex distance | ∞ | ∞ | PASS |
| 18 | Unreachable target: path is None | None | None | PASS |
| 19 | Directed edge is one-way | True | True | PASS |
| 20 | Negative weight rejected by Dijkstra | NegativeWeightError | NegativeWeightError | PASS |
| 21 | Unknown start vertex rejected | KeyError | KeyError | PASS |
| 22 | Non-numeric weight rejected | TypeError | TypeError | PASS |

22/22 cases passed

`python test_graph.py` additionally passes: iterative/recursive DFS equality from every start, path cost = reported distance for every source/target pair, and a cross-check of Dijkstra against an independent Bellman-Ford on 200 random directed/undirected graphs.

## Complexity (adjacency list, V vertices, E edges)
| Algorithm | Time | Space |
|---|---|---|
| BFS | O(V + E) | O(V) (queue + visited + parent) |
| DFS | O(V + E) | O(V) (stack/recursion depth + visited) |
| Dijkstra (binary heap, lazy deletion) | O((V + E) log V) | O(V + E) for the heap in the worst case, O(V) for dist/prev |

## Guide Questions
**1. How does the queue make BFS behave differently from the DFS stack?**
A queue is first-in-first-out, so BFS finishes every vertex at distance *k* before any at *k+1*, exploring level by level. A stack (or recursion) is last-in-first-out, so DFS follows one branch as deep as possible before backtracking. From Gate, BFS visits the neighbors Admin and Library first; DFS goes Admin→Canteen→Gym→Dorm before returning.

**2. Why must neighbor order be defined before comparing traversal results?**
Several valid BFS/DFS orders exist for the same graph, and the order depends on which neighbor is processed first. Without a fixed rule (here: alphabetical), a hand trace and a program could differ without either being wrong, and results could not be reproduced or graded.

**3. Under what condition can BFS produce a shortest path, and what does it minimize?**
When every edge has the same cost (unweighted graph), BFS finds a path with the **minimum number of edges**. On weighted graphs it does not minimize weight, as shown by Gate→Lab (BFS weight 9 vs Dijkstra 8).

**4. Why is Dijkstra invalid for graphs with negative edge weights?**
Dijkstra finalizes a vertex when it is popped, assuming no later path can be shorter, which holds only if extending a path never decreases its cost. A negative edge breaks this. In the A→B 4, A→C 5, C→B −3 example, B is finalized at 4 although the true shortest is 2. The implementation therefore rejects such graphs.

**5. What is the benefit of storing predecessor information with distances?**
Distances alone give only the cost. The predecessor map lets the program reconstruct the actual route to any target by walking back from the target to the source, and shows unreachable vertices (no predecessor, distance ∞).

**6. How do adjacency lists affect complexity?**
Each vertex's neighbors are stored directly, so BFS/DFS look at each edge a constant number of times: O(V + E) instead of O(V²) for an adjacency matrix, which matters on sparse graphs. Dijkstra likewise relaxes each edge once, each costing a heap push of O(log V), giving O((V + E) log V).

**7. Which test case gave the strongest evidence that the routing implementation is correct?**
The randomized cross-check against an independent Bellman-Ford implementation (200 random graphs, directed and undirected, including unreachable vertices and zero-weight edges) agreeing on every distance. Among specific cases, Gate→Library (3, via the detour, instead of the direct edge 4) is the clearest evidence that the algorithm picks lower weight over fewer edges.

## Conclusion
The adjacency-list graph, BFS, DFS and Dijkstra all behave correctly: 22/22 tabulated cases and all automated tests pass, hand traces match program output, and invalid input (negative weights, unknown vertices, bad weight types) is rejected. BFS suits unweighted reachability and minimum-edge paths, DFS suits exhaustive exploration and reachability (it does not give shortest paths), and Dijkstra suits weighted routing with non-negative weights.

## Files Submitted
- `graph.py`, `traversals.py`, `dijkstra.py`, `test_graph.py`, `run_demo.py`
- `output/edge_table.md`, `output/graph_diagram.png`, `output/traversal_traces.md`, `output/routing_results.md`, `output/bfs_vs_dijkstra.md`, `output/invalid_input.md`, `output/test_report.md`
- `output_capture.txt` (console capture of `run_demo.py`)
- `README.md`
