# Recourse Complexity

## Definition

**Recourse complexity** measures the total number of changes (updates) required to a data structure or solution as new information arrives in a streaming or online setting. Specifically, in the context of low-rank matrix approximation, recourse quantifies how many of the $k$ basis vectors (or "factors") must be recomputed when a new data point arrives.

Formally, given a stream of data $A(1), A(2), \ldots, A(n)$ where $A(t)$ contains the first $t$ rows of matrix $A$, recourse is the total number of modifications to the maintained rank-$k$ approximation across all $n$ time steps:

$$\text{Recourse} = \sum_{t=1}^{n} \left| \text{changes to basis at step } t \right|$$

## Key Equations

**Optimal low-rank approximation cost:** For a matrix $A \in \mathbb{Z}^{n \times d}$ and rank $k < r = \text{rank}(A)$, the Frobenius norm cost is:

$$\text{Cost}_k(A) = \min_{V: \text{rank}(V) = k} \|A - PV(A)\|_F^2$$

where $PV$ denotes projection onto the subspace $V$.

**Theorem 1.1 (Sublinear additive error recourse):**
For integer matrix $A \in \mathbb{Z}^{n \times d}$ with rank $r > k$ and bounded entries $|a_{ij}| \leq M$, there exists an algorithm achieving:

$$\text{Recourse} = O\left(\frac{k}{\varepsilon}\log(ndM)\right)$$

while maintaining approximation error:

$$\left|\text{Cost}_k(A(t)) - \widehat{\text{Cost}}_k(A(t))\right| \leq \varepsilon \|A(t)\|_F^2$$

at all times $t \in [n]$.

**Theorem 1.2 (Linear recourse under bounded condition number):**
For streams with online condition number $\kappa_{\text{online}} \leq \text{poly}(n)$:

$$\text{Recourse} = O\left(\frac{k}{\varepsilon^2}\log^3 n\right)$$

achieving $(1+\varepsilon)$-multiplicative approximation to the optimal rank-$k$ subspace.

## Physical Intuition / Derivation

### Why Recourse Matters

In streaming/online settings, recomputing a basis from scratch is prohibitively expensive. Recourse quantifies the **stability** of the solution: low recourse means the algorithm can maintain a good approximation with minimal structural changes.

### The Fundamental Trade-off

A key insight from the theory is that **optimal low-rank approximations are inherently unstable**:

- The optimal subspace $V(t-1)$ at time $t-1$ may differ substantially from $V(t)$ at time $t$, even after adding just one new row.
- In the worst case, $\Omega(nk)$ recourse is necessary to always maintain the mathematically optimal rank-$k$ subspace—this requires recomputing all $k$ basis vectors at each of $n$ steps.

### Relaxations Enable Efficiency

The source material shows that by **relaxing the optimality requirement**, we can achieve sublinear recourse:

1. **Additive error relaxation** (Theorem 1.1): Instead of minimizing $\|A(t) - \text{best rank-}k\|_F^2$ exactly, we allow error $\varepsilon \|A(t)\|_F^2$. This permits basis reuse across many steps, yielding recourse $O(k \log(ndM)/\varepsilon)$—potentially sublinear in $n$.

2. **Condition number assumption** (Theorem 1.2): If the online condition number is bounded, the optimal subspace changes gradually. Perturbation theory shows that rank-one updates cause only $O(1)$ changes to the top-$k$ singular vectors, enabling amortized linear recourse in $k$.

### Perturbation Analysis

The key lemma (2.3) states: under bounded online condition number, rank-one perturbations induce only $O(1)$ distance in the optimal rank-$k$ subspace. This allows "blocking" multiple updates before recomputation becomes necessary.

## Applications in Engineering

### Machine Learning & Online Learning
- **Real-time dimensionality reduction**: Maintaining PCA-like projections as data streams arrive (e.g., sensor networks, financial feeds)
- **Concept drift handling**: Detecting when the low-rank structure has shifted significantly enough to warrant basis update
- **Budget-conscious incremental learning**: Trading approximation quality for computational budget constraints

### Numerical Linear Algebra & Optimization
- **Incremental SVD**: Updating singular value decompositions of evolving matrices without full recomputation
- **Kaczmarz/stochastic gradient methods**: Analyzing update frequency for basis vectors in iterative solvers
- **Sparse matrix updates**: Efficiently managing structural changes in compressed representations

### Signal Processing & Data Compression
- **Adaptive compression**: Video streaming where key frames dictate when to recompute basis (codebook)
- **Network traffic analysis**: Maintaining low-rank models of traffic matrices with periodic updates

### Control & Systems Theory
- **Subspace identification under online perturbations**: Tracking dominant modes in dynamical systems with evolving dynamics
- **Robust state estimation**: Balancing model fidelity against computational cost in real-time state observers

## Common Mistakes / Pitfalls

1. **Confusing recourse with approximation error**: Low recourse does not guarantee low approximation error, and vice versa. Theorem 1.1 achieves low recourse but allows additive $\varepsilon \|A(t)\|_F^2$ error. These are decoupled objectives.

2. **Assuming additive vs. multiplicative error are equivalent**: Multiplicative $(1+\varepsilon)$-error (Theorem 1.2) is much harder to achieve than additive $\varepsilon \|A(t)\|_F^