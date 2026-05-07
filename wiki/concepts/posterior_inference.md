# Posterior Inference

## Definition

**Posterior inference** is the computational problem of learning a latent distribution or model parameters from noisy observations, using a score-based oracle that provides gradient estimates of the log-density. Formally, given:
- A latent distribution $\pi$ over $\mathbb{R}^d$ (supported on $[-R, R]^d$)
- Noisy observations $X \sim \pi_\sigma = \pi * \mathcal{N}(0, \gamma^2 I_d)$ (signal convolved with noise)
- Access to an $L_p$-accurate score oracle $\hat{s}_\sigma(x)$ approximating $\nabla \log \pi_\sigma(x)$

The goal is to reconstruct or sample from $\pi$ using adaptive queries to $\hat{s}_\sigma$ at different noise levels $\sigma > 0$.

The key challenge: **posterior inference requires scanning through an exponentially large range of noise scales** to find informative regimes where the data provides meaningful signal about the latent structure.

---

## Key Equations

**Posterior distribution at noise level $\sigma$:**
$$\pi_\sigma(x) = (\pi * \mathcal{N}(0, \gamma^2 I_d))(x)$$

**Score function (gradient of log-density):**
$$s_{\pi,\sigma}(x) = \nabla \log \pi_\sigma(x)$$

**Oracle approximation error (Lp norm):**
$$\mathbb{E}_{X \sim \pi_\sigma}\left[\|\hat{s}_\sigma(X) - s_{\pi,\sigma}(X)\|_p^2\right] \leq \varepsilon_p \sigma^p$$

**Lipschitz constant of score function:**
$$L_\sigma \leq \frac{3}{\gamma^2 + \sigma^2} + \frac{7R^2d}{(\gamma^2 + \sigma^2)^2}$$

**Query lower bound:**
For any algorithm making at most $Q$ adaptive score queries:
$$Q \lesssim \frac{c \cdot d \log(R/\gamma)}{\sqrt{d}} \cdot H + H$$
where $H = \log(d/\varepsilon_{\text{err}}) + \log(R/\gamma)$

This yields a lower bound of $\widetilde{\Omega}(\exp(\sqrt{d}))$ query complexity in the worst case.

---

## Physical Intuition / Derivation

### The Informative Window Problem

The core difficulty in posterior inference stems from a **mismatch between likelihood and geometry** at different noise scales.

**At a fixed noise level $\sigma$:**
1. The posterior mass concentrates on a thin "band" of squared distances: $\|Z\|_2^2 = \sigma^2 d \pm \tilde{O}(\sigma^2\sqrt{d})$ (with probability $1 - 1/\text{poly}(d)$)
2. Within this band, the likelihood weights vary exponentially:
$$\frac{\exp(-r_-^2/(2\sigma^2))}{\exp(-r_+^2/(2\sigma^2))} = \exp\left(\Theta(\sqrt{d})\right)$$
3. But the Hamming shell volumes *also* vary by $\exp(\Theta(\sqrt{d}))$ in opposite direction

This **compensation** creates a gap: the high-surface-area parts of the band become "empty" before the true high-weight regions become populated. The effective informative window spans a multiplicative range of $\exp(\tilde{\Theta}(\sqrt{d}))$ in the hidden parameter space.

### Scanning Across Scales

Because each query at a single noise level $\sigma$ only rules out a $\text{poly}(d)$ range of the parameter space, and there are $\Theta(d/\log d)$ such non-overlapping ranges, we must query:
$$\sqrt{d \log(R/\gamma)}$$
distinct smoothing levels to reliably hit an informative scale.

In the worst case, with high-dimensional structure and bounded noise $\gamma$, this can blow up to $\exp(\tilde{\Theta}(\sqrt{d}))$ levels.

---

## Applications in Engineering

### 1. **Score-Based Generative Modeling**
- Denoising diffusion models use score oracles $\hat{s}_\sigma$ to iteratively refine samples
- Posterior inference analysis bounds the number of diffusion timesteps needed for high-fidelity generation
- Critical for computing minimum query budgets in neural score networks

### 2. **Bayesian Inverse Problems**
- Reconstructing physical parameters (e.g., material properties, system state) from noisy measurements
- The posterior inference framework quantifies how many forward simulations (queries) are needed to achieve target reconstruction error
- Example: seismic imaging, where signal attenuation ($\gamma$) and dimensionality ($d$) directly impact computational cost

### 3. **Variational Inference & MCMC Tuning**
- Posterior inference theory guides the design of tempering schedules (varying $\sigma$) in annealed importance sampling
- Predicts when temperature schedules become inefficient (requiring exponential number of intermediate levels)

### 4. **Machine Learning Robustness**
- Understanding how model dimensionality and noise tolerance interact during training
- Bounds on the number of stochastic gradient steps needed for convergence in high-dimensional settings

### 5. **Signal Processing Under Uncertainty**
- Deconvolution with unknown noise structure: posterior inference lower bounds apply when noise characteristics are hidden
- Optimal filter design: the $L_\sigma$-Lipschitz constraint bounds the bandwidth of effective filters at scale $\sigma$

---

## Common Mistakes / Pitfalls

### 1. **Assuming Uniform Exponential Gains Across Scales**
**Mistake:** Treating posterior inference as simply "exponentially many scales needed" without accounting for problem structure.
**Reality:** The bound depends critically on $\log(R/\gamma)$ (the logarithmic "diameter" in parameter space) and interaction dimension via $\sqrt{d}$.