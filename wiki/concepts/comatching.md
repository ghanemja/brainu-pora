# Comatching

## Definition

A **comatching** is a set of vertex pairs in a geometric graph where corresponding path endpoints maintain controlled spatial separation constraints. Formally, given a graph $G = (V, E)$ embedded in a metric space $(V, \text{dist})$, a comatching is a collection of pairs $\{(p_i, q_i)\}_{i=1}^{\ell}$ such that the shortest paths between distinct pairs exhibit strong topological disjointness properties.

In the context of **linked noncrossing instances** (metric graphs with geometric constraints), a comatching is characterized by the separation property:

**Separation Lemma (Lemma 2.1):** For any two distinct pairs $(p_i, q_i)$ and $(p_j, q_j)$ in a comatching, the shortest paths $\langle p_i q_j \rangle$ and $\langle p_j q_i \rangle$ are vertex-disjoint (they do not intersect except possibly at endpoints).

This enforces a rigid topological structure on the arrangement of vertex pairs in the plane.

## Key Equations

**Distance contradiction principle:**
$$2(1-\varepsilon)R \geq \text{dist}(p_i, q_j) + \text{dist}(p_j, q_i) = \text{dist}(p_i, q_i) + \text{dist}(p_j, q_j) > 2R$$

This inequality demonstrates that if a shared vertex $u$ exists on both paths, the combined path lengths violate the diameter constraint $R$, yielding contradiction.

**Comatching size bound (planar graphs):**
$$\ell = O(1/\varepsilon)$$

where $\ell$ denotes the maximum number of pairs in a comatching and $\varepsilon$ characterizes the metric constraint tightness.

**General bound for bounded genus surfaces:**
$$\ell = O(g/\varepsilon)$$

where $g$ is the Euler genus of the surface.

## Physical Intuition / Derivation

### Why Disjointness Matters

Consider two pairs $(p_i, q_i)$ and $(p_j, q_j)$ attempting to share a common vertex $u$. The paths $\langle p_i q_j \rangle$ and $\langle p_j q_i \rangle$ would then create a "crossing" pattern. This crossing generates a distance-length constraint:

$$\text{dist}(p_i, q_j) + \text{dist}(p_j, q_i) \geq \text{dist}(p_i, u) + \text{dist}(u, q_j) + \text{dist}(p_j, u) + \text{dist}(u, q_i)$$

Rearranging:
$$= [\text{dist}(p_i, u) + \text{dist}(u, q_i)] + [\text{dist}(p_j, u) + \text{dist}(u, q_j)] \geq \text{dist}(p_i, q_i) + \text{dist}(p_j, q_j)$$

If the diameter is constrained to $R$ with slack factor $(1-\varepsilon)$, this inequality violates the diameter bound, creating an impossibility.

### Planar Arrangement Structure

The only feasible configuration for many pairs in a planar linked noncrossing instance is a **ladder-like arrangement** (Figure 6): pairs arrange sequentially along a strip where:
- Pairs do not interleave
- Paths remain geometrically disjoint
- The constraint on strip "width" limits pairs to $O(1/\varepsilon)$

### Extension to Surfaces

For graphs embedded on surfaces of Euler genus $g > 0$, one applies a cutting procedure:
1. Cut the surface along $O(g)$ shortest paths to produce a planar graph
2. Partition pairs by distance profile to the cutset
3. Within each partition, pairs induce a planar comatching structure
4. This multiplicative structure allows bounds to scale with genus

## Applications in Engineering

### Network Routing and Capacity Planning
- **Telecommunications networks:** Comatching constraints model link-disjoint paths required for fault-tolerant routing. The bound $\ell = O(1/\varepsilon)$ quantifies maximum concurrent protected paths.
- **Data center networking:** Ensures disjoint paths for backup routes in software-defined networks (SDNs) under spatial constraints.

### Graph Sparsification and Metric Embeddings
- **VC dimension analysis:** The comatching size relates to set system complexity, enabling efficient data structure design for metric range queries.
- **Approximation algorithms:** Bounds on comatching size derive hardness results for distance-constrained clustering and placement problems.

### Topological Data Analysis
- **Persistent homology:** Comatching structures appear in analyzing path components in filtered complexes.
- **Geometric graph analysis:** Used to bound the complexity of optimal geometric matchings under metric constraints.

### Computational Geometry
- **Planar subdivision schemes:** Comatching bounds govern the complexity of hierarchical decompositions in planar graphs.
- **Mobility networks:** Trajectory planning on surfaces where disjoint path constraints (e.g., vehicle routes) must respect topological boundaries.

## Common Mistakes / Pitfalls

1. **Assuming arbitrary disjointness suffices:** One might assume any pair of vertex-disjoint paths forms a valid comatching. The key constraint is that *cross-paths* $\langle p_i q_j \rangle$ and $\langle p_j q_i \rangle$ must be disjoint—a stronger, more subtle requirement.

2. **Confusing with standard matchings:** A comatching is not a matching (a set of edge-disjoint pairs). The pairs are vertex pairs with path-based constraints, not edge selections.

3. **Overlooking metric space dependence:** The bound $\ell = O(1/\varepsilon)$ assumes a specific metric and diameter constraint. Different metrics or relaxed constraints yield different bounds. The structure is not purely combinatorial.

4. **Misapplying to non-planar graphs directly:** The arrangement in