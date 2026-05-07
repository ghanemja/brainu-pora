# Approximation Algorithms

## Definition

An **approximation algorithm** is a polynomial-time algorithm that solves an optimization problem by computing a solution guaranteed to be within a known factor of the optimal solution. For a minimization problem, an $\alpha$-approximation algorithm produces a solution with value $\text{OPT} \leq \text{ALG} \leq \alpha \cdot \text{OPT}$, where $\alpha \geq 1$ is the **approximation ratio** (or approximation factor).

For maximization problems, the inequality reverses: $\text{ALG} \geq \frac{1}{\alpha} \cdot \text{OPT}$.

In the **approximate near neighbor problem** (a common approximation framework), given a metric space $(M, d_M)$, parameters $c \geq 1$ and $r > 0$, a $(c,r)$-approximation algorithm must:
- **Input**: a query point $q \in M$ with $d_M(q, X) \leq r$
- **Output**: a point $x \in X$ such that $d_M(q, x) \leq c \cdot r$

The factor $c$ is the approximation ratio; the algorithm trades exact optimality for computational efficiency.

---

## Key Equations

**Approximation Ratio Definition (Minimization)**
$$\alpha = \frac{\text{ALG}}{\text{OPT}}$$

**Approximation Ratio Definition (Maximization)**
$$\alpha = \frac{\text{OPT}}{\text{ALG}}$$

**Distance-Based Approximation Guarantee**
$$d_M(q, x) \leq c \cdot d_M(q, x^*)$$
where $x^*$ is the true nearest neighbor and $x$ is the approximate result.

**Query Complexity Trade-off** (from nearest neighbor search literature)
For fast query time $\text{poly}(d \log n)$, approximation ratios commonly achieve:
$$\text{Approx Ratio} \approx p^{O(1)} + \log \log p$$
for $\ell_p$ metric spaces with $p > 2$.

---

## Physical Intuition / Derivation

### Why Approximation Algorithms Matter

Exact algorithms for NP-hard problems often require exponential time. Approximation algorithms provide a principled way to trade **solution quality for computational speed**.

**Example: Nearest Neighbor Search**

Imagine searching for the closest point in a massive high-dimensional dataset. An exact algorithm must compare the query against every point: $O(n)$ distance computations. An approximation algorithm with ratio $c$ may return a point up to $c$ times farther away but use only $O(\log n)$ distance evaluations via **locality-sensitive hashing** or **space partitioning**.

### Building Intuition: Metric Spaces

In a metric space with distance metric $d$, approximate nearest neighbor relaxes the constraint:
- **Exact NNS**: Find $x^* = \arg\min_{x \in X} d(q, x)$
- **Approximate NNS**: Find $x$ where $d(q, x) \leq c \cdot d(q, x^*)$

For $\ell_p$ spaces (Minkowski norms), the approximation ratio depends on the dimension and the value of $p$:

$$\|x\|_p = \left( \sum_{i=1}^{d} |x_i|^p \right)^{1/p}$$

Higher $p$ (closer to $\ell_\infty$) generally requires worse approximation ratios in fast query-time regimes because the metric structure is less "clustered."

### Why Randomization Helps

Randomized approximation algorithms (which succeed with probability $\geq 2/3$) can achieve better approximation ratios and faster query times than deterministic variants by:
- Using randomized data structures (e.g., locality-sensitive hashing)
- Making random pivot choices to partition the space
- Amplifying success probability via independent trials

---

## Applications in Engineering

### 1. **Machine Learning & Nearest Neighbor Classification**
Approximate nearest neighbor is the backbone of $k$-NN classifiers. In modern systems with millions of examples, exact NNS is infeasible; a $c$-approximation may degrade classification accuracy by only $\sim c\%$ while reducing query time from $O(n)$ to $O(\log^k n)$.

### 2. **Information Retrieval & Vector Similarity Search**
Search engines and recommendation systems embed documents/items as high-dimensional vectors. Approximate similarity search (e.g., finding similar users, products, or documents) must handle billions of vectors; approximation ratios like $O(\log \log d)$ are acceptable trade-offs.

### 3. **Computational Geometry & Facility Location**
Approximation algorithms solve facility location problems: place $k$ facilities to minimize total distance to demand points. The classic greedy algorithm achieves $\ln(n)$-approximation; variants provide better ratios for specific geometric settings.

### 4. **Network Design & Routing**
Steiner tree and shortest path problems in large networks use approximation algorithms. A 2-approximation Steiner tree is often preferred to exponential-time exact computation.

### 5. **Image Search & Content-Based Retrieval**
Visual search systems embed images as feature vectors in $\ell_2$ spaces. Approximate nearest neighbor retrieval (with ratio $c \approx 1.5$) enables real-time search over billions of images.

### 6. **High-Dimensional Data Analysis**
In data mining, clustering, and dimensionality reduction, approximation algorithms handle high-dimensional spaces where exact methods fail. For $\ell_p$ metrics with $p > 2$, approximation ratios scale with $p^{O(1)}$, reflecting computational difficulty.

---

## Common Mistakes / Pitfalls

### 1. **Confusing "Approximation" with "Heuristic"**
- **Mistake**: Treating approximation algorithms and heuristics as interchangeable.
- **Reality**: Approximation algorithms come with *guaranteed* approximation ratios; heuristics have no such guarantee. An algorithm that is "usually