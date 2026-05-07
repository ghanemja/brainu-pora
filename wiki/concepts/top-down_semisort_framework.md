# top-down semisort framework

## Definition

The **top-down semisort framework** is a parallel algorithm paradigm for permuting an array of $n$ records such that all records with equal keys become contiguous, without necessarily sorting records with the same key. The framework, originally developed by Gu–Shun–Sun–Blelloch (GSSB), achieves $O(n)$ work with high probability (whp) while maintaining polylogarithmic depth, making it suitable for practical parallel execution.

Formally, given an input array $A$ of $n$ records with keys drawn from an arbitrary universe $U$, semisort produces a permutation of $A$ where:
$$\forall i, j : \text{key}(A[i]) = \text{key}(A[j]) \land i < j \implies \text{key}(A[i]) = \text{key}(A[k]) \text{ for all } i \leq k \leq j$$

## Key Equations

**Sampling probability:**
$$p_s = \Theta\left(\frac{1}{\log n}\right)$$

**Heavy key threshold:**
$$\tau = \Theta(\log n)$$

**Light bucket count:**
$$B = \Theta\left(\frac{n}{\log^2 n}\right)$$

**Destination array allocation function** (used for both heavy and light records):
$$\text{size}(D_x) = \alpha \cdot f(\sigma_x)$$
where $\alpha \geq 2$ is a slack factor and $f$ is a carefully chosen allocation function that maps sample counts to destination sizes.

**Work complexity:**
- **Total work:** $W = O(n)$ whp
- **Total depth (parallel):** $D = O(\log^2 n)$ whp

## Physical Intuition / Derivation

### Why Top-Down?

The framework is "top-down" because it recursively partitions the problem:
1. **Identify problem structure** via sampling (top-level view)
2. **Partition into subproblems** based on key frequency
3. **Solve subproblems independently** with tight work bounds

### The Three-Phase Structure

**Phase 1: Sampling and Bucketing**
The algorithm first takes a representative sample (size $\sim n/\log n$) and sorts it to estimate key multiplicities without fully sorting the input. This gives approximate counts $\sigma_x$ for each key $x$.

*Insight:* Using $p_s = 1/\log n$ samples ensures that with high probability, heavy keys (appearing $\geq \Theta(\log n)$ times) are well-represented while avoiding oversampling.

**Phase 2: Placement**
Heavy keys (frequent keys) and light keys (infrequent keys) are treated separately:
- **Heavy records**: Each distinct heavy key gets its own destination array $D_x^H$ sized based on $\sigma_x$
- **Light records**: Hashed into $B = \Theta(n/\log^2 n)$ buckets to disperse them, preventing any single bucket from becoming too large

*Insight:* The slack factor $\alpha \geq 2$ provides buffer space to absorb variance in placement without causing overflow, ensuring $O(1)$ work per record placement.

**Phase 3: Local Semisorting**
Each destination array (whether for a heavy key or light bucket) is small enough to semisort independently:
- **Heavy keys**: Records with the same key are already in their destination array; no further work needed
- **Light buckets**: Each bucket contains $O(\log^2 n)$ distinct keys, each appearing $\leq O(\log^2 n)$ times; semisorting via hash table insertion followed by radix sort takes $O(m_b)$ work per bucket $b$

*Insight:* By guaranteeing small per-bucket work via careful allocation, the total expected work becomes $\sum_b O(m_b) = O(n)$ in expectation and $O(n)$ whp.

### Why High Probability?

The key technical contribution is **upgrading Phase 3 to high probability**. The main steps are:

1. **Tight size bounds on packed buckets $C_b$**: Each distinct record hashed to bucket $b$ has multiplicity $\leq O(\log^2 n)$ whp, so $|C_b| = O(\log^2 n \cdot \log^2 n) = O(\log^4 n)$ whp
2. **Concentration via Chernoff bounds**: The randomized hash function distributes light records uniformly, so bucket sizes concentrate around their expectation
3. **Union bound over $B$ buckets**: With $B = \Theta(n/\log^2 n)$ buckets, union bounding across all buckets still yields whp guarantees

## Applications in Engineering

### Data Processing and ETL
- **Database systems**: Efficiently grouping records by key in distributed query processing
- **Log aggregation**: Organizing records from distributed systems by source or event type
- **MapReduce shuffle**: Redistributing intermediate key-value pairs before reduce phase

### Load Balancing
- **Task scheduling**: Grouping tasks by resource requirement for balanced allocation
- **Network packet routing**: Organizing packets by destination for batch processing

### Scientific Computing
- **Particle simulations**: Grouping particles by spatial region before local computations
- **Sparse matrix operations**: Organizing matrix elements by row/column for structured processing

### Machine Learning
- **Feature grouping**: Organizing training data samples by categorical feature values
- **Distributed SGD**: Gathering gradients by parameter server before aggregation

### Practical Strengths
- **Polylogarithmic depth**: Suitable for GPUs and FPGA implementations where depth is critical
- **O(n) work**: Optimal scaling with input size, matching lower bounds
- **Practical constants**: Slack factor $\alpha$ can be tuned for specific hardware characteristics

## Common Mistakes / Pitfalls

### 1. Confusing Semisort with Full Sort
**Mistake**: Assuming semisort requires ordering within keys like standard sort.

**Reality**: Semisort only requires *grouping* equal keys; the internal order is irrelevant. This allows skipping expensive comparison-based sorting.

### 