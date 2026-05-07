# Statistical Query Algorithms

## Definition

A **statistical query (SQ) algorithm** is a computational model that learns from data by making queries to an oracle that returns statistical information about the data distribution, rather than accessing individual samples directly. Formally, an SQ algorithm can only query the data through a statistical oracle that, given a bounded function $\phi: \mathcal{X} \to [-1, 1]$ and error tolerance $\tau > 0$, returns an estimate $\hat{v}$ of $\mathbb{E}[\phi(X)]$ satisfying:

$$|\hat{v} - \mathbb{E}[\phi(X)]| \leq \tau$$

The SQ model is useful for understanding **computational-statistical gaps**: situations where information-theoretic sample complexity differs fundamentally from the sample complexity of polynomial-time algorithms.

## Key Equations

### Mean Estimation
For $\ell_2$-norm error $\rho$, the sample complexity hierarchy is:

$$n_{\text{info-theoretic}} \asymp d e^{1/\rho^2}$$
$$n_{\text{SQ}} \asymp d^{1/\rho^2}$$
$$n_{\text{poly-time}} \asymp d^{1/\rho^2}$$

This reveals a **statistical-computational gap**: information theory permits exponentially fewer samples than what any SQ algorithm (or polynomial-time algorithm) requires.

### Covariance Estimation
For estimating a positive-definite covariance matrix $\Sigma \in \mathbb{C}^{d \times d}_{++}$ under contamination with corruption level $\epsilon$, an SQ algorithm requires:

$$n \gtrsim d^{1/\rho} \text{ samples for relative operator norm error } \rho$$

with the bound:

$$\left\|\Sigma^{-1/2}\hat{\Sigma}\Sigma^{-1/2} - I_d\right\|_{\text{op}} \gtrsim \sqrt{\frac{d + \log(1/\delta)}{n(1-\epsilon)}} + \frac{\log(1/(1-\epsilon))}{\log\left(1 + \frac{\epsilon n}{d + \log(1/\delta)}\right)}$$

### Linear Regression with Missing Data
For linear regression where missingness depends arbitrarily on both response $Y$ and covariates $X$:

$$\hat{\theta} - \theta\|_2 \gtrsim \sigma \cdot \log\left(\frac{1}{1-\epsilon}\right) \sqrt{\log\left(1 + \epsilon^2 \frac{1}{1-\epsilon} \cdot \frac{n}{d + \log(1/\delta)}\right)}$$

Importantly, polynomial-time algorithms nearly achieve this bound (up to $\log\log$ factors), indicating **no statistical-computational gap** in this setting.

## Physical Intuition / Derivation

### Why SQ Algorithms Matter

Consider learning a high-dimensional distribution. Two learning models compete:

1. **Unrestricted learning**: An algorithm with full access to samples—can compute any statistic. Sample complexity $\Omega(d e^{1/\rho^2})$ suffices for mean estimation.

2. **SQ learning**: An algorithm that queries only aggregate statistics (e.g., "what is the mean of this coordinate?", "what is the average product $x_i x_j$?"). Sample complexity $\Omega(d^{1/\rho^2})$.

**Why the gap exists**: To estimate a mean to precision $\rho$ in dimension $d$, an SQ algorithm must estimate $d$ coordinates independently (due to the structure of the oracle). Each coordinate requires $1/\rho^2$ samples. The exponential factor $e^{1/\rho^2}$ in the information-theoretic bound reflects the possibility that unrestricted algorithms can exploit correlations across coordinates.

### Lower Bound Intuition

SQ lower bounds follow from a **parity-cutting principle**: if a function's Fourier coefficients are concentrated on low-influence parities, no SQ algorithm can distinguish it from the uniform distribution using polynomially many queries. This translates to sample complexity lower bounds via information-theoretic reductions.

### Why Linear Regression is Different

In linear regression with missing data, polynomial-time algorithms (based on strongly convex empirical risk minimization) nearly match information-theoretic lower bounds. This occurs because the problem has enough **algebraic structure**: the linear model and convexity allow standard optimization to avoid the curse of SQ queries.

## Applications in Engineering

### 1. **Robust Machine Learning and Contamination Tolerance**
When datasets contain unknown corruptions (Byzantine attacks, outliers), SQ algorithms provide certified learning guarantees. The covariance estimation framework applies to:
- **Robust PCA**: Recovering low-rank structure despite contaminated observations
- **Defensive ML**: Quantifying how many samples suffice to learn when an adversary corrupts an $\epsilon$ fraction

### 2. **Sample Complexity Analysis in High-Dimensional Statistics**
SQ lower bounds guide algorithm design:
- Determines whether observed computational bottlenecks are fundamental or algorithmic
- Informs whether to invest in better algorithms or accept exponential sample complexity
- Applies to: sparse recovery, community detection, clustering under contamination

### 3. **Missing Data Imputation**
In real-world datasets with missing observations:
- Medical records with incomplete measurements (MCAR/MAR)
- Sensor networks with dropped readings
- The SQ framework shows that when missingness depends on both features and response, polynomial-time algorithms suffice—no exponential sample blow-up required

### 4. **Distributed and Private Learning**
SQ algorithms naturally model:
- **Differential privacy**: A privatized data release mechanism is similar to an SQ oracle with limited sensitivity
- **Federated learning**: Aggregating statistics across agents without sharing raw data

## Common Mistakes / Pitfalls

### 1. **Conflating SQ Lower Bounds with Computational Hardness**
**Wrong**: "SQ lower bound $\Rightarrow$ problem is hard."
**Right**: SQ lower bounds show that *a specific algorithmic class* (SQ algorithms) is weak. Unrestricted polynomial-time algorithms may exist (though often