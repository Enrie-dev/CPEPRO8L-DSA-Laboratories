"""BFS and DFS. Neighbor order = sorted (alphabetical), via Graph.neighbors()."""
from collections import deque


def bfs(graph, start):
    """Return (order, parent) using a FIFO queue. parent[start] is None."""
    if start not in graph.adj:
        raise KeyError(f"unknown start vertex {start!r}")
    visited = {start}
    parent = {start: None}
    order = []
    queue = deque([start])
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.neighbors(u):
            if v not in visited:        # mark when ENQUEUED so no duplicates
                visited.add(v)
                parent[v] = u
                queue.append(v)
    return order, parent


def dfs_recursive(graph, start):
    """Return (order, parent) using recursion."""
    if start not in graph.adj:
        raise KeyError(f"unknown start vertex {start!r}")
    visited, order, parent = set(), [], {start: None}

    def visit(u):
        visited.add(u)
        order.append(u)
        for v in graph.neighbors(u):
            if v not in visited:
                parent[v] = u
                visit(v)

    visit(start)
    return order, parent


def dfs_iterative(graph, start):
    """Explicit-stack DFS giving the SAME order as dfs_recursive.

    Neighbors are pushed in reverse so the alphabetically first is popped first.
    A vertex is marked visited when popped (not when pushed).
    """
    if start not in graph.adj:
        raise KeyError(f"unknown start vertex {start!r}")
    visited, order, parent = set(), [], {start: None}
    stack = [(start, None)]
    while stack:
        u, p = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        parent[u] = p
        order.append(u)
        for v in reversed(graph.neighbors(u)):
            if v not in visited:
                stack.append((v, u))
    return order, parent


def bfs_trace(graph, start):
    """Markdown hand-trace table: selected vertex, queue after, visited set, order."""
    visited = {start}
    queue = deque([start])
    order = []
    rows = [("-", f"[{start}]", "{" + start + "}", "")]
    step = 0
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
        step += 1
        rows.append((u, "[" + ", ".join(queue) + "]",
                     "{" + ", ".join(sorted(visited)) + "}", " ".join(order)))
    out = [f"BFS trace from {start}", "",
           "| Selected | Queue (front→back) | Visited | Order so far |", "|---|---|---|---|"]
    out += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    return "\n".join(out)


def dfs_trace(graph, start):
    """Markdown hand-trace table for the explicit-stack DFS (top of stack = right)."""
    visited, order = set(), []
    stack = [start]
    rows = [("-", f"[{start}]", "{}", "")]
    while stack:
        u = stack.pop()
        if u in visited:
            rows.append((f"{u} (already visited, skip)", "[" + ", ".join(stack) + "]",
                         "{" + ", ".join(sorted(visited)) + "}", " ".join(order)))
            continue
        visited.add(u)
        order.append(u)
        for v in reversed(graph.neighbors(u)):
            if v not in visited:
                stack.append(v)
        rows.append((u, "[" + ", ".join(stack) + "]",
                     "{" + ", ".join(sorted(visited)) + "}", " ".join(order)))
    out = [f"DFS trace from {start}", "",
           "| Selected (popped) | Stack (bottom→top) | Visited | Order so far |", "|---|---|---|---|"]
    out += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    return "\n".join(out)


def path_from_parent(parent, target):
    """Rebuild the start→target path from a parent map, or None if unreachable."""
    if target not in parent:
        return None
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]
