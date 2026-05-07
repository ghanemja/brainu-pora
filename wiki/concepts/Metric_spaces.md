# Metric spaces

## Definition

A **metric space** is a pair $(M, d)$ consisting of a set $M$ (the "points" or "elements") and a function $d: M \times M \to \mathbb{R}_{\geq 0}$ (the "distance" or "metric") that satisfies four axioms for all $x, y, z \in M$:

1. **Non-negativity**: $d(x, y) \geq 0$
2. **Identity of indiscernibles**: $d(x, y) = 0 \iff x = y$
3. **Symmetry**: $d(x, y) = d(y, x)$
4. **Triangle inequality**: $d(x, z) \leq d(x, y) + d(y, z)$

The triangle inequality is the defining property that distinguishes metric spaces from mere distance functions—it enforces a geometric consistency where "going directly" is never longer than "taking a detour."

## Key Equations

The most commonly studied metric spaces in engineering are $\ell_p$ spaces, where the metric is:

$$d_p(x, y) = \left(\sum_{i=1}^{d} |x_i - y_i|^p\right)^{1/p}$$

for $p \geq 1$ and vectors $x, y \in \mathbb{R}^d$.

**Special cases:**
- $\ell_1$ (Manhattan/taxicab distance): $d_1(x, y) = \sum_{i=1}^{d} |x_i - y_i|$
- $\ell_2$ (Euclidean distance): $d_2(x, y) = \sqrt{\sum_{i=1}^{d} (x_i - y_i)^2}$
- $\ell_\infty$ (Chebyshev distance): $d_\infty(x, y) = \max_{i=1}^{d} |x_i - y_i|$

For a general metric space $(M, d)$, the **distance from a point to a set** is defined as:

$$d(q, X) = \min_{x \in X} d(q, x)$$

## Physical Intuition / Derivation

### Why Metric Spaces Matter

A metric space provides the minimal mathematical structure needed to talk meaningfully about **proximity** and **similarity**. The triangle inequality ensures that distances behave intuitively: if you can go from $A$ to $C$ directly, or via $B$, the direct path is never longer. This property is fundamental to why nearest-neighbor algorithms work reliably.

### Intuition via $\ell_p$ Norms

The family of $\ell_p$ metrics reveals how the choice of distance function reflects different problem semantics:

- **$\ell_1$ distance** counts taxicab steps—natural in urban navigation or when costs accumulate linearly along each coordinate.
- **$\ell_2$ distance** emerges from Pythagorean geometry—natural for physical distances in 2D/3D, and computationally convenient (differentiable, norm-preserving under rotation).
- **$\ell_\infty$ distance** asks "what's the largest discrepancy in any dimension?"—natural in robust optimization where you want to minimize the worst-case error.

As $p$ increases from 1 to $\infty$, the $\ell_p$ ball transitions from a diamond shape to a circle to a square. This geometric shift affects algorithm behavior: high-$p$ metrics are "smoother" in some algorithmic senses, but may be more computationally expensive.

### The Approximate Near Neighbor Problem

Real applications rarely need the *exact* nearest neighbor—a nearby point suffices. The **$(c, r)$-Approximate Near Neighbor (ANN)** problem formalizes this: given distance threshold $r$ and approximation factor $c \geq 1$, find any point $x \in X$ within distance $cr$ of query $q$ (when $q$ is already within distance $r$ of the dataset). This relaxation enables dramatically faster algorithms.

## Applications in Engineering

### 1. Machine Learning & Similarity Search
- **k-NN classification and clustering**: Assign query points to classes/clusters based on nearest training examples. Metric spaces enable efficient indexing (e.g., ball trees, KD-trees).
- **Approximate nearest neighbor search (ANN)**: Modern recommendation systems and image retrieval use approximate metrics and fast ANN data structures to handle billions of points.

### 2. Robotics & Navigation
- **Path planning**: Compute distances in configuration space (often non-Euclidean) to find collision-free paths. Metric spaces validate admissible heuristics for A* search.
- **Obstacle avoidance**: $\ell_\infty$ distance (Chebyshev) naturally encodes axis-aligned bounding-box checks.

### 3. Signal Processing & Computer Vision
- **Nearest-neighbor denoising**: Denoise signals by replacing each point with an average of nearby neighbors in a learned metric space.
- **Face recognition and person re-identification**: Embed faces as points in a learned metric space (via deep metric learning) where distances reflect identity.

### 4. Information Retrieval & Databases
- **Full-text search and semantic similarity**: Map documents to vector embeddings in metric spaces; query returns nearest neighbors.
- **Database indexing**: Metric indices (cover trees, ball trees) accelerate range queries and nearest-neighbor joins on unstructured data.

### 5. Numerical Optimization
- **Convergence analysis**: Metric space structure underpins proof that gradient descent stays close to optimality (ball-around-optimum argument).
- **Approximation guarantees**: Metric approximation factors bound how far an algorithm's solution is from optimal.

## Common Mistakes / Pitfalls

### 1. Confusing $\ell_p$ norms with similarity metrics
**Mistake:** Using $1 - \cos(\theta)$ as a "distance"—it's a dissimilarity but does *not* satisfy the triangle inequality for all pairs.  
**Fix:** Verify axioms explicitly, or use standard metric families ($\ell_p$, geodesic distances on manifolds).

### 2. Assuming