# Sampling

## Definition

**Sampling** is the process of selecting a representative subset of elements from a larger population or dataset to make inferences about the whole, or to reduce computational burden while maintaining statistical guarantees. In the context provided, sampling is a preliminary data reduction step that enables efficient parallel processing with high-probability performance bounds.

Formally: Given a set $A$ of $n$ elements, we independently include each element in sample $S$ with probability $p_s$. This produces a random subset $S \subseteq A$ where $|S| \approx p_s \cdot n$ in expectation.

## Key Equations

**Sampling Distribution:**
$$\sigma_x \sim \text{Bin}(N_x, p_s)$$
where $\sigma_x$ is the observed count of key $x$ in the sample, and $N_x$ is its true multiplicity.

**Chernoff Bound (Lower Tail):**
$$\Pr[\hat{W} \leq \mu - t] \leq \exp\left(-\frac{t^2}{2\mu}\right)$$
This concentration inequality bounds the probability that a sampled quantity deviates significantly below its expectation.

**Space Allocation Function:**
$$T = \alpha \left(\sum_{x \in H} f(\sigma_x) + \sum_{b \in [B]} f(\sigma_b)\right)$$
where $f(\sigma)$ maps sample counts to allocated space, ensuring $f(s) \lesssim s + O(\log n)$ with high probability.

**Concentration Bound:**
$$p_s f(s) \leq s + 2c\log n + \sqrt{2sc\log n} \quad \text{(Eq. 3.3)}$$

## Physical Intuition / Derivation

### Why Sample?

When processing large datasets (e.g., sorting $n$ records), examining every element may be prohibitive. Sampling provides a *sketch* of the data distribution at cost $O(n \cdot p_s)$, enabling algorithms to make intelligent allocation decisions before full processing.

### The Sampling-then-Allocate Pattern

The source material describes a **parallel semisort** algorithm that exemplifies this pattern:

1. **Sample Phase:** Draw $S$ by including each record independently with probability $p_s$ (typically $p_s = \Theta(\log n / n)$ for heavy-hitter detection).

2. **Inference Phase:** From sample counts $\sigma_x$, estimate true multiplicities $N_x$ and bucket sizes $N_b$.

3. **Allocation Phase:** Pre-allocate output space based on estimates. If $\sigma_x$ is large, allocate enough space to hold all $N_x$ copies with high probability.

### Why Concentration Matters

The key challenge: sample counts $\sigma_x$ are random. Chernoff bounds guarantee that with appropriate choice of $f(\cdot)$:
$$\Pr[\text{allocated space insufficient}] = \Pr[N_x > f(\sigma_x)] \leq n^{-c}$$

By union bound over $n$ keys and $B \leq n$ buckets, the underallocation event fails with probability $O(n^{1-c})$, which vanishes for $c > 1$.

### Total Space Analysis

The allocation function $f$ must satisfy:
$$f(s) = s + O(\log n) + O(\sqrt{s \log n})$$

This "$s$ plus logarithmic overhead" form ensures:
- When $s$ is large (heavy hitters), the dominant term is $s$ itself
- When $s$ is small, the $O(\log n)$ term handles sampling variance
- The algorithm allocates $T = \Theta(n)$ total space with high probability

## Applications in Engineering

### 1. **Parallel Database Query Processing**
Sampling estimates cardinality and value distributions before executing expensive aggregations or joins. Query optimizers use sample-based statistics to choose execution plans.

### 2. **Network Traffic Analysis**
Sample packets (e.g., 1-in-1000) to estimate flow sizes, detect anomalies, and allocate buffer memory in routers without inspecting every packet.

### 3. **MapReduce / Distributed Sorting**
The semisort algorithm is foundational in distributed systems. Samplers determine bucket boundaries for range-partitioning before the shuffle phase, ensuring load balancing.

### 4. **Approximate Nearest Neighbor Search**
Sampling guides construction of search indices (e.g., LSH or hierarchical clustering). Sample-based clustering determines which buckets to allocate.

### 5. **Streaming Algorithms**
When processing infinite or massive data streams (e.g., sensor data), sampling maintains sketches (count-min arrays, HyperLogLog) that fit in memory while approximating aggregate statistics.

### 6. **Statistical Learning & A/B Testing**
Sample user interactions to estimate click-through rates, conversion rates, or feature importance without analyzing entire user bases.

## Common Mistakes / Pitfalls

### 1. **Ignoring Concentration Bounds**
**Mistake:** Assuming $|S| = p_s \cdot n$ exactly, rather than accounting for variance.  
**Correction:** Use Chernoff/Hoeffding bounds. The sample size fluctuates; design algorithms to handle $\Theta(p_s \cdot n \pm O(\sqrt{p_s n \log n}))$.

### 2. **Naive Union Bound Inflation**
**Mistake:** If $n$ is very large (e.g., $10^9$), a union bound over $n$ events with individual failure probability $n^{-2}$ still fails with non-negligible probability.  
**Correction:** Use $p_s = \Theta(\log n / n)$ so that individual failure probabilities are smaller. Ensure union bound gives $n^{-\Omega(1)}$ failures.

### 3. **Underestimating Logarithmic Factors**
**Mistake:** Claiming "sample counts determine space exactly."  
**Correction:** The allocation function $f(\sigma) = \sigma + O(\log^k n)$ carries logarithmic overhead. For small samples, this overhead dominates; algorithms must handle skewed or pathological distributions gracefully.

### 4. **