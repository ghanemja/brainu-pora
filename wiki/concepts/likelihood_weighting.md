# Likelihood Weighting

## Definition

**Likelihood weighting** is a Monte Carlo sampling technique used in probabilistic inference to estimate expectations under a target distribution when direct sampling is intractable. The method reweights samples drawn from a proposal (or simpler) distribution by the ratio of target to proposal likelihoods, allowing unbiased estimation of quantities under the target distribution.

In the context of the source material, likelihood weighting quantifies the relative influence of different regions of the posterior distribution. Specifically, when comparing two regions with different squared distances $r_-^2$ and $r_+^2$ from the center, the **likelihood weight ratio** determines how much the posterior mass concentrates in each region relative to its geometric volume.

## Key Equations

For sampling under a target distribution $\pi$ using proposal distribution $q$:

$$\mathbb{E}_{\pi}[f(X)] = \mathbb{E}_q\left[f(X) \cdot \frac{\pi(X)}{q(X)}\right]$$

where $\frac{\pi(X)}{q(X)}$ is the likelihood weight.

In the Gaussian setting with squared radii $r_\pm^2 = \tau^2 d \pm \Theta(\tau^2\sqrt{d})$, the **per-center likelihood weight ratio** is:

$$\frac{\exp(-r_-^2/(2\tau^2))}{\exp(-r_+^2/(2\tau^2))} = \exp\left(\frac{r_+^2 - r_-^2}{2\tau^2}\right) = \exp\left(\Theta(\sqrt{d})\right)$$

This exponential scaling in $\sqrt{d}$ creates a fundamental gap: while the Hamming shell surface areas differ by $\exp(\Theta(\sqrt{d}))$, the likelihood weights **exactly compensate** this difference by an equal exponential factor.

The number of distinct smoothing levels required to reliably hit an informative scale scales as:

$$\log_{\exp(\tilde{\Theta}(\sqrt{d}))}(\exp(\Theta(d))) = \tilde{\Theta}(\sqrt{d})$$

## Physical Intuition / Derivation

### The Core Compensation Phenomenon

Likelihood weighting reveals a subtle interplay between geometry and probability:

1. **Geometric volume** in $\mathbb{R}^d$: Hamming shells at different radii have surface areas that grow exponentially with dimension. Two shells at radii differing by $\Theta(\tau^2\sqrt{d})$ differ in volume by $\exp(\Theta(\sqrt{d}))$.

2. **Gaussian likelihood decay**: A Gaussian posterior $\pi_\sigma = \pi_{\text{pre}} * N(0, \gamma^2 I_d)$ assigns exponentially smaller likelihood to points farther from the center. For squared distances differing by $\Theta(\tau^2\sqrt{d})$, the likelihood ratio is $\exp(\Theta(\sqrt{d}))$.

3. **Exact cancellation**: These two effects—geometric amplification and likelihood attenuation—exactly cancel at leading order in $\sqrt{d}$. This creates an **informative window** problem: many different codebook sizes $n$ can produce indistinguishable observations because likelihood weighting compensates geometric effects.

### Why This Matters for Sampling

In high dimensions, if one naively sampled uniformly from a thin shell (constant volume), then reweighted by likelihood, the weights would be nearly constant—providing no information about which regions truly matter. The likelihood weighting ratio demonstrates this mathematically:

- Two regions appear equally plausible by surface area (both have $\exp(\Theta(\sqrt{d}))$ volume difference)
- But likelihood weights are also $\exp(\Theta(\sqrt{d}))$ different
- These effects **exactly offset**, requiring $\exp(\tilde{\Theta}(\sqrt{d}))$ many distinct scales to resolve

This exponential amplification of required query complexity is the source of the $\exp(\Omega(\sqrt{d}))$ lower bound.

## Applications in Engineering

### 1. **Bayesian Inference & Probabilistic Programming**
Likelihood weighting is foundational in particle filters and importance sampling for posterior inference when the prior is not conjugate to the likelihood. Engineering systems (control, robotics) use this for state estimation.

### 2. **Generative Modeling & Score-Based Diffusion**
The source material addresses score-based generative models where $s_{\pi,\sigma}(X) = \nabla \log \pi_\sigma(X)$ is the score function. Likelihood weighting determines the relative importance of different noise levels $\sigma$ in training; some noise scales contribute more effectively than others.

### 3. **Uncertainty Quantification**
In structural reliability and risk assessment, likelihood weighting is used in subset simulation and adaptive MCMC to estimate rare-event probabilities.

### 4. **Signal Processing & Detection**
Weighted maximum likelihood estimation uses likelihood ratios for signal detection under model uncertainty.

### 5. **Computational Chemistry & Molecular Simulation**
Sampling conformations of molecules under biased potentials uses likelihood reweighting to recover equilibrium ensemble properties.

## Common Mistakes / Pitfalls

### 1. **Forgetting Normalization**
Likelihood weights must sum to 1 for consistent probability estimation. Unnormalized weights lead to biased estimates:
$$\hat{\mu} = \frac{\sum_{i=1}^N w_i f(X_i)}{\sum_{i=1}^N w_i}, \quad w_i = \frac{\pi(X_i)}{q(X_i)}$$
Omitting the denominator gives incorrect results.

### 2. **Ignoring Weight Variance**
When some weights are exponentially larger than others (as in the $\exp(\Theta(\sqrt{d}))$ example), effective sample size collapses:
$$N_{\text{eff}} = \frac{(\sum_i w_i)^2}{\sum_i w_i^2} \ll N$$
High-dimensional problems often suffer catastrophic weight concentration, requiring adaptive resampling.

### 3. **Confusing Likelihood Ratio with Posterior Odds**
The likelihood weight $\pi(X)/q(X)$ is not the same as