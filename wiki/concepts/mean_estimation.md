# Mean Estimation

## Definition

**Mean estimation** is the fundamental statistical task of computing an unbiased estimate of the expected value (population mean) $\mu$ of a distribution $D$ from $n$ i.i.d. samples $\{x_1, x_2, \ldots, x_n\}$ drawn from $D$.

In the **robust mean estimation** setting, the data is contaminated: an adversary replaces a fraction $\alpha \in (0, 1/2)$ of clean samples with arbitrary or shifted samples. The goal remains to accurately estimate $\mu$ despite this corruption.

### Mean-Shift Contamination Model

A specific contamination paradigm where:
- Fraction $1-\alpha$ of samples: drawn from clean distribution $D$
- Fraction $\alpha$ of samples: drawn from adversarially shifted versions of $D$ (translations of $D$ by arbitrary means)

This is weaker than Huber's contamination model (where corrupted samples can be arbitrary) but stronger than the clean i.i.d. setting.

## Key Equations

**Empirical mean estimator (uncontaminated case):**
$$\hat{\mu} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

**Sample complexity bound (under Fourier conditions):**

For a base distribution with characteristic function $\phi(t) = \mathbb{E}[e^{i\langle t, X\rangle}]$, robust mean estimation to accuracy $\epsilon$ requires:
$$n = \text{poly}\left(\frac{d}{\alpha \epsilon}, \log(1/\delta)\right)$$

under mild spectral conditions on $\phi$ (specifically, existence of a "Fourier witness").

**Contamination tolerance:** Consistent estimation is possible when contamination fraction $\alpha < 1/2$.

## Physical Intuition / Derivation

### Why Standard Empirical Mean Fails

The empirical mean is **not robust** to contamination. A single outlier can shift the mean arbitrarily far:
$$\hat{\mu}_{\text{bad}} = \frac{(1-\alpha)n\mu + \alpha n \cdot B}{n}$$
where $B$ is an adversarial shift of arbitrary magnitude.

### Robustness via Fourier Analysis

The key insight is to use **Fourier-domain filtering**:

1. **Characteristic function preservation:** Under mean-shift contamination, the contaminated empirical characteristic function $\hat{\phi}(t)$ remains close to the true characteristic function in certain directions.

2. **Fourier witness:** A direction $t^* \in \mathbb{R}^d$ such that:
   - $|\phi(t^*)|$ is bounded away from zero
   - The spectral mass is concentrated near $t^*$
   
   This direction allows discrimination between clean and contaminated data in Fourier space.

3. **Filtering strategy:**
   - Compute empirical characteristic function $\hat{\phi}_n(t)$
   - Use Fourier witness to identify/downweight samples deviating in the contaminated direction
   - Reconstruct mean via inverse Fourier transform

### Sample Complexity Intuition

For Gaussian or Laplace distributions, dimension-independent sample complexity is achievable. For general distributions:
- Sample complexity grows with dimension $d$
- Growth factor depends on "separability" of the distribution in Fourier space
- Mild spectral conditions ensure the contaminated and clean distributions are distinguishable

## Applications in Engineering

### 1. **Sensor Network Calibration**
Estimating true environmental parameters (temperature, pressure) when some sensor readings are biased due to miscalibration. Mean-shift contamination models systematic sensor drift.

### 2. **Data Quality in Machine Learning Pipelines**
Training datasets often contain systematic labeling errors or out-of-distribution noise that shifts features. Robust mean estimation enables reliable preprocessing.

### 3. **Signal Processing**
Estimating true signal statistics when measurement channels are subject to additive noise or gain shifts (modeled as mean-shift).

### 4. **System Identification**
In control systems, identifying true dynamics when some measurements are corrupted by time-varying biases rather than random noise.

### 5. **Financial Data Analysis**
Computing true market statistics when a fraction of data points reflect market anomalies or reporting errors with systematic biases.

## Common Mistakes / Pitfalls

### 1. **Confusing Robust and Resistant Estimators**
- **Robust:** Gracefully degrades with contamination (asymptotic analysis)
- **Resistant:** Works perfectly up to contamination fraction $\alpha$ (finite-sample guarantees)

Mean estimation with mean-shift contamination achieves resistance (exact estimation), not just robustness.

### 2. **Assuming Tukey's Median Works Universally**
Coordinate-wise medians are robust in 1D but suffer curse of dimensionality in high dimensions. Fourier-based methods address this.

### 3. **Ignoring Spectral Conditions**
Not all distributions admit sample-efficient robust mean estimation. The mild spectral conditions (existence of Fourier witness) are essential—without them, lower bounds prove hardness.

### 4. **Conflating with Huber Contamination**
In Huber's model, consistent estimation is *impossible* for general distributions. Mean-shift contamination is fundamentally easier because corrupted samples still come from recognizable (shifted) versions of $D$.

### 5. **Overestimating Contamination Tolerance**
While $\alpha < 1/2$ is necessary, sample complexity becomes prohibitive as $\alpha$ approaches $1/2$. Practical algorithms require small $\alpha$.

## See Also

- [[Robust Statistics]] — parent field addressing estimation under data contamination
- [[Characteristic Function]] — Fourier-domain tool central to mean-shift detection
- [[Sample Complexity]] — theoretical analysis of data requirements for estimation
- [[Contamination Models]] — taxonomy including Huber, mean-shift, and variants
- [[High-Dimensional Statistics]] — curse/blessing of dimensionality in robust estimation

## Sources

- Diakonikolas, I., Iakovidis, G., Kane, D. M., & Liu, S. (2026). "Sample Complexity Bounds for Robust Mean Estimation with Mean-Shift