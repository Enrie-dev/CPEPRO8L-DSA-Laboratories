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
