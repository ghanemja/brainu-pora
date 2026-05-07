# Layering Tree

## Definition

A **layering tree** is a hierarchical tree structure constructed from a graph $G = (V, E)$ by decomposing it into layers based on shortest-path distances from a source vertex. It provides a coarse structural summary of the original graph.

### Formal Construction

Given a connected graph $G = (V, E)$ and a source vertex $s \in V$:

1. **BFS Layers**: Define layer $i$ as
   $$L_i = \{v \in V \mid d_G(s, v) = i\}$$
   where $d_G(s,v)$ is the shortest path distance. We use $L_{\leq k} = L_0 \cup \cdots \cup L_k$ and $L_{\geq k} = L_k \cup \cdots \cup L_{n-1}$.

2. **Connected Components**: For each layer $i$, let $S_i = \{S_i^1, \ldots, S_i^{s_i}\}$ denote the set of connected components of $G \setminus L_{\leq i-1}$.

3. **Parts**: The **parts** at layer $i$ are the intersections:
   $$P_i = \{P_i^1, \ldots, P_i^{s_i}\} \quad \text{where} \quad P_i^j = S_i^j \cap L_i$$
   Each part is the subset of vertices in a connected component that actually belong to layer $i$.

4. **Layering Tree**: The tree $T = (P, E_T)$ where:
   - Vertices are all parts across all layers: $P = \bigcup_{i \geq 0} P_i$
   - Edges connect parts if vertices between them are adjacent in $G$:
   $$(P, P') \in E_T \iff \exists u \in P, u' \in P': (u, u') \in E(G)$$

### Key Parameters

- **Length of layering tree**: $l(T) = \max_{P \in P} \max_{u,v \in P} d_G(u,v)$ — the maximum diameter among all parts
- **Subtree notation**: $T_k = T[\bigcup_{i < k} P_i]$ — the induced subtree on layers $0$ through $k-1$

## Key Equations

**Partition property:**
$$V(G) = \bigcup_{P \in P} P \quad \text{(disjoint union)}$$

**Layer decomposition:**
$$L_i = \bigcup_{j=1}^{s_i} P_i^j \quad \text{(disjoint)}$$

**Distance within parts:**
For any part $P \in P$ with diameter $\text{diam}(P)$:
$$\text{diam}(P) \leq l(T)$$

**Relationship to treelength:** If $G$ has tree decomposition with treelength $j$, then the layering tree has length $l(T) = O(j)$ [CD00].

## Physical Intuition / Derivation

### Why Layering Trees Matter

Consider navigating a road network from a source city $s$. The BFS layers naturally partition cities by distance from $s$ — cities equidistant from $s$ form a "frontier." However, not all cities at the same distance are connected; they may belong to different connected regions.

The **key insight** is that the layering tree abstracts away vertex-level details and works at the component level:

1. **Layer structure** organizes vertices by distance, like concentric rings around $s$
2. **Connected components** identify which regions are isolated from each other at each distance level
3. **Parts** mark "gateways" — the specific vertices where each region touches a distance layer
4. **The resulting tree** connects parts that share edges in $G$

### Why Is It a Tree?

The connectivity structure must be acyclic because:
- If a cycle existed in $T$, it would imply parts $P_i^j$ (at layer $i$) and $P_k^\ell$ (at layer $k$, $k > i$) both lie in the same connected component and are connected through intermediate parts
- But by construction, vertices can only move forward through layers (increasing distance from $s$) or backward, never creating cycles
- This hierarchical causality (BFS structure) enforces tree topology

## Applications in Engineering

### 1. **Network Routing & Distributed Systems**
- Hierarchical routing algorithms can use the layering tree to reduce routing tables
- Example: In a sensor network, gateways (parts) reduce complex multi-hop topology to tree navigation
- Complexity reduction: instead of $O(|V|)$ state, maintain $O(|P|)$ state

### 2. **VLSI & Circuit Design**
- Partitioning circuits into layers for hierarchical layout
- Computing **treelength** bounds signal propagation delay in gate networks
- Chordal and nearly-chordal graphs (common in IC design) have $l(T) = O(k)$

### 3. **Mesh Decomposition & Geometry**
- In computational geometry, layering trees are related to **merge trees** and **Reeb graphs**
- Applications: topological data analysis, shape segmentation
- Simplification of complex geometric structures

### 4. **Algorithm Design**
- **Centralized algorithms**: BFS structure enables efficient tree-based processing
- **Approximation algorithms**: Layering trees yield $O(1)$ or $O(\log n)$ approximations for graph problems on graphs with bounded treelength
- **Distance computation**: For graphs with small $l(T)$, shortest paths can be computed efficiently using tree structure

### 5. **Dynamic Networks**
- Layering trees naturally update when the source $s$ moves
- Used in dynamic routing for mobile networks and swarms

## Common Mistakes / Pitfalls

### 1. **Confusing Layers with Parts**
- ❌ Mistake: Treating $L_i$ and $P_i$ as the same
- ✓ Correct: $L_i$ is all vertices at distance $i$; parts partition