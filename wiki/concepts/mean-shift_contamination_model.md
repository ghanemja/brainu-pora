# mean-shift contamination model

## Definition

The mean-shift contamination model is a robust statistics framework for analyzing estimators under adversarial data corruption. In this model:

- A dataset consists of $n$ samples nominally drawn from a clean distribution $D$ over $\mathbb{R}^d$
- An adversary is allowed to **replace** a fraction $\alpha \in (0, 1/2)$ of samples with arbitrary points
- Critically: the adversarial samples need not be arbitrary; they are drawn from **shifted versions** of the base distribution $D$
- Mathematically, each observed sample $x$ is:
  - drawn from $D$ with probability $1-\alpha$ (clean)
  - drawn from $D + \mu_{\text{adv}}$ with probability $\alpha$ (contaminated by unknown shift $\mu_{\text{adv}} \in \mathbb{R}^d$)

The goal is to estimate the mean $\mathbb{E}[X]$ of the clean distribution despite contamination.

## Key Equations

**Observed distribution under contamination:**
$$P_{\text{obs}} = (1-\alpha)D + \alpha(D + \mu_{\text{adv}})$$

**Observed mean:**
$$\mathbb{E}_{\text{obs}}[X] = (1-\alpha)\mathbb{E}_D[X] + \alpha(\mathbb{E}_D[X] + \mu_{\text{adv}}) = \mathbb{E}_D[X] + \alpha\mu_{\text{adv}}$$

**Target estimation error (per coordinate or in norm):**
For an estimator $\hat{\mu}$ of the true mean $\mu^* = \mathbb{E}_D[X]$:
$$\|\hat{\mu} - \mu^*\| \leq \epsilon$$

**Sample complexity:** The number of samples $n$ required to achieve error $\epsilon$ with confidence $1-\delta$, expressed as:
$$n = \text{poly}(d, 1/\alpha, 1/\epsilon, \log(1/\delta), \text{spectral properties of } D)$$

**Fourier-based characterization** (central to this model):
For characteristic function $\phi(\mathbf{t}) = \mathbb{E}[e^{i\langle \mathbf{t}, X \rangle}]$, recovery is possible if $D$ satisfies spectral conditions such as bounded variance or tail decay in Fourier domain.

## Physical Intuition / Derivation

### Why mean-shift contamination?

Classical **Huber's contamination model** allows the adversary to replace samples with *arbitrary* points anywhere in space. A key insight from prior work: under Huber's model, consistent mean estimation is **information-theoretically impossible** because the adversary can place corrupted samples far away, and there's no way to distinguish them.

The mean-shift model is *weaker* because:
- The adversary cannot inject completely arbitrary points
- Corrupted samples still come from the distribution $D$, just shifted
- This geometric constraint makes the problem tractable

### Intuition via Fourier witnesses

The core challenge is detecting contamination without knowing its magnitude $\alpha$ or direction $\mu_{\text{adv}}$. The solution relies on **Fourier analysis**:

1. Sample the empirical distribution and compute its characteristic function $\hat{\phi}(\mathbf{t})$
2. For a clean distribution, $\hat{\phi}(\mathbf{t}) \approx \phi(\mathbf{t})$
3. Under contamination, $\hat{\phi}(\mathbf{t}) \approx (1-\alpha)\phi(\mathbf{t}) + \alpha e^{i\langle \mathbf{t}, \mu_{\text{adv}} \rangle}\phi(\mathbf{t})$
4. A **Fourier witness** is a frequency $\mathbf{t}$ where $|\phi(\mathbf{t})|$ is small but its absolute value reveals contamination

The characteristic function acts as a "fingerprint"—contaminated data leaves detectable marks in Fourier space.

### Spectral conditions

The model requires mild conditions on $D$:
- The characteristic function must decay sufficiently fast
- Equivalently: $D$ cannot have heavy point masses or pathological structure
- Gaussian, sub-Gaussian, and Laplace distributions satisfy these conditions

## Applications in Engineering

### 1. **Sensor Networks & IoT**
- Sensors occasionally transmit corrupted readings (sensor drift, miscalibration)
- Mean-shift model: drift shifts measurements by a fixed offset rather than introducing random noise
- Application: robust localization, temperature monitoring, air quality assessment
- Advantage over Huber: accounts for systematic bias rather than arbitrary faults

### 2. **Machine Learning & Feature Estimation**
- Training data contamination (label noise, out-of-distribution examples)
- Estimate feature statistics (mean pixel values, word embeddings) robustly
- The model helps separate systematic biases from arbitrary outliers

### 3. **Control Systems**
- Estimate plant state from noisy sensor measurements
- Sensor faults often manifest as constant biases (mean shifts) rather than arbitrary spikes
- Used in conjunction with Kalman filters for robust state estimation

### 4. **Medical Data Analysis**
- Patient measurements (blood pressure, glucose) may be systematically biased by equipment calibration drift
- Mean-shift contamination reflects real miscalibration scenarios
- Sample-efficient estimation avoids requiring excessive patient samples

### 5. **Signal Processing**
- Channel estimation under fading with timing offsets (introduce deterministic shifts)
- Frequency synchronization estimation with biased measurements
- Phase noise has additive structure compatible with mean-shift model

### 6. **Network Monitoring**
- Estimate average latency/throughput when some monitoring agents report systematically biased metrics
- Distinguish between systematic bias and arbitrary anomalies

## Common Mistakes / Pitfalls

### 1. **Confusing with Huber's Model**
**Mistake:** Assuming mean-shift and Huber contamination have similar difficulty.  
**Reality:** Mean-shift is substantially easier (consistent estimation possible); the geometric constraint on contamination is crucial.

### 2. **Ign