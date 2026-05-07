# Calibration

## Definition

**Calibration** is a property of a predictor (or classifier) that measures how well the predicted confidence or probability values align with actual empirical frequencies. Formally, a predictor $f: X \to [0,1]$ is calibrated with respect to a distribution $D$ over input-output pairs if, for all predicted values $p \in [0,1]$, the empirical frequency of positive outcomes among instances where $f$ predicts $p$ equals (or is very close to) $p$.

The **calibration distance** $\text{CalDist}_D(f)$ quantifies how far a given predictor deviates from perfect calibration. It represents the minimum "work" required to transform predictor $f$ into a perfectly calibrated predictor while preserving its predictions on the underlying distribution.

## Key Equations

The calibration distance can be computed via dynamic programming when the support $X$ has structure:

$$\text{CalDist}_D(f) = \min_{g \in C(D)} d(f, g)$$

where $C(D)$ is the set of all perfectly calibrated predictors and $d(f,g)$ is a distance metric (typically total variation or Wasserstein distance).

For discrete supports with **type-sparsity** (at most $k$ distinct types of indistinguishable elements):

$$\text{opt}(m_0, m_1, \ldots, m_k) = \min \left\{ \text{cost}_{\text{partition}} : \text{contiguous partition of first } m_i \text{ elements of type } i \right\}$$

The recursion enumerates $O(|X|^{2k})$ subproblems, each solvable in polynomial time.

## Physical Intuition / Derivation

### Why Calibration Matters

A weather forecast predicting "60% chance of rain" is calibrated if, over all days when such predictions are issued, it rains on approximately 60% of them. A miscalibrated system might predict 60% but experience only 30% rainfall—overconfident predictions erode user trust and lead to poor downstream decisions.

### The Indistinguishability Insight

The key algorithmic observation is that **indistinguishable elements can be permuted without changing calibration**. Two inputs $x_1, x_2$ are indistinguishable if:
- They have identical label distribution: $D_x(x_1) = D_x(x_2)$
- They induce identical marginal predictions: $\mu_D(x_1) = \mu_D(x_2)$

This means the optimal recalibration problem has **inherent symmetry**: rather than considering all $|X|!$ permutations, we can work with contiguous partitions of types, reducing the state space from exponential to polynomial (or quasi-polynomial with approximation).

### Type-Sparsity Reduction

When a distribution $D$ has only $k$ types, we restrict attention to **type-monotone predictors** that preserve order within each type. This maintains calibration while dramatically reducing the search space:

- **Exact algorithm**: $O(|X|^{2k})$ time (polynomial for constant $k$)
- **Approximation**: Replace $D$ with an $\varepsilon$-close type-sparse surrogate
  - Uniform $X$-marginal: $O(1/\varepsilon)$ types → runtime $|X|^{O(1/\varepsilon)}$ (QPTAS)
  - General marginal: $O(\log(|X|/\varepsilon)/\varepsilon^2)$ types → runtime $|X|^{O(\log(|X|/\varepsilon)/\varepsilon^2)}$ (QPTAS)

### Prediction-Sparsity and PTAS

For fully general cases, a different sparsification exploits the range of a calibrated witness predictor $g$. By partitioning $[0,1]$ into $O(1/\varepsilon)$ intervals and quantizing predictions within each interval, one can construct a PTAS (polynomial-time approximation scheme) that:
1. Maintains perfect calibration
2. Preserves distance from $f$ up to error $\varepsilon$
3. Runs in time polynomial in $|X|$ and $1/\varepsilon$

## Applications in Engineering

### Machine Learning & Model Validation
- **Medical diagnosis**: A 95% confidence score should be correct 95% of the time to guide clinical decisions safely
- **Autonomous vehicles**: Reliability estimates must be calibrated so downstream safety systems can trust uncertainty quantification
- **Recommendation systems**: User satisfaction models must calibrate predicted satisfaction probabilities to avoid systematic over/under-promising

### Signal Processing & Control
- **Sensor fusion**: Confidence levels attached to fused measurements must reflect true error distributions
- **Adaptive filters**: Uncertainty estimates guide step-size adaptation; miscalibration destabilizes feedback

### Risk & Finance
- **Credit scoring**: A model assigning 5% default probability must match actual default rates in that risk bucket
- **Portfolio optimization**: Volatility estimates and correlation calibration directly impact hedge ratios and position sizing

### Manufacturing & Quality Control
- **Defect detection**: Confidence in defect presence should align with true defect rates for optimal stopping/inspection policies
- **Process monitoring**: Alarm thresholds calibrated to prediction confidence minimize false positives/negatives

## Common Mistakes / Pitfalls

1. **Confusing accuracy with calibration**: A classifier can be highly accurate but poorly calibrated. Example: a model that predicts $\{0.0, 1.0\}$ with 90% accuracy may assign 1.0 to instances with 60% true positive rate.

2. **Ignoring label distribution drift**: Calibration is distribution-dependent. A model calibrated on historical data may become miscalibrated when the true label distribution shifts.

3. **Over-fitting calibration to finite test sets**: Empirical calibration on small samples exhibits high variance; this is why the algorithmic reduction to sparse representations is essential.

4. **Misapplying isotonic regression or temperature scaling blindly**: These post-hoc recalibration methods assume the predictor's ranking is appropriate; they fail if the relative ordering of confidence scores is fundamentally wrong.

5. **Forgetting the cost of recalibration