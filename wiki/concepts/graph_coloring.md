# Graph Coloring

## Definition

**Graph coloring** is the assignment of labels (called "colors") to vertices of a graph such that no two adjacent vertices share the same color. Formally, given an undirected graph $G = (V, E)$, a **proper $k$-coloring** is a function $c: V \to \{1, 2, \ldots, k\}$ such that for every edge $(u, v) \in E$, we have $c(u) \neq c(v)$.

The **chromatic number** $\chi(G)$ is the minimum number of colors required for a proper coloring of $G$. A **$(k+1)$-coloring** (or **$(\Delta+1)$-coloring**) is one that uses at most $k+1$ colors, where $\Delta$ is the maximum degree of the graph.

### Related Variants
- **Distributed coloring**: Vertices color themselves using only local neighborhood information
- **Parallel coloring**: Simultaneous assignment of colors across multiple processors
- **Matroid coloring**: Generalization requiring independent sets form matroids

## Key Equations

$$\chi(G) \geq \omega(G)$$

where $\omega(G)$ is the clique number (size of the largest clique).

$$\chi(G) \leq \Delta(G) + 1$$

**Brooks' Theorem**: For most graphs, $\chi(G) \leq \Delta(G)$, except for complete graphs and odd cycles.

For a greedy coloring algorithm:
$$\chi_{\text{greedy}}(G) \leq \Delta(G) + 1$$

The **fractional chromatic number** (via LP-relaxation) provides a lower bound:
$$\chi_f(G) \leq \chi(G)$$

## Physical Intuition / Derivation

### Why Graph Coloring Matters

Consider a scheduling problem: you have tasks (vertices) where some tasks conflict (edges). You want to partition tasks into non-conflicting groups (color classes). The minimum number of groups needed is the chromatic number.

### Algorithmic Approaches

**Greedy Coloring**: Process vertices in some order, assigning each vertex the smallest color not used by its neighbors. This guarantees at most $\Delta + 1$ colors because a vertex has at most $\Delta$ neighbors.

**LP-Rounding for Matroid Coloring** (from source material): For complex constraints like matroid independence:
1. **Cast as optimization**: Frame coloring as a $(k+1)$-matroid intersection problem, where feasible colorings correspond to valid matroid decompositions
2. **LP relaxation**: Solve the linear program to get fractional (approximate) color assignments
3. **Rounding phase**: Convert fractional solution to integral via randomized or derandomized techniques

The key insight is that instead of directly constructing an independent set (which requires understanding matroid structure), we use LP-rounding to navigate the constraint space more efficiently.

### Distributed Coloring

In distributed settings (cited Johansson, Luby), nodes color themselves synchronously:
- Each node independently flips a random coin
- Nodes that flip heads attempt coloring
- If no neighbor has the same color, commit; otherwise retry
- Achieves $(\Delta+1)$-coloring in $O(\log n)$ rounds with high probability

## Applications in Engineering

### 1. **Register Allocation (Compilers)**
- Variables are vertices; interference between variables creates edges
- Colors = physical CPU registers
- Minimize registers needed (cost of CPU design)

### 2. **Frequency Assignment (Wireless Networks)**
- Base stations are vertices; interference range creates edges
- Colors = radio frequencies
- Minimize spectrum usage (regulatory/cost constraints)

### 3. **Parallel Task Scheduling**
- Tasks are vertices; dependencies/conflicts are edges
- Colors = time slots or processors
- Minimize makespan or processor count

### 4. **Map Coloring (Geospatial Systems)**
- Regions are vertices; adjacent regions share edges
- Colors = display colors or data classification
- The famous four-color theorem guarantees $\chi \leq 4$ for planar maps

### 5. **Graph Decomposition (Hypergraph Algorithms)**
- Coloring graphs decomposes them into independent sets
- Used in clique counting, k-core decomposition (parallel algorithms)
- Enables divide-and-conquer parallel processing (referenced in SPAA 2022 work)

### 6. **Resource Conflict Resolution**
- In distributed systems, coloring resolves resource contention
- Used in lock-free data structure design
- Determines synchronization barriers in parallel algorithms

## Common Mistakes / Pitfalls

### 1. **Confusing Chromatic Number with Degree**
- ❌ Thinking $\chi(G) = \Delta(G)$ always
- ✓ Remember: $\chi(G) \leq \Delta(G) + 1$ in general, and $\chi(G) \leq \Delta(G)$ except rare cases (complete graphs, odd cycles)

### 2. **Greedy Coloring Optimality**
- ❌ Assuming greedy coloring finds optimal coloring
- ✓ Greedy is a $(1 + \ln \Delta)$-approximation at best; NP-hard to optimize

### 3. **Ignoring Graph Structure**
- ❌ Using generic algorithms on special graphs (bipartite, planar, trees)
- ✓ Bipartite graphs have $\chi = 2$; trees have $\chi = 2$; these permit faster algorithms

### 4. **Distributed vs. Centralized Complexity**
- ❌ Expecting distributed algorithms to match centralized time complexity
- ✓ Distributed algorithms incur $O(\log n)$ or $O(\Delta)$ rounds even when centralized is polynomial

### 5. **Matroid Reduction Loss**
- ❌ Naively reducing general matroid coloring to partition matroids
- ✓ This can increase chromatic number drastically; use LP-rounding + matroid intersection instead (as in cited work)

## See Also

- [[Independent Set Problem]] — Finding maximum set of non-adjacent vertices; dual to coloring
- [[