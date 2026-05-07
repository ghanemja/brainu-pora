# coreset construction

## Definition

A **coreset** is a small, weighted subset of a larger dataset that preserves the essential statistical properties of the original data with respect to a target objective function. Formally, for a dataset $X = \{x_1, \ldots, x_n\}$ and an objective function $f(w, X)$ parameterized by $w$, a coreset $C$ with weights $\{u_1, \ldots, u_m\}$ (where $m \ll n$) satisfies:

$$\left| f(w, X) - f(w, C) \right| \leq \varepsilon \cdot f(w, X)$$

with high probability for all (or all relevant) parameter vectors $w$. The subset is constructed via **importance sampling**, where points are retained based on their statistical importance to the model rather than uniformly at random.

The primary advantage is **data reduction**: replacing an $n$-point dataset with an $m$-point weighted coreset reduces computational complexity while maintaining statistical accuracy within multiplicative error bounds of $(1 \pm \varepsilon)$.

---

## Key Equations

### Multiplicative Error Bound (1-ε Approximation)

For a coreset $C$ with importance weights $u_i$, the objective function is approximated as:

$$(1 - \varepsilon) f(w, X) \leq f(w, C) \leq (1 + \varepsilon) f(w, X)$$

with high probability over randomization in coreset construction.

### Log-Likelihood Preservation (Semi-parametric Setting)

For likelihood-based models, the coreset preserves log-likelihood within:

$$\left| \ell(w; X) - \ell(w; C) \right| \leq \varepsilon \cdot |\ell(w; X)|$$

where $\ell(w; X) = \sum_{i=1}^n \log p(x_i | w)$ is the total log-likelihood.

### Importance Weight Assignment

Points are sampled with probability proportional to their sensitivity or leverage. For point $x_i$, the weight is typically:

$$u_i \propto \text{leverage}(x_i) \text{ or } \text{sensitivity}(x_i)$$

Points are included in $C$ if sampled; their weights are then adjusted to re-weight the remaining subset to approximate the full objective.

---

## Physical Intuition / Derivation

### Why Coresets Work: The Representativeness Principle

A dataset contains **redundancy**: many points contribute similarly to the objective function. A coreset identifies and retains the most **informative** points while upweighting them to compensate for removed points.

**Key insight**: Points near decision boundaries, outliers, or in low-density regions are typically more "informative" than points in high-density clusters, because they have higher **leverage** or **sensitivity** to parameter changes.

### Construction Strategy

1. **Identify importance**: Assign each point a score reflecting its influence on $f(w, X)$. In regression, this is typically leverage (diagonal of the hat matrix); in density estimation, it relates to sensitivity of the likelihood.

2. **Importance sampling**: Sample $m$ points with probability proportional to their importance score:
   $$\Pr[\text{include } x_i] = \min\left(1, \frac{c \cdot s_i}{\sum_j s_j}\right)$$
   where $s_i$ is the importance score and $c$ controls the expected coreset size.

3. **Re-weighting**: If point $x_i$ is included in $C$, assign it weight:
   $$u_i = \frac{\sum_j s_j}{c \cdot s_i}$$
   This re-weighting ensures $\sum_{i \in C} u_i \cdot \ell(w; x_i) \approx \sum_{j=1}^n \ell(w; x_j)$.

### Semi-parametric Extension (MCTMs)

For multivariate conditional transformation models, a geometric approximation based on the **convex hull** of input data addresses numerical instability in normalizing logarithmic terms:

- The convex hull provides a geometric bound on the support of the data
- This stabilizes computations when dealing with unbounded density estimates
- Ensures coresets remain feasible even with complex, high-dimensional distributions

---

## Applications in Engineering

### 1. **Large-Scale Machine Learning**
   - **Scalable distributed training**: Construct coresets on each machine, then combine coresets across nodes rather than transmitting full datasets.
   - **Streaming data**: Incrementally update coresets as new data arrives without reprocessing historical data.
   - **Cloud computing**: Reduce memory and bandwidth requirements for distributed optimization.

### 2. **Regression and Density Estimation**
   - **Non-parametric regression**: Accelerate kernel methods, spline fitting, and Gaussian process inference on massive datasets.
   - **Conditional density estimation**: Maintain statistical accuracy in semi-parametric distributional models while reducing computation from $O(n)$ to $O(m)$ where $m \ll n$.

### 3. **Real-time Anomaly Detection**
   - Construct lightweight coresets of historical data for baseline models.
   - Quickly evaluate new observations against the coreset rather than the full dataset.
   - Critical in network intrusion detection, sensor systems, and fault diagnosis.

### 4. **Geospatial and Climate Data**
   - Climate models with massive sensor networks: use coresets to represent spatial variability without processing every sensor.
   - Remote sensing: identify key pixels/regions (via leverage) that best represent image characteristics.

### 5. **Uncertainty Quantification**
   - In Bayesian inference on big data, coresets reduce MCMC burn-in and convergence time.
   - Posterior approximation remains accurate within $\varepsilon$ bounds.

---

## Common Mistakes / Pitfalls

### 1. **Confusing Coresets with Uniform Subsampling**
   - **Error**: Treating a randomly selected subset as a coreset without importance weighting.
   - **Reality**: Uniform subsampling loses tail behavior and rare events; coresets deliberately oversample high-leverage