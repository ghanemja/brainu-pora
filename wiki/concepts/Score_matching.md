# Score Matching

## Definition

**Score matching** is a training objective for estimating the score function (gradient of log-probability) of a probability distribution. The score function is defined as:

$$s_\pi(x) = \nabla_x \log \pi(x)$$

In practice, we train a neural network $\hat{s}_\theta(x)$ to approximate the true score by minimizing the **score matching loss**:

$$\mathcal{L}_{\text{SM}}(\theta) = \mathbb{E}_{x \sim \pi}\left[\frac{1}{2}\|\hat{s}_\theta(x)\|_2^2 + \text{tr}\left(\nabla_x \hat{s}_\theta(x)\right)\right]$$

This objective avoids computing the partition function, making it practical for high-dimensional distributions where explicit density evaluation is intractable.

For noisy/smoothed distributions (common in diffusion models), the smoothed score is:

$$s_{\pi,\sigma}(x) = \nabla_x \log \pi_\sigma(x)$$

where $\pi_\sigma$ is the distribution $\pi$ convolved with Gaussian noise of variance $\sigma^2$.

## Key Equations

**Standard Score Matching Objective:**
$$\min_\theta \mathbb{E}_{x \sim \pi}\left[\frac{1}{2}\|\hat{s}_\theta(x)\|_2^2 + \text{tr}\left(\nabla_x \hat{s}_\theta(x)\right)\right]$$

**Denoising Score Matching** (preferred in practice):
$$\min_\theta \mathbb{E}_{\sigma, x \sim \pi, \epsilon \sim \mathcal{N}}\left[\|\hat{s}_\theta(x + \sigma\epsilon, \sigma) - (-\epsilon/\sigma)\|_2^2\right]$$

**$L^p$-Accuracy Assumption** (Assumption 2 from source):
$$\mathbb{E}_{X \sim \pi_\sigma}\left[\|\hat{s}_\sigma(X) - s_{\pi,\sigma}(X)\|_2^p\right] \leq \varepsilon_{\text{err}}^p \sigma^p$$

for some polynomial error bound $\varepsilon_{\text{err}} = 1/\text{poly}(d)$ and exponent $p \geq 2$.

**Query Complexity Bounds:**
- Upper bound (DDPM): $\tilde{O}(d)$ queries for TV error $\leq 0.01$
- Lower bound (general case): $\tilde{\Omega}(\sqrt{d})$ queries necessary
- With Lipschitz regularity ($L$-Lipschitz scores): $O(L\sqrt{d})$ queries achievable

## Physical Intuition / Derivation

### Why Score Matching?

The core challenge in generative modeling is sampling from a distribution $\pi(x)$ without explicit density access. Gradient-based sampling methods (e.g., Langevin dynamics, diffusion models) require the **score**—the direction and magnitude of steepest log-probability increase.

Direct score matching avoids computing $\nabla_x \log Z$ (the partition function gradient) by exploiting an integration-by-parts identity. Starting from the expected squared error:

$$\mathbb{E}_x\|\hat{s}(x) - \nabla_x \log \pi(x)\|_2^2$$

Integration by parts yields an equivalent objective requiring only the divergence of $\hat{s}$, not the intractable partition function.

### Why Smoothing?

In diffusion models, scores are estimated at multiple noise levels $\sigma$. Gaussian smoothing ensures:
1. **Regularity**: $\pi_\sigma$ is infinitely differentiable
2. **Stability**: Early-stopping and TV convergence guarantees become possible
3. **Physical alignment**: Matches actual noise injection during diffusion training

### Connection to Diffusion Models

Score matching is the **standard training objective** for diffusion models. A score network $\hat{s}_\theta(x, \sigma)$ trained via denoising score matching can then be integrated into reverse diffusion processes (DDPM, DDIM) to generate samples via iterative refinement.

## Applications in Engineering

### 1. **Generative Modeling** (Machine Learning)
- Core training method for diffusion models (image, audio, 3D generation)
- Enables unconditional and conditional generation without adversarial training
- More stable than GANs; better mode coverage than VAEs

### 2. **Physics-Informed Sampling**
- Sampling from Boltzmann distributions in molecular dynamics
- Posterior inference in inverse problems (e.g., medical imaging reconstruction)
- Energy-based model training without explicit normalization

### 3. **Uncertainty Quantification**
- Score-based methods for Bayesian inference
- Sampling from intractable posteriors in high-dimensional inference problems

### 4. **Controllable Generation**
- Conditional score matching enables guided generation
- Applications: text-to-image, inpainting, style transfer

## Common Mistakes / Pitfalls

### 1. **Confusing Score with Probability Gradient**
Score is $\nabla_x \log \pi(x)$, NOT $\nabla_x \pi(x)$. The log prevents collapse to maximum-likelihood point and provides numerical stability.

### 2. **Ignoring the Trace Term**
Students often drop the divergence term $\text{tr}(\nabla_x \hat{s})$ and only optimize $\|\hat{s}\|_2^2$. This is **incorrect**—the trace term is essential for consistency. Use denoising score matching in practice to avoid computing it explicitly.

### 3. **Misunderstanding Smoothing Scale $\sigma$**
The noise level $\sigma$ is **not arbitrary**. In diffusion theory:
- Small $\sigma$: score is sharp but harder to learn reliably
- Large $\sigma$: score is diffuse; easy to learn but covers less distribution mass
- Diffusion scheduling requires careful choice across the $\sigma$ spectrum

### 4. **Overlooking