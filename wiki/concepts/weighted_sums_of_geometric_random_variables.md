# Weighted Sums of Geometric Random Variables

## Definition

A **weighted sum of geometric random variables** is a random variable of the form:

$$S = \sum_{i=1}^{n} w_i X_i$$

where:
- $X_i \sim \text{Geom}(p_i)$ are independent geometric random variables with success probability $p_i$
- $w_i \geq 0$ are non-negative weights
- $S$ represents the total weighted "cost" or "work" when multiple independent geometric processes occur with different probabilities and importance weights

**Geometric random variable:** $X \sim \text{Geom}(p)$ counts the number of trials until the first success in a sequence of independent Bernoulli trials with success probability $p$. Thus $P(X = k) = (1-p)^{k-1}p$ for $k \geq 1$, with $E[X] = 1/p$.

## Key Equations

### First and Second Moments

$$E[S] = \sum_{i=1}^{n} w_i E[X_i] = \sum_{i=1}^{n} \frac{w_i}{p_i}$$

$$\text{Var}(S) = \sum_{i=1}^{n} w_i^2 \text{Var}(X_i) = \sum_{i=1}^{n} w_i^2 \frac{1-p_i}{p_i^2}$$

(by independence)

### Chernoff-Type Tail Bounds

For weighted sums of geometric random variables, effective concentration inequalities require careful analysis. A key result (central to Hutton & Melrod's parallel algorithm analysis) uses **simple tabulation hashing** to derive:

$$P(S > (1+\delta)\mu) \leq \exp\left(-\Omega\left(\frac{\delta^2 \mu^2}{\sum_i w_i^2}\right)\right)$$

for appropriate regimes, where $\mu = E[S]$. The denominator $\sum_i w_i^2$ reflects the variance structure.

### High-Probability Bound

When applied to parallel algorithm analysis with $w_i$ chosen according to graph structure:

$$P(S = O(\mu \log^c n)) = 1 - n^{-\Omega(1)}$$

(whp guarantee) requires $\sum_i w_i^2 = O(\mu^2 / \text{polylog}(n))$.

## Physical Intuition / Derivation

### Why Geometric Variables?

In parallel algorithms, geometric random variables naturally model **random retry patterns**:
- Each processor/thread attempts a task with success probability $p$
- If unsuccessful, it retries independently
- The number of trials until success follows a geometric distribution

### Why Weights?

Different tasks have different costs or priorities:
- In **semisort algorithms**: weights may correspond to element values or bucket depths
- In **graph algorithms**: weights correspond to vertex degrees or cut sizes
- Heavier weights indicate higher-impact or more expensive components

### Building Intuition via Linearity

By linearity of expectation, the expected total work is simply the sum of weighted expectations. However, **concentration** (showing the work stays close to expectation with high probability) is nontrivial because:

1. **Variance can compound:** If even one weight is large (e.g., one vertex has high degree), it can dominate the tail risk
2. **Standard Chernoff bounds may fail:** Classical concentration arguments for sums require bounded random variables or sub-exponential tails; geometric variables have heavy tails
3. **Structure matters:** The specific weight distribution (determined by the problem structure, e.g., graph degree distribution) determines whether concentration is achievable

### Key Insight: Bounded Weights Condition

For effective high-probability bounds, we need:

$$\sum_{i=1}^{n} w_i^2 \ll \left(\sum_{i=1}^{n} w_i\right)^2$$

This holds when weights are **balanced** (no single weight dominates). Hutton & Melrod achieve this via **culled balanced partition**: iteratively remove high-degree vertices until the remaining graph admits balanced random partitions.

## Applications in Engineering

### 1. **Parallel Algorithm Design**
- **Semisort & integer sorting (whp linear work):** Weight = position in array; geometric = retry depth when conflicts occur
- **Graph coloring & MIS:** Weight = degree of vertex; geometric = rounds until successful coloring
- **Load balancing:** Weights model task complexities; geometric models stochastic completion times

### 2. **Work-Efficient Parallel Primitives**
Upgrading from expected to high-probability work bounds in:
- Parallel quicksort with random pivots
- Distributed hash table insertions (retry on collision)
- Randomized load balancing in multi-processor systems

### 3. **Network Algorithms**
- **Distributed coloring/MIS:** Each node attempts to claim its color/independent status; retries if conflicts detected
- **Packet routing:** Model retry delays with geometric distributions; weights = packet priorities or hop counts

### 4. **Monte Carlo Simulations**
When algorithms use **randomized restarts**:
- Number of restarts ~ Geom$(p)$ where $p$ = probability of success per run
- Total work = (work per run) × (number of restarts)
- Multiple independent modules with different success rates

### 5. **Probabilistic Data Structures**
- **Cuckoo hashing:** Retry depth for resolving collisions
- **Skip lists:** Levels traversed with geometric expectations; weights = element importance or access frequency

## Common Mistakes / Pitfalls

### ❌ Mistake 1: Forgetting Variance Dominance
**Wrong:** Assuming $E[S]$ concentration follows from independent $E[X_i]$
**Right:** Must bound $\sum_i w_i^2 \text{Var}(X_i)$, which can be much larger than $(E[S])^2$ if one weight is very large

### ❌ Mistake 2: Applying Chernoff Directly
**Wrong:** Using standard Chernoff/Hoeffding bounds designed for