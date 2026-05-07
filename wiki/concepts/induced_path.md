# induced path

## Definition

An **induced path** in a graph $G = (V, E)$ is a sequence of vertices $P = (v_1, v_2, \ldots, v_k)$ such that:

1. Consecutive vertices are connected: $(v_i, v_{i+1}) \in E$ for all $i \in \{1, \ldots, k-1\}$
2. **No non-consecutive vertices are connected**: For any $i, j$ with $|i - j| \geq 2$, we have $(v_i, v_j) \notin E$

In other words, an induced path is a path where the induced subgraph on its vertex set contains *only* the edges along the path itself—no "shortcuts" or chord edges are allowed.

**Contrast with ordinary paths:** A regular path allows arbitrary edges between non-consecutive vertices. An induced path forbids them entirely.

## Key Equations

### Maximum Weight Induced Path Problem

Given vertex weights $w_v$ and edge weights $w_{uv}$, find an induced path $P^*$ maximizing:

$$w(P) = \sum_{v \in P} w_v + \sum_{(u,v) \in E(P)} w_{uv}$$

subject to the constraint that no edges exist between non-consecutive vertices in $P$.

### Column Generation Pricing Subproblem

In the co-3-plex polytope formulation, the pricing subproblem seeks a maximum induced path with composite weights:

$$w(P) = \sum_{v \in P} \left(w_v - \mu_v\right) + \sum_{(u,v) \in E(P)} \sum_{\substack{K \in \mathcal{K}(G) \\ \{u,v\} \subseteq K}} \lambda_K$$

where:
- $w_v$ are vertex weights
- $\mu_v$ are dual values from vertex degree constraints
- $\lambda_K$ are dual values from clique constraints
- $\mathcal{K}(G)$ is the set of all maximal cliques

## Physical Intuition / Derivation

### Why Induced Paths Matter

Induced paths are *structurally rigid* constraints. When you forbid chords, you force a linear topology with no shortcuts. This makes them useful for:

1. **Hardness characterization**: The exponential number of induced paths (compared to polynomial triangles) is precisely what makes the general co-3-plex problem hard to solve via standard linear programming relaxations.

2. **Graph recognition**: Induced paths are fundamental to characterizing graph classes:
   - Chordal graphs have no induced cycles of length ≥ 4
   - $t$-chordal graphs bound induced path structures
   - Path length and forbidden induced subgraphs define graph families

3. **Algorithmic leverage**: On *chordal graphs*, despite exponentially many induced paths, the **maximum weight induced path problem is solvable in polynomial time**. This is because the path-finding algorithm can exploit the chordal structure (every cycle has a chord) to prune the search space efficiently.

### Why Exponential Count?

Consider a simple path graph $P_n$ with $n$ vertices arranged linearly. Any contiguous subsequence forms an induced path. There are $\binom{n}{2}$ such subsequences, which is polynomial for this special case. However, in general graphs, induced paths can weave through the vertex set in combinatorially many ways without creating chords—leading to exponential enumeration in the worst case.

## Applications in Engineering

### 1. Polyhedral Combinatorial Optimization

**Column generation for integer programs**: The exponential number of induced paths necessitates **column generation algorithms** rather than explicit enumeration. This is used in:
- Network design problems with path-based formulations
- Scheduling with precedence constraints (paths in DAGs)
- Telecommunication network routing

### 2. Chordal Graph Algorithms

**Polynomial-time solvability on chordal graphs** enables efficient solution of:
- Maximum clique and weighted clique cover problems
- Sparse linear system solving (chordal structure in matrix factorization)
- Junctiontree inference in probabilistic graphical models

### 3. Graph Classification in Computer Vision / Pattern Recognition

Induced paths are used to distinguish graph classes:
- Identifying forbidden subgraph patterns in molecular graphs
- Detecting structural anomalies in network data
- Characterizing protein interaction networks

### 4. Cache-Oblivious Algorithm Design

Induced paths can model memory access patterns without explicit jumps, relevant to:
- Sequential scan locality in database query optimization
- Pipeline scheduling in compilers

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Induced Paths with Simple Paths

**Wrong**: "An induced path is just a path where we don't revisit vertices."

**Correct**: An induced path additionally forbids edges between *any* non-consecutive vertices, not just the immediate neighbors. This is a much stronger constraint.

### Mistake 2: Assuming Polynomial Enumeration Always

**Wrong**: "If a problem is solvable in polynomial time, we can afford to enumerate all induced paths."

**Correct**: While the *optimization* problem (finding the maximum weight induced path) is polynomial on chordal graphs, *enumerating* all induced paths remains exponential. The algorithm exploits the graph structure to avoid enumeration.

### Mistake 3: Generalizing Chordal Results Carelessly

**Wrong**: "If induced paths are tractable on chordal graphs, they must be tractable on all perfect graphs."

**Correct**: Tractability on chordal graphs relies on specific structural properties (all cycles ≥ 4 have chords). Perfect graphs lack these guarantees. Generalization to contraction-perfect graphs is open and likely intractable for weighted variants.

### Mistake 4: Overlooking the Role of Dual Variables

**Wrong**: "The pricing subproblem just finds any heavy induced path."

**Correct**: The dual variables $\mu_v$ and $\lambda_K$ fundamentally shape which paths are attractive to the column generation algorithm. A path with high vertex weights but poor clique-intersection properties may have negative reduced cost and be discarded.

## See Also

- [[chordal graph]] — graphs where all cycles of length ≥ 4 have