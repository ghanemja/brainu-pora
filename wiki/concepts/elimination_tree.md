# Elimination Tree

## Definition

An **elimination tree** (also called **elimination forest** when considering multiple disconnected components) is a rooted tree or forest constructed from an undirected graph $G = (V, E)$ that encodes a hierarchical decomposition of the graph's structure. Specifically:

- Each node in the tree corresponds to a vertex in $G$
- The tree structure captures ancestor-descendant relationships between vertices
- A key property: **for every edge $\{u,v\} \in E$, one of $u$ or $v$ must be an ancestor of the other in the tree**

The **depth** of an elimination tree is the length of the longest path from any leaf to the root. This depth parameter $\tau$ quantifies the "tree-likeness" of the graph and directly impacts the complexity of algorithms operating on $G$.

**Related concept**: An elimination forest is a generalization where the graph structure induces a forest (multiple trees) rather than a single tree.

---

## Key Equations

For an elimination tree $T$ of depth $\tau$ on a graph $G = (V,E)$ with $n = |V|$ vertices:

$$\text{Depth}(T) = \tau$$

For algorithmic applications (from Theorem 11), runtime complexity bounds are expressed as:

$$\text{Time Complexity} = 4^{\tau} \cdot n^{O(1)}$$

This shows **exponential dependence on tree depth** but only polynomial dependence on vertex count—making elimination trees valuable for parameterized algorithms.

---

## Physical Intuition / Derivation

### Why Elimination Trees Matter

Consider a general graph that is "nearly" a tree. A tree is trivial to process: any algorithm can work top-down or bottom-up efficiently. Real graphs have cycles, but if those cycles are "localized" relative to some tree structure, we can exploit this.

An elimination tree captures exactly this idea: it provides a **hierarchical ordering** of vertices such that the graph's deviation from tree structure (all its edge "violations") is characterized by the depth parameter.

### Construction Intuition

The tree is built so that whenever an edge connects two vertices, one must dominate the other hierarchically. This forces "bad" edges (those creating cycles) to span only certain levels of the tree. Algorithms can then:

1. Process the tree bottom-up, layer by layer
2. At each layer, handle the local structure (which is constrained by the hierarchy)
3. Use dynamic programming or matching techniques to combine solutions from subtrees

### Example: Edge Subdivision (Lemma 10)

The source material shows a practical manipulation: if a graph $G$ is subdivided by introducing a new vertex $p_e$ for each edge $e$, creating $G'$:

- **Original graph $G$**: Has even and odd cycles mixed
- **Subdivided graph $G'$**: All edges have depth $\tau + 1$; every cycle in $G'$ becomes even length

This transformation converts a hard general problem (cycles of any parity) into a bipartite case (all even cycles) while preserving the cycle cover structure and only increasing tree depth by 1.

---

## Applications in Engineering

### 1. **Graph Algorithm Parameterization**
Elimination trees enable **Fixed-Parameter Tractable (FPT)** algorithms for problems that are NP-hard in general:
- **Hamiltonian cycle detection** (parameterized by tree depth $\tau$): solvable in $4^{\tau} n^{O(1)}$ time
- **Partial cycle covers**: counting and verifying edge sets forming cycle covers on specified vertex subsets

### 2. **Sparse Matrix Factorization**
In numerical linear algebra, elimination trees represent the dependency structure during Gaussian elimination:
- The tree encodes which matrix entries must be processed before others
- Enables efficient **symbolic factorization** and **reordering** for sparsity
- Critical in finite element method (FEM) computations

### 3. **Compiler Optimization & Program Analysis**
- Control flow graphs and data dependency graphs are analyzed via elimination orderings
- Tree structures enable efficient liveness analysis and register allocation

### 4. **Circuit Design & Logic Synthesis**
- Netlist representation can be hierarchically decomposed using elimination forests
- Supports efficient circuit partitioning and verification

### 5. **Bioinformatics: Phylogenetic Tree Inference**
- Evolutionary relationships (tree structure) plus additional constraints (cross-edges) model realistic biological systems
- Elimination trees help decompose complex dependency structures in gene regulatory networks

---

## Common Mistakes / Pitfalls

### ❌ **Mistake 1: Confusing Elimination Tree with Spanning Tree**
- **Wrong**: "An elimination tree is just any spanning tree of the graph"
- **Correct**: A spanning tree is a specific *subset* of edges; an elimination tree is a structural ordering imposed on vertices such that edge endpoints maintain ancestor-descendant relationships

### ❌ **Mistake 2: Assuming Unique Elimination Tree**
- **Wrong**: "There is one correct elimination tree for a graph"
- **Correct**: A graph may have *many* valid elimination trees; the goal is often to find one with minimal depth

### ❌ **Mistake 3: Ignoring Depth in Algorithm Analysis**
- **Wrong**: "The tree depth doesn't significantly affect runtime"
- **Correct**: Since complexity is $4^{\tau} n^{O(1)}$, even moderate increases in $\tau$ (e.g., from 10 to 15) multiply runtime by $4^5 \approx 1000\times$

### ❌ **Mistake 4: Misunderstanding the Ancestor-Descendant Constraint**
- **Wrong**: "Edges should only connect parents to direct children"
- **Correct**: Edges can connect *any* ancestor to *any* descendant; they need not be adjacent in the tree

### ❌ **Mistake 5: Overlooking Edge Subdivision Overhead**
- **Wrong**: "Subdividing edges doubles the problem size linearly"
- **Correct**: Subdividing adds $|E|$ new vertices and increases tree depth by at most 1—a mild overhead when depth is the bottleneck parameter

---

## See Also

- [[Parameterized Complexity]] – framework enabling algorithms with single-exponential dependence on parameter (depth here)
- [[Treewidth & Pathwidth]] – related structural