# Wasserstein Distance / Optimal Transport

## Definition

The **Wasserstein distance** (also called **earth mover's distance** or **optimal transport cost**) is a metric that measures the minimum cost required to transform one probability distribution into another by "moving" probability mass optimally.

Given two probability distributions $\mu$ and $\nu$ over a metric space $(X, d)$, the $p$-Wasserstein distance is defined as:

$$W_p(\mu, \nu) = \left(\inf_{\pi \in \Pi(\mu,\nu)} \int_{X \times X} d(x,y)^p \, d\pi(x,y)\right)^{1/p}$$

where $\Pi(\mu,\nu)$ is the set of all **couplings** (joint distributions) with marginals $\mu$ and $\nu$.

**Intuition:** Imagine $\mu$ represents a pile of sand at location $x$ and $\nu$ represents a hole at location $y$. The Wasserstein distance is the minimum total "cost" of transporting all sand from piles to holes, where the cost is proportional to distance times mass moved.

For the **1-Wasserstein distance** (most common in applications):

$$W_1(\mu, \nu) = \inf_{\pi} \mathbb{E}_{(x,y) \sim \pi}[d(x,y)]$$

## Key Equations

### 1-Wasserstein (Earth Mover's Distance)
$$W_1(\mu, \nu) = \inf_{\pi \in \Pi(\mu,\nu)} \int d(x,y) \, d\pi(x,y)$$

### Discrete Case (Finite Supports)
For empirical distributions on finite sets, the problem becomes a linear program:
$$W_1(\mu, \nu) = \min_{\pi} \sum_{i,j} d(x_i, y_j) \pi_{ij}$$
subject to:
- $\sum_j \pi_{ij} = \mu_i$ (marginal constraints)
- $\sum_i \pi_{ij} = \nu_j$
- $\pi_{ij} \geq 0$

### Kantorovich-Rubinstein Duality
$$W_1(\mu, \nu) = \sup_{\|f\|_L \leq 1} \left|\int f \, d\mu - \int f \, d\nu\right|$$

where the supremum is over all 1-Lipschitz functions. This dual formulation is computationally tractable and reveals that Wasserstein distance measures the maximum discrepancy across all Lipschitz-constrained test functions.

### Transportation Cost Decomposition
For a partition of the domain into regions, the total transport cost is:
$$\text{Cost}(\mu \to \nu) = \sum_{\text{regions}} \text{(mass in region)} \times \text{(internal transport cost)}$$

This additive structure is crucial for lower-bounding transport costs (as shown in the calibration analysis).

## Physical Intuition / Derivation

### Why "Optimal"?

The Wasserstein distance solves a fundamental problem: **how should we match mass in one distribution to mass in another to minimize total transport?**

Consider two discrete point masses:
- $\mu$: point masses $m_1, m_2, \ldots$ at locations $x_1, x_2, \ldots$
- $\nu$: point masses $n_1, n_2, \ldots$ at locations $y_1, y_2, \ldots$

A **coupling** $\pi_{ij}$ specifies how much mass moves from $x_i$ to $y_j$. The optimal coupling minimizes total "effort" (distance × mass).

### Contrast with Other Distances

| Distance | Formula | Limitation |
|----------|---------|-----------|
| **KL Divergence** | $D_{KL}(\mu\|\|\nu) = \int \log(\mu/\nu) d\mu$ | Not metric; asymmetric; infinite if supports don't overlap |
| **Total Variation** | $TV(\mu,\nu) = \frac{1}{2}\int\|\mu - \nu\|$ | Ignores geometry of space; $= 0$ or $1$ for disjoint supports |
| **Wasserstein** | $W_1 = \inf_\pi \mathbb{E}[d(x,y)]$ | **Metric, geometry-aware, differentiable w.r.t. distributions** |

The Wasserstein distance is **geometrically sensitive**: moving a distribution by distance $\delta$ costs approximately $\delta$ in Wasserstein, whereas other distances may be insensitive.

### Lower Bounds via Monge's Problem

When coupling is one-to-one (bipartite matching), the Monge formulation gives:
$$W_1(\mu, \nu) \geq \inf_{\sigma} \int d(x, \sigma(x)) \, d\mu(x)$$

where $\sigma$ is a measure-preserving map. For partitioned domains, **cost is lower-bounded by** $\text{(mass)} \times \text{(minimum distance to move within partition)}$, even when optimal transport requires moving only a fraction of the mass.

## Applications in Engineering

### 1. **Machine Learning & Generative Models**
- **Wasserstein GANs (WGAN):** Use $W_1$ as loss instead of KL/JS divergence for more stable training and meaningful gradients even when supports don't overlap
- **Distribution Matching:** Training neural networks to match generated distributions to real data
- **Domain Adaptation:** Measuring and minimizing domain shift between training and deployment

### 2. **Calibration & Prediction Quality**
- **Calibration Distance:** Measure discrepancy between predicted probabilities and true outcomes by computing optimal transport cost on 1D line (as in source material)
- **Lower bounds on sample complexity:** If predictions are separated and must be moved to calibrate, lower bounds derive from partitioning argument: cost $\sim \Omega(1/k)$ for $k$ predictions

### 3. **Computer Vision & Image