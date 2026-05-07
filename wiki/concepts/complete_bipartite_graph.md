# complete bipartite graph

## Definition

A **complete bipartite graph**, denoted $K_{s,t}$, is a bipartite graph whose vertex set can be partitioned into two disjoint sets $A$ and $B$ with $|A| = s$ and $|B| = t$, such that every vertex in $A$ is adjacent to every vertex in $B$, and there are no edges within $A$ or within $B$.

Formally: $K_{s,t} = (A \cup B, E)$ where $E = \{(u,v) : u \in A, v \in B\}$, so $|E| = s \cdot t$.

A graph is said to be **$K_{s,t}$-free** if it does not contain $K_{s,t}$ as a subgraph.

## Key Equations

The number of edges in $K_{s,t}$:
$$|E(K_{s,t})| = s \cdot t$$

The degree of each vertex in $A$ (in $K_{s,t}$):
$$\deg_A(v) = t \quad \forall v \in A$$

The degree of each vertex in $B$:
$$\deg_B(v) = s \quad \forall v \in B$$

For a $K_{s,t}$-free graph $G$ with $n$ vertices and maximum degree $\Delta$, a fundamental consequence of the Kővári–Sós–Turán theorem bounds the number of edges:
$$|E(G)| \leq \frac{1}{2}(s-1)^{1/t} n^{2-1/t} + \frac{t-1}{2}n$$

When $s = t$ (the symmetric case), this simplifies for $K_{t,t}$-free graphs.

## Physical Intuition / Derivation

### Why Complete Bipartite Graphs Matter

Complete bipartite graphs are **extremal structures** in graph theory—they represent the "densest possible" bipartite subgraphs without being fully bipartite themselves. They serve as forbidden minors/subgraphs because:

1. **Structural Characterization**: Many natural graph classes can be defined by forbidding $K_{s,t}$:
   - Planar graphs are $K_{3,3}$-free (Kuratowski's theorem)
   - Graphs of bounded degeneracy are $K_{t,t}$-free for $t = \Delta + 1$
   - Nowhere dense graphs exclude $K_{t,t}$ for appropriate $t$

2. **Algorithmic Significance**: Excluding $K_{t,t}$ provides **structural sparsity** that enables efficient algorithms:
   - The absence of large complete bipartite subgraphs limits local density
   - This sparsity can be exploited for FPT (fixed-parameter tractable) algorithms
   - Problems intractable on general graphs become tractable on $K_{t,t}$-free graphs

### Intuitive Picture

Imagine a bipartite matching scenario: $K_{s,t}$ is like having $s$ "suppliers" on one side and $t$ "consumers" on the other, where every supplier can serve every consumer. This complete connectivity makes it a "densest" bipartite structure. Problems that become hard when such complete connections exist become easier when they're forbidden.

## Applications in Engineering

### 1. Circuit Design & VLSI
- **Two-layer routing problems**: $K_{s,t}$-free constraints model congestion avoidance in networks where certain resource connections must be avoided
- **Cross-layer interference analysis**: Forbidding $K_{3,3}$ ensures planarity in 2D layout problems

### 2. Computational Complexity for Practical Problems
- **Matrix completion (d-EDMC)**: The source material uses $K_{t,t}$-freeness in the complement graph to model partial matrix structure. Excluding $K_{t,t}$ transforms intractable completion problems into FPT algorithms
- **Treewidth approximation**: $K_{t,t}$-free graphs have bounded treewidth, enabling dynamic programming on tree decompositions

### 3. Network Design
- **Communication networks**: Avoiding $K_{s,t}$ subgraphs ensures network sparsity, reducing bottlenecks
- **Bipartite matching in resource allocation**: Understanding which $K_{s,t}$ structures can be avoided helps design stable matching algorithms

### 4. Machine Learning & Sparse Recovery
- **Graph-based learning**: $K_{t,t}$-free assumptions encode sparsity priors on data dependencies
- **Kernel design**: Bipartite graphs with forbidden structures model interactions between features and samples

## Common Mistakes / Pitfalls

1. **Confusing $K_{s,t}$ with $K_n$**: $K_{s,t}$ is bipartite (can be 2-colored); $K_n$ is only bipartite when $n \leq 2$. Do not treat them as equivalent dense graphs.

2. **Assuming $K_{t,t}$-freeness implies sparsity everywhere**: $K_{t,t}$-freeness bounds the size of bipartite cliques but does not preclude dense cliques within single partitions. A $K_{t,t}$-free graph can still contain $K_{t}$ (complete graph on $t$ vertices).

3. **Forgetting the asymmetry of $K_{s,t}$ vs. $K_{t,s}$**: When $s \neq t$, these are distinct (though isomorphic). The parameter choice matters for algorithmic bounds.

4. **Misapplying Kővári–Sós–Turán bounds**: The theorem applies to graphs that do *not* contain $K_{s,t}$. Existence of the subgraph invalidates the bound.

5. **Confusing forbidden subgraph with forbidden minor**: $K_{3,3}$-freeness (subgraph) is stronger than $K_{3,3}$-minor-free. The source material deals with subgraph freeness.

## See Also

- [[bipartite graph]] — foundational structure
- [[graph minor]] — forbidden minors as structural constraints
- [[pla