# Spiked covariance model

## Definition

The **spiked covariance model** is a statistical framework for detecting weak signals embedded in high-dimensional noise. It describes a data distribution where:

- **Null model**: Data is drawn from a standard Gaussian with identity covariance: $\mathbf{X} \sim \mathcal{N}(0, \mathbf{I}_d)$
- **Planted model**: Data is drawn from a Gaussian with a low-rank "spike" added to the covariance: $\mathbf{X} \sim \mathcal{N}(0, \mathbf{I}_d + \beta \mathbf{v}\mathbf{v}^T)$

where $\beta > 0$ is the signal strength and $\mathbf{v} \in \mathbb{R}^d$ is a unit-norm signal vector (often unknown).

The central challenge is to **distinguish** between these two distributions given $n$ samples, with constraints on computational resources such as memory in streaming settings.

## Key Equations

**Planted covariance matrix:**
$$\boldsymbol{\Sigma}_{\text{planted}} = \mathbf{I}_d + \beta \mathbf{v}\mathbf{v}^T$$

**Sample covariance (empirical):**
$$\hat{\boldsymbol{\Sigma}} = \frac{1}{n}\sum_{i=1}^{n} \mathbf{x}_i \mathbf{x}_i^T$$

**Likelihood ratio (null vs. planted):**
$$\Lambda = \frac{p_{\text{planted}}(\mathbf{X})}{p_{\text{null}}(\mathbf{X})} \approx \exp\left(\frac{\beta n}{2}\mathbf{v}^T\hat{\boldsymbol{\Sigma}}\mathbf{v} - \frac{\beta n}{4}(1+\beta)\right)$$

For detection with $n$ samples, the signal-to-noise ratio is characterized by:
$$\text{SNR} = \beta \sqrt{n}$$

**Memory-sample tradeoff (sparse PCA regime):**
For detecting a $k$-sparse spike in dimension $d$ with $n$ samples, memory lower bounds scale as:
$$M \geq \Omega\left(\frac{k \log(d/k)}{c}\right)$$
where $c$ is the number of passes over the data.

## Physical Intuition / Derivation

### The Signal Detection Problem

Imagine observing $n$ high-dimensional data points in $\mathbb{R}^d$. Under the null hypothesis, all variance is isotropic (uniform in all directions). Under the planted hypothesis, there is one special direction $\mathbf{v}$ where variance is amplified by an amount $\beta$.

The **sample covariance** $\hat{\boldsymbol{\Sigma}}$ should have:
- Eigenvalues near 1 in all directions under null
- One eigenvalue near $1 + \beta$ in direction $\mathbf{v}$ under planted model

### Why This Matters Computationally

**Information-theoretic threshold:** With unlimited computation, detection is possible when $\beta \sqrt{n}$ is large enough (roughly $\beta \sqrt{n} \gtrsim 1$).

**Computational threshold:** With polynomial time/memory constraints, detection may require much stronger signal: $\beta \sqrt{n} \gtrsim \sqrt{d}$ or worse. This gap is the **statistical-computational tradeoff**.

### Memory-Sample Tradeoff Intuition

In streaming settings with limited memory $M$:
- **Pass 1**: Store $O(M)$ bytes of a matrix sketch
- **Pass 2, 3, ...**: Process data again, using stored information

The tradeoff says: if you use few passes, you need $\Omega(k\log(d/k))$ bits to store enough information to reliably detect a $k$-sparse spike among $d$ dimensions.

## Applications in Engineering

### 1. **Sparse Principal Component Analysis (PCA)**
Detect dominant sparse directions in high-dimensional data (genomics, fMRI). The spiked model formalizes when sparse signals are detectable.

### 2. **Anomaly Detection in Streaming Data**
Identify deviations from baseline covariance structure in real-time sensor networks or financial data streams, subject to memory constraints.

### 3. **Hidden Clique/Biclique Detection in Graphs**
The planted spike model underlies detection of planted dense subgraphs. The spiked covariance analysis transfers to graph adjacency matrix analysis.

### 4. **Communication-Constrained Signal Processing**
Characterize fundamental tradeoffs between memory/bandwidth and detection capability in distributed sensing systems.

### 5. **Phase Transitions in Machine Learning**
Understand threshold phenomena in unsupervised learning: below critical signal strength, no algorithm detects the signal regardless of computational power.

## Common Mistakes / Pitfalls

1. **Confusing population vs. sample thresholds:** The spike may be theoretically detectable (information-theoretically) but computationally hard. The spiked model formalizes this distinction.

2. **Ignoring sparsity:** The full-rank spiked model ($\mathbf{v}$ dense) is easier than sparse variants ($\mathbf{v}$ supported on $k \ll d$ coordinates). Sparse PCA is harder.

3. **Assuming eigenvalue gaps suffice:** In the planted regime, the top eigenvalue shifts, but with limited samples and noise, the **signal direction** remains hard to identify even if the eigenvalue itself separates from the bulk.

4. **Misapplying memory lower bounds:** Memory bounds apply to **streaming algorithms** (online, multi-pass). Offline algorithms with random access to full data are unaffected by these bounds.

5. **Underestimating pass complexity:** Multi-pass streaming allows information accumulation across passes. The number of passes $c$ directly enters memory tradeoff formulas—more passes → potentially lower per-pass memory required.

## See Also

- [[Planted structures detection]]: General framework for detecting implanted patterns in random structures
- [[Sparse PCA]]: Principal component analysis