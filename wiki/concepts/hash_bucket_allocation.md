# Hash Bucket Allocation

## Definition

**Hash bucket allocation** is a dynamic memory allocation strategy for hash tables where the size of storage allocated to each bucket (or to each key's associated data) is determined probabilistically based on sampled evidence of its frequency or load. Rather than allocating fixed-size buckets a priori, the allocation adapts to observed demand: buckets expected to receive many items are allocated more space, while light buckets receive minimal allocation.

In the context of parallel semisort algorithms, allocation is computed as:

$$T = \alpha \left( \sum_{x \in H} f(\sigma_x) + \sum_{b \in [B]} f(\sigma_b) \right)$$

where:
- $\sigma_x$ = observed sample count of key $x$ (drawn from $\text{Bin}(N_x, p_s)$)
- $\sigma_b$ = observed sample size of bucket $b$
- $f(\cdot)$ = allocation function mapping observed counts to space budgets
- $\alpha$ = safety factor (overallocation constant)
- $H$ = set of "heavy" keys (high frequency), $[B]$ = set of buckets

## Key Equations

### Chernoff Bound for Underallocation Failure

If $\sigma_x \sim \text{Bin}(N_x, p_s)$ and $f(\sigma) = c\log n + \sqrt{2\sigma c\log n}$, then:

$$\Pr[N_x > f(\sigma_x)] \leq n^{-c}$$

This guarantees that true multiplicity $N_x$ exceeds allocated space $f(\sigma_x)$ with probability at most $n^{-c}$ per key.

### Allocation Function Bound

$$p_s f(s) \leq s + 2c\log n + \sqrt{2sc\log n} \quad \text{for all } s \geq 0 \tag{3.3}$$

This relationship ensures that expected actual load (left side) stays below expected allocated space.

### Total Allocation

$$\Pr[\text{Eunder}] \leq O(n^{1-c})$$

Union bound over $n$ keys and $B \leq n$ buckets ensures underallocation fails with high probability. Total space achieves:

$$T = \Theta(n) \text{ with probability } 1 - n^{-\Omega(1)}$$

### Light Bucket Size Bound

For light records (those in non-heavy buckets):

$$|C_b| = O(\log^4 n) \text{ w.h.p.}$$

where $C_b$ is the set of light records packed into bucket $b$.

## Physical Intuition / Derivation

### Why Adaptive Allocation Matters

In a naive hash table with fixed bucket sizes, either:
1. Buckets overflow (collision chains grow), requiring rehashing
2. We overallocate uniformly, wasting space on light buckets

The key insight: **sample a fraction $p_s$ of items, use sample statistics to predict true frequencies, then allocate conservatively based on high-probability bounds.**

### The Three-Stage Process

**1. Sampling & Estimation**
- Independently sample each input record with probability $p_s$
- Compute sample multiplicities $\sigma_x$ from the sample
- Partition into heavy ($H$: $\sigma_x \geq \tau$) and light ($L$) keys

**2. Conservative Bound via Concentration**
- Use Chernoff lower tail: the true count $N_x$ exceeds the sample by roughly $\sqrt{N_x \log n}$ in the worst case
- Allocate $f(\sigma_x) \approx \sigma_x + \text{(safety margin)}$ to guarantee $N_x \leq f(\sigma_x)$ with high probability
- The function $f(s) = c\log n + \sqrt{2sc\log n}$ adds $\sqrt{2sc\log n}$ headroom proportional to $\sqrt{s}$

**3. Total Space Analysis**
- For heavy keys: few of them exist ($|H| \leq n/\log n$ typically), so $\sum_x f(\sigma_x) = O(n)$
- For light buckets: pack them densely (collision chains of length $O(\log^4 n)$) and use union bound to show rehashing succeeds with O(1) expected attempts
- Total: $T = \Theta(n)$ with high probability, **linear in input size**

### Why Concentration Inequalities Are Essential

Without concentration (Chernoff bounds, Theorem 2.3), we cannot bound allocation failure probability uniformly. A naive approach—allocate based on single observation—would require $\Theta(n \log n)$ space in worst case (tail events). Sampling + concentration trades small sample size for probabilistic guarantees on *all* keys/buckets simultaneously (union bound).

## Applications in Engineering

### 1. **Parallel External Sorting**
- Hash bucket allocation is a core subroutine in the **Parallel Semisort** algorithm (Algorithm 1)
- Allows sorting $n$ records on a parallel machine without knowing key distribution in advance
- Avoids pathological cases (e.g., all keys identical) by adaptive partitioning
- Example: sorting log files, genomic data, or web crawl records where skew is unknown

### 2. **Distributed Hash Tables (DHTs)**
- Systems like **Dynamo**, **Cassandra** use similar ideas to allocate replica storage
- Predict hot keys from sampled request rates; allocate additional cache/storage accordingly
- Prevents cache misses and network bottlenecks on frequently accessed items

### 3. **Memory-Constrained Database Indexes**
- Hash table indexes with bounded memory: allocate bucket slots adaptively to observed key frequencies
- Reduces index size by avoiding uniform over-provisioning for rare keys
- Critical for in-memory databases (Redis, Memcached) with SLA guarantees

### 4. **Network Packet Classification**
- Routers hash packets by flow ID into buckets for load balancing
- Bucket allocation adapts to observed traffic distribution without offline analysis
- Ensures no single bucket overflows despite skewed flow sizes

###