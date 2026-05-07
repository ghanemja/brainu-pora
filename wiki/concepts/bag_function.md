# Bag Function

## Definition

A **bag function** $B$ is a fundamental component of a **tree decomposition** $(T, B)$ of a graph $G$. 

For a tree decomposition, $B$ is a function that assigns to each node $v$ in the decomposition tree $T$ a subset of vertices $B(v) \subseteq V(G)$, called a **bag**, such that:

1. **Vertex Coverage**: Every vertex of $G$ appears in at least one bag: $V(G) = \bigcup_{v \in V(T)} B(v)$
2. **Edge Coverage**: For every edge $\{u,w\}$ in $G$, there exists at least one bag $B(v)$ containing both $u$ and $w$
3. **Connectivity Property**: For each vertex $u \in V(G)$, the set of tree nodes $\{v \in V(T) : u \in B(v)\}$ induces a connected subtree of $T$

The **size** of a bag function is the maximum cardinality: $\max_{v \in V(T)} |B(v)|$.

The **adhesion** between adjacent tree nodes $v$ and $w$ is the intersection: $|B(v) \cap B(w)|$.

## Key Equations

For a tree decomposition $(T, B)$ and a subset $X \subseteq V(G)$:

$$T_X = \text{Induced subgraph of } T \text{ on nodes } \{v \in V(T) : B(v) \cap X \neq \emptyset\}$$

If $X$ induces a connected subgraph of $G$, then $T_X$ is connected (by the connectivity property).

**Adhesion bound**: For connected subgraphs $X_1, X_2, \ldots, X_k$ of $G$, if their corresponding $T_{X_i}$ subtrees pairwise intersect along a path $P$ in $T$, the adhesion along edges in $P$ must be at least $k-1$.

## Physical Intuition / Derivation

Think of a tree decomposition as a **hierarchical clustering** of graph vertices:

- The tree $T$ represents a recursive decomposition strategy—each node organizes a local region of the graph
- Each bag $B(v)$ contains vertices that must be "remembered" at that decomposition level
- The connectivity property ensures that if a vertex appears in two distant parts of the tree, all intermediate bags must contain it

**Why bags have limited size matters:**
- Small bag size $k$ (captured by treewidth = $k-1$) means the graph has a hierarchical structure that can be exploited algorithmically
- Large adhesions force many vertices to be duplicated across tree nodes, limiting decomposition efficiency

**Derivation context** (from source material): In the given excerpt, a bag function is constructed for a specific graph $G_k$ using a tree $T$ of non-leaf nodes, where each bag contains:
$$B(v) = \{v, s_1, s_2, I(v), I(s_1), I(s_2)\}$$
with $s_1, s_2$ as children of $v$ in the original tree $T_1$, and $I$ denoting some auxiliary vertex set. This construction yields bag size 6 and adhesion size 2.

## Applications in Engineering

### Structural Analysis & Optimization
- **Parameterized algorithms**: Problems intractable on general graphs become solvable in $f(k) \cdot n^{O(1)}$ time on graphs with treewidth $k$ (where bag function bounds the decomposition size)
- **Dynamic programming**: Process graphs recursively by solving subproblems on bags and combining solutions at adhesions

### Network & Circuit Design
- **Planar graph analysis**: Planar graphs have bounded treewidth; bag functions guide efficient layout and routing algorithms
- **VLSI partitioning**: Hierarchical decompositions using bag functions minimize communication between circuit partitions

### Machine Learning & AI
- **Probabilistic graphical models**: Tree decompositions provide exact inference algorithms for Bayesian networks; bags correspond to clique potentials
- **Constraint satisfaction**: Bag functions structure CSP solving by local consistency at each bag and global consistency via adhesions

### Computer Vision & Image Processing
- **Scene decomposition**: Hierarchical scene graphs use bag-like structures to organize spatial relationships

## Common Mistakes / Pitfalls

1. **Confusing bag size with treewidth**: Treewidth = (minimum bag size over all decompositions) − 1. A single bad decomposition with large bags doesn't bound treewidth.

2. **Assuming adhesions are symmetric**: While mathematically $|B(v) \cap B(w)| = |B(w) \cap B(v)|$, directional dependencies in algorithms may treat them asymmetrically—verify both directions when propagating information.

3. **Missing the connectivity requirement**: A function $B$ that covers vertices and edges but violates the connectivity property is **not** a valid bag function. Each vertex's bags must form a connected path in $T$.

4. **Overlooking adhesion bottlenecks**: Small adhesions are algorithmically advantageous (fewer variables to track), but pathological structures can force adhesion size to scale with bag size. The source material shows this constraint prevents certain minors.

5. **Incorrect minor exclusion arguments**: When proving a graph cannot contain a minor via decomposition (as in the source), mistakenly assuming a single bag can intersect all branch sets without checking its size against the number of branch sets—adhesion arguments rigorously exploit size constraints.

## See Also

- [[Tree Decomposition]]
- [[Treewidth]]
- [[Graph Minor]]
- [[Pathwidth]]
- [[Adhesion (Graph Theory)]]

## Sources

- Lecture/paper excerpt on tree decomposition of $G_k$, Items 2–4 (minor exclusion arguments)
- Definition synthesized from standard algorithmic graph theory references on tree decompositions and bag functions