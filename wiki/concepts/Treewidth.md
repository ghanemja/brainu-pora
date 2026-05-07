# Treewidth

## Definition

**Treewidth** is a graph parameter that measures how "tree-like" a graph is. Formally, the treewidth of a graph $G$, denoted $\text{tw}(G)$, is the smallest width achievable by any tree decomposition of $G$.

A **tree decomposition** of a graph $G = (V, E)$ is a pair $(T, \{X_t\}_{t \in V(T)})$ where:
- $T$ is a rooted tree
- Each node $t \in T$ has an associated **bag** $X_t \subseteq V(G)$
- The following properties hold:
  1. **Covering**: Every vertex and edge of $G$ appears in at least one bag
  2. **Running Intersection Property**: For each vertex $v \in V(G)$, the set of nodes $\{t \in V(T) : v \in X_t\}$ forms a connected subtree of $T$
  3. **Vertex-edge covering**: For every edge $uv \in E$, there exists a bag containing both $u$ and $v$

The **width** of a tree decomposition is $\max_{t \in V(T)} |X_t| - 1$.

A **nice tree decomposition** is a normalized tree decomposition where $T$ has a special structure enabling efficient dynamic programming. In addition to the above properties, a nice tree decomposition is rooted with specific node types:

- **Introduce vertex node**: one child $t'$, with $X_t = X_{t'} \cup \{v\}$ for some $v \notin X_{t'}$
- **Forget node**: one child $t'$, with $X_t = X_{t'} \setminus \{v\}$ for some $v \notin X_t$
- **Introduce edge node**: one child $t'$, with $X_t = X_{t'}$ and edge $uv$ introduced (where $u, v \in X_t$)
- **Join node**: two children $t_1, t_2$, with $X_t = X_{t_1} = X_{t_2}$
- **Root and leaves**: satisfy $X_r = X_l = \emptyset$

## Key Equations

$$\text{tw}(G) = \min \{ \text{width}(T, X) : (T, X) \text{ is a tree decomposition of } G \}$$

For a tree decomposition $(T, X)$:
$$\text{width}(T, X) = \max_{t \in V(T)} |X_t| - 1$$

**Key structural property**: For a node $t$ in a tree decomposition, the bag $X_t$ acts as a **separator** between the subgraph $G_t$ (induced by vertices in bags of the subtree rooted at $t$) and the rest of $G$. Any path leaving $G_t$ must pass through $X_t$.

## Physical Intuition / Derivation

### Why Tree Decomposition Matters

Imagine trying to decompose a complex network (road network, electrical grid, communication network) into simpler pieces. A tree decomposition recursively breaks the graph into overlapping subgraphs organized in a tree structure. The "width" measures the minimal overlap size needed—small overlaps mean the graph is closer to a tree.

**Key insight**: Trees have treewidth 1 (a single bag per vertex). Dense graphs like cliques of size $k$ have treewidth $k-1$ (need all vertices in one bag). Sparse graphs typically have low treewidth.

### The Connectivity Principle

The running intersection property is crucial: if a vertex $v$ appears in bags $X_t$ and $X_s$, then it must appear in all bags on the path between $t$ and $s$ in $T$. This ensures that local information about $v$ is contiguous, enabling correct dynamic programming.

### Why Nice Tree Decompositions?

Nice tree decompositions enforce a strict structure with limited node types. This structure makes dynamic programming systematically simpler: 
- **Introduce** nodes let you add vertices incrementally
- **Forget** nodes let you eliminate vertices no longer needed
- **Join** nodes combine independent subproblems
- The four operations cover all necessary structural transformations

Any tree decomposition can be converted to a nice tree decomposition with at most linear increase in the number of nodes (polynomial-time transformation).

## Applications in Engineering

### 1. **Network Design and Analysis**
- Computing optimal placement of sensors/routers in networks with bounded treewidth
- Evaluating robustness via minimum vertex separators (separator has size $\leq \text{tw}(G) + 1$)
- Finding minimum feedback vertex sets in sparse networks

### 2. **VLSI and Chip Design**
- Routing and placement problems in circuit layouts often have low treewidth structure
- Treewidth bounds enable efficient solutions to problems otherwise NP-hard
- Layer assignment in hierarchical designs

### 3. **Constraint Satisfaction and SAT Solving**
- Variable elimination order optimization (related to tree decomposition)
- Bounded treewidth CNF formulas admit polynomial-time satisfiability checking
- Clause learning and propagation in SAT solvers benefit from decomposition structure

### 4. **Path Finding and Distance Preservation**
- Computing distance-preserving subgraphs: shortcuts in low-treewidth graphs can be efficiently found
- Shortest path problems on graphs of bounded treewidth via dynamic programming on decompositions
- Route planning in transportation networks with hierarchical structure

### 5. **Control Systems and Graph-Based Models**
- State-space representation of distributed systems with low coupling (low treewidth)
- Decentralized control synthesis: decompose into weakly-coupled subsystems
- Model reduction for systems with block-sparse interaction patterns

### 6. **Bioinformatics**
- Phylogenetic tree analysis (trees naturally have treewidth 1)
- RNA secondary structure prediction (outerplanar subgraphs have treewidth 3)
- Protein interaction networks with hierarchical organization

## Common Mistakes / Pitfalls

### 1. **Confusing Treewidth with Tree Structure**
A graph has treewidth 1 if and only if it