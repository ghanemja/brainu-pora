# Relative Error Estimation

## Definition

**Relative error estimation** is a quantitative measure of the accuracy of an approximate or estimated value compared to a true or reference value, expressed as a fraction or percentage of the reference value. In algorithmic and experimental contexts, it quantifies how far an estimate deviates from ground truth, normalized by the magnitude of the quantity being estimated.

Formally, for an estimated value $\hat{x}$ and true value $x$:

$$\text{Relative Error} = \frac{|\hat{x} - x|}{|x|}$$

When expressed as a percentage:

$$\text{Relative Error (\%)} = \frac{|\hat{x} - x|}{|x|} \times 100\%$$

In statistical contexts with repeated measurements or sampling, relative error is often characterized through **confidence intervals** (e.g., 90% CI) to capture the distribution of errors across multiple trials.

---

## Key Equations

**Point estimate:**
$$RE = \frac{|\hat{x} - x|}{|x|}$$

**Confidence interval bounds:**
For a set of $n$ independent estimate samples $\{\hat{x}_1, \hat{x}_2, \ldots, \hat{x}_n\}$, the empirical $100(1-\alpha)\%$ confidence interval for relative error is:
$$\left[\min_i RE_i, \max_i RE_i\right]$$
or using quantiles:
$$\left[RE_{\alpha/2}, RE_{1-\alpha/2}\right]$$

**Acceptable termination criterion (sampling-based algorithms):**
A common auto-termination strategy stops sampling when the change in estimate falls below a threshold $\epsilon$:
$$\left|\hat{x}_{k} - \hat{x}_{k-1}\right| < \epsilon \cdot |x_k|$$
where $\epsilon$ is the relative change tolerance (e.g., 0.02 for 2%).

---

## Physical Intuition / Derivation

### Why Relative Error Matters

Absolute error alone is often misleading. Consider:
- Estimating a distance of 1 km with error of 1 m: absolute error is large, but relative error is $10^{-3}$ (negligible)
- Estimating a microscopic measurement of 1 μm with error of 1 nm: absolute error seems small, but relative error is $10^{-3}$ (significant)

Relative error **normalizes** by the scale of the quantity, making it dimensionless and comparable across different problem sizes and domains.

### Distribution Perspective

In sampling-based algorithms (Monte Carlo, graph sampling, etc.), estimates are random variables. Instead of single point estimates, practitioners:
1. **Run multiple trials** to build an estimate distribution
2. **Extract statistics**: mean, confidence intervals, min/max bounds
3. **Report ranges** (e.g., "90% confidence interval") rather than point estimates

This acknowledges the inherent variance in stochastic algorithms and provides decision-makers with risk bounds.

### Auto-Termination Strategy

For iterative sampling algorithms, two thresholds are commonly used:

- **Inner loop termination**: Stop when a batch of new samples contributes less than threshold $\epsilon_{\text{inner}}$ (e.g., 2%) to the estimate
- **Outer loop termination**: Stop when successive iterations change the overall estimate by less than $\epsilon_{\text{outer}}$ (e.g., 0.2%)

This balances computational cost against accuracy improvement: marginal gains in relative error don't justify further computation.

---

## Applications in Engineering

### 1. **Numerical Simulation & Scientific Computing**
- Assessing finite element method (FEM) accuracy for structural analysis
- Evaluating convergence of iterative solvers (e.g., GMRES, CG) by monitoring relative error in residuals
- **Example**: FEM stress estimation with target relative error < 5%

### 2. **Graph & Network Algorithms**
- Estimating properties on massive graphs (node counts, edge weights, centrality measures) via sampling
- **Motivation**: Computing exact values is infeasible; sampling provides fast approximate answers with quantified error bounds
- **Example** (from source): TLS algorithm achieved 435× speedup over exact methods while maintaining 90% CI relative errors

### 3. **Machine Learning & Optimization**
- Evaluating model predictions: relative error in regression problems
- Early stopping in iterative optimization when relative improvement drops below threshold
- Importance weighting in variance reduction techniques

### 4. **Signal Processing & Measurement Systems**
- Quantifying sensor accuracy independent of signal magnitude
- Comparing filters or estimators across different signal ranges
- Tolerance specifications in analog-to-digital conversion

### 5. **Experimental Design & Data Collection**
- Setting sample sizes to achieve target relative error confidence intervals
- Power analysis: determining rounds needed to discriminate between methods
- Quality control: accepting/rejecting batches based on relative error metrics

---

## Common Mistakes / Pitfalls

### 1. **Confusing Absolute and Relative Error**
**Mistake**: Reporting only absolute error when magnitudes vary widely.
**Fix**: Always report relative error in comparative studies; use absolute error only for same-scale quantities.

### 2. **Neglecting Estimate Variance**
**Mistake**: Reporting point estimates from stochastic algorithms without confidence intervals.
**Fix**: Run multiple independent trials; report confidence intervals (e.g., 90% CI) and min/max bounds, not just means.

### 3. **Misinterpreting Confidence Intervals**
**Mistake**: Believing "90% CI" means "90% probability the true value is in this interval" (frequentist misinterpretation).
**Correct interpretation**: "If we repeated the experiment many times, ~90% of computed intervals would contain the true value."

### 4. **Ignoring Relative Error Near Zero**
**Mistake**: Computing $RE = \frac{|\hat{x} - x|}{|x|}$ when $x \approx 0$ leads to division by near-zero.
**Fix**: Use alternative metrics (absolute error, normalized error with problem-dependent denominator) or shift variables away from zero.

### 5. **Setting Termination Thresholds Too Aggressively**
**Mistake**: Using very loose thresholds (e.g., 10% change