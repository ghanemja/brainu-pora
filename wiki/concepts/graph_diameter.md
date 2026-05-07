# Graph Diameter

## Definition

The **diameter** of a connected graph $G = (V, E)$ is the maximum shortest-path distance between any pair of vertices:

$$D = \max_{u, v \in V} d(u, v)$$

where $d(u, v)$ is the length of the shortest path from $u$ to $v$ in terms of number of edges.

For disconnected graphs, the diameter is typically defined as infinite, or the diameter is computed separately for each connected component.

## Key Equations

**Formal notation:**
$$D(G) = \max_{u, v \in V(G)} \text{dist}(u, v)$$

**Bounds on diameter:**
- **Lower bound (from vertex count):** For a connected graph with $n$ vertices, $D \geq \lceil \log_k n \rceil$ in a $k$-regular graph (approximately)
- **Upper bound (from planar graphs):** Planar graphs can have diameter $D = O(n)$ in the worst case, but structured planar graphs often have $D = O(\sqrt{n})$
- **Tree diameter:** For a tree with $n$ vertices, $1 \leq D \leq n-1$

## Physical Intuition / Derivation

The diameter captures the **maximum communication cost** in a network represented as a graph:

- **Vertices** = locations/processors/nodes
- **Edges** = direct communication links
- **Diameter** = worst-case number of hops required for any two nodes to communicate

### Why It Matters for Distributed Computing

In distributed algorithms, information propagates one hop per round. Any algorithm solving a global property (e.g., consensus, spanning tree construction) requires *at least* $\Omega(D)$ rounds, since the farthest nodes must communicate. This makes $D$ a **universal lower bound**.

### Intuitive Example

Consider a line graph with 5 vertices: `v₁ — v₂ — v₃ — v₄ — v₅`
- Shortest path from $v_1$ to $v_5$ has length 4
- Therefore $D = 4$
- Any distributed algorithm must run for at least 4 rounds

## Applications in Engineering

### 1. **Distributed Systems & Networks**
- **Algorithm round complexity:** Protocol designers use $D$ to set lower bounds on communication rounds
- **Message routing:** Diameter bounds maximum latency in unoptimized routing schemes
- **Fault tolerance:** In replicated systems, diameter affects consensus protocol complexity (see [[Byzantine Fault Tolerance]])

### 2. **Planar Graph Optimization** (from source material)
- **Planar separators:** Lipton-Tarjan theorem guarantees $O(D)$-sized separators for planar graphs
- **Distributed planar algorithms:** Graph diameter determines round complexity for computing shortest paths, max-flow, and min-cut on planar graphs
- **Derandomization:** Deterministic separator algorithms (as described in the source) allow derandomization of distributed algorithms for planar graph problems

### 3. **Wireless Sensor Networks**
- Network diameter determines **multi-hop latency** bounds
- Affects aggregation and data collection protocols
- Critical for real-time applications with timing constraints

### 4. **Social Networks & Graph Analysis**
- **Six degrees of separation:** Small-world networks have surprisingly small diameter despite large $n$
- Used to characterize network structure and connectivity properties

### 5. **VLSI & Chip Design**
- Diameter of interconnection networks affects **maximum signal propagation delay**
- Influences clock period constraints in synchronous designs

## Common Mistakes / Pitfalls

1. **Confusing diameter with radius:**
   - **Radius** $r(G) = \min_v \max_u d(u,v)$ (minimum eccentricity)
   - **Diameter** $D(G) = \max_v \max_u d(u,v)$ (maximum eccentricity)
   - Always $r(G) \leq D(G)$, and $D(G) \leq 2 \cdot r(G)$

2. **Assuming diameter is tight for lower bounds:**
   - $\Omega(D)$ rounds is necessary but often *not* sufficient
   - Distributed algorithms may require $\tilde{O}(D)$ or $\tilde{O}(D^2)$ rounds even with diameter $D$

3. **Ignoring graph structure:**
   - Dense graphs can have small diameter but still large separators
   - Sparse graphs (e.g., trees) can have large diameter but admit small separators

4. **Discrete vs. continuous confusion:**
   - Graph diameter measures *hops* (discrete), not geometric distance
   - A spatial graph embedding doesn't determine diameter

5. **Misapplying to disconnected graphs:**
   - Diameter is undefined (or infinite) for disconnected graphs
   - Must clarify whether the problem involves connected components separately

## See Also

- [[Balanced Separator]] — Sets of vertices whose removal disconnects the graph; size is often bounded by diameter or $\sqrt{n}$
- [[Distributed Algorithms]] — Algorithms where diameter $D$ gives a universal lower bound on round complexity
- [[Planar Graphs]] — Special graph family where structure constrains both diameter and separator size
- [[Graph Centrality]] — Related metrics including radius, eccentricity, and closeness centrality
- [[Shortest Path Algorithms]] — Fundamental subroutine for computing diameter

## Sources

- Abd-Elhaleem, Y., Dory, M., & Weimann, O. "A Simple Distributed Deterministic Planar Separator." *arXiv:2602.22916* (2026).
- Lipton, R. J., & Tarjan, R. E. "A Separator Theorem for Planar Graphs." *FOCS'77* (1977).
- Ghaffari, M., & Parter, M. "Distributed Deterministic Edge Coloring." *DISC'17* (2017).