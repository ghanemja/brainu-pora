# Signed Tree Models

## Definition

A **signed tree model** of a graph $G = (V, E)$ is a compact hierarchical representation consisting of:

1. A **rooted binary tree** $T$ whose leaves are in bijective correspondence with the vertices of $V(G)$
2. A set of **transversal pairs** (edges in $T$): pairs of nodes $(x, y)$ in $T$, each colored with one of two colors (conventionally interpreted as "biclique" or "anti-biclique")
3. **Semantics**: Each transversal pair $(x, y)$ with color $c$ induces edges between all pairs of vertices $(u, v)$ where $u$ is a leaf in the subtree rooted at $x$ and $v$ is a leaf in the subtree rooted at $y$:
   - If $c$ indicates a **biclique**, all such pairs are connected in $G$
   - If $c$ indicates an **anti-biclique**, no such pairs are connected in $G$

**Formally**: A signed tree model is the tuple $(T, \Phi, \sigma)$ where:
- $T$ is a rooted binary tree
- $\Phi: V(G) \to \text{Leaves}(T)$ is a bijection
- $\sigma: E(T) \to \{\text{biclique}, \text{anti-biclique}\}$ assigns colors to edges used as transversal pairs

The **width** of a signed tree model is the number of transversal pairs $p$.

## Key Equations

**Single-Source Shortest Path Runtime:**
$$\text{Time}(SSSP) = O(p \log n)$$

where $p$ is the number of transversal pairs and $n = |V(G)|$.

**All-Pairs Shortest Path Runtime (bounded merge-width $w$):**
$$\text{Time}(APSP) = O(n^2 \log n)$$

**All-Pairs Shortest Path Runtime (symmetric difference $\Delta$ with $\Delta = O(n^{1/3})$):**
$$\text{Time}(APSP) = O(n^{7/3} \log^2 n)$$

**Sparse Representation Guarantee:**
For graph classes of bounded width parameter, the number of transversal pairs satisfies:
$$p = O(n)$$

## Physical Intuition / Derivation

### Why Tree Models Work

Signed tree models exploit **recursive decomposition** of vertex sets. The key insight is that graphs with modest structural regularity (measured by width parameters) can be recursively partitioned into two groups whose connectivity is described by simple rules:

1. **Hierarchical Partitioning**: The binary tree recursively splits the vertex set. At each level, vertices are grouped into two subtrees.

2. **Simplified Connectivity Rules**: Rather than storing all $O(n^2)$ edges, transversal pairs encode **bipartite structure**. A single transversal pair with color "biclique" implicitly represents many edges simultaneously (potentially $\Theta(n^2)$ edges from a single pair).

3. **Width Measures**: Graph classes like those with bounded:
   - **Twin-width**: measures how many "twins" (structurally similar vertices) must be distinguished
   - **Merge-width**: dual to twin-width; measures difficulty of hierarchically merging vertices
   - **Flip-width**: counts cost of local edits
   - **Degeneracy**: bounded maximum degree in subgraphs

   all admit signed tree models with $O(n)$ transversal pairs.

### Why This Enables Fast Shortest Paths

The algorithm exploits the compact representation during BFS/Dijkstra traversal:
- Instead of iterating over $O(n^2)$ edges, iterate over $O(p) = O(n)$ transversal pairs
- Each transversal pair connects two subtrees; process all cross-edges in bulk
- The tree structure and binary representation allow efficient frontier updates in $O(\log n)$ amortized time per pair

## Applications in Engineering

### 1. **Network Analysis with Structural Constraints**
When network topologies have known recursive structure (e.g., hierarchical data centers, organizational networks), signed tree models provide compact representations enabling rapid distance queries and routing computation.

### 2. **First-Order Model Checking**
Computing logical properties of graphs with witnesses (low merge-width, low twin-width) reduces from cubic to quadratic time, making verification of large systems tractable.

### 3. **Graph Algorithms on Structured Data**
- **Social networks**: bounded twin-width characterizes many real social graphs
- **Biological networks**: hierarchical modular structure is common
- **Road networks**: geographic structure often yields low width parameters

### 4. **Matrix Multiplication and Reachability**
Bounded twin-width graphs enable $O(n^2 \log n)$ APSP and related algorithms, useful for:
- Transitive closure computation
- Diameter and radius computation
- Centrality measures (eccentricity, Wiener index)

### 5. **Parameterized Complexity**
Signed tree models serve as **structural witnesses** for fixed-parameter tractable (FPT) algorithms, allowing algorithms parameterized by structural width parameters rather than $n$ or $m$ alone.

## Common Mistakes / Pitfalls

### 1. **Confusing Width with Edge Count**
A signed tree model with $p = O(n)$ transversal pairs does **not** imply the graph has $O(n)$ edges. Transversal pairs encode bicliques/anti-bicliques that can represent $\Theta(n^2)$ edges. The power lies in **implicit representation**.

### 2. **Assuming Width Parameters Are Equivalent**
Twin-width, merge-width, flip-width, and degeneracy are **related but distinct**. A graph may have low twin-width but high degeneracy (or vice versa). Always verify which parameter bound applies.

### 3. **Forgetting the Input Assumption**
The $O(p \log n)$ SSSP algorithm assumes the **signed tree model is given as input**. Computing the model itself may be expensive (NP-hard in some cases). Applications only benefit when a witness is provided or can be computed efficiently.

### 4. **