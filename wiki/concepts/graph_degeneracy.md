# Graph Degeneracy

## Definition

A graph $G$ is **$k$-degenerate** if every subgraph of $G$ contains a vertex of degree at most $k$. Equivalently, the **degeneracy** $d(G)$ of a graph is the smallest integer $k$ such that $G$ is $k$-degenerate.

More formally:
$$d(G) = \min\{k : \text{every subgraph } H \subseteq G \text{ has } \delta(H) \leq k\}$$

where $\delta(H)$ denotes the minimum vertex degree in $H$.

### Characterization via Ordering

A graph $G$ is $k$-degenerate if and only if there exists an **acyclic ordering** (or degeneracy ordering) of vertices $v_1, v_2, \ldots, v_n$ such that each vertex $v_i$ has at most $k$ neighbors among $\{v_{i+1}, \ldots, v_n\}$ (i.e., neighbors that appear later in the ordering).

## Key Equations

**Bound on edge count:**
$$|E(G)| \leq d(G) \cdot |V(G)| - \binom{d(G)+1}{2}$$

For large graphs, this simplifies to:
$$|E(G)| = O(d(G) \cdot |V(G)|)$$

**Relationship to average degree:**
$$\bar{d}(G) \leq 2d(G)$$

The average degree is at most twice the degeneracy.

**Iterative removal bound:**
When successively removing minimum-degree vertices, if the degeneracy is $d$, then at step $i$:
$$\min_v \deg_i(v) \leq d$$

where $\deg_i(v)$ is the degree of $v$ in the remaining graph.

## Physical Intuition / Derivation

### Why Degeneracy Matters

Degeneracy captures the **sparsity structure** of a graph—it measures how "recursively sparse" the graph is. Unlike density measures (e.g., average degree) that only characterize the whole graph, degeneracy ensures *every* subgraph is sparse.

### Intuitive Construction

Consider building a graph one vertex at a time by **reverse removal order**:
1. Start with an empty graph
2. Add vertices in the order $v_n, v_{n-1}, \ldots, v_1$
3. When adding $v_i$, connect it to at most $k$ previously added vertices

This process generates a $k$-degenerate graph. Conversely, any $k$-degenerate graph admits such a construction—this is guaranteed by the degeneracy ordering theorem.

### Why the Iterative Reduction Works

The source material's iterative removal process (moving vertices from $U$ to $\dot{U}$ while removing neighbors) exploits degeneracy:
- A vertex $v$ in a sparse graph has bounded neighbors in any neighborhood $B_r(v)$
- By Lemma 6.1, max degree $\leq 30$ in $V^+$, bounding the "reach" of removals
- This allows partitioning the vertex set into independent reducible subproblems

### Charge Distribution Principle

The source material uses a **charging argument** on vertex degrees:
$$\sum_{v \in V^-} d(v) \leq -\sum_{v \in V^-} 31 \cdot T(v) < 31 \sum_{v \in V^+} T(v) \leq 31 \cdot 54 \cdot |V^+|$$

This bounds negatively charged vertices by their degree contribution, which is controlled by degeneracy properties of the subgraph they induce.

## Applications in Engineering

### 1. **VLSI Circuit Design**
- **Constraint satisfaction:** Circuits with bounded degeneracy allow efficient scheduling and resource allocation
- **Sparse matrix problems:** Circuit netlist hypergraphs are often degenerate; this enables linear-time analysis algorithms
- Example: Checking routability in placement with bounded-degree subgraph conditions

### 2. **Network Analysis**
- **Peer-to-peer networks:** Bounded degeneracy ensures distributed algorithms (like gossip protocols) converge efficiently
- **Graph coloring in wireless networks:** Low degeneracy implies small chromatic number $\chi(G) \leq d(G) + 1$, simplifying channel assignment
- **Anomaly detection:** Sudden degeneracy increases (dense subgraphs) indicate community formation or attacks

### 3. **Computational Geometry**
- **Mesh generation:** Planar graphs (degeneracy $\leq 5$) guarantee quality bounds on triangle mesh properties
- **Intersection graphs:** Geometric intersection graphs often have bounded degeneracy, enabling efficient range queries

### 4. **Algorithm Design**
- **Linear-time algorithms:** Many NP-hard problems become polynomial (even linear) on degenerate graphs:
  - Coloring: $O(n + m)$ greedy algorithm achieves $(d+1)$-coloring
  - Independent set enumeration: exponential only in $d$, not $n$
- **Memory-efficient processing:** Streaming algorithms can process vertices in degeneracy order with bounded buffer size

### 5. **Combinatorial Optimization**
- **Graph minor testing:** K4-minor testing in planar graphs uses degeneracy $\leq 3$ structure
- **Parameterized complexity:** Many hardness results parametrized by $d(G)$ rather than $|V(G)|$

### 6. **Machine Learning on Graphs**
- **Graph neural networks:** Degenerate graphs admit efficient node ordering for sequential processing
- **Kernel methods:** Degeneracy bounds VC dimension in graph kernels

## Common Mistakes / Pitfalls

### 1. **Confusing Degeneracy with Average Degree**
❌ **Wrong:** "A 30-degenerate graph has average degree 30"
✓ **Correct:** Average degree is *at most* 60; many vertices may have degree 1

### 2. **Assuming Weak Local Structure Implies Global Sparsity**
❌ **Wrong