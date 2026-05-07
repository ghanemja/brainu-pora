# bag (tree decomposition)

## Definition

A **bag** in a tree decomposition $(T, \beta)$ of a graph $G$ is a subset of vertices $B_t \subseteq V(G)$ associated with each node $t$ in a tree $T$. The tree decomposition is a pair consisting of:

1. A tree $T$ with nodes (often called "bags" themselves)
2. A labeling function $\beta: V(T) \to 2^{V(G)}$ assigning a subset of graph vertices to each tree node

The bags must satisfy three conditions:
- **Coverage**: Every vertex of $G$ appears in at least one bag
- **Edge property**: For every edge $(u,v) \in E(G)$, there exists at least one bag containing both $u$ and $v$
- **Connectedness**: For each vertex $v \in V(G)$, the set of tree nodes $\{t \in V(T) : v \in \beta(t)\}$ forms a connected subtree of $T$

In the context of the source material, bags are the result of decomposing a planar graph $G$ using a spanning tree $H$. Each bag contains vertices from the original graph, and the adjacency structure of bags in the tree reflects how the original graph's vertex neighborhoods are organized.

## Key Equations

**Tree-width**: The tree-width of a decomposition is:
$$\text{tw}(G, \beta) = \max_{t \in V(T)} |\beta(t)| - 1$$

**Adhesion size** (separator between adjacent bags): For an edge $e = (s,t) \in E(T)$, the adhesion is:
$$\text{ad}_e = |\beta(s) \cap \beta(t)|$$

**Path coverage property**: For a spanning tree $H$ with $L$ terminals, each subpath can be covered by paths from the family:
$$T_i = \bigcup_{j: j \neq i} \overline{p_i q_j}$$
where each $T_i$ forms a tree and the union of all paths remains acyclic.

## Physical Intuition / Derivation

Think of a tree decomposition as a hierarchical clustering of a graph's vertices. Rather than analyzing the entire graph at once, you organize it into overlapping regions (bags) arranged in a tree structure.

**Why bags matter:**
- The overlap between adjacent bags (the adhesion) represents the "interface" between two regions
- The connectedness property ensures that if a vertex appears in multiple bags, those bags form a path through the tree—no disconnected scattered copies
- Many hard computational problems become tractable when restricted to graphs with small tree-width (small bags)

**Construction intuition from source material:**
Starting with a planar graph $G$ and a carefully chosen spanning tree $H$:
1. Identify separators $S$ induced by edges of the tree decomposition
2. Each separator is formed by two upward paths connected via a "closing edge" in $G \setminus H$
3. Vertices inside/outside the separator's planar loop belong to bags on different sides of the corresponding tree edge
4. A pair of vertices is "bad" (problematic) if its connection path crosses a separator—these are classified as either "separated" or "contaminating"

The goal is to choose $H$ such that the fraction of bad pairs is minimized, directly controlling the quality of the decomposition.

## Applications in Engineering

**Algorithm Design:**
- **Dynamic Programming on Trees**: Many NP-hard problems (Steiner tree, vertex cover, independent set) become polynomial-time solvable on graphs with bounded tree-width via DP over the tree decomposition
- Treewidth-based algorithms: complexity is typically $f(\text{tw}) \cdot n^{O(1)}$

**Circuit Design & VLSI:**
- Partitioning circuits hierarchically for placement and routing
- Identifying critical paths and bottleneck connections between circuit regions
- Managing power distribution networks (PDN) through hierarchical decomposition

**Network Analysis:**
- Analyzing communication networks by decomposing into manageable subdomains
- Identifying critical separators for network resilience and redundancy planning

**Compiler Design & Program Analysis:**
- Control flow graph decomposition for program optimization
- Register allocation using graph coloring on tree decompositions

**Finite Element Methods:**
- Mesh decomposition for domain-based solvers
- Identifying interface regions for coupled multiphysics problems

**Graph-Based Optimization:**
- Constraint satisfaction problems with bounded tree-width become tractable
- Integer linear programming with sparse structure exploits tree decomposition

## Common Mistakes / Pitfalls

1. **Confusing bags with cliques**: A bag is NOT a complete subgraph. It's a set of vertices that may have few edges between them. The tree-width bound doesn't require the bag to form a clique in $G$.

2. **Ignoring the connectedness property**: Students often assume bags can be arbitrary overlapping sets. The requirement that vertices form a *connected subtree* of $T$ is essential and non-obvious—it's not automatic from coverage and edge properties.

3. **Overcounting tree-width**: The tree-width is $\max |\beta(t)| - 1$, not $\max |\beta(t)|$. The "-1" adjustment is standard but easy to forget.

4. **Assuming all decompositions are equivalent**: Different tree decompositions of the same graph can have very different tree-widths. The problem of finding a minimum tree-width decomposition is NP-hard.

5. **Misinterpreting adhesion**: The adhesion of an edge is not necessarily small even in "good" decompositions. Separators can have linear size in planar graphs, but this is often unavoidable.

6. **Bad pair classification**: In the source material, assuming a pair is bad w.r.t. a separator $S$ just because it spans $S$ locally—must verify intersection with the planar loop $\xi_S$.

## See Also

- [[tree-width]]
- [[graph separator]]
- [[planar graph decomposition]]
- [[dynamic programming on graphs]]
- [[adhesion (tree decomposition)]]

## Sources

- Lecture/paper excerpt on tree decomposition, separators, and spanning trees for planar graphs (Theorem 3.5 reference, Claims 5.9–5.10)
- Context: