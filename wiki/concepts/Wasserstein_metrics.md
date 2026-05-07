# Wasserstein Metrics

## Definition

Wasserstein metrics (also called *optimal transport distances*) quantify the minimum "cost" required to transform one probability distribution into another. Formally, the **p-Wasserstein distance** between two probability measures $\mu$ and $\nu$ on a metric space $(\mathcal{X}, d)$ is:

$$W_p(\mu, \nu) := \left( \inf_{\gamma \in \Gamma(\mu,\nu)} \mathbb{E}_{(x,y)\sim\gamma}[d(x,y)^p] \right)^{1/p}$$

where:
- $\Gamma(\mu, \nu)$ is the set of all **couplings** (joint distributions) with marginals $\mu$ and $\nu$
- The infimum ranges over all possible ways to "match" samples from $\mu$ to samples from $\nu$
- The coupling that achieves the infimum is called the **optimal transport plan**

**Euclidean Wasserstein distance** (most common in machine learning):
$$W_2(\mu, \nu) = \left( \inf_{\gamma} \mathbb{E}_{(x,y)\sim\gamma}[\|x-y\|_2^2] \right)^{1/2}$$

This is also called the **Fréchet distance** for Gaussians.

## Key Equations

### Relationship to KL Divergence and Stronger Convergence

Unlike KL divergence $D_{KL}(\mu \| \nu)$, Wasserstein distances metrize weak convergence:

$$W_p(\mu, \nu) \text{ bounds convergence from below: } W_2(\mu, \nu)^2 \leq \sqrt{D_{KL}(\mu \| \nu)}$$

For Gaussian convergence, the Wasserstein distance scales more gracefully:
- **KL error** for DDPM: $D_{KL}(p_T \| q_T) \gtrsim \frac{d}{T^2}$ (dimension-dependent decay)
- **Wasserstein error** provides dimension-dependent lower bounds: $W_2(p_T, q_T) \gtrsim \sqrt{\frac{d}{T^2}}$

### Tensorization Property

For product distributions, **KL is additive** while Wasserstein scales differently:

$$D_{KL}(p^{\otimes d} \| q^{\otimes d}) = d \cdot D_{KL}(p \| q)$$

This asymmetry is critical: achieving $\varepsilon$-KL accuracy on a $d$-dimensional product requires $(\varepsilon/d)$-accuracy per marginal, creating potential for dimension-dependent lower bounds via tensorization.

### Query Complexity for Sampling

For strongly log-concave targets with condition number $\kappa$, first-order oracle access (gradient queries $\nabla V(x)$) requires:

$$\Omega\left(\min\left\{\sqrt{\kappa \log d}, d\right\}\right) \text{ queries}$$

to achieve constant Wasserstein distance accuracy.

## Physical Intuition / Derivation

### Why Wasserstein Over KL?

KL divergence can assign infinite cost to distributions with disjoint support, making it ill-suited for convergence analysis when distributions change qualitatively. Wasserstein distance is a **true metric**:
- Symmetry: $W_p(\mu,\nu) = W_p(\nu,\mu)$
- Triangle inequality holds
- $W_p(\mu,\nu) = 0 \iff \mu = \nu$

**Intuitive example**: If $\mu = \delta_0$ (point mass at origin) and $\nu = \delta_\epsilon$ (point mass at distance $\epsilon$), then:
- $D_{KL}(\mu \| \nu) = \infty$ (disjoint support)
- $W_2(\mu, \nu) = \epsilon$ (cost to slide mass distance $\epsilon$)

### Optimal Transport Plan Interpretation

The solution $\gamma^*$ to the Wasserstein minimization reveals the **optimal way to couple** $\mu$ to $\nu$. In 1D with monotone distributions, this is deterministic: sort both distributions and match quantiles. In higher dimensions, the structure becomes more complex but reveals intrinsic geometric relationships between distributions.

### Diffusion Models and Smoothing Scales

In diffusion-based sampling, querying the smoothed score $s_{\pi,\sigma} = \nabla \log(\pi * \mathcal{N}(0,\sigma^2 I))$ aggregates information over $O(\sigma)$ neighborhoods. This smoothing fundamentally changes the information-theoretic landscape compared to pointwise gradient queries—large $\sigma$ reveals global structure efficiently, while small $\sigma$ enables local refinement. The **bottleneck is identifying the informative smoothing scale**, not the raw query count.

## Applications in Engineering

### 1. Generative Modeling & Diffusion Models
- **Training objective**: Minimizing $W_2(p_{\text{data}}, p_\theta)$ is more stable than KL divergence for diffusion models
- **Score estimation**: Natural loss function for learning diffusion models in practice
- **Convergence analysis**: Wasserstein bounds directly relate to sampling quality without dimension-dependent blowup from KL

### 2. Optimal Transport & Logistics
- **Resource allocation**: Minimum cost to transport goods from supply nodes to demand nodes
- **Inventory management**: Wasserstein distance quantifies distribution mismatch between current and target inventory levels
- **Supply chain optimization**: Solves assignment problems via linear programming (monge-kantorovich formulation)

### 3. Machine Learning for Domain Adaptation
- **Distribution shift**: Measures discrepancy between source and target domains when $\kappa > 1$
- **Hypothesis transfer**: Bounds on generalization using Wasserstein rather than KL provide tighter guarantees under covariate shift

### 4. Statistical Testing
- **Two-sample testing**: Nonparametric test statistics based on empirical Wasserstein distance are consistent and computationally tractable
- **Good