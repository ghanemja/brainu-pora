# Sensitivity Analysis

## Definition

**Sensitivity analysis** is a computational and analytical technique that quantifies how changes in input parameters affect the output or performance metrics of a system, algorithm, or model. It measures the responsiveness of system behavior to perturbations in design choices, configuration parameters, or input variables.

Formally, the sensitivity of an output $Y$ to a parameter $p$ can be expressed as:

$$S_p = \frac{\partial Y}{\partial p} \quad \text{or} \quad S_p = \frac{\Delta Y / Y}{\Delta p / p}$$

where the first form represents local (derivative-based) sensitivity and the second represents normalized or elasticity-based sensitivity.

## Key Equations

### Local Sensitivity (Infinitesimal Perturbations)
$$\frac{\partial Y}{\partial p}\bigg|_{p=p_0}$$

Measures instantaneous rate of change of output with respect to parameter.

### Normalized Sensitivity (Dimensionless)
$$S_p^{\text{norm}} = \frac{p_0}{Y_0} \frac{\partial Y}{\partial p}\bigg|_{p=p_0}$$

Makes sensitivity independent of scale and units, enabling comparison across different parameters.

### Perturbation-Based Sensitivity Ratio
$$\text{Sensitivity Ratio} = \frac{Y(p \cdot \lambda)}{Y(p_0)}$$

Used empirically to test robustness over a range $\lambda \in [a, b]$ relative to nominal value $p_0$. Common approach: vary parameter from $0.5p_0$ to $1.5p_0$ and measure performance degradation.

## Physical Intuition / Derivation

### Why Sensitivity Analysis Matters

A well-designed system should be **robust**—it should maintain acceptable performance even when parameters deviate from their nominal (ideal) values. Sensitivity analysis answers:

1. **Which parameters matter most?** Not all parameters affect output equally.
2. **How much can we deviate?** What is the allowable tolerance?
3. **Is our choice near an optimum?** If small perturbations cause large output changes, we may be near a boundary or unstable region.

### Example from Source Material

In the HyperMotivo algorithm context, researchers tested sensitivity to parameter $\alpha^*$ by evaluating the ratio:

$$\frac{T(\alpha)}{T(\alpha^*)}$$

where $T(\alpha)$ is the preprocessing time using parameter value $\alpha$. By varying $\alpha$ from $0.5\alpha^*$ to $1.5\alpha^*$ and observing that the time ratio stays near 1.0 (Figure 4), they demonstrated:

- **Robustness**: The algorithm is stable across a 3× parameter range
- **Safe Design Choice**: $\alpha^*$ was not finely-tuned but still performed well, suggesting the solution lies in a flat region of the parameter space rather than a sharp optimum
- **Practical Validation**: No need for expensive hyperparameter tuning

## Applications in Engineering

### Algorithm Design & Optimization
- **Parameter tuning**: Verify that chosen hyperparameters yield stable performance
- **Worst-case analysis**: Identify failure modes when parameters drift
- **Trade-off analysis**: Compare sensitivity of competing algorithms (e.g., HyperMotivo vs. naive Algorithm 1 in computational complexity)

### Systems Engineering
- **Tolerancing**: Set manufacturing tolerances based on how sensitive system performance is to dimensional variations
- **Robustness validation**: Confirm designs work across operational temperature ranges, material property variations, aging effects
- **Failure mode identification**: Detect which parameters, if perturbed, would cause unacceptable degradation

### Control Systems
- **Stability margins**: Analyze how sensitive closed-loop stability is to controller gains
- **Model uncertainty**: Quantify robustness to errors in plant model parameters

### Numerical Computing
- **Step-size selection**: Verify integrators, optimizers behave stably across a range of step sizes
- **Convergence criteria**: Ensure tolerance parameters don't cause numerical instability or excessive computation

### Finance & Operations Research
- **Risk assessment**: Sensitivity of portfolio returns to interest rates, volatility
- **Break-even analysis**: How much demand must change to affect profitability

## Common Mistakes / Pitfalls

### 1. **One-at-a-time (OAT) Sensitivity Only**
Varying one parameter while holding others fixed misses **parameter interactions**. If $Y = p_1 \cdot p_2$, varying only $p_1$ ignores how the effect depends on $p_2$.

**Better approach**: Use multivariate or global sensitivity analysis (e.g., Sobol indices, Morris screening) for complex systems.

### 2. **Local vs. Global Confusion**
Derivative-based sensitivity (local) near $p_0$ says nothing about behavior across the full parameter space. A parameter might be insensitive locally but critical elsewhere.

**Better approach**: Perform sensitivity over the realistic operating range, not just infinitesimal perturbations.

### 3. **Neglecting Scale**
Raw derivative $\frac{\partial Y}{\partial p}$ depends on units. Comparing sensitivities of different parameters requires normalization.

**Mistake example**: Concluding that $\frac{\partial T}{\partial \alpha} = 100 \, \text{s}$ is "more sensitive" than $\frac{\partial T}{\partial \beta} = 50 \, \text{s}$ without checking parameter ranges and output magnitude.

### 4. **Not Accounting for Correlations**
In real systems, parameter variations are often correlated (e.g., temperature and material properties). Independent sensitivity analysis can be misleading.

### 5. **Over-Interpreting Flat Sensitivity**
The HyperMotivo example shows $T(\alpha)/T(\alpha^*) \approx 1$ across a wide range, suggesting "not finely-tuned." However, this could also indicate:
- The algorithm is insensitive and $\alpha$ doesn't matter (not necessarily good)
- The measurements have high noise
- The parameter truly is robust

**Better practice**: Combine with other analyses (e.g., profiling, theoretical complexity analysis) to interpret results.

## See Also

- [[Parameter Tuning / Hyperparameter Optimization]] – Methods