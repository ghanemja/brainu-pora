# Approximation factor

## Definition

An **approximation factor** (or **approximation ratio**) $\hat{c}$ is a multiplicative guarantee on the quality of an approximate solution relative to the optimal solution in an optimization problem. Formally, for a minimization problem with optimal value $\text{OPT}$ and approximate solution value $\text{ALG}$:

$$\text{ALG} \leq \hat{c} \cdot \text{OPT}$$

The approximation factor $\hat{c} \geq 1$ quantifies how far the approximate solution deviates from optimal; $\hat{c} = 1$ means the solution is optimal, while larger values indicate progressively worse approximations.

In the context of **approximate nearest neighbor (ANN) search**, an $\hat{c}$-approximate solution to a nearest neighbor query returns a point whose distance to the query is at most $\hat{c}$ times the distance to the true nearest neighbor.

## Key Equations

**Basic approximation guarantee:**
$$d(q, x') \leq \hat{c} \cdot d(q, x^*)$$

where $x^*$ is the true nearest neighbor and $x'$ is the $\hat{c}$-approximate solution.

**Geometric improvement through iteration:**
$$\hat{c}_i = \hat{c}_{i-1}^{1-2/p}$$

This shows how the approximation factor improves (decreases) across successive iterations of a refined search procedure, with convergence dependent on the ambient dimension $p$.

**Convergence criterion:**
After $k = O(p \log \log \hat{c}_0)$ iterations:
$$\hat{c}_k = 2^{O(p)}$$

At this point, further improvements become prohibitively expensive.

## Physical Intuition / Derivation

### Why Approximation Factors Matter

Exact solutions to many geometric problems—especially in high dimensions—are computationally prohibitive. The approximation factor framework trades exactness for computational efficiency in a quantifiable way.

### Iterative Refinement Pattern

The source material illustrates a powerful technique: **cascading approximations**. Starting with a coarse approximation $\hat{c}_0$:

1. Use an ANN data structure to find an approximate solution $x_i$ with factor $\hat{c}_i$
2. The diameter of the region around $x_i$ shrinks due to geometric properties (e.g., the Mazur map distortion)
3. Re-query within this smaller region with a refined ANN structure
4. Each iteration yields a better approximation $\hat{c}_{i+1} < \hat{c}_i$

The recurrence $\hat{c}_i = \hat{c}_{i-1}^{1-2/p}$ reveals **super-geometric convergence**: the exponent $1 - 2/p$ is less than 1, so improvements accelerate. For small $p$, convergence is fast; for large $p$, it slows.

### When to Stop Iterating

The algorithm terminates when $\hat{c}_k = 2^{O(p)}$ because:
- Further improvements require querying ANN structures on increasingly small regions
- The space/time complexity overhead exceeds the benefit of the marginal improvement
- The approximation factor is already polylogarithmic in practical terms

## Applications in Engineering

### 1. **Nearest Neighbor Search in High Dimensions**
- Machine learning: feature matching, clustering, k-NN classifiers
- Computer vision: image retrieval, SIFT matching
- Approximate factors allow sublinear-time queries in massive datasets (e.g., billions of vectors)

### 2. **Metric Embeddings and Dimensionality Reduction**
- Embedding high-dimensional metric spaces into $\ell_p$ spaces with controlled distortion
- Approximation factors quantify the quality of the embedding
- Applications: network design, routing protocols, distributed systems

### 3. **Geometric Data Structures**
- Range search with approximation guarantees
- Location-based services: finding nearby restaurants/hospitals within a radius
- Approximation factors allow trading exact geometry for query speed

### 4. **Algorithm Analysis**
- Approximation-factor analysis is standard in NP-hard problems (TSP, bin packing, scheduling)
- Engineering tradeoff: polynomial-time algorithms achieving constant or $O(\log n)$ factors are often acceptable

### 5. **Numerical Methods**
- Iterative solvers using approximation factors to measure convergence
- Control system design: acceptable error bounds on state estimation

## Common Mistakes / Pitfalls

1. **Confusing approximation factor with error percentage**: A factor of $\hat{c} = 1.5$ means the solution is 50% worse than optimal, not 1.5% worse.

2. **Assuming smaller factors always cost more**: While true asymptotically, sophisticated multi-level structures (as in the source material) can achieve better factors *without* proportional increases in complexity.

3. **Neglecting dimension dependence**: The convergence rate $\hat{c}_i = \hat{c}_{i-1}^{1-2/p}$ depends critically on $p$. High-dimensional problems may require more iterations and careful tuning of $p$.

4. **Ignoring hidden constants**: The notation $2^{O(p)}$ hides constants. For practical $p \in (2, 100)$, this can range from $2^2$ to $2^{100}$—a vast difference.

5. **Treating approximation factor as fixed throughout algorithm**: The source material shows factors *change* at each iteration; using the initial factor for complexity analysis is incorrect.

6. **Forgetting to account for sparsity**: The sparse neighborhood cover (Definition 4.1) ensures small space complexity through subsets of diameter $\beta r$; failing to respect this structure breaks the algorithm's efficiency guarantees.

## See Also

- [[Approximate Nearest Neighbor Search (ANN)]]
- [[Metric Embeddings]]
- [[Sparse Neighborhood Cover]]
- [[Computational Complexity and Hardness of Approximation]]
- [[High-Dimensional Geometry and Curse of Dimensionality]]

## Sources

- Lecture/paper excerpt on cascading ANN data structures with iterative approximation refinement (referencing Hadjicos