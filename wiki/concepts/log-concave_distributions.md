# log-concave distributions

## Definition

A probability distribution $\pi(x)$ on $\mathbb{R}^d$ is **log-concave** if its density can be written as:
$$\pi(x) = e^{-V(x)}$$
where $V: \mathbb{R}^d \to \mathbb{R}$ is a **convex function** (the potential).

Equivalently, $\pi$ is log-concave if:
$$\log \pi(\lambda x + (1-\lambda)y) \geq \lambda \log \pi(x) + (1-\lambda) \log \pi(y)$$
for all $x, y \in \text{supp}(\pi)$ and $\lambda \in [0,1]$.

A distribution is **strongly log-concave** (with parameter $m > 0$) if $V$ is $m$-strongly convex, equivalently:
$$\nabla^2 V(x) \succeq m I$$

**Log-smooth** distributions satisfy $V$ being $L$-smooth (Lipschitz continuous gradient):
$$\|\nabla V(x) - \nabla V(y)\| \leq L\|x - y\|$$

## Key Equations

**Score function** (gradient of log-density):
$$s(x) := \nabla \log \pi(x) = -\nabla V(x)$$

**Smoothed score** (diffusion-style oracle access with noise level $\sigma$):
$$s_{\pi,\sigma}(x) := \nabla \log(\pi * \mathcal{N}(0, \sigma^2 I)) = \mathbb{E}_{z \sim \mathcal{N}(0,I)}[s(x + \sigma z)]$$

The smoothed score aggregates information from an $O(\sigma)$-radius neighborhood.

**KL divergence tensorization** for product targets:
$$D_{\text{KL}}(p^{\otimes d} \| q^{\otimes d}) = d \cdot D_{\text{KL}}(p \| q)$$

**Query complexity lower bounds** (strongly log-concave, smooth case):
$$\widetilde{\Omega}\left(\min\{\sqrt{\kappa \log d}, d\}\right)$$
where $\kappa$ is the condition number (ratio $L/m$).

**Non-log-concave worst-case complexity**: $\exp(\Omega(d))$ queries required.

## Physical Intuition / Derivation

### Why Log-Concavity Matters

Log-concave distributions are the "nicest" non-Gaussian distributions from an optimization and sampling perspective. The convexity of the potential $V$ means:
- The density has a unique global maximum (unimodal)
- The level sets $\{x: \pi(x) \geq t\}$ are convex
- Gradient-based methods work well (no local modes to trap samplers)

### The Geometry of Smoothing

When we query the **diffusion-smoothed score** $s_{\pi,\sigma}(x)$, we're not querying the true gradient $-\nabla V(x)$ directly. Instead, we obtain a local average:

$$s_{\pi,\sigma}(x) \approx -\nabla V(x) + O(\sigma^2 \nabla^2 V(x))$$

This creates a **scale-dependent exploration problem**:
- **Large $\sigma$**: Reveals coarse global structure, can rule out exponentially many candidate regions simultaneously
- **Small $\sigma$**: Refines local geometry but becomes expensive

The information-theoretic bottleneck shifts from "locating the mode among exponential noise" (classical oracle) to "choosing the right smoothing scale trajectory" (diffusion oracle).

### Condition Number Dependence

For a Gaussian with covariance $\Sigma = \text{diag}(\lambda_1, \ldots, \lambda_d)$ where $\lambda_1 \geq \cdots \geq \lambda_d$, the condition number $\kappa = \lambda_1/\lambda_d$ controls:
- How many steps are needed to couple the algorithm to the target distribution
- Block-Krylov methods achieve $\widetilde{O}(\sqrt{\kappa \log d})$ query complexity

## Applications in Engineering

### 1. **Sampling and Inference**
Log-concave distributions appear naturally in:
- **Bayesian statistics**: Posterior from log-concave prior + convex likelihood (linear regression, logistic regression)
- **Variational inference**: Fitting log-concave approximations to posterior distributions
- **Markov Chain Monte Carlo**: Analyzing convergence rates for LMC (Langevin Monte Carlo) on log-concave targets

### 2. **Diffusion Models and Generative AI**
- Diffusion samplers with learned score networks face fundamental lower bounds even for log-concave targets
- This establishes that $T = \Omega(\sqrt{d}/\varepsilon)$ diffusion steps are **necessary** to achieve $\varepsilon$-KL accuracy
- Informs design of continuous-time samplers and refinement strategies

### 3. **Optimization**
- **Convex optimization**: Log-concave densities enable efficient sampling-based optimization (e.g., hit-and-run samplers)
- **Dimension-dependent complexity**: Query lower bounds guide algorithm design for high-dimensional problems

### 4. **Product Distributions and Tensorization**
- Analyzing separable (product) targets $p^{\otimes d}$ via KL additivity
- Recent results show polylog$(1/\varepsilon)$ complexity in 1D rules out polynomial dimension-dependent barriers

## Common Mistakes / Pitfalls

### 1. **Confusing "log-concave" with "unimodal"**
Log-concavity implies unimodality, but not all unimodal distributions are log-concave. Many heavy-tailed distributions fail log-concavity.

### 2. **Assuming fast sampling for all log-concave targets**
While log-concavity enables polynomial algorithms, dimension-dependent lower bounds still apply: $\Omega(\sqrt{\