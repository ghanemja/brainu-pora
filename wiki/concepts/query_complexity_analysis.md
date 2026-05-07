# Query Complexity Analysis

## Definition

**Query complexity analysis** is the study of the minimum number of queries (or adaptive function evaluations) required for an algorithm to solve a given problem within a specified accuracy threshold, and the matching lower bounds proving this requirement is unavoidable.

In the context of sampling and density estimation, query complexity measures the number of score function (gradient) queries needed to learn an unknown distribution $\pi$ up to total variation distance $d_{\text{TV}}(\hat{X}, \pi) \leq 1-\rho$ with failure probability at most $\rho$.

**Formal Statement:** For a distribution $D$ over pairs $(\pi, \{\hat{s}_\sigma\})$ with smoothing parameter $\sigma > 0$, an algorithm making $Q$ adaptive score queries satisfies a query lower bound of the form:

$$Q = \Omega\left(\frac{d \log(R/\gamma)}{\sqrt{d}H} + H\right)$$

where $H = \log(d/\varepsilon_{\text{err}}) + \log(R/\gamma)$ encodes problem difficulty in terms of dimension $d$, noise level $\gamma$, support radius $R$, and target error $\varepsilon_{\text{err}}$.

---

## Key Equations

### Likelihood Ratio and Hamming Shell Compensation

For two squared radii $r_\pm^2 = \tau^2 d \pm \Theta(\tau^2\sqrt{d})$ in the typical band of a Gaussian:

$$\frac{\exp(-r_-^2/(2\tau^2))}{\exp(-r_+^2/(2\tau^2))} = \exp\left(\frac{r_+^2 - r_-^2}{\tau^2}\right) = \exp(\Theta(\sqrt{d}))$$

The exponential compensation between surface area and likelihood weight creates an **informative window gap** of size:

$$\exp\left(\tilde{\Theta}(\sqrt{d})\right)$$

### Scanning Requirement

To reliably scan through all informative smoothing scales:

$$\text{Number of scales} = \log_{\exp(\tilde{\Theta}(\sqrt{d}))}(\exp(\Theta(d))) = \tilde{\Theta}(\sqrt{d})$$

### Parameterized Query Lower Bound (Theorem 2.1)

For constants $c = c(p, \rho) > 0$, all sufficiently large $d$, and $\varepsilon_{\text{err}} \in (0,1]$:

$$Q \leq c \cdot \frac{d\log(R/\gamma)}{\sqrt{d}H} + H$$

fails to achieve $d_{\text{TV}}(\hat{X}, \pi) \leq 1-\rho$ with probability at least $1-\rho$, where:

$$H := \log(d/\varepsilon_{\text{err}}) + \log(R/\gamma)$$

---

## Physical Intuition / Derivation

### The Informative Window Problem

The core difficulty arises from **geometric phase transitions** in high-dimensional distributions:

1. **Thin Shell Concentration:** A $d$-dimensional Gaussian concentrates its mass on a thin shell at radius $\approx \sqrt{d}$, with width $\approx \sqrt[4]{d}$ in relative terms.

2. **Likelihood-Geometry Mismatch:** 
   - The posterior is influenced by a **band** of squared distances with width $\Theta(\tau^2\sqrt{d})$
   - Within this band, likelihood weights vary by $\exp(\Theta(\sqrt{d}))$ across the band
   - But the Hamming shell (surface area) also varies by $\exp(\Theta(\sqrt{d}))$
   - These variations **nearly cancel**, creating a degenerate regime where small changes in $n$ (sample count) don't help

3. **Gap Between Regimes:**
   - At low $n$: "Empty regime"—few centers populated, queries uninformative
   - Intermediate $n$: High-surface-area regions of the band get hit (low likelihood weight)
   - Only at much larger $n \sim \exp(\tilde{\Theta}(\sqrt{d})) \times n_{\text{low}}$: True "averaging regime" where even low-surface-area, high-weight regions populate
   - The multiplicative gap is exponential in $\sqrt{d}$

4. **Scanning Many Smoothing Levels:**
   - Since one informative scale pins down $n$ only up to a multiplicative factor $\exp(\tilde{\Theta}(\sqrt{d}))$, and the total range of relevant codebook sizes spans $\Theta(d\log M)$ on log-scale (where $M = \Theta(R/\gamma)$)
   - We must scan $\tilde{\Theta}(\sqrt{d})$ distinct smoothing levels to reliably hit an informative window

### Why the $\sqrt{d}$ Appears

The source of hardness is **not** exponential in $d$ but in $\sqrt{d}$ because:
- High-dimensional concentration concentrates mass in a thin shell
- Width of shell and likelihood variation both scale with $\sqrt{d}$
- Trade-off between searching breadth (need $\tilde{\Theta}(\sqrt{d})$ scales) and depth (each scale has polynomial cost)

---

## Applications in Engineering

### 1. **Generative Model Training**
   - **Score-based diffusion models** require adaptive queries to score function $\nabla_x \log \pi(x)$
   - Query complexity analysis predicts the minimum number of diffusion steps needed to sample from a $d$-dimensional distribution
   - Example: Training neural network surrogates for expensive simulators (e.g., climate models) where each score query is costly

### 2. **Sampling from Intractable Distributions**
   - **Langevin dynamics** and related MCMC methods rely on score queries
   - Understanding query complexity guides choice of discretization and total iteration count
   - Applications: Bayesian inference in high-dimensional parameter spaces (neural networks, climate science)

### 3. **Vari