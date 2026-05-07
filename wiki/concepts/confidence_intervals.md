# Confidence Intervals

## Definition

A **confidence interval (CI)** is a range of values $[L, U]$ constructed from sample data that is intended to contain an unknown population parameter with a specified probability, called the **confidence level**. 

For a parameter $\theta$ and confidence level $\alpha$ (commonly 90%, 95%, or 99%), a $100(1-\alpha)\%$ confidence interval means:

$$P(L \leq \theta \leq U) = 1 - \alpha$$

This does **not** mean there is a $(1-\alpha) \times 100\%$ probability that $\theta$ lies in any particular realized interval $[l, u]$—rather, if we repeated the sampling procedure many times, approximately $100(1-\alpha)\%$ of the constructed intervals would contain the true parameter.

In engineering contexts, confidence intervals quantify **uncertainty in estimates** derived from limited observations or simulations, providing a principled way to communicate the precision and reliability of measurements or algorithmic results.

## Key Equations

### Standard Normal Case (Large Samples)

For an estimator $\hat{\theta}$ with approximately normal distribution:

$$\text{CI} = \hat{\theta} \pm z_{\alpha/2} \cdot \text{SE}(\hat{\theta})$$

where $z_{\alpha/2}$ is the critical value from the standard normal distribution and $\text{SE}(\hat{\theta})$ is the standard error.

### Student's t-Distribution (Small Samples)

When the population standard deviation is unknown and sample size is small ($n < 30$):

$$\text{CI} = \bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$

where $t_{\alpha/2, n-1}$ is the critical value from the t-distribution with $n-1$ degrees of freedom.

### Relative Error Bounds

In engineering, confidence intervals are often expressed as relative errors around an estimate $\hat{\theta}$:

$$\text{Relative Error} = \frac{\theta - \hat{\theta}}{\theta}$$

The confidence interval for relative error quantifies how far the estimate may deviate from the true value as a percentage.

## Physical Intuition / Derivation

### Why Confidence Intervals Matter

Consider measuring a quantity repeatedly (or simulating an algorithm multiple times). Each measurement or run produces a slightly different result due to **noise, sampling variation, or stochastic algorithms**. A single point estimate $\hat{\theta}$ provides no information about its reliability.

A confidence interval addresses this by saying: *"Based on this data, I'm $(1-\alpha) \times 100\%$ confident the true value lies between $L$ and $U$."*

### Frequentist Interpretation

The confidence level $1-\alpha$ reflects the **long-run frequency**: if you constructed confidence intervals from many independent samples, the fraction containing the true parameter would approach $1-\alpha$.

**Key insight**: The interval is random (depends on data), but the parameter is fixed. We don't assign probability to the parameter being in a particular interval.

### Relationship to Margin of Error

The **margin of error** is the half-width of the confidence interval:

$$\text{ME} = z_{\alpha/2} \cdot \text{SE}(\hat{\theta})$$

Wider intervals reflect greater uncertainty; narrower intervals reflect more precise estimates (achieved through larger sample sizes or lower variability).

## Applications in Engineering

### 1. **Algorithm Performance Analysis**

In the source material, confidence intervals (specifically 90% CIs) quantify the reliability of algorithmic estimates:
- Box plots with confidence intervals visualize estimate distributions across multiple runs
- Engineers compare algorithms not just on mean performance, but on the **range of plausible outcomes**
- Example: If two algorithms have overlapping 90% confidence intervals, the difference may not be statistically significant

### 2. **Experimental Measurements**

Confidence intervals are standard in:
- **Materials testing**: Tensile strength, fatigue life, failure modes
- **Sensor calibration**: Measurement precision and bias
- **Environmental monitoring**: Pollutant concentrations, temperature variations

### 3. **Sampling-Based Estimation**

When exact computation is infeasible (as in graph algorithms, Monte Carlo methods):
- Sample a subset of the domain
- Construct confidence intervals around estimates
- Use CI width to determine if more samples are needed

**Example from source**: The TLS algorithm uses automatic termination based on how much recent batches change the estimate (inner rounds stop when estimate change < 2%, outer rounds < 0.2%), equivalent to confidence-interval-based stopping criteria.

### 4. **Quality Control & Manufacturing**

Confidence intervals define **tolerance ranges** and **statistical process control** limits:
- Specification limits: Does a process stay within acceptable bounds?
- Control charts: Are observed variations within expected confidence bounds?

### 5. **Simulation & Computational Studies**

For stochastic simulations (Monte Carlo, agent-based models):
- Run multiple independent replications
- Construct CIs around performance metrics
- Determine required number of replications for target precision

## Common Mistakes / Pitfalls

### 1. **Misinterpreting the Confidence Level**

❌ **Wrong**: "There is a 90% probability the parameter lies in this interval."

✓ **Correct**: "If we repeated the experiment many times, 90% of such intervals would contain the parameter."

The parameter is fixed; probability refers to the procedure, not the specific realized interval.

### 2. **Confusing Confidence Intervals with Credible Intervals**

- **CI (frequentist)**: Based on repeated sampling behavior
- **Credible interval (Bayesian)**: Represents posterior probability; does allow statements like "90% probability parameter is in [L, U]"

### 3. **Using Wrong Standard Error**

- For sample mean: $\text{SE} = s / \sqrt{n}$ (not $s$ itself)
- For proportions: $\text{SE} = \sqrt{p(1-p)/n}$
- For differences: $\text{SE}$ combines variances of both groups

### 4. **Assuming Symmetry**

Not all sampling distributions are symmetric. For skewed data or small samples:
- Use **bootstrap methods** or **permutation tests** instead of normal approximation
- Consider **non-paramet