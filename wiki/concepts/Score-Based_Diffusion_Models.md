# Score-Based Diffusion Models

## Definition

Score-based diffusion models are a class of generative models that learn to sample from a target distribution $p_0(\mathbf{x})$ by reversing a carefully designed noise diffusion process. The key innovation is learning the **score function** $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ (the gradient of the log-density) at each timestep $t \in [0, T]$, which enables sampling via a reverse diffusion process.

Formally, a score-based diffusion model operates via:
1. **Forward process**: Gradually add noise to data, transforming $p_0$ into a tractable distribution (typically standard Gaussian)
2. **Score learning**: Train a neural network $s_\theta(\mathbf{x}, t)$ to estimate $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ at each time $t$
3. **Reverse sampling**: Use the learned score to generate new samples by reversing the noise injection

## Key Equations

### Forward Diffusion Process (Variance Exploding SDE)

The forward process is typically formulated as a stochastic differential equation (SDE):

$$d\mathbf{x} = \mathbf{f}(\mathbf{x}, t) dt + g(t) d\mathbf{w}$$

where $\mathbf{f}(\mathbf{x}, t)$ is the drift term, $g(t)$ is the diffusion coefficient, and $\mathbf{w}$ is a Wiener process.

For the common **variance-exploding** formulation:

$$d\mathbf{x} = \sqrt{\frac{d\sigma^2}{dt}} d\mathbf{w}$$

with $\sigma(t)$ monotonically increasing from 0 to large values, so $p_T(\mathbf{x}) \approx \mathcal{N}(0, \sigma_T^2 I)$.

### Reverse Process (Score-Based Sampling)

The reverse SDE is given by:

$$d\mathbf{x} = -\frac{g(t)^2}{2} \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) dt + g(t) d\bar{\mathbf{w}}$$

where $d\bar{\mathbf{w}}$ is the reverse-time Wiener process.

In practice, we substitute the learned score function $s_\theta(\mathbf{x}, t) \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x})$:

$$d\mathbf{x} = -\frac{g(t)^2}{2} s_\theta(\mathbf{x}, t) dt + g(t) d\bar{\mathbf{w}}$$

### Score Matching Loss

The score function is learned via **denoising score matching**:

$$\mathcal{L}(\theta) = \mathbb{E}_{t, \mathbf{x}_0 \sim p_0, \boldsymbol{\epsilon} \sim \mathcal{N}(0, I)} \left[ \left\| s_\theta(\mathbf{x}_t, t) - \nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t | \mathbf{x}_0) \right\|_2^2 \right]$$

where $\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \boldsymbol{\epsilon}$ with scaling coefficients $\alpha_t$ and $\sigma_t$ determined by the noise schedule.

### Simplified Form (Denoising Perspective)

Many implementations use the equivalent formulation where the network predicts the noise directly:

$$\mathcal{L}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}} \left[ \left\| \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t) - \boldsymbol{\epsilon} \right\|_2^2 \right]$$

The connection to the score is: $s_\theta(\mathbf{x}_t, t) = -\frac{\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)}{\sigma_t}$

## Physical Intuition / Derivation

### Why Reverse a Diffusion Process?

The core insight is that if we can learn to reverse noise injection, we can generate samples from complex distributions by starting from simple Gaussian noise.

**Forward intuition**: Diffusing data (adding noise) transforms any distribution into a standard Gaussian—a process we understand well. The challenge is reversing this process.

**Reverse intuition**: By Fokker-Planck theory, the reverse-time SDE perfectly undoes the forward process *if we know the true score function* $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$. This score tells us the direction of highest probability density at each point and time.

### Score Function as a Probability Gradient

The score $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ has a geometric interpretation:
- It points in the direction of steepest increase in log-probability
- In high-density regions, the score magnitude is large (strong signal about where to go)
- In low-density regions, the score is weaker (less certain)

This is why the reverse process naturally follows the score: it's an optimal direction to escape noise and approach high-probability regions of the data distribution.

### From Variational Lower Bound to Score Matching

Score-based models can be derived from variational bounds on the likelihood, but more directly, **denoising score matching** leverages:

1. The perturbed distribution $p_t(\mathbf{x}_t | \mathbf{x}_0) = \mathcal{N}(\alpha_t \mathbf{x}_0, \sigma_t^2 I)$ has a known