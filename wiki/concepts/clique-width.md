# clique-width

## Definition

**Clique-width** is a graph invariant that measures the structural complexity of a graph by quantifying how it can be recursively decomposed using four operations on labeled vertices. Formally, the clique-width of a graph $G$, denoted $\text{cw}(G)$, is the minimum number of labels needed to construct $G$ using the following operations:

1. **Create** a single vertex with a given label
2. **Disjoint union** of two labeled graphs
3. **Relabel** all vertices with label $i$ to label $j$
4. **Join** all vertices labeled $i$ to all vertices labeled $j$ (for $i \neq j$)

A graph has clique-width $k$ if it can be constructed using at most $k$ distinct labels through these operations.

### Formal Characterization

The clique-width can equivalently be defined via **clique-width expressions** (or $k$-expressions): a tree structure where:
- Leaves correspond to single vertices
- Internal nodes represent the four operations above
- The width is the maximum number of distinct labels appearing on any path from root to leaf

## Key Equations

**Relationship to treewidth:**
$$\text{tw}(G) \leq \text{cw}(G) - 1$$

where $\text{tw}(G)$ denotes the treewidth of $G$. However, this inequality can be arbitrarily loose.

**Bounds for specific graph classes:**
- Complete graphs: $\text{cw}(K_n) = 2$ (for $n \geq 2$)
- Trees: $\text{cw}(T) \leq 3$
- Cographs (complement-reducible graphs): $\text{cw}(G) \leq 2$
- Bipartite permutation graphs: $\text{cw}(G) \leq 3$

**NP-hardness characterization:** For any fixed $k$, determining if $\text{cw}(G) \leq k$ is NP-complete, even for severely restricted graph classes.

## Physical Intuition / Derivation

### Why Clique-Width Matters

Clique-width captures a notion of **modular decomposition** and **recursive structure** that differs fundamentally from treewidth:

- **Treewidth** measures how tree-like a graph is (good for path-like decompositions)
- **Clique-width** measures how a graph can be built incrementally from small labeled components via joins

### Intuitive Construction

Imagine building a graph step-by-step:
1. Start with isolated vertices, each labeled with colors from a palette of $k$ labels
2. Merge groups: you can combine separate components or relabel vertices
3. Add edges: connect all vertices of one color to all vertices of another color

The key insight: **small label sets force structure**. A graph with clique-width 2 can only be built with 2 labels—meaning its structure is highly constrained and often admits efficient algorithms.

### Why Not Just Use Treewidth?

Many important graph classes (e.g., cliques, dense graphs) have large treewidth but small clique-width. Conversely, some sparse structures (e.g., random graphs) have moderate clique-width but large treewidth. This makes clique-width a complementary complexity measure.

## Applications in Engineering

### 1. **Graph Coloring Problems**
From the source material (Jaffke et al., 2024), parameterization by clique-width has been applied to **$b$-coloring**: finding proper colorings where each color class contains a vertex adjacent to all other colors. Fixed-parameter tractable (FPT) algorithms exist when parameterized by clique-width, enabling efficient solutions for structured graphs.

### 2. **VLSI Design & Circuit Optimization**
Clique-width bounds appear in:
- Register allocation in compilers
- Module placement and routing (structured designs have bounded clique-width)
- Symmetry detection in circuit netlists

### 3. **Database Query Optimization**
Query graphs in relational databases often have bounded clique-width. Algorithms exploiting this structure enable polynomial-time evaluation of otherwise hard queries.

### 4. **Constraint Satisfaction & SAT Solving**
Variable interaction graphs in CSP instances often have bounded clique-width. This structure is exploited in:
- Structural decomposition methods
- Hybrid algorithms combining SAT and structural reasoning

### 5. **Algorithmic Meta-Theorems**
The **Courcelle theorem** and its generalizations guarantee that problems expressible in **Monadic Second-Order Logic (MSO)** can be solved in FPT time on graphs of bounded clique-width. This covers:
- Independent set / vertex cover
- Hamiltonian path detection
- Subgraph isomorphism (for fixed patterns)

## Common Mistakes / Pitfalls

### 1. **Confusing Clique-Width with Treewidth**
- **Mistake:** Assuming a small treewidth implies small clique-width
- **Reality:** The reverse inequality ($\text{cw}(G) \leq 2^{\text{tw}(G)+1}$) shows clique-width can be exponentially larger
- **Example:** A clique $K_n$ has $\text{cw}(K_n) = 2$ but $\text{tw}(K_n) = n-1$

### 2. **Underestimating NP-Hardness**
- **Mistake:** Assuming clique-width can be approximated efficiently
- **Reality:** Computing clique-width is NP-hard; no constant-factor approximation exists (under standard assumptions)
- **Mitigation:** Use heuristics or restrict to graph classes where efficient computation is known (cographs, permutation graphs, etc.)

### 3. **Misapplying FPT Results**
- **Mistake:** Thinking an FPT algorithm for bounded clique-width is "practical" for clique-width $> 5$
- **Reality:** The exponential dependence on clique-width can be prohibitive; algorithms often have form $O(f(k) \cdot n^c)$ where $f(k)$ grows very fast
- **Example:** From source