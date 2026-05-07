# chromatic number

## Definition

The **chromatic number** $\chi(G)$ of a graph $G = (V, E)$ is the minimum number of colors required to assign a color to each vertex such that no two adjacent vertices share the same color. This is called a **proper coloring** of the graph.

More generally, for a matroid $M = (U, \mathcal{I})$, the chromatic number $\chi(M)$ is the minimum number of independent sets needed to partition the ground set $U$. An **independent set** in a matroid is any set belonging to the family $\mathcal{I}$ of independent sets.

For **matroid intersection coloring**, given $k$ matroids $M_1, M_2, \ldots, M_k$ on a common ground set $U$, the chromatic number is the minimum number of colors needed to partition $U$ into color classes $S_1, S_2, \ldots, S_c$ such that each $S_i$ is independent in **all** $k$ matroids simultaneously.

## Key Equations

For a single graph or matroid, the chromatic number satisfies:
$$\chi(G) \geq \omega(G)$$
where $\omega(G)$ is the **clique number** (size of the largest clique). For bipartite graphs, $\chi(G) = 2$.

For matroid intersection coloring with $k$ matroids:
$$\chi_{\text{intersection}}(M_1, \ldots, M_k) \leq (2k-1) \chi_{\max}$$
where $\chi_{\max} = \max_i \chi(M_i)$ is the maximum chromatic number among individual matroids.

For two matroids specifically:
$$\chi_{\text{intersection}}(M_1, M_2) \leq 2\chi_{\max}$$

The **approximation ratio** for a polynomial-time algorithm is:
$$\text{Approximation Ratio} = \frac{\text{Algorithm Output}}{\text{Optimal Solution}}$$

## Physical Intuition / Derivation

### Graph Coloring Context
Imagine you need to schedule $n$ meetings (vertices) in different time slots (colors), where certain meetings cannot occur simultaneously if the people involved would conflict (edges between vertices). The chromatic number tells you the minimum number of time slots required.

For simple cases:
- A **path graph** (vertices in a line) needs only 2 colors
- A **complete graph** $K_n$ (all vertices connected) needs $n$ colors
- A **cycle** of odd length needs 3 colors; even-length cycles need 2

### Matroid Coloring Context
Matroids generalize independence in linear algebra. For example, the matroid of linearly independent vectors in $\mathbb{R}^d$ has chromatic number at most $d+1$ (by a greedy coloring argument).

For **matroid intersection**, the challenge is much harder: you must partition elements so that each partition is independent in *all* matroids simultaneously. The non-constructive bounds (e.g., $2\chi_{\max}$ for two matroids) come from topological Hall's theorem and Sperner's Lemma, but don't yield algorithms.

**Why is this hard?** Greedy coloring works for single matroids but fails for intersections, because a set that is independent in $M_1$ might force dependence in $M_2$.

## Applications in Engineering

### 1. **Frequency Allocation in Wireless Networks**
Assign radio frequencies (colors) to transmitters (vertices) such that nearby transmitters don't interfere. This is the classic graph coloring problem. When multiple constraints apply (e.g., distance, power, antenna patterns), matroid intersection coloring becomes relevant.

### 2. **Task Scheduling with Resource Constraints**
Schedule jobs on processors where:
- Certain jobs cannot run simultaneously (graph edges)
- Resource constraints form matroids (e.g., bandwidth, memory, power budgets)
Colors represent time slots; the goal is to minimize total execution time.

### 3. **Register Allocation in Compilers**
Assign CPU registers to variables in a program. Graph coloring on the **interference graph** (two variables are adjacent if they must live simultaneously). Real processors have matroid constraints on register types and access patterns.

### 4. **Basis Conjecture Applications** (Rota's Conjecture)
The paper's application: given multiple bases of matroids with shared ground sets, partition elements so each color class can be completed to a basis in all matroids. This has applications in:
- Combinatorial designs
- Linear algebra over finite fields
- Error-correcting codes

### 5. **Routing in VLSI Design**
Route wires (colors = wire layers) on a chip respecting:
- Non-crossing constraints (graph coloring)
- Matroid constraints from circuit topology

## Common Mistakes / Pitfalls

1. **Confusing chromatic number with other graph properties:**
   - $\chi(G)$ ≠ minimum degree + 1 (this is an upper bound)
   - $\chi(G)$ ≠ degeneracy (though closely related)
   - $\chi(G)$ ≠ clique cover number (dual problem)

2. **Greedy coloring doesn't give optimal coloring:**
   Greedy algorithms give $\chi(G) \leq \Delta(G) + 1$ where $\Delta$ is max degree, but often use far more colors than necessary.

3. **Assuming matroid intersection coloring reduces to graph coloring:**
   A direct reduction loses the matroid structure and gives weaker bounds. The paper's key contribution is a **flexible decomposition** technique that preserves matroid structure while avoiding this pitfall.

4. **Thinking approximation algorithms always exist:**
   Graph coloring is $NP$-hard to approximate to within factor $n^{1-\epsilon}$ for general graphs. For matroids, good approximations require exploiting matroid properties explicitly.

5. **Underestimating the power of non-constructive proofs:**
   Topological proofs (Hall's theorem, Sperner's Lemma) *prove* bounds exist but give no algorithm. Constructivizing them—the paper's achievement—requires new structural insights.