# failure probability

## Definition

**Failure probability** (denoted $\beta$) is the probability that an algorithm produces an incorrect or unreliable output on a given problem instance. It quantifies the upper bound on the likelihood that an algorithm will fail to meet its correctness or performance guarantees.

In the context of **replicable algorithms**, failure probability has a specialized meaning: it is the probability that re-running the same algorithm on a fresh sample drawn from the same distribution—while using *correlated randomness*—produces a *different output* than the original run. An algorithm is $\rho$-replicable with failure probability $\beta$ if:

$$\Pr[\text{output}_1 \neq \text{output}_2] \leq \beta$$

when both runs use the same random seed structure but different data samples, with replicability parameter $\rho$ controlling the correlation strength.

## Key Equations

### Single Algorithm
For a single algorithm $A$ with sample complexity $n_i$, replicability parameter $\rho$, and inherent failure probability $\beta_0$:
- The algorithm succeeds (outputs consistently) with probability $\geq 1 - \beta_0$

### Composition of $k$ Algorithms

When composing $k$ independent replicable algorithms $A_1, \ldots, A_k$, each with failure probability $\beta_0$ and sample complexity $n_j$:

$$n_{\text{composed}} = O\left(\frac{\sum_j n_j}{\rho^2} \operatorname{polylog}\left(\frac{k}{\rho\beta_0}\right)\right)$$

$$\beta_{\text{composed}} = O\left(\frac{k\sqrt{\beta_0 \log k}}{\rho\beta_0}\right) = O\left(\sqrt{\frac{k\beta_0}{\rho^2}} \log k\right)$$

**Key observation:** The failure probability grows as $O(k\sqrt{\beta_0})$ rather than $O(k\beta_0)$ (which would occur under naive composition), but still worse than differential privacy's advanced composition scaling.

### Naive Composition Bound (Lower Bound)
A simple union bound over $k$ independent algorithms gives:
$$\beta_{\text{naive}} = O(k\rho)$$

This is tight for independent problem instances—no refined analysis can improve it.

## Physical Intuition / Derivation

### Why Failure Probability Matters in Composition

Imagine running $k$ algorithms in parallel, each solving a different subproblem. If you re-run all $k$ algorithms with fresh data:
- Each individual algorithm fails to replicate with probability $\beta_0$
- Under independence, the probability that *at least one* fails is roughly $1 - (1-\beta_0)^k \approx k\beta_0$ for small $\beta_0$

**This is the naive union bound:** failure probabilities add linearly when algorithms are independent.

### Why Naive Composition Fails for Replicability

Unlike **differential privacy**—where advanced composition theorems refine the analysis of the same algorithm—replicability has a fundamental barrier:

1. **Differential privacy** measures how much an algorithm's output distribution changes when one data point is replaced. Changing one point affects only local information, so refined composition tracks *cumulative noise propagation*.

2. **Replicability** measures whether the output changes under a *complete resample*. Each algorithm's replication failure is fundamentally tied to sampling variability over the entire dataset. When $k$ algorithms operate independently, their replication errors are statistically independent, making a union bound tight up to constants.

**Resolution:** Rather than refining the naive composition, the algorithm must be redesigned using:
1. Conversion to **perfectly generalizing (PG) algorithms** (which have differential privacy-like guarantees)
2. Composition of PG algorithms (which admits advanced composition)
3. Conversion back to replicable algorithms via **correlated sampling**

### Scaling with Success Probability

A secondary question: if we want lower failure probability (smaller $\beta_0$), how much does sample complexity increase?

**Answer:** For many problems, the dependence is *logarithmic*:
$$n \propto \log\left(\frac{1}{\beta_0}\right)$$

This means boosting $\beta_0 \to (\beta_0/k)^2$ to maintain constant composed failure probability requires only $O(\log k)$ multiplicative overhead in sample complexity.

## Applications in Engineering

### Distributed Machine Learning & Federated Learning
- **Failure probability** quantifies the risk that model outputs diverge across training runs
- Critical for safety-sensitive applications (autonomous vehicles, medical diagnosis)
- Composition bounds ensure system-wide reliability when training multiple models or learning hierarchical tasks

### Signal Processing & Control Systems
- In multi-sensor fusion, each sensor has a failure probability; composition theorems guarantee that aggregated estimates remain stable
- Replication via re-measurement (e.g., repeated radar scans) must remain consistent despite environmental noise

### Software Testing & Verification
- Failure probability bounds are used in Monte Carlo verification of hardware and software
- Composition with test coverage ensures that the probability of undetected bugs decreases as multiple verification passes are composed

### Reinforcement Learning
- Learning composed tasks (subtasks in hierarchical RL) requires failure probability composition
- Each policy must maintain consistency across environment resets and trajectory resampling

### Privacy-Preserving Analytics
- Parallel analysis of sensitive datasets: each query has a failure probability. Composition bounds ensure the aggregate system fails gracefully
- Related to differential privacy guarantees, which share similar composition structures

## Common Mistakes / Pitfalls

1. **Assuming union bound is tight for replicability**
   - *Error:* Concluding that $\beta_{\text{composed}} = O(k\beta_0)$ for replicable algorithms
   - *Correction:* The actual bound is $O(k\sqrt{\beta_0})$ due to the structure of replication failures, which are correlated through the data distribution

2. **Conflating failure probability with error rate**
   - *Error:* Using "failure probability" to mean algorithmic error (e.g., classification error on test data)
   - *Correction:* In replicability, failure probability is about *consistency across reruns*, not accuracy on unseen data

3