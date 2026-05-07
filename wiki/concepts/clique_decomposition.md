# Clique Decomposition

## Definition

**Clique decomposition** is a graph-theoretic technique for decomposing a graph $G$ into a union of cliques (complete subgraphs). In the context of parameterized algorithms, clique decomposition serves as a structural tool to identify and isolate independent substructures within a graph, enabling efficient enumeration and constraint satisfaction.

More formally: Given a graph $G = (V, E)$, a clique decomposition is a partition (or cover) of edges/vertices into cliques $Q_1, Q_2, \ldots, Q_x$ such that:
$$G[V] \subseteq \bigcup_{i=1}^{x} Q_i$$

In the path-packing context referenced in the source material, clique decomposition is used to:
- **Isolate feasible substructures**: Each clique $Q_i$ corresponds to a set of vertex-disjoint or partially-overlapping subpaths between designated vertices in a matching $M$
- **Enable color-coding**: Assign distinct colors to cliques in a solution, with high probability guaranteeing that each color class corresponds to exactly one clique in an optimal solution
- **Constrain search space**: Reduce the solution space by restricting path construction to unions of maximum-size feasible cliques from each color class

## Key Equations

### Clique Feasibility Constraint
A clique $Q'_i$ of color $i$ is **feasible** with respect to a guessed tuple $\tau$ if it contains all required subpath endpoints and respects adjacency relations:
$$Q'_i \text{ feasible} \iff Q'_i \text{ contains all } P_i \text{ subpaths respecting } T(P_i) \text{ constraints}$$

### Solution Space Reduction
For a YES instance with correct guess $\tau$ and coloring $C_\tau$, an optimal solution exists entirely within:
$$G\left[\bigcup_{i=1}^{x} Q'_i \cup M\right]$$

where $Q'_i$ is the maximum feasible clique of color $i$.

### Enumeration Complexity
The enumeration bounds for clique decomposition-based algorithms:
- Ordered partitions: $O(2^m \cdot m^m)$ where $m = |M|$ (matching size)
- Permutations of subpath endpoints: $O(m! \cdot m)$
- Clique colorings: Each clique subset receives distinct color, enumerated across all partition possibilities

## Physical Intuition / Derivation

### Why Clique Decomposition Matters

**Problem Setup**: Consider a path-packing problem where you must connect specific terminal pairs using length-constrained paths that together form a solution. The challenge is that the graph is large and unstructured—naive algorithms explore exponentially many possibilities.

**Key Insight**: In an optimal solution, the paths decompose into clique-based substructures. A clique $Q_i$ is a "coherent region" of the graph where all subpaths between certain terminal pairs can be routed with full connectivity. By identifying these regions upfront:

1. **Structural Compression**: Instead of reasoning about arbitrary subgraphs, you work with complete subgraphs (cliques) where connectivity is maximal
2. **Color-Coding Probabilistic Guarantee**: Assign random colors to vertices. With high probability, if an optimal solution uses $x$ cliques, the color-coding scheme assigns each clique a unique color. This transforms exponential worst-case search into parameterized search over color classes
3. **Constraint Tightening**: Once you identify that a color-i clique must contain subpaths $P_i$, you can formulate tight Integer Linear Program (ILP) constraints, eliminating infeasible path combinations early

### Derivation Outline

1. **Phase 1 - Structural Enumeration**: Enumerate all possible ordered partitions of terminal pairs into subpaths. This is expensive ($2^m \cdot m^m$) but independent of graph size $n$.

2. **Phase 2 - Clique Coloring**: For each partition, color vertices such that each clique in the optimal solution gets a unique color with probability $\geq 1 - 1/\text{poly}(n)$. This reduces the solution space to examining cliques of a single color.

3. **Phase 3 - ILP Formulation**: Within the union of maximum-size feasible cliques per color, formulate an ILP that enforces:
   - Exact path lengths: $\sum_{e \in \text{path}} 1 = l$
   - Clique capacity: $\sum_{\text{subpaths}} v_{\text{used}} \leq |Q'_i|$

This three-phase approach transforms an NP-hard problem into a parameterized framework with complexity $f(k) \cdot \text{poly}(n)$ where $k$ is the parameter (typically matching size or number of paths).

## Applications in Engineering

### 1. **Network Design & Routing**
- **Optical Networks**: Decompose wavelength-routing graphs into cliques of mutually non-interfering paths; each clique can share a wavelength
- **VLSI Routing**: Identify cliques of nets that can be routed in the same metal layer without crosstalk

### 2. **Supply Chain & Logistics**
- **Vehicle Routing**: Decompose delivery networks into cliques of routes that share distribution hubs; optimize each independently
- **Inventory Networks**: Cliques represent tightly coupled supply nodes; decomposition enables distributed optimization

### 3. **Telecommunications**
- **Call Routing**: Decompose the graph of possible call paths into cliques representing circuit groups with full connectivity
- **5G Network Slicing**: Partition network paths into service cliques (e.g., eMBB, URLLC) for quality-of-service guarantees

### 4. **Computational Biology**
- **Protein Interaction Networks**: Identify cliques as functional modules; decomposition reveals modular structure
- **DNA Sequence Assembly**: Cliques in overlap graphs represent unambiguous sequence segments

### 5. **Parallel & Distributed Systems**
- **Task Scheduling**: Decompose task dependency graphs into cliques of tasks with full synchronization; schedule cliques to minimize idle time
- **Distributed Database