# Sample Complexity

## Definition

**Sample complexity** is the minimum number of samples (data points) required by an algorithm to achieve a target accuracy with high probability. More formally, for a given learning or estimation problem, sample complexity is the function $n(\epsilon, \delta, d, \ldots)$ that specifies how many independent samples are necessary to:

- Estimate an unknown parameter to error at most $\epsilon$ with probability at least $1 - \delta$
- Achieve this in dimension $d$ (or higher-dimensional settings)
- Under given distributional or adversarial assumptions

In the context of **contaminated/robust mean estimation**, the sample complexity captures the fundamental tradeoff between:
- Error tolerance $\epsilon$ (desired accuracy)
- Contamination level $\alpha$ (fraction of adversarially corrupted samples)
- Tail behavior $\sigma$ (distribution's heavy-tailedness)
- Robustness parameter $\delta$ (concentration measure)

## Key Equations

### Lower Bound for Contaminated Mean Estimation

For univariate distributions $D$ satisfying regularity conditions, any algorithm estimating the mean to error $\epsilon$ under $\alpha$-mean-shift contamination requires:

$$n \geq \Omega\left(\frac{1}{(\delta\sigma)^{1/3}} + \left(\frac{\epsilon}{\alpha}\right)^3\left(\frac{\delta}{\sigma}\right)^2\right)$$

where:
- $\delta$ = L₂-norm concentration measure of Fourier coefficients near integer points
- $\sigma$ = tail bound parameter (Pr$_{x \sim D}[|x| \geq R] \leq \sigma/R$)
- $\epsilon$ = target error
- $\alpha$ = contamination fraction

**Simplified regime** (when $(\epsilon/\alpha)^3(\delta/\sigma)^2 \leq (\delta\sigma)^{1/3}$):

$$n = \Omega\left(\frac{1}{(\delta\sigma)^{1/3}}\right)$$

### High-Dimensional Scaling

For $d$-dimensional product distributions, the sample complexity scales as:

$$n(\text{multivariate}) = \max\left(n(\text{univariate}), \Omega(d)\right)$$

By Hölder's inequality, this gives a combined lower bound of:

$$n \geq d^{1/p} \cdot (\text{univariate lb})^{1/q} \quad \text{where } \frac{1}{p} + \frac{1}{q} = 1$$

For Gaussian distributions with $\alpha$-mean shift in $d$ dimensions:

$$n = d^{0.99} \cdot e^{\Omega(({\alpha}/{\epsilon})^2)}$$

(tight up to polynomial factors)

### Upper Bound (Algorithmic)

A properly designed robust mean estimator achieves error $\epsilon$ using:

$$n = \tilde{O}\left(\frac{d}{\alpha^2} + \frac{1}{(\delta\sigma)^{1/3}}\right)$$

This typically requires empirical covariance-based filtering or moment-based methods.

## Physical Intuition / Derivation

### Why Sample Complexity Matters

Imagine estimating a distribution's mean when some adversary can **corrupt a fraction $\alpha$ of the samples**. If you collect $n$ samples:
- In expectation, $\approx \alpha n$ are corrupted (shifted by arbitrary amounts)
- You only trust $\approx (1-\alpha)n$ samples
- The adversary tries to make your estimator as wrong as possible

**The tradeoff:**
- Smaller $\alpha$ (less corruption) → fewer samples needed
- Larger $\epsilon$ (looser accuracy requirement) → fewer samples needed
- Heavier tails ($\sigma$ large) → *more* samples needed, because outliers are harder to distinguish from corruption

### Why Does $(\delta\sigma)^{-1/3}$ Appear?

The term $(1/(\delta\sigma)^{1/3})$ arises from an **information-theoretic lower bound** constructed via:

1. **Fourier analysis**: The distribution $D$ has most of its Fourier mass concentrated near integer frequencies (controlled by $\delta$)
2. **Adversarial hardness**: An adversary places contamination in frequency regions where they can't be detected
3. **Dimension of indistinguishability**: The adversary needs roughly $1/(\delta\sigma)^{1/3}$ samples to align contamination with the signal

### Why $(\epsilon/\alpha)^3(\delta/\sigma)^2$ Appears

When $\epsilon/\alpha$ is large (target error is loose relative to contamination), a second regime dominates:
- You need roughly $(\epsilon/\alpha)^3$ overhead to tolerate the contamination magnitude
- Tail heaviness ($\sigma$) makes this worse (multiplied by $(\delta/\sigma)^2$)

## Applications in Engineering

### 1. **Robust Statistics & Data Cleaning**
- **Data center monitoring**: Removing sensor faults from network telemetry while maintaining mean estimates of throughput/latency
- **Manufacturing QC**: Estimating true process mean when up to $\alpha$ fraction of measurements are outliers
- **Medical imaging**: Reconstructing patient statistics from partially corrupted sensor data

### 2. **Machine Learning & Training**
- **Label noise robustness**: Training on datasets with $\alpha$ fraction of mislabeled examples
- **Byzantine-resilient distributed learning**: Coordinating across machines where $\alpha$ fraction send adversarial gradients
- **Sample-efficient reinforcement learning**: Quantifying how many environment interactions needed to learn robust policies despite adversarial perturbations

### 3. **Signal Processing**
- **Spectrum estimation with interference**: Estimating signal characteristics when $\alpha$ fraction of frequency bins contain jamming
- **Communication under erasure**: Recovering transmitted mean values with some packets corrupted

### 4. **Control Systems**
- **Sensor fusion with outliers**: Combining measurements from multiple sensors where a fraction may fail
- **Adversarial robustness**: Designing controllers that learn models from partially corrupted state observations

### 5