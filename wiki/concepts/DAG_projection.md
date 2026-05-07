# DAG Projection

## Definition

A **DAG projection** is a directed acyclic graph (DAG) constructed as a graph transformation that approximates properties of an arbitrary directed graph while preserving tractability for distance and flow computations.

### Formal Construction

Given a directed graph $G = (V, G) \to V(G) \cup \{\perp\}$ is a surjective mapping where:
- Vertices $u' \in \pi^{-1}(u)$ for $u \in V(G)$ are **copies** of vertex $u$
- Vertices $u' \in \pi^{-1}(\perp)$ are **Steiner vertices** (auxiliary vertices with no original preimage)

The **width** of $G'$ is defined as:
$$w(G') = \max_{u \in V(G)} |\pi^{-1}(u)|$$

A projection $G'$ is a **DAG projection** if and only if $G'$ is acyclic (contains no directed cycles).

### Key Structural Properties

| Property | Measure |
|----------|---------|
| Size (edges) | $\|E(G')\| = m^{1+o(1)}$ or $O(m \log^3 n)$ |
| Width | $w(G') = n^{o(1)}$ or $O(\log n)$ |
| Vertices | $\|V(G')\| = n^{1+o(1)}$ or $O(n \log n)$ |

## Key Equations

### Distance Preservation Guarantee

For a $(1+\varepsilon)$-distance-preserving DAG projection $G'$:

$$\mathrm{dist}_G(s,t) \leq \mathrm{dist}_{G'}(\pi^{-1}(s), \pi^{-1}(t)) \leq (1+\varepsilon) \mathrm{dist}_G(s,t)$$

where $\mathrm{dist}_{G'}(\pi^{-1}(s), \pi^{-1}(t))$ denotes the shortest path distance from any copy of $s$ to any copy of $t$ in $G'$.

### Query Cost

To compute distance between original vertices $s, t$:
$$\mathrm{dist}_{G'}(\pi^{-1}(s), \pi^{-1}(t)) = \min_{s' \in \pi^{-1}(s), t' \in \pi^{-1}(t)} \mathrm{dist}_{G'}(s', t')$$

This can be computed by adding zero-weight dummy edges from source $s_0 \to \pi^{-1}(s)$ and $\pi^{-1}(t) \to t_0$, then finding $\mathrm{dist}_{G'}(s_0, t_0)$.

### Size-Approximation Tradeoff

For distance approximation:
$$\text{Approximation} \times \text{Size} \approx O(\log n \log \log n) \text{ to } (1 + 1/\mathrm{polylog}(n)) \text{ with } m^{1+o(1)}$$

## Physical Intuition / Derivation

### Why DAGs?

Directed graphs with cycles pose fundamental difficulties for sparse approximation:
- **Cycles create shortcuts**: A cycle allows arbitrary reweighting of paths
- **No tree decomposition**: Unlike undirected graphs, directed graphs don't admit good tree cuts naturally
- **DAGs are structured**: By breaking cycles through duplication and Steiner vertices, we gain acyclicity

### Construction Philosophy

DAG projections work by:

1. **Vertex Multiplication**: Create multiple "copies" of high-degree or high-traffic vertices to distribute flow paths
2. **Steiner Insertion**: Add auxiliary vertices to reroute paths through low-weight edges
3. **Acyclicity by Design**: Ensure all edges in $G'$ are oriented such that no cycles form

This is analogous to **network decomposition** in parallel computing: instead of fighting the original graph's structure, we transform it into a tractable form.

### Why Size is $m^{1+o(1)}$

- Previous approaches achieved $O(m \log^3 n)$ with polylog approximation
- Subpolynomial factors $m^{o(1)}$ come from:
  - Width: $n^{o(1)}$ copies per vertex
  - Degree preservation: Each original edge spawns $\text{polylog}(n)$ edges in $G'$
  - Total: $m \cdot \text{polylog}(n) = m^{1+o(1)}$

## Applications in Engineering

### Network Routing and Traffic Engineering

**Distance-Approximating DAGs** enable scalable algorithms for:
- **OSPF/BGP simulation**: Approximate all-pairs shortest paths for large networks without storing full routing tables
- **Latency prediction**: Quickly estimate end-to-end delays in data center networks
- Trade 0.1% approximation error for orders-of-magnitude speedup in query time

### Maximum Flow / Network Design

**Flow-approximating DAGs** (Theorem 1.2) provide:
- **Congestion minimization**: Route flows approximately optimally using sparse DAG structure
- **Circuit design**: DAGs model acyclic hardware paths; approximations guide placement/routing
- **Supply chain optimization**: Directed commodity flows in acyclic production networks

### Large-Scale Graph Processing

- **MapReduce/Spark**: Store compressed graph representation that fits in distributed cache
- **Stream processing**: Maintain small DAG to answer distance/flow queries on streaming edges
- **Dynamic shortest paths**: Incrementally maintain DAG projections as graph evolves

### Machine Learning on Graphs

- **Graph neural networks**: Use DAG projection as backbone for sparse computation graphs
- **Knowledge graphs**: Compress RDF/property graphs into flow-approximating DAGs
- **Computational graphs**: TensorFlow/PyTorch use implicit DAGs; projection theory explains sparsification

## Common Mistakes / Pitfalls

### 1. Confusing "Width" with "Number of Copies"

**Wrong**: "A width-$k$ projection uses $k