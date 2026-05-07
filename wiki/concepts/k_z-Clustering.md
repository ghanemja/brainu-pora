# (k, z)-Clustering

## Definition

**(k, z)-Clustering** is a generalization of the classic $k$-means and $k$-median clustering problems in metric spaces (particularly Euclidean spaces), where the goal is to partition a dataset into $k$ clusters to minimize the sum of the $z$-th power of distances from each point to its nearest cluster center.

**Formal Statement:** Given a set of $n$ points $P \subseteq \mathbb{R}^d$ and parameters $k$ (number of clusters) and $z$ (distance power), find a set of $k$ centers $C = \{c_1, \ldots, c_k\}$ that minimizes:

$$\text{Cost}(P, C) = \sum_{p \in P} \min_{c \in C} \|p - c\|^z$$

**Special cases:**
- $z = 1$: $k$-**Median** problem
- $z = 2$: $k$-**Means** problem
- General $z > 0$: handles variable distance power penalties

The problem is $\mathcal{NP}$-hard for $k \geq 2$ and $d \geq 2$, requiring approximation algorithms in practical settings.

## Key Equations

**Objective Function:**
$$\text{Cost}(P, C) = \sum_{i=1}^{n} d(p_i, C)^z, \quad \text{where} \quad d(p_i, C) = \min_{c \in C} \|p_i - c\|$$

**Approximation Ratio:** An algorithm achieves $\alpha$-approximation if:
$$\mathbb{E}[\text{Cost}_{\text{alg}}(P, C)] \leq \alpha \cdot \text{OPT}(P, C)$$

**Optimal Value Estimation:** With additive error bounds:
$$|\text{OPT}_{\text{est}} - \text{OPT}_{\text{true}}| \leq \delta \cdot \text{OPT}_{\text{true}}$$

## Physical Intuition / Derivation

### Why (k, z)-Clustering Matters

The parameter $z$ controls **distance sensitivity**:
- Small $z$ (e.g., $z=1$): Clustering is **robust to outliers** because distant points contribute linearly
- Large $z$ (e.g., $z=2$): Clustering is **sensitive to outliers** (distances are squared), pulling centers toward extreme points

### Computational Challenge

The source material identifies a fundamental tension in clustering algorithm design:

1. **Graph-Based Approaches** (Jain-Vazirani framework):
   - Use ruling sets on geometric graphs
   - Inherent complexity: graph problems require $\Omega(\log n)$ rounds or more due to lower bounds
   - Cannot exploit Euclidean structure beyond basic connectivity

2. **Tree Embedding Approaches**:
   - Achieve polylog$(n)$-approximation for $k$-Median via probabilistic tree embeddings
   - **Critical limitation**: Embeddings incur $\Omega(\log n)$ metric distortion (lower bound from Bourgain, 1985)
   - Cannot extend to powers $z > 1$ (ill-suited for handling $d(p,c)^z$ when $z \neq 1$)

### Breakthrough Insight

The new framework ([source paper] Theorem 1.1) **breaks the tree embedding barrier** by:
- Directly leveraging **Euclidean geometric primitives** (approximate range queries, metric ruling sets)
- Avoiding global graph constructions that inherit lower bounds
- Implementing in **MPC (Massively Parallel Computation)** with constant rounds
- Achieving $O(1)$-approximation for cost *estimation* (first of its kind)

### Round Efficiency

Key assumption: $d = O(\log n)$ (intrinsic or via preprocessing). This allows:
- Geometric decomposition into $O(\log n)$ levels
- Each level: $O(1)$ communication rounds
- Total: $O(1)$ rounds for fully-scalable distributed algorithms

## Applications in Engineering

### 1. **Data Center Resource Allocation**
   - Cluster virtual machines or workloads ($k$ resource pools)
   - Use $z > 1$ to penalize outliers (high-latency or resource-hungry tasks)
   - Minimize average $z$-th power of distance to nearest center

### 2. **Geospatial Service Placement**
   - Deploy $k$ server farms to minimize latency$^z$ to customers
   - $z=2$: penalizes very distant regions (emergency services)
   - $z=1$: balanced coverage (retail warehouses)

### 3. **Machine Learning Feature Clustering**
   - High-dimensional embeddings with varying importance
   - $z$ reflects sensitivity to embedding quality per task

### 4. **Supply Chain Optimization**
   - Determine $k$ distribution centers minimizing transportation cost$^z$
   - $z=2$: quadratic costs (fuel, wear scale nonlinearly)

### 5. **Distributed Computing / MPC**
   - Partition input data across $k$ machines
   - Minimize data skew measured in $\ell^z$ norm
   - Achievable in $O(1)$ rounds if dimension $d = O(\log n)$

## Common Mistakes / Pitfalls

### 1. **Conflating $z$-Clustering with $z$-Norm**
   **Error:** Assuming $(k,z)$-Clustering minimizes $\|\text{something}\|_z$-norm.
   
   **Correct:** It minimizes the **$z$-th power of Euclidean distances**, i.e., $\sum d(p_i, C)^z$ where $d$ is Euclidean distance, not a $\ell_z$ norm of residuals.

### 2. **Tree Embeddings Are Universal**
   **Error:** Believing tree embeddings can extend to all $(k,z)$ problems.
   
   **Correct:** Tree embeddings inherently distort distances by $\Omega(\log n)$