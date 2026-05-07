# Robust Statistics

## Definition

Robust statistics is the field concerned with designing estimators and statistical procedures that maintain accuracy and reliability when data deviates from standard modeling assumptions, particularly in the presence of **data contamination**.

The fundamental problem: given a dataset where a fraction of samples may be corrupted, outliers, or drawn from a different distribution, compute statistics (e.g., mean, covariance) that accurately reflect the *true* underlying clean data rather than the contaminated observations.

### Contamination Models

**Huber's contamination model** (classical):
- A proportion $\alpha \in (0, 1/2)$ of samples are adversarially corrupted
- Remaining fraction $(1-\alpha)$ are drawn i.i.d. from the true distribution $D$
- The corrupted samples can come from *any* arbitrary distribution

**Mean-shift contamination model** (more restrictive):
- A proportion $\alpha$ of samples are replaced with draws from shifted versions of $D$
- Rather than arbitrary corruption, the adversary can only translate/shift the base distribution
- This model allows consistent estimation even when Huber's model does not

## Key Equations

### Mean Estimation Error

For a robust estimator $\hat{\mu}$ of the true mean $\mu^*$ under contamination level $\alpha$:

$$\mathbb{E}\left[\|\hat{\mu} - \mu^*\|_2\right] = O(f(\alpha, d, \epsilon))$$

where the error depends on:
- Contamination fraction $\alpha$
- Dimension $d$
- Accuracy parameter $\epsilon$

### Sample Complexity Bounds

For general base distributions satisfying spectral conditions on the characteristic function:

$$N = \text{poly}\left(\frac{d}{\epsilon^2}\right) \cdot p(\alpha)$$

where $p(\alpha)$ is a polynomial (or near-polynomial) function of the contamination level.

### Fourier-Based Characterization

The characteristic function of distribution $D$:

$$\phi_D(t) = \mathbb{E}[e^{i\langle t, X \rangle}] \quad \text{for } X \sim D$$

Under mean-shift contamination by shift vector $s$:

$$\phi_{D_s}(t) = e^{i\langle t, s \rangle} \phi_D(t)$$

The **Fourier witness** (key technical concept): a frequency $t^*$ where $|\phi_D(t^*)| > 1 - \delta$ for small $\delta$, enabling separation of clean vs. shifted samples.

## Physical Intuition / Derivation

### Why Robustness Matters

In practice, real-world datasets rarely satisfy the ideal i.i.d. assumption:
- **Sensor noise**: outliers, measurement errors, calibration drift
- **Human error**: data entry mistakes, mislabeling
- **Distribution shift**: test data differs from training; out-of-distribution inputs
- **Adversarial corruption**: malicious data manipulation in security-critical applications

Standard estimators (e.g., sample mean $\bar{X} = \frac{1}{n}\sum_{i=1}^n X_i$) collapse catastrophically under contamination—a single adversarial point can push the mean arbitrarily far.

### Intuition for Mean-Shift Model

The mean-shift model sits between:
- **No contamination** (trivial)
- **Arbitrary Huber contamination** (provably impossible to estimate consistently in high dimensions)

By restricting the adversary to *shift* the distribution rather than arbitrarily corrupt, the estimator can:
1. Use Fourier analysis to detect shifted copies (they have different phase behavior in frequency domain)
2. Identify and downweight suspicious samples
3. Recover the true mean with polynomial sample complexity

### Fourier-Based Approach

**Key insight**: A shifted distribution $D_s$ has characteristic function $\phi_{D_s}(t) = e^{i\langle t, s \rangle}\phi_D(t)$. 

- The clean distribution concentrates mass around $\phi_D(0) = 1$
- Shifted versions have oscillating phases depending on the shift $s$ and frequency $t$
- At carefully chosen frequencies, clean and shifted samples have measurably different Fourier signatures
- A "Fourier witness" $t^*$ is a frequency where this separation is most pronounced

This enables a two-step algorithm:
1. Query the empirical characteristic function at witness frequencies
2. Use these queries to identify and filter out contaminated samples
3. Compute the mean on cleaned data

## Applications in Engineering

### 1. **Sensor Fusion & Robotics**
- Integrating data from multiple sensors where some fail or drift
- Robust attitude/position estimation in autonomous systems
- Outlier rejection in multi-sensor localization (GPS + IMU + lidar)

### 2. **Distributed Machine Learning**
- Byzantine-resilient averaging across worker nodes (some may send corrupted gradients)
- Federated learning with untrustworthy clients
- Aggregating model updates in presence of poisoning attacks

### 3. **Quality Control & Manufacturing**
- Estimating process parameters when measurement equipment occasionally malfunctions
- Defect detection while accounting for false positives in inspection systems
- Statistical process control under sporadic measurement drift

### 4. **Financial Data Analysis**
- Estimating asset returns when transaction data contains errors or flash crashes
- Portfolio optimization resistant to market microstructure noise and tick-related artifacts
- Risk metrics robust to extreme but rare events

### 5. **Medical Imaging & Diagnostics**
- Reconstructing signals from noisy/corrupted medical sensors
- Averaging across multiple scanners with different calibration drifts
- Patient population statistics when data includes miscoded/mislabeled cases

### 6. **Network Security**
- Detecting and mitigating botnet-based data poisoning attacks
- Aggregate statistics (average traffic patterns) robust to compromised nodes
- Malware signature generation from contaminated training data

## Common Mistakes / Pitfalls

### 1. **Confusing Contamination Models**
- Assuming algorithms for mean-shift contamination work against Huber contamination
- **Error**: These models have fundamentally different sample complexity; Huber contamination does *not* permit consistent