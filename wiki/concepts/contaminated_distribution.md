# contaminated distribution

## Definition

A **contaminated distribution** is a probability distribution that results from mixing a "clean" base distribution with an adversarial corruption. Formally, in the **α-mean-shift contaminated model**, the observed distribution is:

$$D^{(\alpha)}_{\mu} = (1-\alpha) D + \alpha Q$$

where:
- $D$ is the clean base distribution over $\mathbb{R}^d$ (centered at origin)
- $\alpha \in (0, 1/2)$ is the **contamination parameter** (fraction of corrupted samples)
- $Q$ is an arbitrary adversarial distribution over mean vectors $\mu$, chosen by an adversary
- The adversary can shift the mean of a fraction $\alpha$ of samples by an unknown vector

Equivalently, in the convolution form: $D^{(\alpha)}_{\mu} = D * Q$, where $*$ denotes convolution.

The **mean-shift error** is characterized by the vector $v = \hat{\mu} - \mu$ where $\hat{\mu}$ is the estimated mean and $\mu$ is the true mean.

## Key Equations

### Characteristic Function Framework

For a distribution $P$ over $\mathbb{R}^d$, the characteristic function is:

$$\varphi_P(\omega) := \mathbb{E}_{x \sim P}\left[e^{2\pi i(\omega \cdot x)}\right], \quad \omega \in \mathbb{R}^d$$

### Critical Fourier Mass Parameter

Define the parameter $\delta$ characterizing identifiability:

$$\delta := \inf_{\|v\| = \varepsilon} \inf_{\omega : \text{dist}(\omega \cdot v, \mathbb{Z}) \geq \alpha} |\varphi_D(\omega)|$$

This represents the smallest magnitude of the characteristic function at frequencies that cannot be "zeroed out" by the adversary.

### Sample Complexity Bounds

**Upper Bound (Theorem 3.2):** There exists an algorithm estimating the contaminated mean from:
$$\tilde{O}_\alpha\left(\frac{d}{\delta^2}\right) \text{ samples}$$

**Lower Bound (Lemma 4.6):** Any algorithm requires at least:
$$\frac{1}{\delta}^{\Omega(1)} \text{ samples}$$

For product distributions in $d$ dimensions, the lower bound generalizes to $(d/\delta)^{\Omega(1)}$.

## Physical Intuition / Derivation

### Why Characteristic Functions?

The adversary's power lies in their ability to **corrupt the Fourier content** of the distribution. Consider what happens at a frequency $\omega$:

- If $\text{dist}(\omega \cdot v, \mathbb{Z}) \leq \alpha$ (distance to nearest integer), the adversary can nearly **cancel out** the contribution of the true mean shift at that frequency by distributing corrupted samples cleverly
- If $\text{dist}(\omega \cdot v, \mathbb{Z}) \geq \alpha$, the adversary **cannot fully eliminate** the signal, and the frequency $\omega$ "sees" the mean shift

### Identifiability Condition

Mean estimation becomes impossible (no algorithm can achieve consistency) when:
$$\delta = 0 \iff \{{\omega : \text{dist}(\omega \varepsilon, \mathbb{Z}) \geq \alpha}\} \text{ has zero Fourier mass}$$

**Example:** A distribution with **band-limited characteristic function** (e.g., sinc²) has $\varphi_D(\omega) = 0$ for $|\omega| \geq B$. Since the useful frequencies are all "outside the band," $\delta = 0$ and mean estimation is impossible under contamination.

### Why Sample Complexity Grows with $1/\delta^2$

To reliably detect a mean shift $v$ at frequency $\omega$, we need enough samples so that:
$$\text{Signal} = |\varphi_D(\omega)| \gg \text{Noise} = \sqrt{\text{Var}[\varphi_{\text{empirical}}] / n}$$

Since the signal strength is $\delta$ (the minimum over hard frequencies), we need roughly $n \sim 1/\delta^2$ samples to achieve signal-to-noise ratio of order 1. The dimension $d$ enters because the adversary has more freedom in higher dimensions to align corruptions with the mean shift.

## Applications in Engineering

### 1. **Machine Learning & Robust Statistics**
- **Robust mean estimation** under label noise or data poisoning attacks
- Training algorithms on datasets with label corruption (e.g., medical imaging with mislabeled samples)
- Byzantine-robust distributed learning in federated systems

### 2. **Signal Processing**
- Detection and parameter estimation when a fraction of received signals are adversarially jammed
- Radar/sonar systems with spoofed or corrupted returns
- Communication channels with malicious interference

### 3. **Quality Control & Manufacturing**
- Estimating true process mean when a fraction of measurements are faulty or sabotaged
- Outlier-robust statistical monitoring of production lines
- Sensor fusion with partially unreliable sensors

### 4. **Finance & Economics**
- Estimating portfolio returns when a fraction of historical data points are corrupted (market manipulation, fraud)
- Robust price index estimation under data quality issues

### 5. **Cybersecurity**
- Intrusion detection with adversarially crafted minority traffic flows
- Malware analysis when portion of samples are obfuscated
- Fingerprint/biometric authentication with deliberate spoofing attempts

## Common Mistakes / Pitfalls

### 1. **Confusing $\alpha$ with Gaussian Variance**
Students often mistakenly think larger $\alpha$ makes estimation *easier* (like narrowing a confidence interval). In fact, larger contamination makes the problem *harder*. However, the relationship is nonlinear: the sample complexity doesn't blow up until $\alpha$ approaches $1/2$ (majority rule breaks down).

### 2. **Assuming Simple Thresholding Works**
A naive approach—"just remove the $\alpha$ fraction of largest deviations"