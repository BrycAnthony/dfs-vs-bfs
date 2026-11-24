# DFS vs. BFS — A Comparative Analysis
**COMP 3305 Class Project — Bryce Anderson, Prairie View A&M University (Fall 2026)**

Python implementation of Depth-First Search and Breadth-First Search with an
experimental comparison of runtime, vertices explored, path quality, and memory.

| File | Purpose |
|---|---|
| `graph_search.py` | `Graph` (adjacency list), `bfs`, `dfs` (iterative), `dfs_recursive`, path reconstruction, cycle detection, topological sort, connected components, graph generators |
| `compare.py` | Three experiments: runtime scaling, grid path-finding, tree memory usage → prints tables, writes `results.json` |
| `DFS_vs_BFS_Demo.ipynb` | Google Colab demo (run all cells) |

## Run
```bash
python3 graph_search.py   # traversal demo on the 8-vertex sample graph
python3 compare.py        # comparative experiments (~30 s)
```
Requires only Python 3.8+ (standard library). The notebook also uses `matplotlib`/`networkx` for plots, both preinstalled on Colab.

## Key results
| Experiment | BFS | DFS |
|---|---|---|
| Runtime, 400k vertices / 1.2M edges | 1,025 ms | 1,590 ms (both O(V+E), linear) |
| 101×101 grid, target 10 steps diagonally away | 221 explored, path 20 (optimal) | 1,021 explored, path 1,020 |
| Binary tree depth 18 (524k nodes), peak memory | 262,144 frontier entries | 19 stack entries |

**Takeaway:** BFS guarantees shortest paths in unweighted graphs but stores a whole level;
DFS uses memory proportional to depth and powers cycle detection / topological sort, but its paths can be very long.
