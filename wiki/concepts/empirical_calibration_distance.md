# empirical calibration distance

## Definition

The **empirical calibration distance** is a sample-based estimator of the *distance from calibration*, which measures how far a probabilistic predictor is from perfect calibration. Specifically:

- **True calibration distance**: Given a data distribution $\mathcal{D}$ over $(X, Y)$ pairs and a predictor $\hat{p}: X \to [0,1]$, the calibration distance is the minimum $\ell_1$ distance (in the marginal distribution) to a perfectly calibrated predictor:

$$\text{CalDist}(\hat{p}, \mathcal{D}) = \min_{\hat{q} \text{ calibrated}} \mathbb{E}_{X \sim \mathcal{D}}[|\hat{p}(X) - \hat{q}(X)|]$$

- **Empirical calibration distance**: Given a finite sample $S = \{(x_1, y_1), \ldots, (x_n, y_n)\}$ drawn from $\mathcal{D}$, the empirical version estimates this quantity using the sample:

$$\widehat{\text{CalDist}}(\hat{p}, S) = \min_{\hat{q} \text{ calibrated on } S} \frac{1}{n}\sum_{i=1}^n |\hat{p}(x_i) - \hat{q}(x_i)|$$

A predictor is **perfectly calibrated** if for all $\alpha \in [0,1]$:
$$\mathbb{P}(Y = 1 \mid \hat{p}(X) = \alpha) = \alpha$$

## Key Equations

**Sample complexity bound**: The empirical calibration distance requires $\Theta(1/\varepsilon^3)$ samples to achieve one-sided estimation (upper bound within $\varepsilon$):

$$\mathbb{P}(\widehat{\text{CalDist}}(\hat{p}, S) \leq \text{CalDist}(\hat{p}, \mathcal{D}) + \varepsilon) \geq 2/3$$

**Two-sided estimation** (both upper and lower bounds) requires polynomial dependence on domain size $|X|$, making it fundamentally harder than one-sided estimation.

**Computational complexity**:
- Tractable: uniform marginal + noiseless labels → polynomial time
- Intractable: general distribution or noisy labels → NP-hard
- Approximable: PTAS (polynomial-time approximation scheme) for general case

## Physical Intuition / Derivation

### Why Calibration Distance?

The calibration distance addresses a fundamental limitation in binary calibration measures: there is no consensus on what "miscalibration" means. Consider two perspectives:

1. **Perfect calibration** is unattainable in practice from finite samples
2. **Existing measures** (e.g., expected calibration error, Brier score) don't directly measure "how far" a predictor is from being calibrated

The calibration distance reframes this: instead of asking *"Is the predictor calibrated?"*, ask *"What is the minimum adjustment needed to make it calibrated?"*

### Geometric Interpretation

In the space of all predictors, calibrated predictors form a submanifold (the set of valid conditional probability functions). The calibration distance is:
- The orthogonal projection onto this manifold in the $\ell_1$ metric (weighted by marginal distribution)
- Invariant to label noise in certain restricted settings (noiseless case)
- Scale-dependent: measured in probability difference units

### Why $\Theta(1/\varepsilon^3)$ Sample Complexity?

The cubic scaling arises from:
1. **Variance concentration**: Estimating distances to a set of functions (not a single function) → superlinear dependence
2. **Search space size**: Valid calibrated predictors form a lower-dimensional manifold; sparsification reduces this effectively to a discrete finite set
3. **Bias-variance tradeoff**: Tighter control requires tracking the entire quantile distribution of predicted probabilities

## Applications in Engineering

### Machine Learning and AI
- **Model validation**: Diagnose miscalibration in neural networks, ensemble methods, and probabilistic classifiers
- **Model selection**: Compare competing architectures or hyperparameters beyond accuracy
- **Uncertainty quantification**: Verify that confidence scores in safety-critical systems (medical diagnosis, autonomous driving) reflect true likelihood

### Weather and Climate Forecasting
- **Forecast reliability**: Assess whether weather systems reporting "90% chance of rain" are truly reliable
- **Ensemble evaluation**: Compare different ensemble prediction systems (e.g., ECMWF vs. GFS) on calibration
- **Historical benchmarking**: Measure improvement in forecast calibration over time

### Financial Risk Management
- **Probability estimates**: Verify that VaR/CVaR models correctly estimate tail probabilities
- **Credit scoring**: Ensure default probability predictions match observed default rates
- **Trading algorithms**: Detect when price prediction systems are overconfident

### Medical and Clinical Diagnostics
- **Risk assessment models**: Validate that patient risk scores are well-calibrated across populations
- **Fairness auditing**: Detect differential calibration across demographic groups (high miscalibration distance can indicate bias)
- **Clinical decision support**: Ensure confidence in diagnostic predictions matches clinical outcomes

## Common Mistakes / Pitfalls

### 1. **Confusing calibration distance with calibration error**
- **Mistake**: Thinking $\text{CalDist} = \text{ECE}$ (Expected Calibration Error)
- **Reality**: CalDist measures distance to the *feasible set*; ECE measures empirical discrepancy. CalDist $\leq$ ECE always.

### 2. **Ignoring computational hardness**
- **Mistake**: Assuming the empirical calibration distance is easy to compute for any distribution
- **Reality**: Computing it is NP-hard for non-uniform marginals or noisy labels. Must use PTAS or restrict to special cases.

### 3. **Underestimating sample requirements**
- **Mistake**: Using too few samples (~100-1000) and assuming concentration
- **Reality**: Need $\Theta(1/\varepsilon^3)$ samples—for $\varepsilon = 0.01$