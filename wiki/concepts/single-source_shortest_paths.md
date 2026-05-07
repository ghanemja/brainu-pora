# single-source shortest paths

## Definition

The **single-source shortest paths problem** is to compute the shortest-path distance from a designated source vertex $s$ to all other vertices in a directed weighted graph $G = (V, E)$ with edge weight function $w: E \to \mathbb{R}$.

**Formal statement:** Given a directed graph $G = (V, E)$ with real-valued edge weights $w(u,v)$ for each edge $(u,v) \in E$, and a source vertex $s \in V$, compute:

$$d(s, v) = \min \{ w(P) : P \text{ is a path from } s \text{ to } v \}$$

for all $v \in V$, where $w(P) = \sum_{(u,v) \in P} w(u,v)$ is the total weight of path $P$.

The problem must handle three constraint regimes:
- **Non-negative weights** ($w(e) \geq 0$ for all $e \in E$)
- **Integral weights** (weights are integers, possibly negative)
- **Real-valued weights** (weights can be any real number, including negative values)

## Key Equations

The optimal substructure principle (Bellman principle) underlies all shortest path algorithms:

$$d(s, v) = \min \left( d(s, v), \min_{(u,v) \in E} \{ d(s, u) + w(u,v) \} \right)$$

This relaxation property is the foundation of iterative refinement algorithms.

For the **Bellman-Ford** update rule applied $|V|-1$ times:

$$d_i(v) = \min \{ d_{i-1}(v), \min_{(u,v) \in E} \{ d_{i-1}(u) + w(u,v) \} \}$$

where $d_i(v)$ represents the shortest path distance using at most $i$ edges.

## Physical Intuition / Derivation

### Why Multiple Algorithms for Different Weight Constraints?

The key insight is that **negative edge weights dramatically increase computational difficulty**:

1. **Non-negative weights (Dijkstra's algorithm)**: Once a vertex's distance is finalized, it never improves. This greedy property enables the priority queue speedup to $O(m + n \log n)$ time, which is optimal for many graphs.

2. **Negative weights allowed**: The greedy assumption breaks. A shortest path might take a long detour through a negative-weight region. Therefore, we cannot finalize distances early. This forces:
   - **Bellman-Ford**: $O(mn)$ time—iterate $n-1$ times, relaxing all edges each time
   - **Modern approaches**: Use structural techniques (shortcutting, betweenness reduction) to avoid the full $O(mn)$ cost for dense graphs

### The Shortcutting Perspective (Li et al. 2026)

The recent $n^{2+o(1)}$ algorithm relies on:

- **Negative vertex reduction**: Identify vertices with negative outgoing edges (the $|N|$ "negative vertices")
- **Shortcut construction**: For each negative vertex $u$, precompute shortest paths to nearby vertices and add direct shortcut edges, reducing the "density" of negative edges in subsequent iterations
- **Iterated refinement**: Repeatedly apply shortcutting to reduce the fraction of paths with many negative hops
- After $O(\log n)$ iterations, paths traverse $O(1)$ negative edges, allowing standard algorithms to terminate

This is fundamentally different from Dijkstra (which doesn't work with negative weights at all) and Bellman-Ford (which is too slow for dense graphs).

## Applications in Engineering

### 1. **Navigation and Routing**
- **GPS navigation**: Computing fastest routes from origin to all destinations (non-negative edge weights = driving times)
- **Multi-hop network routing**: OSPF and similar protocols use Dijkstra; when asymmetric link costs exist, shortest path algorithms apply
- **Urban transit planning**: Finding optimal bus/subway connections with transfers and varying speeds

### 2. **Network Design and Analysis**
- **Telecommunication networks**: Computing minimum-latency paths; negative weights can represent cost credits for using certain links
- **Financial networks**: Modeling arbitrage detection (finding profitable exchange sequences); negative cycles correspond to arbitrage opportunities

### 3. **Robotics and Motion Planning**
- **Path planning in weighted terrain**: Cost of traversal varies by terrain type (mud, rock, etc.)
- **Robot arm kinematics**: Shortest motion sequences to reach target configuration, with costs representing energy or time

### 4. **Compiler Optimization**
- **Critical path scheduling**: Determining longest computation paths in program dependence graphs (dual of shortest path)
- **Register allocation**: Cost minimization in program instruction sequences

### 5. **Logistics and Supply Chain**
- **Vehicle routing with tolls/incentives**: Negative edge weights represent refunds on certain routes
- **Multi-modal transportation**: Shortest cost path across different transport modes

## Common Mistakes / Pitfalls

### 1. **Misapplying Dijkstra to Negative Weights**
- **Error**: Using Dijkstra's algorithm on graphs with negative edge weights produces incorrect results because the greedy "finalize distance" property is violated.
- **Fix**: Use Bellman-Ford ($O(mn)$) or modern algorithms for real-valued weights, not Dijkstra.

### 2. **Negative Cycles Are Undetectable Without Extra Work**
- **Error**: If a negative cycle exists on some path from $s$ to $v$, the shortest path is undefined (can arbitrarily decrease by looping). Standard algorithms may not detect this.
- **Fix**: Run Bellman-Ford for exactly $|V|$ iterations; if distances decrease on the $|V|$-th iteration, a negative cycle exists.

### 3. **Confusing Distance Arrays and Path Trees**
- **Error**: Computing shortest **distances** (single value per vertex) is different from reconstructing actual **paths**. Many implementations compute distances but store no parent pointers.
- **Fix**: Maintain a parent array $\text{parent}[v]$ pointing backward along shortest path edges; reconstruct path by backtracking from destination to source.

### 4. **Forgetting All-Pairs