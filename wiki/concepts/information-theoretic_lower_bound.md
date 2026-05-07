# information-theoretic lower bound

## Definition

An **information-theoretic lower bound** is a fundamental limit on the sample complexity (or computational resources) required to solve a statistical estimation problem, derived from information theory rather than algorithmic constraints. It establishes a *necessary* condition: no algorithm—regardless of computational power—can achieve a target accuracy $\rho$ using fewer samples than the bound prescribes.

Formally, for an estimation problem with parameter space of dimension $d$ and target error $\rho$, an information-theoretic lower bound proves that any estimator $\hat{\theta}$ requires:

$$n \geq f(d, 1/\rho, \delta, \ldots)$$

samples in the worst case, where $\delta$ is the failure probability. This bound is **independent of the algorithm used**—it applies to all estimators, efficient or not.

## Key Equations

For the problems discussed in the source material:

**Mean Estimation (all-or-nothing setting):**
$$n \gtrsim d \cdot e^{1/\rho^2}$$
samples are necessary and sufficient information-theoretically to achieve $\ell_2$ error at most $\rho$.

**Covariance Estimation:**
$$n \gtrsim d \cdot e^{1/\rho}$$
samples necessary to achieve relative operator norm error $\rho$.

**Linear Regression:**
$$n \gtrsim d \cdot e^{1/\rho^2}$$
samples necessary and sufficient.

These bounds establish baseline requirements that all estimators must satisfy.

## Physical Intuition / Derivation

### Why Information-Theoretic Bounds Matter

Information-theoretic lower bounds answer the question: **"What is the fundamental limit imposed by nature, not computation?"** They arise from two sources:

1. **Statistical Complexity**: Data has finite information content. To distinguish between $M$ hypotheses with high confidence, roughly $\log M$ bits of information are needed.

2. **Dimensionality Curse**: In dimension $d$, the parameter space grows exponentially, requiring exponentially more samples to explore it thoroughly.

### Intuitive Derivation (Sketch)

Consider mean estimation in dimension $d$:
- To achieve error $\rho$, we must distinguish the true mean from all means at distance $> \rho$.
- The effective "volume" of hypotheses grows with $d$ and shrinks with $\rho$.
- Fisher information theory shows that each sample provides roughly $O(d)$ bits of information about the mean.
- Achieving error $\rho$ requires reducing uncertainty by a factor exponential in $1/\rho^2$, necessitating roughly $e^{1/\rho^2}$ samples.

### Hardness vs. Tractability

The source material reveals a crucial distinction:

| Problem | Information-Theoretic | Computational (SQ) | Gap? |
|---------|----------------------|-------------------|------|
| Mean estimation | $d \cdot e^{1/\rho^2}$ | $d^{\Omega(1/\rho^2)}$ | **Yes** |
| Covariance | $d \cdot e^{1/\rho}$ | $d^{1/\rho}$ | **Yes** |
| Linear regression | $d \cdot e^{1/\rho^2}$ | $d \cdot e^{1/\rho^2}$ (achievable) | **No** |

This reveals that:
- Some problems have **statistical-computational gaps**: information-theoretically feasible but computationally hard.
- Other problems (like linear regression) have no such gap—efficient algorithms match the lower bound.

## Applications in Engineering

### 1. Machine Learning & Statistical Estimation
- **Model Selection**: Determines minimum dataset size before any algorithm can succeed.
- **Algorithm Design**: If an algorithm matches the information-theoretic bound, it is *optimal* and no better algorithm exists (up to constants).

### 2. Sensor Networks & Distributed Systems
- **Minimum Measurement Requirements**: For state estimation in dynamical systems, bounds dictate the minimum sensor count needed to reconstruct the state with guaranteed accuracy.
- **Communication Complexity**: Combines with rate-distortion theory to determine bandwidth needs.

### 3. Compressed Sensing
- Establishes how many measurements $m$ are required to recover a $k$-sparse signal in dimension $d$:
$$m \gtrsim k \log(d/k)$$
This bound is often *tight*, proving existing algorithms (orthogonal matching pursuit, basis pursuit) are near-optimal.

### 4. Privacy-Utility Tradeoffs
- **Differential Privacy**: Information-theoretic bounds quantify the privacy cost of accurate estimation. Adding Laplace noise for differential privacy requires sample complexity to increase by factor $e^{\Theta(1/\epsilon)}$ (where $\epsilon$ is privacy parameter).

### 5. Contaminated Data & Robustness
- **Adversarial Corruption**: The source material studies *missing data* corruption. Bounds show that robustness to contamination comes at an exponential cost in sample complexity (compared to clean data).

## Common Mistakes / Pitfalls

### 1. Confusing "Lower Bound" with "Achievable"
- **Mistake**: Thinking that because a lower bound is $\Omega(e^{1/\rho^2})$, no algorithm achieves this rate.
- **Reality**: Information-theoretic bounds are *achievable* (by definition—information theory is constructive). The bound says "at least this many samples; algorithms exist using this many."

### 2. Ignoring Hidden Constants
- **Mistake**: Claiming $n \gtrsim d \cdot e^{1/\rho^2}$ means $n = d \cdot e^{1/\rho^2}$ exactly.
- **Reality**: The $\gtrsim$ notation hides polylogarithmic factors and constants. Actual constants matter in practice.

### 3. Assuming Bounds Apply to All Settings
- **Mistake**: Taking a bound from "all-or-nothing" missing data and applying it to "multiple pattern" missingness without adjusting.
- **Reality**: The source material notes these settings are non-comparable. Multiple-pattern settings admit a multiplicative factor $C^{|S|}$ degradation, where $|S|