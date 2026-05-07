# Exponential Time Hypothesis (ETH)

## Definition

The **Exponential Time Hypothesis (ETH)** is a foundational conjecture in parameterized complexity theory that asserts there is **no algorithm** solving the 3-SAT problem faster than $2^{O(n)}$ time, where $n$ is the number of variables.

More formally:

**ETH Conjecture:** There exists a constant $c > 0$ such that 3-SAT on $n$ variables cannot be solved in time $2^{cn}$.

In the context of parameterized algorithms with a parameter $k$ (such as treewidth), ETH implies:
- Problems with parameter $k$ cannot be solved in time $2^{o(k)} \cdot \text{poly}(n)$ unless the conjecture is false
- This provides **lower bounds** on algorithm runtime under reasonable complexity assumptions

## Key Equations

The ETH conjecture does not assert specific equations, but rather **conditional lower bounds** on runtime:

$$T(n) \geq 2^{\Omega(n)} \text{ for 3-SAT}$$

For parameterized problems with treewidth parameter $k$, ETH implies:

$$T(k, n) \geq 2^{\Omega(k)} \cdot \text{poly}(n) \text{ is not achievable}$$

More specifically, if an algorithm achieves running time:

$$T(k, n) = 2^{O(k \log k)} \cdot n^{O(1)}$$

then under ETH, there is **no faster algorithm** of the form:

$$T(k, n) = 2^{o(k \log k)} \cdot n^{O(1)}$$

## Physical Intuition / Derivation

### Why ETH Matters

ETH is not a theorem but a **reasonable complexity assumption**—analogous to $P \neq NP$, but more specific. It captures the intuition that:

1. **Exhaustive search is unavoidable for hard problems:** Some NP-hard problems (like 3-SAT) resist better algorithms, and the best known algorithms are roughly brute-force

2. **Parameterization trades dimensionality:** A problem parameterized by $k$ may be solvable in time $f(k) \cdot \text{poly}(n)$, but ETH constrains how fast $f(k)$ can grow

3. **Tightness in algorithms:** When an algorithm achieves $2^{O(k \log k)}$ runtime (as in the source material's Optimal Morse Matching algorithm), ETH provides evidence that this is **optimal**—no better dependence on $k$ exists

### How ETH Enables Lower Bounds

ETH doesn't directly prove lower bounds. Instead, it is used **conditionally**:

1. **Reduce** a problem $B$ to a 3-SAT variant known to satisfy ETH
2. **Preserve the parameter** under reduction (e.g., via Width Preserving Strategy framework)
3. **Conclude:** If $B$ had a $2^{o(k)}$ algorithm, then 3-SAT would violate ETH
4. **Therefore:** Under ETH, no $2^{o(k)}$ algorithm for $B$ exists

## Applications in Engineering

### 1. **Algorithm Design and Optimization**
- **Approximation algorithms:** When exact algorithms are ETH-hard, approximation or heuristic approaches become the practical choice
- **Fixed-parameter tractability:** Engineers can focus on parameterized algorithms for specific graph structures (bounded treewidth, bounded pathwidth)

### 2. **Computational Topology**
From the source material: The Optimal Morse Matching problem on CW complexes achieves $2^{O(k \log k)} n$ via treewidth parameterization. ETH shows this is **tight**—no fundamentally better algorithm exists under standard assumptions.

**Application:** Computational geometry, mesh simplification, and topological data analysis rely on such algorithms; ETH guides which refinements are worthwhile.

### 3. **Graph Algorithms and Network Design**
- **Directed Feedback Vertex Set (DFVS):** Finding minimum vertex feedback sets in digraphs is known to be $2^{\Theta(k)}$-hard under ETH when parameterized by solution size
- **Practical impact:** Network optimization problems involving cycle removal (e.g., breaking circular dependencies in software) require heuristics when exact algorithms are ETH-hard

### 4. **Constraint Satisfaction & Satisfiability**
- **SAT solvers:** Engineering of industrial SAT solvers (MiniSat, Glucose) acknowledges ETH by using techniques like:
  - Variable branching heuristics
  - Clause learning
  - Restarts
- These do not violate ETH but exploit problem structure in practice

### 5. **VLSI Design and EDA**
- Circuit satisfiability and timing verification problems reduce to SAT
- ETH justifies investment in **structure exploitation** (bounded treewidth decompositions, symmetry breaking) rather than purely algorithmic improvements

## Common Mistakes / Pitfalls

### 1. **Confusing ETH with P vs. NP**
- **Mistake:** "ETH proves P ≠ NP" or vice versa
- **Fact:** ETH is an independent conjecture; it could be true even if P = NP (though less interesting), and it's stronger than P ≠ NP

### 2. **Ignoring Parameter Choice**
- **Mistake:** Claiming "ETH prohibits all $2^{O(f(k))}$ algorithms" without specifying what $k$ is
- **Fact:** ETH applies to the specific choice of parameter. A problem may be $2^{O(k)}$ when $k = \text{treewidth}$ but $2^{O(k^2)}$ when $k = \text{pathwidth}$

### 3. **Forgetting the Polynomial Factor**
- **Mistake:** Treating $2^{O(k)}$ and $2^{o(k)} \cdot \text{poly}(n)$ as the same
- **Fact:** ETH disallows $2^{o(k)} \cdot n^{O(1)}$, but $2^{O(k