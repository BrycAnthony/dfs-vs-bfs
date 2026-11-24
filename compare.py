"""
Comparative analysis of BFS vs DFS.

Experiment 1 - Runtime scaling on random connected graphs (avg degree 6):
               both should grow linearly in V + E.
Experiment 2 - Open n x n grid, search from the top-left corner to the
               centre and to the far corner: vertices explored, path length
               found, and peak frontier size (memory).
Experiment 3 - Complete binary tree: peak frontier size during a full
               traversal (BFS holds a whole level, DFS only one branch).
Results are printed as tables and saved to results.json.
"""
import json
import time
from statistics import median

from graph_search import bfs, dfs, grid_graph, random_graph, reconstruct_path, complete_tree


def time_it(fn, *args, repeats=5):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - t0)
    return median(times) * 1000  # ms


def experiment_runtime(sizes=(10_000, 50_000, 100_000, 200_000, 400_000)):
    rows = []
    for n in sizes:
        g = random_graph(n, avg_degree=6, seed=42)
        edges = sum(len(v) for v in g.adj.values()) // 2
        rows.append({"V": n, "E": edges,
                     "bfs_ms": round(time_it(bfs, g, 0), 1),
                     "dfs_ms": round(time_it(dfs, g, 0), 1)})
    return rows


def experiment_grid(n=101):
    g = grid_graph(n)
    start = (0, 0)
    out = {}
    for label, target in (("near", (n // 10, n // 10)),
                          ("centre", (n // 2, n // 2)),
                          ("far corner", (n - 1, n - 1))):
        row = {}
        for name, algo in (("BFS", bfs), ("DFS", dfs)):
            r = algo(g, start, target)
            path = reconstruct_path(r["parent"], target)
            row[name] = {"explored": r["explored"],
                         "path_len": len(path) - 1,
                         "peak_frontier": r["peak_frontier"]}
        row["optimal"] = abs(target[0]) + abs(target[1])
        out[label] = row
    return out


def experiment_tree(branching=2, depths=(8, 10, 12, 14, 16, 18)):
    """Full traversal of a complete binary tree: peak frontier = memory."""
    rows = []
    for d in depths:
        g = complete_tree(branching, d)
        rows.append({"depth": d, "V": len(g),
                     "bfs_peak": bfs(g, 0)["peak_frontier"],
                     "dfs_peak": dfs(g, 0)["peak_frontier"]})
    return rows


if __name__ == "__main__":
    print("Experiment 1: runtime on random graphs (median of 5 runs)")
    print(f"{'V':>8} {'E':>9} {'BFS ms':>9} {'DFS ms':>9}")
    rt = experiment_runtime()
    for r in rt:
        print(f"{r['V']:>8} {r['E']:>9} {r['bfs_ms']:>9} {r['dfs_ms']:>9}")

    n = 101
    print(f"\nExperiment 2: {n}x{n} open grid ({n*n} vertices), start (0,0)")
    grid = experiment_grid(n)
    for label, row in grid.items():
        print(f"  target {label} (optimal path = {row['optimal']} steps)")
        for name in ("BFS", "DFS"):
            d = row[name]
            print(f"    {name}: explored {d['explored']:>6}  path {d['path_len']:>6}  "
                  f"peak frontier {d['peak_frontier']:>6}")

    print("\nExperiment 3: complete binary tree, full traversal - peak frontier (memory)")
    tree = experiment_tree()
    print(f"{'depth':>6} {'V':>8} {'BFS peak':>9} {'DFS peak':>9}")
    for r in tree:
        print(f"{r['depth']:>6} {r['V']:>8} {r['bfs_peak']:>9} {r['dfs_peak']:>9}")

    with open("results.json", "w") as f:
        json.dump({"runtime": rt, "grid": grid, "grid_n": n, "tree": tree}, f, indent=2)
    print("\nSaved results.json")
