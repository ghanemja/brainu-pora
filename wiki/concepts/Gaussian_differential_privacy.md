# Gaussian Differential Privacy

## Definition

**Gaussian Differential Privacy (GDP)** is a relaxation and refinement of classical differential privacy that quantifies privacy loss through the lens of Gaussian distributions rather than worst-case bounds. It provides tighter, more composable privacy guarantees for algorithms that add Gaussian noise.

Formally, a randomized algorithm $\mathcal{M}$ satisfies **$\mu$-Gaussian Differential Privacy** if for all neighboring datasets $D$ and $D'$ (differing in one record), the hypothesis test between $\mathcal{M}(D)$ and $\mathcal{M}(D')$ can be characterized by a Gaussian random variable with mean $\mu$ and unit variance. This means the log-likelihood ratio between the two output distributions is approximately Gaussian-distributed.

More precisely: the KL divergence between the output distributions is bounded by $\frac{\mu^2}{2}$, and crucially, the **Rényi divergence of order 2** (denoted $D_2$) characterizes the privacy profile:

$$D_2(\mathcal{M}(D) \| \mathcal{M}(D')) = \mu^2$$

## Key Equations

### Privacy Parameter Relationship
For an algorithm adding Gaussian noise $\mathcal{N}(0, \sigma^2)$ to a function $f$ with $\ell_2$-sensitivity $\Delta_2$:

$$\mu = \frac{\Delta_2}{\sigma}$$

The algorithm satisfies $\mu$-GDP.

### Composition Law (Key Advantage)
When composing $k$ independent mechanisms with parameters $\mu_1, \mu_2, \ldots, \mu_k$, the combined mechanism satisfies:

$$\mu_{\text{composed}}^2 = \sum_{i=1}^{k} \mu_i^2$$

This is fundamentally different from classical composition, which scales linearly in $k$.

### Conversion to $(\epsilon, \delta)$-DP
A $\mu$-GDP mechanism can be converted to $(\epsilon, \delta)$-differential privacy with:

$$\epsilon = \mu\sqrt{2\ln(1/\delta)} + \mu^2 \ln(1/\delta)$$

or approximately, for small $\delta$:

$$\epsilon \approx \mu\sqrt{2\ln(1/\delta)}$$

### Rényi Divergence Formulation
For Gaussian mechanisms, the Rényi divergence of order $\alpha$ is:

$$D_\alpha(\mathcal{M}(D) \| \mathcal{M}(D')) = \frac{\alpha \mu^2}{2(\alpha-1)}$$

which converges to $\frac{\mu^2}{2}$ (KL divergence) as $\alpha \to 1$.

## Physical Intuition / Derivation

### Why Gaussian?

Classical differential privacy bounds the worst-case output likelihood ratio between neighboring datasets. This is extremely conservative for Gaussian mechanisms—most instances are far from the worst case.

GDP exploits the fact that when you add Gaussian noise, the *distribution* of privacy losses (log-likelihood ratios) is itself approximately Gaussian. Rather than bounding the worst case, GDP characterizes the typical behavior.

### Composition Advantage

Imagine running $k$ algorithms sequentially, each with classical privacy budget $\epsilon$. Classical composition (via union bound) gives total budget $k\epsilon$—linear scaling, which becomes prohibitive.

With GDP, each mechanism contributes $\mu_i^2$ to the squared privacy parameter. Since they compose via **quadratic sum**:

$$\mu_{\text{total}}^2 = \sum_{i=1}^{k} \mu_i^2 \sim \sqrt{k} \cdot \mu_{\text{single}}$$

This improves to **square-root scaling** in the number of queries—a dramatic improvement for high-dimensional problems or many-query settings.

### Derivation Sketch

For a query $f: \mathcal{X}^n \to \mathbb{R}$ with $\ell_2$-sensitivity $\Delta_2$ and Gaussian noise $\mathcal{N}(0, \sigma^2)$:

1. The log-likelihood ratio is:
$$\ln\frac{p_D(y)}{p_{D'}(y)} = \frac{2(f(D) - f(D')) \cdot y - (f(D)^2 - f(D')^2)}{2\sigma^2}$$

2. This is a linear functional of $y \sim \mathcal{N}(0, \sigma^2 I)$, so its distribution is Gaussian with:
   - Mean: $\frac{f(D) - f(D')}{\sigma^2} \cdot \frac{f(D) - f(D')}{2} = O\left(\frac{\Delta_2^2}{\sigma^2}\right)$
   - Variance: $O(1)$ (normalized by careful scaling)

3. Setting $\mu = \Delta_2/\sigma$ gives the Gaussian parameter.

## Applications in Engineering

### Machine Learning and Statistics

- **Differentially Private Machine Learning**: GDP improves privacy guarantees for iterative algorithms (SGD, EM) where multiple gradient updates must be protected. Square-root composition enables feasible privacy-utility tradeoffs.

- **Federated Learning**: When aggregating updates from many clients, GDP's composition law reduces privacy budget waste from naive union bounds, allowing more client participation.

- **Synthetic Data Generation**: GDP-based mechanisms can generate realistic synthetic datasets with formal privacy guarantees, useful in healthcare and finance where sharing raw data is infeasible.

### Systems and Data Analysis

- **Database Query Systems**: PINQ and similar systems use GDP to handle many ad-hoc queries. Better composition bounds mean users can ask more questions before privacy is exhausted.

- **Time Series Analysis**: Releasing sequential statistics (e.g., daily aggregate counts) with GDP protection scales much better than classical DP over many time steps.

- **Replicability Engineering**: Recent work (see [[Replicability in Learning]]) uses GDP as a foundation to ensure that ML systems produce consistent outputs across repeated independent runs—critical for reproducible scientific