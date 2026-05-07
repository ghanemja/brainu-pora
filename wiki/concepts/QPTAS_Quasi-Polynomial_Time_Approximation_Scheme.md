# QPTAS (Quasi-Polynomial Time Approximation Scheme)

## Definition

A **Quasi-Polynomial Time Approximation Scheme (QPTAS)** is a family of approximation algorithms that, for any constant $\varepsilon > 0$, produces a $(1+\varepsilon)$-approximate solution to an optimization problem in time bounded by $\text{poly}(n) \cdot 2^{\text{poly}(\log n)}$, where $n$ is the input size.

More precisely, a QPTAS for an optimization problem $\Pi$ is an algorithm $A_\varepsilon$ such that:
- **Input:** instance $I$ of size $n$, approximation parameter $\varepsilon > 0$
- **Output:** feasible solution with objective value within factor $(1+\varepsilon)$ of optimal
- **Runtime:** $n^{f(1/\varepsilon)} \cdot \text{poly}(\log n)$ where $f$ is an arbitrary function

The key distinguishing feature is that the exponent of $n$ can depend on $1/\varepsilon$, but growth must be sub-polynomial in $\varepsilon^{-1}$.

### Relationship to other schemes:
- **PTAS** (Polynomial-Time Approximation Scheme): runs in $\text{poly}(n, 1/\varepsilon)$ — strictly faster than QPTAS
- **FPTAS** (Fully Polynomial-Time Approximation Scheme): runs in $\text{poly}(n, 1/\varepsilon)$ — stronger; allows output encoding in polynomial space
- **Approximation Algorithm:** produces a fixed-factor approximation in polynomial time

## Key Equations

The runtime bound for a QPTAS can be expressed as:

$$T(n, \varepsilon) = n^{O(\log(1/\varepsilon)/\varepsilon^2)} \text{ or } n^{O(1/\varepsilon)}$$

For the type-sparsity approach in the source material:

$$|X|^{O(\log(|X|/\varepsilon)/\varepsilon^2)}$$

where $|X|$ is the instance size and $\varepsilon$ is the approximation parameter.

**Approximation guarantee:**
$$\text{ALG}(I) \leq (1 + \varepsilon) \cdot \text{OPT}(I) \quad \text{for minimization}$$

**Total variation distance bound:**
$$d_{\text{TV}}(D, D') \leq O(\varepsilon) \Rightarrow \text{calibration error} \leq O(\varepsilon)$$

## Physical Intuition / Derivation

### Why QPTAS matters

The gap between polynomial and exponential time is vast. A QPTAS occupies a middle ground: it runs faster than brute force ($2^n$) but slower than true polynomial schemes. The key insight is **controlled discretization**—we trade off solution quality for computational tractability by working with simplified versions of the problem.

### Core Strategy: Type-Sparsity Reduction

The source material illustrates QPTAS construction through **type-sparsity**:

1. **Identify indistinguishability:** Elements of the same "type" (sharing identical prediction properties) are interchangeable. For binary classifications, all 0-valued elements are indistinguishable from each other.

2. **Reduce state space:** Instead of tracking individual elements, track how many of each type we've processed. With $k$ types, dynamic programming has $O(|X|^k)$ states instead of $2^{|X|}$.

3. **Discretize the distribution:** Round probabilities to coarse granularity $O(\varepsilon)$. This introduces controlled error:
   - **Uniform marginal case:** Rounding conditional probabilities to multiples of $O(\varepsilon)$ gives $O(1/\varepsilon)$ distinct types
   - **General case:** Discretizing both marginal and conditional probabilities yields $O(\log(|X|/\varepsilon)/\varepsilon^2)$ types

4. **Solve exact DP on discretized instance:** Run exact algorithm on simplified problem, incurring:
   - **Approximation error:** $O(\varepsilon)$ from discretization (via total variation distance)
   - **Computational cost:** $|X|^{O(\log(|X|/\varepsilon)/\varepsilon^2)}$ from DP states

### Why quasi-polynomial, not polynomial?

The exponent $\log(|X|/\varepsilon)/\varepsilon^2$ depends on both problem size and accuracy. As $\varepsilon \to 0$, the exponent grows unboundedly (though slower than polynomial in $1/\varepsilon$). This is fundamentally different from PTAS:

$$\text{QPTAS: } |X|^{O(\log(|X|/\varepsilon)/\varepsilon^2)} \text{ vs. PTAS: } |X|^{O(1/\varepsilon)} \cdot \text{poly}(\log |X|)$$

The quasi-polynomial class (solvable in $n^{\text{poly}(\log n)}$ time) naturally captures problems where state space blows up only logarithmically in the inverse accuracy.

## Applications in Engineering

### 1. **Resource Allocation & Scheduling**
- **Calibrated prediction systems:** Ensuring predictions match empirical frequencies (the source domain). QPTAS methods enable fast calibration verification for systems with few distinct predictor types (e.g., credit scoring with categorical variables).
- **Type-based clustering:** Engineering systems where items cluster into few distinguishable classes; QPTAS enables optimal partition of resource allocation.

### 2. **Machine Learning & Statistics**
- **Calibration distance computation:** For classifiers producing predictions on continuous $[0,1]$ domain, QPTAS provides fast approximate calibration metrics without expensive brute-force search.
- **Robust prediction:** When training data has only a few distinct feature vectors (frequent in practice for categorical data), type-sparsity naturally reduces search complexity.

### 3. **Optimization Under Uncertainty**
- **Probabilistic optimization:** Many engineering problems