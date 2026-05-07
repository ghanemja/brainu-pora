# Differential Privacy (ε-DP)

## Definition

**Differential Privacy** is a formal mathematical guarantee that a randomized algorithm's output is insensitive to changes in any single individual's data. Specifically, a mechanism $M$ is $\varepsilon$-**differentially private** if for all pairs of neighboring datasets $D$ and $D'$ that differ in exactly one record, and for all possible outputs $S$ of $M$:

$$\Pr[M(D) \in S] \leq e^{\varepsilon} \cdot \Pr[M(D') \in S]$$

where $\varepsilon > 0$ is the **privacy budget** (smaller $\varepsilon$ means stronger privacy guarantees).

Two datasets are **neighbors** if one can be obtained from the other by adding, removing, or modifying a single individual's record.

---

## Key Equations

### Privacy Loss Definition
For neighboring datasets $D \sim D'$, the instantaneous privacy loss is:
$$L(D, D') = \ln \left( \frac{\Pr[M(D) = o]}{\Pr[M(D') = o]} \right)$$

### Fairness and Welfare Metrics (from source)
The mechanisms considered optimize two objectives:

$$\text{FAIR}(D, M(D)) = \text{maximum individual deviation from true outcome}$$

$$\text{SWDIFF}(D, M(D)) = \text{social welfare loss (sum of deviations)}$$

### Lower Bounds over Dataset Family $SPM_\lambda$
For any $\varepsilon$-DP mechanism $M$:

$$\text{FAIR}(D, M(D)) = \Omega\left(\frac{m}{n\varepsilon \ln(1/\beta)} + m\lambda\right) \quad \text{w.p. } \geq \beta$$

$$\text{SWDIFF}(D, M(D)) = \Omega\left(\left(\frac{m}{n\varepsilon^2}\ln(1/\beta)\right)^2 + m\lambda\right) \quad \text{w.p. } \geq \beta$$

where $m$ is a characteristic scale, $n$ is dataset size, and $\lambda$ parameterizes dataset sparsity.

---

## Physical Intuition / Derivation

### Why Differential Privacy Matters

Consider a database of patient medical records. An adversary observing an algorithm's output (e.g., "median treatment cost is $X$") might infer whether a specific person is in the database. Differential privacy prevents such inferences by ensuring the algorithm's output is **statistically similar** regardless of whether any individual's data is included.

### The Privacy-Utility Tradeoff

The source material illustrates a fundamental tension:

1. **Strong privacy** ($\varepsilon \to 0$): Algorithm output becomes nearly independent of individual records → high noise → poor utility
2. **Weak privacy** ($\varepsilon$ large): Algorithm can closely follow true data → low noise → less privacy protection

The theorems show this tradeoff explicitly:
- FAIR error scales as $\Omega(m/(n\varepsilon))$ — inversely proportional to privacy budget
- As $n$ increases, can spread privacy budget across more individuals, reducing per-capita error
- The $\ln(1/\beta)$ factor reflects that low-probability catastrophic failures are acceptable under DP

### Dataset Sparsity and Sensitivity

A key insight from the source: the mechanism's error depends on **dataset geometry**, specifically sparsity around the median:

- **Worst case** ($D_1$): No agents within distance $m$ on one side of median → high sensitivity to perturbations
- **Better case** ($D_2$): Agents uniformly distributed → perturbations have smaller effect

The term $m\lambda$ in lower bounds captures this minimum irreducible error from sparsity; no amount of privacy budget eliminates it.

---

## Applications in Engineering

### 1. **Machine Learning & Data Mining**
- Training algorithms on sensitive datasets (medical, financial) while publishing models or aggregate statistics
- Federated learning: coordinating model updates across distributed devices without centralizing sensitive data
- Example: $\varepsilon$-DP stochastic gradient descent for privacy-preserving neural networks

### 2. **Census and Public Statistics**
- U.S. Census Bureau uses differential privacy (noise infusion) to publish demographic statistics while protecting individual privacy
- Differentially private histograms and contingency tables for public health data

### 3. **Database Systems**
- Differentially private query answering: database systems that respond to queries with noised answers
- Protecting sensitive attributes in microdata release

### 4. **Location Services & Mobility Data**
- GPS-based applications: locating median facility location (as in source) without revealing individual trajectories
- Ride-sharing and navigation services: aggregate traffic patterns without tracking individuals

### 5. **Social Networks & Recommendation Systems**
- Graph algorithms (centrality, community detection) on networks with sensitive edges
- Recommendation systems learning from user data while preserving individual preferences

---

## Common Mistakes / Pitfalls

### 1. **Confusing "Neighboring" Datasets**
**Error**: Thinking $D$ and $D'$ must differ by small amounts, not exactly one record.

**Correction**: Differential privacy specifically considers datasets differing in **one individual's complete record** (or one record addition/removal). This creates worst-case sensitivity.

### 2. **Assuming Privacy is Automatic with Noise**
**Error**: "I'll just add Gaussian noise—that's private."

**Correction**: Need formal guarantees. Random noise alone doesn't prevent inference; the $e^\varepsilon$ bound ensures bounded information leakage, which random noise alone doesn't provide.

### 3. **Misinterpreting the Privacy Budget $\varepsilon$**
**Error**: Believing $\varepsilon = 0.1$ is "10% privacy."

**Correction**: $\varepsilon$ is the privacy loss bound. Smaller $\varepsilon$ is stronger privacy. $\varepsilon = 0.1$ allows $e^{0.1} \approx 1.105$ times probability ratio—very strong. $\varepsilon = 1$ allows $e \approx 2.718$