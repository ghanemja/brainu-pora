# LP-rounding algorithm

## Definition

An **LP-rounding algorithm** is a two-phase algorithmic technique for solving combinatorial optimization problems:

1. **LP Relaxation Phase**: Formulate a discrete (NP-hard) optimization problem as a linear program (LP) by relaxing integrality constraints on decision variables.
2. **Rounding Phase**: Convert the fractional LP solution into a feasible integer solution while maintaining approximation guarantees.

The rounding phase typically employs randomized or deterministic procedures to map fractional values $[0,1]$ to discrete assignments $\{0,1\}$ while bounding the degradation in objective value.

**Context in matroid intersection**: LP-rounding is particularly powerful for matroid intersection problems where the constraint structure (independence oracles) is difficult to handle combinatorially. The LP relaxation captures matroid constraints via the matroid polytope, and the rounding algorithm exploits structural properties of the fractional solution to produce a valid independent set.

## Key Equations

For a matroid intersection problem with $k$ matroids $M_1, \ldots, M_k$ on universe $U$, the LP relaxation takes the form:

$$\max \sum_{e \in U} c_e x_e$$

subject to:

$$\sum_{e \in S} x_e \leq r_i(S) \quad \forall S \subseteq U, \forall i \in [k]$$

$$0 \leq x_e \leq 1 \quad \forall e \in U$$

where $r_i(S)$ is the rank function of matroid $M_i$.

The **approximation ratio** $\alpha$ relates the LP optimum $\text{OPT}_{\text{LP}}$ to the integer optimum $\text{OPT}$:

$$\text{OPT}_{\text{int}} \geq \frac{1}{\alpha} \text{OPT}_{\text{LP}}$$

For $k$-matroid intersection coloring, the state-of-the-art LP-rounding achieves:

$$\text{coloring approximation} = O(k(k-1) \chi_{\max})$$

where $\chi_{\max}$ is the maximum chromatic number among individual matroids.

## Physical Intuition / Derivation

### Why LP Relaxation?

Matroid intersection problems have rich structure captured by polytopes, but the integrality gap between the LP relaxation and the integer optimum can be significant. However, the LP solution provides a **fractional embedding** that reveals latent geometric structure.

### Rounding Strategy

The rounding algorithm exploits the following insight:

1. **Obtain fractional solution** $x^* \in [0,1]^{|U|}$ satisfying all LP constraints (matroid rank inequalities).

2. **Identify structure**: Even though $x^*$ may not directly encode an independent set, it contains embedded independent sets. The key observation is that:
   - Elements with high fractional value tend to cluster in independent sets
   - Multiple independent sets can be "extracted" via lexicographic ordering, sampling, or greedy procedures

3. **Iterative extraction**: Repeatedly find approximate independent sets (possibly with slightly relaxed constraints) and use them to form a coloring:
   - Find an independent set $I_1$ that covers "most" of the value in $x^*$
   - Update remaining fractional values
   - Repeat $O(k)$ or $O(k^2)$ times

4. **Approximation loss**: Each rounding iteration loses a factor depending on the matroid structure (e.g., rank of smallest contracted matroid). For $k$ matroids, cumulative loss yields $O(k(k-1))$.

### Concreteness: Two-Matroid Case

For two matroids $M_1, M_2$:
- The LP polytope is the intersection of two matroid polytopes
- A fractional solution is a convex combination of $O(n)$ basis pairs (by Carathéodory)
- Rounding can decompose this into $O(1)$ independent sets by finding "rainbow" independent sets respecting lexicographic optimality

## Applications in Engineering

### 1. **Resource Allocation & Scheduling**
- Assigning tasks to processors under multiple independence constraints (e.g., bandwidth limits, memory bounds)
- Two-matroid rounding guarantees near-optimal allocation despite NP-hardness

### 2. **Network Design**
- **Degree-bounded spanning trees**: Finding low-degree networks satisfying connectivity (matroid 1) and degree bounds (matroid 2)
- LP-rounding provides $(2 + \epsilon)$-approximation to optimal degree-bounded networks

### 3. **Combinatorial Optimization in Compiler Design**
- **Instruction scheduling**: Respecting both data dependencies (matroid) and resource constraints (matroid)
- LP-rounding produces provably good schedules

### 4. **Matroid Basis Coloring (Rota's Conjecture Context)**
- **Basis selection problems**: Decomposing multiple bases into monochromatic independent sets
- Applied in linear algebra decompositions and tensor optimization

### 5. **Submodular Maximization**
- LP-rounding extends to constrained submodular optimization (e.g., maximizing information gain subject to matroid constraints)

### 6. **Bipartite Matching with Constraints**
- Two-matroid LP-rounding solves degree-constrained matching more efficiently than set cover approaches

## Common Mistakes / Pitfalls

### 1. **Confusing Integrality Gap with Approximation Ratio**
- The LP integrality gap is $\Omega(k)$ for $k$-matroid intersection
- But the LP-rounding *algorithm* may achieve better guarantees by carefully using the fractional solution's structure
- **Error**: Assuming the rounding ratio equals the integrality gap

### 2. **Ignoring Matroid-Specific Structure**
- Generic LP-rounding (e.g., randomized rounding) gives $O(k \log n)$ for $k$-matroid intersection
- Exploiting matroid-specific properties (rank functions, lexicographic orderings) is essential for $O(k^2)$ improvements
- **Error**: Treating all constraints