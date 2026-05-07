# Rényi divergence

## Definition

The **Rényi divergence** of order $q$ (where $q > 0, q \neq 1$) is a family of divergences measuring the "distance" between two probability distributions. For probability measures $\mu$ and $\pi$ on a space with reference measure $\lambda$, the Rényi divergence of order $q$ is defined as:

$$R_q(\mu \| \pi) = \frac{1}{q-1} \log \mathbb{E}_{\pi}\left[\left(\frac{d\mu}{d\pi}\right)^q\right]$$

where $\frac{d\mu}{d\pi}$ is the Radon–Nikodym derivative (density ratio).

**Special cases:**
- As $q \to 1$: $R_q(\mu \| \pi) \to D_{\text{KL}}(\mu \| \pi)$ (Kullback–Leibler divergence)
- As $q \to \infty$: $R_q(\mu \| \pi) \to D_{\text{H}}(\mu \| \pi) = \log \sup_x \frac{d\mu}{d\pi}$ (Hellinger-like limit)
- $q = 2$: Chernoff information / chi-squared divergence scale

## Key Equations

**Chi-squared divergence** (related to $q=2$ case):
$$\chi^2(\mu \| \pi) = \mathbb{E}_{\pi}\left[\left(\frac{d\mu}{d\pi}\right)^2\right] - 1$$

**Relationship to acceptance probability preservation:**
If $R_q(\mu_0 \| \pi) \leq \varepsilon$ for $q > 1$, then the ratio of acceptance probabilities is multiplicatively controlled:
$$\frac{\mathbb{E}_{\mu_0}[\alpha(x)]}{\mathbb{E}_{\pi}[\alpha(x)]} \in [e^{-q\varepsilon/(q-1)}, e^{q\varepsilon/(q-1)}]$$

where $\alpha(x)$ is the Metropolis–Hastings acceptance probability.

## Physical Intuition / Derivation

### Why Rényi divergence for warm starting?

The critical insight is that **Rényi divergence controls the worst-case density ratio** between the initialization distribution $\mu_0$ and the target $\pi$:

$$R_q(\mu_0 \| \pi) \text{ small} \implies \text{no region of space where } \frac{d\mu_0}{d\pi} \text{ is exponentially small}$$

This is fundamentally different from other common metrics:

| Metric | Multiplicative Ratio Control | Pathology |
|--------|------------------------------|-----------|
| **Rényi ($q > 1$)** | ✓ Yes | None—controls density ratio uniformly |
| **Total Variation** | ✗ No | Can have $\pi$-typical regions with $\mu_0$-probability 0 |
| **Wasserstein** | ✗ No | Measures displacement, not density mismatch |
| **KL divergence** | ✗ No | Dominated by low-probability tail events |

### The acceptance probability bottleneck

In Metropolis-Hastings style samplers, the acceptance probability is:
$$\alpha(x \to y) = \min\left(1, \frac{\pi(y)}{\pi(x)}\right)$$

If $\mu_0$ initializes at a region where $\pi$ is exponentially unlikely (permitted by weak metrics), then:
- First proposal from $\mu_0$ generates $x$ with small $\pi(x)$
- Even if $y$ is sampled well, $\alpha(x \to y)$ is exponentially small in dimension $d$
- The Metropolis filter **throttles**, rejecting nearly all proposals

Rényi divergence prevents this: if $\chi^2(\mu_0 \| \pi) = O(1)$, then any region with substantial $\mu_0$-mass cannot be exponentially suppressed under $\pi$.

## Applications in Engineering

### 1. **Warm-start MCMC sampling**
In high-dimensional Bayesian inference, cold starts of Markov chain Monte Carlo (MHMC, MALA) suffer from low acceptance rates. Using Rényi divergence-based initialization criteria ensures:
- Non-negligible $\pi$-average acceptance probability when starting from $\mu_0$
- Enables $d^{1/4}$ (instead of $d^{1/2}$) query complexity for high-accuracy log-concave sampling
- Critical for variational inference warm starts and tempering schedules

### 2. **Importance sampling diagnostics**
Rényi divergence bounds the variance of importance sampling estimates:
$$\text{Var}_\pi(\hat{Z}) \lesssim e^{2R_2(\mu \| \pi)} - 1$$
Used to certify when proposal distributions $\mu$ are suitable for unbiased estimation.

### 3. **Information-theoretic rate analysis**
In adaptive sampling and optimal experimental design, Rényi divergence characterizes:
- Optimal information gain in parameter estimation
- Concentration properties of empirical distributions
- Distinguishability between competing hypotheses

### 4. **Machine learning generalization bounds**
Order-$q$ Rényi divergence appears in PAC-Bayes bounds and differential privacy analyses, controlling generalization error without requiring bounded loss.

## Common Mistakes / Pitfalls

1. **Conflating $q=1$ limit with KL divergence**
   - The limit $\lim_{q \to 1} R_q(\mu \| \pi) = D_{\text{KL}}(\mu \| \pi)$ requires careful analysis
   - For finite $q > 1$, behavior is qualitatively different: Rényi divergence $\ll$ KL for distributions with heavy tails

2. **Assuming all Rényi orders are equivalent**
   - Different $q$ values control different reg