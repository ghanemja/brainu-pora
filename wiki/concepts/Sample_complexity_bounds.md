# Sample Complexity Bounds

## Definition

**Sample complexity bounds** quantify the minimum number of samples required to learn or estimate a target property of a distribution (or verify properties like calibration) to within a specified accuracy level $\varepsilon$, with high probability. More formally, sample complexity is the smallest $n$ such that with $n$ independent samples from an unknown distribution $D$, an estimator can achieve error $\leq \varepsilon$ with probability $\geq 1-\delta$.

In the context of calibration, sample complexity bounds establish:
- **Lower bounds**: The fundamental minimum sample size needed to distinguish between two scenarios
- **Upper bounds**: Sufficient conditions on sample size to guarantee convergence

A key distinction emerges between:
- **Computational sample complexity**: samples needed with efficient algorithms
- **Statistical sample complexity**: information-theoretic lower bounds (ignoring computation)

## Key Equations

### Lower Bound Construction (Indistinguishability)

For a domain with $k$ "hidden" elements, collision probability requires:

$$\text{Sample size needed for collision} = \Omega(\sqrt{|X|})$$

This arises from the birthday paradox: the probability of collision among $k$ elements from a domain of size $|X|$ becomes non-negligible only at $O(\sqrt{|X|})$ samples.

### Calibration Distance Lower Bound

Consider a domain $X = \{x_-, x_+\} \cup \{x_1, \ldots, x_k\}$ with mass allocation:
- $\mu_D(x_-) = \mu_D(x_+) = 1/4$  
- $\mu_D(x_i) = 1/(2k)$ for $i = 1, \ldots, k$

**Pure case** (all $\mu_D(x_i) = 1/2$):
$$\text{CalDist}_D(f) = \frac{1}{4}\left|\frac{1}{3} - \frac{1}{2}\right| + \frac{1}{4}\left|\frac{2}{3} - \frac{1}{2}\right| = \frac{1}{12}$$

**Mixed case** ($\mu_D(x_i) \sim \text{Bernoulli}(1/2)$ independently):
$$\text{CalDist}_D(f) \leq \frac{1}{24} + O(1/\sqrt{k})$$

The $\Omega(1)$ gap in calibration distance between indistinguishable cases (requiring $\Omega(\sqrt{|X|})$ samples to distinguish) yields a sample complexity lower bound.

### General Transportation/Cost Framework

For partitions of domain $X$:
- Cost per partition element: $\Omega(1/k^2)$ for separation $\Omega(1/k)$
- Total partition cost: $k \cdot \Omega(1/k^2) = \Omega(1/k)$

## Physical Intuition / Derivation

### Why Collisions Matter

With fewer than $\sqrt{|X|}$ samples, the probability that any two domain elements appear together in the sample is vanishingly small. This means:

1. **Indistinguishability**: If an adversary designs two distributions that differ only on rare elements, distinguishing them requires seeing those elements multiple times.
2. **Information-theoretic bottleneck**: Until collisions occur, observed labels are independent draws from $\text{Bernoulli}(1/2)$, providing no information about the underlying structure.

### Two-Distribution Trap

The proof constructs:
- **Distribution A (pure)**: All hidden elements have $\mu_D = 1/2$ → requires moving all mass → cost = $1/12$
- **Distribution B (mixed)**: Hidden elements randomly assigned 0 or 1 → roughly half move to each side → cost $\approx 1/24$

Before collision ($n \ll \sqrt{k}$), the samples look identical under both distributions, but the true calibration distance differs by $\Omega(1)$. This forces any algorithm to take at least $\Omega(\sqrt{|X|})$ samples.

### Robustness to Non-Typicality

The analysis handles the realistic case where only a *large fraction* (not all) elements are "typical" because the cost lower bound is proportional to size, absorbing constants and variations.

## Applications in Engineering

### 1. **Machine Learning / Calibration**
- Ensuring probabilistic classifiers make well-calibrated predictions (e.g., when model predicts 60% confidence, true accuracy ≈60%)
- Determining minimum validation set size to certify calibration with error $\varepsilon$

### 2. **Statistical Testing & A/B Testing**
- Computing required sample sizes for hypothesis tests with power $1-\beta$ and significance $\alpha$
- Trade-off: increasing sample size reduces both Type I and Type II error

### 3. **Reinforcement Learning**
- Horizon length $O(1/\varepsilon^3)$ for sequential calibration (related result: Hart's analysis)
- Sample complexity of learning optimal policies in unknown MDPs

### 4. **Cryptography & Adversarial Settings**
- Distinguishing two families of distributions under computational constraints
- Lower bounds on adversary samples needed to break schemes

### 5. **Sensor Networks & Distributed Estimation**
- Minimum number of sensor readings to estimate environmental properties within tolerance
- Communication-sample complexity trade-offs in distributed learning

### 6. **Quality Assurance / Manufacturing**
- Batch inspection size to detect defects with confidence
- Reliability testing: samples needed to certify MTBF (mean time between failures)

## Common Mistakes / Pitfalls

### 1. **Confusing Necessary and Sufficient Conditions**
- A lower bound (e.g., $\Omega(\sqrt{|X|})$) is *necessary* but not always *achievable* computationally
- Algorithm may require exponentially more samples than information-theoretic minimum

### 2. **Ignoring Hidden Constants**
- $\Omega(1/\varepsilon^2)$ and $O(1/\varepsilon^2)$ differ by constants that matter in practice
- $O(\sqrt{|X|})$ could mean