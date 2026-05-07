# bipartite perfect matching polytope

## Definition

A **bipartite perfect matching polytope** is the convex hull of all perfect matchings in a bipartite graph $G = (X \cup Y, E)$, where $|X| = |Y| = n$. A perfect matching $M$ is a set of edges such that every vertex is incident to exactly one edge in $M$.

Formally, the polytope is:
$$P_{\text{bpm}} = \text{conv}\{x \in \{0,1\}^{|E|} : x \text{ is a perfect matching}\}$$

where each $x_e \in \{0,1\}$ indicates whether edge $e$ is in the matching.

### Related Variant: Odd-Red Bipartite Perfect Matching Polytope

When edges are colored red and blue, the **odd-red bipartite perfect matching polytope** restricts to perfect matchings containing an *odd* number of red edges:
$$P_{\text{odd-red}} = \text{conv}\{x \in \{0,1\}^{|E|} : x \text{ is a perfect matching with odd red edges}\}$$

Similarly, the **exact bipartite perfect matching polytope** restricts to matchings with *exactly* $k$ red edges for fixed $k$.

## Key Equations

### Standard LP Relaxation
The classical relaxation uses degree constraints:
$$\sum_{e \in \delta(v)} x_e = 1 \quad \forall v \in X \cup Y$$
$$0 \le x_e \le 1 \quad \forall e \in E$$

where $\delta(v)$ denotes edges incident to vertex $v$.

### Parity Constraint for Odd-Red Variant
For odd-red matchings, one must additionally enforce:
$$\sum_{e \in R} x_e \equiv 1 \pmod{2}$$

where $R$ is the set of red edges.

## Physical Intuition / Derivation

### Why the Standard Relaxation is Insufficient

The degree constraint polytope alone does not describe the integer hull precisely. The fractional vertices (where $x_e = 1/2$ on all edges) are feasible for the LP relaxation but represent no actual perfect matching.

### Why Parity Makes the Problem Harder

The odd-red constraint introduces a **mod-2 constraint**, which fundamentally complicates polyhedral structure:

1. **Non-unimodular structure**: The constraint matrix is not totally unimodular, so standard matching polytope techniques fail.

2. **Exponential extension complexity**: Jia, Svensson, and Yuan proved that any *linear* description of $P_{\text{odd-red}}$ requires **exponentially many constraints** (in the size of $n$). This means no polynomial-sized system of linear inequalities can exactly characterize the polytope.

3. **Complex facets**: Even worse, the facets require coefficients with large magnitude and diversity—ruling out simple $\{0, \pm 1\}$-coefficient descriptions. This indicates the polytope exhibits genuinely intricate geometry rather than simple structure.

### Algorithmic Solvability vs. Polyhedral Complexity

Crucially, the odd-red bipartite perfect matching **problem is in P** (solvable in polynomial time), but its **polytope is intractable** to describe explicitly. This represents a deep separation between:
- **Algorithmic complexity**: Can find solutions efficiently
- **Polyhedral complexity**: Cannot describe solution set concisely

## Applications in Engineering

### 1. Deterministic Algorithms for Exact Matching
The polyhedral structure directly impacts deterministic algorithms for finding a perfect matching with exactly $k$ red edges—an open problem in randomized algorithms that has applications in:
- Scheduling with fairness constraints
- Bipartite resource allocation where certain resources must be allocated in controlled amounts

### 2. Combinatorial Optimization with Parity
Parity-constrained variants of classical problems arise in:
- **Network design**: Finding flows or cuts with odd cardinality (e.g., odd minimum cut problems)
- **Electrical network synthesis**: Parity constraints appear in T-join problems fundamental to Eulerian decomposition

### 3. Integer Programming Theory
Understanding the odd-red matching polytope informs the broader theory of **bimodular integer programs**, which have limited polyhedral understanding and applications in:
- Mixed-integer programming solvers
- Approximation algorithms for constrained matching and packing problems

## Common Mistakes / Pitfalls

### 1. Assuming Solvability Implies Simple Structure
**Mistake**: "The problem is polynomial-time solvable, so its polytope must have a nice description."

**Reality**: The odd-red perfect matching is solvable but has exponential extension complexity. Polyhedral complexity is independent of algorithmic complexity.

### 2. Expecting $\{0, \pm 1\}$ Coefficients Suffice
**Mistake**: Trying to relax parity-constrained problems using only "natural" constraints with coefficients in $\{0, \pm 1\}$.

**Reality**: The facets of $P_{\text{odd-red}}$ necessarily involve coefficients of large magnitude. The Jia-Svensson-Yuan relaxation is not exact and is hard to separate over.

### 3. Confusing Exact Description with Optimization
**Mistake**: Using "the problem is solvable" to justify working with loose LP relaxations.

**Reality**: For many combinatorial problems, one solves via combinatorial algorithms (e.g., augmenting paths, Edmond's algorithm), not via LP solvers. Loose relaxations don't harm tractability but do hinder dual bounds and approximation guarantees.

### 4. Underestimating Mod-2 Structure
**Mistake**: Treating parity constraints as minor perturbations of unconstrained matching problems.

**Reality**: Mod-2 constraints fundamentally destroy total unimodularity and introduce hard polyhedral complexity. They are conceptually close to other hard constraints (e.g., cardinality constraints in matroid polytopes).

## See Also

- [[matching polytope|Matching Polytopes and Edmonds' Characterization]]
- [[extension complexity|Extension Complexity and Communication Complexity]]
- [[T-join and odd cuts|T-Joins and Odd-