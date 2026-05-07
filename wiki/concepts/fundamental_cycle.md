# Fundamental Cycle

## Definition

A **fundamental cycle** is a cycle formed in an undirected graph by adding a single non-tree edge to a spanning tree. Formally, given a spanning tree $T$ of graph $G$ and a non-tree edge $e = (u, v) \notin T$, the fundamental cycle is the unique cycle formed by $e$ together with the unique path between $u$ and $v$ in $T$:

$$C_e = P_T(u,v) \cup \{e\}$$

where $P_T(u,v)$ denotes the unique tree path connecting vertices $u$ and $v$ in $T$.

Each non-tree edge generates exactly one fundamental cycle, and the set of all fundamental cycles forms a **fundamental cycle basis** for the graph.

## Key Equations

For a graph $G = (V, E)$ with a spanning tree $T$:

- **Number of fundamental cycles**: $|E| - |V| + 1$ (the cyclomatic complexity or circuit rank)
- **Fundamental cycle basis size**: equals the dimension of the cycle space, denoted $\nu(G) = m - n + c$ where $m = |E|$, $n = |V|$, and $c$ is the number of connected components

For weighted vertex-balanced separator applications:
$$\text{Weight}(P) \leq \frac{3}{4} \cdot \text{Weight}(G)$$

where $P$ is a path in the spanning tree, ensuring that the fundamental cycle created by adding edge $e = (u,v)$ produces a balanced separator.

## Physical Intuition / Derivation

**Why fundamental cycles matter:**

Consider building a spanning tree by progressively adding edges—you can add exactly $n-1$ edges without creating any cycles. Once you add any additional edge beyond these $n-1$, you immediately close a cycle. This new edge, combined with the tree's unique path between its endpoints, forms a fundamental cycle.

**Geometric intuition:** In planar graph embeddings, each non-tree edge "cuts across" the tree structure, creating a cycle that encloses a well-defined region. For separator algorithms (as in the source material), adding a non-tree edge to a balanced tree path creates a fundamental cycle that partitions the graph into interior and exterior regions.

**Why this matters for distributed algorithms:** The hop-diameter $D$ bounds the length of any tree path. When a spanning tree $T$ (constructed as a BFS tree with root $r$) is augmented with a non-tree edge to close a fundamental cycle, the resulting cycle-path separator has size $O(D)$ in terms of hop distance, enabling efficient distributed computation in $\tilde{O}(D)$ rounds.

## Applications in Engineering

### 1. **Distributed Graph Algorithms**
The fundamental cycle concept directly enables deterministic distributed algorithms for:
- Depth-first search (DFS)
- Single-source shortest paths
- Maximum flow computation
- Minimum cut detection
- Reachability queries

All these can be derandomized using fundamental cycle-based separators in the CONGEST model.

### 2. **Graph Partitioning & Load Balancing**
Fundamental cycles provide natural partitioning boundaries. In distributed systems, splitting computation along fundamental cycle separators achieves balanced workload distribution without randomization, crucial for predictable performance in embedded planar graphs (common in mesh networks, circuit routing).

### 3. **Circuit Analysis & Network Flow**
In electrical circuit analysis, fundamental cycles correspond to independent mesh equations. Kirchhoff's voltage law is applied to fundamental cycles to determine loop currents:
$$\sum_{e \in C_i} v_e = 0$$

### 4. **Planarity Testing & Graph Embedding**
Fundamental cycles help verify planarity. A graph is planar iff its cycle space can be realized as face boundaries—fundamental cycles are generators of this space.

### 5. **Mesh Generation & Finite Element Methods**
In computational geometry, fundamental cycles in triangulation graphs guide adaptive refinement strategies and quality assurance for FEM mesh topology.

## Common Mistakes / Pitfalls

1. **Confusing with the cycle basis:** Not all cycles are fundamental cycles. A graph may have cycles that require combinations of multiple fundamental cycles to express. Fundamental cycles are the *minimal generating set* of the cycle space.

2. **Tree-dependency:** A fundamental cycle depends entirely on the choice of spanning tree. Different spanning trees generate different fundamental cycle bases for the same graph. There is no "the" fundamental cycle—only fundamental cycles *with respect to* a particular tree.

3. **Assuming uniqueness of the path:** Once $T$ is fixed, the path $P_T(u,v)$ is unique. However, adding different non-tree edges yields different fundamental cycles. Don't conflate the tree structure with cycle properties.

4. **Weight distribution errors:** In weighted settings (as in the source material), each vertex must transfer weight to exactly *one* face/cycle, not multiple faces. Overcounting destroys the balance guarantee. Ensure: 
   $$\sum_{v \in V} w(v) = \text{total weight}$$
   with each vertex counted exactly once across all cycles.

5. **Hop-diameter misconception:** The hop-diameter $D$ bounds the tree path length, but does *not* directly bound the number of vertices in a fundamental cycle. In dense graphs, a short path in hops may traverse many edges.

## See Also

- [[Spanning Tree]] — The tree structure that defines fundamental cycles
- [[Graph Cycle Basis]] — The algebraic structure of which fundamental cycles are generators
- [[Graph Separator]] — How fundamental cycles create vertex partitions for divide-and-conquer algorithms
- [[Planar Graph]] — Geometric setting where fundamental cycles correspond to faces
- [[CONGEST Model]] — Distributed computing model where fundamental cycle algorithms are applied

## Sources

- Distributed planar graph algorithm paper featuring deterministic $\tilde{O}(D)$-round separator algorithms using fundamental cycles (Theorem 1 and surrounding discussion)
- Analysis of balanced weight distribution and vertex-to-face assignment schemes avoiding overcounting in fundamental cycles
- Applications to DFS, shortest paths, maximum flow, and global min-cut in the distributed CONGEST model