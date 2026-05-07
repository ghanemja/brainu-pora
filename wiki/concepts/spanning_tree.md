# Spanning Tree

## Definition

A **spanning tree** of a graph $G = (V, E)$ is an acyclic subgraph $T \subseteq G$ that:
- Contains all vertices in $V$ (is "spanning")
- Is connected
- Contains exactly $|V| - 1$ edges (is a tree)

In weighted or vertex-weighted graphs, a spanning tree maintains these structural properties while potentially optimizing for weight-related objectives (e.g., minimum total weight, balanced weight distribution across subtrees).

**Key property**: For any spanning tree $T$ of a connected graph $G$, adding any non-tree edge $e \notin T$ to $T$ creates exactly one fundamental cycle.

## Key Equations

For a connected graph $G$ with $n$ vertices:

$$|E_T| = n - 1 \quad \text{(number of edges in any spanning tree)}$$

**Fundamental cycle**: If $e = (u,v) \notin T$ and $P$ is the unique path from $u$ to $v$ in $T$, then:
$$C = P \cup \{e\}$$
is a fundamental cycle with respect to edge $e$.

**Balanced weight condition** (vertex-weighted case):
$$w(v) \leq \frac{1}{12} \sum_{u \in V} w(u) \quad \text{for all } v \in V$$

This ensures that removing any single vertex doesn't trivially unbalance the tree structure.

## Physical Intuition / Derivation

### Why Spanning Trees Matter

A spanning tree is a **minimal connectivity structure**: it connects all vertices with the fewest possible edges. Think of it as the "backbone" of a graph—remove any edge from a spanning tree and the graph becomes disconnected; add any edge back and you create exactly one cycle.

### Construction & Cycles

The fundamental cycle property emerges naturally: a connected graph with $n$ vertices needs at least $n-1$ edges. A spanning tree uses exactly this minimum. Any additional edge must close a loop with existing tree edges, forming a unique cycle.

### Role in Distributed Algorithms

In distributed computing (CONGEST model), spanning trees serve as:
1. **Communication scaffolds**: algorithms can propagate information along the tree with predictable latency
2. **Weight distribution mechanisms**: vertices transfer loads to incident faces/regions, avoiding double-counting
3. **Separator generators**: fundamental cycles in spanning trees can partition graphs into balanced components

The source material demonstrates that a path $P$ in a BFS spanning tree, combined with a carefully chosen non-tree edge, can form a 3/4-balanced separator (a cut that divides vertex weight nearly evenly) in $\tilde{O}(D)$ rounds, where $D$ is hop-diameter.

## Applications in Engineering

### 1. **Network Design & Routing**
- Telecommunication networks use spanning trees (protocols like STP—Spanning Tree Protocol) to eliminate loops and ensure every node is reachable with predictable routing
- Minimal edge set reduces infrastructure cost while maintaining connectivity

### 2. **Distributed Computing**
- **Parallel algorithms**: synchronize computation across processors using a spanning tree backbone
- **Distributed DFS/BFS**: fundamental operation for graph exploration in networked systems
- **Leader election and consensus**: tree structures simplify voting and aggregation

### 3. **VLSI & Circuit Design**
- **Clock distribution networks**: spanning trees minimize skew and propagation delay
- **Power distribution**: spanning trees model minimal-cost interconnect for delivering power to all circuit elements

### 4. **Graph Partitioning & Load Balancing**
- Spanning trees enable deterministic separator algorithms
- Used in mesh refinement, domain decomposition, and load distribution across parallel systems
- The source work applies this to maximum-flow, min-cut, and shortest-path problems on planar graphs

### 5. **Wireless Sensor Networks**
- Energy-efficient multi-hop routing via tree-based topologies
- Aggregation and in-network processing along tree edges

## Common Mistakes / Pitfalls

1. **Confusing "spanning tree" with "unique tree"**
   - A graph may have exponentially many spanning trees
   - Different algorithms (DFS, BFS, greedy) produce different trees
   - Application requirements determine which tree is suitable

2. **Assuming all spanning trees have equal weight**
   - In weighted graphs, spanning trees vary significantly in total edge weight
   - Minimum spanning tree (MST) is a specific optimization problem, not a property of all spanning trees
   - Vertex-weighted problems require explicit balance conditions (e.g., the 1/12 weight bound in the source material)

3. **Neglecting cycles**
   - Non-tree edges are not "redundant"; they're critical for robustness and cycle basis
   - Removing a tree edge disconnects; adding a non-tree edge closes a specific cycle
   - Failing to account for this leads to incorrect separator or partition algorithms

4. **Ignoring diameter constraints in distributed settings**
   - Tree depth (or diameter) directly bounds communication latency
   - BFS trees minimize diameter relative to a source; arbitrary spanning trees may be very deep
   - For $\tilde{O}(D)$ complexity, tree construction method matters

5. **Over-counting in weight/load distribution**
   - Naive assignment of vertex weight to multiple adjacent faces causes bias
   - The source material solves this elegantly: each vertex assigns weight to *one* face, ensuring exact count

## See Also

- [[Minimum Spanning Tree (MST)]] – optimization variant; see Kruskal's and Prim's algorithms
- [[Breadth-First Search (BFS)]] – constructive method producing spanning trees of minimal diameter
- [[Depth-First Search (DFS)]] – alternative spanning tree construction
- [[Graph Separators]] – use fundamental cycles from spanning trees to partition graphs
- [[Fundamental Cycle Basis]] – cycle space generated by non-tree edges relative to a spanning tree

## Sources

- Distributed planar graph algorithm paper (excerpt provided): focuses on deterministic $\tilde{O}(D)$-round spanning tree-based separator algorithms in the CONGEST model, with applications to DFS, shortest paths, max-flow, and min-cut
- Theorem 1 establishes that a 3/4-balanced separator can be found via a path in a spanning tree with careful weight assignment
- Fundamental cycles and their role in distributed graph algorithms, particularly for planar graphs with