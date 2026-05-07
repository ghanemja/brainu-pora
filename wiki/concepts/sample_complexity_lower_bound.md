# Sample Complexity Lower Bound

## Definition

A **sample complexity lower bound** is a theoretical result establishing the minimum number of samples an algorithm must observe to achieve a target accuracy level with high probability. In the context of contaminated distributions, it characterizes how the number of required samples scales with problem parameters: contamination level, dimension, error tolerance, and distributional properties.

Formally, a lower bound proves that **any algorithm** (regardless of cleverness) solving a particular inference task requires at least $N(\alpha, \epsilon, d, \delta)$ samples in the worst case. This contrasts with upper bounds, which show that specific algorithms achieve a task with at most $M(\alpha, \epsilon, d, \delta)$ samples.

### In Contamination Settings

When estimating the mean $\mu$ of a distribution $D$ given $\alpha$-mean-shift contaminated samples:
- An adversary can corrupt a fraction $\alpha$ of observations by shifting their mean by an unknown vector $\mathbf{v}$ with $\|\mathbf{v}\| = \epsilon$
- A lower bound quantifies the *information-theoretic* cost of robustness: how many extra samples are needed to overcome adversarial corruption

## Key Equations

Let $\phi_D(\omega)$ denote the characteristic function (Fourier transform) of distribution $D$:

$$\phi_D(\omega) := \mathbb{E}_{x \sim D}\left[e^{2\pi i(\omega \cdot x)}\right], \quad \omega \in \mathbb{R}^d$$

Define the **Fourier mass parameter**:

$$\delta := \inf_{\mathbf{v}: \|\mathbf{v}\| = \epsilon} \inf_{\omega: \text{dist}(\omega \cdot \mathbf{v}, \mathbb{Z}) \geq \alpha} |\phi_D(\omega)|$$

**Main Lower Bound (Theorem 1.2):**

$$\text{Sample complexity} \geq \frac{1}{\delta^{\Omega(1)}} \text{ samples in 1D}$$

$$\text{Sample complexity} \geq \left(\frac{d}{\delta}\right)^{\Omega(1)} \text{ samples in } d \text{ dimensions (product distributions)}$$

Complementary upper bound:

$$\text{Sample complexity} \leq \widetilde{O}_\alpha\left(\frac{d}{\delta^2}\right) \text{ samples}$$

where $\widetilde{O}_\alpha$ hides poly-logarithmic factors and dependencies on $\alpha$.

## Physical Intuition / Derivation

### Why Fourier Analysis?

The adversary's strategy is to **zero out the characteristic function** in a carefully chosen region:
- The adversary can make $\phi_{D^{(\alpha)}_\mu}(\omega) = 0$ for all frequencies $\omega$ satisfying $\text{dist}(\omega \cdot \mathbf{v}, \mathbb{Z}) \leq \alpha$
- This exploits periodic structure: frequencies near lattice points become unreliable signals

The mean-shift contamination model produces:
$$D^{(\alpha)}_\mu = (1-\alpha)D + \alpha Q$$

where $Q$ is the adversary's choice. By choosing $Q$ to concentrate mass strategically, the adversary creates blind spots in Fourier space.

### The Bottleneck: Information-Theoretic Gap

Frequencies where $|\phi_D(\omega)| \geq \delta$ are the **safe frequencies** the algorithm can reliably use:
- Only outside $\{\omega : \text{dist}(\omega \cdot \mathbf{v}, \mathbb{Z}) \leq \alpha\}$ do we retain signal
- The smaller $\delta$, the weaker the signal in safe frequencies
- Weak signal requires exponentially more samples to distinguish from noise

**Dimension dependence:** In $d$ dimensions, the number of "safe" Fourier coordinates scales like $d$, leading to $\Omega(d)$ factor in sample complexity (for product distributions).

### Consistency Impossibility

If $\delta = 0$ (equivalently, if the characteristic function is **bandlimited** with support $[-B, B]$), then:
- No safe frequencies exist
- The adversary can corrupt the algorithm's observations beyond recovery
- **No consistent estimator exists**, regardless of sample size

Example: The sinc$^2$ distribution (Fourier transform of triangular window) is bandlimited, making mean estimation impossible under contamination.

## Applications in Engineering

### 1. Robust Machine Learning
- **Adversarial training certification**: Lower bounds establish fundamental limits on model robustness against poisoned training data
- **Algorithm design**: Guides whether to invest in algorithmic improvements or accept statistical hardness

### 2. Sensor Network Calibration
- Multiple unreliable sensors (some may malfunction or be hacked) measure a signal's mean
- Lower bounds determine how many redundant sensors are needed for certified accuracy
- Directly applies to IoT systems where fraction $\alpha$ of devices may fail

### 3. Statistical Quality Control
- Manufacturing processes: contamination $\alpha$ represents fraction of defective batches
- Lower bounds quantify inspection sample size needed for reliable process mean estimation
- Informs cost-benefit trade-offs in product sampling

### 4. Signal Processing & Communication
- Receivers decode transmitted signals corrupted by adversarial jamming (fraction $\alpha$ of spectrum)
- Sample complexity bounds determine required signal duration or bandwidth for recovery
- Critical for military/secure communications

### 5. Financial Risk Estimation
- Portfolio risk assessment with potentially fraudulent transaction data (contamination $\alpha$)
- Lower bounds show how many market observations are required to certify portfolio safety
- Applies to high-frequency trading and risk management

## Common Mistakes / Pitfalls

### 1. Confusing Lower and Upper Bounds
**Mistake:** Assuming a lower bound proves an algorithm cannot do better.  
**Reality:** A lower bound only states what *some* adversary can force; clever algorithms may match or beat it.

### 2. Ignoring Distribution-Dependent Constants
**Mistake:** Treating $\delta$ as a universal constant independent of $D$.  
**Reality:** $\delta$ is **problem-dependent** and vanishes