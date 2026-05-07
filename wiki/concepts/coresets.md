# Coresets

## Definition

A **coreset** is a small weighted subset of a larger dataset that provably approximates the original dataset for a specific computational problem. Formally, for a problem instance $P = (X, \mathcal{F})$ where $X$ is a dataset and $\mathcal{F}$ is a family of objective functions, a coreset $C \subseteq X$ with weights $w: C \to \mathbb{R}^+$ is an $(\varepsilon, \delta)$-coreset if:

$$\left| f(C) - f(X) \right| \leq \varepsilon \cdot f(X) + \delta$$

holds for all $f \in \mathcal{F}$ (or a subset of interest).

**Key characteristic**: Coresets are *problem-specific* and *certificate-bearing*—they come with theoretical guarantees that solutions computed on the coreset approximate solutions on the original data within controlled error bounds.

## Key Equations

### Error Guarantee
For clustering problems, the multiplicative error bound is:

$$\text{cost}(C, k) \leq (1 + \varepsilon) \cdot \text{cost}(X, k) + \delta$$

where $\text{cost}(X, k)$ is the optimal clustering cost on the full dataset.

### Coreset Size Bound
For $k$-median and $k$-means clustering in metric and Euclidean spaces:

$$|C| = O\left(\frac{k \log n}{\varepsilon^2}\right) \text{ or } O\left(\frac{k}{\varepsilon^d}\right)$$

depending on the metric and problem variant, where $n = |X|$ and $d$ is the ambient dimension.

### Weighted Objective Preservation
If $w(c)$ denotes the weight of coreset point $c$:

$$\sum_{x \in X} f(x) \approx_{(\varepsilon,\delta)} \sum_{c \in C} w(c) \cdot f(c)$$

## Physical Intuition / Derivation

### Why Coresets Matter

In massive datasets (billions of points), computing exact solutions is infeasible. A coreset compresses the data while guaranteeing that:
1. **Algorithms run on compressed data** → computational speedup
2. **Approximation guarantees transfer** → solutions on the coreset solve the original problem approximately

**Example: k-means clustering**

The full dataset $X$ might have $n = 10^9$ points. A coreset $C$ with $|C| = O(k \log n / \varepsilon^2) \approx 10^4$ points (for modest $k, \varepsilon$) allows running expensive clustering algorithms in seconds instead of hours, while maintaining an $(1+\varepsilon)$-approximation.

### Construction Strategy

Coresets are typically built via:

1. **Sensitivity-based sampling**: Points with high "importance" to the objective are sampled with higher probability
2. **Geometric decomposition**: Space is partitioned (e.g., via quadtrees, balls), and each region contributes points to the coreset
3. **Reweighting**: Points in dense regions are downweighted; isolated points upweighted

**Formal sampling**: For a point $x \in X$ with sensitivity $s(x)$:

$$\Pr[x \in C] = \min\left(1, c \cdot \frac{s(x) \bar{s}}{\sum_{x' \in X} s(x')}\right)$$

where $\bar{s}$ is the average sensitivity and $c$ is a concentration parameter.

### Error Analysis

The approximation error comes from:
- **Sampling error**: Random variance when selecting a subset
- **Reweighting error**: Adjusting weights to preserve aggregate statistics
- **Discretization error**: When grouping nearby points

These are controlled via Chernoff bounds and concentration inequalities, yielding high-probability guarantees that hold for all functions in $\mathcal{F}$ simultaneously.

## Applications in Engineering

### 1. **Clustering at Scale**
- $k$-means, $k$-median on massive point clouds (images, documents, sensor data)
- Replace expensive Lloyd iterations on $10^9$ points with fast iterations on $10^4$-point coreset
- Enables real-time clustering in streaming/online settings

### 2. **Computational Geometry**
- **Furthest-neighbor queries** (de Berg & Theocharous, 2024): A coreset for a simple polygon allows approximate nearest/furthest neighbor queries with $O(\log |C|)$ space
- **Ball covers**: Approximating geometric covering problems (Chepoi et al., 2007)

### 3. **Machine Learning & Data Mining**
- Feature selection and dimensionality reduction
- Training neural networks on summarized datasets
- Outlier detection (points not in any coreset cell are potentially anomalous)

### 4. **Distributed & Streaming Algorithms**
- **Merge-reduce paradigm**: Each machine computes a coreset; merge coresets hierarchically
- **Streaming**: Maintain a coreset as data arrives incrementally; space complexity $O(\log^* n)$ (or poly-logarithmic)

### 5. **Optimization Problems**
- Facility location, facility placement
- Submodular optimization
- Linear regression and $\ell_p$ regression fitting

## Common Mistakes / Pitfalls

### 1. **Assuming Coresets are Universal**
❌ *Mistake*: "This coreset works for any clustering problem."  
✓ *Correct*: Coresets are problem-specific. A coreset for $k$-means is not necessarily a coreset for $k$-median or $k$-center.

### 2. **Ignoring Dimension Dependence**
❌ *Mistake*: Applying a Euclidean coreset in high dimensions without checking complexity.  
✓ *Correct*: Many bounds scale as $O(k/\varepsilon^d)$, which explodes in high $d$. Metric coresets avoid this via $O(k\log n/\varepsilon^2)$.

### 