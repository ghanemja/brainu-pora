# k-core decomposition

## Definition

A **k-core** of a graph $G = (V, E)$ is a maximal subgraph $H \subseteq G$ in which every vertex has degree at least $k$ within $H$. The **k-core decomposition** is the process of recursively identifying and removing all k-cores from a graph, partitioning vertices into coreness levels.

More formally:
- A vertex $v$ has **coreness** $c(v) = k$ if it belongs to the $k$-core but not to the $(k+1)$-core.
- The **core number** of a graph is the maximum $k$ for which a non-empty $k$-core exists.

## Key Equations

The coreness of a vertex can be computed iteratively through peeling:

$$c(v) = \max \{ k : v \text{ remains after } k \text{ iterations of removing degree-0 vertices} \}$$

**Degeneracy relationship**: A graph with degeneracy $d$ has maximum core number equal to $d$:
$$\text{coreness}_{\max}(G) = \text{degeneracy}(G)$$

where degeneracy is the minimum $d$ such that every subgraph has a vertex of degree $\leq d$.

## Physical Intuition / Derivation

### Understanding k-cores Through Iterative Peeling

Think of k-core decomposition as repeatedly "stripping away" the periphery of a graph:

1. **Round 0**: Identify all vertices with degree $< k$. These have coreness $< k$.
2. **Round 1**: Remove those vertices (and their incident edges). Recompute degrees in the remaining subgraph.
3. **Repeat**: Continue until no vertices remain with degree $< k$.

Any vertex that survives $k$ complete rounds of this process has **at least coreness $k$**.

### Why This Matters

- **Dense clusters**: Vertices in a k-core form a densely connected substructure (minimum degree $k$).
- **Robustness measure**: A high coreness indicates a vertex is embedded in a tightly connected region—removing peripheral nodes doesn't disconnect it.
- **Hierarchical structure**: The nested sequence of k-cores reveals hierarchical community structure in networks.

### Algorithmic Observation

The greedy peeling algorithm is optimal:
$$\text{Time complexity} = O(|V| + |E|)$$

This is because each vertex is examined at most once per removal phase, and total phases $\leq$ maximum degree.

## Applications in Engineering

### 1. **Network Analysis & Social Networks**
- Identifying influential or tightly-knit subgroups
- Community detection by examining high-coreness layers
- Spam/bot detection (peripheral nodes often have low coreness in legitimate networks)

### 2. **Biological Networks**
- Protein interaction networks: k-cores identify protein complexes with strong internal interactions
- Gene regulatory networks: high-coreness genes often represent core regulatory hubs

### 3. **Citation & Knowledge Networks**
- Finding seminal papers/concepts (high coreness = frequently co-cited with many peers)
- Identifying key research communities by coreness level

### 4. **Graph Visualization**
- Layered drawing: place vertices by coreness; high-coreness vertices in center, low-coreness at periphery
- Reduces clutter and reveals structure

### 5. **Scalability in Parallel Systems**
- **Batch-dynamic k-core decomposition** [[20]] enables efficient updates when edges are added/removed in batches
- Critical for streaming graph analysis where edges arrive continuously
- Practical parallelization exploits independence of peeling rounds

### 6. **Graph Coloring & Independent Sets**
- k-core decomposition relates to $(k+1)$-coloring problems [[19]]
- Degeneracy bounds the chromatic number: $\chi(G) \leq \text{degeneracy}(G) + 1$

## Common Mistakes / Pitfalls

### 1. **Confusing k-core with k-clique**
- A k-core requires each vertex to have degree $\geq k$ *within the subgraph*, not a clique.
- A k-clique is much more restrictive: $\binom{k}{2}$ required edges vs. $\geq k \cdot k/2$ in a k-core.

### 2. **Thinking k-cores are unique per layer**
- The $(k+1)$-core is always a subgraph of the $k$-core, but intermediate removals are order-dependent in naïve implementations.
- Coreness (the final assignment) is unique; the decomposition process is not.

### 3. **Underestimating complexity in dynamic settings**
- Naïve updates after edge insertion can require recomputing entire decomposition: $O(|V| + |E|)$ per update.
- Batch algorithms amortize this cost: multiple updates before recomputation.

### 4. **Applying to directed graphs without care**
- Definition extends to directed graphs (in-degree, out-degree, or both).
- Must clarify which variant; results differ significantly.

### 5. **Ignoring degeneracy as a key parameter**
- If degeneracy $d$ is small, decomposition is very fast and layers are thin.
- For dense graphs with large $d$, k-cores may provide little insight.

## See Also

- [[Graph degeneracy]] – fundamental parameter bounding k-core decomposition
- [[Community detection]] – k-cores used for hierarchical clustering
- [[Maximal independent set]] – related parallel algorithm techniques [[21]]
- [[Graph coloring]] – chromatic number bounded by degeneracy via k-cores [[19]]
- [[Batch-parallel graph algorithms]] – practical scalability of dynamic k-core updates [[20]]

## Sources

- [20] Q. Liu, J. Shi, L. Dhulipala, and J. Shun. "Parallel batch-dynamic k-core decomposition and related graph problems." *ACM Symposium on Parallelism in Algorithms and Architectures (SPAA)*, 2022.
- [19] Öjvind Johansson. "Simple distributed (δ+1)-coloring of graphs." *Information Processing Letters*, 70(5