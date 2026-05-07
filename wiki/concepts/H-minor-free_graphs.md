# H-minor-free graphs

## Definition

An **H-minor-free graph** is a graph $G$ that does not contain $H$ as a minor. Formally, $H$ is a minor of $G$ if $H$ can be obtained from a subgraph of $G$ by contracting edges.

**Equivalently:** A graph $G$ is $H$-minor-free if there is no way to:
1. Select a subgraph of $G$
2. Contract zero or more edges in that subgraph
3. Obtain a graph isomorphic to $H$

**Bounded minor class:** A class $\mathcal{G}$ is $H$-minor-free if every graph in $\mathcal{G}$ is $H$-minor-free for some fixed graph $H$.

### Examples
- **Planar graphs** are $K_5$-minor-free and $K_{3,3}$-minor-free (by Kuratowski's theorem)
- **Outerplanar graphs** are $K_4$-minor-free
- **Graphs of bounded treewidth $t$** are $K_{t+2}$-minor-free

---

## Key Equations

### Treewidth and Minors (Robertson-Seymour)

For a graph $G$ that is $H$-minor-free with $|V(H)| = h$:

$$\text{treewidth}(G) \leq f(h)$$

where $f(h)$ is a function depending only on $h$.

### Neighborhood Growth

If $Z \subseteq V(G)$ with $|Z| = k$ and the graph is $H$-minor-free, the $d$-neighborhood $N_G^d[Z]$ may contain up to $O(n)$ vertices (worst case), but admits structured decompositions when $H$ is sparse.

For **apex-minor-free** graphs (subset of $H$-minor-free): if $Z$ is a solution set intersecting each tree decomposition bag in $\tilde{O}(\sqrt{k})$ vertices, algorithms can run in time:

$$2^{\tilde{O}(\sqrt{k})} \cdot n^{O(1)}$$

---

## Physical Intuition / Derivation

### Why H-minor-free matters

**Structural constraint via minors:** The minor relation is a partial order on graphs. If $G$ is $H$-minor-free, then $G$ avoids a specific "obstruction" that would force it to have certain structural properties (high treewidth, dense subgraphs, etc.).

**Graph classes form a hierarchy:**
```
All graphs
    ↑
K₆-minor-free (extremely broad)
    ↑
K₃,ₕ-minor-free (more restrictive)
    ↑
K₅-minor-free (planar graphs)
    ↑
K₄-minor-free (outerplanar)
    ↑
Bounded treewidth
```

### Limits of the framework

The source material reveals a critical limitation: **H-minor-free graphs are too broad for some algorithmic results.**

**Counterexample from source:** Consider:
- $G_0$ = planar graph with arbitrarily large treewidth
- $G$ = $G_0$ plus a universal vertex $z$ connected to all vertices in $G_0$

Then:
- $G$ is $K_6$-minor-free
- But $G$ has arbitrarily large treewidth (cannot be bounded polynomially)
- The $1$-hop neighborhood of $\{z\}$ is the entire graph

**Lesson:** Fixing $H$ alone doesn't guarantee controlled treewidth. For algorithmic guarantees, we need stronger restrictions like **apex-minor-free** or **$K_{3,h}$-minor-free** graphs.

---

## Applications in Engineering

### 1. VLSI Routing & Graph Layout
In circuit design, if the constraint graph is minor-restricted, routing problems admit better approximation algorithms. Planar routing problems (a special case of $K_5$-minor-free) have well-studied solutions.

### 2. Network Design
Sparse minor-free classes (like $K_{3,h}$-minor-free) model communication networks with bounded expansion properties. Algorithms for facility location and network optimization run in subexponential time on these restricted classes.

### 3. Algorithm Design for Hard Problems
**Subgraph isomorphism** (finding a pattern $P$ in a host graph $G$):
- For $G$ apex-minor-free, solvable in time $2^{\tilde{O}(\sqrt{|V(P)|})} |V(G)|^{O(1)}$
- General $H$-minor-free: problem remains NP-hard even for $k=1$ (source notes finding degree-constrained neighborhoods in $K_6$-minor-free graphs is as hard as 3-coloring planar graphs)

### 4. Distributed Computing
Minor-free graph classes with bounded expansion enable local algorithms—problems solvable in $O(\log n)$ communication rounds on graphs with forbidden minors.

---

## Common Mistakes / Pitfalls

### Mistake 1: Assuming H-minor-free ⟹ bounded treewidth
**Wrong:** "If $G$ is $K_6$-minor-free, then $G$ has polynomial treewidth in some parameter."

**Correct:** $K_6$-minor-free is too broad. You need stronger restrictions (e.g., apex-minor-free, $K_{3,h}$-minor-free, or explicit treewidth bounds).

### Mistake 2: Confusing minor-free with subgraph-free
**Wrong:** "$K_6$-minor-free" = "no $K_6$ subgraph"

**Correct:** Minor-free allows contraction; $K_6$-minor-free graphs can contain $K_6$ subgraphs if vertices can be merged into it.

### Mistake 3: Not recognizing the hierarchy
**Wrong:** Treating all $H$-minor-free classes as equally tractable.

**Correct:** Sparsity of $H$ (e.g., $K_{