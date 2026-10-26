"""Dijkstra's single-source shortest paths using heapq."""
import heapq
import math


class NegativeWeightError(ValueError):
    """Raised when a graph with a negative edge weight is given to Dijkstra."""


def dijkstra(graph, source):
    """Return (dist, prev).

    dist[v] = shortest distance from source (math.inf if unreachable)
    prev[v] = predecessor of v on one shortest path (None for source/unreachable)

    Ties: the heap orders by (distance, vertex name) and a predecessor is only
    replaced on a STRICTLY shorter distance, so results are deterministic and the
    first-discovered equal-cost route is kept.
    """
    if source not in graph.adj:
        raise KeyError(f"unknown source vertex {source!r}")
    for u, v, w in graph.edges():
        if w < 0:
            raise NegativeWeightError(
                f"negative weight {w} on edge {u}->{v}: Dijkstra requires non-negative weights")

    dist = {v: math.inf for v in graph.adj}
    prev = {v: None for v in graph.adj}
    dist[source] = 0
    heap = [(0, source)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:                 # stale heap entry (lazy deletion)
            continue
        done.add(u)
        for v in graph.neighbors(u):
            nd = d + graph.weight(u, v)
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def reconstruct_path(prev, dist, source, target):
    """Path source→target as a list, or None if target is unreachable."""
    if dist[target] == math.inf:
        return None
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    path.reverse()
    assert path[0] == source
    return path


def routing_table(graph, source):
    """Markdown routing table with distance and path for every vertex."""
    dist, prev = dijkstra(graph, source)
    lines = [f"Routing table from {source}", "",
             "| Target | Distance | Path |", "|---|---:|---|"]
    for v in graph.vertices():
        p = reconstruct_path(prev, dist, source, v)
        if p is None:
            lines.append(f"| {v} | unreachable | - |")
        else:
            lines.append(f"| {v} | {dist[v]} | {' → '.join(p)} |")
    return "\n".join(lines)
