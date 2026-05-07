# Differential Privacy

## Definition

**Differential privacy** is a mathematical framework for quantifying and guaranteeing privacy protection when analyzing sensitive datasets. An algorithm $\mathcal{A}$ is $(\varepsilon, \delta)$-differentially private if, for any two neighboring datasets $D$ and $D'$ that differ in a single individual's record, and for any possible output set $S$:

$$\mathbb{P}[\mathcal{A}(D) \in S] \leq e^{\varepsilon} \cdot \mathbb{P}[\mathcal{A}(D') \in S] + \delta$$

**Intuition of parameters:**
- $\varepsilon$ (epsilon): Controls the *privacy loss* through multiplicative slack. Smaller $\varepsilon$ means stronger privacy guarantees. Typical values: $\varepsilon \in [0.1, 10]$ depending on sensitivity.
- $\delta$ (delta): Allows for a small probability $\delta$ of complete privacy failure. Should be negligible (e.g., $\delta < 1/n$ where $n$ is dataset size).
- **Perfect privacy** ($\varepsilon = 0, \delta = 0$): Output is independent of any individual's data.

## Key Equations

### Basic Definition (Probability Form)
For neighboring datasets $D \sim D'$:
$$\frac{\mathbb{P}[\mathcal{A}(D) = o]}{\mathbb{P}[\mathcal{A}(D') = o]} \leq e^{\varepsilon}$$

### Laplace Mechanism
To release a real-valued query $f(D)$ with sensitivity $\Delta f$ (max change when one record changes):
$$\mathcal{A}(D) = f(D) + \text{Laplace}(0, \Delta f / \varepsilon)$$
Achieves $\varepsilon$-differential privacy.

### Composition (Advanced)
Given $k$ algorithms each $(\varepsilon_i, \delta_i)$-differentially private, their sequential composition is:
- **Basic composition**: $(k\varepsilon, k\delta)$-differentially private
- **Advanced composition** (from source): $\left(\sqrt{2k\ln(1/\delta')}\cdot\varepsilon + k\varepsilon(e^{\varepsilon}-1), \delta + k\delta'\right)$-differentially private for any $\delta' > 0$

The source material achieves composition of perfectly generalizing algorithms with parameters where:
$$\varepsilon^* \approx \sqrt{\sum_{i} \varepsilon_i^2}, \quad \delta^* = O\left(\delta \cdot \text{polylog}(n)\right)$$

### Replicability and Composition (From Source)
For $k$ problems with sample complexities $n_1, \ldots, n_k$, joint replicable solution requires:
$$n_{\text{total}} = \tilde{O}\left(\sum_{i=1}^{k} n_i\right) \text{ samples}$$
maintaining constant replicability $\rho$, versus naive $\tilde{O}(nk^2)$ bound.

## Physical Intuition / Derivation

### Why Differential Privacy Matters

Consider releasing the average salary from a dataset. Without privacy protection, an adversary could:
1. Ask for the average with employee X included
2. Ask for the average without X  
3. Subtract to infer X's salary (or whether X is in dataset)

Differential privacy prevents this by adding carefully calibrated randomness so that changing one record produces statistically indistinguishable outputs.

### The Mechanism: Laplace Mechanism Walkthrough

To release query result $f(D)$ where sensitivity $\Delta f = \max_{D \sim D'} |f(D) - f(D')|$ is 1 (e.g., counting queries):

1. **Sensitivity analysis**: Determine how much output can change with one record's modification
2. **Noise scaling**: Add noise proportional to sensitivity and inverse to privacy budget
3. **Trade-off**: Larger noise → stronger privacy ($\varepsilon$ decreased) but worse utility

For $\varepsilon = 1$: noise scale = $\Delta f / 1 = 1$, giving reasonable privacy-utility trade-off.

### Composition: The Core Challenge

Running multiple analyses on same dataset compounds privacy loss:
- After $k$ independent releases with privacy budget $\varepsilon$ each, total privacy loss ≈ $k\varepsilon$
- This linear scaling becomes prohibitive for large $k$ (many questions on same data)

The source material's key insight: By converting replicable algorithms to *perfectly generalizing* ones (which depend only on training data distribution, not specific samples), composition becomes a privacy analysis problem with tighter $\sqrt{\sum \varepsilon_i^2}$ scaling rather than $\sum \varepsilon_i$ scaling.

## Applications in Engineering

### 1. **Census and Government Statistics**
- U.S. Census Bureau released 2020 Census data with differential privacy
- Protects individual household information while enabling valid aggregate statistics
- Allows researchers to analyze demographic trends without privacy risks

### 2. **Machine Learning & Federated Learning**
- **Differentially private SGD (DP-SGD)**: Train neural networks with privacy guarantees
- **Federated learning**: Each device trains locally, central server aggregates with privacy noise
- Applications: Keyboard prediction (Google), on-device model improvement (Apple)

### 3. **Medical Data Analysis**
- Hospitals can release anonymized patient records with formal privacy guarantees (not ad hoc k-anonymity)
- Enables discovery of side effects and treatment efficacy without HIPAA violations
- Pharmaceutical companies analyze adverse event reports

### 4. **Database Systems**
- Query engines that answer questions on sensitive data (e.g., healthcare records, financial transactions)
- Prevents inference attacks through query combinations
- PostgreSQL extension: PostgreSQL with differential privacy via PyDP

### 5. **Web Analytics & Recommendation Systems**
- Apple's Local Differential Privacy: collects emoji usage statistics on-device with privacy guarantee
- Browser-collected statistics on visited URLs/page features
- No centralized server