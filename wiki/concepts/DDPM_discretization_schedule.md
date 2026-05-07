# DDPM Discretization Schedule

## Definition

The DDPM (Denoising Diffusion Probabilistic Models) discretization schedule specifies how noise is injected into data during the forward diffusion process, and consequently how many steps $T$ are required in the reverse process to achieve a target accuracy. It defines the variance schedule $\{\beta_t\}_{t=1}^T$ that governs the rate of noise addition at each timestep.

**Formally**, the forward process is:
$$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t I)$$

The discretization schedule determines the sequence $\{\beta_1, \beta_2, \ldots, \beta_T\}$, which collectively control:
- How quickly information about the data distribution is lost
- The signal-to-noise ratio at each reverse step
- The total computational cost (proportional to $T$)

## Key Equations

Under a **standard DDPM discretization schedule**, the KL divergence error of the terminal marginal (comparing reverse process to target) satisfies:

$$\text{KL}(q(x_T) \| p(x_T)) \gtrsim \frac{d}{T^2}$$

where $d$ is the dimension of the data.

This implies that to achieve **KL divergence $\leq \varepsilon^2$**, one requires:

$$T = \Omega\left(\sqrt{\frac{d}{\varepsilon}}\right) \text{ steps}$$

### Tensorization and Product Targets

For product targets $p^{\otimes d}$, KL divergence is additive:
$$D_{\text{KL}}(p^{\otimes d} \| q^{\otimes d}) = d \cdot D_{\text{KL}}(p \| q)$$

This means achieving $\varepsilon$-KL accuracy on the full product distribution requires $(\varepsilon/d)$-KL accuracy on each marginal, creating a dimension-dependent amplification.

## Physical Intuition / Derivation

### Why Discretization Matters

The DDPM schedule is fundamentally about **pacing information recovery**. Consider the reverse process: at each step $t \to t-1$, we denoise by removing noise added during the forward pass. The schedule controls the *difficulty* of this denoising:

- **Large $\beta_t$**: Aggressive noise injection → harder denoising → requires better score function estimates
- **Small $\beta_t$**: Conservative noise injection → easier denoising → but requires more steps to remove all noise

### The Discretization Error Barrier

The $T^{-2}$ scaling arises from a fundamental accuracy bottleneck: even with **exact scores** $s(x_t) = \nabla_x \log p_t(x)$ and a simple Gaussian target, the discrete timesteps introduce irremovable error. This is not due to score estimation error but to the *discrete approximation* itself.

Intuitively: each reverse step must traverse a "gap" determined by $\beta_t$. With $T$ steps and $\beta_t$ roughly constant, the gap per step is $O(1/T)$, and accumulated discretization error scales as $O(d/T^2)$ in high dimensions.

### Smoothing and Information Aggregation

In practice, learned score networks are queried with noisy inputs at chosen noise levels $\sigma$. The key insight is that:

$$s_{\pi,\sigma}(x) = \nabla \log(\pi * \mathcal{N}(0, \sigma^2 I))$$

aggregates information from an $O(\sigma)$ neighborhood. **Large $\sigma$ reveals coarse global structure** (ruling out many modal regions simultaneously), while **small $\sigma$ refines local details**. The bottleneck for practical algorithms is identifying the informative smoothing scale.

## Applications in Engineering

### 1. **Generative Modeling**
DDPM discretization schedules are critical for training diffusion models in:
- Image generation (e.g., text-to-image synthesis)
- 3D shape generation
- Molecular design

The schedule determines training stability and inference speed. Standard linear or cosine schedules balance computational cost against generation quality.

### 2. **Inverse Problems & Uncertainty Quantification**
In engineering applications (e.g., inverse problems in geophysics, medical imaging), diffusion-based samplers use DDPM schedules to:
- Recover uncertainty estimates alongside point estimates
- Maintain computational feasibility for high-dimensional problems
- Leverage dimension-dependent scaling knowledge to allocate compute

### 3. **Sampling from Log-Concave Distributions**
For Gaussian targets with condition number $\kappa$, known lower bounds show:
$$\widetilde{\Omega}(\min\{\sqrt{\kappa \log d}, d\}) \text{ queries required}$$

This guides algorithm selection: block-Krylov methods asymptotically match these bounds.

### 4. **Score-Based Generative Models in Control**
In offline reinforcement learning and robotics, score-based samplers with DDPM schedules are used to generate action sequences. The discretization schedule affects:
- Sample quality for planning
- Real-time feasibility constraints
- Convergence of policy learning

## Common Mistakes / Pitfalls

### 1. **Confusing Discretization Error with Score Estimation Error**
Students often assume that exact scores eliminate all error. **Reality**: Under standard DDPM schedules, even exact scores yield $\text{KL} \gtrsim d/T^2$. This is a fundamental discretization barrier, not a limitation of learned approximations.

### 2. **Ignoring Dimension-Dependence**
The $T = \Omega(\sqrt{d/\varepsilon})$ scaling is often overlooked in 2D toy problems. **In high dimensions** (e.g., $d=10^4$ for images), this becomes the dominant computational cost.

### 3. **Assuming Linear Schedules are Optimal**
Standard linear variance schedules $\beta_t = \text{const}$ are convenient but not universally optimal. Problem-specific schedules (e.g., based on condition number) can significantly reduce $