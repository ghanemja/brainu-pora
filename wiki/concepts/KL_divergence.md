# KL Divergence

## Definition

The **Kullback-Leibler (KL) divergence**, also called relative entropy, is a non-symmetric measure of how one probability distribution differs from a reference distribution. It quantifies the information loss when using one distribution to approximate another.

Formally, for two probability distributions $p$ and $q$ over the same sample space:

$$D_{KL}(p \| q) = \int p(x) \log \frac{p(x)}{q(x)} dx$$

for continuous distributions, or equivalently in discrete form:

$$D_{KL}(p \| q) = \sum_x p(x) \log \frac{p(x)}{q(x)}$$

**Key properties:**
- $D_{KL}(p \| q) \geq 0$ always, with equality if and only if $p = q$ almost everywhere
- **Asymmetric**: $D_{KL}(p \| q) \neq D_{KL}(q \| p)$ in general
- Measured in nats (natural logarithm) or bits (logarithm base 2)
- Not a true distance metric (violates symmetry and triangle inequality)

## Key Equations

**Basic definition:**
$$D_{KL}(p \| q) = \mathbb{E}_{x \sim p}\left[\log \frac{p(x)}{q(x)}\right] = \mathbb{E}_{x \sim p}[\log p(x)] - \mathbb{E}_{x \sim p}[\log q(x)]$$

**For Gaussian distributions** $p = \mathcal{N}(\mu_p, \Sigma_p)$ and $q = \mathcal{N}(\mu_q, \Sigma_q)$:

$$D_{KL}(p \| q) = \frac{1}{2}\left[\text{tr}(\Sigma_q^{-1}\Sigma_p) + (\mu_q - \mu_p)^T\Sigma_q^{-1}(\mu_q - \mu_p) - d + \log\frac{\det \Sigma_q}{\det \Sigma_p}\right]$$

**Additivity for product distributions** (critical for dimension scaling):
$$D_{KL}(p^{\otimes d} \| q^{\otimes d}) = d \cdot D_{KL}(p \| q)$$

This shows that achieving $\varepsilon$-KL accuracy on a $d$-dimensional product target requires $(\varepsilon/d)$-KL accuracy on each marginal—a fundamental scaling barrier.

**Reverse KL (mode-seeking) vs. Forward KL (mean-seeking):**
- $D_{KL}(p \| q)$ penalizes $q$ placing mass where $p$ has none (forward KL; zero-forcing)
- $D_{KL}(q \| p)$ penalizes $p$ placing mass where $q$ has none (reverse KL; mode-seeking)

## Physical Intuition / Derivation

### Information-Theoretic Perspective

KL divergence emerges naturally from information theory. If we encode samples from the true distribution $p$ using an optimal code for distribution $q$, the expected extra bits required per sample is $D_{KL}(p \| q)$. Thus it measures the "surprise" of the true data under the wrong model.

### Derivation from Maximum Likelihood

When fitting a model $q_\theta$ to true distribution $p$, maximum likelihood estimation minimizes:

$$\mathcal{L}(\theta) = -\mathbb{E}_{x \sim p}[\log q_\theta(x)]$$

This is equivalent to minimizing $D_{KL}(p \| q_\theta)$ up to a constant (the entropy of $p$), which is why KL divergence is fundamental to machine learning.

### Why Asymmetry Matters

The asymmetry reflects different failure modes:
- **Forward KL** $D_{KL}(p \| q)$: Requires $q$ to cover all modes of $p$ (inclusive, zero-forcing). Used when $p$ is the ground truth.
- **Reverse KL** $D_{KL}(q \| p)$: Tolerates missing modes; focuses on explaining the modes of $p$ well (exclusive, mode-seeking). Used in variational inference.

### Dimension Dependence

From the product rule, a $d$-dimensional problem scales as $d \cdot D_{KL}(\text{marginal})$. This creates a fundamental bottleneck: as dimension grows, matching quality must improve quadratically (e.g., for diffusion models with $T$ steps, $KL \gtrsim d/T^2$, requiring $T = \Omega(\sqrt{d/\varepsilon})$ steps).

## Applications in Engineering

### 1. **Generative Modeling & Diffusion Models**
- Measures the gap between learned score functions and true data distribution
- Governs convergence rates: terminal marginal KL under DDPM satisfies $KL \gtrsim d/T^2$
- Determines number of sampling steps needed: $T = \Omega(\sqrt{d/\varepsilon})$ for accuracy $\varepsilon^2$

### 2. **Variational Inference**
- Core objective in variational autoencoders (VAEs): $\mathcal{L} = -\mathbb{E}_q[\log p(x|z)] + D_{KL}(q(z|x) \| p(z))$
- The KL term acts as a regularizer, pushing the learned posterior toward the prior
- Reverse KL naturally encourages posterior collapse in high dimensions

### 3. **Information Bottleneck & Compression**
- Data compression: $D_{KL}(p \| q)$ bounds the minimum bits needed to encode samples from $p$ using code optimized for $q$
- Rate-distortion theory: trade-off between compression and reconstruction fidelity

### 4. **Optimal Transport & Sampling**
- Basis for query complexity lower bounds in sampling algorithms
- Smoothed score access (via diffusion oracle $s_{\pi,