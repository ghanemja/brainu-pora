# Composition Theorem

## Definition

The **composition theorem** is a fundamental result in theoretical computer science and statistical learning theory that characterizes how replicability—the ability to produce identical outputs when given the same random seed—composes across multiple sequential problems.

**Formal Statement (Non-Adaptive Case):** Given $k$ independent instances of statistical problems $T_1, T_2, \ldots, T_k$, each solvable with sample complexity $n$ while maintaining $\rho$-replicability, there exists a black-box reduction that solves all $k$ problems jointly with:

- **Sample complexity:** $\tilde{O}(nk)$ (nearly linear in $k$)
- **Replicability guarantee:** $\rho$-replicable for the composed algorithm

**Adaptive Case (Lower Bound):** When problems may depend on outputs of previous rounds or may be drawn from new distributions (adversarially chosen), any $\rho$-replicable algorithm requires sample complexity:

$$m = \Omega(nk^2)$$

This establishes a fundamental separation between the two settings.

## Key Equations

**Non-Adaptive Composition Bound:**
$$\text{SC}_{\text{composed}} = \tilde{O}(n \cdot k)$$

where $n = \text{SC}_{\text{single}}$ and $\tilde{O}$ suppresses polylogarithmic factors.

**Adaptive Composition Lower Bound:**
$$\text{SC}_{\text{adaptive}} = \Omega(n k^2)$$

**Composition Gap (Separation):**
$$\frac{\text{SC}_{\text{adaptive}}}{\text{SC}_{\text{non-adaptive}}} = \Omega(k)$$

This polynomial separation shows that adaptativity fundamentally increases the difficulty of maintaining replicability.

## Physical Intuition / Derivation

### Why Non-Adaptive Composition Works Efficiently

In the non-adaptive case, all $k$ problems are known upfront and independent. The key insight is that **shared randomness can be exploited**: a single random seed can be used to run a replicable subroutine for each problem independently. Since the problems don't depend on each other's outputs, there is no information leakage that would require additional samples to maintain consistency.

Think of it like making $k$ independent bets: once you decide your betting strategy (the random seed), you can apply it to all bets in parallel without any of them interfering with each other. The replicability of the final result follows naturally from the replicability of each component.

**Black-box reduction structure:**
- Take a $\rho$-replicable algorithm $\mathcal{A}$ for a single problem instance
- For problem $i$, run $\mathcal{A}_i$ with the same initial random seed (or derived from a master seed)
- Since each $\mathcal{A}_i$ is replicable and problems are independent, the composition remains replicable
- The factor of $k$ in sample complexity comes from needing $n$ samples for each of the $k$ instances

### Why Adaptive Composition Costs Quadratically

In the adaptive setting, an adversary can craft later problems based on the outputs of earlier ones. This creates a **feedback loop** that threatens replicability:

1. **First problem solved:** Outputs $y_1$ (must be replicable given seed)
2. **Adversary observes $y_1$:** Crafts problem $T_2$ specifically designed to be sensitive to small perturbations in $y_1$
3. **Second problem solved:** Any variation in $y_2$ from replicability failure now depends on the (now-public) output $y_1$
4. **Cascade effect:** Each round must "re-stabilize" the randomness to maintain replicability across all rounds

This requires $\Omega(nk^2)$ samples: roughly $\Omega(nk)$ to solve the problems and another factor of $k$ to ensure the composition itself doesn't drift. The quadratic dependence emerges from having to isolate and protect each round's output against adversarial structure.

## Applications in Engineering

### 1. **Replicable Machine Learning Systems**

In production ML systems, replicability is critical for regulatory compliance, auditing, and debugging. The composition theorem applies directly:

- **Application:** Training an ensemble of $k$ independent ML models on independent subproblems while maintaining reproducibility
- **Benefit:** Near-linear scaling rather than quadratic; enables practical deployment of $k$ models where $k$ is large
- **Example:** In financial risk modeling, composing $k$ independent replicable risk estimation algorithms for different market segments

### 2. **Parallel Best-Arm Identification**

In multi-armed bandit problems repeated in parallel across $k$ independent instances (e.g., A/B testing across $k$ markets):

- **Challenge:** Naive composition of $k$ single-instance algorithms exhibits $\Omega(k^2)$ sample complexity
- **Solution via Composition Theorem:** Direct application yields a black-box algorithm with $\tilde{O}(nk)$ complexity
- **Practical impact:** In replicable reinforcement learning, enables efficient identification of optimal actions across multiple environments without intricate joint exponential mechanisms

### 3. **Distributed Query Processing**

In database systems with $k$ independent query problems:

- **Application:** Process $k$ analytical queries replicably (same results on re-execution with same parameters)
- **Benefit:** Non-adaptive composition guarantees efficient scaling as the number of queries grows
- **Constraint:** If query dependencies exist (adaptive case), must account for $\Omega(k^2)$ overhead

### 4. **Robustness Certification**

In adversarial robustness verification:

- **Setting:** Compose $k$ independent robustness certificates across network layers or perturbation types
- **Application:** Non-adaptive composition provides near-linear certification cost; adaptive adversaries require quadratic resources

### 5. **Statistical Hypothesis Testing**

In multiple comparison problems with sequential decisions:

- **Non-adaptive:** Pre-specified family of $k$ tests with replicable p-value computation scales as $\tilde{O}(nk)$
- **Adaptive:** Data-dependent test selection (e.g., stagewise procedures) exhibits quadratic complexity via composition theorem lower bound

## Common Mistakes / Pitfalls