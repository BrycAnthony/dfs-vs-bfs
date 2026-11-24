"""
COMP 3305 Class Project - Depth-First Search vs. Breadth-First Search
Author: Bryce Anderson

Implements BFS and DFS (iterative and recursive) on an adjacency-list graph,
plus instrumentation used for the comparative analysis:
  - order in which vertices are visited
  - number of vertices explored before reaching a target
  - peak frontier size (queue/stack) -> memory behaviour
  - length of the path found (BFS = shortest in unweighted graphs)
"""
from collections import deque
import sys


class Graph:
    """Unweighted graph stored as an adjacency list (dict: vertex -> list)."""

    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def add_vertex(self, v):
        self.adj.setdefault(v, [])

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def neighbors(self, v):
        return self.adj.get(v, [])

    def __len__(self):
        return len(self.adj)


# ---------------------------------------------------------------------------
# Breadth-First Search  -  FIFO queue, explores level by level
# ---------------------------------------------------------------------------
def bfs(graph, start, target=None):
    """Return dict with visit order, parent map, explored count, peak frontier."""
    visited = {start}
    parent = {start: None}
    queue = deque([start])
    order = []
    peak = 1
    while queue:
        u = queue.popleft()
        order.append(u)
        if u == target:
            break
        for w in graph.neighbors(u):
            if w not in visited:
                visited.add(w)
                parent[w] = u
                queue.append(w)
        peak = max(peak, len(queue))
    return {"order": order, "parent": parent, "explored": len(order),
            "peak_frontier": peak, "found": target in parent if target is not None else None}


# ---------------------------------------------------------------------------
# Depth-First Search  -  LIFO stack, goes as deep as possible first
# ---------------------------------------------------------------------------
def dfs(graph, start, target=None):
    """Iterative DFS (explicit stack). Visits neighbours in the same order as
    the recursive version so both produce identical traversal orders."""
    visited = set()
    parent = {start: None}
    stack = [start]
    order = []
    peak = 1
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        if u == target:
            break
        for w in reversed(graph.neighbors(u)):
            if w not in visited:
                parent[w] = u
                stack.append(w)
        peak = max(peak, len(stack))
    return {"order": order, "parent": parent, "explored": len(order),
            "peak_frontier": peak, "found": target in visited if target is not None else None}


def dfs_recursive(graph, start, visited=None, order=None):
    """Classic recursive DFS (limited by Python's recursion depth)."""
    if visited is None:
        visited, order = set(), []
    visited.add(start)
    order.append(start)
    for w in graph.neighbors(start):
        if w not in visited:
            dfs_recursive(graph, w, visited, order)
    return order


def reconstruct_path(parent, target):
    if target not in parent:
        return None
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]


# ---------------------------------------------------------------------------
# Applications built on top of BFS / DFS
# ---------------------------------------------------------------------------
def has_cycle_directed(graph):
    """DFS with 3 colours: a back edge to a GRAY vertex means a cycle."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.adj}

    def visit(u):
        color[u] = GRAY
        for w in graph.neighbors(u):
            if color[w] == GRAY or (color[w] == WHITE and visit(w)):
                return True
        color[u] = BLACK
        return False

    return any(color[v] == WHITE and visit(v) for v in graph.adj)


def topological_sort(graph):
    """DFS-based topological order of a DAG."""
    seen, out = set(), []

    def visit(u):
        seen.add(u)
        for w in graph.neighbors(u):
            if w not in seen:
                visit(w)
        out.append(u)

    for v in graph.adj:
        if v not in seen:
            visit(v)
    return out[::-1]


def connected_components(graph):
    """Counts components by running BFS from every unvisited vertex."""
    seen, comps = set(), []
    for v in graph.adj:
        if v not in seen:
            comp = bfs(graph, v)["order"]
            seen.update(comp)
            comps.append(comp)
    return comps


# ---------------------------------------------------------------------------
# Graph generators used in the experiments
# ---------------------------------------------------------------------------
def grid_graph(n, walls=frozenset()):
    """n x n grid maze; vertices are (row, col); walls are blocked cells."""
    g = Graph()
    for r in range(n):
        for c in range(n):
            if (r, c) in walls:
                continue
            g.add_vertex((r, c))
            for dr, dc in ((0, 1), (1, 0)):
                rr, cc = r + dr, c + dc
                if rr < n and cc < n and (rr, cc) not in walls:
                    g.add_edge((r, c), (rr, cc))
    return g


def random_graph(n, avg_degree, seed=0):
    import random
    rnd = random.Random(seed)
    g = Graph()
    for v in range(n):
        g.add_vertex(v)
    for v in range(1, n):  # spanning tree keeps the graph connected
        g.add_edge(v, rnd.randrange(v))
    extra = n * avg_degree // 2 - (n - 1)
    for _ in range(max(0, extra)):
        g.add_edge(rnd.randrange(n), rnd.randrange(n))
    return g


def complete_tree(branching, depth):
    """Complete tree: every internal node has `branching` children."""
    g = Graph()
    g.add_vertex(0)
    frontier, nxt = [0], 1
    for _ in range(depth):
        new = []
        for u in frontier:
            for _ in range(branching):
                g.add_edge(u, nxt)
                new.append(nxt)
                nxt += 1
        frontier = new
    return g


def sample_graph():
    """Small 8-vertex graph used on the slides and in the demo."""
    g = Graph()
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
                 ("C", "F"), ("C", "G"), ("C", "H"), ("E", "H"), ("F", "H")]:
        g.add_edge(u, v)
    return g


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    g = sample_graph()
    print("Sample graph adjacency list:")
    for v, ns in g.adj.items():
        print(f"  {v}: {ns}")
    print("\nBFS order from A:          ", " -> ".join(bfs(g, "A")["order"]))
    print("DFS order from A:          ", " -> ".join(dfs(g, "A")["order"]))
    print("DFS (recursive) from A:    ", " -> ".join(dfs_recursive(g, "A")))
    rb, rd = bfs(g, "A", "H"), dfs(g, "A", "H")
    print("\nPath A->H found by BFS:", reconstruct_path(rb["parent"], "H"))
    print("Path A->H found by DFS:", reconstruct_path(rd["parent"], "H"))

    dag = Graph(directed=True)
    for u, v in [("Intro CS", "Data Structures"), ("Discrete Math", "Algorithms"),
                 ("Data Structures", "Algorithms"), ("Algorithms", "AI")]:
        dag.add_edge(u, v)
    print("\nDFS application - course order (topological sort):", topological_sort(dag))
    print("Cycle in course graph?", has_cycle_directed(dag))
