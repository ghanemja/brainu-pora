# Automatic Termination Strategy

## Definition

An **automatic termination strategy** is a computational stopping criterion that halts iterative sampling or approximation algorithms when the marginal improvement in estimate quality falls below a predefined threshold, rather than fixing the number of iterations a priori. This adaptive approach reduces computational cost while maintaining solution quality by monitoring convergence in real time.

In the context of sampling-based algorithms, termination occurs when consecutive batches of samples contribute negligently small changes to the current estimate, eliminating wasteful over-sampling.

## Key Equations

For an iterative algorithm producing estimates $\hat{E}_i$ at iteration $i$, the automatic termination condition is:

$$\left| \frac{\hat{E}_{i} - \hat{E}_{i-1}}{\hat{E}_{i-1}} \right| < \epsilon$$

where $\epsilon$ is a relative error threshold (e.g., $\epsilon = 0.02$ for 2% change, or $\epsilon = 0.002$ for 0.2% change).

**Batch-wise formulation:** When sampling in batches of size $b$:

$$\text{Terminate if} \quad \left| \frac{\hat{E}_{i} - \hat{E}_{i-1}}{\hat{E}_{i-1}} \right| < \epsilon_{\text{inner}}$$

where $\epsilon_{\text{inner}}$ controls inner loop convergence (e.g., 2%), and separately apply a coarser threshold $\epsilon_{\text{outer}}$ (e.g., 0.2%) for outer iteration termination.

## Physical Intuition / Derivation

### Why Fixed Iteration Counts Are Wasteful

Traditional iterative algorithms require the user to specify iteration count $r$ a priori. This creates a dilemma:
- **Too small $r$**: Insufficient convergence; high relative error
- **Too large $r$**: Wasted computation on already-converged estimates

The key insight is that **information gain is non-uniform across iterations**—early iterations typically produce large improvements, while later iterations yield diminishing returns following a roughly linear or sublinear decay pattern (as noted in the source material: "relative errors of WPS decrease nearly linearly in the initial ten seconds").

### Automatic Termination Rationale

By monitoring the *fractional change* in the estimate after each batch, the algorithm automatically detects the "elbow point" where marginal improvements become negligible. This is a form of **convergence detection** that adapts to the problem instance and dataset characteristics.

**Why percentage-based thresholds?** Relative error (not absolute error) is dimensionless and scale-invariant, making the strategy applicable across different problem scales.

### Nested Termination (Inner and Outer Loops)

The two-level termination structure is common in nested sampling:
- **Inner termination ($\epsilon_{\text{inner}} = 2\%$)**: Refinement within each outer iteration stops when local convergence is reached
- **Outer termination ($\epsilon_{\text{outer}} = 0.2\%$)**: Higher precision (stricter threshold) for the overall algorithm, ensuring global solution quality

This hierarchy reflects: coarse inner decisions feed into a stricter outer budget, balancing efficiency and accuracy.

## Applications in Engineering

### 1. **Graph Analytics & Network Analysis**
The source material demonstrates application to **edge sampling in large graphs** (the TLS algorithm):
- Computing graph statistics (clustering coefficients, triangles) via adaptive sampling
- Terminating when edge subset contributions stabilize
- Achieved **85–95% query reduction** vs. fixed-budget methods

### 2. **Monte Carlo Simulations**
- **Structural reliability analysis**: Stop sampling when failure probability estimates stabilize
- **Uncertainty quantification**: Terminate when confidence intervals narrow below a tolerance
- **Material property estimation**: Halt statistical sampling when coefficient estimates converge

### 3. **Machine Learning Model Tuning**
- **Hyperparameter search**: Stop exploring when validation metric improvements plateau
- **Cross-validation**: Early stopping when fold-level metrics stabilize
- **Ensemble methods**: Terminate boosting rounds when out-of-bag error saturates

### 4. **Scientific Computing & Numerical Methods**
- **Iterative linear solvers**: Stop when residual norm $\|\mathbf{r}_i\| < \epsilon \|\mathbf{r}_0\|$
- **Stochastic gradient descent**: Terminate training when loss plateau is detected over moving window
- **Finite element refinement**: Adaptively stop mesh refinement when error estimate stagnates

### 5. **Quality Control & Testing**
- **Defect sampling**: In manufacturing, stop inspection when defect rate estimates converge
- **Compliance testing**: Terminate test runs when failure modes are exhausted or probabilities stabilize

## Common Mistakes / Pitfalls

### 1. **Choosing Thresholds Without Problem Context**
- **Mistake**: Using the same $\epsilon$ for all problems (e.g., always 0.2%)
- **Reality**: Threshold should reflect acceptable precision for the application. A 0.2% improvement on a 0.001-magnitude estimate has different significance than on a 1000-magnitude estimate
- **Fix**: Scale thresholds based on problem-specific accuracy requirements and baseline variance

### 2. **Confusing Absolute vs. Relative Change**
- **Mistake**: Stopping when absolute change $|\hat{E}_i - \hat{E}_{i-1}| < \delta$ is small
- **Problem**: For small estimates, this may truncate too early; for large estimates, it may not terminate
- **Fix**: Always use relative change: $\left|\frac{\hat{E}_i - \hat{E}_{i-1}}{\hat{E}_{i-1}}\right|$

### 3. **Ignoring Noise in Small Samples**
- **Mistake**: Terminating on a single batch showing <2% change, when the next batch might show 10% change
- **Reality**: Early batches have high variance; temporary plateaus can occur randomly
- **Fix**: Use moving averages or require multiple consecutive sub-threshold batches before terminating

### 4. **Over-Aggressive Inner Loop Termination**
- **Mistake**: Setting $\epsilon_{\text{inner}}$ too tightly, causing insufficient refinement per outer iteration
- **Consequence**: Many outer iterations with