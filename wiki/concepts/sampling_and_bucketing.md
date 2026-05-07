# Sampling and Bucketing

## Definition

**Sampling and bucketing** is a foundational algorithmic technique that partitions a large dataset into manageable subsets (buckets) by first drawing a small random sample to estimate properties of the full dataset. The sample statistics inform bucket sizing and key classification, allowing divide-and-conquer processing while maintaining high-probability performance bounds.

In the context of the semisort algorithm, sampling and bucketing works as follows:

1. **Sampling phase**: Each record in an input array $A$ of $n$ records is independently sampled with probability $p_s = \Theta(1/\log n)$ into a sample array $S$.

2. **Estimation phase**: The sample is sorted to compute approximate counts $\sigma_x$ for each key $x$ present in $A$.

3. **Classification phase**: Keys are classified as **heavy** if $\sigma_x \geq \tau$ (where $\tau = \Theta(\log n)$ is a threshold), and the remaining keys are **light**. Records are segregated into heavy records array $H$ and light records array $L$.

4. **Bucketing phase**: Light records are distributed across $B = \Theta(n/\log^2 n)$ buckets using a hash function $h: U \to [B]$, where $U$ is the key universe.

## Key Equations

**Sampling probability:**
$$p_s = \Theta\left(\frac{1}{\log n}\right)$$

**Expected sample size:**
$$\mathbb{E}[|S|] = n \cdot p_s = \Theta\left(\frac{n}{\log n}\right)$$

**Heavy key threshold:**
$$\tau = \Theta(\log n)$$

**Number of light buckets:**
$$B = \Theta\left(\frac{n}{\log^2 n}\right)$$

**Destination array allocation:**
$$\text{size}\left(D^H_x\right) = \alpha f(\sigma_x), \quad \text{size}\left(D^L_b\right) = \alpha f(\sigma_b)$$

where $f$ is a carefully chosen allocation function and $\alpha \geq 2$ is a slack factor compensating for estimation error.

**Expected multiplicity bound for light records:**
$$\text{multiplicity}(x \in L) = O(\log^2 n) \text{ whp}$$

## Physical Intuition / Derivation

### Why Sample?

The core insight is that computing exact statistics on a massive array is expensive, but a small *representative* sample allows us to estimate global structure cheaply. Since $p_s = \Theta(1/\log n)$, we examine only $\Theta(n/\log n)$ records—dramatically fewer than $n$—yet obtain statistically sound estimates.

### Why Stratify by Heavy/Light?

Key multiplicity varies wildly in real data. Heavy keys (frequent items) appear $\geq \tau = \Theta(\log n)$ times. For heavy keys:
- We allocate dedicated destination arrays to avoid contention
- Each destination array is guaranteed sufficient capacity (with slack $\alpha$)

Light keys (infrequent items) collectively appear in $L$, and we group them into buckets by hash to exploit locality and amortize costs.

### Why Hash Light Records?

Rather than sorting light records globally (expensive), we partition them into $B$ buckets. Each bucket contains records with diverse keys but similar hash signatures. This:
- Reduces per-bucket size to $\Theta(n/\log^2 n)$ expected
- Enables efficient local processing (e.g., sorting or hash-table insertion) within each bucket
- Parallelizes well—buckets can be processed independently

### High-Probability Analysis

The sample $S$ is large enough ($\Theta(n/\log n)$ records) that:
- Sample counts $\sigma_x$ concentrate around true counts: $\sigma_x = (1 \pm o(1)) \cdot \text{count}(x)$ whp
- Heavy keys are correctly identified
- Light bucket sizes don't exceed allocated capacity $\alpha f(\sigma_b)$ whp

The concentration follows from concentration inequalities (Chernoff bounds) applied to the binomial sampling process.

## Applications in Engineering

### 1. **Parallel Sorting and Semisort**
The semisort problem requires records with equal keys to be contiguous. Sampling and bucketing enables work-efficient parallel algorithms achieving $O(n)$ work and $O(\log^2 n)$ depth whp—crucial for many-core processors.

### 2. **Big Data Processing**
MapReduce and distributed systems use sampling to estimate data skew before partitioning:
- Sample records to identify heavy hitters (frequent keys)
- Allocate more reducers to hot keys
- Distribute light keys across standard reducers

### 3. **Load Balancing**
In parallel computing, tasks with unpredictable cost are sampled to estimate distribution:
- Identify expensive tasks (heavy)
- Assign light tasks uniformly to cores
- Give heavy tasks dedicated processors to avoid bottlenecks

### 4. **Sketching and Streaming Algorithms**
Sampling is fundamental to approximate algorithms:
- Count-min sketch uses hash-bucketing to estimate item frequencies
- Heavy-hitter detection samples incoming streams to identify dominant keys
- Space-efficient frequency estimation relies on bucket-based aggregation

### 5. **Database Query Optimization**
Query planners sample tables to estimate result sizes and selectivity:
- Sample rows to predict distribution of join keys
- Allocate hash table buckets accordingly
- Optimize partition strategies for distributed joins

### 6. **Network Load Balancing**
Routers sample packets to detect traffic patterns:
- Identify heavy flows (source-destination pairs)
- Route heavy flows on dedicated paths
- Distribute light flows through standard load balancers

## Common Mistakes / Pitfalls

### 1. **Incorrect Threshold Design**
Setting $\tau$ too low classifies infrequent keys as heavy, wasting dedicated resources. Setting it too high misses actual heavy keys. The rule $\tau = \Theta(\log n)$ balances false positives and false negatives via concentration bounds.

### 2. **Ignoring Slack Factor**
Forgetting the slack factor $\alpha