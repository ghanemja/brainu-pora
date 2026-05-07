# tree decomposition

## Definition

A **tree decomposition** of a graph $G = (V, E)$ is a pair $(T, \beta)$ where:

- $T = (V(T), E(T))$ is a tree (the decomposition tree or "meta-tree")
- $\beta : V(T) \to 2^V$ maps each node (called a **bag**) to a subset of vertices in $G$

satisfying three properties:

1. **Vertex coverage**: Every vertex of $G$ appears in at least one bag: $\bigcup_{b \in V(T)} \beta(b) = V$

2. **Edge coverage**: For every edge $(u,v) \in E$, there exists a bag $b$ such that both $u, v \in \beta(b)$

3. **Connectedness (running intersection property)**: For any vertex $v \in V$, the set of bags containing $v$ forms a connected subtree of $T$

The **width** of a tree decomposition is $\max_{b \in V(T)} |\beta(b)| - 1$ (the maximum bag size minus one). The **treewidth** $\text{tw}(G)$ of a graph is the minimum width over all possible tree decompositions.

## Key Equations

For a graph $G$ with a tree decomposition $(T, \beta)$ and weight function $\chi : V(G) \to \{0,1\}$:

**Lemma 3.6 (Balanced Separation):** If $T$ has maximum degree 3 and $W = \chi(V(G))$, then either:

$$\exists b \in V(T) : \chi(\beta(b)) \geq \frac{W}{4k}$$

or there exists a set $F \subseteq E(T)$ with $|F| = k$ edges such that every connected component $C$ of $T - F$ satisfies:

$$\chi\left(\bigcup_{b \in V(C)} \beta(b)\right) \geq \frac{W}{4k}$$

This provides a **balanced recursive decomposition**: any tree decomposition can be recursively partitioned into $k$ regions where each region contains a non-trivial fraction of the original weight.

## Physical Intuition / Derivation

Tree decomposition can be understood as a hierarchical clustering of a graph's vertices:

**Motivation from planar graphs:** Planar graphs often exhibit local structure—they can be understood through a "zoom-out" process where we group nearby vertices together, and the hierarchical relationships between these groups form a tree.

**The running intersection property** ensures that if a vertex $v$ appears in bags $b_1$ and $b_2$, it must appear in all bags on the unique path between them in $T$. This prevents pathological "wraparounds" and maintains geometric coherence.

**Width as a complexity measure:** The treewidth captures how "tree-like" a graph is:
- Trees have treewidth 1 (each vertex in its own bag, plus incident edges)
- Planar graphs have treewidth $O(\sqrt{n})$ (by planar separator theorems)
- Complete graphs have treewidth $n-1$ (must put all vertices in one bag)

**Balanced decomposition (Lemma 3.6)** works by greedily finding edges in $T$ that separate the graph into roughly equal-weight parts. The algorithm exploits the degree-3 constraint: at degree-2 nodes, you have at most two choices for continuing; at degree-3 nodes, the pigeonhole principle guarantees one branch has substantial weight.

## Applications in Engineering

### 1. **Algorithm Design (Parameterized Complexity)**
Tree decompositions enable dynamic programming on bounded-treewidth graphs. For many NP-hard problems (vertex coloring, maximum independent set, Steiner tree), algorithms running in $2^{O(\text{tw})} \cdot \text{poly}(n)$ time are possible via tree DP. This is crucial for handling sparse, nearly-planar graphs in network design.

### 2. **Planar Graph Processing**
Planar graphs appear in VLSI layout, geographic routing, and road networks. Lemma 3.6 provides a divide-and-conquer framework: by removing $k$ edges from the tree decomposition, you partition a planar graph into $k$ regions with balanced load. This supports:
- **Distributed algorithms**: partition a geographical network across $k$ processors
- **Load balancing**: ensure no single region is overloaded

### 3. **Graph Neural Networks & Machine Learning**
Tree decompositions structure the message-passing graph in graph neural networks. Networks trained on low-treewidth subgraphs can be evaluated more efficiently, and the hierarchical decomposition provides interpretable intermediate representations.

### 4. **Computational Biology**
In phylogenetic tree inference and protein interaction networks, tree decompositions reveal modular structure. Modules (bags) represent functional clusters; tree edges represent cross-module dependencies.

### 5. **SAT Solving & Constraint Satisfaction**
Modern SAT solvers use tree decompositions implicitly via "clause-group resolution." The treewidth bounds the size of intermediate formulas in resolution-based proofs.

## Common Mistakes / Pitfalls

1. **Confusing treewidth with tree size:** A graph's treewidth is a structural property independent of the size of the decomposition tree $T$. You can have $|V(T)| \gg |V(G)|$ (there are canonical representations, but they're not unique).

2. **Assuming uniqueness:** Tree decompositions are not unique. Many different $(T, \beta)$ pairs can have the same width. The minimum width (treewidth) is unique, but algorithms may produce different decompositions of the same optimal width.

3. **Forgetting the running intersection property:** This is the key constraint. You cannot simply partition vertices arbitrarily into bags. The *connectivity* of bags containing each vertex is essential and easy to violate when constructing decompositions manually.

4. **Misinterpreting Lemma 3.6's degree-3 assumption:** The lemma requires $T$ to have maximum degree ≤ 3. Not all tree decompositions satisfy this; you may need to apply a normalization step first (binary tree decompositions always exist