# Chernoff bounds

## Definition

**Chernoff bounds** are concentration inequalities that quantify the probability that a sum of independent random variables deviates significantly from its expected value. They provide exponentially decreasing tail bounds, making them among the tightest concentration results for sums of independent random variables.

Specifically, Chernoff bounds apply to sums of independent Bernoulli random variables and provide separate bounds for upper and lower tail deviations. These bounds are fundamental in probability theory and form the foundation for analyzing randomized algorithms and probabilistic data structures.

## Key Equations

### Standard Chernoff Bounds (Bernoulli Case)

Let $X = \sum_{i=1}^{n} X_i$ where $X_i \in \{0,1\}$ are independent random variables, and let $\mu = \mathbb{E}[X]$.

**Upper tail bound** (for $\delta \geq 0$):
$$\Pr[X \geq (1 + \delta)\mu] \leq \exp\left(-\frac{\delta^2 \mu}{2 + \delta}\right)$$

**Lower tail bound** (for $\delta \in [0,1]$):
$$\Pr[X \leq (1 - \delta)\mu] \leq \exp\left(-\frac{\delta^2 \mu}{2}\right)$$

### Chernoff Bounds for Geometric Random Variables

Let $G_1, \ldots, G_r$ be independent with $G_i \sim \text{Geom}(p)$ and $G = \sum_{i=1}^{r} G_i$. Then for $\lambda \geq 1$:

$$\Pr[G \geq \lambda \cdot \mathbb{E}[G]] \leq \exp\left(-\frac{(\lambda-1)^2}{2\lambda} r\right)$$

This extends Chernoff bounds beyond Bernoulli variables to geometric distributions, useful in analyzing randomized algorithms with variable iteration counts.

## Physical Intuition / Derivation

### Why Exponential Bounds?

The remarkable power of Chernoff bounds comes from the **moment generating function** approach. Rather than directly analyzing $\Pr[X \geq (1+\delta)\mu]$, we use Markov's inequality on an exponentially scaled version:

$$\Pr[X \geq t] = \Pr[e^{sX} \geq e^{st}] \leq \frac{\mathbb{E}[e^{sX}]}{e^{st}}$$

for any $s > 0$. Since the $X_i$ are independent:
$$\mathbb{E}[e^{sX}] = \prod_{i=1}^{n} \mathbb{E}[e^{sX_i}]$$

For Bernoulli variables with $p_i = \Pr[X_i = 1]$:
$$\mathbb{E}[e^{sX_i}] = 1 - p_i + p_i e^s = 1 + p_i(e^s - 1)$$

Optimizing over $s$ yields the exponential decay in $\delta^2 \mu$.

### Intuition

- The bounds **tighten exponentially** as $\mu$ increases: with more samples, rare deviations become exponentially less likely
- The numerator $\delta^2 \mu$ combines:
  - **$\delta^2$**: the squared relative deviation from the mean
  - **$\mu$**: the absolute scale of the sum
- The denominator $(2 + \delta)$ or $2$ (in the lower tail) reflects the severity of the deviation

### Key Insight

For small deviations ($\delta \ll 1$), the bounds simplify to approximately $\exp(-\delta^2 \mu / 2)$, showing that the probability decays quadratically in $\delta$ and linearly in the number of trials $\mu$.

## Applications in Engineering

### 1. Randomized Algorithms Analysis
Chernoff bounds are essential for proving high-probability correctness guarantees:
- **Load balancing**: When distributing $n$ jobs randomly among $m$ servers, Chernoff bounds quantify the probability that any server receives more than $(1+\delta) n/m$ jobs
- **Monte Carlo algorithms**: Showing that randomized search or sampling algorithms find correct answers with high probability

### 2. Distributed Computing & Parallel Algorithms
In the cited context (parallel prefix scans, filters, reductions):
- Bound the probability of work imbalance across processors
- Analyze randomized work-stealing schedulers
- Guarantee that parallel primitives complete within expected time with high probability

### 3. Hash Table & Data Structure Design
- **Collision analysis**: With universal hashing (mentioned in source), Chernoff bounds prove that the number of collisions in a hash table with $n$ elements and $m$ slots concentrates around $n^2/(2m)$ with high probability
- **Load factors**: Ensure that no bucket becomes overfull with overwhelming probability

### 4. Network & Communication Systems
- Packet routing: Bound congestion on network links when traffic is routed probabilistically
- Queue analysis: Determine buffer sizes to handle traffic spikes

### 5. Machine Learning & Sampling
- **Union bound + Chernoff**: When selecting a random sample of size $n$ from a population to estimate a property, Chernoff bounds guarantee the sample estimate stays within $\epsilon$ of the true value with high probability

### 6. Randomized Optimization
- Probabilistic algorithms for satisfiability (SAT), coloring, and other NP-hard problems use Chernoff bounds to prove that random restarts/assignments succeed with high probability

## Common Mistakes / Pitfalls

### 1. **Confusing Upper and Lower Bounds**
Students often apply the wrong bound. Remember:
- **Upper tail** ($X \geq (1+\delta)\mu$) uses $(2+\delta)$ in denominator
- **Lower tail** ($X \leq (1-\delta)\mu$) uses $2$ in denominator
- The lower bound requires $\delta \in [0,1]$; the upper bound