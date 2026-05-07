# Subtree sum computation

## Definition

**Subtree sum computation** is a distributed graph algorithm procedure that, given a rooted tree $T$ with a designated root $r$, computes for each node $u$ the aggregate sum of all values in the subtree rooted at $u$. In the CONGEST distributed computing model, this operation must be completed using local message passing where each node can send $O(\log n)$ bits per round to its neighbors.

Formally, given:
- A tree $T = (V, E)$ with designated root $r \in V$
- Input values $x_v$ associated with each vertex $v \in V$

The goal is for every node $u$ to compute:
$$S_u = \sum_{v \in \text{subtree}(u)} x_v$$

where $\text{subtree}(u)$ denotes all vertices in the subtree rooted at $u$ (including $u$ itself).

## Key Equations

The fundamental recurrence relation underlying subtree sums is:

$$S_u = x_u + \sum_{w \in \text{children}(u)} S_w$$

where $\text{children}(u)$ denotes the set of immediate children of node $u$ in the rooted tree.

**Round Complexity Bound (Lemma 8):**

For a tree $T$ rooted at vertex $r$, deterministic subtree sum computation requires:
$$\tilde{O}(1) \text{ part-wise aggregations}$$

where $\tilde{O}$ suppresses logarithmic factors. This translates to $\tilde{O}(D)$ rounds on a general graph of diameter $D$ when combined with low-congestion shortcuts.

For the dual-graph version (Lemma 11), the complexity is similarly:
$$\tilde{O}(D) \text{ deterministic rounds}$$

## Physical Intuition / Derivation

### Why This Is Non-Trivial

In a centralized setting, subtree sums can be computed via a single DFS traversal in $O(n)$ time. However, in distributed computing, information propagates at network speed: a message can travel at most one hop per round. Thus naive approaches that gather all subtree values to the root require $\Omega(D)$ rounds where $D$ is the tree diameter.

### The Key Insight: Aggregation Pipelining

The efficiency arises from **part-wise aggregations**—a technique that leverages tree structure:

1. **Bottom-up phase**: Leaf nodes and nodes at minimal depth send their local sums upward to parents. Rather than waiting for the entire subtree to report, parents begin computing partial aggregates as information arrives.

2. **Pipelining opportunity**: While a node is communicating its subtree sum upward, its children can simultaneously process their children's contributions. This temporal overlap, combined with careful scheduling using low-congestion shortcuts, reduces the critical path.

3. **Low-congestion shortcuts role**: When the original graph $G$ has large diameter $D$, a partition of $G$ into vertex-disjoint subgraphs $\{G_i\}$ is constructed. Low-congestion shortcuts $\{H_i\}$ ensure that:
   - Each component $G_i \cup H_i$ has small diameter
   - No edge is overloaded (appears in at most $c = \tilde{O}(D)$ shortcuts)
   
   This allows tree algorithms to be efficiently simulated on the restricted graph topology.

### Derivation Sketch for Dual-Tree Case (Lemma 11)

The dual-tree procedure operates on the face-graph $G^*$ of a planar graph:
- Vertices of $G^*$ correspond to faces of $G$
- The algorithm must first establish which vertices of $G$ belong to which faces (Lemma 9)
- Then aggregate values per face (Lemma 10)
- Finally, compute subtree sums over the spanning tree $T^*$ of $G^*$ using the same bottom-up aggregation strategy

## Applications in Engineering

### 1. Planar Mesh Processing (Finite Element Analysis)

In computational mechanics, planar triangulations represent discretized domains. Computing subtree sums over face-trees enables:
- **Distributed load aggregation**: Summing distributed loads from all sub-regions below a given hierarchical partition
- **Centroid and moment calculations**: Aggregating geometric or physical quantities across mesh regions in parallel

### 2. Network Routing and Congestion Analysis

In distributed routing protocols:
- Computing subtree sums over routing trees aggregates traffic statistics (packet counts, bytes transmitted) for each subtree
- Enables load-balancing decisions without centralizing all statistics at the root
- Critical for **congestion detection** at intermediate routers

### 3. Distributed Linear Algebra (Graph Laplacian Solvers)

Modern distributed algorithms for solving linear systems $Ax = b$ on graphs:
- Require computing aggregates over tree-structured sub-problems
- Subtree sums support the iterative refinement phases in methods like **conjugate gradient**
- Used in spectral clustering and graph partitioning algorithms

### 4. Distributed Tree-Structured Machine Learning

Decision tree inference in federated/edge environments:
- Each node in the tree may coordinate decisions across multiple sub-models
- Subtree sum computation aggregates prediction confidences or gradient contributions bottom-up
- Enables privacy-preserving inference where leaf nodes don't communicate directly with root

### 5. Topology Control and Hierarchical Clustering

In wireless sensor networks and ad-hoc networks:
- Computing subtree sums over hierarchical cluster trees aggregates **energy reserves**, **hop counts**, or **signal strengths**
- Supports adaptive protocol decisions based on global subtree properties without global broadcast

## Common Mistakes / Pitfalls

### 1. **Confusing Primal and Dual Computations**

A common error is treating subtree sums on faces (Lemma 11) the same as subtree sums on vertex trees (Lemma 8). The dual case requires:
- Knowledge of face IDs (obtained via Lemma 9)
- Mapping vertex values to face values
- Handling the fact that a single vertex participates in *multiple* incident faces

Forgetting to account for multi-face participation leads to incorrect aggregations.

### 2. **Underestimating Diameter Effects**