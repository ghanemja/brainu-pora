# graph minor

## Definition

A **graph minor** is a graph obtained from another graph by a sequence of the following operations:

1. **Vertex deletion**: Remove a vertex and all incident edges
2. **Edge deletion**: Remove an edge
3. **Edge contraction**: Remove an edge and merge its two endpoints into a single vertex

Formally, a graph $H$ is a minor of graph $G$ (written $H \preceq G$) if $H$ can be obtained from $G$ through zero or more of these operations.

**Equivalent characterization**: $H$ is a minor of $G$ if there exists a minor model—a function that maps each vertex $v \in V(H)$ to a connected, non-empty subgraph $T_v \subseteq G$ such that:
- The subgraphs $T_v$ are pairwise vertex-disjoint
- For each edge $(u,v) \in E(H)$, there exists at least one edge in $G$ connecting $T_u$ to $T_v$

## Key Equations

**Robertson-Seymour theorem** (structural characterization):
For any infinite sequence of finite graphs, there exist indices $i < j$ such that the $i$-th graph is a minor of the $j$-th graph.

**Tree decomposition bound** (from source context):
If a graph has a tree decomposition with maximum bag size $k$ and maximum adhesion (separator) size $a$, then certain minors are forbidden. Specifically:
- If $K_{n}$ (complete graph on $n$ vertices) is a minor, then some bag must contain at least $n$ vertices
- If $K_{s,t}$ (complete bipartite graph) is a minor, the tree decomposition structure creates path-connectivity constraints

## Physical Intuition / Derivation

Graph minors formalize the notion of "local structural simplification":

**Why contractions matter**: Contracting an edge is like fusing two entities that are strongly coupled. This operation preserves high-level connectivity patterns while reducing complexity. If two components communicate through a single edge, merging them doesn't destroy global reachability properties.

**Why minors are harder to avoid than subgraphs**: Deletion alone (subgraph operation) only removes elements. Contraction allows you to abstract away unnecessary detail—compress short paths into single edges. This makes the minor relation much coarser: many different graphs can have the same minor.

**The tree decomposition perspective** (from source):
- A tree decomposition breaks a graph into overlapping "bags" arranged in a tree structure
- For a graph to contain $K_{3,4}$ as a minor, you need three "left" parts and four "right" parts, all pairwise connected
- Tree structure forces connectivity: if disjoint parts $T_X$ and $T_Y$ must both touch all four right parts, then every path connecting them must contain a bottleneck (adhesion)
- Adhesion size bounds limit how many branch sets can simultaneously "pass through" a region → forbidden minor

**Intuitive example**: A planar graph cannot contain $K_5$ or $K_{3,3}$ as minors (Kuratowski's theorem). You can't compress the non-planar structure no matter how much you delete and contract.

## Applications in Engineering

### 1. **Circuit Design & Netlist Optimization**
- Identify when a circuit netlist contains a forbidden minor (e.g., non-planar substructure)
- Use minor-monotone properties to verify routability without building full layout
- Hierarchical circuit compression uses contraction to abstract subcircuits

### 2. **Network Topology & Routing**
- Determine if a network has certain connectivity bottlenecks (via forbidden minors)
- Grid graph minors characterize planar vs. non-planar routing requirements
- Sparse graph approximations preserve minor relationships

### 3. **VLSI Placement & Floorplanning**
- Tree decomposition width (treewidth) relates to layout area
- Bounded treewidth implies efficient hierarchical decomposition strategies
- Use minor exclusion to reject infeasible placement configurations early

### 4. **Model Checking & Formal Verification**
- Parameterized verification for graphs of bounded treewidth (via minor structural theorems)
- Fixed-parameter tractable (FPT) algorithms for problems on minor-closed graph classes
- Certification of distributed algorithm correctness on network topologies

### 5. **Mesh Generation & Computational Geometry**
- Ensure generated meshes avoid pathological minors (e.g., high-density local structure)
- Use minor-monotonicity to guarantee mesh quality properties transfer across refinement levels

## Common Mistakes / Pitfalls

### 1. **Confusing minors with subgraphs**
**Error**: Thinking that if $H$ is not a subgraph of $G$, then $H$ is not a minor.
**Reality**: Contraction is powerful. $K_5$ is a minor of any complete graph $K_n$ for $n \geq 5$, but may not appear as a subgraph.

### 2. **Assuming minor order is total**
**Error**: Expecting that for any two graphs, one must be a minor of the other.
**Reality**: The minor relation is a partial order. Incomparable graphs exist (e.g., cycle $C_4$ and star $K_{1,4}$).

### 3. **Ignoring connectivity requirements**
**Error**: Thinking you can arbitrarily partition $G$ to create a minor model.
**Reality**: Each part $T_v$ in the minor model **must induce a connected subgraph**. Disconnected branch sets don't count.

### 4. **Misapplying tree decomposition bounds**
**Error**: Assuming that finding a tree decomposition with small bags guarantees absence of certain minors.
**Reality**: Bag size provides necessary but not sufficient conditions. You need to verify the adhesion (separator) sizes along paths, as shown in the source.

### 5. **Forgetting monotonicity**
**Error**: Modifying a minor-free graph by edge deletion and expecting it might gain the forbidden minor.
**Reality**: The minor relation is monotone: $H \preceq G$ and $G' \subseteq G$ implies $H \preceq G'$ only via deletion. Contractions preserve minors downward.

## See Also

- [[tree