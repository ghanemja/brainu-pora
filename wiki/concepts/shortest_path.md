# shortest path

## Definition

A **shortest path** between two vertices $u$ and $v$ in a graph $G = (V, E)$ is a sequence of edges connecting $u$ to $v$ such that the total weight (or edge count in unweighted graphs) is minimized. Formally:

$$\text{dist}_G(u, v) = \min \{ \text{length of path } P : u \to v \}$$

In the context of **fault-tolerant distance oracles**, a shortest path must be computed even when up to $f$ edges have been adversarially deleted from the graph. The oracle must return a distance $d$ satisfying:

$$\text{dist}_{G - F \cap G}(a, b) \leq d \leq t \cdot \text{dist}_{G - F \cap G}(a, b)$$

where $F$ is a deletion set with $|F| \leq f$, and $t$ is the approximation factor.

## Key Equations

**Distance in unweighted graphs:**
$$\text{dist}_G(u, v) = \begin{cases} 
0 & \text{if } u = v \\
1 + \min_{w \in \Gamma(u)} \text{dist}_G(w, v) & \text{otherwise}
\end{cases}$$

where $\Gamma(u)$ denotes the neighbors of $u$.

**Fault-tolerant distance query:**
Given a graph $G$ and deletion set $F \subseteq E$ with $|F| \leq f$, recover:
$$d^* = \text{dist}_{G-F}(a, b)$$

**Path length bounds in 2-hop star graphs:**
For vertices in a 2-hop star with root $v$:
- Vertices in $L_1$ (direct neighbors of $v$): path length $\leq 1$
- Vertices in $L_2$ (neighbors of $L_1$): path length $\leq 3$ under specific degree conditions

## Physical Intuition / Derivation

### Why Shortest Path Matters

In unweighted graphs, the shortest path represents the **minimum number of hops** needed to reach from source to destination. This is fundamental because:

1. **Direct metric**: In networks, fewer hops typically means lower latency, less congestion, and higher reliability
2. **Optimality principle**: Any subpath of a shortest path is itself a shortest path (Bellman's principle)

### Robustness Under Failures

The source material discusses shortest path computation when edges may fail or be deleted. The key insight is that after deleting a set $F$ of edges:

$$\text{dist}_{G-F}(u, v) \geq \text{dist}_G(u, v)$$

The distance can only increase or stay the same. For **2-hop star topologies** (common in hub-and-spoke networks), the analysis shows:

- If a vertex $u \in L_2$ has degree $\geq 5f/d$ in the residual graph $G - F$, then there exists a neighbor $w$ with high enough degree to guarantee a path to $v$ of length $\leq 3$
- This relies on the **pigeonhole principle**: with $|F| \leq f$ deletions and degree threshold $d/2 \geq 5f/d$, enough edges must remain to maintain connectivity

### Why Path Length $\leq 3$ in $L_2$?

For a vertex $u \in L_2$:
$$u \to w \to l \to v$$

where:
- $u \to w$: edge exists if $w \in \Gamma(u)$ and not deleted
- $w \to l$: edge exists if $l \in \Gamma(w)$ and not in the "BAD" set of heavily-deleted vertices
- $l \to v$: edge exists because $l \in L_1$ (direct neighbor of $v$)

## Applications in Engineering

### 1. **Network Routing**
- **OSPF (Open Shortest Path First)**: Uses Dijkstra's algorithm to compute shortest paths in IP networks
- **SDN controllers**: Compute shortest paths for packet forwarding with link failures
- Approximation factor $t$ trades off storage space for query accuracy in resource-constrained routers

### 2. **GPS Navigation & Map Services**
- Google Maps, Waze compute shortest paths in road networks millions of times per second
- Fault-tolerance matters: roads close, traffic data updates dynamically
- Distance oracles enable sub-millisecond query times on billion-node graphs

### 3. **Telecommunications**
- Setting up circuits with minimum latency
- Handling link failures gracefully (up to $f$ simultaneous failures)
- Critical for SLA (Service Level Agreement) guarantees

### 4. **Robotics & Motion Planning**
- Shortest path in configuration space for robot arm motion
- Clearance guarantees under sensor uncertainty (fault-tolerant variant)

### 5. **Supply Chain & Logistics**
- Warehouse-to-customer routing minimizing travel distance/time
- Robustness against traffic incidents or facility closures

## Common Mistakes / Pitfalls

### 1. **Confusing Shortest Path with Arbitrary Path**
Students sometimes return *any* path rather than verifying it is shortest. In sparse graphs, random paths can be exponentially longer.

### 2. **Ignoring Edge Weights**
Dijkstra's algorithm requires non-negative weights. Using BFS on weighted graphs gives incorrect results.

### 3. **Not Accounting for Directed vs. Undirected**
A shortest path in a directed graph $G$ may differ drastically from the reverse direction. Must be explicit about directionality.

### 4. **Misunderstanding Approximation Factors**
An oracle with approximation $t = 2$ means:
$$d_{\text{query}} \leq 2 \cdot d_{\text{true}}$$
This does NOT guarantee finding the actual shortest path; only a 2-approximation.

### 5. **Overlooking Failure Model Constraints**
The source material specifies $|F| \leq f$ *and* "at most $d/2$ of $v$'s edges are deleted." Ign