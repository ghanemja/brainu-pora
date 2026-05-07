# Dijkstra's Algorithm

## Definition

**Dijkstra's algorithm** is a greedy algorithm for solving the single-source shortest paths problem on weighted directed graphs with **non-negative edge weights**. Given a source vertex $s$ and a directed graph $G = (V, E)$ with edge weight function $w: E \to \mathbb{R}^{\geq 0}$, the algorithm computes the shortest path distance $d(s, v)$ from $s$ to every vertex $v \in V$.

The algorithm maintains:
- A set $S$ of vertices whose shortest path distance from $s$ has been finalized
- A priority queue $Q$ of unexplored vertices, keyed by their current estimated distance from $s$

## Key Equations

The algorithm iteratively selects the vertex $u \in Q$ with minimum estimated distance:

$$u = \arg\min_{v \in Q} \text{dist}[v]$$

For each outgoing edge $(u, v)$, it performs **relaxation**:

$$\text{dist}[v] = \min(\text{dist}[v], \text{dist}[u] + w(u, v))$$

**Time Complexity** (classic implementation with binary heap):
$$T(n, m) = O(m + n \log n)$$

where $n = |V|$ is the number of vertices and $m = |E|$ is the number of edges.

## Physical Intuition / Derivation

**Why does Dijkstra's algorithm work?**

The key insight is the **greedy choice property**: if all edge weights are non-negative, once a vertex $u$ is removed from the priority queue and added to $S$, its distance $\text{dist}[u]$ is permanently optimal—no future path can be shorter.

*Proof sketch:* Suppose some other path to $u$ with length $\text{dist}[u] + \delta$ (where $\delta > 0$) exists. This path must visit some vertex $v \notin S$ before reaching $u$. But then $\text{dist}[v] < \text{dist}[u] + \delta$, and since $v$ was processed before $u$, we have $\text{dist}[v] \leq \text{dist}[u]$. This contradicts $\text{dist}[u]$ being minimal when extracted.

**Why non-negative weights are essential:**

With negative edge weights, the greedy selection fails. Consider a graph where vertex $u$ is selected with $\text{dist}[u] = 5$, but a later relaxation via edge $(v, u)$ with weight $-10$ could improve $u$ to distance $\text{dist}[v] - 10 < 5$. This is why negative weights require algorithms like **Bellman-Ford** (which runs in $O(mn)$ time) or modern approaches like those discussed in the source material.

## Applications in Engineering

### 1. **Network Routing Protocols**
   - GPS navigation systems (Google Maps, Waze) use variants of Dijkstra's to compute shortest routes with non-negative distance/time metrics
   - OSPF (Open Shortest Path First) Internet routing protocol uses Dijkstra's algorithm as its core

### 2. **Telecommunications**
   - Network optimization: finding minimum-latency paths in data centers
   - Circuit design: shortest wire routing between components

### 3. **Robotics & Path Planning**
   - Motion planning in obstacle-free or discretized environments
   - Computing distance fields for collision avoidance

### 4. **Game Development**
   - NPC pathfinding on weighted terrain (grass costs less movement than water)
   - Multiplayer game server routing

### 5. **Supply Chain & Logistics**
   - Computing minimum-cost distribution routes
   - Facility location optimization

## Common Mistakes / Pitfalls

### 1. **Applying to Negative Weight Graphs**
   - **Mistake:** Using Dijkstra's on graphs with negative edge weights
   - **Result:** Algorithm returns incorrect distances
   - **Fix:** Use Bellman-Ford or other negative-weight algorithms

### 2. **Inefficient Priority Queue Implementation**
   - **Mistake:** Using an unsorted list for the priority queue ($O(n)$ extract-min per iteration)
   - **Result:** Algorithm runs in $O(n^2)$ time instead of $O(m + n \log n)$
   - **Fix:** Use a binary heap or Fibonacci heap

### 3. **Double-Processing Vertices**
   - **Mistake:** Not maintaining a "visited" set; allowing vertices to be processed multiple times
   - **Result:** Redundant work and incorrect behavior
   - **Fix:** Add $u$ to $S$ immediately upon extraction

### 4. **Forgetting to Initialize**
   - **Mistake:** Not setting $\text{dist}[s] = 0$ and $\text{dist}[v] = \infty$ for all other vertices
   - **Result:** Algorithm produces garbage output

### 5. **Integer Overflow** (implementation detail)
   - **Mistake:** Using finite "infinity" values (e.g., `INT_MAX`) without careful arithmetic
   - **Result:** Addition can overflow when checking $\text{dist}[u] + w(u, v)$

## See Also

- [[Bellman-Ford Algorithm]] — Single-source shortest paths with negative edge weights; $O(mn)$ time
- [[Priority Queue]] — Underlying data structure; implementation choice affects performance
- [[A* Search]] — Informed variant of Dijkstra's for goal-directed search using heuristics
- [[Shortest Path Problem]] — General problem class; variants include all-pairs (Floyd-Warshall) and negative weights
- [[Minimum Spanning Tree]] — Related graph optimization problem (Prim's algorithm uses similar greedy approach)

## Sources

- Bellman-Ford in Almost-Linear Time for Dense Graphs (Li, Li, Zhang; 2026) — context on recent algorithmic advances for real-weighted shortest paths and comparison to Dijkstra's $O(m + n \log n)$ bound for non-negative weights