# Clique Partition

## Definition

A **clique partition** of a graph $G = (V, E)$ is a partition $P$ of the vertex set $V$ into disjoint subsets $C_1, C_2, \ldots, C_m$ such that each subset $C_i$ forms a **clique** (a complete subgraph where every pair of vertices is connected by an edge).

Formally:
- $C_i \cap C_j = \emptyset$ for all $i \neq j$
- $\bigcup_{i=1}^{m} C_i = V$
- For each $C_i \in P$, the induced subgraph $G[C_i]$ is a complete graph $K_{|C_i|}$

The **clique partition number** $\kappa(G)$ is the minimum number of cliques required to partition $V(G)$.

A **clique size bound** restricts each clique to have size at most $l$: $|C| \leq l$ for all $C \in P$.

## Key Equations

The relationship between clique partition and contraction operations:

$$G_{/X} = G/E(G[X])$$

where $G_{/X}$ denotes the graph obtained by contracting all edges in the induced subgraph $G[X]$ (equivalently, collapsing each connected component of $G[X]$ into a single vertex).

For bounded clique partitions with parameter $l$, the **treewidth scaling property** holds:

$$\text{tw}(G_{/X_i}) = O(kl)$$

when sets $X_1, \ldots, X_k$ satisfy $\sum_{i=1}^{k} |X_i| = O(|P|l)$ and each clique has size $\leq l$.

## Physical Intuition / Derivation

### Why Clique Partitions Matter

Clique partitions decompose a graph into maximal cohesive regions—sets of mutually connected vertices. This is useful because:

1. **Structural Simplification**: Many NP-hard problems become tractable when the graph has bounded clique size or few cliques. Algorithms can handle each clique independently, then combine results.

2. **Hierarchical Approximation**: A clique partition $P$ can be viewed as a "quotient graph" $G_P$ where each vertex represents a clique. This abstraction is coarser than the original graph but retains connectivity information.

3. **Contraction-Based Decomposition**: When decomposing a graph for algorithms (e.g., treewidth-based DP), contracting vertices within a clique doesn't break internal structure—the clique remains complete. This enables controlled reduction of graph size while preserving treewidth bounds.

### Key Insight from Source Material

The source illustrates a sophisticated application: to handle graphs with bounded clique partitions efficiently, one can:
- Use the clique partition $P$ to define quotient graph $G_P$
- Find a planar approximation $H$ via Lipschitz embedding
- Apply contraction decomposition to $H$, then lift results back to $G$
- Expand each clique (of size $\leq l$) when estimating treewidth: if $G_P$ achieves treewidth $O(k)$ after contractions, then $G$ achieves $O(kl)$ since each clique introduces $l$ vertices

This avoids the naive approach (which fails) of trying to directly approximate $G_P$ with a grid representation.

## Applications in Engineering

### 1. **Computational Geometry & Intersection Graphs**
Graphs derived from geometric objects (unit disks, fat objects) naturally have bounded clique partitions corresponding to densely packed regions. This enables:
- Steiner tree approximation algorithms
- Network design with geometric constraints
- Rapid facility location problems

### 2. **VLSI & Circuit Design**
Clique partitions model **interference graphs** in circuit layouts:
- Vertices = components/nets
- Edges = interference/conflict relationships
- Cliques = groups of mutually interfering elements
- Partitioning minimizes cross-talk and scheduling complexity

### 3. **Scheduling & Resource Allocation**
In scheduling problems (e.g., frequency assignment, processor allocation):
- Each clique represents a set of tasks/resources that must be handled together
- Partition size bounds directly translate to resource requirements
- Reduces complexity of conflict resolution

### 4. **Network Optimization**
For communication networks with QoS constraints:
- Cliques represent densely connected regions (clusters)
- Partition bounds enable bounded-resource routing
- Supports polynomial-time approximation algorithms for problems like minimum bottleneck paths

### 5. **Machine Learning & Data Clustering**
Graph-based clustering uses clique detection:
- Cliques identify dense subgraphs (cohesive groups in social networks, protein complexes in biology)
- Bounded clique partitions provide guarantees on cluster homogeneity

## Common Mistakes / Pitfalls

### 1. **Confusing Clique Partition with Clique Cover**
- **Clique partition**: disjoint cliques covering all vertices (a partition)
- **Clique cover**: arbitrary collection of cliques covering all vertices (may overlap)
- The clique partition number $\kappa(G)$ is **always $\geq$ clique cover number**

### 2. **Assuming Clique Partition Size Equals Chromatic Number**
- Clique partition size (vertex coloring in complement graph) and chromatic number are distinct
- For a graph $G$: $\kappa(G)$ is the chromatic number of $\overline{G}$ (the complement), not $G$

### 3. **Overlooking Hidden Edges in Contractions**
When contracting $G_{/X}$, edges within $G[X]$ are removed, but:
- Multi-edges do not form in standard graph contractions
- The resulting treewidth bound depends carefully on the structure preserved
- Naive contraction may lose critical structural properties

### 4. **Over-Generalizing Planar Graph Results**
The source notes that contraction decomposition theorems for unit disk graphs are insufficient for general fat object intersection graphs. Don't assume:
- Results for specific graph classes (planar,