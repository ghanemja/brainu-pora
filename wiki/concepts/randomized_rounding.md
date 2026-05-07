# randomized rounding

## Definition

**Randomized rounding** is a technique for converting randomized (probabilistic) hypotheses or solutions into deterministic ones while preserving theoretical guarantees on error or objective value. 

In the context of learning theory, a randomized hypothesis outputs a probability distribution over labels rather than a single deterministic label. Randomized rounding converts this distribution into a single deterministic prediction by sampling from the distribution according to some rounding rule, typically with performance guarantees that degrade gracefully.

More broadly in optimization, randomized rounding refers to the conversion of fractional solutions (e.g., from linear programming relaxations) into integral solutions by treating fractional values as probabilities.

## Key Equations

For a randomized hypothesis $h_{\text{rand}}: \mathcal{X} \to [0,1]$ that outputs probability $p(x)$ for positive classification, a natural randomized rounding rule is:

$$\hat{y}(x) = \begin{cases} 1 & \text{with probability } p(x) \\ 0 & \text{with probability } 1-p(x) \end{cases}$$

**Error preservation guarantee** (typical form): If the randomized hypothesis achieves error $\epsilon_{\text{rand}}$, the deterministic hypothesis obtained via randomized rounding achieves error:

$$\epsilon_{\text{det}} \leq O(\epsilon_{\text{rand}})$$

The constant factor depends on problem structure. In the malicious noise setting referenced in the source, randomized rounding achieves error approaching $\frac{1}{2} \cdot \frac{\eta}{1-\eta}$ when the data has no "heavy points" (points that appear with atypical frequency).

## Physical Intuition / Derivation

### Why Randomization Helps

In adversarial/stochastic environments, a deterministic predictor is forced to commit to a single answer at each point. A randomized predictor has more flexibility: it can express *uncertainty* through probability distributions. This is particularly valuable in settings like weather prediction, where saying "60% chance of rain" is more informative than forcing either "rain" or "no rain."

### The Conversion Process

When we have a good randomized hypothesis, we face a practical problem: real systems must output concrete predictions, not probabilities. Randomized rounding bridges this gap via probabilistic derandomization:

1. **Compute randomized hypothesis** $h_{\text{rand}}(x) = p(x)$, which minimizes expected loss over the probability distribution.

2. **Round via sampling**: For each test point, sample the deterministic label from the distribution $p(x)$.

3. **Concentration argument**: By concentration inequalities (e.g., Chernoff bounds), if we test on many points or aggregate predictions, the empirical error of the deterministic version concentrates near the randomized version's expected error.

### Key Insight from Source Material

The source emphasizes a subtle point: in datasets with *no heavy points*, randomized rounding can convert any good randomized hypothesis to a good deterministic one efficiently. Heavy points—those appearing with unusual frequency—are the only obstruction. This means:

- If the adversary or data distribution treats all points roughly equally, randomized rounding works well.
- Adversaries are forced to attack via heavy points if they want to create a gap between randomized and deterministic error.

## Applications in Engineering

### 1. Machine Learning with Uncertainty
- **Robust classifiers**: Convert probabilistic outputs from neural networks or Bayesian classifiers into discrete predictions while maintaining calibration.
- **Adversarial training**: Under malicious label noise (adversary flips up to $\eta$ fraction of labels), randomized rounding enables learners to achieve near-optimal error rates without solving intractable combinatorial problems.

### 2. Combinatorial Optimization
- **Integer programming**: Convert fractional LP relaxations into integral solutions for problems like maximum cut, set cover, and facility location with approximation guarantees.
- **Scheduling**: Round fractional task schedules to integer assignments while bounding makespan increase.

### 3. Online Learning & Control
- **Bandit algorithms**: Balance exploration-exploitation via randomized rounding of confidence intervals.
- **Reinforcement learning**: Convert soft policy distributions (from policy gradient methods) into executable deterministic policies.

### 4. Distributed Systems
- **Distributed consensus**: Randomized rounding of voting probabilities to reach deterministic agreement.
- **Load balancing**: Round fractional task assignments to discrete server assignments while controlling load variance.

## Common Mistakes / Pitfalls

1. **Assuming error is preserved exactly**: Randomized rounding incurs a *factor* degradation in error, not just a constant additive loss. For example, if randomized error is $\epsilon$, deterministic error may be $c \cdot \epsilon$ for some constant $c > 1$.

2. **Forgetting the role of heavy points**: In the malicious noise setting, randomized rounding works only when the data has no dominant points. A small set of frequently-repeated adversarial examples can break the technique entirely.

3. **Confusing rounding with averaging**: Randomized rounding is a *per-instance* random choice, not averaging multiple predictions. Taking the average of deterministic predictions is a different (often weaker) approach.

4. **Ignoring computational cost**: While randomized rounding is theoretically elegant, the underlying randomized hypothesis may require solving hard combinatorial problems. Efficiency depends on how the randomized solution is computed first.

5. **Applying without concentration analysis**: Simply sampling doesn't guarantee good empirical error on finite test sets. Always verify concentration bounds (Chernoff, Hoeffding, etc.) apply to your setting.

## See Also

- [[PAC Learning]] – Probably Approximately Correct framework; randomized rounding improves PAC bounds under noise.
- [[VC Dimension]] – Controls sample complexity; referenced in source theorem statements.
- [[Adversarial Robustness]] – Malicious noise is a formal adversarial model; randomized rounding is a key technique.
- [[Linear Programming Relaxation]] – Source of fractional solutions that randomized rounding converts to integral solutions.
- [[Concentration Inequalities]] – Mathematical foundations for error preservation guarantees.

## Sources

- Primary lecture/paper excerpt on learning with adversarial noise (Section 2.1, malicious noise model)
- Valiant (1985) – Original PAC model definition
- Cesa-Bianchi et al