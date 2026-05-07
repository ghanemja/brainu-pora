# Steiner tree

## Definition

A **Steiner tree** for a graph $G = (V, E)$ with a terminal set $T \subseteq V$ is a tree (acyclic connected subgraph) that spans all terminals in $T$. The tree may use additional non-terminal vertices (called Steiner vertices) from $V \setminus T$ to reduce total edge cost. Formally:

$$\text{StTree}(G, T) = \min_{\text{subtrees connecting } T} \sum_{e \in \text{tree}} w(e)$$

where $w(e)$ is the edge weight. Unlike a minimum spanning tree (which must connect *all* vertices), a Steiner tree connects only required terminals, often at lower cost.

## Key Equations

**Steiner tree approximation bound:**
For an EPTAS (Efficient Polynomial-Time Approximation Scheme), we seek a solution $S$ such that:
$$\text{Cost}(S) \leq (1 + \varepsilon) \cdot \text{StTree}(G, T)$$
for any $\varepsilon > 0$, with runtime polynomial in graph size and $\log(1/\varepsilon)$.

**Steiner-tree spanner:** A subgraph $H \subseteq G$ is a $(1+\varepsilon)$-Steiner-tree spanner if:
$$\text{StTree}(H, T) \leq (1 + \varepsilon) \cdot \text{StTree}(G, T)$$

**Column length bound (planar case):** Given a face $F$ with boundary partitioned into South and North portions, the total length of all columns is:
$$\sum_i |C_i| \leq O(1/\varepsilon) \cdot |\text{South}|$$

## Physical Intuition / Derivation

### Why Steiner Trees Matter

In network design, we often need to connect specific nodes (terminals) with minimum total wire/cable length. Allowing intermediate junction points (Steiner vertices) can yield significantly cheaper solutions than directly connecting terminals:

- **Rectilinear case:** Connecting three points at vertices of an equilateral triangle requires length $2$ with Steiner point, but $\sqrt{3} \approx 1.73$ without.
- **Routing networks:** In VLSI design, intermediate via points reduce congestion and total wire length.

### EPTAS Construction Strategy (Planar Graphs)

The algorithm from Borradaile, Klein, and Mathieu [24] proceeds in three phases:

1. **Skeleton construction:** Build a sparse subgraph containing a near-optimal Steiner tree, sized $\text{poly}(1/\varepsilon) \cdot \text{StTree}(G, T)$.

2. **Columns and mortars:** Each face of the skeleton is subdivided using "columns"—shortest paths between designated boundary points. These columns partition faces into rectangular "bricks." Only every $\kappa$-th column (where $\kappa = \text{poly}(1/\varepsilon)$) is retained in the mortar graph.

3. **Bounded treewidth decomposition:** The mortar graph, when contracted appropriately using Lemma 2.5, achieves treewidth $O(2^{\text{poly}(1/\varepsilon)})$, enabling dynamic programming.

### Key Technical Insight (Lemma 2.5)

When contracting a set $X$ in a graph $G$ to solve a problem optimally, it suffices to contract not just $X$ itself, but its $r$-neighborhood $X_r = N_H(X, r)$. This preserves tree decomposition quality:
$$\text{tw}(G / X_r) = O(\Delta c) \cdot \text{tw}(H / X)$$
where $c$ relates to Lipschitz constants and $\Delta$ is maximum degree. This is crucial because it allows decomposition algorithms to "see through" contracted regions without losing optimality guarantees.

## Applications in Engineering

### Network and Infrastructure Design
- **Telecommunications:** Minimize optical fiber deployment while connecting required hubs; Steiner vertices represent switching nodes.
- **Power grids:** Connect substations with minimum copper conductor material.
- **Water/gas distribution:** Route pipelines to service districts at lowest cost.

### VLSI and Chip Design
- **Rectilinear Steiner trees:** Standard routing model in automated layout. Reducing tree cost directly decreases chip area, power, and delay.
- **Clock distribution:** Balance signal arrival times at synchronization points using carefully placed buffers (Steiner nodes).

### Transportation and Logistics
- **Hub-and-spoke networks:** Connect delivery regions through intermediate depots (Steiner vertices) to minimize total distance.

### Facility Location
- **Clustered service centers:** Place depots to serve scattered customer regions at minimum total routing distance.

## Common Mistakes / Pitfalls

1. **Confusing with MST:** Students often assume Steiner tree ≤ MST cost; in fact, Steiner tree ≤ MST *always*, sometimes strictly. The MST solves a different problem (connecting all vertices, not just terminals).

2. **Assuming polynomial-time exactness:** The general Steiner tree problem is NP-hard. EPTAS exists only for restricted classes (planar, bounded treewidth, intersection graphs). No known polynomial-time exact algorithm for arbitrary graphs.

3. **Ignoring distance metric:** Steiner trees in Euclidean space (geometric Steiner trees) have different properties than graph Steiner trees. The rectilinear model differs from Euclidean.

4. **Overlooking terminal set size:** Complexity depends on $|T|$. For $|T| = 2$, the problem reduces to shortest path; for $|T| = |V|$, it becomes MST.

5. **Misapplying approximation bounds:** An $(1+\varepsilon)$-approximation algorithm running in time $n^{O(1/\varepsilon)}$ is *not* polynomial-time—it is an EPTAS (good for fixed $\varepsilon$) but not PTAS if the exponent depends on $1/\varepsilon$.

## See Also

- [[Minimum