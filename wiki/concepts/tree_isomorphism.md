# Tree Isomorphism

## Definition

**Tree isomorphism** is the problem of determining whether two trees are **structurally identical**—that is, whether there exists a bijective mapping between their vertices that preserves the edge relationships. More formally:

Two rooted trees $T$ and $T'$ are **isomorphic** if there exists a bijection $\phi: V(T) \to V(T')$ such that:
- $\phi$ maps the root of $T$ to the root of $T'$
- For all vertices $u, v \in V(T)$: $(u, v) \in E(T) \iff (\phi(u), \phi(v)) \in E(T')$

In the context of **graph pattern matching** (as in the source material), tree isomorphism checking is used to:
1. **Identify matching subtree structures** across different rooted spanning trees within a graph
2. **Enumerate and count** all occurrences of a specific tree pattern $T$ within a larger graph $G$, parameterized by root vertex and color assignment
3. **Sample uniformly** from the distribution of matching tree patterns using dynamic programming

The key insight is that tree isomorphism is **computationally tractable** in polynomial time (unlike general graph isomorphism), making it suitable for algorithmic applications in pattern detection.

---

## Key Equations

### Tree Decomposition and Recursive Counting

The fundamental recursive formula for counting colored tree patterns is:

$$C(T, S, v) = \frac{1}{d} \sum_{\substack{S_1, S_2 \subset S \\ S_1 \cap S_2 = \emptyset}} C(T_1, S_1, v) \sum_{u \sim v} C(T_2, S_2, u)$$

**where:**
- $C(T, S, v)$ = count of $h$-treelets (rooted subgraphs with $h = |S|$ colored vertices) isomorphic to tree $T$, rooted at vertex $v$, with color set $S$
- $T_1, T_2$ = subtrees obtained by splitting $T$ at its root, with $T_1$ retaining the root and $T_2$ rooted at a child
- $S = S_1 \cup S_2$ = partition of color labels across the two subtrees
- $d$ = normalization factor depending only on the tree structure $T$
- $u \sim v$ = $u$ is a neighbor (adjacent vertex) of $v$ in graph $G$

### Time Complexity

**Build-up phase:** $2^{O(k)} \cdot O(\|G\|)$  
**Sampling phase (per sample):** $2^{O(k)} \cdot O(\log n)$

The exponential dependence on $k$ (tree size) is unavoidable but acceptable for small patterns; the dependence on graph size scales linearly or logarithmically.

---

## Physical Intuition / Derivation

### Why Tree Isomorphism Matters

Trees have a unique property: they contain **exactly one simple path** between any two vertices. This constraint makes isomorphism checking tractable:

1. **No cycles** → no ambiguity in structural mapping; a tree's connectivity is entirely determined by its adjacency relationships
2. **Unique rooted forms** → trees become *ordered* structures that can be processed bottom-up recursively

### The Recursive Decomposition Strategy

The recursive formula works by:

1. **Choosing a root** for tree $T$ and virtually "cutting" it into two subtrees $T_1$ and $T_2$
2. **Distributing colors** ($S_1, S_2$) to vertices in each subtree—colors represent a labeling (e.g., different chemical elements in a molecule)
3. **Counting independently** how many ways $T_1$ can appear rooted at $v$ and how many ways $T_2$ can appear rooted at neighbors $u$ of $v$
4. **Multiplying counts** across all compatible partitions

This is **dynamic programming over tree structure**: subproblems are tree isomorphisms for smaller subtrees, memoized via the $C$ table.

### Why Normalization Factor $d$ is Needed

If a tree has **automorphisms** (self-symmetries), the same tree instance might be counted multiple times under different vertex mappings. The factor $d$ corrects for overcounting due to the tree's symmetry group.

---

## Applications in Engineering

### 1. **Bioinformatics & Molecular Structure Matching**
- **Subgraph/subtree matching** in protein interaction networks to identify functional motifs
- **Chemical compound libraries**: find all occurrences of a molecular scaffolds (represented as trees) within large compound databases
- **Phylogenetic analysis**: identify isomorphic evolutionary subtrees across multiple species trees

### 2. **Network Analysis**
- **Motif detection** in social networks, citation networks, and communication graphs
- **Anomaly detection**: find recurring structural patterns that may indicate coordinated activity or attacks
- **Sampling representative subgraphs**: uniformly sample small connected regions to estimate global network properties without exhaustive enumeration

### 3. **Compiler Design & Program Analysis**
- **Abstract syntax tree (AST) matching**: identify code patterns, refactoring opportunities, or potential bugs by matching rooted tree structures in program syntax
- **Pattern-based optimization**: recognize isomorphic subtrees in intermediate representations to apply algebraic simplifications

### 4. **Database Query Processing**
- **Tree-structured data retrieval** (XML, hierarchical JSON) requires efficient matching of query trees against data trees
- **Index structures** leverage tree isomorphism for pruning search spaces

### 5. **Machine Learning on Graphs**
- **Graph neural networks** rely on understanding subgraph isomorphism for **receptive field design** and **motif-based feature extraction**
- **Graphlet kernels** count matching small tree patterns to create vector representations of graphs for classification tasks

---

## Common Mistakes / Pitfalls

### 1. **Confusing Rooted vs. Unrooted Trees**
**Mistake**: Assuming tree isomorphism is independent of root choice.  
**Reality**: Rooted tree isomorphism is **stricter** than unrooted isomorphism. The formula $C(T, S