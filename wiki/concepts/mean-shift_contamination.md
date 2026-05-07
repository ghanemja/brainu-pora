# mean-shift contamination

## Definition

**Mean-shift contamination** is an adversarial corruption model where an attacker modifies the mean of a statistical distribution by an unknown amount. Specifically, given a base distribution $D$ centered at zero with mean $\mu = 0$, an adversary observes samples and shifts the mean to some contaminated mean $\tilde{\mu}$, creating a corrupted distribution $D^{(\alpha)}_{\tilde{\mu}}$.

The model is parameterized by:
- **Base distribution** $D$ with characteristic function $\phi_D$
- **Contamination parameter** $\alpha \in (0, 1/2)$: controls the fraction/magnitude of allowable mean shift
- **Mean shift** $v$: the vector by which the adversary displaces the mean, with $\|v\| = \varepsilon$ (target error)

The adversary's power is *bounded but directional*: they can only shift the mean, not arbitrarily corrupt all moments.

## Key Equations

**Contaminated distribution (convolution form):**
$$D^{(\alpha)}_{\mu} = D \ast Q$$

where $D$ is the base distribution and $Q$ is an adversarially-chosen distribution over mean vectors constrained by the contamination bound $\alpha$.

**Characteristic function of contaminated distribution:**
$$\phi_{D^{(\alpha)}_{\mu}}(\omega) = \phi_D(\omega) \cdot e^{2\pi i(\omega \cdot \mu)}$$

**Fourier-based identifiability condition:**

Define the set of "identifiable" frequencies as:
$$\Omega_{\text{safe}} = \{\omega : \text{dist}(\omega \cdot v, \mathbb{Z}) \geq \alpha\}$$

where $\text{dist}(\cdot, \mathbb{Z})$ is the distance to the nearest integer.

**Sample complexity (Theorem 1.2):**

Upper bound: An algorithm can estimate the mean from
$$\tilde{O}_\alpha\left(\frac{d}{\delta^2}\right)$$
samples, where
$$\delta = \inf_v \min_{\omega \in \Omega_{\text{safe}}} |\phi_D(\omega)|$$

Lower bound: Any algorithm requires $\Omega(1/\delta^{1})$ samples (univariate) or $\Omega((d/\delta)^{1})$ samples (multivariate product distributions).

## Physical Intuition / Derivation

### Why Fourier Analysis Matters

The key insight is that mean-shift contamination is *frequency-dependent*. When the adversary shifts the mean by $v$, this manifests in the Fourier domain as:
$$\phi_{D^{(\alpha)}_{\mu}}(\omega) = \phi_D(\omega) \cdot e^{2\pi i(\omega \cdot \mu)}$$

The phase factor $e^{2\pi i(\omega \cdot \mu)}$ encodes the mean shift. At certain frequencies, this phase wraps around the unit circle and becomes undetectable—specifically, when $\omega \cdot v \approx \text{integer}$.

### Adversarial Geometry

The set $\{\omega : \text{dist}(\omega \cdot v, \mathbb{Z}) \leq \alpha\}$ represents frequencies where the adversary can effectively "zero out" the signal by choosing $\mu = v$ such that $e^{2\pi i(\omega \cdot v)} \approx 1$. 

Conversely, frequencies where $\text{dist}(\omega \cdot v, \mathbb{Z}) \geq \alpha$ remain identifiable because the phase shift is large enough to distinguish from noise.

### Sample Complexity Through Fourier Mass

The parameter $\delta$ captures how much Fourier mass the distribution concentrates in identifiable frequencies:
$$\delta = \inf_v \min_{\omega \in \Omega_{\text{safe}}} |\phi_D(\omega)|$$

- **Large $\delta$**: Distribution has significant energy at identifiable frequencies → easy to estimate mean
- **Small $\delta$**: Most energy at frequencies the adversary can corrupt → hard to estimate mean
- **$\delta = 0$**: Band-limited distributions (e.g., sinc²) where no frequencies escape corruption → **impossible to estimate consistently**

## Applications in Engineering

### 1. Robust Statistics & Quality Control
In manufacturing, mean-shift contamination models systematic bias introduced by adversarial or Byzantine sensors. Engineers must distinguish true process mean from shifted measurements.

### 2. Adversarial Machine Learning
Training data may be poisoned with a systematic shift in features (e.g., adversary adds $+0.1$ to all sensor readings). This theory bounds sample complexity for robust mean estimation in neural networks.

### 3. Distributed Sensing & Byzantine-Tolerant Algorithms
In wireless sensor networks or IoT systems, compromised nodes may report measurements with consistent bias. The theory informs how many redundant sensors are needed to overcome this contamination.

### 4. Calibration & Drift Estimation
Sensor drift (systematic measurement error) can be modeled as mean-shift contamination. The Fourier characterization determines whether drift is *identifiable* from noisy measurements without ground truth.

### 5. Communication Under Adversarial Noise
In information theory, mean-shift contamination models an eavesdropper who can introduce correlated bias. The theory bounds how many channel uses are needed for reliable communication.

## Common Mistakes / Pitfalls

### 1. Confusing Contamination with Outliers
**Wrong:** Treating mean-shift contamination as if outliers are uniformly random corruptions.

**Right:** The adversary is *strategic and coordinated*—all contaminated samples shift by the same (unknown) vector $v$, not random noise added independently.

### 2. Ignoring the Role of Dimensionality in $\delta$
**Wrong:** Assuming $\delta$ is independent of dimension $d$.

**Right:** For product distributions, $\delta$ may depend on $d$ (e.g., multivariate Gaussians have different Fourier structure). The $(d/\delta)^{\Omega(1)}$ lower bound reflects this coupling.

### 3. Assuming High-Variance