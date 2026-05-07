# Score-Based Sampling

## Definition

**Score-based sampling** is a family of generative sampling algorithms that use learned or computed score functions to draw samples from a target probability distribution. The **score function** is the gradient of the log probability:

$$s(x) := \nabla \log \pi(x)$$

Score-based samplers iteratively refine samples by moving in directions of increasing probability (or equivalently, decreasing potential energy). The approach is typically implemented via diffusion processes, where samples are evolved through a reverse stochastic differential equation that requires score estimates at various noise levels.

A key variant is **diffusion-style access** to smoothed scores:

$$s_{\pi,\sigma}(x) := \nabla \log(\pi * \mathcal{N}(0, \sigma^2 I))$$

where the score is computed on a convolution of the target with a Gaussian kernel of standard deviation $\sigma$. This smoothing aggregates information from an $O(\sigma)$-neighborhood around $x$.

## Key Equations

**Score function definition:**
$$s(x) = \nabla \log \pi(x) = -\nabla V(x) \quad \text{(for } \pi(x) \propto e^{-V(x)}\text{)}$$

**Smoothed score (diffusion-style oracle):**
$$s_{\pi,\sigma}(x) = \nabla \log \int \pi(y) \mathcal{N}(x | y, \sigma^2 I) dy$$

**KL divergence scaling with DDPM discretization:**
$$\text{KL}(\text{terminal marginal}) \gtrsim \frac{d}{T^2}$$

where $d$ is dimension and $T$ is the number of steps, requiring $T = \Omega(\sqrt{d}/\varepsilon)$ steps for KL $\leq \varepsilon^2$ accuracy.

**Tensorization property (product targets):**
$$D_{\text{KL}}(p^{\otimes d} \| q^{\otimes d}) = d \cdot D_{\text{KL}}(p \| q)$$

Achieving $\varepsilon$-KL accuracy on the product requires $(\varepsilon/d)$-KL accuracy per marginal.

## Physical Intuition / Derivation

### Why Scores?

The score function $\nabla \log \pi(x)$ points toward regions of high probability. In Bayesian inference, this is proportional to $-\nabla V(x)$, a negative potential gradient—analogous to a force field pulling samples downhill in energy landscape.

### Diffusion-Based Interpretation

Score-based sampling emerges naturally from *reverse diffusion processes*. Forward diffusion gradually corrupts data with noise; the reverse process reconstructs samples by:
1. Starting from pure noise
2. At each step, using $s_{\pi,\sigma}(x)$ to drift toward the denoised distribution
3. Gradually decreasing noise level $\sigma$ to sharpen the result

The smoothing at scale $\sigma$ is not a limitation—it is a feature. Large $\sigma$ reveals global modes and rules out many candidate regions simultaneously, while small $\sigma$ refines local geometry. This multi-scale structure is far more efficient than pointwise potential queries.

### Oracle Model Distinctions

**First-order oracle (standard):** Access to $\nabla V(x)$ and $V(x)$ separately. For strongly log-concave targets, requires $\tilde{\Omega}(\sqrt{\kappa \log d})$ queries on Gaussians with condition number $\kappa$.

**Diffusion-style oracle (smoothed):** Access only to $s_{\pi,\sigma}(x)$ at user-chosen pairs $(x, \sigma)$. The bottleneck shifts: because smoothing aggregates neighborhoods, the critical challenge becomes *identifying an informative smoothing scale*. This changes the query complexity landscape substantially.

### Dimension Dependence

Lower bounds depend critically on target structure:
- **Gaussian targets** (log-concave): $\Omega(\sqrt{\kappa \log d})$ queries
- **General non-log-concave**: $\exp(\Omega(d))$ queries (probability mass hidden in exponentially many separated regions)

However, under diffusion-style access with polylog$(1/\varepsilon)$ scores (achievable in 1D), dimension-dependent polynomial lower bounds disappear—the smoothing fundamentally changes the query landscape.

## Applications in Engineering

### 1. **Generative AI & Deep Learning**
Score-based samplers power modern diffusion models used in image generation (Stable Diffusion, DALL-E 3), video synthesis, and molecular design. Networks learn the score function from data.

### 2. **Bayesian Inference & Posterior Sampling**
In inverse problems (medical imaging, subsurface characterization), score functions enable efficient sampling from high-dimensional posteriors without requiring explicit likelihood evaluations.

### 3. **Molecular Dynamics & Drug Discovery**
Score-based samplers explore conformational spaces and generate novel compounds by navigating energy landscapes defined via molecular potentials or learned neural networks.

### 4. **Uncertainty Quantification**
Engineering systems (structural mechanics, fluid dynamics) use diffusion-based sampling to propagate uncertainty through models and characterize failure regions in design spaces.

### 5. **Reinforcement Learning & Control**
Score-based methods guide policy sampling in exploration, enabling efficient navigation of high-dimensional action spaces with learned reward landscapes.

## Common Mistakes / Pitfalls

1. **Conflating score queries with potential queries:**  
   Querying $s_{\pi,\sigma}(x)$ is *not* equivalent to separately querying $V(x)$ and $\nabla V(x)$. The smoothing creates fundamental algorithmic advantages that generic first-order oracle lower bounds do not capture.

2. **Ignoring noise level as a design parameter:**  
   Naïve implementations use a fixed $\sigma$ schedule. Optimal performance requires adaptive or carefully tuned $\sigma(t)$ that transitions from coarse global structure to fine local detail. The bottleneck is often *scale selection*, not the number of score evaluations.

3. **Assuming dimension-independent complexity:**  
   Even with smoothed scores, dimension dependencies emerge for non-log-concave targets.