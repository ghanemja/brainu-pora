# Concentration Inequality

## Definition

A **concentration inequality** is a probabilistic bound that quantifies how much a random variable deviates from its expected value. Formally, for a random variable $X$ with expectation $E[X]$, a concentration inequality provides an upper bound on the probability that $|X - E[X]|$ exceeds some threshold $t > 0$:

$$\Pr[|X - E[X]| > t] \leq f(t, \text{problem parameters})$$

where $f$ typically decays exponentially in $t^2$ (sub-exponential or exponential concentration). Concentration inequalities are fundamental tools for proving that random processes behave predictably on average, with high probability (w.h.p.).

## Key Equations

### McDiarmid's Inequality (Bounded Differences)

For a function $f: [k]^n \to \mathbb{R}$ where changing one input coordinate changes the output by at most $c_i$:

$$\Pr[|f(Z_1,\ldots,Z_n) - E[f]| > t] \leq 2\exp\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right)$$

### Lipschitz Form (Applied in Source)

If $X_i = f_i(Z_{v_1}, \ldots, Z_{v_n})$ where $f_i$ is Lipschitz with constant $d_v$ (change in one variable causes change $\leq d_v$ in output):

$$\Pr[|X_i - E[X_i]| > t] \leq 2\exp\left(-\frac{t^2}{\sum_v d_v^2}\right)$$

When $\sum_v d_v^2 \leq \Delta(G') \cdot m'$ (graph degree × edge count):

$$\Pr[|X_i - E[X_i]| > t] \leq 2\exp\left(-\frac{t^2}{\Delta(G') \cdot m'}\right)$$

## Physical Intuition / Derivation

Concentration inequalities answer the question: *"If I average over many independent or weakly-dependent random choices, how likely is the result to deviate significantly from the expected value?"*

### Why They Matter

1. **Predictability**: With concentration, randomized algorithms become deterministic in practice—they succeed with overwhelming probability
2. **Local Smoothness**: The key insight is that no single random variable should have disproportionate influence (Lipschitz/bounded differences condition)
3. **Union Bound Compatibility**: Exponential bounds allow union bounds over many events while remaining non-trivial

### Derivation Sketch (McDiarmid)

The proof uses a **martingale** perspective:
- Condition on variables $Z_1, \ldots, Z_i$ sequentially, creating a martingale
- Each step changes the expectation by at most $c_i$ (bounded differences)
- Apply Azuma-Hoeffding inequality to the martingale
- Results in Gaussian-like tail bounds

In the source material, the Lipschitz form arises because:
- Vertex labels $Z_v \in [k]$ assign each vertex to a bucket
- Changing one label affects the output $X_i$ only through incident edges
- Incident edges number $\deg(v)$, so Lipschitz constant is $d_v = \deg(v)$
- Summing squared Lipschitz constants: $\sum_v d_v^2 = \sum_v \deg(v)^2 \leq \Delta(G') \sum_v \deg(v) = 2\Delta(G')m'$

## Applications in Engineering

### Parallel Algorithm Analysis
The source material uses concentration to analyze a **parallel graph partitioning algorithm**:
- Randomly partitions vertices into $k$ buckets
- Uses concentration to prove w.h.p. that cut edges = $O(m/k^2)$
- Enables union bound over $k$ partition classes
- Guarantees linear work, polylogarithmic depth (no bottlenecks)

### Machine Learning
- **Generalization bounds**: Empirical risk concentration around true risk
- **Confidence intervals**: Training/test accuracy concentration
- **Bandit algorithms**: Concentration drives exploration-exploitation tradeoffs

### Network & Distributed Systems
- **Load balancing**: Prove w.h.p. all servers see $\approx$ average load
- **Randomized routing**: Bound queue lengths in packet networks
- **Consensus protocols**: Prove convergence with high probability

### Randomized Algorithms
- **Quicksort analysis**: Pivot selection concentrates runtime
- **Hash tables**: Bucket occupancy concentrates → $O(1)$ access w.h.p.
- **Monte Carlo methods**: Output error concentrates around deterministic value

## Common Mistakes / Pitfalls

### 1. **Ignoring the Lipschitz Constant**
**Mistake**: Applying McDiarmid with wrong bounds on $c_i$.  
**Reality**: Must carefully bound how each variable affects the output. In the source, naively bounding all incident edges gives loose bounds; the algorithm architecture ensures $\Delta(G') \leq m'/(k^4 \log n)$ to tighten them.

### 2. **Forgetting Independence Requirements**
**Mistake**: Applying concentration to highly dependent variables.  
**Reality**: Bounded differences still work with limited dependence (each variable appears in bounded number of differences), but independence helps. If $X_i$ depends on $X_j$ strongly, you must use conditional inequalities.

### 3. **Assuming "High Probability" is Absolute**
**Mistake**: Treating w.h.p. statements as certainties.  
**Reality**: "w.h.p." typically means $1 - 1/n^c$ for constant $c$. For $n = 10^9$, this is $\approx 99.9\%$, not 100%. Always verify probability is acceptable for your application.

### 4. **Threshold Selection Without Justification**
**Mistake**: Choosing $t = \Theta(m'/k^2)$ arbit